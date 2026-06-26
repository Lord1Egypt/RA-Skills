#!/usr/bin/env node

/**
 * Polymarket Arbitrage Pro v7.1.2
 * 
 * 功能：Polymarket预测市场真实交易
 * - 市场扫描与套利检测
 * - 真实链上交易
 * - SkillPay按调用收费
 * 
 * 环境变量：
 *   POLYMARKET_PRIVATE_KEY - Polygon钱包私钥（必需）
 *   SKILLPAY_KEY - SkillPay密钥（必需）
 */

const fetch = require('node-fetch');
const crypto = require('crypto');
const { ethers } = require('ethers');

const API = 'https://gamma-api.polymarket.com';
const CLOB_API = 'https://clob.polymarket.com';
const CHAIN_ID = 137; // Polygon

// 环境变量
const PRIVATE_KEY = process.env.POLYMARKET_PRIVATE_KEY;
const SKILLPAY_KEY = process.env.SKILLPAY_KEY;
const SKILL_ID = 'cc7d6401-0a5c-46eb-8694-673ffa587c8b';

// 全局状态
let wallet = null;
let walletAddress = null;
let clobClient = null;

// ============ 钱包初始化 ============

async function initWallet() {
  if (!PRIVATE_KEY) {
    console.log('⚠️ 未设置 POLYMARKET_PRIVATE_KEY');
    return false;
  }
  
  try {
    const cleanKey = PRIVATE_KEY.startsWith('0x') ? PRIVATE_KEY.slice(2) : PRIVATE_KEY;
    wallet = new ethers.Wallet('0x' + cleanKey);
    walletAddress = wallet.address;
    console.log('✅ 钱包已连接:', walletAddress.slice(0, 6) + '...' + walletAddress.slice(-4));
    
    // 初始化CLOB客户端
    await initClobClient();
    return true;
  } catch (e) {
    console.error('❌ 私钥格式错误:', e.message);
    return false;
  }
}

// ============ CLOB客户端初始化 ============

async function initClobClient() {
  try {
    // 动态导入
    const { ClobClient } = require('@polymarket/clob-client');
    
    clobClient = new ClobClient(CLOB_API, CHAIN_ID, wallet);
    
    // 派生API凭证
    const apiCreds = await clobClient.createOrDeriveApiKey();
    console.log('✅ CLOB客户端已初始化');
    return true;
  } catch (e) {
    console.log('⚠️ CLOB SDK未安装，使用API下单');
    return false;
  }
}

// ============ Polymarket API ============

async function getMarkets(limit = 50) {
  const res = await fetch(`${API}/markets?active=true&closed=false&limit=${limit}`);
  return await res.json();
}

async function getMarketDetails(conditionId) {
  try {
    const res = await fetch(`${API}/markets?conditionId=${conditionId}`);
    const markets = await res.json();
    return markets[0] || null;
  } catch (e) {
    return null;
  }
}

// ============ 真实交易下单 ============

async function placeOrder(tokenId, side, price, size) {
  if (!walletAddress) {
    console.log('❌ 需要配置POLYMARKET_PRIVATE_KEY才能交易');
    return null;
  }
  
  console.log(`📝 提交订单: ${side} ${size} @ ${price}`);
  console.log(`   Token: ${tokenId.slice(0, 20)}...`);
  
  // 如果CLOB客户端可用，使用SDK下单
  if (clobClient) {
    try {
      const { Side, OrderType } = require('@polymarket/clob-client');
      
      const response = await clobClient.createAndPostOrder(
        {
          tokenID: tokenId,
          price: price,
          size: size,
          side: side === 'BUY' ? Side.BUY : Side.SELL,
          orderType: OrderType.GTC,
        },
        {
          tickSize: '0.01',
          negRisk: false,
        }
      );
      
      console.log('✅ 订单已提交:', response.orderID);
      return response;
    } catch (e) {
      console.log('⚠️ SDK下单失败:', e.message);
    }
  }
  
  // 备用：直接调用API
  try {
    const order = {
      token_id: tokenId,
      price: price,
      size: size,
      side: side.toUpperCase(),
      order_type: 'GTC',
      nonce: Date.now(),
      fee_rate_bps: 0
    };
    
    // 签名订单
    const signature = await wallet.signMessage(JSON.stringify(order));
    
    // 提交订单
    const res = await fetch(`${CLOB_API}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${walletAddress}:${signature}`
      },
      body: JSON.stringify(order)
    });
    
    const result = await res.json();
    
    if (result.orderID) {
      console.log('✅ 订单已提交:', result.orderID);
      return result;
    } else {
      console.log('⚠️ 订单提交响应:', result);
      return result;
    }
  } catch (e) {
    console.log('⚠️ API下单失败    return { error: e.message };
:', e.message);
  }
}

// ============ SkillPay 收费 ============

async function checkBalance() {
  if (!SKILLPAY_KEY || !walletAddress) return 0;
  
  try {
    const resp = await fetch(
      `https://skillpay.me/api/v1/billing/balance?user_id=${walletAddress}`,
      { headers: { 'X-API-Key': SKILLPAY_KEY } }
    );
    const data = await resp.json();
    return data.balance || 0;
  } catch (e) {
    return 0;
  }
}

async function chargeUser() {
  if (!SKILLPAY_KEY || !walletAddress) return { ok: true };
  
  try {
    const resp = await fetch(`https://skillpay.me/api/v1/billing/charge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': SKILLPAY_KEY
      },
      body: JSON.stringify({
        user_id: walletAddress,
        skill_id: SKILL_ID,
        amount: 0
      })
    });
    
    const data = await resp.json();
    
    if (data.success) {
      return { ok: true, balance: data.balance };
    } else {
      return { ok: false, balance: data.balance, payment_url: data.payment_url };
    }
  } catch (e) {
    return { ok: true };
  }
}

// ============ 套利检测 ============

async function detectArbitrage(markets) {
  const opportunities = [];
  
  for (const market of markets.slice(0, 30)) {
    if (!market.clobTokenIds || market.clobTokenIds.length < 2) continue;
    
    const yesToken = market.clobTokenIds[0];
    const noToken = market.clobTokenIds[1];
    
    let yesPrice = 0.5, noPrice = 0.5;
    try {
      if (market.outcomePrices) {
        const prices = JSON.parse(market.outcomePrices);
        yesPrice = parseFloat(prices[0]) || 0.5;
        noPrice = parseFloat(prices[1]) || 0.5;
      }
    } catch (e) {}
    
    const total = yesPrice + noPrice;
    const deviation = Math.abs(1 - total);
    
    if (deviation > 0.02) {
      opportunities.push({
        question: market.question,
        yesPrice,
        noPrice,
        yesToken,
        noToken,
        deviation: (deviation * 100).toFixed(2)
      });
    }
  }
  
  return opportunities.sort((a, b) => b.deviation - a.deviation);
}

// ============ 主命令 ============

async function scan() {
  console.log('🔍 扫描Polymarket市场...\n');
  
  // 显示余额
  const balance = await checkBalance();
  if (SKILLPAY_KEY) {
    console.log(`💰 余额: ${balance} tokens`);
  }
  
  // 检查付费状态
  const payment = await chargeUser();
  if (!payment.ok) {
    console.log('⚠️ 余额不足，请充值后继续使用');
    console.log('💳 充值链接:', payment.payment_url);
    return;
  }
  
  const markets = await getMarkets();
  console.log(`📊 活跃市场: ${markets.length}`);
  
  const ops = await detectArbitrage(markets);
  
  if (ops.length === 0) {
    console.log('❌ 暂无套利机会');
    return;
  }
  
  console.log(`\n✅ 发现 ${ops.length} 个机会:\n`);
  for (const op of ops.slice(0, 3)) {
    console.log(`📌 ${op.question.substring(0, 60)}...`);
    console.log(`   Yes: ${(op.yesPrice*100).toFixed(1)}% | No: ${(op.noPrice*100).toFixed(1)}% | 偏离: ${op.deviation}%`);
    
    // 自动交易
    if (walletAddress) {
      // 买入便宜的
      if (op.yesPrice < 0.5) {
        await placeOrder(op.yesToken, 'BUY', op.yesPrice, 10);
      } else if (op.noPrice < 0.5) {
        await placeOrder(op.noToken, 'BUY', op.noPrice, 10);
      }
    }
    console.log('');
  }
}

async function start() {
  console.log('🚀 启动持续监控...\n');
  await initWallet();
  
  setInterval(async () => {
    console.log(`\n⏰ ${new Date().toLocaleTimeString()}`);
    await scan();
  }, 60000);
}

async function balance() {
  await initWallet();
  console.log('💰 钱包地址:', walletAddress);
  
  const balance = await checkBalance();
  if (SKILLPAY_KEY) {
    console.log(`💳 剩余调用次数: ${balance} tokens`);
  }
}

// ============ CLI ============

(async () => {
  const cmd = process.argv[2] || 'scan';

  console.log('🤖 Polymarket Arbitrage Pro v7.1.4');
  console.log('=============================================\n');

  if (cmd === 'scan') {
    await initWallet();
    await scan();
  } else if (cmd === 'start') {
    await start();
  } else if (cmd === 'balance') {
    await balance();
  } else if (cmd === 'help') {
    console.log('用法: node polymarket-trade.js <command>');
    console.log('');
    console.log('命令:');
    console.log('  scan     - 扫描市场机会');
    console.log('  start    - 启动持续监控');
    console.log('  balance  - 查看余额');
    console.log('  help     - 显示帮助');
    console.log('');
    console.log('环境变量:');
    console.log('  POLYMARKET_PRIVATE_KEY - Polygon钱包私钥（必需）');
    console.log('  SKILLPAY_KEY          - SkillPay密钥（必需）');
  } else {
    console.log(`未知命令: ${cmd}`);
  }
})();
