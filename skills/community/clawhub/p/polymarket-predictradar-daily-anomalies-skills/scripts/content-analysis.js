/**
 * content-analysis.js
 * Polymarket Daily Anomaly Detection — 3 signal types + JSON export
 *
 * Signal 1: Insider Watch (suspicious new-wallet activity)  — daily, ≤50
 * Signal 2: Whale Wars   (opposing whale bets)              — daily, ≤15
 * Signal 3: Black Swan    (probability shocks)              — 48h,   ≤30
 *
 * Usage:
 *   MCP_URL=https://api.predictradar.ai node content-analysis.js
 *
 * Requires: polymarket-data-layer shared data layer (mcp-client, gamma-client)
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Shared data layer ────────────────────────────────────────
const mcp   = require('../../polymarket-data-layer/scripts/mcp-client');
const gamma = require('../../polymarket-data-layer/scripts/gamma-client');

// ── Configuration ────────────────────────────────────────────
const CFG = {
  base: {
    min_volume_24h: 50000,
    min_trades_24h: 20,
  },
  insider: {
    max_wallet_trades: 5,
    min_trade_usd:  1000,
    max_buy_price:  0.50,
    min_size_vs_avg: 2.0,
    limit:           50,
  },
  whale_wars: {
    min_market_vol: 200000,
    min_wallet_usd:  25000,
    limit:            15,
  },
  black_swan: {
    min_abs_change:  0.70,
    min_start_price: 0.05,
    max_end_price:   0.95,
    min_vol_2h:   100000,
    lookback_days:     2,
    limit:            30,
  },
};

// ── Domain classification (same rules as tag-all-domains.js) ──
const DOMAIN_LABELS = {
  POL: 'Politics', GEO: 'Geopolitics', FIN: 'Finance',
  CRY: 'Crypto',   SPT: 'Sports',      TEC: 'Technology',
  CUL: 'Culture',  GEN: 'General',
};

const CAT_MAP = {
  'us-current-affairs': 'POL', 'politics': 'POL',
  'global politics': 'GEO', 'global-politics': 'GEO', 'ukraine & russia': 'GEO',
  'business': 'FIN', 'economics': 'FIN', 'finance': 'FIN',
  'crypto': 'CRY', 'nfts': 'CRY', 'defi': 'CRY',
  'sports': 'SPT', 'nba playoffs': 'SPT', 'nba': 'SPT', 'nfl': 'SPT',
  'olympics': 'SPT', 'chess': 'SPT', 'poker': 'SPT',
  'tech': 'TEC', 'science': 'TEC', 'space': 'TEC',
  'pop-culture': 'CUL', 'pop-culture ': 'CUL', 'art': 'CUL',
};

const Q_RULES = [
  [/\b(trump|biden|harris|clinton|obama|election|president|congress|senate|democrat|republican|white house|tariff|gov.shutdown|vp |cabinet|inaugur|ballot|midterm|primary|nato|un |imf )\b/i, 'POL'],
  [/\b(nfl|nba|ufc|soccer|premier.?league|world.?cup|super.?bowl|wimbledon|us.?open|masters|pga|formula.?1|f1 |formula 1|moto.?gp|nascar|basketball|football|baseball|hockey|tennis|boxing|mma|chess|poker|esport|olympic|world.?series|champions.?league|euro.?cup|copa|afc|nfc|playoffs?|championship|t20|cricket|ipl|ashes)\b/i, 'SPT'],
  [/\b(ukraine|russia|china|israel|iran(?:ian)?|hamas|hezbollah|nato|war|ceasefire|sanction|xi |putin|zelensky|middle.?east|taiwan|venezuela|geopolit|kim jong|north korea|south korea|india|pakistan|saudi|cartel|border|migrant|refugee|regime)\b/i, 'GEO'],
  [/\b(fed |federal reserve|interest.?rate|rate.?cut|s&p|stock|nasdaq|dow |ipo |earnings|gdp|inflation|recession|oil.?price|crude|gold.?price|commodit|treasury|bond.?yield|cpi |ppi |jobs.?report|unemployment|fomc)\b/i, 'FIN'],
  [/\b(bitcoin|btc |eth |ethereum|crypto|solana|sol |doge|xrp|bnb |chainlink|polygon|avalanche|defi |nft |blockchain|coinbase|binance|sec.+crypto|stablecoin|altcoin|halving|layer.?2|web3)\b/i, 'CRY'],
  [/\b(ai |artificial.?intelligence|openai|chatgpt|gpt.?\d|gemini|claude |anthropic|spacex|nasa|starship|rocket|elon.?musk.+tweet|twitter|x\.com|apple|google|microsoft|meta |tesla|nvidia|semiconductor|quantum|cyber|hack|data.?breach)\b/i, 'TEC'],
  [/\b(oscar|grammy|golden.?globe|academy.?award|bafta|emmy|vma|movie|film|box.?office|album|billboard|chart|taylor.?swift|beyonce|kanye|celebrity|kim.?kardashian|reality.?tv|tiktok.+ban|super.?bowl.+halftime)\b/i, 'CUL'],
];

function marketToDomain(question, category) {
  const q = (question || '').toLowerCase();
  for (const [re, d] of Q_RULES) {
    if (re.test(q)) return d;
  }
  if (category) {
    const c = category.trim().toLowerCase();
    if (CAT_MAP[c]) return CAT_MAP[c];
  }
  return null;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Helpers ──────────────────────────────────────────────────
function sep(title) {
  console.log('\n' + '='.repeat(72));
  console.log('  ' + title);
  console.log('='.repeat(72));
}

function printTable(rows, fields) {
  if (!rows?.length) { console.log('  (no results)'); return; }
  const cols = fields || Object.keys(rows[0]);
  const widths = cols.map(k =>
    Math.max(k.length, ...rows.map(r => String(r[k] ?? '').length))
  );
  console.log('  ' + cols.map((k, i) => k.padEnd(widths[i])).join(' | '));
  console.log('  ' + widths.map(w => '-'.repeat(w)).join('-+-'));
  for (const row of rows)
    console.log('  ' + cols.map((k, i) => String(row[k] ?? '').padEnd(widths[i])).join(' | '));
  console.log(`\n  Total: ${rows.length} rows`);
}

// ── Active markets (shared filter) ───────────────────────────
async function getActiveMarkets() {
  process.stdout.write(`  [base] Active markets (vol>=$${(CFG.base.min_volume_24h/1000).toFixed(0)}k, trades>=${CFG.base.min_trades_24h})...`);
  const rows = await mcp.queryWithRetry(`
    SELECT
      market_id,
      count()          AS trades_24h,
      sum(usd_amount)  AS volume_24h,
      avg(usd_amount)  AS avg_trade_size
    FROM trades
    WHERE traded_at >= now() - INTERVAL 24 HOUR
      AND type = 'trade'
      AND usd_amount > 0
      AND market_id IS NOT NULL
    GROUP BY market_id
    HAVING volume_24h >= ${CFG.base.min_volume_24h}
       AND trades_24h >= ${CFG.base.min_trades_24h}
    ORDER BY volume_24h DESC
    LIMIT 3000
  `, { maxRows: 3000, retries: 3 });
  console.log(` ${rows.length} markets`);
  return rows;
}

// ── Signal 1: Insider Watch ──────────────────────────────────
async function runInsiderWatch(activeMarkets) {
  sep('Signal 1: Insider Watch');
  const C = CFG.insider;
  console.log(`  Criteria: new wallet (trades<=${C.max_wallet_trades}) | buy>=$${C.min_trade_usd.toLocaleString()} | price<=${C.max_buy_price} | size>=${C.min_size_vs_avg}x avg`);

  if (!activeMarkets.length) { console.log('  No active markets'); return []; }

  const marketMap = new Map(activeMarkets.map(r => [r.market_id, r]));
  const activeIds = activeMarkets.map(r => `'${r.market_id}'`).join(',');

  // Q1: 24h buys matching criteria
  process.stdout.write(`  [Q1] 24h buys (price<=${C.max_buy_price}, amount>=$${C.min_trade_usd.toLocaleString()})...`);
  const buys = await mcp.queryWithRetry(`
    SELECT
      market_id,
      wallet_address,
      price        AS buy_price,
      usd_amount   AS trade_size,
      traded_at
    FROM trades
    WHERE traded_at >= now() - INTERVAL 24 HOUR
      AND type = 'trade'
      AND side = 'buy'
      AND outcome_index = 0
      AND price <= ${C.max_buy_price}
      AND price > 0
      AND usd_amount >= ${C.min_trade_usd}
      AND market_id IN (${activeIds})
      AND wallet_address IS NOT NULL
      AND wallet_address != ''
    ORDER BY usd_amount DESC
    LIMIT 3000
  `, { maxRows: 3000, retries: 3 });
  console.log(` ${buys.length} rows`);

  if (!buys.length) return [];

  // Q2: Historical trade counts for these wallets
  const walletSet = [...new Set(buys.map(r => r.wallet_address))];
  const walletIn  = walletSet.map(w => `'${w}'`).join(',');
  process.stdout.write(`  [Q2] ${walletSet.length} wallets historical trade count...`);
  const walletCounts = await mcp.queryWithRetry(`
    SELECT wallet_address, count() AS total_trades
    FROM trades
    WHERE type = 'trade'
      AND wallet_address IN (${walletIn})
    GROUP BY wallet_address
  `, { maxRows: 5000, retries: 3 });
  console.log(` done (${walletCounts.length} rows)`);

  const wcMap = new Map(walletCounts.map(r => [r.wallet_address, Number(r.total_trades)]));

  // Filter
  const allPassed = [];
  for (const b of buys) {
    const totalTrades = wcMap.get(b.wallet_address) ?? 9999;
    if (totalTrades > C.max_wallet_trades) continue;

    const mkt = marketMap.get(b.market_id);
    if (!mkt) continue;

    const avgSize   = parseFloat(mkt.avg_trade_size);
    const tradeSize = parseFloat(b.trade_size);
    if (tradeSize < C.min_size_vs_avg * avgSize) continue;

    allPassed.push({
      market_id_short: b.market_id.slice(0, 16) + '...',
      wallet_short:    b.wallet_address.slice(0, 10) + '...',
      buy_price:       +parseFloat(b.buy_price).toFixed(4),
      trade_usd:       Math.round(tradeSize),
      avg_mkt_usd:     Math.round(avgSize),
      x_avg:           +(tradeSize / avgSize).toFixed(1),
      wallet_trades:   totalTrades,
      traded_at:       b.traded_at,
      market_id:       b.market_id,
      wallet_address:  b.wallet_address,
    });
  }

  allPassed.sort((a, b) => b.trade_usd - a.trade_usd);

  // Multi-wallet aggregation: same market, multiple new wallets
  const byMarket = new Map();
  for (const r of allPassed) {
    if (!byMarket.has(r.market_id)) byMarket.set(r.market_id, []);
    byMarket.get(r.market_id).push(r);
  }
  const aggregated = [];
  for (const [mid, trades] of byMarket) {
    if (trades.length >= 2) {
      const totalUsd = trades.reduce((s, t) => s + t.trade_usd, 0);
      const avgPrice = trades.reduce((s, t) => s + t.buy_price * t.trade_usd, 0) / totalUsd;
      const wallets = trades.map(t => t.wallet_address);
      aggregated.push({
        ...trades[0],
        wallet_count:   trades.length,
        wallets,
        wallet_address: wallets[0],
        wallet_short:   `${trades.length} new addresses`,
        trade_usd:      totalUsd,
        buy_price:      +avgPrice.toFixed(4),
        avg_buy_price:  +avgPrice.toFixed(4),
        x_avg:          +(totalUsd / trades[0].avg_mkt_usd).toFixed(1),
        is_aggregated:  true,
      });
    } else {
      trades[0].wallet_count = 1;
      trades[0].is_aggregated = false;
      aggregated.push(trades[0]);
    }
  }
  aggregated.sort((a, b) => b.trade_usd - a.trade_usd);

  const final = aggregated.slice(0, C.limit);
  console.log(`\n  Filtered: ${allPassed.length} -> top ${final.length}`);
  printTable(final, ['wallet_short', 'buy_price', 'trade_usd', 'avg_mkt_usd', 'x_avg', 'wallet_trades', 'market_id_short']);

  const byStep = {
    total_buys:     buys.length,
    after_new_addr: buys.filter(b => (wcMap.get(b.wallet_address) ?? 9999) <= C.max_wallet_trades).length,
    after_size_mul: allPassed.length,
  };
  console.log(`\n  [diag] total_buys=${byStep.total_buys} -> new_addr=${byStep.after_new_addr} -> size_filter=${byStep.after_size_mul}`);

  return final;
}

// ── Signal 2: Whale Wars ─────────────────────────────────────
async function runWhaleWars() {
  sep('Signal 2: Whale Wars');
  const C = CFG.whale_wars;
  console.log(`  Criteria: same market | each side >=$${(C.min_wallet_usd/1000).toFixed(0)}k | opposing | 24h | market vol >=$${(C.min_market_vol/1000).toFixed(0)}k`);

  // Q1: High-volume markets
  process.stdout.write(`  [Q1] Markets (vol>=$${(C.min_market_vol/1000).toFixed(0)}k, 24h)...`);
  const bigMarkets = await mcp.queryWithRetry(`
    SELECT
      market_id,
      sum(usd_amount) AS volume_24h,
      count()         AS trades_24h
    FROM trades
    WHERE traded_at >= now() - INTERVAL 24 HOUR
      AND type = 'trade'
      AND market_id IS NOT NULL
      AND usd_amount > 0
    GROUP BY market_id
    HAVING volume_24h >= ${C.min_market_vol}
    ORDER BY volume_24h DESC
    LIMIT 300
  `, { maxRows: 300, retries: 3 });
  console.log(` ${bigMarkets.length} markets`);

  if (!bigMarkets.length) { console.log('  No qualifying markets'); return []; }

  const bigMarketMap = new Map(bigMarkets.map(r => [r.market_id, r]));
  const bigIds = bigMarkets.map(r => `'${r.market_id}'`).join(',');

  // Q2: Per-wallet buy/sell totals
  process.stdout.write('  [Q2] Per-wallet buy/sell aggregation...');
  const walletSides = await mcp.queryWithRetry(`
    SELECT
      market_id,
      wallet_address,
      sumIf(usd_amount, side = 'buy')  AS buy_total,
      sumIf(usd_amount, side = 'sell') AS sell_total,
      count()                          AS trade_count
    FROM trades
    WHERE traded_at >= now() - INTERVAL 24 HOUR
      AND type = 'trade'
      AND market_id IN (${bigIds})
      AND wallet_address IS NOT NULL
      AND usd_amount > 0
    GROUP BY market_id, wallet_address
    HAVING buy_total >= ${C.min_wallet_usd} OR sell_total >= ${C.min_wallet_usd}
    ORDER BY market_id, greatest(buy_total, sell_total) DESC
    LIMIT 3000
  `, { maxRows: 3000, retries: 3 });
  console.log(` ${walletSides.length} rows`);

  // Find opposing pairs
  const byMarket = new Map();
  for (const r of walletSides) {
    if (!byMarket.has(r.market_id)) byMarket.set(r.market_id, []);
    byMarket.get(r.market_id).push(r);
  }

  const pairs = [];
  for (const [marketId, wallets] of byMarket) {
    const buyers  = wallets
      .filter(w => parseFloat(w.buy_total) >= C.min_wallet_usd && parseFloat(w.buy_total) > parseFloat(w.sell_total))
      .sort((a, b) => parseFloat(b.buy_total) - parseFloat(a.buy_total));
    const sellers = wallets
      .filter(w => parseFloat(w.sell_total) >= C.min_wallet_usd && parseFloat(w.sell_total) > parseFloat(w.buy_total))
      .sort((a, b) => parseFloat(b.sell_total) - parseFloat(a.sell_total));

    if (!buyers.length || !sellers.length) continue;

    const A      = buyers[0];
    const B      = sellers[0];
    const mkt    = bigMarketMap.get(marketId);
    const buyAmt  = Math.round(parseFloat(A.buy_total));
    const sellAmt = Math.round(parseFloat(B.sell_total));

    pairs.push({
      market_id:       marketId,
      market_id_short: marketId.slice(0, 16) + '...',
      vol_24h_usd:    Math.round(parseFloat(mkt.volume_24h)),
      buyer_wallet:    A.wallet_address,
      buyer_short:     A.wallet_address.slice(0, 10) + '...',
      buyer_usd:       buyAmt,
      seller_wallet:   B.wallet_address,
      seller_short:    B.wallet_address.slice(0, 10) + '...',
      seller_usd:      sellAmt,
      total_bet_usd:   buyAmt + sellAmt,
    });
  }

  pairs.sort((a, b) => b.total_bet_usd - a.total_bet_usd);
  const final = pairs.slice(0, C.limit);

  console.log(`\n  Opposing pairs: ${pairs.length} -> top ${final.length}`);
  printTable(final, ['market_id_short', 'vol_24h_usd', 'buyer_short', 'buyer_usd', 'seller_short', 'seller_usd', 'total_bet_usd']);
  return final;
}

// ── Signal 3: Black Swan ─────────────────────────────────────
async function runBlackSwan() {
  sep('Signal 3: Black Swan');
  const C = CFG.black_swan;
  console.log(`  Criteria: 2h abs change>=${C.min_abs_change} | start>=${C.min_start_price} | vol>=$${(C.min_vol_2h/1000).toFixed(0)}k | past ${C.lookback_days} days`);

  process.stdout.write('  [Q1] 2h price window scan...');
  const rows = await mcp.queryWithRetry(`
    SELECT
      market_id,
      toDateTime(intDiv(toUnixTimestamp(traded_at), 7200) * 7200) AS time_bucket,
      min(price)      AS min_price,
      max(price)      AS max_price,
      max(price) - min(price)  AS abs_change,
      round((max(price) - min(price)) * 100, 1) AS change_pp,
      argMin(price, traded_at) AS first_price,
      argMax(price, traded_at) AS last_price,
      sum(usd_amount) AS vol_2h_usd,
      count()         AS trades_2h
    FROM trades
    WHERE traded_at >= now() - INTERVAL ${C.lookback_days} DAY
      AND traded_at IS NOT NULL
      AND type = 'trade'
      AND outcome_index = 0
      AND price > 0
      AND usd_amount > 0
      AND market_id IS NOT NULL
    GROUP BY market_id, time_bucket
    HAVING min_price >= ${C.min_start_price}
       AND max_price <= ${C.max_end_price}
       AND (max_price - min_price) >= ${C.min_abs_change}
       AND vol_2h_usd >= ${C.min_vol_2h}
    ORDER BY abs_change DESC, vol_2h_usd DESC
    LIMIT 200
  `, { maxRows: 200, retries: 3 });
  console.log(` ${rows.length} candidates`);

  // Keep only highest-change window per market
  const deduped = new Map();
  for (const r of rows) {
    const prev = deduped.get(r.market_id);
    if (!prev || parseFloat(r.abs_change) > parseFloat(prev.abs_change)) {
      deduped.set(r.market_id, r);
    }
  }

  const results = [...deduped.values()]
    .sort((a, b) => parseFloat(b.abs_change) - parseFloat(a.abs_change))
    .slice(0, C.limit)
    .map(r => {
      const fp = +parseFloat(r.first_price).toFixed(4);
      const lp = +parseFloat(r.last_price).toFixed(4);
      const direction = lp > fp ? 'UP' : lp < fp ? 'DOWN' : 'FLAT';
      return {
        market_id:       r.market_id,
        market_id_short: r.market_id.slice(0, 16) + '...',
        time_bucket:     r.time_bucket,
        min_price:       +parseFloat(r.min_price).toFixed(4),
        max_price:       +parseFloat(r.max_price).toFixed(4),
        first_price:     fp,
        last_price:      lp,
        direction,
        change_pp:       parseFloat(r.change_pp) + 'pp',
        vol_2h_usd:      Math.round(parseFloat(r.vol_2h_usd)),
        trades_2h:       Number(r.trades_2h),
      };
    });

  printTable(results, ['market_id_short', 'time_bucket', 'first_price', 'last_price', 'direction', 'change_pp', 'vol_2h_usd', 'trades_2h']);
  return results;
}

// ── Market name enrichment via Gamma API ─────────────────────
async function enrichMarketNames(allMarketIds) {
  if (!allMarketIds.length) return new Map();

  // Step 1: market_id -> condition_id via MCP trades table.
  // trades.condition_id is the canonical mapping in the MCP-backed workflow.
  process.stdout.write('  [names] Mapping market_id -> condition_id...');
  const inList = allMarketIds.map(id => `'${id}'`).join(',');
  let cidRows = [];
  try {
    cidRows = await mcp.queryWithRetry(`
      SELECT DISTINCT market_id, condition_id
      FROM trades
      WHERE market_id IN (${inList})
        AND condition_id IS NOT NULL
        AND condition_id != ''
      LIMIT 500
    `, { maxRows: 500, retries: 3 });
    console.log(` ${cidRows.length} mappings`);
  } catch (e) {
    console.log(` mapping query failed: ${e.message}`);
  }

  if (!cidRows.length) return new Map();

  const cidMap = new Map(cidRows.map(r => [r.market_id, r.condition_id]));

  // Step 2: condition_id -> market metadata via Gamma API
  const conditionIds = cidRows.map(r => r.condition_id);
  process.stdout.write(`  [names] Gamma API (${conditionIds.length} condition IDs)...`);
  const gammaMarkets = await gamma.fetchByConditionIds(conditionIds);
  console.log(` ${gammaMarkets.length} resolved`);

  // Build conditionId -> market info map
  const marketInfoMap = new Map();
  for (const m of gammaMarkets) {
    if (m.conditionId) {
      const eventSlug = (m.events && m.events[0] && m.events[0].slug) || m.slug || '';
      marketInfoMap.set(m.conditionId, {
        question:       m.question  || '',
        slug:           eventSlug,
        category:       m.category  || '',
        end_date:       m.endDate   ? m.endDate.slice(0, 10) : '',
        polymarket_url: eventSlug ? `https://polymarket.com/event/${eventSlug}` : '',
      });
    }
  }

  // market_id -> market info
  const result = new Map();
  for (const [mid, cid] of cidMap) {
    const info = marketInfoMap.get(cid);
    if (info) result.set(mid, info);
  }
  return result;
}

// ── Main ─────────────────────────────────────────────────────
async function main() {
  const runAt = new Date().toISOString();
  console.log('\n' + '='.repeat(72));
  console.log('  Polymarket Daily Anomaly Detection');
  console.log('  Run at:', runAt);
  console.log('='.repeat(72));

  // Health check
  const ok = await mcp.ping();
  if (!ok) {
    console.error('  [ERROR] MCP service unavailable. Set MCP_URL env var if needed.');
    process.exit(1);
  }
  console.log('  [MCP] Connected');

  const activeMarkets = await getActiveMarkets();

  const insider   = await runInsiderWatch(activeMarkets);
  await sleep(500);
  const whaleWars = await runWhaleWars();
  await sleep(500);
  const blackSwan = await runBlackSwan();

  // ── Market name enrichment ──────────────────────────────────
  sep('Market Name Resolution');
  const allMids = [
    ...insider.map(r => r.market_id),
    ...whaleWars.map(r => r.market_id),
    ...blackSwan.map(r => r.market_id),
  ].filter((v, i, a) => a.indexOf(v) === i);

  const nameMap = await enrichMarketNames(allMids);
  console.log(`  Resolved ${nameMap.size} / ${allMids.length} market names`);

  // Attach names + domain
  function attachName(r) {
    const info = nameMap.get(r.market_id) || {};
    return {
      ...r,
      market_name: info.question     || '',
      market_url:  info.polymarket_url || '',
      market_end:  info.end_date     || '',
      domain:      marketToDomain(info.question, info.category) || 'GEN',
    };
  }

  const insiderNamed   = insider.map(attachName);
  const whaleWarsNamed = whaleWars.map(attachName);
  let   blackSwanNamed = blackSwan.map(attachName);

  // Black Swan: filter out completed sports events
  const today = runAt.slice(0, 10);
  const beforeFilter = blackSwanNamed.length;
  blackSwanNamed = blackSwanNamed.filter(r => {
    if (!['GEN', 'SPT'].includes(r.domain)) return true;
    if (r.market_end && r.market_end <= today) return false;
    return true;
  });
  if (beforeFilter !== blackSwanNamed.length) {
    console.log(`\n  [filter] Black Swan: ${beforeFilter} -> ${blackSwanNamed.length} (removed ${beforeFilter - blackSwanNamed.length} completed sports events)`);
  }

  // Print preview
  console.log('\n  Insider Watch:');
  insiderNamed.forEach(r => console.log(`    [${r.market_id.slice(0,8)}...] [${r.domain}] ${r.market_name || '(unknown)'}`));
  console.log('\n  Whale Wars:');
  whaleWarsNamed.forEach(r => console.log(`    [${r.market_id.slice(0,8)}...] [${r.domain}] ${r.market_name || '(unknown)'}`));
  console.log('\n  Black Swan (top 5):');
  blackSwanNamed.slice(0,5).forEach(r => console.log(`    [${r.market_id.slice(0,8)}...] [${r.domain}] ${r.market_name || '(unknown)'}`));

  // ── Summary ──────────────────────────────────────────────────
  sep('Summary');
  console.log(`  Insider Watch: ${insiderNamed.length} events`);
  console.log(`  Whale Wars:    ${whaleWarsNamed.length} pairs`);
  console.log(`  Black Swan:    ${blackSwanNamed.length} events`);

  // ── JSON export ──────────────────────────────────────────────
  const output = {
    generated_at: runAt,
    date:         runAt.slice(0, 10),
    config: CFG,
    results: {
      insider_watch: insiderNamed.map(r => ({
        market_id:      r.market_id,
        market_name:    r.market_name,
        market_url:     r.market_url,
        market_end:     r.market_end,
        domain:         r.domain,
        wallet_count:   r.wallet_count || 1,
        wallets:        r.wallets || [r.wallet_address],
        wallet_address: r.wallet_address,
        buy_price:      r.buy_price,
        trade_usd:      r.trade_usd,
        avg_mkt_usd:    r.avg_mkt_usd,
        x_avg:          r.x_avg,
        wallet_trades:  r.wallet_trades,
        traded_at:      r.traded_at,
        is_aggregated:  r.is_aggregated || false,
      })),
      whale_wars: whaleWarsNamed.map(r => ({
        market_id:     r.market_id,
        market_name:   r.market_name,
        market_url:    r.market_url,
        market_end:    r.market_end,
        domain:        r.domain,
        vol_24h_usd:   r.vol_24h_usd,
        buyer_wallet:  r.buyer_wallet,
        buyer_usd:     r.buyer_usd,
        seller_wallet: r.seller_wallet,
        seller_usd:    r.seller_usd,
        total_bet_usd: r.total_bet_usd,
      })),
      black_swan: blackSwanNamed.map(r => ({
        market_id:   r.market_id,
        market_name: r.market_name,
        market_url:  r.market_url,
        market_end:  r.market_end,
        domain:      r.domain,
        time_bucket: r.time_bucket,
        min_price:   r.min_price,
        max_price:   r.max_price,
        first_price: r.first_price,
        last_price:  r.last_price,
        direction:   r.direction,
        change_pp:   r.change_pp,
        vol_2h_usd:  r.vol_2h_usd,
        trades_2h:   r.trades_2h,
      })),
    },
  };

  const filename = `content-signals-${runAt.slice(0, 10)}.json`;
  fs.writeFileSync(filename, JSON.stringify(output, null, 2), 'utf-8');
  const kb = (JSON.stringify(output).length / 1024).toFixed(1);
  console.log(`\n  [export] ${filename}  (${kb} KB)`);
}

main().catch(err => {
  console.error('\n[FATAL]', err.message);
  process.exit(1);
});
