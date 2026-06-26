// session-search.mjs - Session 日志搜索 (v2.0)
// 从 OpenClaw session 日志中搜索对话内容

import fs from 'fs';
import path from 'path';
import { loadConfig, getPath } from '../db/config-loader.mjs';

// 搜索 session 日志
export function searchSessionLogs(keywords, options = {}) {
  const { maxFiles = 3, maxResultsPerFile = 3, daysBack = 7 } = options;
  const config = loadConfig();
  const sessionDir = getPath('sessionDir', config);

  if (!fs.existsSync(sessionDir)) {
    console.warn('Session 目录不存在:', sessionDir);
    return [];
  }

  const results = [];
  const cutoff = Date.now() - daysBack * 24 * 60 * 60 * 1000;

  // 获取最近的 session 文件
  const files = fs.readdirSync(sessionDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({
      name: f,
      path: path.join(sessionDir, f),
      mtime: fs.statSync(path.join(sessionDir, f)).mtime.getTime()
    }))
    .filter(f => f.mtime >= cutoff)
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, maxFiles);

  for (const file of files) {
    try {
      const content = fs.readFileSync(file.path, 'utf-8');
      const lines = content.split('\n').filter(Boolean);
      const matches = [];

      for (const line of lines) {
        try {
          const entry = JSON.parse(line);

          // 检查是否匹配关键词
          const text = extractText(entry);
          if (!text) continue;

          const matchScore = matchKeywords(text, keywords);
          if (matchScore > 0) {
            matches.push({
              sessionId: file.name.replace('.jsonl', ''),
              timestamp: entry.timestamp || entry.created_at,
              role: entry.role || 'unknown',
              text: text.slice(0, 500),
              matchScore,
              keywords: keywords.filter(k => text.includes(k)),
            });
          }
        } catch {}
      }

      // 按匹配度排序，取前N条
      matches.sort((a, b) => b.matchScore - a.matchScore);
      results.push(...matches.slice(0, maxResultsPerFile));

    } catch (e) {
      console.warn('读取 session 失败:', file.name, e.message);
    }
  }

  return results;
}

// 提取文本内容
function extractText(entry) {
  if (typeof entry.content === 'string') return entry.content;
  if (entry.message?.content) {
    if (typeof entry.message.content === 'string') return entry.message.content;
    if (Array.isArray(entry.message.content)) {
      return entry.message.content
        .filter(c => c.type === 'text')
        .map(c => c.text)
        .join(' ');
    }
  }
  if (entry.text) return entry.text;
  return '';
}

// 匹配关键词
function matchKeywords(text, keywords) {
  let score = 0;
  const lowerText = text.toLowerCase();

  for (const kw of keywords) {
    const lowerKw = kw.toLowerCase();
    if (lowerText.includes(lowerKw)) {
      score += lowerKw.length; // 长关键词权重更高
    }
  }

  return score;
}

// 获取 session 内的消息上下文
export function getSessionContext(sessionId, options = {}) {
  const { aroundId, contextSize = 2 } = options;
  const config = loadConfig();
  const sessionDir = getPath('sessionDir', config);
  const filePath = path.join(sessionDir, `${sessionId}.jsonl`);

  if (!fs.existsSync(filePath)) return [];

  const messages = [];
  const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(Boolean);

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const text = extractText(entry);
      if (text) {
        messages.push({
          id: entry.id || entry.message_id,
          timestamp: entry.timestamp || entry.created_at,
          role: entry.role || 'user',
          text,
        });
      }
    } catch {}
  }

  // 如果指定了 aroundId，返回上下文窗口
  if (aroundId) {
    const idx = messages.findIndex(m => m.id === aroundId);
    if (idx >= 0) {
      const start = Math.max(0, idx - contextSize);
      const end = Math.min(messages.length, idx + contextSize + 1);
      return messages.slice(start, end);
    }
  }

  return messages;
}

// 获取最近的 session 消息
export function getRecentSessionMessages(options = {}) {
  const { limit = 100, daysBack = 1 } = options;
  const config = loadConfig();
  const sessionDir = getPath('sessionDir', config);

  if (!fs.existsSync(sessionDir)) return [];

  const cutoff = Date.now() - daysBack * 24 * 60 * 60 * 1000;
  const messages = [];

  const files = fs.readdirSync(sessionDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({
      name: f,
      path: path.join(sessionDir, f),
      mtime: fs.statSync(path.join(sessionDir, f)).mtime.getTime()
    }))
    .filter(f => f.mtime >= cutoff)
    .sort((a, b) => b.mtime - a.mtime);

  for (const file of files) {
    try {
      const lines = fs.readFileSync(file.path, 'utf-8').split('\n').filter(Boolean);
      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          const text = extractText(entry);
          if (text && text.length > 10) {
            messages.push({
              sessionId: file.name.replace('.jsonl', ''),
              timestamp: entry.timestamp || entry.created_at,
              role: entry.role || 'user',
              text,
            });
          }
        } catch {}
      }
    } catch {}

    if (messages.length >= limit) break;
  }

  return messages.slice(0, limit);
}