// session-search.mjs - 日志优先检索模块
// 用于在memory文件找不到时，搜索session日志

import fs from 'fs';
import path from 'path';

const SESSION_DIR = '/root/.openclaw/agents/main/sessions';

// 提取消息内容
function extractContent(obj) {
  const msg = obj?.message || {};
  if (typeof msg.content === 'string') return msg.content;
  if (Array.isArray(msg.content)) {
    return msg.content.map(c => c.text || c).join(' ');
  }
  return '';
}

// 搜索单个session文件
function searchSessionFile(filePath, keywords, maxResults = 5) {
  const results = [];
  const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(l => l.trim());
  
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      const role = obj?.message?.role;
      const content = extractContent(obj);
      
      if (!role || !content) continue;
      
      // 关键词匹配（简单版本，后面用向量）
      const matched = keywords.some(kw => 
        content.toLowerCase().includes(kw.toLowerCase())
      );
      
      if (matched) {
        results.push({
          role,
          content: content.slice(0, 300),
          timestamp: obj.timestamp,
          score: keywords.filter(kw => content.toLowerCase().includes(kw.toLowerCase())).length
        });
      }
    } catch (e) {}
  }
  
  // 按score降序，取前maxResults
  return results.sort((a, b) => b.score - a.score).slice(0, maxResults);
}

// 搜索所有session
export function searchSessionLogs(keywords, options = {}) {
  const { maxFiles = 3, maxResultsPerFile = 3, daysBack = 7 } = options;
  
  // 获取最近的session文件
  const files = fs.readdirSync(SESSION_DIR)
    .filter(f => f.endsWith('.jsonl') && !f.includes('.reset') && !f.includes('.deleted'))
    .map(f => ({
      name: f,
      path: path.join(SESSION_DIR, f),
      mtime: fs.statSync(path.join(SESSION_DIR, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, maxFiles);
  
  const allResults = [];
  for (const file of files) {
    const results = searchSessionFile(file.path, keywords, maxResultsPerFile);
    allResults.push(...results.map(r => ({ ...r, session: file.name })));
  }
  
  return allResults.sort((a, b) => b.score - a.score).slice(0, 10);
}

// 获取最近对话摘要
export function getRecentSessionSummary(minutes = 60, maxMsgs = 20) {
  const cutoff = Date.now() - minutes * 60 * 1000;
  const files = fs.readdirSync(SESSION_DIR)
    .filter(f => f.endsWith('.jsonl') && !f.includes('.reset') && !f.includes('.deleted'))
    .map(f => ({
      path: path.join(SESSION_DIR, f),
      mtime: fs.statSync(path.join(SESSION_DIR, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, 2); // 最近2个session
  
  const messages = [];
  for (const file of files) {
    const lines = fs.readFileSync(file.path, 'utf-8').split('\n').filter(l => l.trim());
    for (const line of lines.slice(-maxMsgs)) {
      try {
        const obj = JSON.parse(line);
        const ts = new Date(obj.timestamp || 0).getTime();
        if (ts > cutoff) {
          const role = obj?.message?.role;
          const content = extractContent(obj);
          if (role && content && content.length < 1000) {
            messages.push({ role, content: content.slice(0, 200), timestamp: obj.timestamp });
          }
        }
      } catch (e) {}
    }
  }
  
  return messages.slice(-maxMsgs);
}

// CLI测试
if (process.argv[1]?.endsWith('session-search.mjs')) {
  const keywords = process.argv.slice(2);
  if (keywords.length === 0) {
    console.log('用法: node session-search.mjs <关键词1> <关键词2> ...');
    console.log('测试最近对话摘要:');
    console.log(getRecentSessionSummary(120, 5));
    process.exit(0);
  }
  
  console.log(`搜索关键词: ${keywords.join(', ')}`);
  const results = searchSessionLogs(keywords);
  console.log(`\n找到 ${results.length} 条匹配:`);
  results.forEach((r, i) => {
    console.log(`\n[${i+1}] ${r.role} (score:${r.score})`);
    console.log(r.content);
  });
}
