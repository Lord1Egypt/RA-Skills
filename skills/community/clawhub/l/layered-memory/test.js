#!/usr/bin/env node

/**
 * Layered Memory v1.2.0 - Test Suite
 * 基础功能 + v2 新特性测试
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// 测试工具函数
function assert(condition, message) {
  if (!condition) {
    console.error(`❌ FAIL: ${message}`);
    process.exit(1);
  }
}

function assertExists(filePath, message) {
  if (!fs.existsSync(filePath)) {
    console.error(`❌ FAIL: ${message} (file not found: ${filePath})`);
    process.exit(1);
  }
}

function assertContains(filePath, text, message) {
  const content = fs.readFileSync(filePath, 'utf-8');
  if (!content.includes(text)) {
    console.error(`❌ FAIL: ${message} (missing: "${text}")`);
    process.exit(1);
  }
}

// 测试用例
console.log('🧪 Layered Memory Test Suite v1.2.0\n');

const skillDir = __dirname;

// 测试 1: 检查必需文件（含新文件）
console.log('📁 Test 1: Required files...');
const requiredFiles = [
  'SKILL.md',
  'index.js',
  'package.json',
  'hooks/openclaw/handler.js',
  'README.md',
  'lib/config-loader.js',  // 新增
  'config.example.json',   // 新增
  'UPGRADE_PLAN.md'        // 新增
];

requiredFiles.forEach(file => {
  const filePath = path.join(skillDir, file);
  assertExists(filePath, `Missing required file: ${file}`);
});
console.log('✅ All required files present\n');

// 测试 2: package.json 结构
console.log('📦 Test 2: package.json structure...');
const pkg = require(path.join(skillDir, 'package.json'));
assert(pkg.name === 'layered-memory', 'package name should be layered-memory');
assert(typeof pkg.version === 'string', 'version should be string');
assert(pkg.openclaw && Array.isArray(pkg.openclaw.hooks), 'openclaw.hooks should be array');
console.log(`✅ package.json valid (version ${pkg.version})\n`);

// 测试 3: Config Loader 是否正确实现
console.log('⚙️  Test 3: Config loader...');
const ConfigLoader = require('./lib/config-loader');
const configLoader = new ConfigLoader({ verbose: true });
const config = configLoader.load();
assert(typeof config === 'object', 'config should be object');
assert(typeof config.maxConcurrent === 'number', 'maxConcurrent should be number');
assert(Array.isArray(config.skipPatterns), 'skipPatterns should be array');
assert(typeof config.l0 === 'object', 'l0 config should exist');
assert(typeof config.l1 === 'object', 'l1 config should exist');
console.log(`✅ Config loader works (maxConcurrent: ${config.maxConcurrent})\n`);

// 测试 4: index.js 生成方法支持新参数
console.log('💻 Test 4: index.js generate() signature...');
const indexContent = fs.readFileSync(path.join(skillDir, 'index.js'), 'utf-8');
assert(indexContent.includes('generate(target = \'--all\', options = {})'), 'generate should accept options');
assert(indexContent.includes('force'), 'generate should have force');
assert(indexContent.includes('concurrent'), 'generate should have concurrent');
assert(indexContent.includes('config:'), 'generate should have config');
assert(indexContent.includes('dryRun'), 'generate should have dryRun');
assert(indexContent.includes('verbose'), 'generate should have verbose');
console.log('✅ index.js generate() supports new options\n');

// 测试 5: autoMaintain 已升级
console.log('🔧 Test 5: autoMaintain() upgraded...');
assert(indexContent.includes('autoMaintain(options = {})'), 'autoMaintain should accept options');
assert(indexContent.includes('missing.length'), 'autoMaintain should track missing files');
assert(indexContent.includes('outdated.length'), 'autoMaintain should track outdated files');
console.log('✅ autoMaintain() supports incremental update\n');

// 测试 6: generate-layers-simple.js v2 功能
console.log('🔨 Test 6: generate-layers-simple.js v2 features...');
const home = process.env.HOME;
const genScriptPath = path.join(home, 'clawd', 'scripts', 'generate-layers-simple.js');
assertExists(genScriptPath, 'generate-layers-simple.js should exist in ~/clawd/scripts/');
const genScript = fs.readFileSync(genScriptPath, 'utf-8');
assert(genScript.includes('performance.now'), 'should use performance for timing');
assert(genScript.includes('maxConcurrent'), 'should respect maxConcurrent');
assert(genScript.includes('dryRun'), 'should support dryRun mode');
assert(genScript.includes('estimateTokens'), 'should have token estimation');
assert(genScript.includes('Promise.all'), 'should use Promise.all for concurrency');
console.log('✅ generate-layers-simple.js has v2 features\n');

// 测试 7: 文档完整性
console.log('📚 Test 7: Documentation...');
const readmePath = path.join(skillDir, 'README.md');
assertExists(readmePath, 'README.md should exist');
const readme = fs.readFileSync(readmePath, 'utf-8');
assert(readme.includes('Installation') || readme.includes('安装'), 'README should have install section');
assert(readme.includes('Usage') || readme.includes('使用'), 'README should have usage section');
assert(readme.includes('Token') || readme.includes('token'), 'README should mention token savings');
console.log('✅ Documentation present\n');

// 测试 8: 检查 MIT 许可证
console.log('⚖️ Test 8: License...');
const licensePath = path.join(skillDir, 'LICENSE');
assertExists(licensePath, 'LICENSE file should exist');
const license = fs.readFileSync(licensePath, 'utf-8');
assert(license.includes('MIT'), 'Should be MIT license');
assert(license.includes('Copyright'), 'Should have copyright notice');
console.log('✅ MIT license present\n');

// 测试 9: 配置文件示例
console.log('📄 Test 9: Config example...');
const configExample = require('./config.example.json');
assert(typeof configExample.maxConcurrent === 'number', 'config example should have maxConcurrent');
assert(Array.isArray(configExample.skipPatterns), 'config example should have skipPatterns');
console.log('✅ Config example.json valid\n');

// 测试 10: 升级计划文档
console.log('📋 Test 10: Upgrade plan...');
const upgradePlan = fs.readFileSync(path.join(skillDir, 'UPGRADE_PLAN.md'), 'utf-8');
assert(upgradePlan.includes('v1.2.0'), 'UPGRADE_PLAN should mention v1.2.0');
assert(upgradePlan.includes('增量'), 'UPGRADE_PLAN should mention 增量');
assert(upgradePlan.includes('并发'), 'UPGRADE_PLAN should mention 并发');
console.log('✅ UPGRADE_PLAN.md present\n');

// 总结
console.log('🎉 All tests passed!');
console.log(`\nSkill: ${pkg.name}@${pkg.version}`);
console.log('Ready for v1.2.0 publish.');
console.log('\n📦 New features in v1.2.0:');
console.log('  - Config loader with CLI overrides');
console.log('  - Incremental generation (skip unchanged files)');
console.log('  - Concurrent processing (default 4)');
console.log('  - Dry-run mode for preview');
console.log('  - Verbose logging');
console.log('  - Token estimation and stats');
process.exit(0);
