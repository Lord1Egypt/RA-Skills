#!/usr/bin/env node
/**
 * 长期计划 - 资产快照更新模块
 * 
 * 心跳时调用，更新index.json中的资产快照
 */

import fs from 'fs';
import path from 'path';

const FUND_API = code => `https://fundgz.1234567.com.cn/js/${code}.js`;

/**
 * 获取基金实时估值
 */
async function fetchFundNav(code) {
  try {
    const res = await fetch(FUND_API(code), { signal: AbortSignal.timeout(5000) });
    const text = await res.text();
    const match = text.match(/jsonpgz\((.+)\)/);
    if (!match) return null;
    return JSON.parse(match[1]);
  } catch (err) {
    console.error(`[asset] 获取 ${code} 失败:`, err.message);
    return null;
  }
}

/**
 * 更新计划的资产快照
 * @param {Object} plan - 计划对象
 * @returns {Object} 更新后的快照
 */
export async function updateAssetSnapshot(plan) {
  const positions = plan.assetSnapshot?.positions || [];
  let totalAsset = 0;
  const updatedPositions = [];
  
  for (const pos of positions) {
    const nav = await fetchFundNav(pos.code);
    if (nav) {
      // 根据金额估算份额，然后乘估值得到当前市值
      // 简化：直接用金额乘涨跌幅估算
      const gainPercent = parseFloat(nav.gszzl) || 0;
      const currentValue = pos.amount * (1 + gainPercent / 100);
      
      totalAsset += currentValue;
      updatedPositions.push({
        ...pos,
        name: nav.name,
        currentValue,
        todayGain: gainPercent
      });
    } else {
      // API失败，保留原值
      totalAsset += pos.amount;
      updatedPositions.push(pos);
    }
  }
  
  // 计算周变动
  const prevTotal = plan.assetSnapshot?.totalAsset || totalAsset;
  const weekChange = ((totalAsset - prevTotal) / prevTotal * 100).toFixed(2);
  
  return {
    lastUpdated: new Date().toISOString().split('T')[0],
    totalAsset: Math.round(totalAsset),
    weekChange: `${weekChange}%`,
    positions: updatedPositions,
    peakAsset: Math.max(prevTotal, totalAsset)  // 记录峰值用于回撤计算
  };
}

/**
 * 更新所有计划的资产快照
 * @param {string} indexFile - index.json路径
 */
export async function updateAllSnapshots(indexFile) {
  const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
  
  for (const plan of index.plans) {
    if (plan.status !== 'active') continue;
    if (!plan.assetSnapshot?.positions?.length) continue;
    
    plan.assetSnapshot = await updateAssetSnapshot(plan);
    console.log(`[asset] ${plan.name}: ${plan.assetSnapshot.totalAsset}元 (${plan.assetSnapshot.weekChange})`);
  }
  
  // 写回index.json（原子写入）
  const tmpFile = indexFile + '.tmp';
  fs.writeFileSync(tmpFile, JSON.stringify(index, null, 2));
  fs.renameSync(tmpFile, indexFile);
  
  return index;
}

// CLI入口
const args = process.argv.slice(2);
if (args.length > 0) {
  const indexFile = args[0];
  updateAllSnapshots(indexFile).then(() => {
    console.log('✅ 资产快照更新完成');
  });
}