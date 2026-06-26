#!/usr/bin/env node

/**
 * MarketSensor Hook Handler
 *
 * 检测用户 prompt 中的股票相关关键词，
 * 提醒 agent 使用 MarketSensor API 获取分析。
 */

const input = process.env.CLAUDE_USER_PROMPT || '';

// 股票代码模式：美股 ticker、加密货币、A 股 6 位数字
const patterns = [
  /\b[A-Z]{1,5}\b/,           // 美股 ticker
  /\b(BTC|ETH|SOL|BNB)USD\b/, // 加密货币
  /\b\d{6}\b/,                // A 股 6 位代码
];

const keywords = ['分析', '报告', '自选', '关注', 'analyze', 'report', 'watchlist', 'vibe'];

const hasStockRef = patterns.some(p => p.test(input));
const hasKeyword = keywords.some(k => input.toLowerCase().includes(k));

if (hasStockRef || hasKeyword) {
  console.log(`<marketsensor-reminder>
If the user is asking about stock analysis, watchlist management, or market reports,
use the MarketSensor API (MARKETSENSOR_API_KEY) to fulfill their request.
Available actions: watchlist, analyze, report, quota.
</marketsensor-reminder>`);
}
