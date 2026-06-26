#!/usr/bin/env node
/**
 * PDF 和图片文本提取工具
 * 支持 PDF 文本提取（优先 pdfplumber，失败则 OCR）
 * 支持图片 OCR（Tesseract.js）
 */

const Tesseract = require('tesseract.js');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

/**
 * 从 PDF 提取文本（优先 pdfplumber，失败则 OCR）
 * @param {string} pdfPath - PDF 文件路径
 * @returns {Promise<string>} 提取的文本
 */
async function extractTextFromPDF(pdfPath) {
  try {
    const result = spawnSync('python3', [
      '-c',
      `import pdfplumber
import sys
try:
    with pdfplumber.open("${pdfPath}") as pdf:
        text = "\\n".join([page.extract_text() or "" for page in pdf.pages])
        print(text)
except Exception as e:
    print(f"ERROR:{e}", file=sys.stderr)
    sys.exit(1)`
    ], { encoding: 'utf8' });

    if (result.status === 0 && result.stdout && result.stdout.trim()) {
      console.error('  ✓ PDF 文本提取成功 (pdfplumber)');
      return result.stdout;
    }
    return await extractTextFromPDFByOCR(pdfPath);
  } catch (error) {
    return await extractTextFromPDFByOCR(pdfPath);
  }
}

/**
 * PDF OCR 提取（将 PDF 转为图片后 OCR）
 * @param {string} pdfPath - PDF 文件路径
 * @returns {Promise<string>} 提取的文本
 */
async function extractTextFromPDFByOCR(pdfPath) {
  const tempDir = path.join('/tmp', 'pdf_ocr_' + Date.now());
  fs.mkdirSync(tempDir, { recursive: true });
  
  // 使用 pdftoppm 将 PDF 转为 PNG
  spawnSync('pdftoppm', ['-png', pdfPath, `${tempDir}/page`], { stdio: 'ignore' });
  
  const images = fs.readdirSync(tempDir).filter(f => f.endsWith('.png')).sort();
  let fullText = '';
  
  for (const img of images) {
    const worker = await Tesseract.createWorker('chi_sim+eng', 1);
    const result = await worker.recognize(path.join(tempDir, img));
    fullText += result.data.text + '\n';
    await worker.terminate();
  }
  
  fs.rmSync(tempDir, { recursive: true, force: true });
  console.error('  ✓ PDF OCR 完成');
  return fullText;
}

/**
 * 从图片提取文本（OCR）
 * @param {string} imagePath - 图片文件路径
 * @returns {Promise<string>} 提取的文本
 */
async function extractTextFromImage(imagePath) {
  const worker = await Tesseract.createWorker('chi_sim+eng', 1);
  const result = await worker.recognize(imagePath);
  await worker.terminate();
  console.error('  ✓ OCR 完成');
  return result.data.text;
}

module.exports = {
  extractTextFromPDF,
  extractTextFromPDFByOCR,
  extractTextFromImage
};
