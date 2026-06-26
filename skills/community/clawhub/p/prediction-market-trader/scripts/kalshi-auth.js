#!/usr/bin/env node
/**
 * Kalshi API Client with RSA-PSS Authentication
 * 
 * Usage:
 *   const { kalshiApi } = require('./kalshi-auth');
 *   const balance = await kalshiApi('GET', '/trade-api/v2/portfolio/balance');
 */

const crypto = require('crypto');
const https = require('https');

const HOSTNAME = 'api.elections.kalshi.com';

function getCredentials() {
  const keyId = process.env.KALSHI_KEY_ID;
  const privKey = process.env.KALSHI_PRIVATE_KEY;
  if (!keyId || !privKey) throw new Error('Set KALSHI_KEY_ID and KALSHI_PRIVATE_KEY env vars');
  return { keyId, privKey };
}

function sign(method, path, privKey) {
  const ts = Math.floor(Date.now() / 1000).toString();
  const msg = ts + method + path;
  const key = crypto.createPrivateKey(privKey);
  const sig = crypto.sign('sha256', Buffer.from(msg), {
    key,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: 32
  });
  return { ts, sig: sig.toString('base64') };
}

function kalshiApi(method, signPath, body) {
  const { keyId, privKey } = getCredentials();
  const { ts, sig } = sign(method, signPath, privKey);
  
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: HOSTNAME,
      path: signPath,
      method,
      headers: {
        'KALSHI-ACCESS-KEY': keyId,
        'KALSHI-ACCESS-TIMESTAMP': ts,
        'KALSHI-ACCESS-SIGNATURE': sig,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    };
    
    const req = https.request(opts, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); }
        catch (e) { resolve({ error: d }); }
      });
    });
    
    if (body) req.write(JSON.stringify(body));
    req.on('error', reject);
    req.end();
  });
}

// Convenience methods
async function getBalance() {
  const bal = await kalshiApi('GET', '/trade-api/v2/portfolio/balance');
  return {
    cash: (bal.balance / 100).toFixed(2),
    portfolio: (bal.portfolio_value / 100).toFixed(2),
    total: ((bal.balance + bal.portfolio_value) / 100).toFixed(2)
  };
}

async function getPositions(status = 'unsettled') {
  return kalshiApi('GET', '/trade-api/v2/portfolio/positions');
}

async function getMarket(ticker) {
  const data = await kalshiApi('GET', '/trade-api/v2/markets/' + ticker);
  return data.market;
}

async function getEvents(seriesTicker, status = 'open', limit = 50) {
  const path = '/trade-api/v2/events';
  const query = `?series_ticker=${seriesTicker}&status=${status}&limit=${limit}`;
  return kalshiApi('GET', path + query);
}

async function placeOrder({ ticker, action = 'buy', side = 'yes', type = 'limit', count, price }) {
  return kalshiApi('POST', '/trade-api/v2/portfolio/orders', {
    ticker, action, side, type, count,
    yes_price: side === 'yes' ? price : undefined,
    no_price: side === 'no' ? price : undefined,
  });
}

async function cancelOrder(orderId) {
  return kalshiApi('DELETE', '/trade-api/v2/portfolio/orders/' + orderId);
}

module.exports = { kalshiApi, getBalance, getPositions, getMarket, getEvents, placeOrder, cancelOrder };

// CLI mode
if (require.main === module) {
  (async () => {
    const bal = await getBalance();
    console.log('Balance:', JSON.stringify(bal, null, 2));
  })().catch(e => console.error(e));
}
