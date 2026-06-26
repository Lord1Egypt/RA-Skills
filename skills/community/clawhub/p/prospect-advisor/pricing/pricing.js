/**
 * 惠迈裂变定价引擎 — 高考志愿填报
 * 
 * 核心逻辑：差价 = 推广者利润空间 = 裂变动力
 */

const TIERS = [
  { key: 'free',     count: 0,   price: 0,     unitPrice: 0,     label: '免费版',   hidden: false },
  { key: 'single',   count: 1,   price: 1999,  unitPrice: 1999,  label: '单人次',   hidden: false },
  { key: 'tier20',   count: 20,  price: 30000, unitPrice: 1500,  label: '20人次',   hidden: true  },
  { key: 'tier50',   count: 50,  price: 50000, unitPrice: 1000,  label: '50人次',   hidden: true  },
  { key: 'tier100',  count: 100, price: 88880, unitPrice: 888,   label: '100人次',  hidden: true  },
];

const FREE_LIMIT = 3; // 免费版可查学校数量

/**
 * 获取定价信息
 */
function getPricing(userRole = 'user') {
  if (userRole === 'user') {
    // 普通用户只看到免费版和单人次
    return TIERS.filter(t => !t.hidden || t.key === 'free' || t.key === 'single');
  }
  // 推广者看到全部
  return TIERS.filter(t => t.key !== 'free');
}

/**
 * 计算推广者利润率
 */
function getProfitAnalysis() {
  const publicPrice = 1999;
  return TIERS.filter(t => t.count > 1).map(tier => ({
    tier: tier.label,
    invest: tier.price,
    unitCost: tier.unitPrice,
    resellPrice: publicPrice,
    perUnitProfit: publicPrice - tier.unitPrice,
    totalProfit: (publicPrice - tier.unitPrice) * tier.count,
    profitRate: (((publicPrice - tier.unitPrice) / tier.unitPrice) * 100).toFixed(0) + '%'
  }));
}

/**
 * 计算套餐价格（含验证）
 */
function calculatePrice(tierKey, quantity = 1) {
  const tier = TIERS.find(t => t.key === tierKey);
  if (!tier) return { valid: false, error: '未知套餐' };
  if (tier.key === 'free') return { valid: true, total: 0, unit: 0, remainingQuantity: FREE_LIMIT };
  return {
    valid: true,
    total: tier.price,
    unit: tier.unitPrice,
    count: tier.count,
    remaining: tier.count
  };
}

/**
 * 验证推广者利润模型
 * 确保裂变逻辑自洽
 */
function verifyPricingModel() {
  const analysis = getProfitAnalysis();
  const issues = [];
  
  for (const item of analysis) {
    if (item.perUnitProfit <= 0) {
      issues.push(`警告: ${item.tier} 推广者无利润空间`);
    }
    if (item.perUnitProfit > item.resellPrice) {
      issues.push(`警告: ${item.tier} 推广者利润高于零售价，存在套利风险`);
    }
  }
  
  return {
    valid: issues.length === 0,
    tiers: analysis,
    issues,
    summary: issues.length === 0 ? '✅ 定价模型自洽，裂变逻辑畅通' : issues.join('; ')
  };
}

module.exports = {
  TIERS, FREE_LIMIT,
  getPricing,
  getProfitAnalysis,
  calculatePrice,
  verifyPricingModel
};
