#!/usr/bin/env node
/**
 * Memory Loader - 加载三层记忆到 SESSION-STATE.md
 * 用法：node memory-loader.js
 *
 * 原为 memory-loader.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');
const SESSION_STATE = path.join(WORKSPACE_DIR, 'SESSION-STATE.md');

function main() {
  const sessionStateHeader = `# SESSION-STATE.md - 会话记忆缓存

> 自动加载的三层记忆内容（用于快速搜索）
> 生成时间: ${new Date().toISOString()}

`;

  let content = sessionStateHeader;

  // 加载长期记忆
  const memoryMd = path.join(WORKSPACE_DIR, 'MEMORY.md');
  if (fs.existsSync(memoryMd)) {
    const memContent = fs.readFileSync(memoryMd, 'utf8');
    // 只加载 ## 之后的正文内容，跳过头部元数据
    const bodyStart = memContent.indexOf('\n## ');
    if (bodyStart !== -1) {
      content += '## 长期记忆 (MEMORY.md)\n\n';
      content += memContent.slice(bodyStart);
      content += '\n\n';
    }
  }

  // 加载今日记忆
  const today = new Date().toISOString().slice(0, 10);
  const todayFile = path.join(MEMORY_DIR, 'daily', `${today}.md`);
  if (fs.existsSync(todayFile)) {
    content += '## 今日记忆\n\n';
    content += fs.readFileSync(todayFile, 'utf8');
    content += '\n\n';
  }

  // 加载昨日记忆
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const yesterdayFile = path.join(MEMORY_DIR, 'daily', `${yesterday}.md`);
  if (fs.existsSync(yesterdayFile)) {
    content += '## 昨日记忆\n\n';
    content += fs.readFileSync(yesterdayFile, 'utf8');
    content += '\n\n';
  }

  // 加载最近 weekly 记忆
  const weeklyDir = path.join(MEMORY_DIR, 'weekly');
  if (fs.existsSync(weeklyDir)) {
    const weeklyFiles = fs.readdirSync(weeklyDir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse()
      .slice(0, 2); // 最近 2 个 weekly

    for (const file of weeklyFiles) {
      content += `## 周记忆 (${file.replace('.md', '')})\n\n`;
      content += fs.readFileSync(path.join(weeklyDir, file), 'utf8');
      content += '\n\n';
    }
  }

  // 写入 SESSION-STATE.md
  fs.writeFileSync(SESSION_STATE, content, 'utf8');
  console.log(`📚 记忆已加载到 SESSION-STATE.md`);
}

main();
