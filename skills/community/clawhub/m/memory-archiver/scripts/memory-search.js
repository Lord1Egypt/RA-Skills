#!/usr/bin/env node
/**
 * Memory Search - 在加载的记忆中搜索
 * 用法：node memory-search.js "搜索关键词"
 *
 * 原为 memory-search.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw', 'workspace');
const SESSION_STATE = path.join(WORKSPACE_DIR, 'SESSION-STATE.md');

function searchInFile(query, file) {
  if (!fs.existsSync(file)) return [];
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  const results = [];
  const lowerQuery = query.toLowerCase();

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].toLowerCase().includes(lowerQuery)) {
      const start = Math.max(0, i - 3);
      const end = Math.min(lines.length - 1, i + 3);
      results.push({
        line: i + 1,
        context: lines.slice(start, end + 1).join('\n')
      });
    }
  }
  return results;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('用法：node memory-search.js "搜索关键词"');
    console.log('例如：node memory-search.js "CSS 框架"');
    process.exit(1);
  }

  const query = args.join(' ');

  if (!fs.existsSync(SESSION_STATE)) {
    console.log('📚 记忆缓存不存在，先加载记忆...');
    const loaderPath = path.join(__dirname, 'memory-loader.js');
    if (fs.existsSync(loaderPath)) {
      try {
        require('child_process').execSync(`node "${loaderPath}"`, { stdio: 'inherit' });
      } catch (e) {
        console.log('⚠️  记忆加载失败');
        process.exit(1);
      }
    }
  }

  console.log(`🔍 搜索: "${query}"`);
  console.log('');

  const results = searchInFile(query, SESSION_STATE);

  if (results.length === 0) {
    console.log('📭 未找到相关记忆');
  } else {
    console.log(`✅ 找到 ${results.length} 处匹配:\n`);
    results.forEach((r, i) => {
      console.log(`--- 匹配 #${i + 1} (行 ${r.line}) ---`);
      console.log(r.context);
      console.log('');
    });
  }
}

main();
