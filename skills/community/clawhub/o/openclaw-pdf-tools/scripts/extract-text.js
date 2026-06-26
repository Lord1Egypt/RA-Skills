#!/usr/bin/env node
/**
 * PDF文字提取工具
 * 使用pdftotext提取PDF中的文本
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function extractText(inputFile, outputFile = null, options = {}) {
  if (!fs.existsSync(inputFile)) {
    throw new Error(`文件不存在: ${inputFile}`);
  }

  const inputPath = path.resolve(inputFile);
  
  let outputPath;
  if (outputFile) {
    outputPath = path.resolve(outputFile);
  } else {
    outputPath = inputPath.replace(/\.pdf$/i, '.txt');
  }
  
  // 构建命令
  const layout = options.preserveLayout ? '-layout' : '';
  const command = `pdftotext ${layout} "${inputPath}" "${outputPath}"`;
  
  try {
    execSync(command, { stdio: 'pipe' });
    
    const text = fs.readFileSync(outputPath, 'utf-8');
    console.log(`✅ 文字提取成功: ${outputPath}`);
    console.log(`📊 提取字符数: ${text.length}`);
    
    return text;
  } catch (error) {
    console.error('❌ 文字提取失败:', error.message);
    console.log('提示: 请确保已安装 poppler-utils');
    return null;
  }
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log('用法: node extract-text.js <input.pdf> [output.txt]');
    console.log('选项: --preserve-layout 保留原始布局');
    process.exit(1);
  }
  
  const inputFile = args[0];
  const outputFile = args[1];
  const options = {
    preserveLayout: args.includes('--preserve-layout')
  };
  
  extractText(inputFile, outputFile, options);
}

module.exports = { extractText };