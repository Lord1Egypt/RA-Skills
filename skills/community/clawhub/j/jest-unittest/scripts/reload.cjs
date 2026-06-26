#!/usr/bin/env node
/**
 * 解析 jest 配置文件，校验关键字段，生成 config.json 供各脚本直接使用。
 *
 * 用法：
 *   node scripts/reload.cjs
 *
 * 输入：.temp/projects/<hash>/source.json
 * 输出：.temp/projects/<hash>/config.json（全字符串，脚本直接读取即可）
 *
 * 支持的 jest 配置格式：
 *   - jest.config.js / .ts / .cjs / .mjs / .json
 *   - collectCoverageFrom: glob 数组，有无 <rootDir>/ 前缀均可
 *   - testMatch / testRegex: 二选一，均可推导 testDir
 *   - roots: 用于推导源码根目录（当 collectCoverageFrom 未配置时）
 */

const fs = require('fs');
const path = require('path');

const project = require('./resolve-project.cjs');
const { skillRoot, projectRoot, projectDir, sourcePath, configPath } = project;

// 产物统一输出到 .temp/coverage
const coverageDir = path.relative(projectRoot, path.join(skillRoot, '.temp', 'coverage'));

function fail(error, hint) {
  console.log(JSON.stringify({ success: false, type: 'config_error', error, hint }, null, 2));
  process.exit(1);
}

// ==================== 1. 读取 source.json ====================
if (!fs.existsSync(sourcePath)) {
  // 首次使用：自动创建目录和空 source.json
  fs.mkdirSync(projectDir, { recursive: true });
  fs.writeFileSync(sourcePath, JSON.stringify({ jestConfigPath: '' }, null, 2) + '\n');
  fail(`source.json 不存在，已自动创建`, `请编辑 ${path.relative(projectRoot, sourcePath)} 并配置 jestConfigPath`);
}

const source = JSON.parse(fs.readFileSync(sourcePath, 'utf-8'));
if (!source.jestConfigPath) {
  fail('source.json 中缺少 jestConfigPath 字段', `请在 ${path.relative(projectRoot, sourcePath)} 中配置 jestConfigPath（jest 配置文件的相对路径）`);
}

// ==================== 2. 读取 jest 配置文件 ====================
const jestConfigFullPath = path.join(projectRoot, source.jestConfigPath);
if (!fs.existsSync(jestConfigFullPath)) {
  fail(`jest 配置文件不存在: ${source.jestConfigPath}`, `请检查 ${path.relative(projectRoot, sourcePath)} 中的 jestConfigPath 是否正确`);
}

const jestContent = fs.readFileSync(jestConfigFullPath, 'utf-8');

// ==================== 3. 解析配置 ====================

/**
 * 从 jest 配置文本中提取数组字段的所有字符串项
 * 支持单引号和双引号，跨行
 */
function extractArrayField(content, fieldName) {
  const regex = new RegExp(fieldName + '\\s*:\\s*\\[([\\s\\S]*?)\\]');
  const match = content.match(regex);
  if (!match) return null;
  const items = match[1].match(/['"]([^'"]+)['"]/g);
  return items ? items.map(s => s.slice(1, -1)) : [];
}

/**
 * 从 jest 配置文本中提取字符串字段的值
 */
function extractStringField(content, fieldName) {
  const regex = new RegExp(fieldName + "\\s*:\\s*['\"]([^'\"]+)['\"]");
  const match = content.match(regex);
  return match ? match[1] : null;
}

/**
 * 去除路径中的 <rootDir>/ 前缀
 */
function stripRootDir(p) {
  return p.replace(/^<rootDir>\//, '');
}

/**
 * 从 glob 中分离目录部分和通配部分
 * 'src/views/_components/**\/*.tsx' → { dir: 'src/views/_components', glob: '**\/*.tsx' }
 * 'src/**\/*.{ts,tsx}' → { dir: 'src', glob: '**\/*.{ts,tsx}' }
 */
function splitGlob(pattern) {
  const cleaned = stripRootDir(pattern);
  const starIdx = cleaned.indexOf('*');
  if (starIdx <= 0) return { dir: cleaned, glob: '' };
  return {
    dir: cleaned.substring(0, starIdx).replace(/\/$/, ''),
    glob: cleaned.substring(starIdx),
  };
}

// --- collectCoverageFrom ---
const coverageFromItems = extractArrayField(jestContent, 'collectCoverageFrom');
let componentDir = '';
let coverageGlob = '';

if (coverageFromItems) {
  // 取第一个非排除项
  for (const item of coverageFromItems) {
    if (item.startsWith('!')) continue;
    const { dir, glob } = splitGlob(item);
    if (dir && glob) {
      componentDir = dir;
      coverageGlob = glob;
      break;
    }
  }
}

// 如果 collectCoverageFrom 没配置或解析失败，尝试从 roots 推导
if (!componentDir) {
  const roots = extractArrayField(jestContent, 'roots');
  if (roots && roots.length > 0) {
    componentDir = stripRootDir(roots[0]).replace(/\/$/, '');
  }
}

// 兜底：默认 src
if (!componentDir) {
  componentDir = 'src';
}
if (!coverageGlob) {
  coverageGlob = '**/*.{ts,tsx,js,jsx}';
}

// --- testDir: 从 testMatch 或 testRegex 推导 ---
let testDir = '';

// 尝试 testMatch
const testMatchItems = extractArrayField(jestContent, 'testMatch');
if (testMatchItems) {
  for (const item of testMatchItems) {
    const cleaned = stripRootDir(item);
    // 匹配 __xxx__ 形式的目录名，如 __tests__
    const dirMatch = cleaned.match(/__(\w+)__/);
    if (dirMatch) {
      testDir = `__${dirMatch[1]}__`;
      break;
    }
  }
}

// 尝试 testRegex
if (!testDir) {
  const testRegex = extractStringField(jestContent, 'testRegex');
  if (testRegex) {
    const dirMatch = testRegex.match(/__(\w+)__/);
    if (dirMatch) {
      testDir = `__${dirMatch[1]}__`;
    }
  }
}

// Jest 默认的 testMatch 包含 __tests__，所以兜底用 __tests__
if (!testDir) {
  testDir = '__tests__';
}

// ==================== 4. 检测 Jest 版本 ====================
let jestMajorVersion = 29; // 默认假设 29
try {
  const { execSync } = require('child_process');
  const versionOutput = execSync('npx jest --version', { cwd: projectRoot, encoding: 'utf-8', timeout: 30000 }).trim();
  const versionMatch = versionOutput.match(/(\d+)\./);
  if (versionMatch) {
    jestMajorVersion = parseInt(versionMatch[1], 10);
  }
} catch (_) {
  // 检测失败时使用默认值
}

// Jest 30+ 将 --testPathPattern 改为 --testPathPatterns
const testPathFlag = jestMajorVersion >= 30 ? '--testPathPatterns' : '--testPathPattern';

// ==================== 5. 生成 config.json ====================
const dirBaseName = path.basename(componentDir);
const baseCmd = `npx jest --config ${source.jestConfigPath} --detectOpenHandles --ci --useStderr --runInBand --coverage --coverageReporters=json`;

const config = {
  jestConfigPath: source.jestConfigPath,
  coverageDir,
  componentDir,
  componentDirBaseName: dirBaseName,
  componentRegex: `${dirBaseName}/([^/]+)/`,
  testDir,
  updateSnapshotCommand: `${baseCmd} --updateSnapshot`,
  testAllCommand: `${baseCmd} --coverageDirectory=${coverageDir}/all`,
  testOneCommand: `${baseCmd} --coverageDirectory=${coverageDir}/{name} ${testPathFlag}=${dirBaseName}/{name}/ --collectCoverageFrom=${componentDir}/{name}/${coverageGlob}`,
};

fs.mkdirSync(projectDir, { recursive: true });
fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');

console.log('reload 成功，config.json 已生成:\n');
console.log(JSON.stringify(config, null, 2));
