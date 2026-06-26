// consolidator.mjs - 巩固逻辑 (v2.0)
// 时间衰减召回 + 自适应升级阈值

import { getDb, saveDatabase } from '../db/database.mjs';
import { logEvent } from '../db/repository.mjs';
import { cosineSimilarity, embedText } from '../search/embedder.mjs';
import { clearIDFCache } from '../search/tokenizer.mjs';

// 有效召回分（时间衰减）
export function effectiveRecallCount(recallDays) {
  const now = Date.now();
  let score = 0;

  for (const day of recallDays) {
    const ts = typeof day === 'string' ? new Date(day).getTime() : day;
    const daysSince = (now - ts) / (1000 * 60 * 60 * 24);
    // 指数衰减：半衰期约7天
    const decay = Math.exp(-0.1 * daysSince);
    score += decay;
  }

  return score;
}

// 升级阈值（自适应）
function getUpgradeThreshold(fromLayer, avgDailyRecalls) {
  // 基础阈值
  const base = {
    'flash': 2.5,
    'active': 5.0,
    'attention': 10.0,
  };

  // 根据使用频率调整：用户越活跃，阈值越高
  const usageFactor = Math.max(0.5, Math.min(2.0, avgDailyRecalls / 5));
  return (base[fromLayer] || 5.0) * usageFactor;
}

// 执行巩固检查
export function consolidate(config) {
  const db = getDb();
  const rows = db.exec(
    "SELECT * FROM memories WHERE status = 'active'"
  );

  if (!rows.length || !rows[0].values.length) return [];

  const upgrades = [];

  // 获取所有活跃记忆的 recallDays 计算平均召回频率
  const allRecallDays = [];
  for (const row of rows[0].values) {
    try {
      const days = JSON.parse(row[7] || '[]'); // recall_days
      allRecallDays.push(...days);
    } catch {}
  }

  // 平均每日召回数（粗估）
  const daysSet = new Set(allRecallDays.map(d => String(d).split('T')[0]));
  const avgDaily = allRecallDays.length / Math.max(1, daysSet.size);

  for (const row of rows[0].values) {
    const [id, title, , , layer, ttl, , , , , recallCount, recallDaysJson] = row;

    let recallDays;
    try { recallDays = JSON.parse(recallDaysJson || '[]'); } catch { recallDays = []; }

    if (recallDays.length === 0) continue;

    const effectiveScore = effectiveRecallCount(recallDays);
    const threshold = getUpgradeThreshold(layer, avgDaily);

    let newLayer = null;

    // flash → active
    if (layer === 'flash' && effectiveScore >= getUpgradeThreshold('flash', avgDaily)) {
      newLayer = 'active';
    }
    // active → attention
    else if (layer === 'active' && effectiveScore >= getUpgradeThreshold('active', avgDaily)
      && new Set(recallDays.map(d => String(d).split('T')[0])).size >= 3) {
      newLayer = 'attention';
    }
    // attention → settled
    else if (layer === 'attention' && effectiveScore >= getUpgradeThreshold('attention', avgDaily)
      && new Set(recallDays.map(d => String(d).split('T')[0])).size >= 7) {
      newLayer = 'settled';
    }

    if (newLayer) {
      const newTtl = { flash: 3, active: 7, attention: 30, settled: 90 }[newLayer];
      db.run(
        "UPDATE memories SET layer = ?, ttl = ? WHERE id = ?",
        [newLayer, newTtl, id]
      );

      logEvent('consolidated', id, {
        from: layer, to: newLayer,
        effectiveScore: Number(effectiveScore.toFixed(2)),
        threshold: Number(threshold.toFixed(2)),
        recallDays: recallDays.length
      });

      upgrades.push({ id, title, from: layer, to: newLayer });
    }
  }

  if (upgrades.length > 0) saveDatabase();
  return upgrades;
}