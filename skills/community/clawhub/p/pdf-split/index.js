#!/usr/bin/env node

/**
 * PDF Split Skill
 * 拆分 PDF 文件，支持批量处理
 */

const fs = require('fs');
const path = require('path');
const { PDFDocument } = require('pdf-lib');

async function splitPDF(pdfFile, mode = 'single', pages = null, outputDir, prefix = '') {
  console.log(`📥 正在处理 PDF: ${pdfFile}`);
  
  if (!fs.existsSync(pdfFile)) {
    throw new Error(`文件不存在：${pdfFile}`);
  }
  
  const pdfBytes = fs.readFileSync(pdfFile);
  const pdf = await PDFDocument.load(pdfBytes);
  const totalPages = pdf.getPageCount();
  
  console.log(`📄 PDF 共 ${totalPages} 页`);
  
  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputFiles = [];
  const baseName = path.parse(pdfFile).name;
  
  if (mode === 'single') {
    // 拆分为单页
    console.log('✂️ 拆分为单页...');
    
    for (let i = 0; i < totalPages; i++) {
      const newPdf = await PDFDocument.create();
      const [copiedPage] = await newPdf.copyPages(pdf, [i]);
      newPdf.addPage(copiedPage);
      
      const outputName = path.join(outputDir, `${prefix}${baseName}_page${i + 1}.pdf`);
      const newPdfBytes = await newPdf.save();
      fs.writeFileSync(outputName, newPdfBytes);
      
      outputFiles.push(outputName);
      console.log(`  → ${outputName}`);
    }
    
  } else if (mode === 'range' && pages) {
    // 按页码范围拆分
    console.log(`✂️ 按页码范围拆分：${pages}`);
    
    const pageRanges = parsePageRanges(pages, totalPages);
    
    for (let r = 0; r < pageRanges.length; r++) {
      const range = pageRanges[r];
      const newPdf = await PDFDocument.create();
      
      for (let i = range.start; i <= range.end; i++) {
        const [copiedPage] = await newPdf.copyPages(pdf, [i - 1]);
        newPdf.addPage(copiedPage);
      }
      
      const outputName = path.join(outputDir, `${prefix}${baseName}_part${r + 1}_${range.start}-${range.end}.pdf`);
      const newPdfBytes = await newPdf.save();
      fs.writeFileSync(outputName, newPdfBytes);
      
      outputFiles.push(outputName);
      console.log(`  → ${outputName}`);
    }
  }
  
  console.log(`✅ 完成！生成 ${outputFiles.length} 个文件`);
  
  return outputFiles;
}

// 解析页码范围
function parsePageRanges(input, totalPages) {
  const ranges = [];
  const parts = input.split(',');
  
  for (const part of parts) {
    const trimmed = part.trim();
    if (trimmed.includes('-')) {
      const [startStr, endStr] = trimmed.split('-');
      const start = parseInt(startStr.trim());
      const end = parseInt(endStr.trim()) || totalPages;
      
      if (start >= 1 && end <= totalPages && start <= end) {
        ranges.push({ start, end });
      }
    } else {
      const page = parseInt(trimmed);
      if (page >= 1 && page <= totalPages) {
        ranges.push({ start: page, end: page });
      }
    }
  }
  
  return ranges;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法：');
    console.log('  node index.js split <PDF 文件> --mode <single|range> -o <输出目录> [选项]');
    console.log('');
    console.log('选项：');
    console.log('  --mode <single|range>  拆分模式（默认：single）');
    console.log('  --pages <range>        页码范围（mode=range 时必需）');
    console.log('  -o <dir>               输出目录');
    console.log('  --prefix <text>        输出文件前缀');
    console.log('');
    console.log('示例：');
    console.log('  node index.js split document.pdf --mode single -o pages/');
    console.log('  node index.js split document.pdf --mode range --pages "1-3,5-7" -o output/');
    console.log('  node index.js split document.pdf --mode single -o pages/ --prefix "page_"');
    process.exit(1);
  }
  
  const mode = args[0];
  
  if (mode === 'split') {
    let inputFile = null;
    let splitMode = 'single';
    let pages = null;
    let outputDir = './output';
    let prefix = '';
    
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--mode' && args[i + 1]) {
        splitMode = args[i + 1];
        i++;
      } else if (args[i] === '--pages' && args[i + 1]) {
        pages = args[i + 1];
        i++;
      } else if (args[i] === '-o' && args[i + 1]) {
        outputDir = args[i + 1];
        i++;
      } else if (args[i] === '--prefix' && args[i + 1]) {
        prefix = args[i + 1];
        i++;
      } else if (!inputFile) {
        inputFile = args[i];
      }
    }
    
    if (!inputFile) {
      console.error('❌ 错误：请指定 PDF 文件');
      process.exit(1);
    }
    
    if (splitMode === 'range' && !pages) {
      console.error('❌ 错误：range 模式需要指定 --pages 参数');
      process.exit(1);
    }
    
    splitPDF(inputFile, splitMode, pages, outputDir, prefix)
      .then(() => process.exit(0))
      .catch(err => {
        console.error('❌ 错误:', err.message);
        process.exit(1);
      });
      
  } else {
    console.error('❌ 错误：未知模式，请使用 split');
    process.exit(1);
  }
}

module.exports = { splitPDF };
