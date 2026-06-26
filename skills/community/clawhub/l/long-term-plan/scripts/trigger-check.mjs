#!/usr/bin/env node
/**
 * 长期计划 - 条件触发检查模块
 * 
 * 心跳时调用，检查所有计划的条件触发器是否满足
 */

/**
 * 基金实时估值API（天天基金）
 */
const FUND_API = code => `https://fundgz.1234567.com.cn/js/${code}.js`;

/**
 * 检查条件触发器
 * @param {Object} trigger - 条件触发器配置
 * @param {Object} context - 上下文（持仓信息、基准净值等）
 * @returns {{ triggered: boolean, message?: string }}
 */
export async function checkConditionalTrigger(trigger, context = {}) {
  try {
    // 基金涨超X%
    if (trigger.condition === 'gain' && trigger.fund.length === 6) {
      const nav = await fetchFundNav(trigger.fund);
      if (!nav) return { triggered: false };
      
      const gainPercent = ((nav.gsz - nav.dwjz) / nav.dwjz * 100);
      const totalGain = ((nav.gsz - context.baselineNav?.[trigger.fund] || nav.dwjz) 
                          / (context.baselineNav?.[trigger.fund] || nav.dwjz) * 100);
      
      if (totalGain >= trigger.value) {
        return {
          triggered: true,
          message: `📈 ${trigger.fund} 累计涨幅已达 ${totalGain.toFixed(1)}%（超过${trigger.value}%阈值），建议${trigger.action}`
        };
      }
    }
    
    // 基金跌超X%
    if (trigger.condition === 'loss' && trigger.fund.length === 6) {
      const nav = await fetchFundNav(trigger.fund);
      if (!nav) return { triggered: false };
      
      const totalLoss = ((nav.gsz - (context.baselineNav?.[trigger.fund] || nav.dwjz)) 
                          / (context.baselineNav?.[trigger.fund] || nav.dwjz) * 100);
      
      if (totalLoss <= -trigger.value) {
        return {
          triggered: true,
          message: `📉 ${trigger.fund} 累计跌幅已达 ${totalLoss.toFixed(1)}%（超过-${trigger.value}%阈值），建议${trigger.action}`
        };
      }
    }
    
    // 整体账户回撤超X%
    if (trigger.condition === 'drawdown') {
      const peakAsset = context.peakAsset || 0;
      const currentAsset = context.currentAsset || 0;
      
      if (peakAsset > 0) {
        const drawdown = (peakAsset - currentAsset) / peakAsset * 100;
        if (drawdown >= trigger.value) {
          return {
            triggered: true,
            message: `⚠️ 整体账户从峰值回撤 ${drawdown.toFixed(1)}%（超过${trigger.value}%阈值），建议${trigger.action}`
          };
        }
      }
    }
    
    // 指数跌到/涨到某点位
    if (trigger.condition === 'fallBelow' || trigger.condition === 'riseAbove') {
      // 暂不实现指数查询（需要股票API），留待后续
      return { triggered: false };
    }
    
  } catch (err) {
    console.error(`[trigger-check] 检查触发器出错:`, err.message);
  }
  
  return { triggered: false };
}

/**
 * 获取基金实时估值
 * @param {string} code - 6位基金代码
 * @returns {Object|null} { name, dwjz(净值), gsz(估值), gszzl(估值涨幅) }
 */
async function fetchFundNav(code) {
  try {
    const url = FUND_API(code);
    const res = await fetch(url, { 
      signal: AbortSignal.timeout(5000) 
    });
    const text = await res.text();
    // 返回格式: jsonpgz({"fundcode":"024975","name":"...",...});
    const match = text.match(/jsonpgz\((.+)\)/);
    if (!match) return null;
    return JSON.parse(match[1]);
  } catch {
    return null;
  }
}

/**
 * 批量检查所有计划的条件触发器
 * @param {Array} plans - 计划列表（含触发器）
 * @param {Object} assetContext - 资产上下文
 * @returns {Array} 触发的提醒列表
 */
export async function checkAllTriggers(plans, assetContext = {}) {
  const alerts = [];
  
  for (const plan of plans) {
    if (plan.status !== 'active' && plan.status !== '进行中') continue;
    
    const triggers = plan.triggers?.conditional || [];
    for (const trigger of triggers) {
      const result = await checkConditionalTrigger(trigger, {
        ...assetContext,
        baselineNav: plan.assetSnapshot?.baselineNavs || {}
      });
      
      if (result.triggered) {
        alerts.push({
          planName: plan.name,
          ...result
        });
      }
    }
  }
  
  return alerts;
}

// CLI入口
if (process.argv[1] && process.argv[1].endsWith('trigger-check.mjs')) {
  const plansFile = process.argv[2];
  if (!plansFile) {
    console.log('用法: node trigger-check.mjs <plans-index.json>');
    process.exit(1);
  }
  
  const plans = JSON.parse(require('fs').readFileSync(plansFile, 'utf-8'));
  checkAllTriggers(plans).then(alerts => {
    if (alerts.length === 0) {
      console.log('✅ 所有条件触发器均未触发');
    } else {
      for (const a of alerts) {
        console.log(`🔔 [${a.planName}] ${a.message}`);
      }
    }
  });
}
