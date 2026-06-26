'use strict';

/**
 * @module placeholder-enforcer
 * @description 占位符强制执行模块 — 申报助手专有
 *
 * 扫描模型输出，检测并替换疑似 AI 编造的编号/金额，
 * 同时豁免用户填写的合法金额数字。
 */

/**
 * 从用户输入数据中提取应豁免替换的数字白名单（字符串形式）
 * @param {object} input
 * @returns {Set<string>}
 */
function buildAmountWhitelist(input) {
  const whitelist = new Set();
  if (!input || typeof input !== 'object') return whitelist;

  const TOP_CURRENCY_FIELDS = [
    'total_budget', 'matching_fund_amount',
    'tencent_fundraising_goal', 'price_quote',
  ];
  for (const field of TOP_CURRENCY_FIELDS) {
    if (typeof input[field] === 'number' && isFinite(input[field])) {
      whitelist.add(String(Math.round(input[field])));
      whitelist.add(String(Math.floor(input[field])));
    }
  }

  if (Array.isArray(input.budget_breakdown)) {
    for (const item of input.budget_breakdown) {
      if (item && typeof item.amount === 'number' && isFinite(item.amount)) {
        whitelist.add(String(Math.round(item.amount)));
        whitelist.add(String(Math.floor(item.amount)));
      }
    }
  }

  if (typeof input.target_count === 'number' && isFinite(input.target_count)) {
    whitelist.add(String(Math.round(input.target_count)));
  }

  return whitelist;
}

/**
 * 扫描模型输出，检测并替换疑似 AI 编造内容。
 *
 * @param {string} text - 模型输出文本
 * @param {object} [input={}] - 用户输入（用于构建金额白名单）
 * @returns {{ text: string, replacements: Array<{original: string, replacement: string, position: number}>, count: number }}
 */
function enforcePlaceholders(text, input = {}) {
  if (typeof text !== 'string') {
    return { text: '', replacements: [], count: 0 };
  }

  const whitelistNumbers = buildAmountWhitelist(input);

  const PATTERNS = [
    {
      regex: /\b\d{4}-\d{4}-\d{4}(?:-\d{4})?\b/g,
      getReplacement: () => '[请填写银行账号]',
    },
    {
      regex: /\b[A-Z]{1,4}\d{4,}\b/g,
      getReplacement: (match) => `[请填写${match.slice(0, 2)}编号]`,
    },
    {
      regex: /\b\d{8,}\b/g,
      getReplacement: () => '[请填写编号]',
    },
  ];

  // 收集所有匹配项（含 pattern 来源），一次性处理
  const allMatches = [];

  for (const { regex, getReplacement } of PATTERNS) {
    regex.lastIndex = 0;
    let m;
    while ((m = regex.exec(text)) !== null) {
      if (!whitelistNumbers.has(m[0])) {
        allMatches.push({
          original: m[0],
          index: m.index,
          replacement: getReplacement(m[0]),
        });
      }
    }
  }

  // 去重（同一位置可能被多个 pattern 命中，保留第一个即可）
  const seen = new Set();
  const uniqueMatches = allMatches.filter(({ index, original }) => {
    const key = `${index}:${original}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  // 从后向前替换，避免索引偏移问题
  uniqueMatches.sort((a, b) => b.index - a.index);

  const replacements = [];
  let result = text;

  for (const { original, index, replacement } of uniqueMatches) {
    result = result.slice(0, index) + replacement + result.slice(index + original.length);
    replacements.push({ original, replacement, position: index });
  }

  // 按原始位置正序返回（方便调用方展示）
  replacements.reverse();

  return { text: result, replacements, count: replacements.length };
}

module.exports = { enforcePlaceholders, buildAmountWhitelist };
