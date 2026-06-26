#!/usr/bin/env node

import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

async function convertHtmlToPdf(inputPath, outputPath, options = {}) {
  const defaultOptions = {
    format: 'A4',
    margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
    ...options
  };

  try {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    // Handle both file paths and URLs
    const isUrl = inputPath.startsWith('http://') || inputPath.startsWith('https://');
    if (isUrl) {
      await page.goto(inputPath, { waitUntil: 'networkidle2' });
    } else {
      const filePath = path.resolve(inputPath);
      const fileUrl = 'file://' + filePath;
      await page.goto(fileUrl, { waitUntil: 'networkidle2' });
    }

    await page.pdf({
      path: outputPath,
      ...defaultOptions
    });

    await browser.close();
    console.log(`✓ PDF created: ${outputPath}`);
    return { success: true, path: outputPath };
  } catch (error) {
    console.error(`✗ Error: ${error.message}`);
    process.exit(1);
  }
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: html-to-pdf.js <input-file|url> <output-pdf> [format] [options-json]');
    console.error('Examples:');
    console.error('  html-to-pdf.js input.html output.pdf');
    console.error('  html-to-pdf.js input.html output.pdf A4');
    console.error('  html-to-pdf.js https://example.com output.pdf A4 \'{"margin":"5mm"}\'');
    process.exit(1);
  }

  const [inputPath, outputPath, format = 'A4', optionsJson = '{}'] = args;
  
  try {
    const options = JSON.parse(optionsJson);
    if (format) options.format = format;
    convertHtmlToPdf(inputPath, outputPath, options);
  } catch (error) {
    console.error(`Invalid JSON options: ${error.message}`);
    process.exit(1);
  }
}

export default convertHtmlToPdf;
