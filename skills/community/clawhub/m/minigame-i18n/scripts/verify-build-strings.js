#!/usr/bin/env node
/**
 * 编译产物二次复核脚本
 * 
 * 用途：在用户完成项目编译后，对编译产物（构建输出目录）进行静态扫描，
 *       检查是否仍有未被替换的中文字符串残留。
 *       这是一个可选的二次复核步骤，用于弥补源码替换可能遗漏的文本。
 * 
 * 原理：
 *   - 使用 @babel/parser 解析编译后的 JS 文件，精确提取字符串字面量中的中文
 *   - 递归扫描 JSON 文件中的中文字符串值（包括 Cocos 序列化资源）
 *   - 如果提供了翻译映射表（chinese_map.json 或 text_translations.json），
 *     可以直接对编译产物执行替换
 * 
 * 使用方法：
 *   # 仅扫描（查找残留中文）
 *   node verify-build-strings.js --scan <编译输出目录>
 * 
 *   # 扫描并替换（使用翻译表替换残留中文）
 *   node verify-build-strings.js --scan <编译输出目录> --replace --translations <翻译表路径>
 * 
 *   # 兼容旧用法（传入单个 JS 文件）
 *   node verify-build-strings.js <输入JS文件> [输出JS文件]
 * 
 * 参数：
 *   --scan            扫描模式：扫描指定目录下所有 JS 和 JSON 文件
 *   --replace         替换模式：与 --scan 配合，对找到的中文执行替换
 *   --translations    翻译表路径（text_translations.json 或 chinese_map.json）
 *   --exclude         排除的目录名（逗号分隔，默认：node_modules,.git,outputs）
 *   --output-dir      扫描结果输出目录（默认：<扫描目录>/i18n_verify_outputs）
 *   --target-lang     目标语言代码（读取 text_translations.json 时使用）
 * 
 * 输出文件（在 output-dir 下）：
 *   residual_chinese_strings.json       — 残留中文字符串列表（去重）
 *   residual_chinese_detail.json        — 残留中文字符串明细（带来源文件和类型）
 *   verify_summary.json                 — 复核摘要报告
 *   replace_log.txt                     — 替换日志（仅替换模式）
 */

const fs = require("fs");
const path = require("path");

const lib_parser = require("@babel/parser");
const lib_traverse = require("@babel/traverse").default;
const lib_generator = require("@babel/generator").default;
const lib_types = require("@babel/types");

// =============================================
// 判断字符串是否包含中文字符
// =============================================
function containsChinese(str) {
  return /[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/.test(str);
}

// =============================================
// 工具：安全读取 JSON 文件（容忍 trailing comma）
// =============================================
function readJSONFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) return null;
    const raw = fs.readFileSync(filePath, "utf-8");
    try {
      return JSON.parse(raw);
    } catch (e) {
      // 容错：去除 trailing comma 后重试
      const fixed = raw.replace(/,\s*([\]}])/g, "$1");
      return JSON.parse(fixed);
    }
  } catch (e) {
    console.error(`\n❌ JSON 文件解析失败: ${filePath}`);
    console.error(`   错误: ${e.message}`);
  }
  return null;
}

// =============================================
// 工具：写入 JSON 文件
// =============================================
function writeJSONFile(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
}

// =============================================
// 判断 JSON 是否为 cc.TextAsset 资源
// =============================================
function isTextAssetFile(jsonData) {
  try {
    if (!Array.isArray(jsonData)) return false;
    const typeDefs = jsonData[3];
    if (!Array.isArray(typeDefs)) return false;
    for (const typeDef of typeDefs) {
      if (Array.isArray(typeDef) && typeDef[0] === "cc.TextAsset") {
        return true;
      }
    }
    return false;
  } catch (e) {
    return false;
  }
}

// =============================================
// 判断 JSON 是否为 Cocos 序列化资源（场景/预制体/组件等）
// =============================================
function isCocosSerializedFile(jsonData) {
  try {
    if (!Array.isArray(jsonData)) return false;
    const typeDefs = jsonData[3];
    if (!Array.isArray(typeDefs)) return false;
    for (const typeDef of typeDefs) {
      if (
        Array.isArray(typeDef) &&
        typeof typeDef[0] === "string" &&
        typeDef[0].startsWith("cc.")
      ) {
        return true;
      }
    }
    return false;
  } catch (e) {
    return false;
  }
}

// =============================================
// 判断 JSON 是否含文本组件的 Cocos 序列化文件
// =============================================
function hasCocosTextComponents(jsonData) {
  try {
    if (!Array.isArray(jsonData)) return false;
    const typeDefs = jsonData[3];
    if (!Array.isArray(typeDefs)) return false;
    for (const typeDef of typeDefs) {
      if (Array.isArray(typeDef)) {
        const name = typeDef[0];
        if (name === "cc.Label" || name === "cc.RichText") return true;
      }
    }
    return false;
  } catch (e) {
    return false;
  }
}

// =============================================
// 递归遍历任意 JSON 结构，找出所有含中文的字符串值
// =============================================
function findChineseStringsInJSON(data, results, parentObj, parentKey) {
  if (typeof data === "string") {
    if (containsChinese(data)) {
      // 尝试将字符串作为 JSON 解析（处理嵌套 JSON 字符串）
      let parsed = null;
      try {
        const trimmed = data.trim();
        if (
          (trimmed.startsWith("{") && trimmed.endsWith("}")) ||
          (trimmed.startsWith("[") && trimmed.endsWith("]"))
        ) {
          parsed = JSON.parse(data);
        }
      } catch (e) {
        // 不是合法 JSON，按普通字符串处理
      }

      if (parsed !== null && typeof parsed === "object") {
        const innerResults = [];
        findChineseStringsInJSON(parsed, innerResults, null, null);
        for (const inner of innerResults) {
          results.push({
            value: inner.value,
            parent: inner.parent,
            key: inner.key,
            _nestedJsonParent: parentObj,
            _nestedJsonKey: parentKey,
            _nestedJsonRoot: parsed,
          });
        }
      } else {
        results.push({ value: data, parent: parentObj, key: parentKey });
      }
    }
  } else if (Array.isArray(data)) {
    for (let i = 0; i < data.length; i++) {
      findChineseStringsInJSON(data[i], results, data, i);
    }
  } else if (data !== null && typeof data === "object") {
    for (const key of Object.keys(data)) {
      findChineseStringsInJSON(data[key], results, data, key);
    }
  }
}

// =============================================
// 递归遍历目录，收集所有文件路径
// =============================================
function walkDirSync(dir, fileList, excludeDirs) {
  fileList = fileList || [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (excludeDirs.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDirSync(fullPath, fileList, excludeDirs);
    } else if (entry.isFile()) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

// =============================================
// 处理单个 JS 文件：扫描/替换中文字符串
// =============================================
function processJSFile(filePath, strMap, globalChineseSet, globalDetailRecords, replaceLog, relPath) {
  try {
    const sourceCode = fs.readFileSync(filePath, "utf-8");

    const ast = lib_parser.parse(sourceCode, {
      sourceType: "module",
      plugins: ["jsx", "typescript", "optionalChaining", "nullishCoalescingOperator"],
      errorRecovery: true, // 容错解析，编译产物可能有特殊语法
    });

    let localCount = 0;
    let localReplaced = 0;

    lib_traverse(ast, {
      StringLiteral(pathNode) {
        const { node } = pathNode;
        if (!containsChinese(node.value)) return;

        // 跳过 import/export 中的模块路径
        if (
          pathNode.findParent(
            (p) => p.isImportDeclaration() || p.isExportDeclaration()
          )
        ) {
          return;
        }

        globalChineseSet.add(node.value);
        globalDetailRecords.push({ value: node.value, source: "js", file: relPath });
        localCount++;

        if (strMap && strMap[node.value] !== undefined) {
          replaceLog.push({ file: relPath, from: node.value, to: strMap[node.value] });
          pathNode.replaceWith(lib_types.stringLiteral(strMap[node.value]));
          pathNode.skip();
          localReplaced++;
        }
      },

      TemplateLiteral(pathNode) {
        const { node } = pathNode;
        for (const elem of node.quasis) {
          if (containsChinese(elem.value.raw)) {
            globalChineseSet.add(elem.value.raw);
            globalDetailRecords.push({ value: elem.value.raw, source: "js-template", file: relPath });
            localCount++;
          }
        }
      },
    });

    // 如果有替换，生成新代码并写回
    if (localReplaced > 0 && strMap) {
      const output = lib_generator(
        ast,
        { retainLines: false, concise: false, jsescOption: { minimal: true } },
        sourceCode
      );
      fs.writeFileSync(filePath, output.code, "utf-8");
    }

    return { found: localCount, replaced: localReplaced };
  } catch (e) {
    console.warn(`  ⚠️ JS 解析失败，跳过: ${relPath} (${e.message})`);
    return { found: 0, replaced: 0, error: e.message };
  }
}

// =============================================
// 处理 JSON 文件：扫描/替换中文字符串
// =============================================
function processJSONFile(filePath, jsonData, strMap, globalChineseSet, globalDetailRecords, replaceLog, relPath) {
  const results = [];
  findChineseStringsInJSON(jsonData, results, null, null);
  if (results.length === 0) return { found: 0, replaced: 0 };

  let localReplaced = 0;
  const nestedJsonRoots = new Set();

  // 确定来源类型
  let sourceType = "json";
  if (isTextAssetFile(jsonData)) sourceType = "text-asset";
  else if (hasCocosTextComponents(jsonData)) sourceType = "scene";
  else if (isCocosSerializedFile(jsonData)) sourceType = "cocos-resource";

  for (const item of results) {
    globalChineseSet.add(item.value);
    globalDetailRecords.push({ value: item.value, source: sourceType, file: relPath });

    if (strMap && strMap[item.value] !== undefined) {
      replaceLog.push({ file: relPath, from: item.value, to: strMap[item.value] });
      item.parent[item.key] = strMap[item.value];
      localReplaced++;
      if (item._nestedJsonParent) {
        nestedJsonRoots.add(item);
      }
    }
  }

  // 回写嵌套 JSON 字符串到父节点
  const writtenBack = new Set();
  for (const item of nestedJsonRoots) {
    const key = `${item._nestedJsonParent}|${item._nestedJsonKey}`;
    if (!writtenBack.has(key)) {
      writtenBack.add(key);
      item._nestedJsonParent[item._nestedJsonKey] = JSON.stringify(item._nestedJsonRoot);
    }
  }

  if (localReplaced > 0 && strMap) {
    fs.writeFileSync(filePath, JSON.stringify(jsonData), "utf-8");
  }

  return { found: results.length, replaced: localReplaced };
}

// =============================================
// 加载翻译映射表
// =============================================
function loadTranslationMap(translationsPath, targetLang) {
  if (!translationsPath || !fs.existsSync(translationsPath)) return null;

  const data = readJSONFile(translationsPath);
  if (!data) return null;

  // 格式1：text_translations.json（标准翻译表）
  if (data.translations && Array.isArray(data.translations)) {
    const map = {};
    for (const entry of data.translations) {
      if (entry.source && entry.translations) {
        // 多语言格式
        const target = targetLang && entry.translations[targetLang];
        if (target) {
          map[entry.source] = target;
        }
      } else if (entry.source && entry.target) {
        // 单语言格式
        map[entry.source] = entry.target;
      }
    }
    console.log(`  ✅ 已加载翻译表 (text_translations.json 格式): ${Object.keys(map).length} 条映射`);
    return map;
  }

  // 格式2：chinese_map.json（简单 key-value 映射）
  if (typeof data === "object" && !Array.isArray(data)) {
    // 过滤掉注释键
    const map = {};
    for (const [key, value] of Object.entries(data)) {
      if (!key.startsWith("_")) {
        map[key] = value;
      }
    }
    console.log(`  ✅ 已加载翻译表 (chinese_map.json 格式): ${Object.keys(map).length} 条映射`);
    return map;
  }

  console.warn(`  ⚠️ 无法识别翻译表格式: ${translationsPath}`);
  return null;
}

// =============================================
// 解析命令行参数
// =============================================
function parseArgs(argv) {
  const result = { _positional: [] };
  let i = 0;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const nextArg = argv[i + 1];
      if (nextArg && !nextArg.startsWith("--")) {
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

// =============================================
// 主流程
// =============================================
const args = parseArgs(process.argv.slice(2));

// 新版扫描模式
if (args.scan !== undefined) {
  const scanDir = typeof args.scan === "string" ? path.resolve(args.scan) : process.cwd();
  const doReplace = args.replace === true;
  const translationsPath = args.translations ? path.resolve(args.translations) : null;
  const targetLang = args['target-lang'] || 'en';
  const excludeStr = args.exclude || "node_modules,.git,outputs,i18n_verify_outputs";
  const excludeDirs = new Set(excludeStr.split(",").map(s => s.trim()));
  const outputDir = args['output-dir']
    ? path.resolve(args['output-dir'])
    : path.join(scanDir, "i18n_verify_outputs");

  console.log(`\n🔍 编译产物二次复核`);
  console.log(`   扫描目录: ${scanDir}`);
  console.log(`   模式: ${doReplace ? "扫描 + 替换" : "仅扫描"}`);
  console.log(`   排除目录: ${Array.from(excludeDirs).join(", ")}`);
  console.log(`   输出目录: ${outputDir}`);

  // 确保输出目录存在
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 加载翻译映射表
  let strMap = null;
  if (doReplace && translationsPath) {
    strMap = loadTranslationMap(translationsPath, targetLang);
    if (!strMap) {
      console.error(`❌ 无法加载翻译表: ${translationsPath}`);
      process.exit(1);
    }
  } else if (doReplace) {
    console.warn(`  ⚠️ 替换模式但未指定 --translations，将仅扫描不替换`);
  }

  // 收集所有文件
  const allFiles = walkDirSync(scanDir, [], excludeDirs);
  const jsFiles = allFiles.filter(f => /\.(js|ts)$/i.test(f));
  const jsonFiles = allFiles.filter(f => /\.json$/i.test(f));

  console.log(`\n   扫描文件: JS/TS ${jsFiles.length} 个, JSON ${jsonFiles.length} 个`);
  console.log(`   开始扫描...\n`);

  const globalChineseSet = new Set();
  const globalDetailRecords = [];
  const replaceLog = [];
  let totalJSFound = 0;
  let totalJSReplaced = 0;
  let totalJSONFound = 0;
  let totalJSONReplaced = 0;
  let jsErrors = 0;

  // 1. 扫描 JS 文件
  for (const filePath of jsFiles) {
    const relPath = path.relative(scanDir, filePath);
    const result = processJSFile(filePath, strMap, globalChineseSet, globalDetailRecords, replaceLog, relPath);
    totalJSFound += result.found;
    totalJSReplaced += result.replaced;
    if (result.error) jsErrors++;
    if (result.found > 0) {
      console.log(`  📄 ${relPath}: ${result.found} 处中文${result.replaced > 0 ? `, ${result.replaced} 处已替换` : ""}`);
    }
  }

  // 2. 扫描 JSON 文件
  for (const filePath of jsonFiles) {
    const relPath = path.relative(scanDir, filePath);
    const jsonData = readJSONFile(filePath);
    if (!jsonData) continue;
    const result = processJSONFile(filePath, jsonData, strMap, globalChineseSet, globalDetailRecords, replaceLog, relPath);
    totalJSONFound += result.found;
    totalJSONReplaced += result.replaced;
    if (result.found > 0) {
      console.log(`  📄 ${relPath}: ${result.found} 处中文${result.replaced > 0 ? `, ${result.replaced} 处已替换` : ""}`);
    }
  }

  // 3. 生成结果
  const uniqueStrings = Array.from(globalChineseSet);

  // 残留中文字符串列表
  const residualFile = path.join(outputDir, "residual_chinese_strings.json");
  writeJSONFile(residualFile, uniqueStrings);

  // 残留明细
  const detailFile = path.join(outputDir, "residual_chinese_detail.json");
  writeJSONFile(detailFile, globalDetailRecords);

  // 复核摘要
  const summary = {
    timestamp: new Date().toISOString(),
    scanDir: scanDir,
    mode: doReplace ? "scan_and_replace" : "scan_only",
    targetLang: targetLang,
    translationsFile: translationsPath,
    statistics: {
      totalFiles: jsFiles.length + jsonFiles.length,
      jsFiles: jsFiles.length,
      jsonFiles: jsonFiles.length,
      jsParseErrors: jsErrors,
      totalResidualUnique: uniqueStrings.length,
      totalResidualOccurrences: globalDetailRecords.length,
      jsResidual: totalJSFound,
      jsonResidual: totalJSONFound,
      jsReplaced: totalJSReplaced,
      jsonReplaced: totalJSONReplaced,
      totalReplaced: totalJSReplaced + totalJSONReplaced,
    },
    result: uniqueStrings.length === 0 ? "clean" : (doReplace && uniqueStrings.length - (totalJSReplaced + totalJSONReplaced) === 0 ? "all_replaced" : "has_residual"),
  };
  const summaryFile = path.join(outputDir, "verify_summary.json");
  writeJSONFile(summaryFile, summary);

  // 替换日志
  if (replaceLog.length > 0) {
    const groupByFile = {};
    for (const { file, from, to } of replaceLog) {
      if (!groupByFile[file]) groupByFile[file] = [];
      groupByFile[file].push({ from, to });
    }
    const lines = [];
    for (const [file, entries] of Object.entries(groupByFile)) {
      lines.push(`[${file}]`);
      for (const { from, to } of entries) {
        lines.push(`  ${from} -> ${to}`);
      }
      lines.push("");
    }
    const logFile = path.join(outputDir, "replace_log.txt");
    fs.writeFileSync(logFile, lines.join("\n"), "utf-8");
    console.log(`\n  📝 替换日志: ${logFile}（共 ${replaceLog.length} 条替换）`);
  }

  // 4. 输出摘要
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📊 二次复核结果`);
  console.log(`   扫描文件: ${jsFiles.length + jsonFiles.length} 个（JS/TS ${jsFiles.length} + JSON ${jsonFiles.length}）`);
  if (jsErrors > 0) {
    console.log(`   ⚠️ JS 解析失败: ${jsErrors} 个`);
  }
  console.log(`   残留中文（去重）: ${uniqueStrings.length} 个`);
  console.log(`   残留中文（总计）: ${globalDetailRecords.length} 处`);
  if (doReplace) {
    console.log(`   已替换: ${totalJSReplaced + totalJSONReplaced} 处`);
  }
  console.log(`   结果: ${summary.result === "clean" ? "✅ 无残留中文" : summary.result === "all_replaced" ? "✅ 残留中文已全部替换" : "⚠️ 存在残留中文"}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`\n📄 扫描结果: ${residualFile}`);
  console.log(`📄 明细记录: ${detailFile}`);
  console.log(`📄 复核摘要: ${summaryFile}`);

  if (uniqueStrings.length > 0 && !doReplace) {
    console.log(`\n💡 提示: 如需替换残留中文，请使用:`);
    console.log(`   node verify-build-strings.js --scan "${scanDir}" --replace --translations <翻译表路径> --target-lang ${targetLang}`);
  }

  console.log(`\n✅ 二次复核完成！`);
  process.exit(0);
}

// =============================================
// 兼容旧用法：传入单个 JS 文件
// =============================================
if (args._positional.length < 1) {
  console.log(`
用法:

  📌 推荐用法（扫描编译产物目录）:
    node verify-build-strings.js --scan <编译输出目录>
    node verify-build-strings.js --scan <编译输出目录> --replace --translations <翻译表路径>

  📌 兼容旧用法（处理单个 JS 文件）:
    node verify-build-strings.js <输入JS文件> [输出JS文件]

参数:
  --scan            扫描目录路径
  --replace         启用替换模式（配合 --scan 使用）
  --translations    翻译表文件路径（text_translations.json 或 chinese_map.json）
  --target-lang     目标语言代码（默认: en）
  --exclude         排除的目录名（逗号分隔）
  --output-dir      结果输出目录

工作流:
  1. 完成源码替换后，提醒用户重新编译项目
  2. 用户编译完成后，告知编译输出目录
  3. 使用 --scan 模式扫描编译产物，检查残留中文
  4. 如有残留，使用 --replace 模式补充替换
`);
  process.exit(1);
}

// 兼容模式：处理单个 JS 文件
const inputFile = path.resolve(args._positional[0]);
const dirX = path.dirname(inputFile);
const outputDir = path.join(dirX, "outputs");
const outputFile = args._positional[1]
  ? path.resolve(args._positional[1])
  : inputFile.replace(/\.js\.bak$/, ".js");

// 创建 outputs 目录
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// 如果 chinese_map.json 不存在，生成一个带示例的模板
const mapFilePath = path.join(outputDir, "chinese_map.json");
if (!fs.existsSync(mapFilePath)) {
  const exampleMap = {
    "_注释": "将中文字符串映射为英文翻译，删除此条示例后使用",
    "开始游戏": "Start Game"
  };
  writeJSONFile(mapFilePath, exampleMap);
  console.log(`📝 已生成映射模板: ${mapFilePath}`);
}
const strMap = readJSONFile(mapFilePath);

// 全局去重集合 & 明细记录 & 替换日志
const globalChineseSet = new Set();
const globalDetailRecords = [];
const replaceLog = [];

console.log(`🚀 开始处理（兼容模式）...`);
console.log(`  工作目录: ${dirX}`);
console.log(`  输出目录: ${outputDir}`);
console.log(`  映射文件: ${strMap ? "✅ 已加载 " + mapFilePath : "❌ 未找到 " + mapFilePath}`);

// 预加载所有 JSON 文件
const excludeDirs = new Set(["outputs", "node_modules", ".git"]);
const allFiles = walkDirSync(dirX, [], excludeDirs);
const allJsonFiles = [];
for (const filePath of allFiles) {
  if (!filePath.endsWith(".json")) continue;
  try {
    const raw = fs.readFileSync(filePath, "utf-8");
    const jsonData = JSON.parse(raw);
    const relPath = path.relative(dirX, filePath);
    allJsonFiles.push({ filePath, jsonData, fileName: relPath });
  } catch (e) {
    // 跳过无法解析的文件
  }
}
console.log(`  已加载 JSON 文件: ${allJsonFiles.length} 个`);

// 处理 JS 代码
const relPath = path.relative(dirX, inputFile);
processJSFile(inputFile, strMap, globalChineseSet, globalDetailRecords, replaceLog, relPath);

// 如果有替换，生成 JS 输出
if (strMap && replaceLog.length > 0) {
  // processJSFile 已直接写入文件
  console.log(`\n  ✅ JS 文件已替换并写入: ${outputFile}`);
}

// 处理所有 JSON
for (const { filePath, jsonData, fileName } of allJsonFiles) {
  processJSONFile(filePath, jsonData, strMap, globalChineseSet, globalDetailRecords, replaceLog, fileName);
}

// 汇总输出
const uniqueStrings = Array.from(globalChineseSet);

const allStringsFile = path.join(outputDir, "all_chinese_strings.json");
writeJSONFile(allStringsFile, uniqueStrings);

const detailFile = path.join(outputDir, "all_chinese_strings_detail.json");
writeJSONFile(detailFile, globalDetailRecords);

console.log(`\n========== 汇总 ==========`);
console.log(`  中文字符串总数: ${uniqueStrings.length} 个（全局去重）`);
console.log(`  明细记录条数: ${globalDetailRecords.length} 条（含重复/多来源）`);
console.log(`  去重字符串: ${allStringsFile}`);
console.log(`  明细记录:   ${detailFile}`);

// 生成替换日志
if (replaceLog.length > 0) {
  const groupByFile = {};
  for (const { file, from, to } of replaceLog) {
    if (!groupByFile[file]) groupByFile[file] = [];
    groupByFile[file].push({ from, to });
  }

  const lines = [];
  for (const [file, entries] of Object.entries(groupByFile)) {
    lines.push(`[${file}]`);
    for (const { from, to } of entries) {
      lines.push(`  ${from} -> ${to}`);
    }
    lines.push("");
  }

  const logFile = path.join(outputDir, "replace_log.txt");
  fs.writeFileSync(logFile, lines.join("\n"), "utf-8");
  console.log(`  替换日志: ${logFile}（共 ${replaceLog.length} 条替换）`);
}

console.log(`\n✅ 全部完成！`);
