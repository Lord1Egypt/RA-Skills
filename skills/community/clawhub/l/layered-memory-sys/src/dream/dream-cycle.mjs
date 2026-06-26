// dream-cycle.mjs - 梦境模式主逻辑 (v2.0)

import { consolidate } from './consolidator.mjs';
import { runMergeChecks } from './merger.mjs';
import { getDb, saveDatabase } from '../db/database.mjs';
import { logEvent } from '../db/repository.mjs';
import { autoDetectMemories } from './auto-writer.mjs';
import { indexAllMemories } from '../search/search-engine.mjs';

export async function execDreamCycle(config) {
  const date = new Date().toISOString().split('T')[0];
  console.log(`💤 梦境模式 v2.0 开始... (${date})`);

  const stats = { consolidate: 0, archive: 0, forget: 0, merge: 0, autowrite: 0 };

  // 1. 自动写入检测
  try {
    const detected = await autoDetectMemories(config);
    stats.autowrite = detected;
    console.log(`✏️ 自动写入检测: ${detected} 条新记忆`);
  } catch (e) {
    console.warn('自动写入检测失败:', e.message);
  }

  // 2. 巩固检查
  try {
    const upgrades = consolidate(config);
    stats.consolidate = upgrades.length;
    for (const u of upgrades) {
      console.log(`🧠 巩固: ${u.title} (${u.from} → ${u.to})`);
      logDreamLog(date, 'consolidate', `${u.title}: ${u.from} → ${u.to}`, u.id);
    }
  } catch (e) {
    console.warn('巩固检查失败:', e.message);
  }

  // 3. 归档/遗忘检查
  try {
    const { archived, forgotten } = archiveAndForget(config);
    stats.archive = archived;
    stats.forget = forgotten;
  } catch (e) {
    console.warn('归档/遗忘检查失败:', e.message);
  }

  // 4. 合并检查
  try {
    const merges = await runMergeChecks(config);
    stats.merge = merges.length;
    for (const m of merges) {
      console.log(`🔗 合并: ${m.mergedTitle} → ${m.title}`);
      logDreamLog(date, 'merge', `${m.mergedTitle} → ${m.title}`, m.id);
    }
  } catch (e) {
    console.warn('合并检查失败:', e.message);
  }

  // 5. 重新索引（如有变更）
  if (stats.consolidate + stats.archive + stats.merge > 0) {
    try {
      await indexAllMemories(config);
    } catch (e) {
      console.warn('重新索引失败:', e.message);
    }
  }

  console.log(`✨ 梦境模式完成`);
  console.log(`💤 统计: 巩固${stats.consolidate}条 归档${stats.archive}条 遗忘${stats.forget}条 合并${stats.merge}条 自动写入${stats.autowrite}条`);

  return stats;
}

// 归档和遗忘
function archiveAndForget(config) {
  const db = getDb();
  const now = new Date();
  const rows = db.exec(
    "SELECT id, title, layer, ttl, last_active_ts FROM memories WHERE status = 'active'"
  );

  if (!rows.length) return { archived: 0, forgotten: 0 };

  let archived = 0, forgotten = 0;

  for (const row of rows[0].values) {
    const [id, title, layer, , lastActiveTs] = row;
    const lastActive = new Date(lastActiveTs);
    const daysSince = (now - lastActive) / (1000 * 60 * 60 * 24);

    let ttl;
    try { ttl = db.exec("SELECT ttl FROM memories WHERE id = ?", [id])[0].values[0][0]; } catch { continue; }

    if (daysSince > ttl) {
      if (layer === 'flash') {
        // 闪存层直接遗忘
        db.run('DELETE FROM memory_tags WHERE memory_id = ?', [id]);
        db.run('DELETE FROM memories WHERE id = ?', [id]);
        logEvent('forgotten', id, { title, daysSince: Math.round(daysSince) });
        forgotten++;
      } else {
        // 其他层归档
        db.run("UPDATE memories SET status = 'archived' WHERE id = ?", [id]);
        logEvent('archived', id, { title, layer, daysSince: Math.round(daysSince) });
        logDreamLog(now.toISOString().split('T')[0], 'archive', `${title} (${layer}, ${Math.round(daysSince)}天)`, id);
        archived++;
      }
    }
  }

  if (archived + forgotten > 0) saveDatabase();
  return { archived, forgotten };
}

// 记录梦境日志
function logDreamLog(date, action, detail, memoryId = '') {
  const db = getDb();
  try {
    db.run(
      'INSERT INTO dream_logs (date, action, detail, memory_id) VALUES (?, ?, ?, ?)',
      [date, action, detail, memoryId]
    );
    saveDatabase();
  } catch {}
}