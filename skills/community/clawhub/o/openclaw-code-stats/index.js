#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/duan/.openclaw/workspace';

const IGNORE_DIRS = ['node_modules', '.git', 'dist', 'build', '__pycache__', '.venv'];
const EXT_MAP = {
  '.js': 'JavaScript',
  '.ts': 'TypeScript',
  '.py': 'Python',
  '.json': 'JSON',
  '.md': 'Markdown',
  '.yaml': 'YAML',
  '.yml': 'YAML',
  '.sh': 'Shell',
  '.bash': 'Shell',
  '.html': 'HTML',
  '.css': 'CSS'
};

function countLines(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return content.split('\n').length;
  } catch {
    return 0;
  }
}

function walkDir(dir, stats) {
  if (!fs.existsSync(dir)) return;
  
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    if (item.startsWith('.')) continue;
    if (IGNORE_DIRS.includes(item)) continue;
    
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      walkDir(fullPath, stats);
    } else {
      const ext = path.extname(item).toLowerCase();
      const lang = EXT_MAP[ext] || 'Other';
      
      stats.totalFiles++;
      const lines = countLines(fullPath);
      stats.totalLines += lines;
      
      if (!stats.byLang[lang]) {
        stats.byLang[lang] = { files: 0, lines: 0 };
      }
      stats.byLang[lang].files++;
      stats.byLang[lang].lines += lines;
    }
  }
}

function main() {
  const stats = {
    totalFiles: 0,
    totalLines: 0,
    byLang: {}
  };
  
  walkDir(WORKSPACE, stats);
  
  console.log('📊 Code Stats for', WORKSPACE);
  console.log('='.repeat(40));
  console.log(`Total Files: ${stats.totalFiles}`);
  console.log(`Total Lines: ${stats.totalLines.toLocaleString()}`);
  console.log('');
  console.log('By Language:');
  
  const sorted = Object.entries(stats.byLang)
    .sort((a, b) => b[1].lines - a[1].lines);
  
  for (const [lang, data] of sorted) {
    const pct = ((data.lines / stats.totalLines) * 100).toFixed(1);
    console.log(`  ${lang}: ${data.files} files, ${data.lines.toLocaleString()} lines (${pct}%)`);
  }
}

main();
