#!/usr/bin/env node

/**
 * 环境检测脚本
 * 检测 Node.js、npm 是否安装，给出安装建议
 */

import { execSync } from 'child_process';
import { platform } from 'os';
import { join } from 'path';

const os = platform();

function runCommand(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: 'pipe' }).trim();
  } catch {
    return null;
  }
}

function getNodeVersion() {
  return runCommand('node --version');
}

function getNpmVersion() {
  return runCommand('npm --version');
}

function getInstallCommands() {
  const commands = {
    darwin: {
      official: 'https://nodejs.org/en/download',
      homebrew: 'brew install node',
      description: 'macOS'
    },
    win32: {
      official: 'https://nodejs.org/en/download',
      installer: '下载 LTS 版本 (64-bit Windows Installer)',
      description: 'Windows'
    },
    linux: {
      official: 'https://nodejs.org/en/download',
      ubuntu: 'curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs',
      centos: 'curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash - && sudo yum install -y nodejs',
      description: 'Linux'
    }
  };
  return commands[os] || commands.linux;
}

function printReport() {
  const nodeVersion = getNodeVersion();
  const npmVersion = getNpmVersion();
  const installCmds = getInstallCommands();

  console.log('🔍 检测环境...\n');

  let allGood = true;

  if (nodeVersion) {
    console.log(`✅ Node.js ${nodeVersion} 已安装`);
  } else {
    console.log(`❌ 未检测到 Node.js`);
    allGood = false;
  }

  if (npmVersion) {
    console.log(`✅ npm ${npmVersion} 已安装`);
  } else {
    console.log(`❌ 未检测到 npm`);
    allGood = false;
  }

  console.log('');

  if (!allGood) {
    console.log('请先安装 Node.js：\n');
    console.log(`🔗 官网下载：${installCmds.official}`);
    
    if (installCmds.homebrew) {
      console.log(`📦 Homebrew: ${installCmds.homebrew}`);
    }
    if (installCmds.installer) {
      console.log(`📦 推荐下载：${installCmds.installer}`);
    }
    if (installCmds.ubuntu) {
      console.log(`📦 Ubuntu/Debian: ${installCmds.ubuntu}`);
      console.log(`📦 CentOS/RHEL: ${installCmds.centos}`);
    }
    
    console.log('\n安装完成后重新运行此技能。');
    process.exit(1);
  }

  console.log('✅ 环境检测通过！\n');
  return { nodeVersion, npmVersion };
}

// 主函数
export async function detectEnvironment() {
  const result = printReport();
  return result;
}

// 如果直接运行
if (import.meta.url === `file://${process.argv[1]}`) {
  detectEnvironment();
}
