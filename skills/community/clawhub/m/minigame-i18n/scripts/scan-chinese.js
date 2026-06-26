#!/usr/bin/env node
/**
 * 中文字符串全量扫描脚本 v1.0
 *
 * 功能：对源码进行全量扫描，提取所有包含中文字符的字符串，输出标准化的扫描报告。
 *
 * 整合来源：
 *   - scanner.js  — AST 解析 JS/TS/JSON/Cocos/Unity/C#
 *   - scan_strings.js — scanner.js 的调用包装器
 *   - verify-build-strings.js — @babel/parser 容错 AST 解析（JSX/TS/可选链等）
 *
 * 支持的语言与文件格式：
 *   - JavaScript (.js)    — 双引擎解析：先 esprima，失败降级 @babel/parser（容错模式）
 *   - TypeScript (.ts)    — @typescript-eslint/typescript-estree AST 解析
 *   - JSON (.json)        — json-source-map 精确定位（含 Cocos 序列化资源深度扫描）
 *   - CSV / TSV (.csv, .tsv) — 逐行逐单元格扫描，精确行列定位
 *   - WXML (.wxml)        — 正则扫描标签文本内容和属性值
 *   - HTML (.html, .htm)  — 正则扫描标签文本内容和属性值
 *   - CSS / WXSS (.css, .wxss) — 提取 content 属性中的中文
 *   - Cocos Creator (.prefab, .fire, .scene) — cc.Label / cc.RichText 文本提取
 *   - Unity (.prefab, .asset, .mat, .unity) — m_Text YAML 字段提取
 *   - C# (.cs)            — 正则匹配字符串字面量（含插值和逐字字符串）
 *   - XML (.xml)          — 标签文本内容和属性值扫描
 *   - 纯文本 (.txt)       — 逐行扫描中文
 *   - 媒体文件            — 仅收集路径（.png, .jpg, .mp3 等）
 *
 * 使用方法：
 *   # 扫描项目源码
 *   node scan-chinese.js --project <项目根目录> [--scan-paths src,assets] [--exclude node_modules,.git]
 *
 *   # 扫描编译产物（兼容 verify-build-strings.js 的能力）
 *   node scan-chinese.js --project <编译输出目录> --build-mode
 *
 *   # 输出 scan_report.json 格式
 *   node scan-chinese.js --project <目录> --output <输出路径>
 *
 *   # 仅输出 CSV（兼容 scan_strings.js）
 *   node scan-chinese.js --project <目录> --format csv --output cn.csv
 *
 * 参数：
 *   --project       项目根目录路径（必填）
 *   --scan-paths    要扫描的子目录列表（逗号分隔，默认: .）
 *   --exclude       排除的目录名（逗号分隔，默认: node_modules,.git,build,dist,temp,library,local,i18n）
 *   --engine        游戏引擎（cocos / unity / laya / native，默认: cocos）
 *   --target-ext    仅扫描指定扩展名（逗号分隔，如 .js,.ts,.json）
 *   --output        输出文件路径（默认: scan_result.json）
 *   --format        输出格式: json / csv（默认: json）
 *   --build-mode    编译产物模式（使用 @babel/parser 容错解析，深度 JSON 递归）
 *   --source-lang   源语言（默认: zh-cn，用于过滤字符串）
 *   --verbose       详细输出
 */

const fs = require('fs');
const path = require('path');
const { performance } = require('perf_hooks');
const crypto = require('crypto');

// ============================================================
// 依赖检测与懒加载
// ============================================================
let esprima, tsEstree, jsonSourceMap, babelParser, babelTraverse, papa, yaml;

/**
 * 多路径 require：依次从以下位置尝试加载模块
 *   1. 脚本自身目录的 node_modules（scripts/node_modules/）
 *   2. 脚本父目录的 node_modules（skill 根目录 node_modules/）
 *   3. --project 指定的项目目录的 node_modules
 *   4. Node.js 默认解析路径（全局安装等）
 */
let _extraModulePaths = [];

function _addProjectModulePath(projectDir) {
  if (projectDir) {
    const projNodeModules = path.join(projectDir, 'node_modules');
    if (fs.existsSync(projNodeModules) && !_extraModulePaths.includes(projNodeModules)) {
      _extraModulePaths.push(projNodeModules);
    }
  }
  // 脚本自身所在目录的 node_modules
  const scriptDir = __dirname;
  const scriptNodeModules = path.join(scriptDir, 'node_modules');
  if (fs.existsSync(scriptNodeModules) && !_extraModulePaths.includes(scriptNodeModules)) {
    _extraModulePaths.unshift(scriptNodeModules);
  }
  // 脚本父目录（skill 根目录）的 node_modules
  const parentNodeModules = path.join(scriptDir, '..', 'node_modules');
  if (fs.existsSync(parentNodeModules) && !_extraModulePaths.includes(parentNodeModules)) {
    _extraModulePaths.unshift(parentNodeModules);
  }
}

function tryRequire(name) {
  // 先通过 Node.js 默认解析（包含已注册的 _extraModulePaths）
  try { return require(name); } catch { /* continue */ }
  // 降级：直接用绝对路径拼接尝试（对非 scoped 包有效）
  for (const modPath of _extraModulePaths) {
    try {
      const fullPath = path.join(modPath, name);
      return require(fullPath);
    } catch { /* continue */ }
  }
  return null;
}

function loadDependencies(buildMode, projectDir) {
  // 注册额外的模块搜索路径
  _addProjectModulePath(projectDir);

  // 将额外路径注入到 Node.js 模块解析路径中（支持 scoped 包如 @babel/parser）
  const Module = require('module');
  for (const modPath of _extraModulePaths) {
    if (!Module._nodeModulePaths.__extraPaths) {
      Module._nodeModulePaths.__extraPaths = true;
    }
    // 使用 module.paths 注入（对当前模块生效）
    if (!module.paths.includes(modPath)) {
      module.paths.unshift(modPath);
    }
  }

  esprima = tryRequire('esprima');
  tsEstree = tryRequire('@typescript-eslint/typescript-estree');
  jsonSourceMap = tryRequire('json-source-map');
  babelParser = tryRequire('@babel/parser');
  const babelTraverseModule = tryRequire('@babel/traverse');
  babelTraverse = babelTraverseModule && (babelTraverseModule.default || babelTraverseModule);
  papa = tryRequire('papaparse');
  yaml = tryRequire('yaml');

  if (buildMode) {
    if (!babelParser) {
      console.error('❌ build-mode 需要 @babel/parser。');
      console.error('   请在以下任一位置安装依赖:');
      console.error(`   1. 脚本目录: cd ${__dirname} && npm install`);
      if (projectDir) console.error(`   2. 项目目录: cd ${projectDir} && npm install @babel/parser @babel/traverse --no-save`);
      process.exit(1);
    }
  } else {
    if (!esprima && !babelParser) {
      console.error('❌ 需要至少安装 esprima 或 @babel/parser。');
      console.error('   请在以下任一位置安装依赖:');
      console.error(`   1. 脚本目录（推荐）: cd ${__dirname} && npm install`);
      if (projectDir) console.error(`   2. 项目目录: cd ${projectDir} && npm install esprima @babel/parser @babel/traverse --no-save`);
      console.error('   脚本目录下的 package.json 已包含所有依赖声明，执行 npm install 即可。');
      process.exit(1);
    }
  }

  // 输出依赖加载状态（verbose 模式在调用方打印）
  return {
    esprima: !!esprima,
    tsEstree: !!tsEstree,
    jsonSourceMap: !!jsonSourceMap,
    babelParser: !!babelParser,
    babelTraverse: !!babelTraverse,
    papa: !!papa,
    yaml: !!yaml,
  };
}

// ============================================================
// 中文检测正则
// ============================================================
const CHINESE_REGEX = /[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/;

function containsChinese(str) {
  return CHINESE_REGEX.test(str);
}

// ============================================================
// MD5 哈希
// ============================================================
function md5(str) {
  return crypto.createHash('md5').update(str).digest('hex');
}

// ============================================================
// 媒体文件类型表
// ============================================================
const MEDIA_TYPES = {
  '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
  '.bmp': 'image', '.webp': 'image', '.svg': 'image', '.ico': 'image',
  '.tiff': 'image', '.tif': 'image', '.pvr': 'image', '.pkm': 'image',
  '.astc': 'image', '.ktx': 'image', '.dds': 'image', '.exr': 'image',
  '.hdr': 'image',
  '.mp3': 'audio', '.wav': 'audio', '.ogg': 'audio', '.m4a': 'audio',
  '.mp4': 'video', '.webm': 'video', '.mkv': 'video', '.flv': 'video',
  '.avi': 'video',
};

// 所有扫描支持的代码/数据文件扩展名
const CODE_EXTENSIONS = new Set([
  '.js', '.ts', '.jsx', '.tsx',
  '.json',
  '.csv', '.tsv',
  '.wxml', '.html', '.htm', '.xml',
  '.css', '.wxss', '.scss', '.less',
  '.prefab', '.fire', '.scene', '.asset', '.mat', '.unity',
  '.cs',
  '.txt',
]);

// ============================================================
// 行列定位工具
// ============================================================
function buildLineStarts(text) {
  const starts = [0];
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\n') {
      starts.push(i + 1);
    }
  }
  return starts;
}

function offsetToLineCol(offset, lineStarts) {
  // 二分查找行号
  let lo = 0, hi = lineStarts.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (lineStarts[mid] === offset) { lo = mid; break; }
    if (lineStarts[mid] < offset) {
      if (mid === lineStarts.length - 1 || lineStarts[mid + 1] > offset) { lo = mid; break; }
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  const line = lo;
  const column = offset - lineStarts[line];
  return { line: line + 1, column: column + 1 }; // 1-based
}

// ============================================================
// 判断是否应跳过此文件
// ============================================================
function shouldSkipFile(filePath, excludeDirs) {
  const parts = filePath.split(path.sep);
  for (const part of parts) {
    if (excludeDirs.has(part)) return true;
  }
  return false;
}

// ============================================================
// 递归收集文件
// ============================================================
function walkDir(dir, fileList, excludeDirs) {
  fileList = fileList || [];
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return fileList; }
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (excludeDirs.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(fullPath, fileList, excludeDirs);
    } else if (entry.isFile()) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

// ============================================================
// 核心扫描类
// ============================================================
class ChineseScanner {
  constructor(options = {}) {
    this.baseDir = options.baseDir || process.cwd();
    this.engine = options.engine || 'cocos';
    this.buildMode = options.buildMode || false;
    this.verbose = options.verbose || false;
    this.sourceLang = options.sourceLang || 'zh-cn';
    this.targetExt = options.targetExt ? new Set(options.targetExt) : null;

    // 统计
    this.stats = {
      totalFiles: 0,
      scannedFiles: 0,
      skippedFiles: 0,
      parseErrors: 0,
      byType: {},
    };

    this.fileContent = ''; // 当前文件内容缓存
    this.varIndex = 0;     // 变量占位符索引
  }

  // =========================================
  // 主入口：扫描目录
  // =========================================
  scan(scanPaths, excludePaths) {
    const strings = [];
    const excludeDirs = new Set(excludePaths);
    const startTime = performance.now();

    console.log('🔍 开始全量中文扫描...');
    console.log(`   项目根目录: ${this.baseDir}`);
    console.log(`   扫描路径: ${scanPaths.join(', ')}`);
    console.log(`   排除目录: ${[...excludeDirs].join(', ')}`);
    console.log(`   游戏引擎: ${this.engine}`);
    console.log(`   编译产物模式: ${this.buildMode ? '是' : '否'}`);

    // 收集所有文件
    const allFiles = [];
    for (const sp of scanPaths) {
      const fullScanPath = path.resolve(this.baseDir, sp);
      if (!fs.existsSync(fullScanPath)) {
        console.warn(`   ⚠️ 扫描路径不存在: ${fullScanPath}`);
        continue;
      }
      const stat = fs.statSync(fullScanPath);
      if (stat.isFile()) {
        allFiles.push(fullScanPath);
      } else {
        walkDir(fullScanPath, allFiles, excludeDirs);
      }
    }

    this.stats.totalFiles = allFiles.length;
    console.log(`\n   发现文件: ${allFiles.length} 个`);

    // 按文件类型分组并扫描
    for (const filePath of allFiles) {
      this.scanFile(filePath, strings);
    }

    const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
    console.log(`\n✅ 扫描完成，耗时: ${elapsed}s`);
    console.log(`   扫描文件: ${this.stats.scannedFiles}/${this.stats.totalFiles}`);
    console.log(`   跳过文件: ${this.stats.skippedFiles}`);
    console.log(`   解析错误: ${this.stats.parseErrors}`);
    console.log(`   发现中文字符串: ${strings.length} 条`);

    if (this.verbose) {
      console.log('   按文件类型统计:');
      for (const [ext, count] of Object.entries(this.stats.byType)) {
        console.log(`     ${ext}: ${count} 条`);
      }
    }

    return strings;
  }

  // =========================================
  // 扫描单个文件
  // =========================================
  scanFile(filePath, strings) {
    const ext = path.extname(filePath).toLowerCase();
    const relPath = path.relative(this.baseDir, filePath).replace(/\\/g, '/');

    // 扩展名过滤
    if (this.targetExt && !this.targetExt.has(ext) && !MEDIA_TYPES[ext]) {
      this.stats.skippedFiles++;
      return;
    }

    // 如果未指定 targetExt，检查是否为已知文件类型
    if (!this.targetExt && !CODE_EXTENSIONS.has(ext) && !MEDIA_TYPES[ext]) {
      this.stats.skippedFiles++;
      return;
    }

    const beforeCount = strings.length;

    try {
      if (ext === '.js' || ext === '.jsx') {
        this.scanJavaScript(filePath, relPath, strings);
      } else if (ext === '.ts' || ext === '.tsx') {
        this.scanTypeScript(filePath, relPath, strings);
      } else if (ext === '.json') {
        this.scanJSON(filePath, relPath, strings);
      } else if (ext === '.csv' || ext === '.tsv') {
        this.scanCSV(filePath, relPath, strings, ext === '.tsv');
      } else if (ext === '.wxml' || ext === '.html' || ext === '.htm') {
        this.scanHTML(filePath, relPath, strings);
      } else if (ext === '.xml') {
        this.scanXML(filePath, relPath, strings);
      } else if (ext === '.css' || ext === '.wxss' || ext === '.scss' || ext === '.less') {
        this.scanCSS(filePath, relPath, strings);
      } else if ((this.engine === 'cocos') && (ext === '.prefab' || ext === '.fire' || ext === '.scene')) {
        this.scanCocosScene(filePath, relPath, strings);
      } else if ((this.engine === 'unity') && (ext === '.prefab' || ext === '.asset' || ext === '.mat' || ext === '.unity')) {
        this.scanUnityFile(filePath, relPath, strings);
      } else if (ext === '.cs') {
        this.scanCSharp(filePath, relPath, strings);
      } else if (ext === '.txt') {
        this.scanPlainText(filePath, relPath, strings);
      } else if (MEDIA_TYPES[ext]) {
        this.collectMedia(filePath, relPath, strings, ext);
      } else {
        this.stats.skippedFiles++;
        return;
      }

      this.stats.scannedFiles++;
      const found = strings.length - beforeCount;
      if (found > 0) {
        this.stats.byType[ext] = (this.stats.byType[ext] || 0) + found;
        if (this.verbose) {
          console.log(`  📄 ${relPath}: ${found} 条中文`);
        }
      }
    } catch (e) {
      this.stats.parseErrors++;
      if (this.verbose) {
        console.warn(`  ⚠️ ${relPath}: ${e.message}`);
      }
    }
  }

  // =========================================
  // JS 文件扫描
  // =========================================
  scanJavaScript(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');

    // 策略1: 尝试 esprima
    let ast = null;
    if (esprima && !this.buildMode) {
      try {
        ast = esprima.parseScript(this.fileContent, { loc: true, range: true });
      } catch {
        try {
          ast = esprima.parseModule(this.fileContent, { loc: true, range: true });
        } catch {
          ast = null;
        }
      }
    }

    // 策略2: 降级到 @babel/parser（更容错）
    if (!ast && babelParser) {
      try {
        ast = babelParser.parse(this.fileContent, {
          sourceType: 'module',
          plugins: ['jsx', 'typescript', 'optionalChaining', 'nullishCoalescingOperator',
                    'classProperties', 'decorators-legacy', 'dynamicImport',
                    'objectRestSpread', 'exportDefaultFrom', 'exportNamespaceFrom'],
          errorRecovery: true,
          ranges: true,
        });
      } catch (e) {
        throw new Error(`JS 解析失败: ${e.message}`);
      }
    }

    if (!ast) {
      throw new Error('无可用的 JS 解析器');
    }

    // 如果是 babel AST，使用 traverse；否则用递归遍历
    if (babelTraverse && ast.type === 'File') {
      this._traverseBabelAST(ast, relPath, strings);
    } else {
      this.varIndex = 0;
      this._extractStringsFromAST(ast, relPath, strings);
    }
  }

  // =========================================
  // TS 文件扫描
  // =========================================
  scanTypeScript(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');

    let ast = null;

    // 策略1: @typescript-eslint/typescript-estree
    if (tsEstree) {
      try {
        ast = tsEstree.parse(this.fileContent, { filePath, loc: true, range: true });
      } catch {
        ast = null;
      }
    }

    // 策略2: @babel/parser with TS plugin
    if (!ast && babelParser) {
      try {
        ast = babelParser.parse(this.fileContent, {
          sourceType: 'module',
          plugins: ['typescript', 'decorators-legacy', 'classProperties',
                    'optionalChaining', 'nullishCoalescingOperator',
                    'objectRestSpread', 'dynamicImport'],
          errorRecovery: true,
          ranges: true,
        });
      } catch (e) {
        throw new Error(`TS 解析失败: ${e.message}`);
      }
    }

    if (!ast) {
      throw new Error('无可用的 TS 解析器');
    }

    if (babelTraverse && ast.type === 'File') {
      this._traverseBabelAST(ast, relPath, strings);
    } else {
      this.varIndex = 0;
      this._extractStringsFromAST(ast, relPath, strings);
    }
  }

  // =========================================
  // Babel AST 遍历（更精确的节点类型识别）
  // =========================================
  _traverseBabelAST(ast, relPath, strings) {
    const self = this;
    babelTraverse(ast, {
      StringLiteral(pathNode) {
        const { node } = pathNode;
        if (!containsChinese(node.value)) return;

        // 跳过 import/export 路径
        if (pathNode.findParent(p => p.isImportDeclaration() || p.isExportDeclaration())) return;

        const loc = node.loc;
        const range = node.start !== undefined && node.end !== undefined ? [node.start, node.end] : [0, 0];

        strings.push({
          value: node.value,
          filePath: relPath,
          type: 'text',
          line: loc ? loc.start.line : 0,
          column: loc ? loc.start.column : 0,
          loc: loc ? {
            start: { line: loc.start.line, column: loc.start.column },
            end: { line: loc.end.line, column: loc.end.column },
          } : { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range,
          variables: [],
        });
      },

      TemplateLiteral(pathNode) {
        const { node } = pathNode;
        // 检查 quasis 中是否包含中文
        let hasChineseQuasi = false;
        let value = '';
        const variables = [];
        let varIdx = 0;

        for (let i = 0; i < node.quasis.length; i++) {
          const quasi = node.quasis[i];
          if (containsChinese(quasi.value.raw)) hasChineseQuasi = true;
          value += quasi.value.raw;
          if (node.expressions[i]) {
            varIdx++;
            const varPlaceholder = `\${variable${varIdx}}`;
            const exprStart = node.expressions[i].start || 0;
            const exprEnd = node.expressions[i].end || 0;
            const exprCode = self.fileContent.slice(exprStart, exprEnd);
            variables.push({ key: varPlaceholder, code: exprCode });
            value += varPlaceholder;
          }
        }

        if (!hasChineseQuasi) return;

        const loc = node.loc;
        const range = node.start !== undefined && node.end !== undefined ? [node.start, node.end] : [0, 0];

        strings.push({
          value,
          filePath: relPath,
          type: variables.length > 0 ? 'template' : 'text',
          line: loc ? loc.start.line : 0,
          column: loc ? loc.start.column : 0,
          loc: loc ? {
            start: { line: loc.start.line, column: loc.start.column },
            end: { line: loc.end.line, column: loc.end.column },
          } : { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range,
          variables,
        });
      },

      BinaryExpression(pathNode) {
        const { node } = pathNode;
        if (node.operator !== '+') return;

        // 仅处理顶层拼接（避免嵌套重复）
        if (pathNode.parentPath && pathNode.parentPath.isBinaryExpression() &&
            pathNode.parentPath.node.operator === '+') return;

        const parts = self._flattenBinaryExpression(node);
        const hasChinese = parts.some(p => p.isStr && containsChinese(p.value));
        if (!hasChinese) return;

        let combinedValue = '';
        const variables = [];
        let varIdx = 0;
        for (const p of parts) {
          if (p.isStr) {
            combinedValue += p.value;
          } else {
            varIdx++;
            const varPlaceholder = `\${variable${varIdx}}`;
            variables.push({ key: varPlaceholder, code: p.code });
            combinedValue += varPlaceholder;
          }
        }

        const loc = node.loc;
        const range = node.start !== undefined && node.end !== undefined ? [node.start, node.end] : [0, 0];

        strings.push({
          value: combinedValue,
          filePath: relPath,
          type: 'concatenation',
          line: loc ? loc.start.line : 0,
          column: loc ? loc.start.column : 0,
          loc: loc ? {
            start: { line: loc.start.line, column: loc.start.column },
            end: { line: loc.end.line, column: loc.end.column },
          } : { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range,
          variables,
          originalExpression: self.fileContent.slice(range[0], range[1]),
        });
      },
    });
  }

  _flattenBinaryExpression(node) {
    if (node.type === 'BinaryExpression' && node.operator === '+') {
      return [...this._flattenBinaryExpression(node.left), ...this._flattenBinaryExpression(node.right)];
    }
    if (node.type === 'StringLiteral' || (node.type === 'Literal' && typeof node.value === 'string')) {
      return [{ isStr: true, value: node.value }];
    }
    if (node.type === 'TemplateLiteral') {
      let val = '';
      for (const q of node.quasis) val += q.value.raw;
      return [{ isStr: true, value: val }];
    }
    const start = node.start || (node.range ? node.range[0] : 0);
    const end = node.end || (node.range ? node.range[1] : 0);
    return [{ isStr: false, code: this.fileContent.slice(start, end) }];
  }

  // =========================================
  // 通用 AST 递归遍历（esprima / ts-estree）
  // =========================================
  _extractStringsFromAST(node, relPath, strings) {
    if (!node || typeof node !== 'object') return;

    if (node.type === 'Literal' && typeof node.value === 'string') {
      if (containsChinese(node.value)) {
        strings.push({
          value: node.value,
          filePath: relPath,
          type: 'text',
          line: node.loc ? node.loc.start.line : 0,
          column: node.loc ? node.loc.start.column : 0,
          loc: node.loc || { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range: node.range || [0, 0],
          variables: [],
        });
      }
      return;
    }

    if (node.type === 'TemplateLiteral') {
      let value = '';
      const variables = [];
      let hasChineseContent = false;

      node.quasis.forEach((quasi, index) => {
        const raw = quasi.value.raw;
        value += raw;
        if (containsChinese(raw)) hasChineseContent = true;

        if (node.expressions && node.expressions[index]) {
          this.varIndex++;
          const varPlaceholder = `\${variable${this.varIndex}}`;
          const expr = node.expressions[index];
          const exprCode = this.fileContent.slice(
            expr.range ? expr.range[0] : 0,
            expr.range ? expr.range[1] : 0
          );
          variables.push({ key: varPlaceholder, code: exprCode });
          value += varPlaceholder;
        }
      });

      if (hasChineseContent) {
        strings.push({
          value,
          filePath: relPath,
          type: variables.length > 0 ? 'template' : 'text',
          line: node.loc ? node.loc.start.line : 0,
          column: node.loc ? node.loc.start.column : 0,
          loc: node.loc || { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range: node.range || [0, 0],
          variables,
        });
      }
      return;
    }

    if (node.type === 'BinaryExpression' && node.operator === '+') {
      const combined = this._combineStrings(node, relPath);
      if (combined && combined.isStr && containsChinese(combined.data.value)) {
        combined.data.loc = node.loc || { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } };
        combined.data.range = node.range || [0, 0];
        strings.push(combined.data);
        return;
      }
    }

    // 递归子节点
    for (const key in node) {
      if (key === 'loc' || key === 'range' || key === 'parent') continue;
      const child = node[key];
      if (Array.isArray(child)) {
        for (const item of child) {
          if (item && typeof item === 'object' && item.type) {
            this._extractStringsFromAST(item, relPath, strings);
          }
        }
      } else if (child && typeof child === 'object' && child.type) {
        this._extractStringsFromAST(child, relPath, strings);
      }
    }
  }

  _combineStrings(node, relPath) {
    if (node.type === 'Literal' && typeof node.value === 'string') {
      return {
        isStr: true,
        data: {
          value: node.value,
          filePath: relPath,
          type: 'text',
          line: node.loc ? node.loc.start.line : 0,
          column: node.loc ? node.loc.start.column : 0,
          variables: [],
        },
      };
    }
    if (node.type === 'BinaryExpression' && node.operator === '+') {
      const left = this._combineStrings(node.left, relPath);
      const right = this._combineStrings(node.right, relPath);
      if (left && right) {
        return {
          isStr: left.isStr || right.isStr,
          data: {
            value: `${left.data.value}${right.data.value}`,
            filePath: relPath,
            type: 'concatenation',
            line: left.data.line,
            column: left.data.column,
            variables: [...left.data.variables, ...right.data.variables],
          },
        };
      }
      return null;
    }
    if (node.type === 'TemplateLiteral') {
      let value = '';
      const variables = [];
      node.quasis.forEach((quasi, index) => {
        value += quasi.value.raw;
        if (node.expressions && node.expressions[index]) {
          this.varIndex++;
          const varPlaceholder = `\${variable${this.varIndex}}`;
          const expr = node.expressions[index];
          variables.push({
            key: varPlaceholder,
            code: this.fileContent.slice(expr.range ? expr.range[0] : 0, expr.range ? expr.range[1] : 0),
          });
          value += varPlaceholder;
        }
      });
      return {
        isStr: true,
        data: {
          value,
          filePath: relPath,
          type: variables.length > 0 ? 'template' : 'text',
          line: node.loc ? node.loc.start.line : 0,
          column: node.loc ? node.loc.start.column : 0,
          variables,
        },
      };
    }
    // 非字符串表达式 → 变量占位符
    this.varIndex++;
    const exprCode = this.fileContent.slice(
      node.range ? node.range[0] : 0,
      node.range ? node.range[1] : 0
    );
    return {
      isStr: false,
      data: {
        value: `\${variable${this.varIndex}}`,
        filePath: relPath,
        type: 'text',
        line: node.loc ? node.loc.start.line : 0,
        column: node.loc ? node.loc.start.column : 0,
        variables: [{ key: `\${variable${this.varIndex}}`, code: exprCode }],
      },
    };
  }

  // =========================================
  // JSON 文件扫描
  // =========================================
  scanJSON(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');

    // 策略1: json-source-map 精确定位
    if (jsonSourceMap) {
      try {
        const { data, pointers } = jsonSourceMap.parse(this.fileContent);

        // 检查是否为 Cocos 序列化资源（需要深度扫描）
        if (this.buildMode && Array.isArray(data)) {
          this._scanCocosSerializedJSON(data, relPath, strings);
        }

        this._collectJsonStrings(data, pointers, '', relPath, strings);
        return;
      } catch {
        // json-source-map 解析失败，降级
      }
    }

    // 策略2: 普通 JSON.parse + 正则定位
    try {
      let raw = this.fileContent;
      let data;
      try {
        data = JSON.parse(raw);
      } catch {
        // 容错: 去除 trailing comma
        const fixed = raw.replace(/,\s*([\]}])/g, '$1');
        data = JSON.parse(fixed);
      }

      // 深度递归扫描（继承 verify-build-strings.js 的能力）
      if (this.buildMode && Array.isArray(data)) {
        this._scanCocosSerializedJSON(data, relPath, strings);
      }

      this._deepScanJSON(data, relPath, strings, []);
    } catch (e) {
      throw new Error(`JSON 解析失败: ${e.message}`);
    }
  }

  _collectJsonStrings(obj, sourceMap, dataPath, relPath, strings) {
    if (typeof obj === 'string') {
      if (containsChinese(obj)) {
        const locInfo = sourceMap[dataPath];
        if (locInfo && locInfo.value) {
          strings.push({
            value: obj,
            filePath: relPath,
            type: 'text',
            line: locInfo.value.line + 1,
            column: locInfo.value.column + 1,
            loc: {
              start: { line: locInfo.value.line + 1, column: locInfo.value.column + 1 },
              end: { line: locInfo.valueEnd.line + 1, column: locInfo.valueEnd.column + 1 },
            },
            range: [locInfo.value.pos, locInfo.valueEnd.pos],
            variables: [],
          });
        }
      }
    } else if (Array.isArray(obj)) {
      obj.forEach((item, index) => {
        this._collectJsonStrings(item, sourceMap, `${dataPath}/${index}`, relPath, strings);
      });
    } else if (obj && typeof obj === 'object') {
      for (const key in obj) {
        const currentPath = `${dataPath}/${key.replace(/\//g, '~1')}`;
        // 也检查 key 中是否含中文
        if (containsChinese(key)) {
          const locInfo = sourceMap[currentPath];
          if (locInfo && locInfo.key) {
            strings.push({
              value: key,
              filePath: relPath,
              type: 'text',
              line: locInfo.key.line + 1,
              column: locInfo.key.column + 1,
              loc: {
                start: { line: locInfo.key.line + 1, column: locInfo.key.column + 1 },
                end: { line: locInfo.keyEnd.line + 1, column: locInfo.keyEnd.column + 1 },
              },
              range: [locInfo.key.pos, locInfo.keyEnd.pos],
              variables: [],
              context: 'json_key',
            });
          }
        }
        this._collectJsonStrings(obj[key], sourceMap, currentPath, relPath, strings);
      }
    }
  }

  // 深度 JSON 递归扫描（无 source-map 时）
  _deepScanJSON(data, relPath, strings, jsonPath) {
    if (typeof data === 'string') {
      if (containsChinese(data)) {
        // 尝试检测嵌套 JSON 字符串
        let parsed = null;
        try {
          const trimmed = data.trim();
          if ((trimmed.startsWith('{') && trimmed.endsWith('}')) ||
              (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
            parsed = JSON.parse(data);
          }
        } catch { /* 非 JSON */ }

        if (parsed && typeof parsed === 'object') {
          this._deepScanJSON(parsed, relPath, strings, [...jsonPath, '(nested)']);
        } else {
          strings.push({
            value: data,
            filePath: relPath,
            type: 'text',
            line: 0,
            column: 0,
            loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
            range: [0, 0],
            variables: [],
            context: `json_path:${jsonPath.join('/')}`,
          });
        }
      }
    } else if (Array.isArray(data)) {
      for (let i = 0; i < data.length; i++) {
        this._deepScanJSON(data[i], relPath, strings, [...jsonPath, i]);
      }
    } else if (data && typeof data === 'object') {
      for (const key of Object.keys(data)) {
        if (containsChinese(key)) {
          strings.push({
            value: key,
            filePath: relPath,
            type: 'text',
            line: 0, column: 0,
            loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
            range: [0, 0],
            variables: [],
            context: 'json_key',
          });
        }
        this._deepScanJSON(data[key], relPath, strings, [...jsonPath, key]);
      }
    }
  }

  // Cocos 序列化资源扫描（build 产物 JSON 格式）
  _scanCocosSerializedJSON(data, relPath, strings) {
    // Cocos 编译产物格式: [version, uuids, paths, typeDefs, ...]
    if (!Array.isArray(data) || data.length < 5) return;
    const typeDefs = data[3];
    if (!Array.isArray(typeDefs)) return;

    let hasLabel = false;
    for (const td of typeDefs) {
      if (Array.isArray(td) && (td[0] === 'cc.Label' || td[0] === 'cc.RichText')) {
        hasLabel = true;
        break;
      }
    }
    if (!hasLabel) return;

    // 深度递归提取含中文的字符串值
    // 已由 _deepScanJSON 或 _collectJsonStrings 覆盖
  }

  // =========================================
  // CSV / TSV 文件扫描
  // =========================================
  scanCSV(filePath, relPath, strings, isTSV) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    const lineStarts = buildLineStarts(this.fileContent);
    const lines = this.fileContent.split(/\r?\n/);
    const separator = isTSV ? '\t' : ',';

    // 解析表头（检测前3行是否为表头/类型/字段名）
    let dataStartRow = 0;
    if (lines.length >= 3) {
      const row2Cells = this._splitCSVLine(lines[1], separator);
      const typeKeywords = new Set(['number', 'string', 'boolean', 'int', 'float', 'bool', 'double', 'long', 'json', 'array']);
      const isTypeRow = row2Cells.every(cell => typeKeywords.has(cell.trim().toLowerCase()) || cell.trim() === '');
      if (isTypeRow) {
        dataStartRow = 3;
      } else {
        // 检测第1行是否全中文（中文表头）
        const row1Cells = this._splitCSVLine(lines[0], separator);
        const hasChineseHeader = row1Cells.some(cell => containsChinese(cell));
        if (hasChineseHeader) {
          dataStartRow = 1;
        }
      }
    }

    // 获取字段名行（如果有）
    let fieldNames = null;
    if (dataStartRow >= 3 && lines.length >= 3) {
      fieldNames = this._splitCSVLine(lines[2], separator);
    } else if (dataStartRow >= 1 && lines.length >= 1) {
      fieldNames = this._splitCSVLine(lines[0], separator);
    }

    // 扫描表头中的中文（标记为 csv_header）
    for (let rowIdx = 0; rowIdx < dataStartRow && rowIdx < lines.length; rowIdx++) {
      const cells = this._splitCSVLine(lines[rowIdx], separator);
      for (let colIdx = 0; colIdx < cells.length; colIdx++) {
        const cellValue = cells[colIdx].trim();
        if (cellValue && containsChinese(cellValue)) {
          // 计算偏移量
          const lineOffset = lineStarts[rowIdx] || 0;
          const cellOffset = this._getCellOffset(lines[rowIdx], colIdx, separator);

          strings.push({
            value: cellValue,
            filePath: relPath,
            type: 'text',
            line: rowIdx + 1,
            column: cellOffset + 1,
            loc: {
              start: { line: rowIdx + 1, column: cellOffset + 1 },
              end: { line: rowIdx + 1, column: cellOffset + cellValue.length + 1 },
            },
            range: [lineOffset + cellOffset, lineOffset + cellOffset + cellValue.length],
            variables: [],
            context: 'csv_header',
          });
        }
      }
    }

    // 扫描数据行中的中文
    for (let rowIdx = dataStartRow; rowIdx < lines.length; rowIdx++) {
      const line = lines[rowIdx];
      if (!line.trim()) continue; // 跳过空行

      const cells = this._splitCSVLine(line, separator);
      for (let colIdx = 0; colIdx < cells.length; colIdx++) {
        const cellValue = cells[colIdx].trim();
        if (!cellValue) continue;
        if (!containsChinese(cellValue)) continue;

        // 跳过纯数字和看起来像 ID 的字段
        if (/^\d+$/.test(cellValue)) continue;
        if (/^[\w#_]+$/.test(cellValue) && !containsChinese(cellValue)) continue;

        const lineOffset = lineStarts[rowIdx] || 0;
        const cellOffset = this._getCellOffset(line, colIdx, separator);
        const fieldName = fieldNames && colIdx < fieldNames.length ? fieldNames[colIdx].trim() : `col_${colIdx}`;

        strings.push({
          value: cellValue,
          filePath: relPath,
          type: 'text',
          line: rowIdx + 1,
          column: cellOffset + 1,
          loc: {
            start: { line: rowIdx + 1, column: cellOffset + 1 },
            end: { line: rowIdx + 1, column: cellOffset + cellValue.length + 1 },
          },
          range: [lineOffset + cellOffset, lineOffset + cellOffset + cellValue.length],
          variables: [],
          context: `csv_data:${fieldName}`,
        });
      }
    }
  }

  _splitCSVLine(line, separator) {
    // 简单 CSV 解析（支持双引号包裹含分隔符的值）
    const cells = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (inQuotes) {
        if (ch === '"') {
          if (i + 1 < line.length && line[i + 1] === '"') {
            current += '"';
            i++;
          } else {
            inQuotes = false;
          }
        } else {
          current += ch;
        }
      } else {
        if (ch === '"') {
          inQuotes = true;
        } else if (ch === separator) {
          cells.push(current);
          current = '';
        } else {
          current += ch;
        }
      }
    }
    cells.push(current);
    return cells;
  }

  _getCellOffset(line, colIdx, separator) {
    // 计算第 colIdx 个单元格在行中的字符偏移
    let cellCount = 0;
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      if (cellCount === colIdx) return i;
      const ch = line[i];
      if (inQuotes) {
        if (ch === '"') {
          if (i + 1 < line.length && line[i + 1] === '"') { i++; }
          else { inQuotes = false; }
        }
      } else {
        if (ch === '"') { inQuotes = true; }
        else if (ch === separator) { cellCount++; }
      }
    }
    return line.length;
  }

  // =========================================
  // HTML / WXML 文件扫描
  // =========================================
  scanHTML(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    const lineStarts = buildLineStarts(this.fileContent);

    // 1. 扫描标签文本内容（排除 <script> 和 <style> 块中的非文本部分）
    // 匹配 >文本内容< 之间的中文
    const textRegex = />([^<]*[\u4e00-\u9fff\u3400-\u4dbf][^<]*)</g;
    let match;
    while ((match = textRegex.exec(this.fileContent)) !== null) {
      const text = match[1].trim();
      if (!text || !containsChinese(text)) continue;

      const offset = match.index + 1; // +1 跳过 >
      const pos = offsetToLineCol(offset, lineStarts);

      strings.push({
        value: text,
        filePath: relPath,
        type: 'text',
        line: pos.line,
        column: pos.column,
        loc: {
          start: { line: pos.line, column: pos.column },
          end: { line: pos.line, column: pos.column + text.length },
        },
        range: [offset, offset + text.length],
        variables: [],
        context: 'html_text',
      });
    }

    // 2. 扫描属性值中的中文
    // 匹配 attr="包含中文的值" 或 attr='包含中文的值'
    const attrRegex = /\b(placeholder|title|alt|label|content|value|aria-label|data-text)\s*=\s*(['"])((?:(?!\2).)*[\u4e00-\u9fff\u3400-\u4dbf](?:(?!\2).)*)\2/gi;
    while ((match = attrRegex.exec(this.fileContent)) !== null) {
      const text = match[3].trim();
      if (!text || !containsChinese(text)) continue;

      const offset = match.index + match[0].indexOf(match[3]);
      const pos = offsetToLineCol(offset, lineStarts);

      strings.push({
        value: text,
        filePath: relPath,
        type: 'text',
        line: pos.line,
        column: pos.column,
        loc: {
          start: { line: pos.line, column: pos.column },
          end: { line: pos.line, column: pos.column + text.length },
        },
        range: [offset, offset + text.length],
        variables: [],
        context: `html_attr:${match[1]}`,
      });
    }
  }

  // =========================================
  // XML 文件扫描
  // =========================================
  scanXML(filePath, relPath, strings) {
    // XML 扫描逻辑与 HTML 类似
    this.scanHTML(filePath, relPath, strings);
  }

  // =========================================
  // CSS / WXSS 文件扫描
  // =========================================
  scanCSS(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    const lineStarts = buildLineStarts(this.fileContent);

    // 提取 content 属性中的中文
    const contentRegex = /content\s*:\s*(['"])((?:(?!\1).)*[\u4e00-\u9fff\u3400-\u4dbf](?:(?!\1).)*)\1/gi;
    let match;
    while ((match = contentRegex.exec(this.fileContent)) !== null) {
      const text = match[2].trim();
      if (!text || !containsChinese(text)) continue;

      const offset = match.index + match[0].indexOf(match[2]);
      const pos = offsetToLineCol(offset, lineStarts);

      strings.push({
        value: text,
        filePath: relPath,
        type: 'text',
        line: pos.line,
        column: pos.column,
        loc: {
          start: { line: pos.line, column: pos.column },
          end: { line: pos.line, column: pos.column + text.length },
        },
        range: [offset, offset + text.length],
        variables: [],
        context: 'css_content',
      });
    }

    // 也扫描 font-family 中的中文字体名
    const fontRegex = /font-family\s*:\s*[^;]*([\u4e00-\u9fff\u3400-\u4dbf]+[^;]*)/gi;
    while ((match = fontRegex.exec(this.fileContent)) !== null) {
      const text = match[1].trim();
      if (!text || !containsChinese(text)) continue;

      const offset = match.index + match[0].indexOf(match[1]);
      const pos = offsetToLineCol(offset, lineStarts);

      strings.push({
        value: text,
        filePath: relPath,
        type: 'text',
        line: pos.line,
        column: pos.column,
        loc: {
          start: { line: pos.line, column: pos.column },
          end: { line: pos.line, column: pos.column + text.length },
        },
        range: [offset, offset + text.length],
        variables: [],
        context: 'css_font_family',
      });
    }
  }

  // =========================================
  // Cocos Creator Scene / Prefab 文件扫描
  // =========================================
  scanCocosScene(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    try {
      const data = JSON.parse(this.fileContent);
      if (!Array.isArray(data)) return;

      for (const item of data) {
        if (!item || typeof item !== 'object') continue;

        // cc.Label
        if (item.__type__ === 'cc.Label' && item._string && containsChinese(item._string)) {
          strings.push({
            value: item._string,
            filePath: relPath,
            type: 'text',
            line: 0, column: 0,
            loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
            range: [0, 0],
            variables: [],
            context: 'cocos_label',
          });
        }

        // cc.RichText
        if (item.__type__ === 'cc.RichText' && item._N$string && containsChinese(item._N$string)) {
          strings.push({
            value: item._N$string,
            filePath: relPath,
            type: 'text',
            line: 0, column: 0,
            loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
            range: [0, 0],
            variables: [],
            context: 'cocos_richtext',
          });
        }
      }
    } catch (e) {
      throw new Error(`Cocos 场景文件解析失败: ${e.message}`);
    }
  }

  // =========================================
  // Unity 文件扫描
  // =========================================
  scanUnityFile(filePath, relPath, strings) {
    if (!yaml) {
      if (this.verbose) console.warn(`  ⚠️ 跳过 Unity 文件（需要 yaml 库）: ${relPath}`);
      return;
    }

    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    try {
      const docs = yaml.parseAllDocuments(this.fileContent);
      for (const doc of docs) {
        if (!doc.contents || !doc.contents.items) continue;
        for (const pair of doc.contents.items) {
          this._findUnityMText(pair, relPath, strings);
        }
      }
    } catch (e) {
      throw new Error(`Unity 文件解析失败: ${e.message}`);
    }
  }

  _findUnityMText(node, relPath, strings) {
    if (node.key && node.key.value === 'm_Text') {
      const val = `${node.value.value}`;
      if (containsChinese(val)) {
        strings.push({
          value: val,
          filePath: relPath,
          type: 'text',
          line: 0, column: 0,
          loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
          range: node.value.range ? [node.value.range[0], node.value.range[1]] : [0, 0],
          variables: [],
          context: 'unity_m_text',
        });
      }
    }
    if (node.value && node.value.items) {
      for (const pair of node.value.items) {
        this._findUnityMText(pair, relPath, strings);
      }
    }
  }

  // =========================================
  // C# 文件扫描
  // =========================================
  scanCSharp(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    const lineStarts = buildLineStarts(this.fileContent);
    const result = [];

    // 正则匹配 C# 字符串字面量（含插值和逐字字符串）
    const baseStringRegex = /('"'|'\\"')|(\/\/[^\r\n]*$|\/\*[\s\S]*?\*\/)|@"((?:\\|""|[^"]|)*?)"|\$@"((?:\\|""|{[^}]+}|[^"]|)*?)|\$"((?:\\\\|\\"|{[^}]+}|[^"])*?)"|"((?:\\\\|\\"|""|[^"])*?)"/gms;

    let match;
    while ((match = baseStringRegex.exec(this.fileContent)) !== null) {
      const [fullMatch, ch, comment, str1, str2, str3, str4] = match;
      if (ch && ch.startsWith("'")) continue;
      if (comment && (comment.startsWith('//') || comment.startsWith('/*'))) continue;

      let content = str1 || str2 || str3 || str4 || '';
      const variables = [];

      // 处理插值变量
      const isInterpolated = fullMatch.startsWith('$');
      if (isInterpolated) {
        content = content.replace(/{([^}]+)}/g, (m, varName) => {
          const idx = variables.length + 1;
          variables.push({ key: `\${variable${idx}}`, code: varName.trim() });
          return `\${variable${idx}}`;
        });
      }

      // 处理转义
      const isVerbatim = fullMatch.startsWith('@') || fullMatch.startsWith('$@');
      if (isVerbatim) {
        content = content.replace(/""/g, '"');
      } else {
        content = content.replace(/\\"/g, '"');
      }

      if (!containsChinese(content)) continue;

      const start = match.index;
      const end = start + fullMatch.length;
      const pos = offsetToLineCol(start, lineStarts);
      const posEnd = offsetToLineCol(end, lineStarts);

      result.push({
        value: content,
        filePath: relPath,
        type: variables.length > 0 ? 'template' : 'text',
        line: pos.line,
        column: pos.column,
        loc: { start: { line: pos.line, column: pos.column }, end: { line: posEnd.line, column: posEnd.column } },
        range: [start, end],
        variables,
      });
    }

    strings.push(...result);
  }

  // =========================================
  // 纯文本文件扫描
  // =========================================
  scanPlainText(filePath, relPath, strings) {
    this.fileContent = fs.readFileSync(filePath, 'utf-8');
    const lineStarts = buildLineStarts(this.fileContent);
    const lines = this.fileContent.split(/\r?\n/);

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line || !containsChinese(line)) continue;

      const lineOffset = lineStarts[i] || 0;
      strings.push({
        value: line,
        filePath: relPath,
        type: 'text',
        line: i + 1,
        column: 1,
        loc: {
          start: { line: i + 1, column: 1 },
          end: { line: i + 1, column: line.length + 1 },
        },
        range: [lineOffset, lineOffset + lines[i].length],
        variables: [],
        context: 'plain_text',
      });
    }
  }

  // =========================================
  // 媒体文件收集
  // =========================================
  collectMedia(filePath, relPath, strings, ext) {
    strings.push({
      value: relPath,
      filePath: relPath,
      type: MEDIA_TYPES[ext],
      line: 0, column: 0,
      loc: { start: { line: 0, column: 0 }, end: { line: 0, column: 0 } },
      range: [0, 0],
      variables: [],
    });
  }
}

// ============================================================
// 过滤：仅保留包含中文的字符串条目
// ============================================================
function filterChineseStrings(strings) {
  return strings.filter(item => {
    if (item.type === 'image' || item.type === 'audio' || item.type === 'video') return false;
    return containsChinese(item.value);
  });
}

// ============================================================
// 去重与生成 key
// ============================================================
function deduplicateAndGenerateKeys(strings) {
  const keyMap = {};

  for (const item of strings) {
    let num = 0;
    while (true) {
      const key = md5(`${item.value}${num}`);
      if (!keyMap[key]) {
        item.key = key;
        keyMap[key] = { value: item.value, type: item.type, associations: [] };
        break;
      } else if (keyMap[key].value === item.value && keyMap[key].type === item.type) {
        item.key = key;
        break;
      } else {
        num++;
      }
    }
    keyMap[item.key].associations.push({
      filePath: item.filePath,
      loc: item.loc,
      range: item.range,
    });
  }

  return strings;
}

// ============================================================
// 输出为 CSV
// ============================================================
function outputCSV(strings, outputPath) {
  const header = 'key,文本,文件路径,行,列,类型,上下文';
  const lines = strings.map(s => {
    const escapeCsv = (val) => {
      const str = `${val}`;
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };
    return [s.key, s.value, s.filePath, s.line, s.column, s.type, s.context || '']
      .map(escapeCsv).join(',');
  });
  const csv = `${header}\n${lines.join('\n')}`;
  fs.writeFileSync(outputPath, csv, 'utf-8');
  console.log(`\n📄 已输出 CSV: ${outputPath} (${strings.length} 条)`);
}

// ============================================================
// 输出为 JSON
// ============================================================
function outputJSON(strings, outputPath, baseDir) {
  const textEntries = strings.filter(s =>
    s.type === 'text' || s.type === 'template' || s.type === 'concatenation'
  );
  const mediaEntries = strings.filter(s =>
    s.type === 'image' || s.type === 'audio' || s.type === 'video'
  );

  const report = {
    version: '1.0',
    projectPath: baseDir,
    sourceLanguage: 'zh-CN',
    scanTime: new Date().toISOString(),
    scanMethod: 'ast_scan',
    summary: {
      totalTextEntries: textEntries.length,
      totalMediaEntries: mediaEntries.length,
      byType: {},
      byFileType: {},
    },
    entries: textEntries,
    mediaEntries: mediaEntries,
  };

  // 统计
  for (const entry of textEntries) {
    report.summary.byType[entry.type] = (report.summary.byType[entry.type] || 0) + 1;
    const ext = path.extname(entry.filePath).toLowerCase();
    report.summary.byFileType[ext] = (report.summary.byFileType[ext] || 0) + 1;
  }

  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2), 'utf-8');
  console.log(`\n📄 已输出 JSON: ${outputPath} (${textEntries.length} 条文本, ${mediaEntries.length} 个媒体文件)`);
}

// ============================================================
// 命令行参数解析
// ============================================================
function parseArgs(argv) {
  const result = { _positional: [] };
  let i = 0;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const nextArg = argv[i + 1];
      if (nextArg && !nextArg.startsWith('--')) {
        result[key] = nextArg;
        i += 2;
      } else {
        result[key] = true;
        i++;
      }
    } else {
      result._positional.push(arg);
      i++;
    }
  }
  return result;
}

// ============================================================
// 主入口
// ============================================================
function main() {
  const args = parseArgs(process.argv.slice(2));

  // 帮助信息
  if (args.help || (!args.project && args._positional.length === 0)) {
    console.log(`
中文字符串全量扫描脚本 v1.0

用法:
  node scan-chinese.js --project <项目根目录> [选项]

选项:
  --project       项目根目录路径（必填）
  --scan-paths    扫描的子目录列表（逗号分隔，默认: .）
  --exclude       排除的目录名（逗号分隔，默认: node_modules,.git,build,dist,temp,library,local,i18n）
  --engine        游戏引擎: cocos / unity / laya / native（默认: cocos）
  --target-ext    仅扫描指定扩展名（逗号分隔，如 .js,.ts,.json）
  --output        输出文件路径（默认: scan_result.json）
  --format        输出格式: json / csv（默认: json）
  --build-mode    编译产物模式（@babel/parser 容错解析）
  --source-lang   源语言（默认: zh-cn）
  --verbose       详细输出
  --help          显示帮助
`);
    process.exit(0);
  }

  const projectDir = path.resolve(args.project || args._positional[0] || '.');
  const scanPathsStr = args['scan-paths'] || '.';
  const scanPaths = scanPathsStr.split(',').map(s => s.trim());
  const excludeStr = args.exclude || 'node_modules,.git,build,dist,temp,library,local,i18n';
  const excludePaths = excludeStr.split(',').map(s => s.trim());
  const engine = args.engine || 'cocos';
  const targetExtStr = args['target-ext'] || '';
  const targetExt = targetExtStr ? targetExtStr.split(',').map(s => s.trim()) : null;
  const outputPath = args.output || path.join(projectDir, 'scan_result.json');
  const format = args.format || 'json';
  const buildMode = args['build-mode'] === true;
  const verbose = args.verbose === true;
  const sourceLang = args['source-lang'] || 'zh-cn';

  if (!fs.existsSync(projectDir)) {
    console.error(`❌ 项目目录不存在: ${projectDir}`);
    process.exit(1);
  }

  // 加载依赖（传入项目目录，支持从项目的 node_modules 中查找）
  const depStatus = loadDependencies(buildMode, projectDir);
  if (verbose) {
    console.log('\n📦 依赖加载状态:');
    for (const [dep, loaded] of Object.entries(depStatus)) {
      console.log(`   ${loaded ? '✅' : '❌'} ${dep}`);
    }
  }

  // 创建扫描器
  const scanner = new ChineseScanner({
    baseDir: projectDir,
    engine,
    buildMode,
    verbose,
    sourceLang,
    targetExt,
  });

  // 执行扫描
  const rawStrings = scanner.scan(scanPaths, excludePaths);

  // 过滤仅中文
  const chineseStrings = filterChineseStrings(rawStrings);

  // 媒体文件（不过滤中文）
  const mediaStrings = rawStrings.filter(s =>
    s.type === 'image' || s.type === 'audio' || s.type === 'video'
  );

  // 合并
  const allStrings = [...chineseStrings, ...mediaStrings];

  // 去重与生成 key
  deduplicateAndGenerateKeys(allStrings);

  // 输出
  if (format === 'csv') {
    outputCSV(chineseStrings, outputPath);
  } else {
    outputJSON(allStrings, outputPath, projectDir);
  }

  // 输出统计
  console.log('\n📊 扫描统计:');
  console.log(`   中文字符串: ${chineseStrings.length} 条`);
  const typeStats = {};
  for (const s of chineseStrings) {
    typeStats[s.type] = (typeStats[s.type] || 0) + 1;
  }
  for (const [type, count] of Object.entries(typeStats)) {
    console.log(`     ${type}: ${count}`);
  }
  console.log(`   媒体文件: ${mediaStrings.length} 个`);
}

// 支持作为模块导出，也支持直接运行
if (require.main === module) {
  main();
} else {
  module.exports = { ChineseScanner, containsChinese, filterChineseStrings, deduplicateAndGenerateKeys };
}
