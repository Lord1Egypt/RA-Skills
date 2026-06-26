#!/usr/bin/env node

/**
 * OCR - Image Text Recognition using Tesseract.js
 * Usage: node ocr.js <image> [--lang chi_sim+eng] [--json]
 */

const Tesseract = require('tesseract.js');
const path = require('path');
const fs = require('fs');

// Parse arguments
const args = process.argv.slice(2);
const imagePath = args.find(a => !a.startsWith('--'));
const langArg = args.find(a => a === '--lang');
const langIndex = langArg ? args.indexOf(langArg) : -1;
const languages = langIndex >= 0 && args[langIndex + 1] ? args[langIndex + 1] : 'chi_sim+eng';
const outputJson = args.includes('--json');

if (!imagePath) {
  console.error('Usage: node ocr.js <image> [--lang chi_sim+eng] [--json]');
  console.error('');
  console.error('Options:');
  console.error('  --lang <langs>  Language codes (default: chi_sim+eng)');
  console.error('                  chi_sim = Simplified Chinese');
  console.error('                  chi_tra = Traditional Chinese');
  console.error('                  eng = English');
  console.error('  --json          Output as JSON');
  process.exit(1);
}

// Resolve image path
const resolvedPath = path.isAbsolute(imagePath) 
  ? imagePath 
  : path.join(process.cwd(), imagePath);

if (!fs.existsSync(resolvedPath)) {
  console.error(`Error: Image not found: ${resolvedPath}`);
  process.exit(1);
}

async function recognize() {
  try {
    console.error(`📝 Recognizing text from: ${path.basename(imagePath)}`);
    console.error(`🌐 Languages: ${languages}`);
    console.error('');

    // Set cachePath to tessdata directory
    const scriptDir = __dirname;
    const tessdataDir = path.join(scriptDir, 'tessdata');

    const result = await Tesseract.recognize(
      resolvedPath,
      languages,
      {
        cachePath: tessdataDir,
        logger: m => {
          if (m.status === 'recognizing text') {
            process.stderr.write(`\r⏳ Progress: ${Math.round(m.progress * 100)}%`);
          }
        }
      }
    );

    console.error('\n');
    
    if (outputJson) {
      console.log(JSON.stringify({
        text: result.data.text,
        confidence: result.data.confidence,
        words: result.data.words.map(w => ({
          text: w.text,
          confidence: w.confidence,
          bbox: w.bbox
        }))
      }, null, 2));
    } else {
      console.log(result.data.text);
    }

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

recognize();
