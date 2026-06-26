// Micro Memory - Utility Functions

import * as fs from 'fs';
import * as path from 'path';

export const STORE_DIR = path.join(__dirname, '..', 'store');
export const INDEX_FILE = path.join(STORE_DIR, 'index.json');
export const LINKS_FILE = path.join(STORE_DIR, 'links.json');
export const REVIEWS_FILE = path.join(STORE_DIR, 'reviews.json');
export const STORE_FILE = path.join(STORE_DIR, 'store.md');
export const ARCHIVE_DIR = path.join(STORE_DIR, 'archive');

export function ensureDir(dir: string): void {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

export function readJson<T>(filePath: string, defaultValue: T): T {
  try {
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf-8');
      return JSON.parse(data) as T;
    }
  } catch (e) {
    console.error(`Error reading ${filePath}:`, e);
  }
  return defaultValue;
}

export function writeJson<T>(filePath: string, data: T): void {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

export function formatTimestamp(date: Date = new Date()): string {
  const pad = (n: number) => n.toString().padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

export function parseTimestamp(ts: string): Date {
  return new Date(ts.replace(' ', 'T'));
}

export function daysBetween(date1: Date, date2: Date): number {
  const msPerDay = 24 * 60 * 60 * 1000;
  return Math.floor((date2.getTime() - date1.getTime()) / msPerDay);
}

export function getStrengthLevel(score: number): string {
  if (score >= 80) return 'permanent';
  if (score >= 60) return 'strong';
  if (score >= 40) return 'stable';
  if (score >= 20) return 'weak';
  return 'critical';
}

export function getStrengthColor(level: string): string {
  const colors: Record<string, string> = {
    permanent: '\x1b[35m', // magenta
    strong: '\x1b[32m',    // green
    stable: '\x1b[36m',    // cyan
    weak: '\x1b[33m',      // yellow
    critical: '\x1b[31m',  // red
  };
  return colors[level] || '\x1b[0m';
}

export function resetColor(): string {
  return '\x1b[0m';
}

export function printColored(text: string, color: string): void {
  const colorCodes: Record<string, string> = {
    cyan: '\x1b[36m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    gray: '\x1b[90m',
  };
  console.log(`${colorCodes[color] || ''}${text}${resetColor()}`);
}

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.substring(0, maxLength - 3) + '...';
}

export function fuzzyMatch(text: string, keyword: string): boolean {
  const normalizedText = text.toLowerCase();
  const normalizedKeyword = keyword.toLowerCase();
  return normalizedText.includes(normalizedKeyword);
}

// ==================== 搜索增强函数 ====================

/**
 * 计算 Levenshtein 编辑距离
 */
export function levenshteinDistance(str1: string, str2: string): number {
  const m = str1.length;
  const n = str2.length;
  const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = Math.min(
          dp[i - 1][j] + 1,     // 删除
          dp[i][j - 1] + 1,     // 插入
          dp[i - 1][j - 1] + 1  // 替换
        );
      }
    }
  }

  return dp[m][n];
}

/**
 * 计算模糊匹配分数 (0-1)
 */
export function fuzzyMatchScore(text: string, keyword: string): number {
  const normalizedText = text.toLowerCase();
  const normalizedKeyword = keyword.toLowerCase();
  
  // 完全匹配
  if (normalizedText === normalizedKeyword) return 1.0;
  
  // 包含匹配
  if (normalizedText.includes(normalizedKeyword)) {
    return 0.8 + (normalizedKeyword.length / normalizedText.length) * 0.2;
  }
  
  // 计算编辑距离相似度
  const distance = levenshteinDistance(normalizedText, normalizedKeyword);
  const maxLen = Math.max(normalizedText.length, normalizedKeyword.length);
  if (maxLen === 0) return 1.0;
  
  return Math.max(0, 1 - distance / maxLen);
}

/**
 * 带容差的模糊匹配
 */
export function fuzzyMatchWithTolerance(text: string, keyword: string, tolerance: number = 0.3): boolean {
  const score = fuzzyMatchScore(text, keyword);
  return score >= (1 - tolerance);
}

/**
 * 正则表达式匹配
 */
export function regexMatch(text: string, pattern: string): boolean {
  try {
    const regex = new RegExp(pattern, 'i');
    return regex.test(text);
  } catch (e) {
    // 如果正则无效，回退到普通包含匹配
    return text.toLowerCase().includes(pattern.toLowerCase());
  }
}

/**
 * 多关键词匹配（AND 逻辑）
 */
export function multiKeywordMatch(text: string, keywords: string[]): boolean {
  const normalizedText = text.toLowerCase();
  return keywords.every(kw => normalizedText.includes(kw.toLowerCase()));
}

/**
 * 计算相关性分数
 */
export function calculateRelevanceScore(memory: { content: string; tag?: string }, keywords: string[]): number {
  let score = 0;
  const content = memory.content.toLowerCase();
  
  for (const keyword of keywords) {
    const normalizedKw = keyword.toLowerCase();
    
    // 标题/内容开头匹配
    if (content.startsWith(normalizedKw)) {
      score += 10;
    }
    // 完整单词匹配
    else if (new RegExp(`\\b${normalizedKw}\\b`, 'i').test(content)) {
      score += 5;
    }
    // 包含匹配
    else if (content.includes(normalizedKw)) {
      score += 3;
    }
    // 模糊匹配
    else if (fuzzyMatchWithTolerance(content, normalizedKw, 0.3)) {
      score += 1;
    }
  }
  
  // 标签匹配加分
  if (memory.tag) {
    for (const keyword of keywords) {
      if (memory.tag.toLowerCase().includes(keyword.toLowerCase())) {
        score += 2;
      }
    }
  }
  
  return score;
}

/**
 * 解析搜索关键词（支持引号包裹的短语）
 */
export function parseSearchKeywords(input: string): string[] {
  const keywords: string[] = [];
  const regex = /"([^"]*)"|(\S+)/g;
  let match;
  
  while ((match = regex.exec(input)) !== null) {
    keywords.push(match[1] || match[2]);
  }
  
  return keywords.length > 0 ? keywords : [input];
}
