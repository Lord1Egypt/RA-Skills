// repository.mjs - 数据访问层 (v2.0)
// 所有数据库操作通过此模块

import { getDb, transaction, saveDatabase } from './database.mjs';

// ============= 记忆 CRUD =============

export function createMemory(mem) {
  return transaction((db) => {
    const createdTs = new Date(mem.created_at || Date.now()).getTime();
    const lastActiveTs = new Date(mem.last_active || Date.now()).getTime();

    db.run(
      `INSERT INTO memories 
       (id, title, summary, content, layer, ttl, type, status,
        created_at, last_active, recall_count, recall_days, turns,
        remind_at, auto_detected, source, metadata, created_ts, last_active_ts)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        mem.id, mem.title, mem.summary || '', mem.content || '',
        mem.layer || 'active', mem.ttl || 7, mem.type || 'exploration',
        mem.status || 'active',
        mem.created_at || new Date().toISOString().split('T')[0],
        mem.last_active || new Date().toISOString().split('T')[0],
        mem.recall_count || 0, JSON.stringify(mem.recall_days || []),
        mem.turns || 0, mem.remind_at || null,
        mem.auto_detected ? 1 : 0, mem.source || '',
        JSON.stringify(mem.metadata || {}), createdTs, lastActiveTs
      ]
    );

    for (const tag of mem.tags || []) {
      db.run('INSERT OR IGNORE INTO memory_tags (memory_id, tag) VALUES (?, ?)', [mem.id, tag]);
    }

    db.run(
      'INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
      ['created', mem.id, JSON.stringify({ title: mem.title })]
    );

    return getMemoryById(mem.id);
  });
}

export function getMemoryById(id) {
  const db = getDb();
  const rows = db.exec(
    'SELECT * FROM memories WHERE id = ?',
    [id]
  );
  if (!rows.length || !rows[0].values.length) return null;
  return rowToMemory(rows[0]);
}

export function listMemories(options = {}) {
  const { layer, status, limit = 100, offset = 0, orderBy = 'last_active_ts', orderDir = 'DESC' } = options;
  const db = getDb();

  let where = 'WHERE status != ?';
  const params = ['archived'];

  if (layer) { where += ' AND layer = ?'; params.push(layer); }
  if (status) { where += ' AND status = ?'; params.push(status); }

  const validOrder = ['created_ts', 'last_active_ts', 'recall_count', 'layer', 'ttl'];
  const order = validOrder.includes(orderBy) ? orderBy : 'last_active_ts';
  const dir = orderDir.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';

  const countRows = db.exec(`SELECT COUNT(*) as cnt FROM memories ${where}`, params);
  const total = countRows[0].values[0][0];

  const dataRows = db.exec(
    `SELECT * FROM memories ${where} ORDER BY ${order} ${dir} LIMIT ? OFFSET ?`,
    [...params, limit, offset]
  );

  const memories = (dataRows.length ? dataRows[0].values : []).map(v => rowToMemoryFromValues(dataRows[0].columns, v));

  // 加载标签
  for (const mem of memories) {
    mem.tags = getTagsForMemory(mem.id);
  }

  return { memories, total, limit, offset };
}

export function updateMemory(id, changes) {
  return transaction((db) => {
    const allowed = ['title', 'summary', 'content', 'layer', 'ttl', 'type', 'status',
      'last_active', 'recall_count', 'recall_days', 'turns', 'remind_at',
      'auto_detected', 'source', 'metadata'];
    const sets = [];
    const params = [];

    for (const [key, val] of Object.entries(changes)) {
      if (!allowed.includes(key)) continue;
      if (key === 'last_active') {
        sets.push('last_active = ?, last_active_ts = ?');
        params.push(val, new Date(val).getTime());
      } else if (key === 'recall_days') {
        sets.push('recall_days = ?');
        params.push(JSON.stringify(val));
      } else if (key === 'metadata') {
        sets.push('metadata = ?');
        params.push(JSON.stringify(val));
      } else if (key === 'auto_detected') {
        sets.push('auto_detected = ?');
        params.push(val ? 1 : 0);
      } else {
        sets.push(`${key} = ?`);
        params.push(val);
      }
    }

    if (sets.length === 0) return getMemoryById(id);

    params.push(id);
    db.run(`UPDATE memories SET ${sets.join(', ')} WHERE id = ?`, params);

    // 更新标签
    if (changes.tags) {
      db.run('DELETE FROM memory_tags WHERE memory_id = ?', [id]);
      for (const tag of changes.tags) {
        db.run('INSERT OR IGNORE INTO memory_tags (memory_id, tag) VALUES (?, ?)', [id, tag]);
      }
    }

    db.run(
      'INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
      ['updated', id, JSON.stringify(changes)]
    );

    return getMemoryById(id);
  });
}

export function deleteMemory(id) {
  return transaction((db) => {
    const mem = getMemoryById(id);
    if (!mem) return false;
    db.run('DELETE FROM memories WHERE id = ?', [id]);
    db.run('INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
      ['deleted', id, JSON.stringify({ title: mem.title })]);
    return true;
  });
}

// ============= 标签 =============

function getTagsForMemory(id) {
  const db = getDb();
  try {
    const rows = db.exec('SELECT tag FROM memory_tags WHERE memory_id = ?', [id]);
    return rows.length ? rows[0].values.map(v => v[0]) : [];
  } catch {
    return [];
  }
}

// ============= 提醒 =============

export function getDueReminders() {
  const db = getDb();
  const now = new Date().toISOString();
  try {
    const rows = db.exec(
      "SELECT * FROM memories WHERE remind_at IS NOT NULL AND remind_at <= ? AND status = 'active'",
      [now]
    );
    return rows.length ? rows[0].values.map(v => {
      const mem = rowToMemoryFromValues(rows[0].columns, v);
      mem.tags = getTagsForMemory(mem.id);
      return mem;
    }) : [];
  } catch {
    return [];
  }
}

// ============= 统计 =============

export function getStats() {
  const db = getDb();
  try {
    const layerRows = db.exec(
      "SELECT layer, COUNT(*) as cnt, AVG(ttl) as avg_ttl FROM memories WHERE status != 'archived' GROUP BY layer"
    );
    const tagRows = db.exec(
      "SELECT tag, COUNT(*) as cnt FROM memory_tags GROUP BY tag ORDER BY cnt DESC LIMIT 20"
    );
    const expiringRows = db.exec(
      "SELECT id, title, layer, (julianday('now') - julianday(last_active)) * 30.44 as days_since, ttl, (ttl - (julianday('now') - julianday(last_active)) * 30.44) as days_left FROM memories WHERE status = 'active' AND days_left < 3 ORDER BY days_left ASC"
    );
    const dreamRows = db.exec(
      "SELECT date, action, detail FROM dream_logs ORDER BY created_at DESC LIMIT 20"
    );

    return {
      layers: layerRows.length ? layerRows[0].values.map(v => ({
        layer: v[0], count: v[1], avgTTL: v[2] ? Number(v[2].toFixed(1)) : 0
      })) : [],
      tags: tagRows.length ? tagRows[0].values.map(v => ({ tag: v[0], count: v[1] })) : [],
      expiring: expiringRows.length ? expiringRows[0].values.map(v => ({
        id: v[0], title: v[1], layer: v[2], daysLeft: Math.max(0, Math.round(v[5]))
      })) : [],
      dreamLogs: dreamRows.length ? dreamRows[0].values.map(v => ({
        date: v[0], action: v[1], detail: v[2]
      })) : [],
    };
  } catch (e) {
    return { layers: [], tags: [], expiring: [], dreamLogs: [] };
  }
}

// ============= 导入导出 =============

export function exportMemories(options = {}) {
  const { layer, type, status } = options;
  const db = getDb();
  
  let sql = 'SELECT * FROM memories';
  const params = [];
  const conditions = [];
  
  // 默认排除 archived
  if (status && status !== 'all') {
    conditions.push('status = ?');
    params.push(status);
  } else if (!status) {
    conditions.push("status != 'archived'");
  }
  if (layer) { conditions.push('layer = ?'); params.push(layer); }
  if (type) { conditions.push('type = ?'); params.push(type); }
  
  if (conditions.length) sql += ' WHERE ' + conditions.join(' AND ');
  sql += ' ORDER BY created_ts DESC';
  
  const rows = db.exec(sql, params);
  if (!rows.length) return { memories: [], count: 0 };
  
  const memories = rows[0].values.map(v => {
    const m = rowToMemoryFromValues(rows[0].columns, v);
    m.tags = getTagsForMemory(m.id);
    return m;
  });
  
  return { memories, count: memories.length };
}

export function importMemories(memories, options = {}) {
  const { mode = 'append' } = options; // append | overwrite | skip
  let imported = 0;
  let skipped = 0;
  let overwritten = 0;
  
  return transaction((db) => {
    for (const mem of memories) {
      const existing = mem.id ? (() => {
        try {
          const r = db.exec('SELECT id FROM memories WHERE id = ?', [mem.id]);
          return r.length && r[0].values.length ? true : false;
        } catch { return false; }
      })() : false;
      
      if (existing) {
        if (mode === 'skip') { skipped++; continue; }
        if (mode === 'overwrite') {
          updateMemory(mem.id, mem);
          overwritten++;
          continue;
        }
      }
      
      // append mode: create with new or existing id
      if (!mem.id) {
        mem.id = 'import-' + Date.now() + '-' + Math.random().toString(36).substr(2, 8);
      }
      
      try {
        const createdTs = new Date(mem.created_at || Date.now()).getTime();
        const lastActiveTs = new Date(mem.last_active || Date.now()).getTime();
        
        db.run(
          `INSERT OR REPLACE INTO memories 
           (id, title, summary, content, layer, ttl, type, status,
            created_at, last_active, recall_count, recall_days, turns,
            remind_at, auto_detected, source, metadata, created_ts, last_active_ts)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            mem.id, mem.title, mem.summary || '', mem.content || '',
            mem.layer || 'active', mem.ttl || 7, mem.type || 'exploration',
            mem.status || 'active',
            mem.created_at || new Date().toISOString().split('T')[0],
            mem.last_active || new Date().toISOString().split('T')[0],
            mem.recall_count || 0, JSON.stringify(mem.recall_days || []),
            mem.turns || 0, mem.remind_at || null,
            mem.auto_detected ? 1 : 0, mem.source || '',
            JSON.stringify(mem.metadata || {}), createdTs, lastActiveTs
          ]
        );
        
        const tag = getTagsForMemory(mem.id);
        db.run('DELETE FROM memory_tags WHERE memory_id = ?', [mem.id]);
        for (const t of mem.tags || []) {
          db.run('INSERT OR IGNORE INTO memory_tags (memory_id, tag) VALUES (?, ?)', [mem.id, t]);
        }
        
        db.run(
          'INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
          ['imported', mem.id, JSON.stringify({ title: mem.title, mode })]
        );
        
        imported++;
      } catch (e) {
        console.error('导入失败:', mem.id, e.message);
      }
    }
    
    return { imported, skipped, overwritten, total: memories.length };
  });
}

// ============= 事件 =============

export function logEvent(eventType, memoryId, detail = {}) {
  const db = getDb();
  db.run(
    'INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
    [eventType, memoryId, JSON.stringify(detail)]
  );
  saveDatabase();
}

export function getEvents(options = {}) {
  const { type, limit = 50 } = options;
  const db = getDb();
  let sql = 'SELECT * FROM events';
  const params = [];
  if (type) { sql += ' WHERE event_type = ?'; params.push(type); }
  sql += ' ORDER BY created_at DESC LIMIT ?';
  params.push(limit);
  const rows = db.exec(sql, params);
  return rows.length ? rows[0].values.map(v => ({
    id: v[0], eventType: v[1], memoryId: v[2],
    detail: JSON.parse(v[3] || '{}'), createdAt: v[4]
  })) : [];
}

// ============= 工具函数 =============

function rowToMemory(row) {
  if (!row.values.length) return null;
  return rowToMemoryFromValues(row.columns, row.values[0]);
}

function rowToMemoryFromValues(columns, values) {
  const obj = {};
  for (let i = 0; i < columns.length; i++) {
    const col = columns[i];
    let val = values[i];
    if (col === 'recall_days' || col === 'metadata') {
      try { val = JSON.parse(val || '[]'); } catch { val = val === '[]' ? [] : {}; }
    } else if (col === 'auto_detected') {
      val = val === 1;
    } else if (col.endsWith('_ts')) {
      val = typeof val === 'number' ? val : new Date(val).getTime();
    }
    // 蛇形命名映射
    const key = col; // 保持数据库列名
    obj[key] = val;
  }

  // 映射为常用字段名
  return {
    id: obj.id,
    title: obj.title,
    summary: obj.summary || '',
    content: obj.content || '',
    layer: obj.layer,
    ttl: obj.ttl,
    type: obj.type,
    status: obj.status,
    created_at: obj.created_at,
    last_active: obj.last_active,
    recall_count: obj.recall_count || 0,
    recall_days: obj.recall_days || [],
    turns: obj.turns || 0,
    remind_at: obj.remind_at,
    auto_detected: obj.auto_detected || false,
    source: obj.source || '',
    metadata: obj.metadata || {},
    embedding_id: obj.embedding_id,
    created_ts: obj.created_ts,
    last_active_ts: obj.last_active_ts,
  };
}
