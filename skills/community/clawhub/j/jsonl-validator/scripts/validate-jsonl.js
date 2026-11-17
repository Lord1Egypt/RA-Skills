'use strict';

const fs = require('fs');
const path = require('path');

function findWorkspace() {
  if (process.env.WORKSPACE_ROOT) return process.env.WORKSPACE_ROOT;
  const cwd = process.cwd();
  if (fs.existsSync(path.join(cwd, 'memory', 'evolution'))) return cwd;
  return cwd;
}

function validateJsonl(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  const results = {
    file: filePath,
    totalLines: lines.length,
    nonEmptyLines: 0,
    validJson: 0,
    invalidJson: 0,
    invalidExamples: [],
    timeRange: {
      earliest: null,
      latest: null
    },
    keyDistribution: {},
    errors: [],
    tooManyInvalidLines: false
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    results.nonEmptyLines++;
    try {
      const obj = JSON.parse(line);
      results.validJson++;
      const keys = Object.keys(obj);
      for (const k of keys) {
        results.keyDistribution[k] = (results.keyDistribution[k] || 0) + 1;
      }
      if (obj.ts) {
        const ts = new Date(obj.ts);
        if (!Number.isNaN(ts.getTime())) {
          if (!results.timeRange.earliest || ts < new Date(results.timeRange.earliest)) {
            results.timeRange.earliest = obj.ts;
          }
          if (!results.timeRange.latest || ts > new Date(results.timeRange.latest)) {
            results.timeRange.latest = obj.ts;
          }
        }
      }
    } catch (e) {
      results.invalidJson++;
      results.invalidExamples.push({
        line: i + 1,
        preview: line.slice(0, 120),
        error: e.message
      });
      if (results.invalidExamples.length >= 5) {
        results.errors.push('More invalid JSON lines exist beyond the first 5 examples.');
        results.tooManyInvalidLines = true;
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
  lines.push('');
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
  if (result.invalidJson > 0) {
    process.exit(2);
  }
}

function runCli(target) {
  if (target === '--help' || target === '-h') {
    console.log('Usage: validate-jsonl <file.jsonl>');
    console.log('Exit codes: 0=valid, 1=usage/missing, 2=invalid lines');
    process.exit(0);
  }
  const resolved = path.resolve(target);
  if (!fs.existsSync(resolved)) {
    console.error('File not found: ' + resolved);
    process.exit(1);
  }
  const result = validateJsonl(resolved);
  console.log(formatReport(result));
  if (result.invalidJson > 0) {
    process.exit(2);
  }
}

const target = process.argv[2];
if (require.main === module && target) {
  if (target === '--version' || target === '-v') {
    console.log('jsonl-validator v1.1.0');
    process.exit(0);
  }
  runCli(target);
}

module.exports = { validateJsonl, formatReport, run: runCli };
