#!/usr/bin/env node
/**
 * 体检项目核查脚本（v2.0）
 *
 * 三重保障：
 * 1. ItemID 有效性验证（模糊匹配中文名/旧编码）
 * 2. 冲突检测（同类父子项去重）→ 来自 check_conflicts.js
 * 3. 核查+去重后的套餐总价
 *
 * 用法:
 *   node verify_items.js HaoLa01 HaoLa105 HaoLa48 HaoLa47
 */
const { checkConflicts } = require('./check_conflicts.js');

const fs = require('fs');
const path = require('path');
const ITEMS_JSON_PATH = path.join(__dirname, '..', 'reference', 'checkup_items.json');

let ITEMS_DB = {};
let NAME_TO_ID = {};

try {
  const data = JSON.parse(fs.readFileSync(ITEMS_JSON_PATH, 'utf-8'));
  ITEMS_DB = data.items || {};
  for (const [id, info] of Object.entries(ITEMS_DB)) {
    const key = info.name.replace(/\s+/g, ' ').trim().toLowerCase();
    NAME_TO_ID[key] = id;
  }
} catch (e) {
  console.error('[ERROR] 无法加载 checkup_items.json:', e.message);
  process.exit(1);
}

// ============================================================
// 第一步：ItemID 有效性验证
// ============================================================
function verifyOne(item) {
  const norm = item.trim();
  if (norm in ITEMS_DB)
    return { id: norm, name: ITEMS_DB[norm].name, price: ITEMS_DB[norm].price, status: '✅', from: 'ItemID' };
  const lowerId = 'HaoLa' + norm.replace(/^HaoLa/i, '');
  if (lowerId in ITEMS_DB)
    return { id: lowerId, name: ITEMS_DB[lowerId].name, price: ITEMS_DB[lowerId].price, status: '✅', from: 'ItemID' };
  const normLower = norm.toLowerCase();
  for (const [key, id] of Object.entries(NAME_TO_ID)) {
    if (key.includes(normLower) || normLower.includes(key))
      return { id, name: ITEMS_DB[id].name, price: ITEMS_DB[id].price, status: '✅', from: '中文名匹配' };
  }
  if (norm.startsWith('HLZXX') && Object.values(OLD_CODE_MAP).includes(norm)) {
    const name = Object.entries(OLD_CODE_MAP).find(([, v]) => v === norm)?.[0];
    const id = Object.entries(ITEMS_DB).find(([, v]) => v.name.toLowerCase() === name)?.[0];
    if (id) return { id, name: ITEMS_DB[id].name, price: ITEMS_DB[id].price, status: '✅', from: '旧编码' };
  }
  return { id: norm, status: '❌', hint: '未找到对应项目，请检查 ID 或中文名称' };
}

function verifyAll(rawItems) {
  const results = [], errors = [];
  for (const item of rawItems) {
    const r = verifyOne(item);
    (r.status === '✅' ? results : errors).push(r);
  }
  return { results, errors };
}

// ============================================================
// CLI
// ============================================================
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: node verify_items.js HaoLa01 HaoLa105 HaoLa48 HaoLa47');
    console.log('');
    console.log('--- 演示 ---');
    const demo = ['HaoLa01', 'HaoLa12', 'HaoLa57', 'HaoLa104', 'HaoLa48', 'HaoLa105', 'HaoLa77', 'HaoLa51', 'HaoLa66', 'HaoLa100'];
    console.log('输入:', demo.join(', '));
    const { results, errors } = verifyAll(demo);
    const { resolved, removed, total } = checkConflicts(results.map(r => r.id));

    console.log('\n━━━ 有效性核查 ━━━');
    results.forEach(r => console.log(`${r.status} ${r.id}  ${r.name}  ¥${r.price}`));
    errors.forEach(e => console.log(`${e.status} ${e.id}  → ${e.hint}`));

    if (removed.length) {
      console.log('\n━━━ 冲突检测（同类父子项，已自动移除）━━━');
      removed.forEach(r => console.log(`  ❌ ${r.id} ${r.name} → ${r.reason}`));
    }

    console.log(`\n✅ 有效: ${results.length}  ❌ 无效: ${errors.length}  🔸 冲突移除: ${removed.length}`);
    console.log(`💰 去重后 ${resolved.length} 项总价: ¥${total}`);
    console.log('\n去重后项目:', resolved.join(', '));
    process.exit(errors.length > 0 ? 1 : 0);
    return;
  }

  const { results, errors } = verifyAll(args);
  console.log('\n🔍 体检项目核查结果\n');

  if (results.length) {
    console.log('━━━ 有效项目 ━━━');
    results.forEach(r => console.log(`${r.status} ${r.id}  ${r.name}  ¥${r.price}  [${r.from}]`));
  }
  if (errors.length) {
    console.log('\n━━━ 无效项目 ━━━');
    errors.forEach(e => console.log(`${e.status} ${e.id}  → ${e.hint}`));
  }

  const { resolved, removed, total } = checkConflicts(results.map(r => r.id));

  if (removed.length) {
    console.log('\n━━━ 冲突检测（同类父子项，已自动移除）━━━');
    removed.forEach(r => console.log(`  ❌ ${r.id} ${r.name} → ${r.reason}`));
  }

  console.log(`\n✅ 有效: ${results.length}  ❌ 无效: ${errors.length}  🔸 冲突移除: ${removed.length}`);
  if (results.length) console.log(`💰 去重后 ${resolved.length} 项总价: ¥${total}（仅供参考，以医院实际收费为准）`);

  if (errors.length > 0) {
    console.log('\n⚠️ 有无效项目，请修正后重新核查');
    process.exit(1);
  }
  if (removed.length > 0) {
    console.log('\n去重后项目:', resolved.join(', '));
    process.exit(1);
  }
  process.exit(0);
}

module.exports = { verifyOne, verifyAll, checkConflicts, ITEMS_DB };
