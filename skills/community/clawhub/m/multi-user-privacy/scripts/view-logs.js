#!/usr/bin/env node

/**
 * 查看隐私检查日志
 * 
 * 用法：
 * node scripts/view-logs.js              # 查看最近 10 条
 * node scripts/view-logs.js 50           # 查看最近 50 条
 * node scripts/view-logs.js --user=xxx   # 查看特定用户
 * node scripts/view-logs.js --failures   # 只查看失败的
 */

const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(process.env.HOME, '.openclaw/logs/privacy-guard.json');
const SIMPLE_LOG = path.join(process.env.HOME, '.openclaw/logs/privacy-guard.log');

function parseArgs() {
  const args = {
    limit: 10,
    user: null,
    failuresOnly: false
  };
  
  for (const arg of process.argv.slice(2)) {
    if (!isNaN(parseInt(arg))) {
      args.limit = parseInt(arg);
    } else if (arg.startsWith('--user=')) {
      args.user = arg.split('=')[1];
    } else if (arg === '--failures') {
      args.failuresOnly = true;
    }
  }
  
  return args;
}

function viewLogs() {
  const args = parseArgs();
  
  if (!fs.existsSync(LOG_FILE)) {
    console.log('📝 暂无日志记录');
    return;
  }
  
  const content = fs.readFileSync(LOG_FILE, 'utf-8');
  const lines = content.trim().split('\n').filter(l => l.trim());
  
  let entries = [];
  for (const line of lines) {
    try {
      entries.push(JSON.parse(line));
    } catch (e) {
      // 跳过无效行
    }
  }
  
  // 过滤
  if (args.user) {
    entries = entries.filter(e => e.user === args.user);
  }
  if (args.failuresOnly) {
    entries = entries.filter(e => e.status !== 'PASS' || !e.privacy.ok);
  }
  
  // 取最近的
  entries = entries.slice(-args.limit);
  
  // 显示
  console.log(`\n📋 隐私检查日志（最近 ${entries.length} 条）\n`);
  console.log('='.repeat(80));
  
  for (const entry of entries) {
    const statusIcon = entry.privacy.ok ? '✅' : '❌';
    console.log(`\n${statusIcon} ${entry.timestamp}`);
    console.log(`   用户：${entry.user}`);
    console.log(`   状态：${entry.status}`);
    console.log(`   记忆：${entry.memory.loaded} 个已加载，${entry.memory.missing} 个缺失`);
    console.log(`   隐私：${entry.privacy.ok ? '通过' : '失败'}`);
    
    if (entry.message) {
      console.log(`   消息：${entry.message.substring(0, 50)}...`);
    }
    if (entry.response) {
      console.log(`   回复：${entry.response.substring(0, 50)}...`);
    }
    if (entry.privacy.issues && entry.privacy.issues.length > 0) {
      console.log(`   问题:`);
      entry.privacy.issues.forEach(issue => {
        console.log(`     - ${issue.type}: ${issue.message}`);
      });
    }
    if (entry.execution_time_ms) {
      console.log(`   耗时：${entry.execution_time_ms}ms`);
    }
  }
  
  console.log('\n' + '='.repeat(80));
  console.log(`\n📁 日志文件：${LOG_FILE}`);
  console.log(`📁 简化日志：${SIMPLE_LOG}`);
  console.log(`\n💡 使用示例:`);
  console.log(`   node scripts/view-logs.js 50          # 查看最近 50 条`);
  console.log(`   node scripts/view-logs.js --failures  # 只查看失败的`);
  console.log(`   node scripts/view-logs.js --user=xxx  # 查看特定用户\n`);
}

viewLogs();
