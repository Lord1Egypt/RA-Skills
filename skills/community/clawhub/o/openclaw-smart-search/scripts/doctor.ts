#!/usr/bin/env ts-node
/**
 * Smart Search 诊断工具
 * 检查所有依赖、配置和 API Key 状态
 */

import { spawnSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

interface CheckResult {
  name: string;
  status: 'ok' | 'warning' | 'error';
  message: string;
  fix?: string;
}

const results: CheckResult[] = [];

function check(name: string, test: () => { status: 'ok' | 'warning' | 'error'; message: string; fix?: string }) {
  try {
    const result = test();
    results.push({ name, ...result });
  } catch (error: any) {
    results.push({ name, status: 'error', message: error.message });
  }
}

// 1. 检查 Node.js 版本
check('Node.js', () => {
  const version = process.version;
  const major = parseInt(version.slice(1).split('.')[0]);
  if (major >= 18) {
    return { status: 'ok', message: `版本 ${version}` };
  }
  return {
    status: 'error',
    message: `版本过低: ${version}`,
    fix: '请升级到 Node.js 18 或更高版本'
  };
});

// 2. 检查 npm
check('npm', () => {
  const result = spawnSync('npm', ['--version'], { encoding: 'utf8', timeout: 5000 });
  if (result.status === 0) {
    return { status: 'ok', message: `版本 ${result.stdout.trim()}` };
  }
  return { status: 'error', message: '未找到 npm' };
});

// 3. 检查 mcporter
check('mcporter', () => {
  const result = spawnSync('which', ['mcporter'], { encoding: 'utf8', timeout: 5000 });
  if (result.status === 0) {
    const versionResult = spawnSync('mcporter', ['--version'], { encoding: 'utf8', timeout: 5000 });
    const version = versionResult.stdout?.trim() || '已安装';
    return { status: 'ok', message: version.split('\n')[0] };
  }
  return {
    status: 'warning',
    message: '未安装',
    fix: '运行: npm install -g mcporter'
  };
});

// 4. 检查环境变量
check('OPENCLAW_MASTER_KEY', () => {
  const key = process.env.OPENCLAW_MASTER_KEY;
  if (!key) {
    return {
      status: 'error',
      message: '未设置',
      fix: '在 .env 文件中设置: OPENCLAW_MASTER_KEY=<your-key>'
    };
  }
  if (key.length < 32) {
    return {
      status: 'warning',
      message: `长度不足 (${key.length} 字符)`,
      fix: '主密钥应至少 32 字符'
    };
  }
  return { status: 'ok', message: '已设置' };
});

// 5. 检查加密配置文件
check('加密配置文件', () => {
  const configPath = path.join(os.homedir(), '.openclaw', 'secrets', 'smart-search.json.enc');
  if (fs.existsSync(configPath)) {
    const stats = fs.statSync(configPath);
    const mode = stats.mode & 0o777;
    if (mode === 0o600) {
      return { status: 'ok', message: `${configPath} (权限正确)` };
    }
    return {
      status: 'warning',
      message: `权限不安全: ${mode.toString(8)}`,
      fix: '运行: chmod 600 ' + configPath
    };
  }
  return {
    status: 'warning',
    message: '不存在',
    fix: '运行: npm run setup'
  };
});

// 6. 检查 API Key 配置
check('API Keys', () => {
  const configPath = path.join(os.homedir(), '.openclaw', 'secrets', 'smart-search.json.enc');
  if (!fs.existsSync(configPath)) {
    return {
      status: 'warning',
      message: '未配置任何 API Key',
      fix: '运行: npm run setup'
    };
  }

  // v1.0.6 修复：不再尝试解析加密文件
  // 加密文件是二进制格式，不能直接解析为 JSON
  // 只检查文件是否存在和权限是否正确
  try {
    const stats = fs.statSync(configPath);
    const mode = stats.mode & 0o777;

    // 检查文件大小（加密文件应该有一定大小）
    if (stats.size < 100) {
      return {
        status: 'warning',
        message: '配置文件可能损坏（文件过小）',
        fix: '运行: npm run setup 重新配置'
      };
    }

    // 文件存在且有合理大小，视为配置正常
    if (mode === 0o600) {
      return { status: 'ok', message: '已配置（加密存储）' };
    }
    return {
      status: 'warning',
      message: '已配置但权限不安全',
      fix: '运行: chmod 600 ' + configPath
    };
  } catch (error: any) {
    return {
      status: 'error',
      message: `无法访问配置文件: ${error.message}`,
      fix: '检查文件权限或运行: npm run setup'
    };
  }
});

// 7. 检查依赖安装
check('项目依赖', () => {
  const nodeModulesPath = path.join(__dirname, '..', 'node_modules');
  if (fs.existsSync(nodeModulesPath)) {
    return { status: 'ok', message: '已安装' };
  }
  return {
    status: 'error',
    message: '未安装',
    fix: '运行: npm install'
  };
});

// 输出结果
console.log('\n🔍 Smart Search 诊断报告');
console.log('='.repeat(60));

let okCount = 0;
let warningCount = 0;
let errorCount = 0;

for (const result of results) {
  const icon = result.status === 'ok' ? '✅' : result.status === 'warning' ? '⚠️' : '❌';
  console.log(`${icon} ${result.name.padEnd(20)} ${result.message}`);

  if (result.fix) {
    console.log(`   💡 ${result.fix}`);
  }

  if (result.status === 'ok') okCount++;
  else if (result.status === 'warning') warningCount++;
  else errorCount++;
}

console.log('='.repeat(60));
console.log(`总计: ${okCount} 正常, ${warningCount} 警告, ${errorCount} 错误\n`);

// 如果有错误，提供修复建议
if (errorCount > 0) {
  console.log('🔧 快速修复步骤:');
  console.log('1. 安装依赖: npm install');
  console.log('2. 配置主密钥: export OPENCLAW_MASTER_KEY="$(openssl rand -base64 32)"');
  console.log('3. 配置 API Keys: npm run setup');
  console.log('4. 安装 mcporter: npm install -g mcporter (可选，用于百炼搜索)');
  console.log('');
  process.exit(1);
}

if (warningCount > 0) {
  console.log('💡 建议修复上述警告以获得最佳体验。\n');
}

console.log('✅ 所有检查通过，Smart Search 可以正常使用！');
console.log('');
console.log('测试搜索:');
console.log('  npm run search "OpenClaw"');
console.log('');