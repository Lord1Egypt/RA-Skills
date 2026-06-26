#!/usr/bin/env node

/**
 * 安装后配置脚本
 * 确认输出目录，输出使用说明
 */

import { homedir } from 'os';
import { join } from 'path';
import { mkdirSync, existsSync, writeFileSync } from 'fs';

const defaultOutputDir = join(homedir(), 'Downloads', 'compressed-images');

function ensureOutputDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
    console.log(`📁 已创建输出目录：${dir}\n`);
  } else {
    console.log(`📁 输出目录已存在：${dir}\n`);
  }
}

function printUsageGuide() {
  console.log('💡 基础使用说明：');
  console.log('   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('   📌 默认设置：');
  console.log('      - 画质：85%（画质优先）');
  console.log('      - 格式：保持原格式');
  console.log('      - 尺寸：不缩放');
  console.log('');
  console.log('   🎮 自定义玩法：');
  console.log('      - 指定格式：/compress image.png --format jpg');
  console.log('      - 调整画质：/compress image.jpg --quality 0.6');
  console.log('      - 限制尺寸：/compress image.jpg --maxWidth 1920');
  console.log('      - 批量压缩：/compress ./photos/ --recursive');
  console.log('      - 组合使用：/compress ./photos/ --format webp --quality 0.8 --recursive');
  console.log('');
  console.log('   📖 完整帮助：/compress --help');
  console.log('   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
}

function saveConfig(config) {
  const configPath = join(homedir(), '.openclaw', 'workspace', 'skills', 'image-compress', 'config.json');
  const configDir = join(homedir(), '.openclaw', 'workspace', 'skills', 'image-compress');
  
  if (!existsSync(configDir)) {
    mkdirSync(configDir, { recursive: true });
  }
  
  writeFileSync(configPath, JSON.stringify(config, null, 2));
}

// 主函数
export async function postInstall(userOutputDir = null) {
  const outputDir = userOutputDir || defaultOutputDir;
  
  ensureOutputDir(outputDir);
  printUsageGuide();
  
  // 保存配置
  saveConfig({
    outputDir: outputDir,
    defaultQuality: 0.85,
    defaultFormat: 'original'
  });
  
  console.log('✅ 安装配置完成！\n');
  console.log('现在可以使用 /compress 命令压缩图片了。');
}

// 如果直接运行
if (import.meta.url === `file://${process.argv[1]}`) {
  postInstall();
}
