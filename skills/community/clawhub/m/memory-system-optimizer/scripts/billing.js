#!/usr/bin/env node
/**
 * SkillPay 收费模块
 * 
 * 使用方法：
 *   node billing.js charge <user_id>
 *   node billing.js balance <user_id>
 *   node billing.js payment-link <user_id> <amount>
 */

const SKILLPAY_API = "https://skillpay.me/api/v1/billing";

// 从环境变量读取配置
const API_KEY = process.env.SKILLPAY_API_KEY;
const SKILL_ID = process.env.SKILLPAY_SKILL_ID;

if (!API_KEY || !SKILL_ID) {
  console.error("❌ 请配置环境变量:");
  console.error("   export SKILLPAY_API_KEY=\"你的APIKey\"");
  console.error("   export SKILLPAY_SKILL_ID=\"你的SkillID\"");
  process.exit(1);
}

const command = process.argv[2];
const userId = process.argv[3] || `user_${Date.now()}`;
const amount = parseFloat(process.argv[4]) || 5.0;

async function charge(userId) {
  console.log(`💳 正在扣费... user: ${userId}`);
  
  const response = await fetch(`${SKILLPAY_API}/charge`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log(`✅ 扣费成功！余额: ${result.balance} USDT`);
    return true;
  } else {
    console.log(`❌ 余额不足！`);
    console.log(`💳 支付链接: ${result.payment_url}`);
    return false;
  }
}

async function getBalance(userId) {
  console.log(`📊 查询余额... user: ${userId}`);
  
  const response = await fetch(`${SKILLPAY_API}/balance?user_id=${userId}`, {
    headers: {
      "X-API-Key": API_KEY
    }
  });
  
  const result = await response.json();
  console.log(`💰 余额: ${result.balance} USDT`);
}

async function createPaymentLink(userId, amount) {
  console.log(`🔗 生成支付链接... user: ${userId}, 金额: ${amount} USDT`);
  
  const response = await fetch(`${SKILLPAY_API}/payment-link`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({
      user_id: userId,
      amount: amount
    })
  });
  
  const result = await response.json();
  console.log(`💳 支付链接: ${result.payment_url}`);
}

async function main() {
  const command = process.argv[2];
  
  switch (command) {
    case "charge":
      await charge(process.argv[3] || `user_${Date.now()}`);
      break;
    case "balance":
      await getBalance(process.argv[3] || `user_${Date.now()}`);
      break;
    case "payment-link":
      await createPaymentLink(
        process.argv[3] || `user_${Date.now()}`,
        parseFloat(process.argv[4]) || 5.0
      );
      break;
    default:
      console.log(`
Usage: node billing.js <command> [args]

Commands:
  charge <user_id>           扣费（检查余额并扣费）
  balance <user_id>          查询余额
  payment-link <user_id> <amount>  生成充值链接

Examples:
  node billing.js charge user_123
  node billing.js balance user_123
  node billing.js payment-link user_123 10
`);
  }
}

main().catch(console.error);
