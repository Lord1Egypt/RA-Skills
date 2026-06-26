#!/usr/bin/env node
/**
 * PDF压缩工具
 * 使用Ghostscript压缩PDF
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function compressPDF(inputFile, outputFile, quality = 'ebook') {
  if (!fs.existsSync(inputFile)) {
    throw new Error(`文件不存在: ${inputFile}`);
  }

  const inputPath = path.resolve(inputFile);
  const outputPath = path.resolve(outputFile);
  
  // 确保输出目录存在
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 质量选项
  const qualitySettings = {
    'screen': '-dPDFSETTINGS=/screen',     // 72 dpi, 最小文件
    'ebook': '-dPDFSETTINGS=/ebook',       // 150 dpi, 中等质量
    'printer': '-dPDFSETTINGS=/printer',   // 300 dpi, 高质量
    'prepress': '-dPDFSETTINGS=/prepress'  // 300 dpi, 最高质量
  };
  
  const qualityOption = qualitySettings[quality] || qualitySettings['ebook'];
  
  const command = `gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite ${qualityOption} -sOutputFile="${outputPath}" "${inputPath}"`;
  
  try {
    // 获取原始文件大小
    const originalSize = fs.statSync(inputFile).size;
    
    execSync(command, { stdio: 'pipe' });
    
    // 获取压缩后文件大小
    const compressedSize = fs.statSync(outputPath).size;
    const reduction = ((1 - compressedSize / originalSize) * 100).toFixed(1);
    
    console.log(`✅ PDF压缩成功: ${outputFile}`);
    console.log(`📊 原始大小: ${(originalSize / 1024).toFixed(1)} KB`);
    console.log(`📊 压缩后大小: ${(compressedSize / 1024).toFixed(1)} KB`);
    console.log(`📊 压缩率: ${reduction}%`);
    
    return true;
  } catch (error) {
    console.error('❌ PDF压缩失败:', error.message);
    return false;
  }
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('用法: node compress.js <input.pdf> <output.pdf> [quality]');
    console.log('质量选项: screen (最小), ebook (默认), printer, prepress');
    process.exit(1);
  }
  
  const [inputFile, outputFile, quality] = args;
  compressPDF(inputFile, outputFile, quality);
}

module.exports = { compressPDF };