#!/usr/bin/env node
/**
 * 检测组件单测覆盖率是否达到 100%
 *
 * 用法：
 *   node scripts/check-coverage-100/index.cjs <组件名>
 *
 * 返回 JSON 对象（通过 stdout 输出），结构如下：
 *
 * status 有三种状态：
 *   - "success"    : 单测通过且覆盖率 100%，只需看 success 字段
 *   - "test_error" : 单测运行报错，查看 error 字段获取报错信息
 *   - "not_covered": 单测通过但覆盖率未达 100%，查看 uncoveredDetails 字段获取未覆盖位置
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const componentName = process.argv[2];

if (!componentName) {
  console.log(JSON.stringify({
    success: false,
    status: 'test_error',
    error: '请指定组件名，例如: node scripts/check-coverage-100/index.cjs button',
  }, null, 2));
  process.exit(1);
}

const config = require('../../../../scripts/guard-config.cjs');
const projectRoot = config.projectRoot;

// ==================== 1. 运行单测 ====================
// 单组件产物输出到 coverageDir/{组件名}
const reportsDir = path.join(projectRoot, config.coverageDir, componentName);

// 清理旧的覆盖率报告
if (fs.existsSync(reportsDir)) {
  fs.rmSync(reportsDir, { recursive: true, force: true });
}

let testExitCode = 0;
let testStderr = '';

try {
  execSync(config.testOneCommand.replace(/\{name\}/g, componentName), {
    cwd: projectRoot,
    encoding: 'utf-8',
    stdio: ['inherit', 'pipe', 'pipe'],
    maxBuffer: 10 * 1024 * 1024,
  });
} catch (err) {
  testExitCode = err.status || 1;
  testStderr = (err.stderr || '').toString();
}

// ==================== 2. 单测报错，直接返回 ====================
if (testExitCode !== 0) {
  console.log(JSON.stringify({
    success: false,
    status: 'test_error',
    error: testStderr.trimEnd() || `单测运行失败 (exit code: ${testExitCode})`,
  }, null, 2));
  process.exit(1);
}

// ==================== 3. 读取覆盖率报告 ====================
const coveragePath = path.join(projectRoot, config.coverageDir, componentName, 'coverage-final.json');

if (!fs.existsSync(coveragePath)) {
  console.log(JSON.stringify({
    success: false,
    status: 'test_error',
    error: `覆盖率报告文件不存在: ${coveragePath}`,
  }, null, 2));
  process.exit(1);
}

const coverageData = JSON.parse(fs.readFileSync(coveragePath, 'utf-8'));

// ==================== 4. 过滤出当前组件的文件 ====================
const componentPattern = `${config.componentDirBaseName}/${componentName}/`;
const componentFiles = Object.keys(coverageData).filter(fp => fp.includes(componentPattern));

if (componentFiles.length === 0) {
  console.log(JSON.stringify({
    success: false,
    status: 'test_error',
    error: `未找到组件 "${componentName}" 的覆盖率数据，请确认组件名是否正确。`,
  }, null, 2));
  process.exit(1);
}

// ==================== 5. 收集未覆盖的详情 ====================

function rel(absPath) {
  return absPath.replace(`${projectRoot}/`, '');
}

function loc(pos) {
  if (!pos) return '?';
  const col = pos.column !== null ? `:${pos.column}` : '';
  return `${pos.line}${col}`;
}

function locRange(start, end) {
  if (!start) return '?';
  const s = loc(start);
  if (!end || (end.line === start.line && end.column === start.column)) return s;
  return `${s} - ${loc(end)}`;
}

function formatLineRanges(lines) {
  if (lines.length === 0) return '';
  const ranges = [];
  let start = lines[0];
  let end = lines[0];
  for (let i = 1; i < lines.length; i++) {
    if (lines[i] === end + 1) {
      end = lines[i];
    } else {
      ranges.push(start === end ? `${start}` : `${start}-${end}`);
      start = lines[i];
      end = lines[i];
    }
  }
  ranges.push(start === end ? `${start}` : `${start}-${end}`);
  return ranges.join(', ');
}

const uncoveredFiles = [];

for (const filePath of componentFiles) {
  const fileData = coverageData[filePath];
  const relativePath = rel(filePath);

  const uncoveredStatements = [];
  const uncoveredBranches = [];
  const uncoveredFunctions = [];
  const uncoveredLines = new Set();

  // --- Statements ---
  const stmtMap = fileData.statementMap || {};
  const s = fileData.s || {};
  for (const id of Object.keys(s)) {
    if (s[id] === 0 && stmtMap[id]) {
      const sm = stmtMap[id];
      uncoveredStatements.push({
        line: sm.start.line,
        location: locRange(sm.start, sm.end),
      });
      if (sm.start && sm.end) {
        for (let l = sm.start.line; l <= (sm.end.line || sm.start.line); l++) {
          uncoveredLines.add(l);
        }
      }
    }
  }

  // --- Branches ---
  const branchMap = fileData.branchMap || {};
  const b = fileData.b || {};
  for (const id of Object.keys(b)) {
    const counts = b[id];
    const bm = branchMap[id];
    if (!bm) continue;
    for (let i = 0; i < counts.length; i++) {
      if (counts[i] === 0) {
        const branchLoc = bm.locations && bm.locations[i];
        uncoveredBranches.push({
          line: bm.loc ? bm.loc.start.line : (branchLoc ? branchLoc.start.line : '?'),
          type: bm.type || 'unknown',
          branchIndex: i,
          location: branchLoc ? locRange(branchLoc.start, branchLoc.end) : locRange(bm.loc?.start, bm.loc?.end),
        });
      }
    }
  }

  // --- Functions ---
  const fnMap = fileData.fnMap || {};
  const f = fileData.f || {};
  for (const id of Object.keys(f)) {
    if (f[id] === 0 && fnMap[id]) {
      const fm = fnMap[id];
      uncoveredFunctions.push({
        name: fm.name || '(anonymous)',
        line: fm.decl ? fm.decl.start.line : fm.loc?.start?.line || '?',
        location: fm.loc ? locRange(fm.loc.start, fm.loc.end) : '?',
      });
    }
  }

  if (uncoveredStatements.length || uncoveredBranches.length || uncoveredFunctions.length) {
    uncoveredFiles.push({
      file: relativePath,
      uncoveredLines: formatLineRanges(Array.from(uncoveredLines).sort((a, b) => a - b)),
      uncoveredStatements,
      uncoveredBranches,
      uncoveredFunctions,
    });
  }
}

// ==================== 6. 输出结果 ====================

if (uncoveredFiles.length === 0) {
  console.log(JSON.stringify({
    success: true,
    status: 'success',
  }, null, 2));
  process.exit(0);
} else {
  console.log(JSON.stringify({
    success: false,
    status: 'not_covered',
    uncoveredDetails: uncoveredFiles,
  }, null, 2));
  process.exit(1);
}
