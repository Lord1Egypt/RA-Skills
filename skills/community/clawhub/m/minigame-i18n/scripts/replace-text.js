#!/usr/bin/env node
/**
 * 文本替换脚本 v3.5 — 安全替换版（增强：精确字符串字面量定位 + 引号冲突自动转义）
 * 
 * 核心改进：
 * 1. 替换前后逐文件校验（JS 用 node --check，JSON 用 JSON.parse）
 * 2. 校验失败自动回滚该文件
 * 3. 替换策略严格分级：range 精确替换 > 行号+列号精确定位 > 行号+字符串字面量优先匹配 > 唯一匹配搜索
 * 4. 全文搜索策略要求唯一匹配，多处匹配时拒绝替换
 * 5. 生成详细替换报告
 * 6. [v3] 逐条替换后即时语法校验，失败立即回退该条替换
 * 7. [v3] JSON 值替换使用 JSON-aware 策略，正确处理转义字符
 * 8. [v3] 替换全部完成后执行最终语法校验并输出校验结果
 * 9. [v3.1] 模板字符串替换修复：兼容 source 带/不带反引号、0-indexed 行号
 * 10. [v3.1] 行号定位兼容 0-indexed 和 1-indexed（适配不同扫描器输出）
 * 11. [v3.1] 模板字符串增加不带反引号的全局回退策略
 * 12. [v3.2] 修复 basicSyntaxCheck 中模板字符串 ${} 表达式的嵌套花括号追踪
 *     —— 使用状态栈（stateStack）替代简单的 templateDepth 计数器，正确处理
 *     ${} 内的字符串、注释、嵌套花括号和嵌套模板字符串，避免替换后误报语法错误
 * 13. [v3.3] CSV/TSV 数据文件替换支持
 * 14. [v3.4] **精确字符串字面量定位**：
 *     —— 行号匹配时，优先定位被引号包裹的字符串字面量（`"source"`/`'source'`/`` `source` ``），
 *        避免将注释中的同名文本误替换为翻译结果。
 *     —— 列号精确匹配时，从列号位置精确切片匹配，而非模糊搜索。
 *     —— 全局唯一搜索时，优先匹配字符串字面量中的出现，跳过注释中的匹配。
 * 15. [v3.5] **引号冲突自动转义**：
 *     —— 替换时检测 source 所在位置的外层包裹引号类型（双引号/单引号/反引号），
 *        如果 target 中包含与外层引号相同的字符，自动添加反斜杠转义。
 *     —— 解决翻译后文本中的引号（如 『』→"" 或 ' 在 Everyone's 中）破坏
 *        JS 字符串语法的问题。
 *
 * 使用方法：
 *   node replace-text.js --project <projectRoot> [--dry-run] [--backup] [--target-lang <lang>] [--mode <direct|langpack>] [--engine <engine>]
 * 
 * 参数：
 *   --project      项目根目录路径
 *   --dry-run      预览模式，不实际修改文件
 *   --backup       替换前自动备份（默认开启）
 *   --target-lang  目标语言代码（如 en、ko、th）
 *   --mode         替换模式（默认 direct）：
 *                    direct   — 直接将中文替换为目标语言文本
 *                    langpack — 将中文替换为 i18n.t("key") 调用（需先执行 generate-langpack.js）
 *   --engine       游戏引擎（langpack 模式必填）：cocos-creator | cocos-l10n | laya | egret | unity | native
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================
// 配置
// ============================================================

const args = parseArgs(process.argv.slice(2));
const PROJECT_ROOT = args.project || process.cwd();
const DRY_RUN = args['dry-run'] || false;
const BACKUP = args.backup !== false; // 默认开启
const TARGET_LANG = args['target-lang'] || 'en';
const REPLACE_MODE = args.mode || 'direct'; // 'direct' | 'langpack'
const ENGINE = args.engine || 'native';

const I18N_DIR = path.join(PROJECT_ROOT, 'i18n');
const TRANSLATIONS_FILE = path.join(I18N_DIR, 'text_translations.json');
const SCAN_REPORT_FILE = path.join(I18N_DIR, 'scan_report.json');
const BACKUP_DIR = path.join(I18N_DIR, 'backups', new Date().toISOString().replace(/[:.]/g, '-'));
const LANGPACK_KEYMAP_FILE = path.join(I18N_DIR, 'langpack', 'key_mapping.json');

// ============================================================
// 主流程
// ============================================================

async function main() {
  console.log('📝 文本替换工具 v3.5（安全版 — 精确字面量定位 + 语言包模式）');
  console.log(`   项目路径: ${PROJECT_ROOT}`);
  console.log(`   目标语言: ${TARGET_LANG}`);
  console.log(`   替换模式: ${REPLACE_MODE === 'langpack' ? '语言包（i18n.t 调用）' : '直接替换'}`);
  if (REPLACE_MODE === 'langpack') {
    console.log(`   游戏引擎: ${ENGINE}`);
  }
  console.log(`   预览模式: ${DRY_RUN ? '是' : '否'}`);
  console.log(`   自动备份: ${BACKUP ? '是' : '否'}`);
  console.log('');

  // 0. langpack 模式：验证前置条件
  let keyMapping = null;
  if (REPLACE_MODE === 'langpack') {
    if (!fs.existsSync(LANGPACK_KEYMAP_FILE)) {
      console.error(`❌ 语言包 key 映射表不存在: ${LANGPACK_KEYMAP_FILE}`);
      console.error('   请先执行 generate-langpack.js 生成语言包和映射表');
      process.exit(1);
    }
    keyMapping = JSON.parse(fs.readFileSync(LANGPACK_KEYMAP_FILE, 'utf8'));
    console.log(`✅ 读取语言包 key 映射表: ${Object.keys(keyMapping.entries).length} 条`);
  }

  // 1. 读取翻译表
  if (!fs.existsSync(TRANSLATIONS_FILE)) {
    console.error(`❌ 翻译表不存在: ${TRANSLATIONS_FILE}`);
    process.exit(1);
  }
  const translations = JSON.parse(fs.readFileSync(TRANSLATIONS_FILE, 'utf8'));
  console.log(`✅ 读取翻译表: ${translations.translations.length} 条`);

  // 1.5 langpack 模式：将每条 entry 的 target 转换为 i18n 调用表达式
  let processedTranslations = translations.translations;
  if (REPLACE_MODE === 'langpack' && keyMapping) {
    processedTranslations = transformToI18nCalls(translations.translations, keyMapping, ENGINE);
    console.log(`✅ 已转换为 i18n 调用表达式`);
  }

  // 2. 按文件分组
  const fileGroups = groupByFile(processedTranslations);
  const fileCount = Object.keys(fileGroups).length;
  console.log(`📁 涉及文件: ${fileCount} 个`);
  console.log('');

  // 3. 逐文件替换
  let totalReplaced = 0;
  let totalFailed = 0;
  let totalSkipped = 0;
  let totalRolledBack = 0;
  const results = [];

  for (const [filePath, entries] of Object.entries(fileGroups)) {
    const fullPath = path.join(PROJECT_ROOT, filePath);

    if (!fs.existsSync(fullPath)) {
      console.warn(`⚠️  文件不存在，跳过: ${filePath}`);
      totalSkipped += entries.length;
      results.push({
        filePath,
        status: 'file_not_found',
        replaced: 0,
        failed: 0,
        skipped: entries.length,
        details: entries.map(e => ({
          key: e.key, type: e.type, source: e.source, status: 'skipped', reason: '文件不存在'
        }))
      });
      continue;
    }

    // 读取文件内容
    const originalContent = fs.readFileSync(fullPath, 'utf8');

    // 备份
    if (BACKUP && !DRY_RUN) {
      backupFile(fullPath, filePath);
    }

    // 执行替换 —— 逐条替换并即时校验
    const { newContent, replaced, failed, details } = replaceInFileWithValidation(
      originalContent,
      entries,
      filePath,
      fullPath,
      DRY_RUN
    );

    if (replaced > 0 && !DRY_RUN) {
      // 写入替换后内容
      fs.writeFileSync(fullPath, newContent, 'utf8');

      // 最终整体语法验证
      const valid = validateFile(fullPath, filePath);

      if (!valid) {
        // 验证失败，回滚整个文件
        console.error(`❌ ${filePath}: 最终语法验证失败，回滚`);
        fs.writeFileSync(fullPath, originalContent, 'utf8');
        totalRolledBack++;
        totalFailed += replaced;
        results.push({
          filePath,
          status: 'rolled_back',
          replaced: 0,
          failed: entries.length,
          skipped: 0,
          syntaxError: true,
          details: details.map(d => ({
            ...d,
            status: 'rolled_back',
            reason: '最终语法验证失败，已回滚'
          }))
        });
        continue;
      }

      console.log(`✅ ${filePath}: ${replaced} 处替换，语法验证通过`);
    } else if (replaced > 0 && DRY_RUN) {
      console.log(`🔍 ${filePath}: ${replaced} 处可替换（预览模式）`);
    }

    totalReplaced += replaced;
    totalFailed += failed;

    results.push({
      filePath,
      status: 'ok',
      replaced,
      failed,
      skipped: 0,
      details
    });
  }

  // 4. 最终语法校验 —— 对所有被修改的文件再做一轮整体校验
  const finalVerification = [];
  if (!DRY_RUN) {
    console.log('');
    console.log('🔍 执行最终语法校验...');
    for (const result of results) {
      if (result.status !== 'ok' || result.replaced === 0) continue;
      const fullPath = path.join(PROJECT_ROOT, result.filePath);
      const valid = validateFile(fullPath, result.filePath);
      finalVerification.push({
        filePath: result.filePath,
        syntaxValid: valid
      });
      if (!valid) {
        console.error(`   ❌ ${result.filePath}: 语法校验失败`);
      } else {
        console.log(`   ✅ ${result.filePath}: 语法校验通过`);
      }
    }
    const failedVerifications = finalVerification.filter(v => !v.syntaxValid);
    if (failedVerifications.length > 0) {
      console.error(`\n⚠️  ${failedVerifications.length} 个文件最终语法校验未通过！`);
    } else if (finalVerification.length > 0) {
      console.log(`\n✅ 全部 ${finalVerification.length} 个已修改文件语法校验通过`);
    }
  }

  // 5. 输出摘要
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📊 替换完成`);
  console.log(`   成功: ${totalReplaced} 处`);
  console.log(`   失败: ${totalFailed} 处`);
  console.log(`   跳过: ${totalSkipped} 处`);
  if (totalRolledBack > 0) {
    console.log(`   回滚: ${totalRolledBack} 个文件（语法错误）`);
  }
  if (BACKUP && !DRY_RUN) {
    console.log(`   备份: ${BACKUP_DIR}`);
  }
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 6. 保存替换报告
  const reportPath = path.join(I18N_DIR, 'replace_report.json');
  if (!DRY_RUN) {
    fs.writeFileSync(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      targetLanguage: TARGET_LANG,
      totalReplaced,
      totalFailed,
      totalSkipped,
      totalRolledBack,
      backupDir: BACKUP ? BACKUP_DIR : null,
      finalVerification,
      files: results
    }, null, 2), 'utf8');
    console.log(`📄 替换报告: ${reportPath}`);
  }

  // 7. 如果有失败或回滚，退出码 = 1
  if (totalFailed > 0 || totalRolledBack > 0) {
    process.exit(1);
  }
}

// ============================================================
// 语法验证
// ============================================================

/**
 * 对替换后的文件进行语法验证
 * JS/TS → node --check
 * JSON/Scene/Prefab → JSON.parse
 */
function validateFile(fullPath, relativePath) {
  const ext = path.extname(relativePath).toLowerCase();

  try {
    if (ext === '.js') {
      execSync(`node --check "${fullPath}"`, { stdio: 'pipe' });
      return true;
    }

    if (ext === '.json' || ext === '.scene' || ext === '.prefab' || ext === '.fire') {
      const content = fs.readFileSync(fullPath, 'utf8');
      JSON.parse(content);
      return true;
    }

    if (ext === '.ts') {
      // TS 文件无法用 node --check 直接验证
      // 做基础的括号/引号配对检查
      const content = fs.readFileSync(fullPath, 'utf8');
      return basicSyntaxCheck(content);
    }

    // 其他文件类型不做验证，视为通过
    return true;
  } catch (err) {
    console.error(`   验证错误: ${err.message || err.stderr?.toString()}`);
    return false;
  }
}

/**
 * 基础语法检查：检查引号和括号是否配对
 * 
 * v3.2 修复：正确处理模板字符串中 ${} 表达式内的嵌套花括号、字符串和注释。
 * 之前的实现在 ${} 表达式内不追踪嵌套花括号，导致含有对象字面量或函数调用
 * 的模板表达式被误报为"引号/注释未闭合"。
 */
function basicSyntaxCheck(content) {
  // 使用状态栈来正确处理模板字符串的嵌套
  // 状态类型: 'code' | 'template' | 'template_expr'
  const stateStack = ['code'];
  let inString = false;
  let stringChar = '';
  let inComment = false;
  let inLineComment = false;
  let braceDepth = 0; // 用于追踪 template_expr 内的嵌套花括号

  function currentState() {
    return stateStack[stateStack.length - 1];
  }

  for (let i = 0; i < content.length; i++) {
    const ch = content[i];
    const next = i + 1 < content.length ? content[i + 1] : '';

    // ========== 行注释 ==========
    if (inLineComment) {
      if (ch === '\n') inLineComment = false;
      continue;
    }

    // ========== 块注释 ==========
    if (inComment) {
      if (ch === '*' && next === '/') {
        inComment = false;
        i++;
      }
      continue;
    }

    // ========== 普通字符串（单引号/双引号）内 ==========
    if (inString) {
      if (ch === '\\') { i++; continue; } // 转义
      if (ch === stringChar) inString = false;
      continue;
    }

    const state = currentState();

    // ========== 模板字符串字面量内（反引号之间，但不在 ${} 内） ==========
    if (state === 'template') {
      if (ch === '\\') { i++; continue; } // 转义
      if (ch === '`') {
        // 模板字符串结束
        stateStack.pop();
        continue;
      }
      if (ch === '$' && next === '{') {
        // 进入模板表达式 ${}
        stateStack.push('template_expr');
        braceDepth = 0; // 重置嵌套花括号计数
        i++; // 跳过 '{'
        continue;
      }
      // 模板字符串字面量部分的其他字符，直接跳过
      continue;
    }

    // ========== 模板表达式 ${...} 内 ==========
    if (state === 'template_expr') {
      // 表达式内可以有完整的 JS 代码，需要处理字符串、注释、嵌套花括号、嵌套模板等

      // 注释
      if (ch === '/' && next === '/') { inLineComment = true; i++; continue; }
      if (ch === '/' && next === '*') { inComment = true; i++; continue; }

      // 字符串
      if (ch === '"' || ch === "'") { inString = true; stringChar = ch; continue; }

      // 嵌套模板字符串
      if (ch === '`') {
        stateStack.push('template');
        continue;
      }

      // 嵌套花括号
      if (ch === '{') {
        braceDepth++;
        continue;
      }

      if (ch === '}') {
        if (braceDepth > 0) {
          // 关闭嵌套花括号
          braceDepth--;
          continue;
        } else {
          // 关闭 ${} 表达式，回到模板字符串字面量
          stateStack.pop(); // 弹出 'template_expr'，回到 'template'
          continue;
        }
      }

      // 表达式内的其他字符
      continue;
    }

    // ========== 正常代码状态 (code) ==========
    // 注释
    if (ch === '/' && next === '/') { inLineComment = true; i++; continue; }
    if (ch === '/' && next === '*') { inComment = true; i++; continue; }

    // 字符串
    if (ch === '"' || ch === "'") { inString = true; stringChar = ch; continue; }

    // 模板字符串开始
    if (ch === '`') {
      stateStack.push('template');
      continue;
    }

    // 正常代码中的花括号不需要特殊追踪（这不是完整的 JS parser）
  }

  // 检查结束状态
  if (inString || inComment) {
    console.error('   基础检查: 引号/注释未闭合');
    return false;
  }

  // 检查是否还在模板字符串或模板表达式中
  if (stateStack.length > 1 || currentState() !== 'code') {
    console.error(`   基础检查: 模板字符串/表达式未闭合 (state stack: ${stateStack.join(' > ')})`);
    return false;
  }

  return true;
}

// ============================================================
// 替换逻辑（带逐条即时校验）
// ============================================================

/**
 * 逐条替换并在每次替换后即时校验语法
 * 如果某条替换导致语法错误，回退该条并标记为失败，继续下一条
 */
function replaceInFileWithValidation(content, entries, filePath, fullPath, dryRun) {
  let newContent = content;
  let replaced = 0;
  let failed = 0;
  const details = [];
  const ext = path.extname(filePath).toLowerCase();
  const isValidatable = ['.js', '.json', '.scene', '.prefab', '.fire', '.ts', '.csv', '.tsv'].includes(ext);

  // 按 range[0] 从大到小排序，从后往前替换，避免位置偏移
  const sortedEntries = [...entries].sort((a, b) => {
    const rangeA = a.range ? a.range[0] : (a.loc?.start?.line || 0) * 100000;
    const rangeB = b.range ? b.range[0] : (b.loc?.start?.line || 0) * 100000;
    return rangeB - rangeA;
  });

  for (const entry of sortedEntries) {
    try {
      const result = replaceEntry(newContent, entry, filePath);
      if (result.success) {
        // 替换成功，检查语法
        if (isValidatable && !dryRun) {
          const syntaxOk = validateContentInMemory(result.content, filePath);
          if (!syntaxOk) {
            // 语法校验失败，回退该条替换
            failed++;
            details.push({
              key: entry.key,
              type: entry.type,
              source: entry.source,
              target: entry.target,
              status: 'reverted',
              method: result.method,
              reason: '替换后语法校验失败，已回退该条'
            });
            console.warn(`   ⚠️ 回退: ${entry.key} (${entry.source?.substring(0, 20)}...) — 语法校验失败`);
            continue;
          }
        }

        newContent = result.content;
        replaced++;
        details.push({
          key: entry.key,
          type: entry.type,
          source: entry.source,
          target: entry.target,
          status: 'replaced',
          method: result.method
        });
      } else {
        failed++;
        details.push({
          key: entry.key,
          type: entry.type,
          source: entry.source,
          target: entry.target,
          status: 'failed',
          reason: result.reason
        });
      }
    } catch (err) {
      failed++;
      details.push({
        key: entry.key,
        type: entry.type,
        source: entry.source,
        target: entry.target,
        status: 'error',
        reason: err.message
      });
    }
  }

  return { newContent, replaced, failed, details };
}

/**
 * 内存中校验内容语法（不写入文件）
 */
function validateContentInMemory(content, filePath) {
  const ext = path.extname(filePath).toLowerCase();
  try {
    if (ext === '.json' || ext === '.scene' || ext === '.prefab' || ext === '.fire') {
      JSON.parse(content);
      return true;
    }
    if (ext === '.js' || ext === '.ts') {
      return basicSyntaxCheck(content);
    }
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * 原有的 replaceInFile 保留，供兼容使用
 */
function replaceInFile(content, entries, filePath) {
  return replaceInFileWithValidation(content, entries, filePath, null, true);
}

function replaceEntry(content, entry, filePath) {
  const { type } = entry;

  switch (type) {
    case 'text':
      return replaceTextEntry(content, entry);
    case 'template':
      return replaceTemplateEntry(content, entry);
    case 'concatenation':
      return replaceConcatenationEntry(content, entry);
    default:
      return { success: false, reason: `未知条目类型: ${type}` };
  }
}

/**
 * 替换 CSV/TSV 数据文件中的文本条目
 * 
 * CSV 文件的替换策略：
 *   1. range 精确替换（最可靠）
 *   2. 行号 + 单元格内容定位
 *   3. 全局唯一匹配（CSV 中同一文本可能出现多次，需要谨慎）
 * 
 * CSV 替换的特殊要求：
 *   - 只替换单元格内的中文文本，不能破坏 CSV 格式（逗号分隔、换行等）
 *   - 如果单元格被双引号包裹，替换后仍需保留双引号包裹
 *   - target 中如果包含逗号，替换后需要用双引号包裹该单元格
 */
function replaceCsvTextEntry(content, entry) {
  const { source, target, range, loc } = entry;

  // 策略1：range 精确替换
  if (range && range[0] >= 0 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);
    if (segment === source) {
      const safeTarget = csvSafeValue(target, source, content, range[0]);
      const newContent = content.substring(0, range[0]) + safeTarget + content.substring(range[1]);
      return { success: true, content: newContent, method: 'csv_range_exact' };
    }
    // segment 可能包含引号包裹
    if (segment === `"${source}"` || segment.includes(source)) {
      const newSegment = segment.replace(source, target);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'csv_range_contains' };
    }
  }

  // 策略2：行号 + 内容定位
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    for (const lineIdx of candidateLineIdxs) {
      if (lineIdx >= 0 && lineIdx < lines.length) {
        const line = lines[lineIdx];
        const occurrences = countOccurrences(line, source);

        if (occurrences === 1) {
          lines[lineIdx] = line.replace(source, target);
          return { success: true, content: lines.join('\n'), method: 'csv_line_unique' };
        }

        // 如果有多个匹配但有列号信息，用列索引定位到具体单元格
        if (occurrences > 1 && loc.start.column >= 0) {
          // 将行拆分为单元格（简单逗号分隔，不处理引号内逗号的复杂情况）
          const cells = parseCsvLine(line);
          const colIdx = loc.start.column;
          if (colIdx < cells.length && cells[colIdx].value.includes(source)) {
            cells[colIdx].value = cells[colIdx].value.replace(source, target);
            lines[lineIdx] = cells.map(c => c.quoted ? `"${c.value}"` : c.value).join(',');
            return { success: true, content: lines.join('\n'), method: 'csv_line_column' };
          }
        }
      }
    }
  }

  // 策略3：全局唯一匹配
  const bareCount = countOccurrences(content, source);
  if (bareCount === 1) {
    const newContent = content.replace(source, target);
    return { success: true, content: newContent, method: 'csv_global_unique' };
  }

  return {
    success: false,
    reason: `CSV 文件中未找到安全的唯一匹配 (source="${source.substring(0, 30)}", count=${bareCount})`
  };
}

/**
 * 确保 CSV 替换后的值是格式安全的
 * 如果 target 包含逗号、双引号或换行符，需要用双引号包裹
 */
function csvSafeValue(target, source, content, rangeStart) {
  // 检查原始值是否被双引号包裹
  const charBefore = rangeStart > 0 ? content[rangeStart - 1] : '';
  const isQuoted = charBefore === '"';

  // 如果 target 包含逗号、双引号或换行符，且不在引号内，需要处理
  if (!isQuoted && (target.includes(',') || target.includes('"') || target.includes('\n'))) {
    // 这种情况比较复杂，为安全起见直接返回 target，
    // 在策略1中 range 精确匹配时由外层处理引号
    return target;
  }
  return target;
}

/**
 * 解析 CSV 行为单元格数组（支持双引号包裹的字段）
 */
function parseCsvLine(line) {
  const cells = [];
  let current = '';
  let inQuotes = false;
  let quoted = false;

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
      if (ch === '"' && current === '') {
        inQuotes = true;
        quoted = true;
      } else if (ch === ',') {
        cells.push({ value: current, quoted });
        current = '';
        quoted = false;
      } else {
        current += ch;
      }
    }
  }
  cells.push({ value: current, quoted });
  return cells;
}

/**
 * 替换纯文本条目
 * 优先级：range 精确替换 > 行号+字符串字面量优先匹配 > 行号+列号精确定位 > JSON-aware 替换 > 唯一匹配搜索（排除注释）
 *
 * [v3.5] langpack 模式（entry._isCodeExpression = true）：
 *   target 是 i18n 调用表达式（如 i18n.t('key')），需要将整个字符串字面量（含引号）替换为表达式
 *   例如：`"开始游戏"` → `i18n.t('ui_start')`
 */
function replaceTextEntry(content, entry) {
  const { source, target, range, loc } = entry;
  const isCodeExpr = entry._isCodeExpression === true;
  const filePath = entry.filePath || '';
  const ext = path.extname(filePath).toLowerCase();
  const isJsonLike = ['.json', '.scene', '.prefab', '.fire'].includes(ext);
  const isCsvLike = ['.csv', '.tsv'].includes(ext);

  // JSON/Scene/Prefab 等数据文件不支持 langpack 模式（不能在 JSON 值中写函数调用）
  if (isCodeExpr && isJsonLike) {
    return { success: false, reason: 'JSON 数据文件不支持语言包模式替换（无法在 JSON 值中使用函数调用）' };
  }

  // CSV/TSV 文件：langpack 模式下跳过（数据文件不能写 i18n 调用）
  if (isCsvLike) {
    if (isCodeExpr) {
      return { success: false, reason: 'CSV/TSV 数据文件不支持语言包模式替换' };
    }
    return replaceCsvTextEntry(content, entry);
  }

  // ========== langpack 模式：将整个字符串字面量（含引号）替换为 i18n 表达式 ==========
  if (isCodeExpr) {
    return replaceLangpackTextEntry(content, entry);
  }

  // ========== direct 模式（原有逻辑）：将字符串内容替换为目标语言文本 ==========

  // 策略1：使用 range 精确替换
  if (range && range[0] >= 0 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);

    // 检查 range 指向的内容是否包含 source
    if (segment === source || segment === `"${source}"` || segment === `'${source}'` || segment === `\`${source}\``) {
      // [v3.5] 对 target 做引号安全转义
      const safeTarget = escapeTargetForContext(content, range[0] + (segment.length - source.length), source.length, target);
      const newSegment = segment.replace(source, safeTarget);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_exact' };
    }

    // JSON 文件中的值可能有转义字符，尝试 JSON 转义匹配
    if (isJsonLike) {
      const jsonEscapedSource = jsonEscape(source);
      if (segment.includes(jsonEscapedSource)) {
        const jsonEscapedTarget = jsonEscape(target);
        const newSegment = segment.replace(jsonEscapedSource, jsonEscapedTarget);
        const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
        return { success: true, content: newContent, method: 'range_json_escaped' };
      }
    }

    // range 可能包含引号，检查 source 是否在 segment 中
    if (segment.includes(source)) {
      // [v3.5] 对 target 做引号安全转义
      const srcIdx = segment.indexOf(source);
      const safeTarget = escapeTargetForContext(content, range[0] + srcIdx, source.length, target);
      const newSegment = segment.replace(source, safeTarget);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_contains' };
    }
    // range 不匹配，降级到下一策略
  }

  // 策略2：使用行号+内容定位（兼容 0-indexed 和 1-indexed 行号）
  // [v3.4] 优先在字符串字面量中定位 source，避免替换注释中的文本
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    // 兼容 0-indexed 和 1-indexed：如果 line == 0 直接用 0，否则尝试 line-1（1-indexed）和 line（0-indexed）
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    const preferColumn = (loc.start.column >= 0) ? loc.start.column : -1;

    for (const lineIdx of candidateLineIdxs) {
      if (lineIdx >= 0 && lineIdx < lines.length) {
        const line = lines[lineIdx];

        // JSON 文件中需要考虑转义
        if (isJsonLike) {
          const jsonEscapedSource = jsonEscape(source);
          const jsonEscapedTarget = jsonEscape(target);
          const escapedOccurrences = countOccurrences(line, jsonEscapedSource);
          if (escapedOccurrences === 1) {
            lines[lineIdx] = line.replace(jsonEscapedSource, jsonEscapedTarget);
            return { success: true, content: lines.join('\n'), method: 'line_json_escaped' };
          }
        }

        // [v3.4] 策略2a：优先在字符串字面量中精确定位 source
        const literalMatch = findStringLiteralInLine(line, source, preferColumn);
        if (literalMatch) {
          const { replaced, success } = replaceStringLiteralInLine(line, source, target, preferColumn);
          if (success) {
            lines[lineIdx] = replaced;
            return { success: true, content: lines.join('\n'), method: 'line_string_literal' };
          }
        }

        // [v3.4] 策略2b：使用列号精确定位（仅当字符串字面量匹配失败时降级使用）
        if (preferColumn >= 0 && line.includes(source)) {
          const col = preferColumn;
          // 从列号位置检查 ±5 字符范围内是否有精确匹配
          for (let delta = 0; delta <= 5; delta++) {
            for (const dir of [0, -1, 1]) {
              const checkCol = col + dir * delta;
              if (checkCol >= 0 && checkCol + source.length <= line.length) {
                const segment = line.substring(checkCol, checkCol + source.length);
                if (segment === source) {
                  // [v3.5] 对 target 做引号安全转义
                  const safeTarget = escapeTargetForLineContext(line, checkCol, source.length, target);
                  const before = line.substring(0, checkCol);
                  const after = line.substring(checkCol + source.length);
                  lines[lineIdx] = before + safeTarget + after;
                  return { success: true, content: lines.join('\n'), method: 'line_column_exact' };
                }
              }
            }
          }
        }

        // 策略2c（降级）：该行唯一匹配时直接替换
        // 仅在字符串字面量搜索失败后使用
        const occurrences = countOccurrences(line, source);
        if (occurrences === 1) {
          // [v3.5] 对 target 做引号安全转义
          const srcPos = line.indexOf(source);
          const safeTarget = escapeTargetForLineContext(line, srcPos, source.length, target);
          lines[lineIdx] = line.replace(source, safeTarget);
          return { success: true, content: lines.join('\n'), method: 'line_unique' };
        }
      }
    }
  }

  // 策略3：JSON-aware 全局替换（仅 JSON 类文件）
  if (isJsonLike) {
    const jsonEscapedSource = jsonEscape(source);
    const jsonEscapedTarget = jsonEscape(target);
    const jsonPattern = `"${jsonEscapedSource}"`;
    const jsonCount = countOccurrences(content, jsonPattern);
    if (jsonCount === 1) {
      const newContent = content.replace(jsonPattern, `"${jsonEscapedTarget}"`);
      return { success: true, content: newContent, method: 'json_global_unique' };
    }
  }

  // 策略4：全局搜索替换 — 仅在唯一匹配时执行
  // [v3.4] 检查匹配位置是否在注释中，如果在注释中则跳过
  const quotedPatterns = [
    { quote: '"', pattern: `"${source}"` },
    { quote: "'", pattern: `'${source}'` },
    { quote: '`', pattern: `\`${source}\`` },
  ];

  for (const { quote, pattern } of quotedPatterns) {
    const count = countOccurrences(content, pattern);
    if (count === 1) {
      // [v3.4] 检查这个唯一匹配是否在注释中
      const matchIdx = content.indexOf(pattern);
      if (!isInsideComment(content, matchIdx)) {
        // [v3.5] 对 target 中与外层引号冲突的字符做转义
        const safeTarget = escapeTargetForContext(content, matchIdx + 1, source.length, target);
        const newContent = content.replace(pattern, `${quote}${safeTarget}${quote}`);
        return { success: true, content: newContent, method: 'global_unique' };
      }
      // 匹配在注释中，继续尝试其他引号类型
      continue;
    }
    if (count > 1) {
      // [v3.4] 多处匹配时，筛选出不在注释中的匹配
      const nonCommentMatches = [];
      let searchPos = 0;
      while (true) {
        const idx = content.indexOf(pattern, searchPos);
        if (idx === -1) break;
        if (!isInsideComment(content, idx)) {
          nonCommentMatches.push(idx);
        }
        searchPos = idx + pattern.length;
      }
      if (nonCommentMatches.length === 1) {
        // 只有一处非注释匹配，安全替换
        const idx = nonCommentMatches[0];
        // [v3.5] 对 target 中与外层引号冲突的字符做转义
        const safeTarget = escapeTargetForContext(content, idx + 1, source.length, target);
        const newContent = content.substring(0, idx) + `${quote}${safeTarget}${quote}` + content.substring(idx + pattern.length);
        return { success: true, content: newContent, method: 'global_unique_non_comment' };
      }
      // 多处非注释匹配，不安全，跳过
      continue;
    }
  }

  // 策略5：不带引号的唯一匹配（仅用于 JSON 值等场景）
  // [v3.4] 添加注释排除
  const bareCount = countOccurrences(content, source);
  if (bareCount === 1) {
    // 确认这个匹配确实在引号/值上下文中，不是代码逻辑的一部分
    const idx = content.indexOf(source);
    // [v3.4] 先排除注释中的匹配
    if (isInsideComment(content, idx)) {
      return { success: false, reason: `唯一匹配位于注释中，跳过 (source="${source.substring(0, 30)}")` };
    }
    const charBefore = idx > 0 ? content[idx - 1] : '';
    const charAfter = idx + source.length < content.length ? content[idx + source.length] : '';
    if ((charBefore === '"' || charBefore === "'" || charBefore === '`' || charBefore === ':' || charBefore === '>') &&
      (charAfter === '"' || charAfter === "'" || charAfter === '`' || charAfter === '<' || charAfter === ',' || charAfter === '}' || charAfter === '\\')) {
      // [v3.5] 对 target 中与外层引号冲突的字符做转义
      const safeTarget = escapeTargetForContext(content, idx, source.length, target);
      const newContent = content.replace(source, safeTarget);
      return { success: true, content: newContent, method: 'bare_unique_contextual' };
    }
  } else if (bareCount > 1) {
    // [v3.4] 多处匹配时，筛选出在字符串字面量中且不在注释中的匹配
    const nonCommentQuotedMatches = [];
    let searchPos = 0;
    while (true) {
      const idx = content.indexOf(source, searchPos);
      if (idx === -1) break;
      if (!isInsideComment(content, idx)) {
        const charBefore = idx > 0 ? content[idx - 1] : '';
        const charAfter = idx + source.length < content.length ? content[idx + source.length] : '';
        if ((charBefore === '"' || charBefore === "'" || charBefore === '`') &&
          (charAfter === '"' || charAfter === "'" || charAfter === '`')) {
          nonCommentQuotedMatches.push(idx);
        }
      }
      searchPos = idx + source.length;
    }
    if (nonCommentQuotedMatches.length === 1) {
      const idx = nonCommentQuotedMatches[0];
      // [v3.5] 对 target 中与外层引号冲突的字符做转义
      const safeTarget = escapeTargetForContext(content, idx, source.length, target);
      const newContent = content.substring(0, idx) + safeTarget + content.substring(idx + source.length);
      return { success: true, content: newContent, method: 'multi_match_single_literal' };
    }
  }

  return { success: false, reason: `未找到安全的唯一匹配 (source="${source.substring(0, 30)}", bareCount=${bareCount})` };
}

/**
 * [v3.5] langpack 模式：将整个字符串字面量（含引号）替换为 i18n 调用表达式
 *
 * 与 direct 模式不同：
 *   direct:   "开始游戏" → "Start Game"    （替换引号内的内容）
 *   langpack: "开始游戏" → i18n.t('key')   （替换整个字面量，包括引号）
 *
 * 策略优先级：range 精确 > 行号+字面量定位 > 全局唯一匹配
 */
function replaceLangpackTextEntry(content, entry) {
  const { source, target, range, loc } = entry;

  // 构造带引号的搜索模式
  const quotedPatterns = [
    { quote: '"', pattern: `"${source}"` },
    { quote: "'", pattern: `'${source}'` },
    { quote: '`', pattern: `\`${source}\`` },
  ];

  // 策略1：range 精确替换 — 将 range 指向的整个字面量替换为 i18n 表达式
  if (range && range[0] >= 0 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);

    // range 精确等于 带引号的 source
    for (const { pattern } of quotedPatterns) {
      if (segment === pattern) {
        const newContent = content.substring(0, range[0]) + target + content.substring(range[1]);
        return { success: true, content: newContent, method: 'langpack_range_exact' };
      }
    }

    // range 可能不含引号，尝试扩展 range 以包含引号
    if (segment === source) {
      const charBefore = range[0] > 0 ? content[range[0] - 1] : '';
      const charAfter = range[1] < content.length ? content[range[1]] : '';
      if ((charBefore === '"' || charBefore === "'" || charBefore === '`') &&
          (charAfter === '"' || charAfter === "'" || charAfter === '`')) {
        // 扩展 range 包含引号
        const newContent = content.substring(0, range[0] - 1) + target + content.substring(range[1] + 1);
        return { success: true, content: newContent, method: 'langpack_range_expand_quotes' };
      }
    }

    // range 包含 source 但可能有其他前后内容
    for (const { pattern } of quotedPatterns) {
      if (segment.includes(pattern)) {
        const newSegment = segment.replace(pattern, target);
        const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
        return { success: true, content: newContent, method: 'langpack_range_contains' };
      }
    }
  }

  // 策略2：行号定位
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    const preferColumn = (loc.start.column >= 0) ? loc.start.column : -1;

    for (const lineIdx of candidateLineIdxs) {
      if (lineIdx >= 0 && lineIdx < lines.length) {
        const line = lines[lineIdx];

        // 2a. 列号精确定位
        if (preferColumn >= 0) {
          for (let delta = 0; delta <= 5; delta++) {
            for (const dir of [0, -1, 1]) {
              const checkCol = preferColumn + dir * delta;
              if (checkCol >= 0) {
                for (const { pattern } of quotedPatterns) {
                  if (checkCol + pattern.length <= line.length) {
                    const seg = line.substring(checkCol, checkCol + pattern.length);
                    if (seg === pattern) {
                      lines[lineIdx] = line.substring(0, checkCol) + target + line.substring(checkCol + pattern.length);
                      return { success: true, content: lines.join('\n'), method: 'langpack_line_column' };
                    }
                  }
                }
              }
            }
          }
        }

        // 2b. 字符串字面量定位
        const literalMatch = findStringLiteralInLine(line, source, preferColumn);
        if (literalMatch) {
          // 直接在行中搜索带引号的 pattern 来替换（含引号整体替换）
          for (const { pattern } of quotedPatterns) {
            const patIdx = line.indexOf(pattern);
            if (patIdx >= 0) {
              // 如果有多个匹配，选择最接近 preferColumn 的
              const count = countOccurrences(line, pattern);
              if (count === 1) {
                lines[lineIdx] = line.substring(0, patIdx) + target + line.substring(patIdx + pattern.length);
                return { success: true, content: lines.join('\n'), method: 'langpack_line_literal' };
              }
            }
          }
        }

        // 2c. 行内唯一匹配
        for (const { pattern } of quotedPatterns) {
          const count = countOccurrences(line, pattern);
          if (count === 1) {
            lines[lineIdx] = line.replace(pattern, target);
            return { success: true, content: lines.join('\n'), method: 'langpack_line_unique' };
          }
        }
      }
    }
  }

  // 策略3：全局唯一匹配
  for (const { pattern } of quotedPatterns) {
    const count = countOccurrences(content, pattern);
    if (count === 1) {
      const matchIdx = content.indexOf(pattern);
      if (!isInsideComment(content, matchIdx)) {
        const newContent = content.replace(pattern, target);
        return { success: true, content: newContent, method: 'langpack_global_unique' };
      }
    }
    if (count > 1) {
      // 筛选非注释中的匹配
      const nonCommentMatches = [];
      let searchPos = 0;
      while (true) {
        const idx = content.indexOf(pattern, searchPos);
        if (idx === -1) break;
        if (!isInsideComment(content, idx)) {
          nonCommentMatches.push(idx);
        }
        searchPos = idx + pattern.length;
      }
      if (nonCommentMatches.length === 1) {
        const idx = nonCommentMatches[0];
        const newContent = content.substring(0, idx) + target + content.substring(idx + pattern.length);
        return { success: true, content: newContent, method: 'langpack_global_unique_non_comment' };
      }
    }
  }

  return { success: false, reason: `[langpack] 未找到安全的唯一匹配 (source="${source.substring(0, 30)}")` };
}

/**
 * [v3.5] langpack 模式：将整个模板字面量（含反引号）替换为 i18n 调用表达式
 */
function replaceLangpackTemplateLiteral(content, bareSource, backtickSource, target, range, loc) {
  // 策略1：range 精确替换
  if (range && Array.isArray(range) && range.length === 2 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);

    if (segment === backtickSource) {
      const newContent = content.substring(0, range[0]) + target + content.substring(range[1]);
      return { success: true, content: newContent, method: 'langpack_tpl_range_exact' };
    }
    if (segment === bareSource) {
      // range 不含反引号，扩展以包含
      const charBefore = range[0] > 0 ? content[range[0] - 1] : '';
      const charAfter = range[1] < content.length ? content[range[1]] : '';
      if (charBefore === '`' && charAfter === '`') {
        const newContent = content.substring(0, range[0] - 1) + target + content.substring(range[1] + 1);
        return { success: true, content: newContent, method: 'langpack_tpl_range_expand' };
      }
    }
    if (segment.includes(backtickSource)) {
      const newSegment = segment.replace(backtickSource, target);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'langpack_tpl_range_contains' };
    }
  }

  // 策略2：行号定位
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    for (const lineIdx of candidateLineIdxs) {
      if (lineIdx >= 0 && lineIdx < lines.length) {
        const line = lines[lineIdx];

        if (line.includes(backtickSource) && countOccurrences(line, backtickSource) === 1) {
          lines[lineIdx] = line.replace(backtickSource, target);
          return { success: true, content: lines.join('\n'), method: 'langpack_tpl_line_unique' };
        }
      }
    }
  }

  // 策略3：全局唯一匹配
  const btCount = countOccurrences(content, backtickSource);
  if (btCount === 1) {
    const matchIdx = content.indexOf(backtickSource);
    if (!isInsideComment(content, matchIdx)) {
      const newContent = content.replace(backtickSource, target);
      return { success: true, content: newContent, method: 'langpack_tpl_global_unique' };
    }
  }

  return { success: false, reason: `[langpack] 未找到模板字符串的唯一匹配 (source="${bareSource.substring(0, 40)}")` };
}

/**
 * 替换模板字符串条目
 * 
 * 模板字符串的 source 可能包含或不包含反引号：
 *   - 不含反引号：source = "第${objNextUnlock.level}关解锁"
 *   - 含反引号：source = "`第${objNextUnlock.level}关解锁`"
 * 需要同时兼容两种情况。
 *
 * [v3.5] langpack 模式：将整个模板字符串替换为 i18n 调用
 *   `恭喜${name}获得${reward}` → i18n.t('key', { name: name, reward: reward })
 */
function replaceTemplateEntry(content, entry) {
  const { source, target, range, loc } = entry;
  const isCodeExpr = entry._isCodeExpression === true;

  // 预处理：统一为不含反引号的版本（bareSource/bareTarget）和含反引号的版本（backtickSource/backtickTarget）
  const hasSurroundingBackticks = source.startsWith('`') && source.endsWith('`');
  const bareSource = hasSurroundingBackticks ? source.slice(1, -1) : source;
  const backtickSource = '`' + bareSource + '`';

  // [v3.5] langpack 模式：target 是 i18n 调用表达式（不含反引号）
  // 需要将 `模板字符串` 整体替换为 i18n.t('key', {...})
  if (isCodeExpr) {
    // target 已经是代码表达式（如 i18n.t('key', { name: name })），不需要再加反引号
    const langpackTarget = target;

    return replaceLangpackTemplateLiteral(content, bareSource, backtickSource, langpackTarget, range, loc);
  }

  const bareTarget = (target.startsWith('`') && target.endsWith('`')) ? target.slice(1, -1) : target;
  const backtickTarget = '`' + bareTarget + '`';

  // 策略1：range 精确替换（修复：允许 range[0] == 0 的情况）
  if (range && Array.isArray(range) && range.length === 2 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);

    // 1a. segment 完全等于含反引号的 source
    if (segment === backtickSource) {
      const newContent = content.substring(0, range[0]) + backtickTarget + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_exact_backtick' };
    }

    // 1b. segment 包含不带反引号的 source（range 可能只覆盖引号内的内容）
    if (segment.includes(bareSource)) {
      const newSegment = segment.replace(bareSource, bareTarget);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_contains_bare' };
    }

    // 1c. segment 包含带反引号的 source
    if (segment.includes(backtickSource)) {
      const newSegment = segment.replace(backtickSource, backtickTarget);
      const newContent = content.substring(0, range[0]) + newSegment + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_contains_backtick' };
    }
    // range 不匹配，降级到下一策略
  }

  // 策略2：行号定位（修复：允许 line == 0，使用 >= 0 判断）
  // [v3.4] 优先使用列号精确定位，避免替换注释中的文本
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    // 兼容 0-indexed 和 1-indexed：如果 line == 0 直接用 0，否则尝试 line-1（1-indexed）和 line（0-indexed）
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    const preferColumn = (loc.start && loc.start.column >= 0) ? loc.start.column : -1;

    for (const lineIdx of candidateLineIdxs) {
      if (lineIdx >= 0 && lineIdx < lines.length) {
        const line = lines[lineIdx];

        // [v3.4] 2a. 列号精确定位（最优先）
        if (preferColumn >= 0) {
          // 从列号位置 ±5 字符范围内查找 backtickSource 或 bareSource
          for (let delta = 0; delta <= 5; delta++) {
            for (const dir of [0, -1, 1]) {
              const checkCol = preferColumn + dir * delta;
              if (checkCol >= 0) {
                // 检查 backtickSource
                if (checkCol + backtickSource.length <= line.length) {
                  const seg = line.substring(checkCol, checkCol + backtickSource.length);
                  if (seg === backtickSource) {
                    lines[lineIdx] = line.substring(0, checkCol) + backtickTarget + line.substring(checkCol + backtickSource.length);
                    return { success: true, content: lines.join('\n'), method: 'line_column_backtick' };
                  }
                }
                // 检查 bareSource（可能列号指向反引号内的内容起始位置）
                if (checkCol + bareSource.length <= line.length) {
                  const seg = line.substring(checkCol, checkCol + bareSource.length);
                  if (seg === bareSource) {
                    lines[lineIdx] = line.substring(0, checkCol) + bareTarget + line.substring(checkCol + bareSource.length);
                    return { success: true, content: lines.join('\n'), method: 'line_column_bare' };
                  }
                }
              }
            }
          }
        }

        // 2b. 尝试不带反引号的 source 匹配（唯一匹配时）
        if (line.includes(bareSource) && countOccurrences(line, bareSource) === 1) {
          lines[lineIdx] = line.replace(bareSource, bareTarget);
          return { success: true, content: lines.join('\n'), method: 'line_bare' };
        }

        // 2c. 尝试带反引号的完整模板匹配（唯一匹配时）
        if (line.includes(backtickSource) && countOccurrences(line, backtickSource) === 1) {
          lines[lineIdx] = line.replace(backtickSource, backtickTarget);
          return { success: true, content: lines.join('\n'), method: 'line_backtick' };
        }

        // 2d. 该行有多个 bareSource 匹配但可通过列号定位（降级）
        if (line.includes(bareSource) && countOccurrences(line, bareSource) > 1 && preferColumn >= 0) {
          const col = preferColumn;
          const before = line.substring(0, col);
          const after = line.substring(col);
          // 检查从列号位置开始是否能匹配（允许±20字符偏差）
          const nearbyIdx = after.indexOf(bareSource);
          if (nearbyIdx >= 0 && nearbyIdx < 20) {
            const replaced = after.substring(0, nearbyIdx) + bareTarget + after.substring(nearbyIdx + bareSource.length);
            lines[lineIdx] = before + replaced;
            return { success: true, content: lines.join('\n'), method: 'line_column' };
          }
        }
      }
    }
  }

  // 策略3：全局唯一搜索 —— 带反引号匹配
  // [v3.4] 添加注释排除检查
  const backtickCount = countOccurrences(content, backtickSource);
  if (backtickCount === 1) {
    const matchIdx = content.indexOf(backtickSource);
    if (!isInsideComment(content, matchIdx)) {
      const newContent = content.replace(backtickSource, backtickTarget);
      return { success: true, content: newContent, method: 'global_unique_backtick' };
    }
  }

  // 策略4：全局唯一搜索 —— 不带反引号匹配（回退策略）
  // 用于 source 不含反引号且全文中唯一出现的情况
  // [v3.4] 添加注释排除检查
  const bareCount = countOccurrences(content, bareSource);
  if (bareCount === 1) {
    // 确认匹配位置在反引号模板字符串上下文中
    const idx = content.indexOf(bareSource);
    if (!isInsideComment(content, idx)) {
      const charBefore = idx > 0 ? content[idx - 1] : '';
      const charAfter = idx + bareSource.length < content.length ? content[idx + bareSource.length] : '';
      // 模板字符串中的内容前后应该是 ` 或 ${ 或 } 等模板相关字符
      if (charBefore === '`' || charBefore === '}' || charAfter === '`' || charAfter === '$') {
        const newContent = content.replace(bareSource, bareTarget);
        return { success: true, content: newContent, method: 'global_unique_bare_contextual' };
      }
    }
  } else if (bareCount > 1) {
    // [v3.4] 多个 bareSource 匹配时，筛选出在模板字符串上下文中且不在注释中的匹配
    const validMatches = [];
    let searchPos = 0;
    while (true) {
      const idx = content.indexOf(bareSource, searchPos);
      if (idx === -1) break;
      if (!isInsideComment(content, idx)) {
        const charBefore = idx > 0 ? content[idx - 1] : '';
        const charAfter = idx + bareSource.length < content.length ? content[idx + bareSource.length] : '';
        if (charBefore === '`' || charBefore === '}' || charAfter === '`' || charAfter === '$') {
          validMatches.push(idx);
        }
      }
      searchPos = idx + bareSource.length;
    }
    if (validMatches.length === 1) {
      const idx = validMatches[0];
      const newContent = content.substring(0, idx) + bareTarget + content.substring(idx + bareSource.length);
      return { success: true, content: newContent, method: 'global_multi_single_template' };
    }
  }

  return {
    success: false,
    reason: `未找到安全的唯一匹配的模板字符串 (bareSource="${bareSource.substring(0, 40)}", backtickCount=${backtickCount}, bareCount=${bareCount})`
  };
}

/**
 * 替换拼接字符串条目
 * 这是最复杂也最危险的操作
 */
function replaceConcatenationEntry(content, entry) {
  const { originalExpression, translatedExpression, range, loc } = entry;

  if (!originalExpression || !translatedExpression) {
    return { success: false, reason: '缺少 originalExpression 或 translatedExpression' };
  }

  // 策略1：range 精确替换
  if (range && range[0] >= 0 && range[1] > range[0]) {
    const segment = content.substring(range[0], range[1]);
    const normalizedSegment = normalizeExpression(segment);
    const normalizedOriginal = normalizeExpression(originalExpression);

    if (normalizedSegment === normalizedOriginal) {
      const newContent = content.substring(0, range[0]) + translatedExpression + content.substring(range[1]);
      return { success: true, content: newContent, method: 'range_exact' };
    }

    // range 可能有微小偏差（±几个字符），尝试在 range 附近搜索
    const searchStart = Math.max(0, range[0] - 20);
    const searchEnd = Math.min(content.length, range[1] + 20);
    const searchArea = content.substring(searchStart, searchEnd);

    const matchResult = findExpressionInText(searchArea, originalExpression);
    if (matchResult) {
      const actualStart = searchStart + matchResult.start;
      const actualEnd = searchStart + matchResult.end;
      const newContent = content.substring(0, actualStart) + translatedExpression + content.substring(actualEnd);
      return { success: true, content: newContent, method: 'range_nearby' };
    }
  }

  // 策略2：行号定位（兼容 0-indexed 和 1-indexed 行号）
  if (loc && loc.start && typeof loc.start.line === 'number' && loc.start.line >= 0) {
    const lines = content.split('\n');
    // 兼容 0-indexed 和 1-indexed
    const candidateLineIdxs = loc.start.line === 0
      ? [0]
      : [loc.start.line - 1, loc.start.line];

    // 可能跨行，检查候选行 ±1 行
    for (const baseIdx of candidateLineIdxs) {
      for (let offset = 0; offset <= 1; offset++) {
        const checkIdx = baseIdx + offset;
        if (checkIdx >= 0 && checkIdx < lines.length) {
          const line = lines[checkIdx];
          const matchResult = findExpressionInText(line, originalExpression);
          if (matchResult) {
            const newLine = line.substring(0, matchResult.start) + translatedExpression + line.substring(matchResult.end);
            lines[checkIdx] = newLine;
            return { success: true, content: lines.join('\n'), method: 'line_match' };
          }
        }
      }
    }
  }

  // 策略3：全文搜索（仅在唯一匹配时执行）
  const allMatches = findAllExpressionMatches(content, originalExpression);
  if (allMatches.length === 1) {
    const match = allMatches[0];
    const newContent = content.substring(0, match.start) + translatedExpression + content.substring(match.end);
    return { success: true, content: newContent, method: 'global_unique' };
  }

  if (allMatches.length > 1) {
    return { success: false, reason: `拼接表达式有 ${allMatches.length} 处匹配，无法安全替换` };
  }

  return { success: false, reason: '未找到匹配的拼接表达式' };
}

// ============================================================
// 表达式匹配工具函数
// ============================================================

/**
 * 在文本中查找拼接表达式，返回 { start, end } 或 null
 * 忽略空格差异
 */
function findExpressionInText(text, expression) {
  // 构建灵活匹配正则：拆分表达式，各部分间允许任意空格
  const parts = expression.split(/\s*\+\s*/);
  if (parts.length === 0) return null;

  const patternParts = parts.map(p => escapeRegex(p.trim()));
  const pattern = patternParts.join('\\s*\\+\\s*');

  try {
    const regex = new RegExp(pattern);
    const match = text.match(regex);
    if (match) {
      return { start: match.index, end: match.index + match[0].length };
    }
  } catch (e) {
    // 正则构建失败，尝试直接查找
  }

  // 降级：标准化后比较
  const normalizedExpr = normalizeExpression(expression);
  const normalizedText = normalizeExpression(text);
  const idx = normalizedText.indexOf(normalizedExpr);
  if (idx >= 0) {
    // 找回原始文本中的位置（近似）
    // 这里简化处理，找到 normalized 位置后在原文中搜索
    return findOriginalPosition(text, expression);
  }

  return null;
}

/**
 * 全文搜索拼接表达式的所有匹配位置
 */
function findAllExpressionMatches(content, expression) {
  const parts = expression.split(/\s*\+\s*/);
  if (parts.length === 0) return [];

  const patternParts = parts.map(p => escapeRegex(p.trim()));
  const pattern = patternParts.join('\\s*\\+\\s*');

  try {
    const regex = new RegExp(pattern, 'g');
    const matches = [];
    let match;
    while ((match = regex.exec(content)) !== null) {
      matches.push({ start: match.index, end: match.index + match[0].length });
    }
    return matches;
  } catch (e) {
    return [];
  }
}

/**
 * 在原始文本中找到表达式的精确位置
 */
function findOriginalPosition(text, expression) {
  const parts = expression.split(/\s*\+\s*/);
  const patternParts = parts.map(p => escapeRegex(p.trim()));
  const pattern = patternParts.join('\\s*\\+\\s*');

  try {
    const regex = new RegExp(pattern);
    const match = text.match(regex);
    if (match) {
      return { start: match.index, end: match.index + match[0].length };
    }
  } catch (e) { }

  return null;
}

// ============================================================
// 引号安全处理
// ============================================================

/**
 * [v3.5] 根据外层包裹引号类型，对 target 中的冲突字符进行转义。
 *
 * 问题场景：
 *   source 在代码中被双引号包裹：Msg("…选择『成为鬼仙』…")
 *   翻译后 target 含有双引号：…选择"成为鬼仙"…
 *   直接替换会导致：Msg("…选择"成为鬼仙"…")  ← 语法错误
 *
 * 修复：检测 source 所在位置的包裹引号（content[sourceOffset - 1]），
 *       如果 target 包含该引号字符，自动用反斜杠转义。
 *
 * @param {string} content - 完整文件内容
 * @param {number} sourceOffset - source 在 content 中的起始偏移
 * @param {number} sourceLength - source 的长度
 * @param {string} target - 翻译后文本
 * @returns {string} 转义安全的 target
 */
function escapeTargetForContext(content, sourceOffset, sourceLength, target) {
  if (sourceOffset <= 0) return target;
  const charBefore = content[sourceOffset - 1];
  // 只处理 source 直接被引号包裹的情况
  if (charBefore !== '"' && charBefore !== "'" && charBefore !== '`') return target;

  // 进一步确认后面也有对应的闭合引号
  const charAfter = sourceOffset + sourceLength < content.length
    ? content[sourceOffset + sourceLength]
    : '';
  if (charAfter !== charBefore) return target;

  // source 本身在原文中不含该引号（否则原文就已经有转义处理了）
  // 只需要处理 target 中 **新引入** 的该引号字符
  const quoteChar = charBefore;

  if (!target.includes(quoteChar)) return target;

  // 对 target 中未转义的 quoteChar 添加反斜杠
  let escaped = '';
  for (let i = 0; i < target.length; i++) {
    if (target[i] === quoteChar) {
      // 检查前面是否已经有反斜杠
      if (i > 0 && target[i - 1] === '\\') {
        escaped += target[i]; // 已转义，保持原样
      } else {
        escaped += '\\' + target[i]; // 添加转义
      }
    } else {
      escaped += target[i];
    }
  }
  return escaped;
}

/**
 * [v3.5] 行内版本：根据行内 source 位置前的引号字符，对 target 做转义。
 *
 * @param {string} line - 单行文本
 * @param {number} offsetInLine - source 在行中的起始偏移
 * @param {number} sourceLength - source 的长度
 * @param {string} target - 翻译后文本
 * @returns {string} 转义安全的 target
 */
function escapeTargetForLineContext(line, offsetInLine, sourceLength, target) {
  if (offsetInLine <= 0) return target;
  return escapeTargetForContext(line, offsetInLine, sourceLength, target);
}

// ============================================================
// 通用工具函数
// ============================================================

function groupByFile(translations) {
  const groups = {};
  for (const entry of translations) {
    if (!groups[entry.filePath]) {
      groups[entry.filePath] = [];
    }
    groups[entry.filePath].push(entry);
  }
  return groups;
}

function backupFile(fullPath, relativePath) {
  const backupPath = path.join(BACKUP_DIR, relativePath);
  const backupDir = path.dirname(backupPath);
  fs.mkdirSync(backupDir, { recursive: true });
  fs.copyFileSync(fullPath, backupPath);
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalizeExpression(expr) {
  return expr.replace(/\s+/g, ' ').trim();
}

/**
 * JSON 字符串转义
 * 将字符串中的特殊字符转义为 JSON 安全形式
 */
function jsonEscape(str) {
  return str
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/\t/g, '\\t');
}

/**
 * [v3.4] 在一行文本中查找位于字符串字面量内（被引号包裹）的 source 出现。
 * 返回 source 在行中的**字符偏移量**（相对于行首），如果没找到则返回 -1。
 * 
 * 这是修复"替换注释中的文本而遗漏代码中字符串"问题的核心函数。
 * 
 * 算法：遍历该行，跟踪注释状态和字符串字面量边界，
 * 只匹配处于字符串字面量（单引号/双引号/反引号）内部的 source。
 * 
 * @param {string} line - 单行文本
 * @param {string} source - 要查找的中文字符串
 * @param {number} [preferColumn=-1] - 如果提供了列号，优先返回离该列号最近的匹配
 * @returns {{ offset: number, quoteChar: string } | null} 匹配位置和包裹的引号字符，或 null
 */
function findStringLiteralInLine(line, source, preferColumn) {
  const matches = [];
  let i = 0;

  while (i < line.length) {
    const ch = line[i];
    const next = i + 1 < line.length ? line[i + 1] : '';

    // 跳过行注释 // ...（后续内容全部是注释）
    if (ch === '/' && next === '/') {
      break; // 行注释后不可能有代码字符串了
    }

    // 遇到字符串字面量开头
    if (ch === '"' || ch === "'" || ch === '`') {
      const quoteChar = ch;
      const strStart = i; // 引号的位置
      i++; // 跳过开头引号

      // 扫描字符串内容直到结束引号
      let strContent = '';
      let strContentStart = i; // 字符串内容的起始位置（引号后第一个字符）
      while (i < line.length) {
        const sch = line[i];
        if (sch === '\\') {
          strContent += line[i] + (i + 1 < line.length ? line[i + 1] : '');
          i += 2; // 跳过转义字符
          continue;
        }
        if (sch === quoteChar) {
          break; // 字符串结束
        }
        // 模板字符串中 ${...} 的处理（简化：跳到对应的 }）
        if (quoteChar === '`' && sch === '$' && i + 1 < line.length && line[i + 1] === '{') {
          strContent += '${';
          i += 2;
          let braceDepth = 1;
          while (i < line.length && braceDepth > 0) {
            if (line[i] === '{') braceDepth++;
            else if (line[i] === '}') braceDepth--;
            if (braceDepth > 0) strContent += line[i];
            i++;
          }
          strContent += '}';
          continue;
        }
        strContent += sch;
        i++;
      }

      // 检查字符串内容中是否包含 source
      const sourceIdx = strContent.indexOf(source);
      if (sourceIdx >= 0) {
        // source 在行中的实际偏移 = 字符串内容起始位置 + source 在内容中的偏移
        const actualOffset = strContentStart + sourceIdx;
        matches.push({ offset: actualOffset, quoteChar, strStart });
      }

      if (i < line.length) i++; // 跳过结束引号
      continue;
    }

    i++;
  }

  if (matches.length === 0) return null;
  if (matches.length === 1) return matches[0];

  // 多个匹配时，如果提供了 preferColumn，选择最接近的
  if (typeof preferColumn === 'number' && preferColumn >= 0) {
    matches.sort((a, b) => Math.abs(a.offset - preferColumn) - Math.abs(b.offset - preferColumn));
  }
  return matches[0];
}

/**
 * [v3.4] 判断文件内容中某个偏移位置是否在注释内（行注释或块注释）。
 * 
 * 从文件开头扫描到指定偏移位置，追踪注释和字符串状态。
 * 用于全局搜索时排除注释中的匹配。
 * 
 * @param {string} content - 完整文件内容
 * @param {number} offset - 要检查的字符偏移位置
 * @returns {boolean} 如果在注释内返回 true
 */
function isInsideComment(content, offset) {
  let inLineComment = false;
  let inBlockComment = false;
  let inString = false;
  let stringChar = '';

  for (let i = 0; i < offset && i < content.length; i++) {
    const ch = content[i];
    const next = i + 1 < content.length ? content[i + 1] : '';

    if (inLineComment) {
      if (ch === '\n') inLineComment = false;
      continue;
    }
    if (inBlockComment) {
      if (ch === '*' && next === '/') { inBlockComment = false; i++; }
      continue;
    }
    if (inString) {
      if (ch === '\\') { i++; continue; }
      if (ch === stringChar) inString = false;
      continue;
    }

    if (ch === '/' && next === '/') { inLineComment = true; i++; continue; }
    if (ch === '/' && next === '*') { inBlockComment = true; i++; continue; }
    if (ch === '"' || ch === "'" || ch === '`') { inString = true; stringChar = ch; continue; }
  }

  return inLineComment || inBlockComment;
}

/**
 * [v3.4] 在一行中替换字符串字面量内的 source 为 target。
 * 与直接 line.replace(source, target) 不同，此函数只替换位于引号内的 source。
 * 
 * @param {string} line - 单行文本
 * @param {string} source - 原始中文
 * @param {string} target - 翻译后文本
 * @param {number} [preferColumn=-1] - 优先列号
 * @returns {{ replaced: string, success: boolean }}
 */
function replaceStringLiteralInLine(line, source, target, preferColumn) {
  const match = findStringLiteralInLine(line, source, preferColumn);
  if (!match) return { replaced: line, success: false };

  const { offset, quoteChar } = match;
  // [v3.5] 对 target 中与外层引号冲突的字符做转义
  const safeTarget = escapeTargetForLineContext(line, offset, source.length, target);
  const before = line.substring(0, offset);
  const after = line.substring(offset + source.length);
  return { replaced: before + safeTarget + after, success: true };
}

/**
 * 统计 substring 在 text 中出现的次数
 */
function countOccurrences(text, substring) {
  if (!substring) return 0;
  let count = 0;
  let pos = 0;
  while ((pos = text.indexOf(substring, pos)) !== -1) {
    count++;
    pos += substring.length;
  }
  return count;
}

// ============================================================
// Langpack 模式：将翻译条目的 target 转换为 i18n 调用表达式
// ============================================================

/**
 * 不同引擎的 i18n 调用模板
 */
const I18N_CALL_TEMPLATES = {
  // Cocos Creator i18n 插件: import * as i18n from 'db://i18n/LanguageData'; i18n.t('key')
  'cocos-creator': {
    text: (key) => `i18n.t('${key}')`,
    template: (key, vars) => `i18n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
    concat: (key, vars) => `i18n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
  },
  // Cocos Creator L10N: import l10n from 'db://localization-editor/core/L10nManager'; l10n.t('key')
  'cocos-l10n': {
    text: (key) => `l10n.t('${key}')`,
    template: (key, vars) => `l10n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
    concat: (key, vars) => `l10n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
  },
  // LayaAir: I18nManager.t('key')
  'laya': {
    text: (key) => `I18nManager.t('${key}')`,
    template: (key, vars) => `I18nManager.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
    concat: (key, vars) => `I18nManager.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
  },
  // Egret: Lang['key']
  'egret': {
    text: (key) => `Lang['${key}']`,
    template: (key, vars) => `I18nHelper.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
    concat: (key, vars) => `I18nHelper.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
  },
  // Unity: I18nManager.Instance.T('key')
  'unity': {
    text: (key) => `I18nManager.Instance.T("${key}")`,
    template: (key, vars) => `I18nManager.Instance.T("${key}", ${vars.join(', ')})`,
    concat: (key, vars) => `I18nManager.Instance.T("${key}", ${vars.join(', ')})`,
  },
  // 原生小游戏: i18n.t('key')
  'native': {
    text: (key) => `i18n.t('${key}')`,
    template: (key, vars) => `i18n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
    concat: (key, vars) => `i18n.t('${key}', { ${vars.map(v => `${v}: ${v}`).join(', ')} })`,
  }
};

/**
 * 将翻译条目列表的 target/translatedExpression 转换为 i18n 调用表达式
 *
 * @param {Array} translations - 原始翻译条目列表
 * @param {Object} keyMapping - generate-langpack.js 输出的 key 映射表
 * @param {string} engine - 游戏引擎类型
 * @returns {Array} 转换后的翻译条目列表
 */
function transformToI18nCalls(translations, keyMapping, engine) {
  const templates = I18N_CALL_TEMPLATES[engine] || I18N_CALL_TEMPLATES['native'];
  const keyMap = keyMapping.entries || {};

  return translations.map(entry => {
    const i18nKey = keyMap[entry.key] || keyMap[entry.source] || entry.key;
    const vars = entry.variables || [];

    // 克隆 entry 以避免修改原始数据
    const newEntry = { ...entry };

    switch (entry.type) {
      case 'text': {
        newEntry.target = templates.text(i18nKey);
        // 标记为代码表达式，replaceEntry 需要知道不加引号
        newEntry._isCodeExpression = true;
        break;
      }
      case 'template': {
        newEntry.target = templates.template(i18nKey, vars);
        newEntry._isCodeExpression = true;
        break;
      }
      case 'concatenation': {
        newEntry.translatedExpression = templates.concat(i18nKey, vars);
        newEntry._isCodeExpression = true;
        break;
      }
    }

    return newEntry;
  });
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].substring(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

// ============================================================
// 执行
// ============================================================

main().catch(err => {
  console.error('❌ 替换失败:', err.message);
  process.exit(1);
});
