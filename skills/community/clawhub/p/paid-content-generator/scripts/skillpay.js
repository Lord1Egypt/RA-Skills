/**
 * SkillPay Billing Integration
 * 收费接口 - 每次调用扣费 0.001 USDT
 */

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = process.env.SKILLPAY_API_KEY || 'sk_a267a27a1eb8381a762a9a6cdb1ea7d722f9f45f345b7319cfd3cccd9fae35c5';
const SKILL_ID = '8e76099f-7d7b-4059-83de-719930c981d6';

/**
 * 查询用户余额
 * @param {string} userId - 用户ID
 * @returns {Promise<number>} - 余额(USDT)
 */
async function checkBalance(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`,
    {
      headers: { 'X-API-Key': BILLING_API_KEY }
    }
  );
  const data = await resp.json();
  return data.balance;
}

/**
 * 扣费 - 每次调用扣费 0.001 USDT
 * @param {string} userId - 用户ID
 * @param {number} amount - 扣费金额，默认0.001 USDT
 * @returns {Promise<{ok: boolean, balance?: number, paymentUrl?: string}>}
 */
async function chargeUser(userId, amount = 0.001) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: amount,
    }),
  });
  
  const data = await resp.json();
  
  if (data.success) {
    return { ok: true, balance: data.balance };
  }
  
  // 余额不足 → 返回充值链接
  return { 
    ok: false, 
    balance: data.balance, 
    paymentUrl: data.payment_url 
  };
}

/**
 * 生成充值链接
 * @param {string} userId - 用户ID
 * @param {number} amount - 充值金额(USDT)，最低8 USDT
 * @returns {Promise<string>} - BNB Chain USDT 支付链接
 */
async function getPaymentLink(userId, amount = 8) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      amount,
    }),
  });
  const data = await resp.json();
  return data.payment_url;
}

module.exports = { 
  checkBalance, 
  chargeUser, 
  getPaymentLink,
  SKILL_ID,
  SKILL_PRICE: 0.001
};
