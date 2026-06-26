#!/usr/bin/env node
/**
 * Pretext Skill — 依赖安装脚本
 * 自动安装运行 Pretext 所需的 npm 依赖
 *
 * 运行方式：node scripts/install-deps.js
 */

'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = __dirname;
  const packageJsonPath = path.join(SKILL_DIR, 'package.json');

console.log('========================================');
console.log('   Pretext Skill — 依赖安装向导');
console.log('========================================\n');

// 读取 package.json
let packageJson;
try {
  packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  console.log('✅ 找到 package.json');
  console.log('   核心依赖：@chenglou/pretext ^0.0.5');
} catch (e) {
  console.error('❌ 未找到 package.json，请确认在 Skill 目录下运行');
  process.exit(1);
}

// 检测 Node.js 版本
const nodeVersion = process.version;
console.log('   Node.js 版本：' + nodeVersion + '\n');

console.log('========================================');
console.log('   第一步：安装 @chenglou/pretext');
console.log('========================================\n');
try {
  execSync('npm install @chenglou/pretext ^0.0.5', {
    cwd: SKILL_DIR,
    stdio: 'inherit',
    env: { ...process.env }
  });
  console.log('\n✅ @chenglou/pretext 安装成功\n');
} catch (e) {
  console.warn('\n⚠️  @chenglou/pretext 安装失败');
  console.warn('   Skill 仍可使用纯 JS fallback 模式运行（功能完整，精度中等）\n');
}

console.log('========================================');
console.log('   第二步：安装 canvas（推荐，可获最高精度）');
console.log('========================================\n');
console.log('提示：canvas 需要 Cairo 图形库（Linux/macOS 通常已有）');
console.log('      Windows 用户如安装失败，Skill 仍可正常运行\n');

try {
  execSync('npm install canvas', {
    cwd: SKILL_DIR,
    stdio: 'inherit',
    env: { ...process.env }
  });
  console.log('\n✅ canvas 安装成功 — 已启用高精度模式\n');
} catch (e) {
  console.warn('\n⚠️  canvas 安装失败（Cairo 系统库未安装）');
  console.warn('   Skill 已内置纯 JS fallback，仍可正常工作');
  console.warn('   如需 canvas：');
  console.warn('   Linux:  sudo apt install libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev');
  console.warn('   macOS:  brew install pkg-config cairo pango jpeg giflib librsvg\n');
}

console.log('========================================');
console.log('   安装完成！');
console.log('========================================\n');
console.log('测试运行：');
console.log('  node scripts/measure.js --text "你好，世界！" --font "16px sans-serif" --width 300');
console.log('  node scripts/batch.js --items "消息1" --items "消息2" --font "14px sans-serif" --width 375');
console.log('  node scripts/layout-lines.js --text "Hello 世界" --font "16px sans-serif" --width 100\n');

