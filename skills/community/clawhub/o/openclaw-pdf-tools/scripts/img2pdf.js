#!/usr/bin/env node
/**
 * 图片转PDF工具
 * 使用ImageMagick或img2pdf将图片转为PDF
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function imagesToPDF(inputFiles, outputFile) {
  // 验证输入文件
  for (const file of inputFiles) {
    if (!fs.existsSync(file)) {
      throw new Error(`文件不存在: ${file}`);
    }
  }

  const inputPaths = inputFiles.map(f => `"${path.resolve(f)}"`).join(' ');
  const outputPath = `"${path.resolve(outputFile)}"`;
  
  // 确保输出目录存在
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 尝试使用img2pdf（更好的PDF质量）
  try {
    execSync(`img2pdf ${inputPaths} -o ${outputPath}`, { stdio: 'pipe' });
    console.log(`✅ 图片转PDF成功: ${outputFile}`);
    return true;
  } catch {
    // 使用ImageMagick作为备选
    console.log('img2pdf不可用，尝试使用ImageMagick...');
    
    try {
      execSync(`convert ${inputPaths} ${outputPath}`, { stdio: 'pipe' });
      console.log(`✅ 图片转PDF成功: ${outputFile}`);
      return true;
    } catch (error) {
      console.error('❌ 图片转PDF失败:', error.message);
      console.log('提示: 请安装 img2pdf (pip install img2pdf) 或 ImageMagick');
      return false;
    }
  }
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('用法: node img2pdf.js <image1.png> [image2.jpg ...] <output.pdf>');
    process.exit(1);
  }
  
  const outputFile = args.pop();
  const inputFiles = args;
  
  imagesToPDF(inputFiles, outputFile);
}

module.exports = { imagesToPDF };