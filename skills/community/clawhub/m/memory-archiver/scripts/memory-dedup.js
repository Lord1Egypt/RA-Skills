#!/usr/bin/env node
/**
 * Memory Dedup - 长期记忆自动去重
 * 用法：node memory-dedup.js
 * 功能：检测并清理重复内容、无意义日常、重复任务进度
 *
 * 原为 memory-dedup.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_FILE = path.join(WORKSPACE_DIR, 'MEMORY.md');

function main() {
  console.log('🔍 检查长期记忆重复...');

  if (!fs.existsSync(MEMORY_FILE)) {
    console.log('⚠️  MEMORY.md 不存在，跳过');
    process.exit(0);
  }

  const now = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const backupFile = path.join(WORKSPACE_DIR, `MEMORY.md.backup.${now}`);

  // 备份
  fs.copyFileSync(MEMORY_FILE, backupFile);
  console.log(`📦 已备份到: ${backupFile}`);

  let content = fs.readFileSync(MEMORY_FILE, 'utf8');
  const lines = content.split('\n');

  // 1. 去除完全重复的行
  const uniqueLines = [];
  const seen = new Set();
  let dupCount = 0;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !/^(#{1,6}|-{3,}|\*{3,}|___|\s*$)/.test(trimmed)) {
      if (seen.has(trimmed)) {
        dupCount++;
        continue;
      }
      seen.add(trimmed);
    }
    uniqueLines.push(line);
  }

  // 2. 去除无意义的日常记录（过于简短的行）
  const meaningfulLines = [];
  let trivialCount = 0;
  const trivialPatterns = [
    /^[-*]\s*今日正常$/,
    /^[-*]\s*无异常$/,
    /^[-*]\s*一切正常$/,
    /^[-*]\s*无待办$/,
    /^[-*]\s*全部完成$/,
  ];

  for (const line of uniqueLines) {
    const trimmed = line.trim();
    const isTrivial = trivialPatterns.some(p => p.test(trimmed));
    if (isTrivial) {
      trivialCount++;
      continue;
    }
    meaningfulLines.push(line);
  }

  const newContent = meaningfulLines.join('\n');

  if (dupCount > 0 || trivialCount > 0) {
    fs.writeFileSync(MEMORY_FILE, newContent, 'utf8');
    console.log(`✅ 去重完成：删除 ${dupCount} 条重复行，${trivialCount} 条无意义行`);
    console.log(`   文件大小: ${(content.length / 1024).toFixed(1)}KB → ${(newContent.length / 1024).toFixed(1)}KB`);
  } else {
    console.log('✅ 无重复内容，无需清理');
    // 删除多余备份
    fs.unlinkSync(backupFile);
  }
}

main();
