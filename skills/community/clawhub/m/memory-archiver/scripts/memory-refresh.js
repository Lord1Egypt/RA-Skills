#!/usr/bin/env node
/**
 * Memory Refresh - 智能刷新记忆缓存（检查后刷新）
 * 用法：node memory-refresh.js
 *
 * 原为 memory-refresh.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw', 'workspace');
const DAILY_FILE = path.join(WORKSPACE_DIR, 'memory', 'daily', `${new Date().toISOString().slice(0, 10)}.md`);
const SESSION_STATE = path.join(WORKSPACE_DIR, 'SESSION-STATE.md');

function main() {
  console.log('🔄 智能刷新记忆缓存...');

  // 检查今日记忆文件是否存在
  if (!fs.existsSync(DAILY_FILE)) {
    console.log('⚠️  今日记忆文件不存在，跳过刷新');
    process.exit(0);
  }

  // 检查 SESSION-STATE.md 是否已包含今日记忆
  if (fs.existsSync(SESSION_STATE)) {
    const sessionContent = fs.readFileSync(SESSION_STATE, 'utf8');
    const today = new Date().toISOString().slice(0, 10);
    if (sessionContent.includes(`## 今日记忆`) && sessionContent.includes(today)) {
      console.log('✅ 记忆缓存已是最新，无需刷新');
      process.exit(0);
    }
  }

  // 刷新记忆缓存
  console.log('📝 刷新记忆缓存...');
  const loaderPath = path.join(__dirname, 'memory-loader.js');
  if (fs.existsSync(loaderPath)) {
    try {
      require('child_process').execSync(`node "${loaderPath}"`, { stdio: 'inherit' });
      console.log('✅ 记忆缓存已刷新');
    } catch (e) {
      console.log('⚠️  刷新失败:', e.message);
    }
  }
}

main();
