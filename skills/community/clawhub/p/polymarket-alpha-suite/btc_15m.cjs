#!/usr/bin/env node
/**
 * BTC 15-Minute Up/Down Scalper for Polymarket
 * 
 * Finds the current/next 15-min BTC market, reads BTC momentum,
 * places a trade on the likely direction, and monitors for resolution.
 * 
 * Usage:
 *   node btc_15m.cjs scan          # Show current & upcoming markets
 *   node btc_15m.cjs scan --5m     # Show 5-min markets instead
 *   node btc_15m.cjs trade --dry   # Dry-run trade current market
 *   node btc_15m.cjs watch --dry   # Continuous dry-run trading loop
 *   node btc_15m.cjs history       # Show past trades
 */

const fs = require('fs');
const path = require('path');

// --- Config ---
// Configurable: 5m or 15m
const MODE = process.argv.includes('--5m') ? '5m' : '15m';
const INTERVAL_SEC = MODE === '5m' ? 5 * 60 : 15 * 60;
const SLUG_PREFIX = MODE === '5m' ? 'btc-updown-5m-' : 'btc-updown-15m-';
const GAMMA_BASE = 'https://gamma-api.polymarket.com';
const DATA_DIR = path.join(__dirname, 'data');
const TRADES_FILE = path.join(DATA_DIR, `btc_${MODE}_trades.json`);
const MAX_TRADE_SIZE = 10; // $10 max per trade
const MIN_EDGE = 0.05; // 5% minimum edge required
const ENTRY_WINDOW_SEC = MODE === '5m' ? 2.5 * 60 : 8 * 60; // 2.5 min for 5m, 8 min for 15m

// Check for environment variables
const POLY_PK = process.env.POLY_PK || process.env.POLYMARKET_PRIVATE_KEY;
const POLY_FUNDER = process.env.POLY_FUNDER || process.env.POLYMARKET_FUNDER;

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// --- Helpers ---
function getCurrentEpoch() {
  return Math.floor(Date.now() / 1000);
}

function getIntervalStart(epochSec) {
  return Math.floor(epochSec / INTERVAL_SEC) * INTERVAL_SEC;
}

function getMarketSlug(epochSec) {
  return SLUG_PREFIX + getIntervalStart(epochSec);
}

async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) return null;
  return r.json();
}

async function getMarket(epochSec) {
  const slug = SLUG_PREFIX + epochSec;
  const data = await fetchJSON(`${GAMMA_BASE}/events/slug/${slug}`);
  if (!data || !data.markets || !data.markets.length) return null;
  const m = data.markets[0];
  return {
    slug,
    title: m.question,
    conditionId: m.conditionId,
    outcomes: JSON.parse(m.outcomes || '["Up","Down"]'),
    prices: JSON.parse(m.outcomePrices || '["0.5","0.5"]').map(Number),
    tokenIds: JSON.parse(m.clobTokenIds || '[]'),
    active: m.active,
    closed: m.closed,
    endDate: m.endDate,
    volume: parseFloat(m.volume || 0),
    liquidity: parseFloat(m.liquidity || 0),
    startEpoch: epochSec,
    endEpoch: epochSec + INTERVAL_SEC,
  };
}

async function getBTCMomentum() {
  try {
    // Use Hyperliquid for real-time BTC data (no rate limit)
    const r = await fetch('https://api.hyperliquid.xyz/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'candleSnapshot', req: { coin: 'BTC', interval: '5m', startTime: Date.now() - 3600000 } })
    });
    if (!r.ok) throw new Error('HL API error');
    const candles = await r.json(); // [{t, o, h, l, c, v}, ...]
    if (!candles || candles.length < 6) return { direction: null, confidence: 0, reason: 'insufficient candles' };
    
    const recent = candles.slice(-6); // last 30 min of 5-min candles
    const current = parseFloat(recent[recent.length - 1].c);
    const fifteenMinAgo = parseFloat(recent[recent.length - 3]?.c || recent[0].c);
    const thirtyMinAgo = parseFloat(recent[0].c);
    
    const change15m = (current - fifteenMinAgo) / fifteenMinAgo;
    const change30m = (current - thirtyMinAgo) / thirtyMinAgo;
    
    // EMA-like weighting: recent matters more
    const momentum = change15m * 0.7 + change30m * 0.3;
    const direction = momentum > 0 ? 'Up' : 'Down';
    
    // Confidence based on strength of move
    const absChange = Math.abs(change15m);
    let confidence;
    if (absChange > 0.005) confidence = 0.7;       // >0.5% in 15m = strong
    else if (absChange > 0.003) confidence = 0.55;  // >0.3% = good
    else if (absChange > 0.002) confidence = 0.4;   // >0.2% = moderate
    else if (absChange > 0.001) confidence = 0.25;  // >0.1% = weak
    else {
      // Flat = structural "Up" bias (Chainlink rounds to same price = Up wins)
      return {
        direction: 'Up',
        confidence: 0.15,
        change15m: (change15m * 100).toFixed(3) + '%',
        change30m: (change30m * 100).toFixed(3) + '%',
        currentPrice: current,
        reason: `FLAT BIAS (15m: ${(change15m * 100).toFixed(3)}%) → Up`
      };
    }
    
    return {
      direction,
      confidence,
      change15m: (change15m * 100).toFixed(3) + '%',
      change30m: (change30m * 100).toFixed(3) + '%',
      currentPrice: current,
      reason: `15m: ${change15m > 0 ? '+' : ''}${(change15m * 100).toFixed(3)}%, 30m: ${change30m > 0 ? '+' : ''}${(change30m * 100).toFixed(3)}%`
    };
  } catch (e) {
    return { direction: null, confidence: 0, reason: e.message };
  }
}

function loadTrades() {
  try { return JSON.parse(fs.readFileSync(TRADES_FILE, 'utf8')); }
  catch { return []; }
}

function saveTrade(trade) {
  const trades = loadTrades();
  trades.push(trade);
  fs.writeFileSync(TRADES_FILE, JSON.stringify(trades, null, 2));
}

// --- Commands ---
async function cmdScan() {
  const now = getCurrentEpoch();
  const currentStart = getIntervalStart(now);
  const prevStart = currentStart - INTERVAL_SEC;
  const nextStart = currentStart + INTERVAL_SEC;
  
  console.log(`🔍 Scanning BTC ${MODE} markets...\n`);
  
  for (const ts of [prevStart, currentStart, nextStart]) {
    const m = await getMarket(ts);
    if (!m) { console.log(`  ❌ ${SLUG_PREFIX}${ts} — not found`); continue; }
    
    const timeLeft = m.endEpoch - now;
    const status = m.closed ? '🔴 CLOSED' : (timeLeft < 0 ? '⏰ RESOLVING' : `🟢 ${Math.floor(timeLeft/60)}m ${timeLeft%60}s left`);
    
    console.log(`  ${status} | ${m.title}`);
    console.log(`    Up: ${(m.prices[0]*100).toFixed(1)}¢  Down: ${(m.prices[1]*100).toFixed(1)}¢`);
    console.log(`    Vol: $${m.volume.toFixed(0)}  Liq: $${m.liquidity.toFixed(0)}`);
    console.log(`    Slug: ${m.slug}`);
    console.log();
  }
  
  // Show momentum
  const mom = await getBTCMomentum();
  console.log(`📊 BTC Momentum: ${mom.direction || 'unclear'} (${mom.reason})`);
  if (mom.currentPrice) console.log(`   Price: $${mom.currentPrice.toLocaleString()}`);
}

async function cmdTrade() {
  const now = getCurrentEpoch();
  const currentStart = getIntervalStart(now);
  const timeIntoCandle = now - currentStart;
  const dryRun = process.argv.includes('--dry') || !POLY_PK;
  
  // Only trade within the entry window
  if (timeIntoCandle > ENTRY_WINDOW_SEC) {
    console.log(`⏰ Too late in candle (${Math.floor(timeIntoCandle/60)}m in, max ${ENTRY_WINDOW_SEC/60}m). Waiting for next.`);
    return { traded: false, reason: 'too_late' };
  }
  
  const market = await getMarket(currentStart);
  if (!market || market.closed) {
    console.log('❌ No active market found');
    return { traded: false, reason: 'no_market' };
  }
  
  // Get momentum signal
  const mom = await getBTCMomentum();
  if (!mom.direction) {
    console.log('❌ No momentum signal:', mom.reason);
    return { traded: false, reason: 'no_signal' };
  }
  
  // Determine which side to buy
  const sideIndex = mom.direction === 'Up' ? 0 : 1;
  const marketPrice = market.prices[sideIndex];
  
  // Calculate edge: our confidence vs market price
  // If we think Up with 60% confidence but market prices Up at 50¢, edge = 10%
  const ourProb = 0.5 + mom.confidence / 2; // convert confidence to probability
  const edge = ourProb - marketPrice;
  
  console.log(`\n📊 Analysis for ${market.title}:`);
  console.log(`   Momentum: ${mom.direction} (${mom.reason})`);
  console.log(`   Market prices: Up ${(market.prices[0]*100).toFixed(1)}¢ / Down ${(market.prices[1]*100).toFixed(1)}¢`);
  console.log(`   Our estimate: ${mom.direction} @ ${(ourProb*100).toFixed(1)}%`);
  console.log(`   Edge: ${(edge*100).toFixed(1)}%`);
  console.log(`   Time left: ${Math.floor((market.endEpoch - now)/60)}m ${(market.endEpoch - now)%60}s`);
  
  if (edge < MIN_EDGE) {
    console.log(`   ⚠️ Edge too small (${(edge*100).toFixed(1)}% < ${MIN_EDGE*100}% min). SKIP.`);
    return { traded: false, reason: 'low_edge', edge };
  }
  
  // Size based on edge (Kelly-lite: bet more when edge is bigger)
  const kellyFraction = Math.min(edge / (1 - marketPrice), 0.25); // cap at 25% of max
  const tradeSize = Math.min(Math.max(kellyFraction * MAX_TRADE_SIZE * 4, 2), MAX_TRADE_SIZE);
  const shares = Math.floor(tradeSize / marketPrice);
  
  console.log(`\n   🎯 TRADE: BUY ${shares} ${mom.direction} @ ${(marketPrice*100).toFixed(1)}¢ ($${(shares * marketPrice).toFixed(2)})`);
  
  if (dryRun) {
    console.log('   📝 DRY RUN — not placing order (use environment variables for live trading)');
    const trade = {
      timestamp: new Date().toISOString(),
      slug: market.slug,
      side: mom.direction,
      shares,
      price: marketPrice,
      cost: shares * marketPrice,
      edge,
      momentum: mom,
      dryRun: true,
      resolved: false,
    };
    saveTrade(trade);
    return { traded: true, dryRun: true, trade };
  }
  
  console.log('   ⚠️ Live trading requires POLY_PK environment variable');
  console.log('   📝 Recording as dry run');
  
  const trade = {
    timestamp: new Date().toISOString(),
    slug: market.slug,
    side: mom.direction,
    shares,
    price: marketPrice,
    cost: shares * marketPrice,
    edge,
    momentum: mom,
    dryRun: true,
    resolved: false,
  };
  saveTrade(trade);
  return { traded: true, dryRun: true, trade };
}

async function cmdWatch() {
  console.log(`👁️ BTC ${MODE} Scalper — Continuous Mode`);
  console.log(`   Max trade: $${MAX_TRADE_SIZE} | Min edge: ${MIN_EDGE*100}% | Entry window: ${ENTRY_WINDOW_SEC/60}m\n`);
  
  const isDryRun = !POLY_PK || process.argv.includes('--dry');
  if (isDryRun) console.log('   ⚠️ DRY RUN MODE (no POLY_PK env variable or --dry flag)\n');
  
  let lastTradedSlug = null;
  
  while (true) {
    const now = getCurrentEpoch();
    const currentStart = getIntervalStart(now);
    const currentSlug = SLUG_PREFIX + currentStart;
    
    if (currentSlug !== lastTradedSlug) {
      console.log(`\n--- New candle: ${new Date(currentStart * 1000).toLocaleString()} ---`);
      const result = await cmdTrade();
      if (result.traded) lastTradedSlug = currentSlug;
    }
    
    // Check if any past trades resolved
    await checkResolutions();
    
    // Wait 30 seconds
    await new Promise(r => setTimeout(r, 30000));
  }
}

async function checkResolutions() {
  const trades = loadTrades();
  let updated = false;
  
  for (const t of trades) {
    if (t.resolved) continue;
    const epochSec = parseInt(t.slug.replace(SLUG_PREFIX, ''));
    const m = await getMarket(epochSec);
    if (!m) continue;
    
    if (m.closed) {
      // Check outcome
      const upPrice = m.prices[0];
      const won = (t.side === 'Up' && upPrice >= 0.99) || (t.side === 'Down' && upPrice <= 0.01);
      t.resolved = true;
      t.won = won;
      t.payout = won ? t.shares : 0;
      t.profit = won ? t.shares - t.cost : -t.cost;
      updated = true;
      
      const emoji = won ? '💰' : '💀';
      console.log(`${emoji} ${t.slug}: ${t.side} ${t.shares}sh @ ${(t.price*100).toFixed(0)}¢ → ${won ? 'WON' : 'LOST'} (${won ? '+' : ''}$${t.profit.toFixed(2)})`);
    }
  }
  
  if (updated) {
    fs.writeFileSync(TRADES_FILE, JSON.stringify(trades, null, 2));
  }
}

async function cmdHistory() {
  const trades = loadTrades();
  if (!trades.length) { console.log('No trades yet.'); return; }
  
  console.log(`📜 BTC ${MODE} Trade History\n`);
  
  let totalPnL = 0, wins = 0, losses = 0, pending = 0;
  
  for (const t of trades.slice(-20)) {
    const status = !t.resolved ? '⏳' : (t.won ? '✅' : '❌');
    console.log(`  ${status} ${t.timestamp.slice(5,16)} | ${t.side.padEnd(4)} ${t.shares}sh @ ${(t.price*100).toFixed(0)}¢ ($${t.cost.toFixed(2)}) | edge: ${(t.edge*100).toFixed(1)}% | ${t.dryRun ? 'DRY' : 'LIVE'} ${t.resolved ? (t.won ? `+$${t.profit.toFixed(2)}` : `-$${Math.abs(t.profit).toFixed(2)}`) : ''}`);
    
    if (t.resolved) {
      totalPnL += t.profit;
      if (t.won) wins++; else losses++;
    } else pending++;
  }
  
  console.log(`\n📊 Summary: ${wins}W / ${losses}L / ${pending}P | WR: ${wins+losses > 0 ? ((wins/(wins+losses))*100).toFixed(0) : 0}% | PnL: ${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`);
}

// --- Main ---
const cmd = process.argv[2] || 'scan';
const handlers = { scan: cmdScan, trade: cmdTrade, watch: cmdWatch, history: cmdHistory };

if (!handlers[cmd]) {
  console.log(`Usage: node btc_15m.cjs [scan|trade|watch|history] [--5m] [--dry]`);
  console.log('  scan          Show current & upcoming markets');
  console.log('  trade --dry   Dry-run trade current market');
  console.log('  watch --dry   Continuous dry-run trading loop');
  console.log('  history       Show past trades');
  console.log('  --5m          Use 5-minute markets instead of 15-minute');
  console.log('  --dry         Force dry-run mode');
  process.exit(1);
}

handlers[cmd]().catch(e => { console.error('Fatal:', e.message); process.exit(1); });