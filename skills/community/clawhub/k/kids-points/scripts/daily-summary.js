#!/usr/bin/env node

/**
 * 每日积分总结 - 定时任务脚本
 * 每天早上 7 点执行，发送前一天的积分总结
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = '/home/wang/.openclaw/agents/kids-study/workspace/kids-points';

/**
 * 获取昨天日期字符串
 */
function getYesterdayStr() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return yesterday.toISOString().split('T')[0];
}

/**
 * 获取今天日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 读取月度账本
 */
function loadMonthlyLog(monthStr) {
  const filePath = path.join(POINTS_DIR, 'monthly', `${monthStr}.md`);
  if (fs.existsSync(filePath)) {
    return fs.readFileSync(filePath, 'utf8');
  }
  return null;
}

/**
 * 生成每日总结
 */
function generateDailySummary() {
  const today = getTodayStr();
  const yesterday = getYesterdayStr();
  const monthStr = today.substring(0, 7); // YYYY-MM
  
  const content = loadMonthlyLog(monthStr);
  
  if (!content) {
    return `📅 **${today} 每日总结**\n\n_暂无积分记录_`;
  }
  
  // 提取昨天记录
  const yesterdayHeader = `### ${yesterday}`;
  const yesterdayIndex = content.indexOf(yesterdayHeader);
  
  let yesterdaySection = '';
  if (yesterdayIndex !== -1) {
    const nextDayIndex = content.indexOf('### ', yesterdayIndex + 1);
    yesterdaySection = content.slice(yesterdayIndex, nextDayIndex === -1 ? content.length : nextDayIndex);
  }
  
  // 提取本月汇总
  const summaryMatch = content.match(/## 本月汇总[\s\S]*?距离上限 \(400 分\) \| ([\d.]+) 分/);
  const balance = summaryMatch ? summaryMatch[1] : '未知';
  
  // 生成总结
  let summary = `📅 **${today} 每日总结**\n\n`;
  summary += `━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (yesterdaySection) {
    summary += `📊 **${yesterday} 积分情况**:\n\n`;
    summary += yesterdaySection.trim() + '\n\n';
  } else {
    summary += `📊 **${yesterday} 积分情况**:\n\n`;
    summary += '_暂无记录_\n\n';
  }
  
  summary += `━━━━━━━━━━━━━━━━━━\n\n`;
  summary += `💰 **当前余额**: ${balance} 分\n\n`;
  summary += `_继续加油！今天也要努力完成任务哦~_ 💪`;
  
  return summary;
}

// 主程序
const summary = generateDailySummary();
console.log(summary);

// 如果需要发送到飞书，可以通过 OpenClaw 的消息接口
// 这里先输出到控制台，由 cron 调用时通过 OpenClaw 发送
