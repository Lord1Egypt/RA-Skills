#!/usr/bin/env node
/**
 * build-frameworks.js — Generate publish/frameworks/ from frameworks/ (compressed)
 *
 * Compression rules:
 *   1. Keep title + core conclusion
 *   2. Remove detailed explanations and examples
 *   3. Keep 1-2 sentence "一句话说明" per section
 *   4. Output to publish/frameworks/<same-name>.md
 *
 * Usage: node build-frameworks.js
 */

const fs = require('fs');
const path = require('path');

const FRAMEWORKS_DIR = path.join(__dirname, '..', 'frameworks');
const PUBLISH_FRAMEWORKS_DIR = path.join(__dirname, '..', 'publish', 'frameworks');

function compressFramework(filePath) {
  let content = fs.readFileSync(filePath, 'utf-8');
  const fileName = path.basename(filePath);
  
  // Remove markdown HRs and compress paragraphs
  // Heuristic: keep first 2 paragraphs after each ## heading, remove rest
  const lines = content.split('\n');
  let output = [];
  let inHeading = false;
  let paraCount = 0;
  let skipUntilNextHeading = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (line.startsWith('---')) {
      continue; // Remove HRs
    }

    if (line.startsWith('##')) {
      output.push(line);
      inHeading = true;
      paraCount = 0;
      skipUntilNextHeading = false;
      continue;
    }

    if (line.startsWith('###')) {
      output.push(line);
      paraCount = 0;
      continue;
    }

    // Heuristic compression: after each heading, keep 1-2 paragraphs
    if (line.trim() === '' && inHeading) {
      paraCount++;
      if (paraCount > 2) {
        skipUntilNextHeading = true;
      }
      if (!skipUntilNextHeading) {
        output.push(line);
      }
      continue;
    }

    if (!skipUntilNextHeading) {
      output.push(line);
    }
  }

  return output.join('\n').replace(/\n{3,}/g, '\n\n'); // Clean up excessive blank lines
}

function buildAll() {
  if (!fs.existsSync(PUBLISH_FRAMEWORKS_DIR)) {
    fs.mkdirSync(PUBLISH_FRAMEWORKS_DIR, { recursive: true });
  }

  const files = fs.readdirSync(FRAMEWORKS_DIR).filter(f => f.endsWith('.md'));
  let totalOriginal = 0;
  let totalCompressed = 0;

  console.log('📦 Compressing framework cards...\n');

  for (const file of files) {
    const srcPath = path.join(FRAMEWORKS_DIR, file);
    const destPath = path.join(PUBLISH_FRAMEWORKS_DIR, file);
    const originalContent = fs.readFileSync(srcPath, 'utf-8');
    const compressed = compressFramework(srcPath);

    fs.writeFileSync(destPath, compressed);
    totalOriginal += originalContent.length;
    totalCompressed += compressed.length;

    const ratio = ((compressed.length / originalContent.length) * 100).toFixed(1);
    console.log(`  ✅ ${file}: ${originalContent.length} → ${compressed.length} bytes (${ratio}%)`);
  }

  console.log(`\n📊 Summary:`);
  console.log(`  Original total:   ${totalOriginal} bytes`);
  console.log(`  Compressed total: ${totalCompressed} bytes`);
  console.log(`  Overall ratio:     ${((totalCompressed / totalOriginal) * 100).toFixed(1)}%`);
  console.log(`\n✅ publish/frameworks/ updated\n`);
}

try {
  buildAll();
} catch (err) {
  console.error('❌ build-frameworks.js failed:', err.message);
  process.exit(1);
}
