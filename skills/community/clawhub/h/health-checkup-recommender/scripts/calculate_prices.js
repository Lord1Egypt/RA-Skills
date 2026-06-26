const fs = require('fs');
const path = require('path');
const { checkConflicts } = require('./check_conflicts.js');

const ITEMS_JSON_PATH = path.join(__dirname, '..', 'reference', 'checkup_items.json');
let ITEMS_DB = {};

try {
  const data = JSON.parse(fs.readFileSync(ITEMS_JSON_PATH, 'utf-8'));
  ITEMS_DB = data.items || {};
} catch (e) {
  console.error('[ERROR] 无法加载 checkup_items.json:', e.message);
  process.exit(1);
}

/**
 * 获取单个项目的价格信息
 * @param {string} itemId - 项目ID（如 'HaoLa01' 或 'haola01'）
 * @returns {{ id, name, price } | null}
 */
function getPriceInfo(itemId) {
  const trimmed = itemId.trim();
  const lower = trimmed.toLowerCase();
  let key;
  if (lower.startsWith('haola')) {
    key = 'HaoLa' + lower.slice(5);
  } else {
    key = 'HaoLa' + lower;
  }

  if (ITEMS_DB[key]) {
    return {
      id: key,
      name: ITEMS_DB[key].name,
      price: ITEMS_DB[key].price
    };
  }
  return null;
}

/**
 * 计算套餐总价（自动处理冲突去重）
 * @param {string[]} itemIds - 项目ID数组
 * @returns {{ total: number, items: Array, count: number, breakdown: string }}
 */
function calculateTotal(itemIds) {
  if (!Array.isArray(itemIds) || itemIds.length === 0) {
    return { total: 0, items: [], count: 0, breakdown: '' };
  }

  // 使用 checkConflicts 进行冲突检测和去重
  const { resolved, removed, total } = checkConflicts(itemIds);

  // 获取详细信息
  const items = resolved.map(id => {
    const info = getPriceInfo(id);
    return info || { id, name: '未知', price: 0 };
  });

  // 生成详细的价格明细
  const breakdown = items.map(item =>
    `  - ${item.id} ${item.name} ¥${item.price}`
  ).join('\n');

  return {
    total,
    items,
    count: items.length,
    breakdown,
    removed: removed.map(r => ({
      id: r.id,
      name: r.name,
      reason: r.reason
    }))
  };
}

/**
 * 格式化输出（供 LLM 直接使用）
 * @param {string[]} itemIds
 * @returns {string}
 */
function formatOutput(itemIds) {
  const result = calculateTotal(itemIds);

  let output = '\n💰 【价格计算结果】\n\n';
  output += `📋 项目明细（共 ${result.count} 项）：\n`;
  output += result.breakdown + '\n\n';

  if (result.removed && result.removed.length > 0) {
    output += `⚠️ 冲突去重（已自动移除 ${result.removed.length} 项）：\n`;
    result.removed.forEach(r => {
      output += `  ❌ ${r.id} ${r.name}\n    → ${r.reason}\n`;
    });
    output += '\n';
  }

  output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  output += `💵 套餐总价：¥${result.total}\n`;
  output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  output += `✅ 验证通过，共 ${result.count} 项\n`;
  output += `（仅供参考，以医院实际收费为准）\n`;

  return output;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('\n📌 用法:');
    console.log('  node calculate_prices.js HaoLa01 HaoLa12 HaoLa57 HaoLa104');
    console.log('\n💡 演示:');
    const demo = ['HaoLa01', 'HaoLa12', 'HaoLa57', 'HaoLa104', 'HaoLa48', 'HaoLa105'];
    console.log(`  输入: ${demo.join(', ')}\n`);
    console.log(formatOutput(demo));
    process.exit(0);
    return;
  }

  console.log(formatOutput(args));
}

// 导出函数供其他模块使用
module.exports = {
  getPriceInfo,
  calculateTotal,
  formatOutput,
  ITEMS_DB
};
