#!/usr/bin/env node

/**
 * 安装脚本
 * 安装 sharp 依赖
 */

import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, writeFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const skillRoot = join(__dirname, '..');

function installSharp() {
  console.log('📦 正在安装 sharp...\n');
  
  try {
    execSync('npm install', {
      cwd: skillRoot,
      stdio: 'inherit'
    });
    console.log('\n✅ sharp 安装完成！\n');
    return true;
  } catch (error) {
    console.error('\n❌ sharp 安装失败');
    console.error('错误信息:', error.message);
    console.log('\n请尝试手动安装：');
    console.log(`   cd ${skillRoot}`);
    console.log('   npm install\n');
    process.exit(1);
  }
}

// 主函数
export async function installDependencies() {
  installSharp();
}

// 如果直接运行
if (import.meta.url === `file://${process.argv[1]}`) {
  installDependencies();
}
