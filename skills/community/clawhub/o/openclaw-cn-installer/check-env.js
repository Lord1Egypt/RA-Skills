#!/usr/bin/env node
/**
 * OpenClaw CN Installer - Environment Checker
 * 检测系统环境是否满足 OpenClaw 运行要求
 */

const { execSync } = require('child_process');
const os = require('os');
const fs = require('fs');
const path = require('path');

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

function check(text, pass, detail = '') {
  const icon = pass ? `${GREEN}✅` : `${RED}❌`;
  console.log(`${icon} ${text}${RESET}${detail ? ` (${detail})` : ''}`);
  return pass;
}

console.log('\n🔍 OpenClaw 中文环境检测\n');
console.log('─'.repeat(50));

const results = [];

// 1. Node.js 版本
try {
  const nodeVersion = process.version.replace('v', '');
  const major = parseInt(nodeVersion.split('.')[0]);
  const pass = major >= 18;
  results.push(check('Node.js 版本', pass, `v${nodeVersion}`));
} catch (e) {
  results.push(check('Node.js 版本', false, '未安装'));
}

// 2. 操作系统
const platform = os.platform();
const arch = os.arch();
const osMap = { darwin: 'macOS', win32: 'Windows', linux: 'Linux' };
results.push(check('操作系统', true, `${osMap[platform] || platform} (${arch})`));

// 3. 内存
const memGB = Math.round(os.totalmem() / 1024 / 1024 / 1024);
results.push(check('内存', memGB >= 4, `${memGB}GB`));

// 4. npm 镜像
try {
  const registry = execSync('npm config get registry', { encoding: 'utf-8' }).trim();
  const isCnMirror = registry.includes('npmmirror') || registry.includes('taobao');
  results.push(check('npm 镜像', true, isCnMirror ? '国内镜像 🇨🇳' : '官方镜像'));
  if (!isCnMirror) {
    console.log(`${YELLOW}💡 建议: npm config set registry https://registry.npmmirror.com${RESET}`);
  }
} catch (e) {
  results.push(check('npm 镜像', false, '无法检测'));
}

// 5. 网络连接
try {
  execSync('curl -s --connect-timeout 3 https://registry.npmmirror.com > /dev/null', { stdio: 'ignore' });
  results.push(check('网络连接', true, '正常'));
} catch (e) {
  results.push(check('网络连接', false, '无法访问 npm 镜像'));
}

// 6. OpenClaw 配置目录
const openclawDir = path.join(os.homedir(), '.openclaw');
const hasConfig = fs.existsSync(openclawDir);
results.push(check('OpenClaw 目录', hasConfig, hasConfig ? '已存在' : '未创建'));

// 7. 检查常用命令
const commands = ['git', 'curl', 'python3'];
commands.forEach(cmd => {
  try {
    execSync(`which ${cmd}`, { stdio: 'ignore' });
    results.push(check(`${cmd} 命令`, true));
  } catch (e) {
    results.push(check(`${cmd} 命令`, false, '未安装'));
  }
});

console.log('─'.repeat(50));

const passCount = results.filter(Boolean).length;
const totalCount = results.length;

console.log(`\n📊 检测结果: ${passCount}/${totalCount} 通过\n`);

if (passCount === totalCount) {
  console.log(`${GREEN}✨ 环境完美，可以开始使用 OpenClaw！${RESET}\n`);
} else if (passCount >= totalCount * 0.7) {
  console.log(`${YELLOW}⚠️  部分功能可能受限，建议修复上述问题${RESET}\n`);
} else {
  console.log(`${RED}❌ 环境不满足要求，请先安装必要的依赖${RESET}\n`);
}

// 推荐下一步
console.log('📖 推荐阅读:');
console.log('   OpenClaw 文档: https://docs.openclaw.ai');
console.log('   中文教程: 运行 node setup-ai.js deepseek\n');
