#!/usr/bin/env node
/**
 * 运行组件测试并分析覆盖率，输出未达 100% 的组件列表
 *
 * 用法：
 *   node scripts/analyze-coverage/index.cjs
 *   node scripts/analyze-coverage/index.cjs --name=button
 *
 * 选项：
 *   --name=<name>     仅检查指定组件的覆盖率
 *
 * 输出 JSON 格式：
 * {
 *   "totalComponents": number,
 *   "fullCoverageCount": number,
 *   "fullCoverageComponents": ["组件名", ...],
 *   "notFullCoverageCount": number,
 *   "notFullCoverageComponents": [
 *     {
 *       "component": "组件名",
 *       "statements": "94.74%",
 *       "branches":   "87.5%",
 *       "functions":  "100%",
 *       "lines":      "100%"
 *     }
 *   ]
 * }
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const config = require('../../../../scripts/guard-config.cjs');
const projectRoot = config.projectRoot;
const args = process.argv.slice(2);

// ==================== 解析参数 ====================
let specificName = null;
for (const arg of args) {
  if (arg.startsWith('--name=')) {
    specificName = arg.replace('--name=', '');
  }
}

// ==================== 1. 运行组件测试 ====================
// 指定组件 → coverageDir/{name}，全量 → coverageDir/all
const subDir = specificName || 'all';
const reportsDir = path.join(projectRoot, config.coverageDir, subDir);
const coveragePath = path.join(reportsDir, 'coverage-final.json');

// 清理旧的覆盖率报告
if (fs.existsSync(reportsDir)) {
  fs.rmSync(reportsDir, { recursive: true, force: true });
}

// 指定组件用 testOneCommand，全量用 testAllCommand
const testCommand = specificName
  ? config.testOneCommand.replace(/\{name\}/g, specificName)
  : config.testAllCommand;

try {
  execSync(testCommand, {
    cwd: projectRoot,
    encoding: 'utf-8',
    stdio: ['inherit', 'pipe', 'pipe'],
    maxBuffer: 10 * 1024 * 1024,
  });
} catch (err) {
  console.log(JSON.stringify({
    error: `测试运行失败: ${(err.stderr || '').toString().trimEnd() || `exit code ${err.status || 1}`}`,
    type: 'test_error',
  }, null, 2));
  process.exit(1);
}

// ==================== 2. 读取覆盖率报告 ====================
if (!fs.existsSync(coveragePath)) {
  console.log(JSON.stringify({
    error: `覆盖率报告文件不存在: ${coveragePath}`,
    type: 'test_error',
  }, null, 2));
  process.exit(1);
}

const coverageData = JSON.parse(fs.readFileSync(coveragePath, 'utf-8'));

// ==================== 3. 按组件名分组聚合覆盖率数据 ====================
const componentStats = {};

for (const [filePath, fileData] of Object.entries(coverageData)) {
  const match = filePath.match(new RegExp(config.componentRegex));
  if (!match) continue;

  const componentName = match[1];

  // 如果指定了组件名，只处理该组件
  if (specificName && componentName !== specificName) continue;

  if (!componentStats[componentName]) {
    componentStats[componentName] = {
      statements: { total: 0, covered: 0 },
      branches: { total: 0, covered: 0 },
      functions: { total: 0, covered: 0 },
      lines: { total: 0, covered: 0 },
    };
  }

  const stats = componentStats[componentName];

  // Statements
  const s = fileData.s || {};
  for (const count of Object.values(s)) {
    stats.statements.total++;
    if (count > 0) stats.statements.covered++;
  }

  // Branches
  const b = fileData.b || {};
  for (const counts of Object.values(b)) {
    for (const count of counts) {
      stats.branches.total++;
      if (count > 0) stats.branches.covered++;
    }
  }

  // Functions
  const f = fileData.f || {};
  for (const count of Object.values(f)) {
    stats.functions.total++;
    if (count > 0) stats.functions.covered++;
  }

  // Lines - 从 statementMap 计算行覆盖率
  const stmtMap = fileData.statementMap || {};
  const coveredLines = new Set();
  const allLines = new Set();

  for (const [id, mapping] of Object.entries(stmtMap)) {
    if (mapping && mapping.start && mapping.end) {
      for (let line = mapping.start.line; line <= mapping.end.line; line++) {
        allLines.add(line);
        if (s[id] > 0) {
          coveredLines.add(line);
        }
      }
    }
  }

  stats.lines.total += allLines.size;
  stats.lines.covered += coveredLines.size;
}

// ==================== 4. 计算百分比并输出 ====================
function pct(covered, total) {
  if (total === 0) return 100;
  return Math.round((covered / total) * 10000) / 100;
}

const notFullCoverage = [];
const fullCoverageComponents = [];

const sortedComponents = Object.keys(componentStats).sort();

for (const name of sortedComponents) {
  const stats = componentStats[name];

  const stmtPct = pct(stats.statements.covered, stats.statements.total);
  const branchPct = pct(stats.branches.covered, stats.branches.total);
  const fnPct = pct(stats.functions.covered, stats.functions.total);
  const linePct = pct(stats.lines.covered, stats.lines.total);

  if (stmtPct === 100 && branchPct === 100 && fnPct === 100 && linePct === 100) {
    fullCoverageComponents.push(name);
  } else {
    notFullCoverage.push({
      component: name,
      statements: `${stmtPct}%`,
      branches: `${branchPct}%`,
      functions: `${fnPct}%`,
      lines: `${linePct}%`,
    });
  }
}

const result = {
  totalComponents: sortedComponents.length,
  fullCoverageCount: fullCoverageComponents.length,
  fullCoverageComponents,
  notFullCoverageCount: notFullCoverage.length,
  notFullCoverageComponents: notFullCoverage,
};

if (specificName) {
  result.queriedComponent = specificName;
}

console.log(JSON.stringify(result, null, 2));
