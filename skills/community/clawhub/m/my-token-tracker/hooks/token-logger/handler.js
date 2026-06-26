#!/usr/bin/env node
/**
 * Token Logger Hook - JavaScript 版本
 * 直接在 Node.js 中记录 token 用量
 */

import { existsSync, readFileSync, appendFileSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';

const DATA_DIR = join(homedir(), '.openclaw', 'workspace', 'skills', 'token-tracker');
const RECORDS_FILE = join(DATA_DIR, 'usage_records.json');
const CONFIG_FILE = join(DATA_DIR, 'config.json');

// 默认价格 (价格单位：美元 per 百万 tokens)
const DEFAULT_PRICES = {
  // Anthropic Claude 系列
  'claude-opus-4.6': { token_in_price: 5.0, token_out_price: 25.0 },
  'claude-sonnet-4.6': { token_in_price: 3.6, token_out_price: 18.0 },
  'claude-haiku-4': { token_in_price: 0.8, token_out_price: 4.0 },
  'claude-3-5-sonnet-20241022': { token_in_price: 3.0, token_out_price: 15.0 },
  'claude-3-5-sonnet-20240620': { token_in_price: 3.0, token_out_price: 15.0 },
  'claude-3-opus-20240229': { token_in_price: 15.0, token_out_price: 75.0 },
  'claude-3-sonnet-20240229': { token_in_price: 3.0, token_out_price: 15.0 },
  'claude-3-haiku-20240307': { token_in_price: 0.25, token_out_price: 1.25 },
  
  // OpenAI GPT 系列
  'gpt-5.4': { token_in_price: 3.13, token_out_price: 18.8 },
  'gpt-5.4-pro': { token_in_price: 37.5, token_out_price: 225.0 },
  'gpt-5.2': { token_in_price: 2.19, token_out_price: 17.5 },
  'gpt-4o': { token_in_price: 3.13, token_out_price: 12.5 },
  'gpt-4o-mini': { token_in_price: 0.19, token_out_price: 0.75 },
  
  // MiniMax 系列
  'minimax-m2.5': { token_in_price: 0.3, token_out_price: 1.2 },
  'minimax-m2.5-highspeed': { token_in_price: 0.6, token_out_price: 2.4 },
  'minimax-m2.1': { token_in_price: 0.3, token_out_price: 1.2 },
  'minimax-portal/MiniMax-M2.5': { token_in_price: 0.3, token_out_price: 1.2 },
  
  // Google Gemini 系列
  'gemini-3-pro': { token_in_price: 2.5, token_out_price: 15.0 },
  'gemini-3-flash': { token_in_price: 0.7, token_out_price: 3.75 },
  'gemma-3-27b': { token_in_price: 0.12, token_out_price: 0.2 },
  
  // Moonshot Kimi 系列
  'kimi-k2.5': { token_in_price: 0.75, token_out_price: 3.75 },
  'kimi-k2-thinking': { token_in_price: 0.75, token_out_price: 3.2 },
  
  // xAI Grok 系列
  'grok-4.1-fast': { token_in_price: 0.25, token_out_price: 0.63 },
  'grok-4.20-beta': { token_in_price: 2.5, token_out_price: 7.5 },
  'grok-code-fast-1': { token_in_price: 0.25, token_out_price: 1.87 },
  
  // 开源模型
  'llama-3.3-70b': { token_in_price: 0.7, token_out_price: 2.8 },
  'qwen-3-235b': { token_in_price: 0.15, token_out_price: 0.75 },
  'qwen-3-235b-thinking': { token_in_price: 0.45, token_out_price: 3.5 },
  'deepseek-v3.2': { token_in_price: 0.4, token_out_price: 1.0 },
  'mistral-small-3.2': { token_in_price: 0.09, token_out_price: 0.25 },
  
  // 向后兼容
  'gpt-3.5-turbo': { token_in_price: 0.5, token_out_price: 1.5 },
  
  // 默认回退
  'default': { token_in_price: 1.0, token_out_price: 2.0 }
};

/**
 * 从 session status 文件读取 token 用量
 * OpenClaw session status 保存在 ~/.openclaw/sessions/ 目录
 */
function getSessionStatus(sessionKey) {
  const sessionsDir = join(homedir(), '.openclaw', 'sessions');
  const statusFile = join(sessionsDir, `${sessionKey}.json`);
  
  if (existsSync(statusFile)) {
    try {
      const data = JSON.parse(readFileSync(statusFile, 'utf-8'));
      return {
        model: data.model || 'unknown',
        tokenIn: data.tokenIn || data.tokens?.in || 0,
        tokenOut: data.tokenOut || data.tokens?.out || 0,
        cost: data.cost || 0
      };
    } catch (e) {
      console.error('[token-logger] Error reading session status:', e.message);
    }
  }
  return null;
}

/**
 * 计算成本
 */
function calculateCost(model, tokenIn, tokenOut) {
  let prices = DEFAULT_PRICES.default;
  
  for (const [key, value] of Object.entries(DEFAULT_PRICES)) {
    if (key !== 'default' && model.toLowerCase().includes(key.toLowerCase())) {
      prices = value;
      break;
    }
  }
  
  return (tokenIn / 1000000 * prices.token_in_price) + 
         (tokenOut / 1000000 * prices.token_out_price);
}

/**
 * 添加记录
 */
function addRecord(sessionKey, model, tokenIn, tokenOut) {
  const cost = calculateCost(model, tokenIn, tokenOut);
  
  let records = [];
  if (existsSync(RECORDS_FILE)) {
    try {
      records = JSON.parse(readFileSync(RECORDS_FILE, 'utf-8'));
    } catch (e) {
      records = [];
    }
  }
  
  const record = {
    timestamp: new Date().toISOString(),
    session_id: sessionKey,
    model: model,
    token_in: tokenIn,
    token_out: tokenOut,
    cost: Math.round(cost * 1000000) / 1000000
  };
  
  records.push(record);
  
  // 确保目录存在
  const dir = dirname(RECORDS_FILE);
  if (!existsSync(dir)) {
    console.log('[token-logger] Data directory does not exist, skipping...');
    return null;
  }
  
  try {
    const fs = await import('fs');
    fs.writeFileSync(RECORDS_FILE, JSON.stringify(records, null, 2));
    console.log('[token-logger] Record added:', record);
    return record;
  } catch (e) {
    console.error('[token-logger] Error saving record:', e.message);
    return null;
  }
}

// Hook handler
const handler = async (event) => {
  // 只处理 session:compact:after 事件
  if (event.type !== 'session' || event.action !== 'compact:after') {
    return;
  }

  console.log('[token-logger] Session compaction detected, logging token usage...');
  console.log('[token-logger] Session:', event.sessionKey);
  console.log('[token-logger] Context:', JSON.stringify(event.context, null, 2));

  // 尝试从 session status 获取数据
  const status = getSessionStatus(event.sessionKey);
  if (status) {
    addRecord(event.sessionKey, status.model, status.tokenIn, status.tokenOut);
  } else {
    console.log('[token-logger] Could not get session status, using context data...');
    
    // 从 event context 尝试获取
    if (event.context?.summary?.tokenCount) {
      const tokens = event.context.summary.tokenCount;
      // 估算 in/out 比例
      const tokenIn = Math.floor(tokens * 0.45);
      const tokenOut = Math.ceil(tokens * 0.55);
      addRecord(event.sessionKey, 'unknown', tokenIn, tokenOut);
    }
  }
};

export default handler;
