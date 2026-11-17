#!/usr/bin/env node
/**
 * 月度欠费检查脚本
 * 在每月 1 号运行，检查上月欠费并记录到本月账本
 */

const fs = require('fs');
const path = require('path');
const handler = require('./handler');

const WORKSPACE = '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = path.join(WORKSPACE, 'kids-points');

/**
 * 获取今天日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 判断是否是每月 1 号
 */
function isMonthStart() {
  const now = new Date();
  return now.getDate() === 1;
}

/**
 * 主函数
 */
function main() {
  const today = getTodayStr();
  console.log(`[${today}] 开始检查月度欠费...`);
  
  // 检查是否是每月 1 号
  if (!isMonthStart()) {
    console.log(`今天不是每月 1 号，跳过欠费检查。`);
    console.log(`下次检查时间：下月 1 号`);
    return;
  }
  
  // 检查欠费
  const overdraft = handler.checkMonthlyOverdraft();
  
  if (overdraft) {
    if (overdraft.alreadyRecorded) {
      console.log(`✅ 上月欠费已记录，无需重复处理。`);
      console.log(`   上月支出：${overdraft.lastMonthExpense} 分`);
      console.log(`   欠费金额：${overdraft.overdraft} 分`);
      console.log(`   本月可用：${overdraft.availableLimit} 分`);
    } else {
      console.log(`⚠️ 检测到上月欠费，已记录到本月账本。`);
      console.log(`   上月支出：${overdraft.lastMonthExpense} 分`);
      console.log(`   额度限制：${overdraft.spendingLimit} 分`);
      console.log(`   欠费金额：${overdraft.overdraft} 分`);
      console.log(`   本月可用：${overdraft.availableLimit} 分`);
      
      // 生成通知消息
      const message = `📊 **月度额度重置通知**\n\n` +
        `**本月额度**: 400 分\n` +
        `**上月欠费**: -${overdraft.overdraft} 分（上月支出 ${overdraft.lastMonthExpense} 分）\n` +
        `**实际可用**: ${overdraft.availableLimit} 分\n\n` +
        `_欠费已自动记入账本，请合理消费哦~_`;
      
      console.log(`\n📤 通知消息:\n${message}`);
    }
  } else {
    console.log(`✅ 上月无欠费，本月可用额度 400 分。`);
  }
}

// 运行主函数
if (require.main === module) {
  main();
}

module.exports = { main, isMonthStart };
