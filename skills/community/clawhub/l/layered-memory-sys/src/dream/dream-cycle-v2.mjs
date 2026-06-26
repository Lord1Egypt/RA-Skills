// dream-cycle-v2.mjs - 梦境模式 v2.0（SQLite 版）
// 支持：巩固/归档/遗忘/合并 + 时间衰减召回 + 来源追溯 + 自动写入检测

import { getDb, saveDatabase, transaction } from '../db/database.mjs';
import { 
  listMemories, updateMemory, getStats, logEvent, getMemoryById 
} from '../db/repository.mjs';
import { search, getEmbedding, storeEmbedding } from '../search/search-engine.mjs';

const LAYERS = ['flash', 'active', 'attention', 'settled'];
const LAYER_TTL = { flash: 3, active: 7, attention: 30, settled: 90 };

// 时间衰减权重
function timeDecayWeight(daysAgo) {
  // 指数衰减：半衰期约7天
  return Math.exp(-0.1 * daysAgo);
}

// 有效召回分数（考虑时间衰减）
function effectiveRecallScore(memory) {
  if (!memory.recall_days || memory.recall_days.length === 0) return 0;

  let score = 0;
  const now = Date.now();
  for (const day of memory.recall_days) {
    const daysAgo = (now - new Date(day).getTime()) / (1000 * 60 * 60 * 24);
    score += timeDecayWeight(daysAgo);
  }
  return score;
}

// 验证支持的真实记忆关键词
const REMEMBER_KEYWORDS = [
  '记住', '记住这个', '别忘了', '不要忘', '记下来',
  '要记得', '帮我记', '帮我记一下', '记录下来',
  '这件事很重要', '记住了', '一定要记住'
];

// 心跳/系统消息关键词（过滤）
const SYSTEM_PATTERNS = [
  'Read HEARTBEAT.md', 'HEARTBEAT_OK', 'HEARTBEAT_',
  'Conversation info (untrusted metadata)',
  'System (untrusted)', 'Queued messages',
  'Exec completed', 'Process exited'
];

// ============= 主流程 =============

export default async function dreamCycle(config) {
  console.log('💤 梦境模式 v2.0 开始...\n');

  const stats = {
    consolidated: 0,
    archived: 0,
    forgotten: 0,
    merged: 0,
    autoWritten: 0
  };

  // 1. 自动写入检测
  const autoResult = await autoDetectMemories(config);
  stats.autoWritten = autoResult;

  // 2. 巩固检查（时间衰减版本）
  stats.consolidated = await consolidateMemories();

  // 3. 归档检查
  stats.archived = await archiveMemories();

  // 4. 合并检查（含来源追溯）
  stats.merged = await mergeMemories();

  // 5. 刷新即将过期记忆的 embedding
  await refreshExpiringEmbeddings();

  // 6. 记录梦境日志
  logDreamCycle(stats);

  console.log(`\n💤 梦境结束：巩固${stats.consolidated} / 归档${stats.archived} / 合并${stats.merged} / 自动写入${stats.autoWritten}`);

  return stats;
}

// ============= 子流程 =============

// 自动写入检测
async function autoDetectMemories(config) {
  try {
    const fs = await import('fs');
    const path = await import('path');
    const sessionsPath = config.sessionDir || '/root/.openclaw/agents/main/sessions';

    if (!fs.existsSync(sessionsPath)) return 0;

    const files = fs.readdirSync(sessionsPath).filter(f => f.endsWith('.jsonl'));
    if (files.length === 0) return 0;

    let count = 0;
    for (const file of files.slice(-3)) { // 只看最近3个session
      const filePath = path.join(sessionsPath, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.split('\n').filter(l => l.trim());

      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          if (entry.role !== 'user') continue;
          const msg = entry.content || '';

          // 过滤系统消息
          if (SYSTEM_PATTERNS.some(p => msg.includes(p))) continue;
          if (msg.length < 10) continue;

          // 检查是否包含"记住"关键词
          if (REMEMBER_KEYWORDS.some(kw => msg.includes(kw))) {
            await createMemoryFromMessage(msg, config);
            count++;
          }
        } catch {}
      }
    }
    return count;
  } catch {
    return 0;
  }
}

async function createMemoryFromMessage(msg, config) {
  const id = `auto-${Date.now()}`;
  const title = msg.substring(0, 50);
  const db = getDb();
  db.run(
    `INSERT INTO memories (id, title, summary, layer, ttl, type, status, 
       created_at, last_active, auto_detected)
     VALUES (?, ?, ?, 'active', 7, 'exploration', 'active', ?, ?, 1)`,
    [id, title, msg.substring(0, 200), 
     new Date().toISOString().split('T')[0],
     new Date().toISOString()]
  );
  saveDatabase();
  logEvent('auto_written', id, { title });
}

// 巩固检查（时间衰减版）
async function consolidateMemories() {
  const db = getDb();
  const rows = db.exec("SELECT * FROM memories WHERE status = 'active'");
  if (!rows.length) return 0;

  let count = 0;
  const memories = rows[0].values.map(v => parseMemoryFromRow(rows[0].columns, v));

  for (const mem of memories) {
    const layerIdx = LAYERS.indexOf(mem.layer);
    if (layerIdx >= LAYERS.length - 1) continue; // 已是最高层

    const score = effectiveRecallScore(mem);
    const recallDays = mem.recall_days.length;

    let upgraded = false;

    // 时间衰减阈值
    if (layerIdx === 0 && score >= 2.5 && recallDays >= 2) {
      upgradeLayer(mem.id, 'active');
      upgraded = true;
    } else if (layerIdx === 1 && score >= 5.0 && recallDays >= 3) {
      upgradeLayer(mem.id, 'attention');
      upgraded = true;
    } else if (layerIdx === 2 && score >= 10.0 && recallDays >= 7) {
      upgradeLayer(mem.id, 'settled');
      upgraded = true;
    }

    if (upgraded) {
      logEvent('consolidated', mem.id, {
        from: mem.layer,
        score: score.toFixed(2),
        recallDays
      });
      count++;
    }
  }
  return count;
}

function upgradeLayer(id, newLayer) {
  const db = getDb();
  const newTTL = LAYER_TTL[newLayer];
  db.run(
    "UPDATE memories SET layer = ?, ttl = ? WHERE id = ?",
    [newLayer, newTTL, id]
  );
  saveDatabase();
}

// 归档检查
async function archiveMemories() {
  const db = getDb();
  const rows = db.exec("SELECT * FROM memories WHERE status = 'active'");
  if (!rows.length) return 0;

  let count = 0;
  const now = Date.now();
  const memories = rows[0].values.map(v => parseMemoryFromRow(rows[0].columns, v));

  for (const mem of memories) {
    const daysSince = (now - (mem.last_active_ts || now)) / (1000 * 60 * 60 * 24);
    if (daysSince > mem.ttl && mem.layer !== 'flash') {
      continue; // 暂不归档，先观察
    }
    if (daysSince > mem.ttl * 1.5) {
      // 超过 TTL 1.5 倍，归档
      db.run(
        "UPDATE memories SET status = 'archived' WHERE id = ?",
        [mem.id]
      );
      logEvent('archived', mem.id, { daysSince: Math.round(daysSince) });
      count++;
    }
  }
  saveDatabase();
  return count;
}

// 合并检查（含来源追溯）
async function mergeMemories() {
  const db = getDb();
  const rows = db.exec(
    `SELECT m1.id as id1, m2.id as id2, m1.title as t1, m2.title as t2,
       m1.layer as l1, m2.layer as l2, m1.recall_count as c1, m2.recall_count as c2,
       m1.recall_days as d1, m2.recall_days as d2, m1.summary as s1, m2.summary as s2
     FROM memories m1 JOIN memories m2 ON m1.id < m2.id
     WHERE m1.status = 'active' AND m2.status = 'active'
       AND m1.layer = m2.layer
       AND m1.remind_at IS NULL AND m2.remind_at IS NULL
   `
  );

  if (!rows.length) return 0;

  let count = 0;
  const pairs = rows[0].values;

  for (const pair of pairs) {
    const v = {
      id1: pair[0], id2: pair[1], t1: pair[2], t2: pair[3],
      l1: pair[4], l2: pair[5], c1: pair[6], c2: pair[7],
      d1: pair[8], d2: pair[9], s1: pair[10], s2: pair[11]
    };

    // 跳过有提醒的记忆
    if (v.id1.includes('remind') || v.id2.includes('remind')) continue;

    // 标签重叠检查
    const tags1 = getTags(v.id1);
    const tags2 = getTags(v.id2);
    const tagOverlap = tags1.filter(t => tags2.includes(t)).length;

    if (tagOverlap >= 3) {
      // 合并（保留召回更多的）
      const primary = v.c1 >= v.c2 ? v : { ...v, id1: v.id2, id2: v.id1, t1: v.t2, t2: v.t1 };

      const newTitle = primary.t1.length >= primary.t2.length ? primary.t1 : primary.t2;
      const newSummary = `${v.s1 || ''} | ${v.s2 || ''}`.substring(0, 500);
      const newRecallDays = JSON.stringify([...new Set([
        ...JSON.parse(v.d1 || '[]'), ...JSON.parse(v.d2 || '[]')
      ])].sort().slice(-10));
      const newRecallCount = v.c1 + v.c2;
      const source = JSON.stringify({
        primary: primary.id1,
        merged: [{ id: v.id2, title: v.t2, mergedAt: new Date().toISOString() }],
        mergedCount: 1
      });

      db.run(
        `UPDATE memories SET title = ?, summary = ?, recall_count = ?, 
          recall_days = ?, source = ? 
         WHERE id = ?`,
        [newTitle, newSummary, newRecallCount, newRecallDays, source, primary.id1]
      );
      db.run("UPDATE memories SET status = 'archived' WHERE id = ?", [primary.id2]);

      logEvent('merged', primary.id1, { merged: primary.id2 });
      count++;
    }
  }

  saveDatabase();
  return count;
}

function getTags(id) {
  const db = getDb();
  try {
    const rows = db.exec('SELECT tag FROM memory_tags WHERE memory_id = ?', [id]);
    return rows.length ? rows[0].values.map(v => v[0]) : [];
  } catch {
    return [];
  }
}

// 刷新即将过期记忆的 embedding
async function refreshExpiringEmbeddings() {
  const stats = getStats();
  for (const mem of stats.expiring.slice(0, 10)) {
    const memory = getMemoryById(mem.id);
    if (memory) {
      const text = `${memory.title} ${memory.summary}`;
      const vector = await getEmbedding(text);
      if (vector) {
        await storeEmbedding(memory.id, vector);
      }
    }
  }
}

// 记录梦境日志
function logDreamCycle(stats) {
  const db = getDb();
  const date = new Date().toISOString().split('T')[0];
  for (const [action, count] of Object.entries(stats)) {
    db.run(
      'INSERT INTO dream_logs (date, action, detail) VALUES (?, ?, ?)',
      [date, action, JSON.stringify({ count })]
    );
  }
  saveDatabase();
}

// 工具函数
function parseMemoryFromRow(columns, values) {
  const obj = {};
  for (let i = 0; i < columns.length; i++) {
    let val = values[i];
    const col = columns[i];
    if (col === 'recall_days') {
      try { val = JSON.parse(val || '[]'); } catch { val = []; }
    } else if (col === 'auto_detected') {
      val = val === 1;
    } else if (col.endsWith('_ts')) {
      val = typeof val === 'number' ? val : new Date(val).getTime();
    }
    obj[col] = val;
  }
  return obj;
}
