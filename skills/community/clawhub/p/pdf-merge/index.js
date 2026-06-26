#!/usr/bin/env node

/**
 * PDF Merge Skill
 * 合并多个 PDF 文件，支持压缩和元数据编辑
 */

const fs = require('fs');
const path = require('path');
const { PDFDocument } = require('pdf-lib');

async function mergePDFs(inputFiles, outputFile, options = {}) {
  const { compress = false, title, author, subject, keywords } = options;
  
  console.log(`📥 正在合并 ${inputFiles.length} 个 PDF 文件...`);
  
  // 创建新的 PDF 文档
  const mergedPdf = await PDFDocument.create();
  
  for (const file of inputFiles) {
    console.log(`  - 读取：${file}`);
    
    if (!fs.existsSync(file)) {
      throw new Error(`文件不存在：${file}`);
    }
    
    const pdfBytes = fs.readFileSync(file);
    const pdf = await PDFDocument.load(pdfBytes);
    
    // 复制所有页面
    const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    copiedPages.forEach((page) => mergedPdf.addPage(page));
  }
  
  // 添加元数据
  if (title) mergedPdf.setTitle(title);
  if (author) mergedPdf.setAuthor(author);
  if (subject) mergedPdf.setSubject(subject);
  if (keywords) mergedPdf.setKeywords(keywords);
  
  // 保存合并后的 PDF
  const mergedPdfBytes = await mergedPdf.save({
    useObjectStreams: compress // 压缩选项
  });
  
  fs.writeFileSync(outputFile, mergedPdfBytes);
  
  console.log(`✅ 完成！输出文件：${outputFile}`);
  console.log(`📊 文件大小：${(mergedPdfBytes.length / 1024 / 1024).toFixed(2)} MB`);
  
  if (compress) {
    console.log('🗜️ 已启用压缩');
  }
  
  return outputFile;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法：');
    console.log('  node index.js merge <PDF1> <PDF2> ... -o <输出文件> [选项]');
    console.log('');
    console.log('选项：');
    console.log('  --compress      启用压缩');
    console.log('  --title <text>  设置标题');
    console.log('  --author <text> 设置作者');
    console.log('  --subject <text> 设置主题');
    console.log('  --keywords <text> 设置关键词');
    console.log('');
    console.log('示例：');
    console.log('  node index.js merge file1.pdf file2.pdf -o merged.pdf');
    console.log('  node index.js merge file1.pdf -o compressed.pdf --compress');
    console.log('  node index.js merge file1.pdf -o output.pdf --title "标题" --author "作者"');
    process.exit(1);
  }
  
  const mode = args[0];
  
  if (mode === 'merge') {
    const inputFiles = [];
    let outputFile = `merged-${Date.now()}.pdf`;
    const options = {
      compress: false,
      title: null,
      author: null,
      subject: null,
      keywords: null
    };
    
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '-o' && args[i + 1]) {
        outputFile = args[i + 1];
        i++;
      } else if (args[i] === '--compress') {
        options.compress = true;
      } else if (args[i] === '--title' && args[i + 1]) {
        options.title = args[i + 1];
        i++;
      } else if (args[i] === '--author' && args[i + 1]) {
        options.author = args[i + 1];
        i++;
      } else if (args[i] === '--subject' && args[i + 1]) {
        options.subject = args[i + 1];
        i++;
      } else if (args[i] === '--keywords' && args[i + 1]) {
        options.keywords = args[i + 1];
        i++;
      } else if (args[i].endsWith('.pdf')) {
        inputFiles.push(args[i]);
      }
    }
    
    if (inputFiles.length < 1) {
      console.error('❌ 错误：至少需要 1 个 PDF 文件');
      process.exit(1);
    }
    
    mergePDFs(inputFiles, outputFile, options)
      .then(() => process.exit(0))
      .catch(err => {
        console.error('❌ 错误:', err.message);
        process.exit(1);
      });
      
  } else {
    console.error('❌ 错误：未知模式，请使用 merge');
    process.exit(1);
  }
}

module.exports = { mergePDFs };
