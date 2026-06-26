#!/usr/bin/env node
/**
 * Polymarket Latency Arbitrage Bot
 * 
 * Exploits the 30-90 second lag between real-time BTC price moves
 * and Polymarket's 5-min/15-min BTC up/down market repricing.
 * 
 * Usage:
 *   node latency_arb.cjs scan              # One-time divergence check
 *   node latency_arb.cjs watch --dry       # Continuous dry-run monitoring
 *   node latency_arb.cjs history           # Past signals & outcomes
 */

const fs = require('fs');
const path = require('path');

// --- Config ---
const GAMMA_BASE = 'https://gamma-api.polymarket.com';
const HL_API = 'https://api.hyperliquid.xyz/info';
const DATA_DIR = path.join(__dirname, 'data');
const SIGNALS_FILE = path.join(DATA_DIR, 'latency_arb_signals.json');
const POLL_MS = 5000;           // Poll every 5 seconds
const MIN_DIVERGENCE = 0.05;    // 5% minimum divergence to flag
const MIN_PRICE_MOVE = 0.001;   // 0.1% minimum BTC move to consider
const TRADE_SIZE = 10;          // $10 per theoretical trade

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// --- Price tracking ---
let priceHistory = []; // [{ts, price}] rolling window

async function fetchBTCCandles() {
  const now = Date.now();
  const r = await fetch(HL_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'candleSnapshot',
      req: { coin: 'BTC', interval: '1m', startTime: now - 5 * 60 * 1000 }
    })
  });
  if (!r.ok) throw new Error(`HL API ${r.status}`);
  return await r.json(); // [{t, T, s, o, h, l, c, v}, ...]
}

function updatePriceHistory(candles) {
  if (!candles || !candles.length) return;
  const now = Date.now();
  
  for (const c of candles) {
    const ts = c.t || c.T;
    const price = parseFloat(c.c);
    // Dedupe by timestamp
    if (!priceHistory.find(p => p.ts === ts)) {
      priceHistory.push({ ts, price });
    }
  }
  
  // Also add current close as "now"
  const latest = candles[candles.length - 1];
  priceHistory.push({ ts: now, price: parseFloat(latest.c) });
  
  // Keep only last 10 minutes
  priceHistory = priceHistory.filter(p => now - p.ts < 600000);
  priceHistory.sort((a, b) => a.ts - b.ts);
}

function getPriceChange(windowSec) {
  if (priceHistory.length < 2) return null;
  const now = Date.now();
  const cutoff = now - windowSec * 1000;
  const older = priceHistory.filter(p => p.ts <= cutoff);
  const baseline = older.length ? older[older.length - 1] : priceHistory[0];
  const current = priceHistory[priceHistory.length - 1];
  return {
    from: baseline.price,
    to: current.price,
    change: (current.price - baseline.price) / baseline.price,
    windowSec,
  };
}

// --- Polymarket ---
async function getMarket(intervalSec, epochSec) {
  const prefix = intervalSec === 300 ? 'btc-updown-5m-' : 'btc-updown-15m-';
  const slug = prefix + epochSec;
  try {
    const r = await fetch(`${GAMMA_BASE}/events/slug/${slug}`);
    if (!r.ok) return null;
    const data = await r.json();
    if (!data || !data.markets || !data.markets.length) return null;
    const m = data.markets[0];
    return {
      slug,
      intervalSec,
      title: m.question,
      outcomes: JSON.parse(m.outcomes || '["Up","Down"]'),
      prices: JSON.parse(m.outcomePrices || '["0.5","0.5"]').map(Number),
      tokenIds: JSON.parse(m.clobTokenIds || '[]'),
      active: m.active,
      closed: m.closed,
      startEpoch: epochSec,
      endEpoch: epochSec + intervalSec,
      volume: parseFloat(m.volume || 0),
      liquidity: parseFloat(m.liquidity || 0),
    };
  } catch { return null; }
}

async function getCurrentMarkets() {
  const now = Math.floor(Date.now() / 1000);
  const epoch5 = Math.floor(now / 300) * 300;
  const epoch15 = Math.floor(now / 900) * 900;
  
  const [m5, m15] = await Promise.all([
    getMarket(300, epoch5),
    getMarket(900, epoch15),
  ]);
  
  return { m5, m15, now };
}

// --- Fair Value Model ---
// Given BTC price movement, estimate the fair probability of "Up" outcome
function estimateFairValue(priceChanges, market) {
  const timeLeft = market.endEpoch - Math.floor(Date.now() / 1000);
  const totalDuration = market.intervalSec;
  const elapsed = totalDuration - timeLeft;
  const elapsedFraction = Math.min(elapsed / totalDuration, 1);
  
  // Use 60-second and 120-second price changes
  const c60 = priceChanges['60s'];
  const c120 = priceChanges['120s'];
  
  if (!c60 && !c120) return null;
  
  const change = c60 ? c60.change : c120.change;
  const absChange = Math.abs(change);
  
  // The further into the candle we are, the more predictive current direction is
  // Early in candle: price could reverse. Late in candle: momentum likely holds.
  // 
  // Model: probability of Up = sigmoid(momentum_score)
  // momentum_score = price_change * time_weight
  // time_weight increases as we get further into the candle
  
  const timeWeight = 1 + elapsedFraction * 3; // 1x at start, 4x at end
  const momentumScore = change * timeWeight * 500; // scale to useful range
  
  // Sigmoid
  const probUp = 1 / (1 + Math.exp(-momentumScore));
  
  return {
    probUp,
    probDown: 1 - probUp,
    change,
    absChange,
    timeLeft,
    elapsedFraction,
    momentumScore,
  };
}

// --- Signal Detection ---
function detectDivergence(market, fairValue) {
  if (!market || !fairValue) return null;
  
  const marketProbUp = market.prices[0];
  const marketProbDown = market.prices[1];
  
  const divUp = fairValue.probUp - marketProbUp;   // positive = Up is underpriced
  const divDown = fairValue.probDown - marketProbDown; // positive = Down is underpriced
  
  // Pick the larger divergence
  const bestSide = Math.abs(divUp) > Math.abs(divDown) ? 'Up' : 'Down';
  const bestDiv = bestSide === 'Up' ? divUp : divDown;
  const sideIndex = bestSide === 'Up' ? 0 : 1;
  const marketPrice = market.prices[sideIndex];
  const fairPrice = bestSide === 'Up' ? fairValue.probUp : fairValue.probDown;
  
  return {
    side: bestSide,
    divergence: bestDiv,
    absDivergence: Math.abs(bestDiv),
    marketPrice,
    fairPrice,
    slug: market.slug,
    timeLeft: fairValue.timeLeft,
    change: fairValue.change,
  };
}

// --- Signals Storage ---
function loadSignals() {
  try { return JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf8')); }
  catch { return []; }
}

function saveSignal(signal) {
  const signals = loadSignals();
  signals.push(signal);
  // Keep last 500
  if (signals.length > 500) signals.splice(0, signals.length - 500);
  fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
}

// --- Commands ---
async function cmdScan() {
  console.log('🔍 Latency Arb — One-time Scan\n');
  
  // Fetch BTC data
  const candles = await fetchBTCCandles();
  updatePriceHistory(candles);
  
  const current = priceHistory[priceHistory.length - 1];
  console.log(`  BTC: $${current.price.toLocaleString()}`);
  
  const changes = {};
  for (const sec of [30, 60, 120, 180]) {
    const c = getPriceChange(sec);
    if (c) {
      changes[sec + 's'] = c;
      const pct = (c.change * 100).toFixed(3);
      const arrow = c.change > 0 ? '↑' : c.change < 0 ? '↓' : '→';
      console.log(`  ${sec}s: ${arrow} ${pct}% ($${c.from.toLocaleString()} → $${c.to.toLocaleString()})`);
    }
  }
  
  // Fetch markets
  const { m5, m15 } = await getCurrentMarkets();
  console.log();
  
  for (const [label, market] of [['5m', m5], ['15m', m15]]) {
    if (!market) { console.log(`  ${label}: ❌ no market`); continue; }
    
    const timeLeft = market.endEpoch - Math.floor(Date.now() / 1000);
    console.log(`  ${label}: Up ${(market.prices[0]*100).toFixed(1)}¢ / Down ${(market.prices[1]*100).toFixed(1)}¢  (${Math.floor(timeLeft/60)}m${timeLeft%60}s left, $${market.volume.toFixed(0)} vol)`);
    
    const fv = estimateFairValue(changes, market);
    if (fv) {
      console.log(`       Fair: Up ${(fv.probUp*100).toFixed(1)}% / Down ${(fv.probDown*100).toFixed(1)}%  (BTC ${(fv.change*100).toFixed(3)}%, ${(fv.elapsedFraction*100).toFixed(0)}% elapsed)`);
      
      const div = detectDivergence(market, fv);
      if (div && div.absDivergence >= MIN_DIVERGENCE) {
        console.log(`       🚨 DIVERGENCE: ${div.side} underpriced by ${(div.absDivergence*100).toFixed(1)}% (market: ${(div.marketPrice*100).toFixed(1)}¢, fair: ${(div.fairPrice*100).toFixed(1)}¢)`);
      } else if (div) {
        console.log(`       ✅ No significant divergence (${(div.absDivergence*100).toFixed(1)}%)`);
      }
    }
  }
}

async function cmdWatch() {
  const isDry = process.argv.includes('--dry');
  console.log('👁️  Latency Arb — Continuous Monitor');
  console.log(`   Mode: ${isDry ? 'DRY RUN' : 'LIVE'} | Poll: ${POLL_MS/1000}s | Min div: ${MIN_DIVERGENCE*100}%\n`);
  
  let lastSignalSlug = null;
  let signalCount = 0;
  
  while (true) {
    try {
      // Update BTC price
      const candles = await fetchBTCCandles();
      updatePriceHistory(candles);
      
      const current = priceHistory[priceHistory.length - 1];
      if (!current) { await sleep(POLL_MS); continue; }
      
      // Get price changes
      const changes = {};
      for (const sec of [30, 60, 120]) {
        const c = getPriceChange(sec);
        if (c) changes[sec + 's'] = c;
      }
      
      // Skip if BTC hasn't moved much
      const c60 = changes['60s'];
      if (!c60 || Math.abs(c60.change) < MIN_PRICE_MOVE * 0.5) {
        process.stdout.write(`\r  ${ts()} BTC $${current.price.toLocaleString()} | flat | signals: ${signalCount}    `);
        await sleep(POLL_MS);
        continue;
      }
      
      // Fetch markets
      const { m5, m15 } = await getCurrentMarkets();
      
      for (const [label, market] of [['5m', m5], ['15m', m15]]) {
        if (!market || market.closed) continue;
        
        const fv = estimateFairValue(changes, market);
        if (!fv) continue;
        
        const div = detectDivergence(market, fv);
        if (!div || div.absDivergence < MIN_DIVERGENCE) continue;
        
        // Avoid duplicate signals for same market
        const sigKey = `${market.slug}-${div.side}`;
        if (sigKey === lastSignalSlug) continue;
        lastSignalSlug = sigKey;
        signalCount++;
        
        const shares = Math.floor(TRADE_SIZE / div.marketPrice);
        const expectedProfit = shares * (div.fairPrice - div.marketPrice);
        
        console.log(`\n  🚨 ${ts()} SIGNAL #${signalCount}`);
        console.log(`     Market: ${label} ${market.slug}`);
        console.log(`     BTC: $${current.price.toLocaleString()} (60s: ${(c60.change*100).toFixed(3)}%)`);
        console.log(`     Side: BUY ${div.side} @ ${(div.marketPrice*100).toFixed(1)}¢ (fair: ${(div.fairPrice*100).toFixed(1)}¢)`);
        console.log(`     Divergence: ${(div.absDivergence*100).toFixed(1)}%`);
        console.log(`     Theoretical: ${shares} shares, cost $${(shares*div.marketPrice).toFixed(2)}, EV +$${expectedProfit.toFixed(2)}`);
        console.log(`     Time left: ${Math.floor(div.timeLeft/60)}m${div.timeLeft%60}s`);
        
        const signal = {
          timestamp: new Date().toISOString(),
          market: label,
          slug: market.slug,
          side: div.side,
          marketPrice: div.marketPrice,
          fairPrice: div.fairPrice,
          divergence: div.absDivergence,
          btcPrice: current.price,
          btcChange60s: c60.change,
          shares,
          cost: shares * div.marketPrice,
          expectedProfit,
          timeLeft: div.timeLeft,
          resolved: false,
          dryRun: isDry,
        };
        saveSignal(signal);
      }
      
      // Periodic status line
      const arrow = c60.change > 0 ? '↑' : '↓';
      process.stdout.write(`\r  ${ts()} BTC $${current.price.toLocaleString()} ${arrow}${(Math.abs(c60.change)*100).toFixed(3)}% | signals: ${signalCount}    `);
      
      // Check resolutions periodically
      await resolveSignals();
      
    } catch (e) {
      console.log(`\n  ⚠️ Error: ${e.message}`);
    }
    
    await sleep(POLL_MS);
  }
}

async function resolveSignals() {
  const signals = loadSignals();
  let updated = false;
  
  for (const s of signals) {
    if (s.resolved) continue;
    
    const now = Math.floor(Date.now() / 1000);
    const endEpoch = parseInt(s.slug.split('-').pop()) + (s.market === '5m' ? 300 : 900);
    
    // Only check if market should be over
    if (now < endEpoch + 60) continue;
    
    const intervalSec = s.market === '5m' ? 300 : 900;
    const epochSec = parseInt(s.slug.split('-').pop());
    const m = await getMarket(intervalSec, epochSec);
    
    if (!m || !m.closed) continue;
    
    const upWon = m.prices[0] >= 0.9;
    const won = (s.side === 'Up' && upWon) || (s.side === 'Down' && !upWon);
    
    s.resolved = true;
    s.won = won;
    s.payout = won ? s.shares : 0;
    s.profit = won ? s.shares - s.cost : -s.cost;
    updated = true;
    
    const emoji = won ? '💰' : '💀';
    console.log(`\n  ${emoji} RESOLVED: ${s.slug} | ${s.side} ${s.shares}sh @ ${(s.marketPrice*100).toFixed(0)}¢ → ${won ? 'WON' : 'LOST'} (${won ? '+' : ''}$${s.profit.toFixed(2)})`);
  }
  
  if (updated) {
    fs.writeFileSync(SIGNALS_FILE, JSON.stringify(signals, null, 2));
  }
}

async function cmdHistory() {
  // Resolve any pending
  await resolveSignals();
  
  const signals = loadSignals();
  if (!signals.length) { console.log('No signals yet. Run "watch --dry" to start collecting.'); return; }
  
  console.log('📜 Latency Arb Signal History\n');
  
  let totalPnL = 0, wins = 0, losses = 0, pending = 0;
  
  for (const s of signals.slice(-30)) {
    const status = !s.resolved ? '⏳' : (s.won ? '✅' : '❌');
    const pnl = s.resolved ? (s.won ? `+$${s.profit.toFixed(2)}` : `-$${Math.abs(s.profit).toFixed(2)}`) : '';
    console.log(`  ${status} ${s.timestamp.slice(5,19)} | ${s.market.padEnd(3)} ${s.side.padEnd(4)} ${s.shares}sh @ ${(s.marketPrice*100).toFixed(0)}¢ (fair: ${(s.fairPrice*100).toFixed(0)}¢) div: ${(s.divergence*100).toFixed(1)}% | BTC ${(s.btcChange60s*100).toFixed(2)}% | ${pnl}`);
    
    if (s.resolved) {
      totalPnL += s.profit;
      if (s.won) wins++; else losses++;
    } else pending++;
  }
  
  const total = wins + losses;
  console.log(`\n📊 Summary: ${wins}W / ${losses}L / ${pending}P | WR: ${total > 0 ? ((wins/total)*100).toFixed(0) : '-'}% | PnL: ${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`);
  
  if (total > 0) {
    const avgWin = wins > 0 ? signals.filter(s => s.won).reduce((a, s) => a + s.profit, 0) / wins : 0;
    const avgLoss = losses > 0 ? signals.filter(s => s.resolved && !s.won).reduce((a, s) => a + s.profit, 0) / losses : 0;
    console.log(`   Avg win: +$${avgWin.toFixed(2)} | Avg loss: $${avgLoss.toFixed(2)}`);
  }
}

// --- Util ---
function ts() { return new Date().toLocaleTimeString('en-US', { hour12: false }); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// --- Main ---
const cmd = process.argv[2] || 'scan';
const handlers = { scan: cmdScan, watch: cmdWatch, history: cmdHistory };

if (!handlers[cmd]) {
  console.log('Usage: node latency_arb.cjs [scan|watch|history]');
  console.log('  scan          One-time divergence check');
  console.log('  watch --dry   Continuous monitoring (dry run)');
  console.log('  history       Past signals & outcomes');
  process.exit(1);
}

handlers[cmd]().catch(e => { console.error('Fatal:', e.message); process.exit(1); });