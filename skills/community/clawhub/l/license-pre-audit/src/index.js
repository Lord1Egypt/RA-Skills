#!/usr/bin/env node
/**
 * License Pre-Audit - 进出口许可文档智能预审系统
 * 
 * 支持：
 * 1. CLI 命令行：许可证文件夹/压缩包路径地址
 * 2. 对话交互：上传许可证压缩包/文件夹目录/路径地址
 * 
 * 流程结构：
 * 1. 扫描许可证文件夹/解压压缩包 -> 2. 验证文件类型 -> 3. 提取文本 (PDF/图片) 
 * 4. LLM 字段提取 -> 5. 盖章检测校准 -> 6. 执行 11 条审核规则 
 * 7. 生成 JSON 报告 + Markdown 表格
 */

const fs = require('fs');
const path = require('path');

// 导入依赖检测模块
const { ensureDependencies } = require('./utils/check-deps');

// 导入工具模块
const { extractTextFromPDF, extractTextFromImage } = require('./utils/pdf-ocr');
const { detectStampByKeywords } = require('./utils/stamp-detect');
const { normalizeFields, removeHasStamp } = require('./utils/field-normalize');
const { runAllRules } = require('./rules');
const { callLLM } = require('./utils/llm-client');

// 导入压缩包处理工具
const { extractArchive, filterValidFiles, detectArchiveType } = require('./utils/extract-archive');

// 导入表格生成工具
const { generateTableData } = require('./utils/generate-table');

// 导入 Prompt（从 MD 文件读取）
const EXTRACT_PROMPT = fs.readFileSync(path.join(__dirname, 'prompts/extract-fields.md'), 'utf8');
const AUDIT_PROMPT = fs.readFileSync(path.join(__dirname, 'prompts/audit-rules.md'), 'utf8');

// 读取配置文件
const configPath = path.join(__dirname, '..', 'references', 'settings.json');
const skillRootDir = path.resolve(__dirname, '..'); // 技能根目录（相对于 src/index.js 向上一级）
const config = fs.existsSync(configPath)
  ? JSON.parse(fs.readFileSync(configPath, 'utf8'))
  : {
    extractPath: path.join(process.env.HOME || process.env.USERPROFILE, 'Documents', 'licence_pre_audit', 'license-audit-upload', 'files'),
    reportPath: path.join(process.env.HOME || process.env.USERPROFILE, 'Documents', 'licence_pre_audit', 'license-audit-upload', 'reports'),
    allowedExtensions: ['.pdf', '.jpg', '.jpeg', '.png', '.webp']
  };

// 将相对路径转换为绝对路径（基于技能根目录）
if (config.extractPath && !path.isAbsolute(config.extractPath)) {
  config.extractPath = path.join(skillRootDir, config.extractPath);
}
if (config.reportPath && !path.isAbsolute(config.reportPath)) {
  config.reportPath = path.join(skillRootDir, config.reportPath);
}

/**
 * 生成北京时间戳（UTC+8）
 * 格式：YYYYMMDDHHmmssSSS（年月日时分秒 +3 位毫秒）
 * @returns {string} 北京时间戳
 */
function getBeijingTimestamp() {
  const now = new Date();
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000); // 加 8 小时
  const year = beijingTime.getUTCFullYear();
  const month = String(beijingTime.getUTCMonth() + 1).padStart(2, '0');
  const day = beijingTime.getUTCDate().toString().padStart(2, '0');
  const hours = String(beijingTime.getUTCHours()).padStart(2, '0');
  const minutes = String(beijingTime.getUTCMinutes()).padStart(2, '0');
  const seconds = String(beijingTime.getUTCSeconds()).padStart(2, '0');
  const ms = String(beijingTime.getUTCMilliseconds()).padStart(3, '0');
  return `${year}${month}${day}${hours}${minutes}${seconds}${ms}`;
}

/**
 * 主函数入口
 */
async function main() {
  // 1. 检测并自动安装依赖
  console.error('\n🚀 License Pre-Audit - 进出口文档智能预审系统');
  console.error('═══════════════════════════════════════════\n');
  
  const depsReady = await ensureDependencies();
  if (!depsReady) {
    console.error('\n❌ 依赖安装失败，请手动安装后重试');
    process.exit(1);
  }
  
  // 获取命令行参数
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('用法：node index.js <文件夹路径或压缩包路径>');
    console.error('示例:');
    console.error('  node index.js ./my-folder');
    console.error('  node index.js ./my-archive.zip');
    console.error('  node index.js /path/to/documents');
    process.exit(1);
  }
  
  const inputPath = args[0];
  
  // 验证路径是否存在
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ 路径不存在：${inputPath}`);
    process.exit(1);
  }
  
  // 2. 开始处理文档
  await processInput(inputPath);
}

/**
 * 处理输入（文件夹或压缩包）
 */
async function processInput(originalInput) {
  // 1. 判断输入是压缩包还是目录
  let workDir;
  let isArchive = false;
  let beijingTimestamp = null; // 用于解压目录和报告文件名的统一时间戳

  if (!fs.existsSync(originalInput)) {
    console.error('❌ 路径不存在:', originalInput);
    process.exit(1);
  }

  const stats = fs.statSync(originalInput);

  if (stats.isFile()) {
    // 检查是否是压缩包
    const archiveType = detectArchiveType(originalInput);

    if (archiveType !== 'unknown') {
      // 是压缩包，需要解压
      isArchive = true;
      beijingTimestamp = getBeijingTimestamp();
      workDir = path.join(config.extractPath, beijingTimestamp);

      console.error('📦 检测到压缩包，开始解压...');
      console.error('📂 解压目录:', workDir);
      try {
        extractArchive(originalInput, workDir);
      } catch (error) {
        console.error('❌ 解压失败:', error.message);
        process.exit(1);
      }
    } else {
      console.error('❌ 不支持的文件格式:', originalInput);
      console.error('支持：文件夹、.zip、.rar、.tar、.tar.gz、.tgz');
      process.exit(1);
    }
  } else if (stats.isDirectory()) {
    workDir = originalInput;
    console.error('📂 检测到目录:', workDir);
  } else {
    console.error('❌ 无效的路径类型:', originalInput);
    process.exit(1);
  }

  // 2. 扫描文件并验证类型
  console.error('🔍 扫描文件并验证类型...');
  const allFiles = fs.readdirSync(workDir, { recursive: true })
    .filter(f => !f.startsWith('.') && !f.includes('__MACOSX'))
    .map(f => path.join(workDir, f))
    .filter(f => fs.statSync(f).isFile());

  const validFiles = filterValidFiles(allFiles, config.allowedExtensions);
  const invalidFiles = allFiles.filter(f => !validFiles.includes(f));

  console.error(`  📂 总共 ${allFiles.length} 个文件`);
  console.error(`  ✅ 有效文件 ${validFiles.length} 个 (${config.allowedExtensions.join(', ')})`);

  if (invalidFiles.length > 0) {
    console.error(`  ⚠️  跳过 ${invalidFiles.length} 个不支持的文件:`);
    invalidFiles.forEach(f => console.error(`    - ${path.basename(f)}`));
  }

  if (validFiles.length === 0) {
    console.error('❌ 没有有效的文档文件');
    if (isArchive) fs.rmSync(workDir, { recursive: true, force: true });
    process.exit(1);
  }

  console.error();

  // 3. 处理每个文件
  const results = [];

  for (const filePath of validFiles) {
    const result = await processDocument(filePath);
    if (result) results.push(result);
    console.error();
  }

  // 4. 执行审核规则
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.error('📊 执行 11 条审核规则...');

  const auditSummary = runAllRules(results);
  console.error('  📋 审核结果:', auditSummary.reviewResult);
  if (auditSummary.reviewDetail) {
    console.error('  📝 详情:');
    auditSummary.reviewDetail.split('\n').forEach(l => l.trim() && console.error('    ' + l));
  }
  console.error();

  // 5. 生成报告（使用北京时间 UTC+8）
  // 如果是压缩包模式，使用解压时生成的时间戳；否则重新生成
  const timestamp = beijingTimestamp || getBeijingTimestamp();
  
  // JSON 报告中的 timestamp 格式：2026-04-24 14:24:55 534
  const year = timestamp.slice(0, 4);
  const month = timestamp.slice(4, 6);
  const day = timestamp.slice(6, 8);
  const hours = timestamp.slice(8, 10);
  const minutes = timestamp.slice(10, 12);
  const seconds = timestamp.slice(12, 14);
  const ms = timestamp.slice(14, 17);
  const timestampFormatted = `${year}-${month}-${day} ${hours}:${minutes}:${seconds} ${ms}`;
  
  const folderName = path.basename(workDir);
  const reportName = `audit-result-${timestamp}.json`;
  const markdownName = `audit-result-${timestamp}.md`;

  // 创建报告目录
  const reportDir = config.reportPath;
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  const reportPath = path.join(reportDir, reportName);
  const markdownPath = path.join(reportDir, markdownName);

  const report = {
    timestamp: timestampFormatted,  // 北京时间格式：2026-04-24 14:24:55 534
    folder: workDir,
    isArchive: isArchive,
    originalInput: originalInput,
    totalFiles: allFiles.length,
    validFiles: validFiles.length,
    processedFiles: results.length,
    auditResults: results.map(r => ({
      filename: r.filename,
      docType: r.docType,
      extractedFields: r.analysis,
      hasStamp: r.hasStamp
    })),
    auditSummary: auditSummary
  };

  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

  // 生成 Markdown 表格
  const tableData = generateTableData(report);
  fs.writeFileSync(markdownPath, tableData.markdown);

  // 直接在聊天界面显示 Markdown 表格（企业微信能正确渲染）
  // 使用 process.stdout.write 确保输出到 stdout，OpenClaw 会捕获并渲染
  const markdownContent = fs.readFileSync(markdownPath, 'utf8');
  process.stdout.write('\n📋 审核结果表格：\n\n');
  process.stdout.write(markdownContent); // 直接输出表格内容到 stdout
  process.stdout.write('\n');

  // 显示报告保存路径（完整绝对路径）
  console.error('💾 报告已保存（完整路径）：');
  console.error('  JSON 报告:', path.resolve(reportPath));
  console.error('  MD 表格:', path.resolve(markdownPath));

  return { markdownPath: path.resolve(markdownPath), markdownContent };
}

/**
 * 调用 LLM 提取字段
 * @param {string} text - 文档文本
 * @param {string} filename - 文件名
 * @returns {Promise<Object>} 提取的字段
 */
async function extractFieldsWithLLM(text, filename) {
  const maxTextLength = 8000;
  const textToProcess = text.length > maxTextLength
    ? text.substring(0, maxTextLength) + '\n...（已截断）'
    : text;

  const userPrompt = `请分析以下文档，识别类型并提取字段：

文件名：${filename}

文档内容：
---
${textToProcess}
---

只返回 JSON，不要任何其他文字！`;

  console.error('  🤖 调用 LLM 提取字段...');
  const fields = callLLM(EXTRACT_PROMPT, userPrompt, { maxTextLength });

  if (fields) {
    console.error('  ✓ 提取完成');
    return fields;
  }

  console.error('  ✗ 提取失败');
  return null;
}

/**
 * 处理单个文档
 * @param {string} filePath - 文件路径
 * @returns {Promise<Object>} 处理结果
 */
async function processDocument(filePath) {
  const filename = path.basename(filePath);
  console.error(`📄 处理：${filename}`);

  const text = path.extname(filePath).toLowerCase() === '.pdf'
    ? await extractTextFromPDF(filePath)
    : await extractTextFromImage(filePath);

  if (!text) {
    console.error('  ❌ 提取失败');
    return null;
  }

  console.error(`  📝 文本长度：${text.length} 字符`);

  const fields = await extractFieldsWithLLM(text, filename);

  if (!fields) {
    console.error('  ✗ 字段提取失败');
    return null;
  }

  // 字段标准化
  const normalizedFields = normalizeFields(fields);

  // 混合模式盖章检测校准
  const docType = normalizedFields.fileType || '未知';
  if (!normalizedFields.hasStamp || normalizedFields.hasStamp === '否') {
    console.error('  🔍 LLM 未明确判定盖章，启动混合模式校准...');
    const calibratedStamp = detectStampByKeywords(text, docType, filename);
    normalizedFields.hasStamp = calibratedStamp ? '是' : '否';
    console.error(calibratedStamp ? '  ✓ 校准成功：判定为已盖章' : '  ✗ 校准失败：判定为未盖章');
  }

  console.error('  📋 类型:', normalizedFields.fileType);
  if (normalizedFields.contractNo) console.error('    合同号:', normalizedFields.contractNo);
  if (normalizedFields.exportCountry) console.error('    出口国:', normalizedFields.exportCountry);
  if (normalizedFields.importerEn) console.error('    进口商:', normalizedFields.importerEn);
  if (normalizedFields.totalAmount) console.error('    总金额:', normalizedFields.totalAmount);

  // 移除 fileType 和 hasStamp（避免在 extractedFields 中重复）
  const { fileType: _, hasStamp: __, ...extractedFields } = normalizedFields;
  return {
    filename,
    analysis: extractedFields,
    docType: normalizedFields.fileType,
    hasStamp: normalizedFields.hasStamp === '是'
  };
}



// 支持命令行调用
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main };
