#!/usr/bin/env node
/**
 * install.js - 记忆系统技能安装脚本
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/home/openclaw/.openclaw/workspace';

console.log('🔧 开始安装 OpenClaw 记忆系统...\n');

// 1. 创建必要目录
const dirs = [
  'memory/multimodal/images',
  'memory/multimodal/tool-calls',
  'memory/multimodal/captions',
  'memory/versions',
  'memory/projects'
];

for (const dir of dirs) {
  const fullPath = path.join(WORKSPACE, dir);
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
    console.log(`✅ 创建目录：${dir}`);
  }
}

// 2. 复制配置文件
const configs = [
  {
    src: 'skills/openclaw-memory-system/configs/multimodal-config.json',
    dst: 'configs/multimodal-config.json'
  },
  {
    src: 'skills/openclaw-memory-system/configs/memory-namespaces.json',
    dst: 'configs/memory-namespaces.json'
  }
];

for (const { src, dst } of configs) {
  const srcPath = path.join(WORKSPACE, src);
  const dstPath = path.join(WORKSPACE, dst);
  
  if (fs.existsSync(srcPath) && !fs.existsSync(dstPath)) {
    fs.copyFileSync(srcPath, dstPath);
    console.log(`✅ 复制配置：${dst}`);
  }
}

console.log('\n✅ 安装完成！\n');
console.log('下一步:');
console.log('1. 编辑 configs/multimodal-config.json 配置存储路径');
console.log('2. 编辑 configs/memory-namespaces.json 配置命名空间');
console.log('3. 运行测试：node skills/multimodal-memory/test-multimodal.js\n');
