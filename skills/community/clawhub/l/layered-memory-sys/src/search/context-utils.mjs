// context-utils.mjs - v1.2 功能：上下文补齐 + Session 分组

import { getSessionContext } from './session-search.mjs';

// 上下文补齐：命中消息前后各 N 条
export function enrichWithContext(match, contextSize = 2) {
  if (!match.sessionId || !match.id) return match;

  const context = getSessionContext(match.sessionId, {
    aroundId: match.id,
    contextSize
  });

  const idx = context.findIndex(m => m.id === match.id);
  if (idx < 0) return match;

  return {
    ...match,
    context: {
      before: context.slice(0, idx),
      after: context.slice(idx + 1),
    }
  };
}

// Session 分组去重
export function groupBySession(results) {
  const groups = new Map();

  for (const r of results) {
    const sid = r.sessionId || 'unknown';
    if (!groups.has(sid)) {
      groups.set(sid, {
        sessionId: sid,
        matches: [],
        bestScore: 0,
      });
    }

    const group = groups.get(sid);
    group.matches.push(r);
    if (r.score > group.bestScore) {
      group.bestScore = r.score;
      group.bestMatch = r;
    }
  }

  // 每组只保留最佳匹配 + 片段汇总
  return Array.from(groups.values())
    .sort((a, b) => b.bestScore - a.bestScore)
    .map(g => ({
      sessionId: g.sessionId,
      matchCount: g.matches.length,
      bestMatch: g.bestMatch,
      allSnippets: g.matches.slice(0, 3).map(m => ({
        title: m.title,
        snippet: m.snippet || m.summary?.slice(0, 100),
        score: m.score,
      })),
    }));
}

// 提取 snippet（带高亮）
export function extractSnippet(text, keywords, maxLen = 150) {
  if (!text) return '';

  // 找到关键词最早出现的位置
  let bestPos = 0;
  let bestScore = 0;

  for (let i = 0; i < text.length; i++) {
    let score = 0;
    for (const kw of keywords) {
      if (text.substring(i, i + kw.length).includes(kw)) {
        score += kw.length;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestPos = i;
    }
  }

  // 提取片段
  const start = Math.max(0, bestPos - 30);
  const end = Math.min(text.length, start + maxLen);
  let snippet = text.slice(start, end);
  if (start > 0) snippet = '...' + snippet;
  if (end < text.length) snippet += '...';

  // 高亮关键词
  for (const kw of keywords) {
    snippet = snippet.replaceAll(kw, `<<<${kw}>>>`);
  }

  return snippet;
}