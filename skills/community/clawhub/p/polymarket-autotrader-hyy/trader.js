#!/usr/bin/env node
// ═══════════════════════════════════════════════════
// Polymarket AutoTrader — Main Entry Point
// Assets: BTC, ETH, SOL, XRP
// Timeframes: 5min, 15min
// ═══════════════════════════════════════════════════

const { ClobClient } = require('@polymarket/clob-client');
const { ethers }     = require('ethers');
const { chargeUser, getPaymentLink } = require('./billing');
const { generateSignal } = require('./strategy');

// ─── Config (set via environment variables) ──────────────────────────────────
const {
  POLYMARKET_PRIVATE_KEY,   // Your Ethereum wallet private key
  POLYMARKET_API_KEY,       // Polymarket CLOB API key
  POLYMARKET_API_SECRET,    // Polymarket CLOB API secret
  POLYMARKET_API_PASSPHRASE,// Polymarket CLOB API passphrase
  SKILLPAY_USER_ID,         // Your SkillPay user ID (set by the caller)
  TRADE_TIMEFRAME = '5m',   // '5m' or '15m'
  TRADE_ASSETS    = 'BTC,ETH,SOL,XRP',
  MAX_TRADE_USDC  = '10',   // Max USDC per trade
  MIN_CONFIDENCE  = '60',   // Minimum signal confidence % to trade
  DRY_RUN         = 'false',// Set 'true' to simulate without real orders
} = process.env;

const HOST      = 'https://clob.polymarket.com';
const CHAIN_ID  = 137; // Polygon mainnet

// ─── Polymarket market slugs for crypto price prediction ─────────────────────
// These are "will X be above $Y at end of day?" markets.
// Dynamically discovered via Gamma API to always use fresh markets.
const GAMMA_API = 'https://gamma-api.polymarket.com';

async function findActiveCryptoMarkets(asset) {
  const query = encodeURIComponent(asset.toUpperCase());
  const url   = `${GAMMA_API}/markets?search=${query}&active=true&closed=false&limit=20`;
  const resp  = await fetch(url);
  const data  = await resp.json();

  // Filter to short-term price prediction markets
  const markets = (data.markets || data || []).filter(m => {
    const q = (m.question || '').toLowerCase();
    return (
      q.includes(asset.toLowerCase()) &&
      (q.includes('price') || q.includes('above') || q.includes('below') || q.includes('reach')) &&
      !m.closed
    );
  });

  // Sort by end_date ascending — prefer markets expiring soon
  markets.sort((a, b) => new Date(a.end_date_iso) - new Date(b.end_date_iso));
  return markets.slice(0, 3);
}

// ─── CLOB client setup ───────────────────────────────────────────────────────
function buildClient() {
  if (!POLYMARKET_PRIVATE_KEY) throw new Error('POLYMARKET_PRIVATE_KEY is required');
  const wallet = new ethers.Wallet(POLYMARKET_PRIVATE_KEY);
  const creds  = POLYMARKET_API_KEY ? {
    key:        POLYMARKET_API_KEY,
    secret:     POLYMARKET_API_SECRET,
    passphrase: POLYMARKET_API_PASSPHRASE,
  } : null;

  return new ClobClient(HOST, CHAIN_ID, wallet, creds);
}

// ─── Place a limit order based on signal ─────────────────────────────────────
async function placeOrder(client, market, signal, maxUsdc) {
  const isDryRun   = DRY_RUN === 'true';
  const tokenId    = signal.signal === 'BUY' ? market.tokens[0].token_id : market.tokens[1].token_id;
  const orderbook  = await client.getOrderBook(tokenId);
  const bestPrice  = signal.signal === 'BUY'
    ? parseFloat(orderbook.asks?.[0]?.price || '0.5')
    : parseFloat(orderbook.bids?.[0]?.price || '0.5');

  const size = parseFloat(maxUsdc) / bestPrice;

  console.log(`\n  [ORDER] ${market.question}`);
  console.log(`  Side: ${signal.signal === 'BUY' ? 'YES (BUY)' : 'NO (SELL)'} | Price: ${bestPrice.toFixed(4)} | Size: ${size.toFixed(2)}`);

  if (isDryRun) {
    console.log('  [DRY RUN] Order not submitted.');
    return { dry_run: true, price: bestPrice, size };
  }

  const order = await client.createAndPostOrder({
    tokenID:   tokenId,
    price:     bestPrice,
    side:      signal.signal === 'BUY' ? 'BUY' : 'SELL',
    size:      size,
    feeRateBps: 0,
    nonce:     0,
    expiration: 0,
  });

  return order;
}

// ─── Main trading loop ────────────────────────────────────────────────────────
async function runTrader() {
  // 1. Billing gate
  const userId = SKILLPAY_USER_ID || 'anonymous';
  const bill   = await chargeUser(userId);
  if (!bill.ok) {
    const link = bill.paymentUrl || await getPaymentLink(userId, 1);
    console.error(`\n❌ Insufficient SkillPay balance (${bill.balance} USDT).`);
    console.error(`   Top up here: ${link}\n`);
    process.exit(1);
  }
  console.log(`✅ Billing OK — balance after charge: ${bill.balance} USDT`);

  // 2. Build CLOB client
  const client     = buildClient();
  const assets     = TRADE_ASSETS.split(',').map(a => a.trim().toUpperCase());
  const timeframe  = TRADE_TIMEFRAME === '15m' ? '15m' : '5m';
  const minConf    = parseInt(MIN_CONFIDENCE, 10);
  const maxUsdc    = parseFloat(MAX_TRADE_USDC);

  console.log(`\n📊 Polymarket AutoTrader`);
  console.log(`   Assets: ${assets.join(', ')} | Timeframe: ${timeframe} | Min confidence: ${minConf}%\n`);

  // 3. Process each asset
  for (const asset of assets) {
    try {
      console.log(`\n── ${asset} ─────────────────────────`);

      // Generate signal
      const sig = await generateSignal(asset, timeframe);
      console.log(`  Signal: ${sig.signal} (${sig.confidence}% conf) | Price: $${sig.price.toFixed(4)}`);
      console.log(`  RSI: ${sig.rsi?.toFixed(1)} | MACD: ${sig.macd?.toFixed(6)} | EMA9/21: ${sig.ema9?.toFixed(4)}/${sig.ema21?.toFixed(4)}`);

      if (sig.signal === 'HOLD' || sig.confidence < minConf) {
        console.log(`  → Skipping (HOLD or low confidence)`);
        continue;
      }

      // Find relevant Polymarket markets
      const markets = await findActiveCryptoMarkets(asset);
      if (!markets.length) {
        console.log(`  → No active Polymarket markets found for ${asset}`);
        continue;
      }

      // Trade on the soonest-expiring market
      const market = markets[0];
      console.log(`  Market: "${market.question}" (exp: ${market.end_date_iso})`);

      const result = await placeOrder(client, market, sig, maxUsdc);
      console.log(`  ✓ Order result:`, JSON.stringify(result, null, 2));

    } catch (err) {
      console.error(`  ✗ Error processing ${asset}:`, err.message);
    }
  }

  console.log('\n✅ Trading cycle complete.\n');
}

// ─── Scheduler ───────────────────────────────────────────────────────────────
async function startScheduler() {
  const tf     = TRADE_TIMEFRAME === '15m' ? '15m' : '5m';
  const ms     = tf === '15m' ? 15 * 60 * 1000 : 5 * 60 * 1000;
  const label  = tf === '15m' ? '15 minutes' : '5 minutes';

  console.log(`🚀 Polymarket AutoTrader started — running every ${label}`);
  console.log(`   DRY_RUN=${DRY_RUN} | Assets=${TRADE_ASSETS}\n`);

  // Run immediately, then on interval
  await runTrader();
  setInterval(runTrader, ms);
}

startScheduler().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
