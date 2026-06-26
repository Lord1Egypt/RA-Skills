#!/usr/bin/env node
/**
 * Job Hunter - PDF Resume Text Extractor
 * Extracts text from a PDF resume using pdfjs-dist.
 * 
 * Usage: node extract_resume.js <input.pdf> <output.md>
 * Requires: npm install pdfjs-dist
 */

import fs from 'fs';
import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';

const [inputPdf, outputMd] = process.argv.slice(2);

if (!inputPdf || !outputMd) {
  console.error('Usage: node extract_resume.js <input.pdf> <output.md>');
  process.exit(1);
}

const data = new Uint8Array(fs.readFileSync(inputPdf));
const doc = await getDocument({ data }).promise;
let text = '';
for (let i = 1; i <= doc.numPages; i++) {
  const page = await doc.getPage(i);
  const content = await page.getTextContent();
  const pageText = content.items.map(item => item.str).join(' ');
  text += pageText + '\n\n';
}
fs.writeFileSync(outputMd, text, 'utf-8');
console.log(`Extracted ${text.length} chars from ${doc.numPages} pages → ${outputMd}`);
