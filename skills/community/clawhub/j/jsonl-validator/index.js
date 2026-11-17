'use strict';
const fs = require('fs');
const path = require('path');

function validateJsonl(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  const results = {
    file: filePath,
    totalLines: lines.length,
    nonEmptyLines: 0,
    validJson: 0,
    invalidJson: 0,
    invalidExamples: [],
    timeRange: { earliest: null, latest: null },
    keyDistribution: {},
    errors: []
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    results.nonEmptyLines++;
    try {
      const obj = JSON.parse(line);
      results.validJson++;
      for (const k of Object.keys(obj)) {
        results.keyDistribution[k] = (results.keyDistribution[k] || 0) + 1;
      }
      if (obj.ts) {
        const ts = new Date(obj.ts);
        if (!Number.isNaN(ts.getTime())) {
          if (!results.timeRange.earliest || ts < new Date(results.timeRange.earliest)) results.timeRange.earliest = obj.ts;
          if (!results.timeRange.latest || ts > new Date(results.timeRange.latest)) results.timeRange.latest = obj.ts;
        }
      }
    } catch (e) {
      results.invalidJson++;
      results.invalidExamples.push({ line: i + 1, preview: line.slice(0, 120), error: e.message });
      if (results.invalidExamples.length >= 5) {
        results.errors.push('More invalid JSON lines exist beyond the first 5 examples.');
        break;
      }
    }
  }

  return results;
}

function formatReport(result) {
  const lines = [];
  lines.push('=== JSONL Validation Report ===');
  lines.push('File: ' + result.file);
  lines.push('Total Lines: ' + result.totalLines);
  lines.push('Non-Empty Lines: ' + result.nonEmptyLines);
  lines.push('Valid JSON: ' + result.validJson);
  lines.push('Invalid JSON: ' + result.invalidJson);
  if (result.timeRange.earliest && result.timeRange.latest) {
    lines.push('Time Range: ' + result.timeRange.earliest + ' -> ' + result.timeRange.latest);
  } else {
    lines.push('Time Range: n/a');
  }
  lines.push('');
  lines.push('[Top Keys]');
  const sortedKeys = Object.entries(result.keyDistribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  for (const [key, count] of sortedKeys) {
    lines.push('  ' + key + ': ' + count);
  }
  if (result.invalidExamples.length) {
    lines.push('');
    lines.push('[Invalid Lines]');
    for (const ex of result.invalidExamples) {
      lines.push('  Line ' + ex.line + ': ' + ex.preview + ' => ' + ex.error);
    }
  }
  if (result.errors.length) {
    lines.push('');
    lines.push('[Errors]');
    for (const err of result.errors) {
      lines.push('  ' + err);
    }
  }
  lines.push('');
  lines.push('=== END REPORT ===');
  return lines.join('\n');
}

function run(targetPath) {
  const resolved = path.resolve(targetPath);
  if (!fs.existsSync(resolved)) {
    console.error('File not found: ' + resolved);
    process.exit(1);
  }
  const result = validateJsonl(resolved);
  console.log(formatReport(result));
  if (result.invalidJson > 0) process.exit(2);
}

function runAll(files) {
  if (!files.length) {
    console.error('No files specified');
    process.exit(1);
  }
  let failed = 0;
  for (const f of files) {
    const resolved = path.resolve(f);
    if (!fs.existsSync(resolved)) {
      console.error('File not found: ' + resolved);
      failed++;
      continue;
    }
    const result = validateJsonl(resolved);
    console.log(formatReport(result));
    if (result.invalidJson > 0) failed++;
  }
  console.log('Validated ' + files.length + ' file(s), ' + failed + ' failed');
  if (failed > 0) process.exit(2);
}

function showHelp() {
  console.log('Usage: node index.js <file.jsonl>');
  console.log('   or: node index.js --all <file1> [<file2>...]');
  console.log('   or: node index.js --help');
  console.log('   or: node index.js --version');
  console.log('Exit codes: 0=valid, 1=usage/missing, 2=invalid lines');
}

function showVersion() {
  console.log('jsonl-validator v1.1.0');
}

const args = process.argv.slice(2);
if (args[0] === '--help' || args[0] === '-h') {
  showHelp();
  process.exit(0);
}
if (args[0] === '--version' || args[0] === '-v') {
  showVersion();
  process.exit(0);
}
if (args[0] === '--all' || args[0] === '-a') {
  runAll(args.slice(1));
} else {
  runAll(args);
}

module.exports = { validateJsonl, formatReport, run, runAll, showHelp, showVersion };
