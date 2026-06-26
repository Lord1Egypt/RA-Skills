// ═══════════════════════════════════════════════════
// SkillPay Billing Integration
// ═══════════════════════════════════════════════════

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = process.env.SKILLPAY_API_KEY;
const SKILL_ID = '15a4951e-5e72-47ef-a3bd-f719d31760f2';

if (!BILLING_API_KEY) throw new Error('SKILLPAY_API_KEY environment variable is not set');
const CHARGE_AMOUNT = 0.001; // USDT per call

async function checkBalance(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`,
    { headers: { 'X-API-Key': BILLING_API_KEY } }
  );
  const data = await resp.json();
  return data.balance;
}

async function chargeUser(userId) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: CHARGE_AMOUNT,
    }),
  });
  const data = await resp.json();

  if (data.success) {
    return { ok: true, balance: data.balance };
  }
  return { ok: false, balance: data.balance, paymentUrl: data.payment_url };
}

async function getPaymentLink(userId, amount = 1) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, amount }),
  });
  const data = await resp.json();
  return data.payment_url;
}

module.exports = { checkBalance, chargeUser, getPaymentLink };
