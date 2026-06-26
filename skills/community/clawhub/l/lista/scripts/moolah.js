#!/usr/bin/env node
'use strict';

/**
 * moolah.js — Lista Lending API tool (BSC + ETH)
 * No external dependencies required — uses Node.js stdlib only.
 *
 * Usage:
 *   node moolah.js [--chain bsc|eth] [--debt-only] dashboard   <wallet>
 *   node moolah.js [--chain bsc|eth] markets     [keyword]
 *   node moolah.js [--chain bsc|eth] vaults      [keyword]
 *   node moolah.js                   prices
 *   node moolah.js                   rewards     <wallet>
 *   node moolah.js                   staking
 *   node moolah.js                   cdp-markets [collateral]
 *
 * Default chain: bsc
 * All output is JSON on stdout. Errors go to stderr with exit code 1.
 */

const https = require('https');

// ── HTTP layer ────────────────────────────────────────────────────────────────

function request(url) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { timeout: 15000 }, (res) => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString())); }
        catch (e) { reject(new Error(`Invalid JSON from ${url}`)); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.end();
  });
}

const BASE = 'https://api.lista.org';

async function apiGet(path, params = {}) {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== '') qs.set(k, String(v));
  }
  const q = qs.toString();
  const url = `${BASE}${path}${q ? '?' + q : ''}`;
  const resp = await request(url);
  if (resp.code && resp.code !== '000000000') throw new Error(`API ${path}: ${resp.message || resp.msg}`);
  return resp.data ?? resp;
}

async function apiGetAll(path, params = {}) {
  const items = [];
  let page = 1;
  while (true) {
    const d = await apiGet(path, { ...params, page: String(page), pageSize: '50' });
    items.push(...(d.list || []));
    if (items.length >= (d.total || 0)) break;
    page++;
  }
  return items;
}

// ── Metric helpers ────────────────────────────────────────────────────────────

const FAMILIES = {
  usd: ['USD1', 'U', 'USDT', 'USDC', 'DAI', 'FDUSD', 'BUSD', 'lisUSD'],
  bnb: ['BNB', 'WBNB', 'slisBNB', 'wstBNB', 'ankrBNB', 'BNBx'],
  eth: ['ETH', 'WETH', 'wstETH', 'stETH', 'rETH'],
  btc: ['BTCB', 'WBTC', 'BTC'],
};

function getFamily(sym) {
  if (!sym) return null;
  const s = sym.replace(/\s/g, '');
  for (const [fam, members] of Object.entries(FAMILIES)) {
    if (members.some(m => s === m || s.includes(m))) return fam;
  }
  return null;
}

function isCorrelated(cSym, lSym) {
  const cf = getFamily(cSym);
  const lf = getFamily(lSym);
  return cf !== null && cf === lf;
}

function riskLevel(ltv, lltv, correlated) {
  if (lltv === 0 || ltv === 0) return 'SAFE';
  const ratio = ltv / lltv;
  if (correlated) {
    if (ratio >= 0.97) return 'DANGER';
    if (ratio >= 0.92) return 'WARNING';
    return 'SAFE';
  }
  if (ratio >= 0.90) return 'DANGER';
  if (ratio >= 0.80) return 'WARNING';
  return 'SAFE';
}

function round2(n) { return Math.round(n * 100) / 100; }

function computeMetrics(collAmt, collUsd, debtAmt, debtUsd, collPrice, loanPrice, lltv) {
  const ltv = collUsd > 0 ? debtUsd / collUsd : 0;
  const healthFactor = ltv > 0 ? lltv / ltv : Infinity;
  const liqPriceUsd = (collAmt > 0 && lltv > 0) ? debtUsd / (collAmt * lltv) : 0;
  const buffer = collPrice > 0 && liqPriceUsd > 0 ? (collPrice - liqPriceUsd) / collPrice : 1;
  const netEquityUsd = collUsd - debtUsd;
  return {
    ltv: round2(ltv),
    healthFactor: ltv > 0 ? round2(healthFactor) : null,
    liqPriceUsd: ltv > 0 ? round2(liqPriceUsd) : null,
    buffer: ltv > 0 ? round2(buffer) : null,
    netEquityUsd: round2(netEquityUsd),
  };
}

// ── Commands ──────────────────────────────────────────────────────────────────

/**
 * dashboard <wallet>
 * Full position overview: positions, totals, pre-computed metrics.
 */
async function cmdDashboard(wallet) {
  if (!wallet) throw new Error('Usage: dashboard <wallet>');

  // Holdings has all position data (amounts, USD, prices) in one call.
  // Borrows gives borrow APY. Totals give aggregated USD.
  const [borrows, holdings, vaultHoldings, totalDep, totalBor, totalCol] = await Promise.all([
    apiGet(`/api/moolah/borrow/${wallet}`),
    apiGet('/api/moolah/one/holding', { userAddress: wallet, type: 'market' }),
    apiGet('/api/moolah/one/holding', { userAddress: wallet, type: 'vault' }),
    apiGet('/api/moolah/one/total', { userAddress: wallet, type: 'deposit' }),
    apiGet('/api/moolah/one/total', { userAddress: wallet, type: 'borrow' }),
    apiGet('/api/moolah/one/total', { userAddress: wallet, type: 'collateral' }),
  ]);

  const holdingsList = holdings.objs || [];
  const vaultDepositsList = (vaultHoldings.objs || []).map(v => ({
    address: v.address,
    name: v.name,
    assets: parseFloat(v.assets || 0),
    assetsUsd: round2(parseFloat(v.assetsUsd || 0)),
    apy: parseFloat(v.apy || 0),
    emissionApy: parseFloat(v.emissionApy || 0),
    curator: v.curator || '',
  }));

  if (holdingsList.length === 0 && vaultDepositsList.length === 0) {
    return {
      wallet: wallet.toLowerCase(), chain: chainKey,
      totals: { depositUsd: 0, borrowUsd: 0, collateralUsd: 0 },
      positions: [],
      vaultDeposits: [],
    };
  }

  // Fetch borrow markets from ALL chains for LLTV lookup — holdings API
  // returns cross-chain data regardless of chain parameter.
  const allMarkets = await apiGetAll('/api/moolah/borrow/markets', {
    zone: '0,1,3,4', chain: 'bsc,ethereum',
  });

  // Build borrow APY lookup by marketId (address field)
  const borrowApyMap = new Map();
  const borrowsArr = Array.isArray(borrows) ? borrows : [];
  for (const b of borrowsArr) {
    if (b.address) borrowApyMap.set(b.address, parseFloat(b.apy || 0));
  }

  // Build LLTV lookup
  const lltvMap = new Map();
  for (const m of allMarkets) {
    lltvMap.set(m.id, parseFloat(m.lltv) || 0);
  }

  const positions = [];
  for (const h of holdingsList) {
    // Filter by selected chain — holdings API returns all chains
    if (h.chain && h.chain !== chainKey) continue;
    const marketId = h.marketId;
    const collateralAmount = parseFloat(h.collateralAmount || 0);
    const collateralUsd = parseFloat(h.collateralUsd || 0);
    const debtAmount = parseFloat(h.loanAmount || 0);
    const debtUsd = parseFloat(h.loanUsd || 0);
    const collPrice = parseFloat(h.collateralPrice || 0);
    const loanPrice = parseFloat(h.loanPrice || 0);
    const lltv = lltvMap.get(marketId) || 0;
    const collSym = h.collateralSymbol || '?';
    const loanSym = h.loanSymbol || '?';
    const zone = h.zone ?? null;

    // Dust filter — only skip truly empty positions
    if (collateralUsd === 0 && debtUsd === 0) continue;
    // Debt-only filter (when --debt-only flag is set)
    if (debtOnly && debtAmount === 0) continue;

    const corr = isCorrelated(collSym, loanSym);
    const metrics = computeMetrics(collateralAmount, collateralUsd, debtAmount, debtUsd, collPrice, loanPrice, lltv);

    positions.push({
      marketId,
      collateralSymbol: collSym,
      loanSymbol: loanSym,
      collateralAmount: round2(collateralAmount),
      collateralUsd: round2(collateralUsd),
      collateralPrice: round2(collPrice),
      debtAmount: round2(debtAmount),
      debtUsd: round2(debtUsd),
      loanPrice: round2(loanPrice),
      borrowRate: borrowApyMap.get(marketId) || 0,
      lltv,
      ltv: metrics.ltv,
      healthFactor: metrics.healthFactor,
      liqPriceUsd: metrics.liqPriceUsd,
      buffer: metrics.buffer,
      netEquityUsd: metrics.netEquityUsd,
      zone,
      isCorrelated: corr,
      riskLevel: debtAmount > 0 ? riskLevel(metrics.ltv, lltv, corr) : 'SAFE',
    });
  }

  return {
    wallet: wallet.toLowerCase(),
    chain: chainKey,
    totals: {
      depositUsd: round2(parseFloat(totalDep.total || 0)),
      borrowUsd: round2(parseFloat(totalBor.total || 0)),
      collateralUsd: round2(parseFloat(totalCol.total || 0)),
    },
    positions,
    vaultDeposits: vaultDepositsList,
  };
}

/**
 * markets [keyword]
 * All borrow markets with rates, liquidity, LLTV.
 */
async function cmdMarkets(keyword) {
  const [marketsData, overall] = await Promise.all([
    apiGetAll('/api/moolah/borrow/markets', {
      zone: '0,1,3,4', chain: chainKey, keyword: keyword || undefined,
    }),
    apiGet('/api/moolah/overall'),
  ]);

  const markets = marketsData.map(m => ({
    id: m.id,
    collateral: m.collateral || m.collateralSymbol,
    loan: m.loan || m.loanSymbol,
    supplyApy: parseFloat(m.supplyApy || 0),
    borrowApy: parseFloat(m.rate || 0),
    liquidityUsd: round2(parseFloat(m.liquidityUsd || 0)),
    lltv: parseFloat(m.lltv || 0),
    zone: m.zone,
    isSmartLending: m.zone === 3,
    utilization: parseFloat(m.utilization || 0),
    termType: m.termType || 0,
  }));

  return {
    chain: chainKey,
    overall: {
      totalDeposits: overall.totalDeposits || '0',
      totalBorrowed: overall.totalBorrowed || '0',
      maxVaultApy: parseFloat(overall.maxVaultApy || 0),
      minBorrowRate: parseFloat(overall.minBorrowRate || 0),
    },
    total: markets.length,
    markets,
  };
}

/**
 * vaults [keyword]
 * All lending vaults with APY, TVL, allocations.
 */
async function cmdVaults(keyword) {
  const vaultsData = await apiGetAll('/api/moolah/vault/list', {
    chain: chainKey, keyword: keyword || undefined,
  });

  const vaults = vaultsData.map(v => {
    const apy = parseFloat(v.apy || 0);
    const emissionApy = v.emissionEnabled ? parseFloat(v.emissionApy || 0) : 0;
    return {
      address: v.address,
      name: v.name,
      assetSymbol: v.assetSymbol,
      apy,
      emissionApy,
      totalApy: apy + emissionApy,
      depositsUsd: round2(parseFloat(v.depositsUsd || 0)),
      utilization: parseFloat(v.utilization || 0),
      zone: v.zone,
      curator: v.curator || '',
      collaterals: (v.collaterals || []).map(c => ({
        name: c.name || c.collateralSymbol,
        loanSymbol: c.loanSymbol,
        allocation: parseFloat(c.allocation || 0),
      })),
    };
  });

  return {
    chain: chainKey,
    total: vaults.length,
    vaults,
  };
}

/**
 * prices
 * All token prices from Lista v2 price endpoint.
 */
async function cmdPrices() {
  const data = await apiGet('/api/v2/price');

  const tokens = [];
  if (data.priceInfo) {
    for (const t of data.priceInfo) {
      tokens.push({
        symbol: t.token || t.symbol,
        address: t.address,
        priceUsd: t.price || t.priceUsd || '0',
      });
    }
  }

  const byAddress = {};
  if (data.prices) {
    for (const [addr, price] of Object.entries(data.prices)) {
      byAddress[addr.toLowerCase()] = String(price);
    }
  }

  return { tokens, byAddress };
}

/**
 * rewards <wallet>
 * Claimable rewards: LISTA emission + bribe.
 */
async function cmdRewards(wallet) {
  if (!wallet) throw new Error('Usage: rewards <wallet>');

  const [emission, bribe, priceData] = await Promise.all([
    apiGet('/api/credit/emission/user-reward', { userAddress: wallet }).catch(() => null),
    apiGet('/api/bribe/getUserRewards', { address: wallet }).catch(() => null),
    apiGet('/api/v2/price').catch(() => null),
  ]);

  // Build price lookup
  const prices = {};
  if (priceData && priceData.priceInfo) {
    for (const t of priceData.priceInfo) {
      const sym = t.token || t.symbol;
      if (sym) prices[sym.toUpperCase()] = parseFloat(t.price || 0);
    }
  }

  const rewards = [];
  let totalUsd = 0;

  // LISTA emission
  if (emission && typeof emission === 'object') {
    const amt = parseFloat(emission.totalAmount || emission.amount || 0);
    if (amt > 0) {
      const usd = round2(amt * (prices['LISTA'] || 0));
      rewards.push({ source: 'LISTA Emission', amount: round2(amt), symbol: 'LISTA', usd });
      totalUsd += usd;
    }
  }

  // Bribe rewards
  if (bribe && typeof bribe === 'object') {
    const bribeList = bribe.list || bribe.rewards || (Array.isArray(bribe) ? bribe : []);
    for (const r of bribeList) {
      const amt = parseFloat(r.amount || r.reward || 0);
      const sym = r.token || r.symbol || '?';
      if (amt > 0) {
        const usd = round2(amt * (prices[sym.toUpperCase()] || 0));
        rewards.push({ source: 'Bribe', amount: round2(amt), symbol: sym, usd });
        totalUsd += usd;
      }
    }
  }

  return {
    wallet: wallet.toLowerCase(),
    rewards,
    totalUsd: round2(totalUsd),
  };
}

/**
 * staking
 * slisBNB staking APR and yield APY.
 */
async function cmdStaking() {
  const [apr, yieldApy] = await Promise.all([
    apiGet('/v1/stakes/latest-apr'),
    apiGet('/v1/stakes/yield-apy'),
  ]);

  const stk = yieldApy.staking || {};
  return {
    apr: parseFloat(apr.apr || 0),
    launchPoolApy: parseFloat(apr.launchPoolApy || 0),
    comprehensiveApy: parseFloat(apr.comprehensiveApy || 0),
    locked: {
      '3m': parseFloat(stk.month3Apy || 0),
      '6m': parseFloat(stk.month6Apy || 0),
      '12m': parseFloat(stk.month12Apy || 0),
    },
  };
}

/**
 * cdp-markets [collateral]
 * CDP borrow markets (lisUSD borrowing against BNB ecosystem collateral).
 */
async function cmdCdpMarkets(collateral) {
  const data = await apiGetAll('/api/cdp/market/list', {});

  let markets = data.map(m => ({
    id: m.ilk || m.id,
    collateral: m.collateralTokenSymbol || m.collateral,
    loan: m.loanTokenSymbol || m.loan || 'lisUSD',
    lltv: parseFloat(m.lltv || 0),
    liquidity: m.liquidity || '0',
    borrowRate: parseFloat(m.borrowRate || m.rate || 0),
  }));

  if (collateral) {
    const kw = collateral.toLowerCase();
    markets = markets.filter(m => m.collateral.toLowerCase().includes(kw));
  }

  return {
    total: markets.length,
    markets,
  };
}

// ── CLI entry point ───────────────────────────────────────────────────────────

const COMMANDS = {
  'dashboard':   [cmdDashboard,  '<wallet>'],
  'markets':     [cmdMarkets,    '[keyword]'],
  'vaults':      [cmdVaults,     '[keyword]'],
  'prices':      [cmdPrices,     ''],
  'rewards':     [cmdRewards,    '<wallet>'],
  'staking':     [cmdStaking,    ''],
  'cdp-markets': [cmdCdpMarkets, '[collateral]'],
};

const HELP = [
  'Lista Lending API tool — BSC + ETH',
  '',
  'Usage: node moolah.js [--chain bsc|eth] [--debt-only] <command> [args]',
  '',
  '  dashboard   <wallet>       Full position report with metrics',
  '  markets     [keyword]      Borrow markets with rates and liquidity',
  '  vaults      [keyword]      Lending vaults with APY and allocations',
  '  prices                     All token prices',
  '  rewards     <wallet>       Claimable rewards (emission + bribe)',
  '  staking                    slisBNB staking APR/APY',
  '  cdp-markets [collateral]   CDP markets (lisUSD borrowing)',
  '',
  'Default: --chain bsc',
  'Output: JSON on stdout. Errors on stderr.',
].join('\n');

// Parse --chain and --debt-only flags
const rawArgs = process.argv.slice(2);
let chainKey = 'bsc';
let debtOnly = false;
const cmdArgs = [];

for (let i = 0; i < rawArgs.length; i++) {
  if (rawArgs[i] === '--chain' && rawArgs[i + 1]) {
    chainKey = rawArgs[++i].toLowerCase();
  } else if (rawArgs[i] === '--debt-only') {
    debtOnly = true;
  } else {
    cmdArgs.push(rawArgs[i]);
  }
}

// Normalise alias
if (chainKey === 'eth') chainKey = 'ethereum';

if (!['bsc', 'ethereum'].includes(chainKey)) {
  process.stderr.write(`Unknown chain "${chainKey}". Valid: bsc, ethereum (or eth)\n`);
  process.exit(1);
}

const [cmd, ...args] = cmdArgs;

if (!cmd || !COMMANDS[cmd]) {
  process.stderr.write(HELP + '\n');
  process.exit(1);
}

COMMANDS[cmd][0](...args)
  .then(result => { console.log(JSON.stringify(result, null, 2)); })
  .catch(err   => { process.stderr.write(`Error: ${err.message}\n`); process.exit(1); });
