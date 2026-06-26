#!/usr/bin/env node

/**
 * OpenClaw技能安全扫描命令行工具
 * 将JavaScript API封装为可执行命令
 */

const { SkillScanner, SecurityReporter } = require('../dist/index.js');
const { HallucinationDetector } = require('../dist/hallucination-detector.js');
const path = require('path');
const fs = require('fs');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    scanPath: 'C:\\Users\\Administrator\\.openclaw\\workspace\\skills',
    outputFormat: 'text',
    enhancedReport: false,
    riskSummary: false,
    help: false,
    version: false,
    scanText: null  // 新增：直接扫描文本
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--version' || arg === '-v') {
      options.version = true;
    } else if (arg === '--format' || arg === '-f') {
      if (i + 1 < args.length) {
        const format = args[++i];
        if (['text', 'json', 'markdown', 'enhanced-text', 'enhanced-markdown'].includes(format)) {
          options.outputFormat = format;
        } else {
          console.error(`错误：不支持的输出格式 "${format}"，支持：text, json, markdown, enhanced-text, enhanced-markdown`);
          process.exit(1);
        }
      }
    } else if (arg === '--scan-path' || arg === '-p') {
      if (i + 1 < args.length) {
        options.scanPath = args[++i];
      }
    } else if (arg === '--enhanced' || arg === '-e') {
      options.enhancedReport = true;
    } else if (arg === '--risk-summary' || arg === '-r') {
      options.riskSummary = true;
    } else if (arg === '--text' || arg === '-t') {
      // 扫描指定文本
      if (i + 1 < args.length) {
        options.scanText = args[++i];
      }
    } else if (arg.startsWith('--')) {
      console.error(`错误：未知选项 "${arg}"`);
      process.exit(1);
    } else {
      // 第一个非选项参数作为扫描路径
      if (!options.scanPathSet) {
        options.scanPath = arg;
        options.scanPathSet = true;
      }
    }
  }

  return options;
}

// 显示帮助信息
function showHelp() {
  console.log(`
OpenClaw技能安全扫描工具 v1.0.4

用法：
  skill-security-scan [选项] [扫描路径]

选项：
  -h, --help                  显示帮助信息
  -v, --version               显示版本信息
  -f, --format <格式>         输出格式：text, json, markdown, enhanced-text, enhanced-markdown (默认: text)
  -p, --scan-path <路径>      要扫描的技能目录路径
  -e, --enhanced              生成增强报告（包含中高危技能详细清单）
  -r, --risk-summary          只显示中高危技能摘要
  -t, --text <文本>           直接扫描文本中的虚假信息/广告

输出格式说明：
  text             基本文本报告
  json             JSON格式报告
  markdown         Markdown格式报告
  enhanced-text    增强文本报告（包含中高危技能清单）
  enhanced-markdown 增强Markdown报告（包含中高危技能清单）

文本扫描示例：
  skill-security-scan --text "您的账号存在异常，请立即转账到安全账户"
  skill-security-scan -t "投资理财，每月稳赚10万"

示例：
  skill-security-scan
  skill-security-scan --format markdown
  skill-security-scan --format json
  skill-security-scan --format enhanced-text
  skill-security-scan --risk-summary
  skill-security-scan "C:\\path\\to\\skills"
  skill-security-scan --scan-path "C:\\path\\to\\skills" --format enhanced-markdown

环境变量：
  OPENCLAW_SKILLS_PATH  默认技能目录路径
`);
}

// 显示版本信息
function showVersion() {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
  console.log(`skill-security-scan v${packageJson.version}`);
}

// 主函数
async function main() {
  const options = parseArgs();

  if (options.help) {
    showHelp();
    return;
  }

  if (options.version) {
    showVersion();
    return;
  }

  // 如果指定了文本扫描，直接扫描文本
  if (options.scanText) {
    console.log(`🔍 扫描文本中的虚假信息...\n`);
    const detector = new HallucinationDetector();
    const result = await detector.scanText(options.scanText);
    
    console.log(`📝 扫描文本: "${options.scanText.substring(0, 50)}..."\n`);
    console.log(`📊 风险等级: ${result.riskLevel.toUpperCase()}`);
    console.log(`📋 检测结果: ${result.summary}\n`);
    
    if (result.detections.length > 0) {
      console.log(`🔴 检测到 ${result.detections.length} 个问题:\n`);
      result.detections.forEach((d, i) => {
        console.log(`  ${i + 1}. [${d.severity.toUpperCase()}] ${d.description}`);
        console.log(`     匹配内容: "${d.matched}"`);
        console.log(`     类别: ${d.category}`);
        console.log();
      });
    }
    
    console.log(`💡 建议:`);
    result.suggestions.forEach(s => console.log(`  ${s}`));
    
    return;
  }

  try {
    console.log(`🚀 开始安全扫描...`);
    console.log(`📁 扫描目录: ${options.scanPath}`);
    console.log(`📝 输出格式: ${options.outputFormat}`);
    console.log('='.repeat(50));

    // 检查目录是否存在
    if (!fs.existsSync(options.scanPath)) {
      console.error(`❌ 错误：扫描目录不存在 "${options.scanPath}"`);
      process.exit(1);
    }

    // 创建扫描器
    const scanner = new SkillScanner(options.scanPath);
    
    // 运行扫描
    console.log('🔍 扫描技能目录...');
    const report = await scanner.scan();
    
    // 生成报告
    const reporter = new SecurityReporter(report);
    
    let output;
    switch (options.outputFormat) {
      case 'json':
        output = JSON.stringify(report, null, 2);
        break;
      case 'markdown':
        output = reporter.generateMarkdownReport();
        break;
      case 'enhanced-text':
        output = reporter.generateEnhancedTextReport();
        break;
      case 'enhanced-markdown':
        output = reporter.generateEnhancedMarkdownReport();
        break;
      case 'text':
      default:
        output = reporter.generateTextReport();
        break;
    }
    
    // 如果指定了风险摘要，只显示摘要
    if (options.riskSummary) {
      output = reporter.generateRiskSummary();
    }

    console.log(output);
    console.log('\n' + '='.repeat(50));
    console.log('✅ 扫描完成！');

  } catch (error) {
    console.error('❌ 扫描失败：', error.message);
    if (error.stack) {
      console.error('堆栈跟踪：', error.stack);
    }
    process.exit(1);
  }
}

// 执行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('❌ 未处理的错误：', error);
    process.exit(1);
  });
}

module.exports = { parseArgs, showHelp, showVersion };