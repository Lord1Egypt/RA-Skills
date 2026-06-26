#!/usr/bin/env node
/**
 * PDF合并工具
 * 使用Ghostscript合并多个PDF文件
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function mergePDFs(inputFiles, outputFile) {
  // 验证输入文件
  for (const file of inputFiles) {
    if (!fs.existsSync(file)) {
      throw new Error(`文件不存在: ${file}`);
    }
  }

  // 确保输出目录存在
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 使用Ghostscript合并PDF
  const inputPaths = inputFiles.map(f => `"${path.resolve(f)}"`).join(' ');
  const outputPath = `"${path.resolve(outputFile)}"`;
  
  const command = `gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=${outputPath} ${inputPaths}`;
  
  try {
    execSync(command, { stdio: 'inherit' });
    console.log(`✅ PDF合并成功: ${outputFile}`);
    return true;
  } catch (error) {
    console.error('❌ PDF合并失败:', error.message);
    return false;
  }
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('用法: node merge.js <input1.pdf> [input2.pdf ...] <output.pdf>');
    process.exit(1);
  }
  
  const outputFile = args.pop();
  const inputFiles = args;
  
  mergePDFs(inputFiles, outputFile);
}

module.exports = { mergePDFs };