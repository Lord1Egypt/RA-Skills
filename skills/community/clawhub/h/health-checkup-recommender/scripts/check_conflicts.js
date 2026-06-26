/**
 * check_conflicts.js - 体检项目冲突检测脚本
 * 父子项去重：选择父项时自动移除其子项
 *
 * 冲突链（HaoLaXX 格式）：
 *   HaoLa01(一般检查) - 基础必选项
 *   HaoLa66(甲功5项) > HaoLa65(甲功3项B) > HaoLa64(甲功3项)
 *   HaoLa57(血脂4项) > HaoLa122(血脂2项)
 *   HaoLa67(甲功7项) > HaoLa66/65/64(甲功系列)
 *
 * 注意：HaoLa48(胃泌素G-17) 和 HaoLa47(胃蛋白酶原测定) 是不同检测指标，无包含关系
 */

const fs = require('fs');
const path = require('path');

const ITEMS_JSON_PATH = path.join(__dirname, '..', 'reference', 'checkup_items.json');
let ITEMS_DB = {};
try {
  ITEMS_DB = JSON.parse(fs.readFileSync(ITEMS_JSON_PATH, 'utf-8')).items || {};
} catch(e) {
  console.error('[ERROR] Cannot load items:', e.message);
  process.exit(1);
}

const CONFLICT_MAP = {
  'HaoLa66': ['HaoLa65', 'HaoLa64'],
  'HaoLa57': ['HaoLa122'],
  'HaoLa67': ['HaoLa66', 'HaoLa65', 'HaoLa64'],
  'HaoLa84': ['HaoLa83', 'HaoLa82', 'HaoLa81', 'HaoLa80', 'HaoLa79', 'HaoLa78', 'HaoLa77', 'HaoLa71', 'HaoLa74', 'HaoLa72', 'HaoLa73', 'HaoLa75'],
  'HaoLa83': ['HaoLa82', 'HaoLa81', 'HaoLa80', 'HaoLa79', 'HaoLa78', 'HaoLa77', 'HaoLa71', 'HaoLa74', 'HaoLa72', 'HaoLa73', 'HaoLa75'],
  'HaoLa82': ['HaoLa80', 'HaoLa79', 'HaoLa78', 'HaoLa77', 'HaoLa71', 'HaoLa74', 'HaoLa76', 'HaoLa77'],
  'HaoLa81': ['HaoLa80', 'HaoLa79', 'HaoLa78', 'HaoLa77', 'HaoLa71', 'HaoLa74', 'HaoLa72', 'HaoLa73'],
  'HaoLa80': ['HaoLa79', 'HaoLa78', 'HaoLa77', 'HaoLa71', 'HaoLa74', 'HaoLa72', 'HaoLa73'],
  'HaoLa79': ['HaoLa71', 'HaoLa74', 'HaoLa76'],
  'HaoLa78': ['HaoLa71', 'HaoLa74'],
  'HaoLa56': ['HaoLa55', 'HaoLa54', 'HaoLa53', 'HaoLa52', 'HaoLa51', 'HaoLa50', 'HaoLa49', 'HaoLa48', 'HaoLa47'],
  'HaoLa55': ['HaoLa54', 'HaoLa53', 'HaoLa52', 'HaoLa51', 'HaoLa50', 'HaoLa49', 'HaoLa48', 'HaoLa47'],
  'HaoLa54': ['HaoLa53', 'HaoLa52', 'HaoLa51', 'HaoLa50', 'HaoLa49', 'HaoLa48', 'HaoLa47'],
  'HaoLa53': ['HaoLa51', 'HaoLa50', 'HaoLa49', 'HaoLa48', 'HaoLa47'],
};

function normalizeId(id) {
  const trimmed = id.trim();
  const lower = trimmed.toLowerCase();
  if (lower.startsWith('haola')) {
    return 'HaoLa' + lower.slice(5);
  }
  return 'HaoLa' + lower;
}

function checkConflicts(itemIds) {
  const unique = [...new Set(itemIds.map(normalizeId))];
  const toRemove = new Set();
  const removed = [];

  for (const id of unique) {
    if (toRemove.has(id)) continue;
    const subsets = CONFLICT_MAP[id.charAt(0).toUpperCase() + id.slice(1)];
    if (!subsets) continue;

    for (const subId of subsets) {
      const subIdLower = normalizeId(subId);
      if (unique.includes(subIdLower) && !toRemove.has(subIdLower)) {
        toRemove.add(subIdLower);
        const parentName = ITEMS_DB[id.charAt(0).toUpperCase() + id.slice(1)]?.name || id;
        const childName = ITEMS_DB[subId]?.name || subId;
        removed.push({
          id: subIdLower,
          name: childName,
          reason: `已被 ${id} ${parentName} 包含`,
          supersededBy: id,
        });
      }
    }
  }

  const resolved = unique.filter(id => !toRemove.has(id));
  const total = Math.round(resolved.reduce((s, id) => {
    const dbKey = id.charAt(0).toUpperCase() + id.slice(1);
    return s + (ITEMS_DB[dbKey]?.price || 0);
  }, 0) * 100) / 100;

  return { resolved, removed, total };
}

if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: node check_conflicts.js HaoLa01 HaoLa48 HaoLa47 HaoLa66 HaoLa65 HaoLa64');
    console.log('');
    const demo = ['HaoLa01', 'HaoLa48', 'HaoLa47', 'HaoLa66', 'HaoLa65', 'HaoLa64', 'HaoLa57', 'HaoLa122'];
    console.log('演示:', demo.join(', '));
    const r = checkConflicts(demo);
    if (r.removed.length) {
      r.removed.forEach(x => console.log(`  ❌ ${x.id} ${x.name} → ${x.reason}`));
    }
    console.log(`\n✅ 去重后: ${r.resolved.join(', ')}  共${r.resolved.length}项 ¥${r.total}`);
    process.exit(r.removed.length > 0 ? 1 : 0);
    return;
  }

  const r = checkConflicts(args);
  if (r.removed.length) {
    r.removed.forEach(x => console.log(`❌ ${x.id} ${x.name} → ${x.reason}`));
    console.log(`\n去重后: ${r.resolved.join(', ')}  共${r.resolved.length}项 ¥${r.total}`);
    process.exit(1);
  }
  console.log(`✅ 无冲突  共${r.resolved.length}项 ¥${r.total}`);
  process.exit(0);
}

module.exports = { checkConflicts, CONFLICT_MAP };
