#!/usr/bin/env node
/**
 * PDF拆分工具
 * 使用pdftk或Ghostscript拆分PDF
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function splitPDF(inputFile, outputDirOrFile, pageRange = null) {
  if (!fs.existsSync(inputFile)) {
    throw new Error(`文件不存在: ${inputFile}`);
  }

  if (pageRange) {
    // 按页码范围拆分
    splitByRange(inputFile, outputDirOrFile, pageRange);
  } else {
    // 拆分为单页
    splitToPages(inputFile, outputDirOrFile);
  }
}

function splitToPages(inputFile, outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const inputPath = path.resolve(inputFile);
  const baseName = path.parse(inputFile).name;
  
  // 使用pdftk拆分（如果可用）
  try {
    execSync(`pdftk "${inputPath}" burst output "${outputDir}/${baseName}_%04d.pdf"`, { stdio: 'pipe' });
    console.log(`✅ PDF拆分成功，输出到: ${outputDir}`);
  } catch {
    // 使用Ghostscript作为备选
    console.log('pdftk不可用，尝试使用Ghostscript...');
    
    // 获取PDF页数
    const info = execSync(`pdfinfo "${inputPath}"`, { encoding: 'utf-8' });
    const pagesMatch = info.match(/Pages:\s+(\d+)/);
    const totalPages = pagesMatch ? parseInt(pagesMatch[1]) : 1;
    
    for (let i = 1; i <= totalPages; i++) {
      const outputFile = `${outputDir}/${baseName}_${String(i).padStart(4, '0')}.pdf`;
      execSync(`gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dFirstPage=${i} -dLastPage=${i} -sOutputFile="${outputFile}" "${inputPath}"`, { stdio: 'pipe' });
    }
    console.log(`✅ PDF拆分成功，共 ${totalPages} 页，输出到: ${outputDir}`);
  }
}

function splitByRange(inputFile, outputFile, pageRange) {
  const inputPath = path.resolve(inputFile);
  const outputPath = path.resolve(outputFile);
  
  // 解析页码范围 (如 "1-5" 或 "1,3,5")
  if (pageRange.includes('-')) {
    const [start, end] = pageRange.split('-').map(Number);
    execSync(`gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dFirstPage=${start} -dLastPage=${end} -sOutputFile="${outputPath}" "${inputPath}"`, { stdio: 'inherit' });
  } else {
    // 多个不连续页面需要pdftk
    const pages = pageRange.split(',').map(p => p.trim());
    execSync(`pdftk "${inputPath}" cat ${pages.join(' ')} output "${outputPath}"`, { stdio: 'inherit' });
  }
  
  console.log(`✅ PDF拆分成功: ${outputFile}`);
}

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('用法: node split.js <input.pdf> <output_dir|output.pdf> [页码范围]');
    console.log('示例:');
    console.log('  node split.js input.pdf output_dir/        # 拆分为单页');
    console.log('  node split.js input.pdf output.pdf 1-5     # 提取1-5页');
    console.log('  node split.js input.pdf output.pdf 1,3,5   # 提取第1,3,5页');
    process.exit(1);
  }
  
  const [inputFile, output, pageRange] = args;
  splitPDF(inputFile, output, pageRange);
}

module.exports = { splitPDF };