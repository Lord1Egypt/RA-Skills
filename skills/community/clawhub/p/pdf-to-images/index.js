#!/usr/bin/env node

/**
 * PDF to Images Skill
 * 将 PDF 转换为图片，支持指定分辨率和页码范围
 */

const fs = require('fs');
const path = require('path');
const pdfjs = require('pdfjs-dist');

// 设置 PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = require.resolve('pdfjs-dist/build/pdf.worker.min.js');

async function pdfToImages(pdfFile, output, format = 'png', scale = 2.0, pages = null) {
  console.log(`📥 正在转换 PDF: ${pdfFile}`);
  
  if (!fs.existsSync(pdfFile)) {
    throw new Error(`文件不存在：${pdfFile}`);
  }
  
  const pdfBytes = fs.readFileSync(pdfFile);
  const pdf = await pdfjs.getDocument({ data: pdfBytes }).promise;
  const totalPages = pdf.numPages;
  
  console.log(`📄 PDF 共 ${totalPages} 页`);
  
  // 解析页码范围
  let pageRanges = [];
  if (pages) {
    pageRanges = parsePageRanges(pages, totalPages);
    console.log(`📋 转换页面：${pageRanges.join(', ')}`);
  } else {
    pageRanges = Array.from({ length: totalPages }, (_, i) => i + 1);
  }
  
  const outputFiles = [];
  const baseName = path.parse(output).name;
  const dirName = path.dirname(output);
  const ext = format === 'jpg' ? 'jpg' : 'png';
  
  // 创建输出目录（如果是目录）
  if (!output.endsWith(`.${ext}`)) {
    if (!fs.existsSync(output)) {
      fs.mkdirSync(output, { recursive: true });
    }
  }
  
  for (const pageNum of pageRanges) {
    console.log(`  - 转换第 ${pageNum} 页...`);
    
    const page = await pdf.getPage(pageNum);
    const viewport = page.getViewport({ scale });
    
    // 创建 canvas（使用 node-canvas）
    const { createCanvas } = require('canvas');
    const canvas = createCanvas(viewport.width, viewport.height);
    const ctx = canvas.getContext('2d');
    
    const renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };
    
    await page.render(renderContext).promise;
    
    // 生成输出文件名
    const outputName = pageRanges.length > 1
      ? path.join(dirName, `${baseName}_page${pageNum}.${ext}`)
      : output;
    
    // 保存为图片
    const buffer = canvas.toBuffer(`image/${format}`);
    fs.writeFileSync(outputName, buffer);
    
    outputFiles.push(outputName);
    console.log(`    → ${outputName}`);
  }
  
  console.log(`✅ 完成！生成 ${outputFiles.length} 个图片文件`);
  
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
        for (let i = start; i <= end; i++) {
          ranges.push(i);
        }
      }
    } else {
      const page = parseInt(trimmed);
      if (page >= 1 && page <= totalPages) {
        ranges.push(page);
      }
    }
  }
  
  return ranges;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('用法：');
    console.log('  node index.js <PDF 文件> -o <输出文件/目录> [选项]');
    console.log('');
    console.log('选项：');
    console.log('  --format <png|jpg>  输出格式（默认：png）');
    console.log('  --scale <number>    缩放比例（默认：2.0，范围：0.5-5.0）');
    console.log('  --pages <range>     页码范围（例如："1-5" 或 "1,3,5"）');
    console.log('');
    console.log('示例：');
    console.log('  node index.js document.pdf -o output.png');
    console.log('  node index.js document.pdf -o output.jpg --format jpg');
    console.log('  node index.js document.pdf -o pages/ --pages "1-5" --scale 3.0');
    process.exit(1);
  }
  
  let outputFile = 'output.png';
  let format = 'png';
  let scale = 2.0;
  let pages = null;
  let inputFile = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-o' && args[i + 1]) {
      outputFile = args[i + 1];
      i++;
    } else if (args[i] === '--format' && args[i + 1]) {
      format = args[i + 1];
      i++;
    } else if (args[i] === '--scale' && args[i + 1]) {
      scale = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--pages' && args[i + 1]) {
      pages = args[i + 1];
      i++;
    } else if (!inputFile) {
      inputFile = args[i];
    }
  }
  
  if (!inputFile) {
    console.error('❌ 错误：请指定 PDF 文件');
    process.exit(1);
  }
  
  // 验证 scale
  if (scale < 0.5 || scale > 5.0) {
    console.error('❌ 错误：scale 必须在 0.5-5.0 之间');
    process.exit(1);
  }
  
  pdfToImages(inputFile, outputFile, format, scale, pages)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('❌ 错误:', err.message);
      process.exit(1);
    });
}

module.exports = { pdfToImages };
