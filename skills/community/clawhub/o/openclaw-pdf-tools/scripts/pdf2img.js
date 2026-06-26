#!/usr/bin/env node
/**
 * PDF转图片工具
 * 使用pdftoppm将PDF页面转为图片
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function pdfToImages(inputFile, outputDir, options = {}) {
  if (!fs.existsSync(inputFile)) {
    throw new Error(`文件不存在: ${inputFile}`);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const inputPath = path.resolve(inputFile);
  const baseName = path.parse(inputFile).name;
  const dpi = options.dpi || 150;
  const format = options.format || 'png';
  
  // 使用pdftoppm转换
  const outputPath = path.join(outputDir, baseName);
  
  try {
    let command;
    if (format === 'png') {
      command = `pdftoppm -png -r ${dpi} "${inputPath}" "${outputPath}"`;
    } else if (format === 'jpg') {
      command = `pdftoppm -jpeg -r ${dpi} "${inputPath}" "${outputPath}"`;
    } else {
      command = `pdftoppm -png -r ${dpi} "${inputPath}" "${outputPath}"`;
    }
    
    execSync(command, { stdio: 'pipe' });
    
    // 统计生成的图片数量
    const files = fs.readdirSync(outputDir).filter(f => f.startsWith(baseName));
    console.log(`✅ PDF转图片成功，共生成 ${files.length} 张图片`);
    console.log(`📁 输出目录: ${outputDir}`);
    
    return files.map(f => path.join(outputDir, f));
  } catch (error) {
    console.error('❌ PDF转图片失败:', error.message);
    console.log('提示: 请确保已安装 poppler-utils');
    return [];
  }
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('用法: node pdf2img.js <input.pdf> <output_dir> [options]');
    console.log('选项:');
    console.log('  --dpi <number>  分辨率，默认150');
    console.log('  --format <type> 输出格式: png 或 jpg，默认png');
    process.exit(1);
  }
  
  const inputFile = args[0];
  const outputDir = args[1];
  
  const options = {};
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--dpi' && args[i + 1]) {
      options.dpi = parseInt(args[++i]);
    } else if (args[i] === '--format' && args[i + 1]) {
      options.format = args[++i];
    }
  }
  
  pdfToImages(inputFile, outputDir, options);
}

module.exports = { pdfToImages };