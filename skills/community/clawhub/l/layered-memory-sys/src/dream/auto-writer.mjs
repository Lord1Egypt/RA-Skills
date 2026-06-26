// auto-writer.mjs - 自动写入检测 (v2.0)
// 从 session 日志检测值得记住的内容

import { createMemory, logEvent } from '../db/repository.mjs';
import { search } from '../search/search-engine.mjs';
import { getRecentSessionMessages } from '../search/session-search.mjs';
import { clearIDFCache } from '../search/tokenizer.mjs';
import { randomUUID } from 'crypto';
import { emit, EVENTS } from '../events/event-bus.mjs';
import { getDb, saveDatabase } from '../db/database.mjs';

// 记住关键词（扩展版）
const REMEMBER_KEYWORDS = [
  '记住这个', '记住', '别忘了', '别忘了这个',
  '记下来', '帮我记', '存起来', '保存一下',
  '下次提醒我', '提醒我', '记住以后', '别忘了',
  '标注一下', '标记一下', '重要的事',
];

// 过滤模式（非真实对话）
const FILTER_PATTERNS = [
  /^Read HEARTBEAT\.md/,
  /^HEARTBEAT_/,
  /^HEARTBEAT_OK/,
  /^Conversation info \(untrusted metadata\)/,
  /^System \(untrusted\)/,
  /^Queued messages/,
  /^Exec completed/,
  /^Exec failed/,
  /^System \(untrusted\)/,
  /^\[non-text content/,
  /^Compaction summary/,
  /^NO_REPLY$/,
  /^<summary>/,
  /^<\/summary>$/,
  /^\s*$/,
];

// ========== 去重追踪 ==========

function ensureProcessedTable() {
  const db = getDb();
  db.exec(`CREATE TABLE IF NOT EXISTS processed_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    created_at INTEGER NOT NULL
  )`);
}

function computeMsgKey(sessionId, text) {
  const key = (sessionId || '') + ':' + (text || '').slice(0, 50);
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = ((hash << 5) - hash) + key.charCodeAt(i);
    hash |= 0;
  }
  return 'msg_' + Math.abs(hash).toString(36) + '_' + (sessionId || 'x').slice(-6);
}

function isProcessed(sessionId, text) {
  try {
    const key = computeMsgKey(sessionId, text);
    const r = getDb().exec('SELECT 1 FROM processed_messages WHERE id = ?', [key]);
    return r.length > 0 && r[0].values.length > 0;
  } catch { return false; }
}

function markProcessed(sessionId, text) {
  try {
    const key = computeMsgKey(sessionId, text);
    getDb().run('INSERT OR IGNORE INTO processed_messages VALUES (?,?,?)',
      [key, sessionId || '', Date.now()]);
    saveDatabase();
  } catch (e) { console.warn('标记失败:', e.message); }
}

// 检测并写入记忆
export async function autoDetectMemories(config) {
  ensureProcessedTable();
  // 1. 获取最近的 session 消息
  let messages;
  try {
    messages = getRecentSessionMessages({ limit: 200, daysBack: 1 });
  } catch (e) {
    console.warn('获取 session 消息失败:', e.message);
    return 0;
  }

  if (!messages || messages.length === 0) return 0;

  let created = 0;

  // 2. 过滤系统消息
  const realMessages = messages.filter(m => {
    if (FILTER_PATTERNS.some(p => p.test(m.text))) return false;
    if (m.text.length < 10) return false;
    return true;
  });

  if (realMessages.length === 0) return 0;

  // 3. 统计对话特征
  const totalTurns = realMessages.length;
  const hasRememberKeyword = realMessages.some(m =>
    REMEMBER_KEYWORDS.some(kw => m.text.includes(kw))
  );

  // 提取所有"记住"相关的内容
  const rememberMessages = realMessages.filter(m =>
    REMEMBER_KEYWORDS.some(kw => m.text.includes(kw))
  );

  // 4. 提取话题标签
  const topicPatterns = [
    /(?:关于|聊聊|讨论一下|看看)(.{2,15}?)(?:的|吧|了|$)/g,
    /(?:帮我|我要|我想|我们)(.{2,15}?)(?:一下|吧|啊|呢|$)/g,
    /#(\S+)/g,
  ];
  const topics = new Set();
  for (const msg of realMessages) {
    for (const pattern of topicPatterns) {
      let match;
      while ((match = pattern.exec(msg.text)) !== null) {
        if (match[1] && match[1].length >= 2) {
          topics.add(match[1].trim());
        }
      }
    }
  }

  // 5. 判断是否需要写入
  const shouldWrite = hasRememberKeyword || totalTurns > 15;

  if (!shouldWrite) return 0;

  // 6. 对每条"记住"消息创建记忆
  for (const msg of rememberMessages) {
    // 🛡️ 去重
    if (isProcessed(msg.sessionId, msg.text)) continue;

    const content = msg.text
      .replace(/^.*?(记住|别忘了|记下来|帮我记|存起来|保存一下|提醒我)/s, '')
      .trim()
      .slice(0, 300);

    if (content.length < 5) continue;

    // 语义去重
    try {
      const existing = await search(content.slice(0, 100), { limit: 3, threshold: 0.85, config });
      if (existing.length > 0) {
        markProcessed(msg.sessionId, msg.text);
        continue;
      }
    } catch {}

    // 创建新记忆
    const title = extractTitle(content);
    const summary = content.slice(0, 200);
    const tagList = Array.from(topics).slice(0, 5);

    try {
      const mem = createMemory({
        id: `auto-${Date.now()}-${randomUUID().slice(0, 8)}`,
        title,
        summary,
        content: msg.text,
        layer: 'attention',
        ttl: 30,
        type: 'recurring',
        tags: tagList.length > 0 ? tagList : ['自动检测'],
        auto_detected: true,
        turns: totalTurns,
        recall_count: 1,
        recall_days: [new Date().toISOString().split('T')[0]],
        created_at: new Date().toISOString().split('T')[0],
        last_active: new Date().toISOString().split('T')[0],
        source: msg.sessionId || '',
      });

      markProcessed(msg.sessionId, msg.text);
      emit(EVENTS.MEMORY_CREATED, mem);
      logEvent('auto-written', mem.id, { title, sessionId: msg.sessionId });
      created++;
    } catch (e) {
      console.warn('创建记忆失败:', e.message);
    }
  }

  // 7. 如果对话轮次多但没有记住关键词，提取摘要
  if (totalTurns > 15 && rememberMessages.length === 0) {
    const mainTopics = Array.from(topics).slice(0, 5);
    if (mainTopics.length > 0) {
      const title = `对话摘要 - ${mainTopics.slice(0, 3).join('/')}`;
      const summary = `对话 ${totalTurns} 轮，话题: ${mainTopics.join(', ')}`;

      // 去重键：基于 session files 的拼接
      const sessionKey = realMessages.map(m => m.sessionId).filter(Boolean).join(',');
      const summaryKey = `summary:${sessionKey.slice(0, 50)}`;

      if (!isProcessed('__summary__', summaryKey)) {
        try {
          const existing = await search(title, { limit: 2, threshold: 0.85, config });
          if (existing.length === 0) {
            createMemory({
              id: `session-${Date.now()}-${randomUUID().slice(0, 8)}`,
              title,
              summary,
              layer: 'flash',
              ttl: 3,
              type: 'short',
              tags: mainTopics,
              auto_detected: true,
              turns: totalTurns,
              recall_count: 0,
              recall_days: [],
              created_at: new Date().toISOString().split('T')[0],
              last_active: new Date().toISOString().split('T')[0],
            });
            created++;
          }
        } catch {}
        markProcessed('__summary__', summaryKey);
      }
    }
  }

  if (created > 0) clearIDFCache();
  return created;
}

// 提取标题
function extractTitle(content) {
  let title = content.replace(/\n/g, ' ').trim().slice(0, 50);
  if (title.length < content.length) title += '...';
  return title || '未命名记忆';
}