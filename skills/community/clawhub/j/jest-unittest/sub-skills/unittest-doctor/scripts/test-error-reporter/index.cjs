#!/usr/bin/env node
/**
 * 检测组件单测运行错误和警告
 *
 * 用法：
 *   node scripts/test-error-reporter/index.cjs
 *   node scripts/test-error-reporter/index.cjs --name=mask
 *
 * 选项：
 *   --name=<name>     仅检查指定组件的测试
 *
 * 输出 JSON 格式（含 hasErrors, hasWarnings, summary, failures, warnings）
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

// ==================== 构建测试命令 ====================
const testCommand = specificName ? config.testOneCommand.replace(/\{name\}/g, specificName) : config.testAllCommand;

// ==================== 1. 运行测试 ====================
let testOutput = '';
let testExitCode = 0;

try {
  testOutput = execSync(`${testCommand} 2>&1`, {
    cwd: projectRoot,
    encoding: 'utf-8',
    shell: true,
    maxBuffer: 50 * 1024 * 1024,
  });
} catch (err) {
  testExitCode = err.status || 1;
  testOutput = (err.stdout || '').toString() + (err.stderr || '').toString();
}

// 去除 ANSI 转义码，确保正则能正确匹配
const fullOutput = testOutput.replace(/\x1b\[[0-9;]*m/g, '');

// ==================== 2. 解析测试统计 ====================

const summary = {
  testSuites: { passed: 0, failed: 0, total: 0 },
  tests: { passed: 0, failed: 0, total: 0 },
};

const suitesMatch = fullOutput.match(/Test Suites:\s+(.*?)\n/);
if (suitesMatch) {
  const line = suitesMatch[1];
  const failedM = line.match(/(\d+)\s+failed/);
  const passedM = line.match(/(\d+)\s+passed/);
  const totalM = line.match(/(\d+)\s+total/);
  if (failedM) summary.testSuites.failed = parseInt(failedM[1], 10);
  if (passedM) summary.testSuites.passed = parseInt(passedM[1], 10);
  if (totalM) summary.testSuites.total = parseInt(totalM[1], 10);
}

const testsMatch = fullOutput.match(/Tests:\s+(.*?)\n/);
if (testsMatch) {
  const line = testsMatch[1];
  const failedM = line.match(/(\d+)\s+failed/);
  const passedM = line.match(/(\d+)\s+passed/);
  const totalM = line.match(/(\d+)\s+total/);
  if (failedM) summary.tests.failed = parseInt(failedM[1], 10);
  if (passedM) summary.tests.passed = parseInt(passedM[1], 10);
  if (totalM) summary.tests.total = parseInt(totalM[1], 10);
}

// ==================== 3. 解析失败的测试（Jest ● 标记） ====================

const failures = [];

const failFileBlocks = fullOutput.split(/\n\s*FAIL\s+/);
for (let i = 1; i < failFileBlocks.length; i++) {
  const block = failFileBlocks[i];

  const firstLine = block.split('\n')[0].trim();
  const testFile = firstLine.replace(/\s*\(.*\)$/, '').trim();

  const compMatch = testFile.match(new RegExp(config.componentRegex));
  const component = compMatch ? compMatch[1] : (specificName || 'unknown');

  const caseParts = block.split(/\n\s*●\s+/);
  for (let j = 1; j < caseParts.length; j++) {
    const casePart = caseParts[j];
    const lines = casePart.split('\n');
    const testName = lines[0].trim();

    const errorContent = casePart.substring(testName.length).trim();
    const error = errorContent.substring(0, 2000);

    const suggestion = getSuggestion(errorContent);

    failures.push({ testFile, component, testName, error, suggestion });
  }
}

// ==================== 4. 解析 console.error / console.warn ====================

const warnings = [];

const consoleBlocks = fullOutput.split(/\n\s+(console\.error|console\.warn)\n/);

for (let i = 1; i < consoleBlocks.length; i += 2) {
  const type = consoleBlocks[i].trim();
  const content = consoleBlocks[i + 1] || '';

  const msgLines = [];
  const detailLines = [];
  let inMsg = true;
  for (const line of content.split('\n')) {
    if (/^\s*(console\.(error|warn)|PASS|FAIL|Tests:|Test Suites:|----)/.test(line)) break;
    if (/^\s+at\s+/.test(line)) {
      inMsg = false;
      detailLines.push(line);
    } else if (/^\s*>?\s*\d+\s*\|/.test(line)) {
      inMsg = false;
      detailLines.push(line);
    } else if (/^\s+\^/.test(line)) {
      inMsg = false;
      detailLines.push(line);
    } else if (line.trim()) {
      if (inMsg) {
        msgLines.push(line.trim());
      } else {
        detailLines.push(line);
      }
    }
  }

  const message = msgLines.join(' ').substring(0, 300);
  if (!message) continue;

  const compMatch = content.match(new RegExp(config.componentRegex));
  const component = compMatch ? compMatch[1] : (specificName || 'unknown');

  const locMatch = content.match(new RegExp(`at\\s+\\S+\\s+\\(([^)]+${config.componentDirBaseName}\\/[^)]+)\\)`));
  const sourceLocation = locMatch ? locMatch[1] : '';

  warnings.push({
    type,
    component,
    message,
    detail: detailLines.join('\n').trim().substring(0, 1500),
    sourceLocation,
  });
}

// 去重 warnings
const warningMap = new Map();
for (const w of warnings) {
  const key = `${w.component}|${w.message}`;
  if (warningMap.has(key)) {
    warningMap.get(key).count++;
  } else {
    warningMap.set(key, { ...w, count: 1 });
  }
}
const dedupedWarnings = Array.from(warningMap.values());

// ==================== 5. 生成输出 ====================

const hasErrors = testExitCode !== 0 || failures.length > 0;
const hasWarnings = dedupedWarnings.length > 0;

let message = '';
if (hasErrors && hasWarnings) {
  message = `单测失败: ${summary.tests.failed} 个测试失败, ${summary.tests.passed} 个通过; 另有 ${dedupedWarnings.length} 个 console 警告/错误`;
} else if (hasErrors) {
  message = `单测失败: ${summary.tests.failed} 个测试失败, ${summary.tests.passed} 个通过`;
} else if (hasWarnings) {
  message = `单测全部通过 (${summary.tests.passed} 个), 但有 ${dedupedWarnings.length} 个 console 警告/错误`;
} else {
  message = `单测全部通过 (${summary.tests.passed} 个), 无错误无警告`;
}

const result = {
  hasErrors,
  hasWarnings,
  testCommand,
  message,
  summary,
  failures,
  warnings: dedupedWarnings,
};

console.log(JSON.stringify(result, null, 2));
process.exit(testExitCode === 0 ? 0 : 1);

// ==================== 工具函数 ====================

function getSuggestion(errorText) {
  const t = errorText.toLowerCase();

  if (t.includes('snapshot') && (t.includes('mismatch') || t.includes('not match') || t.includes('obsolete'))) {
    return `快照不匹配，可运行 updateSnapshotCommand（见 config.json）更新快照，或检查组件输出是否有意外变化`;
  }
  if (t.includes('cannot find module') || t.includes('module not found')) {
    return '模块找不到，检查导入路径是否正确、文件是否存在、依赖是否已安装';
  }
  if (t.includes('is not defined') || t.includes('referenceerror')) {
    return '引用错误，检查变量/函数是否已正确导入或定义';
  }
  if (t.includes('timeout') || t.includes('exceeded') || t.includes('async callback was not invoked')) {
    return '异步超时，检查 async/await 和 Promise 是否正确处理，或增加 jest.setTimeout';
  }
  if (t.includes('not wrapped in act')) {
    return 'React state 更新未包装在 act() 中，使用 waitFor 或将操作包裹在 act(async () => { ... }) 中';
  }
  if (t.includes('typeerror') || t.includes('cannot read propert')) {
    return '类型错误或属性访问错误，检查对象是否为 null/undefined，考虑使用可选链 ?.';
  }
  if (t.includes('expected') || t.includes('toequal') || t.includes('tobe') || t.includes('received')) {
    return '断言失败，检查预期值与实际值的差异，确认组件逻辑或测试条件是否正确';
  }
  if (t.includes('not implemented')) {
    return '浏览器 API 未实现（jsdom 限制），需要在测试中 mock 该 API（如 window.scrollTo、window.matchMedia 等）';
  }
  return '请结合错误信息和堆栈检查测试用例和组件代码';
}
