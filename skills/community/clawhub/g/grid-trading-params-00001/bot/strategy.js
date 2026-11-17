/**
 * 网格策略：在价格区间内按档位挂限价单。
 * 策略参数（多行 key=value 或 JSON）：
 *   symbol=BTC/USDT
 *   gridLevels=5
 *   lowerPrice=auto     ← 省略或填 auto：启动时按当前价 ±rangePercent% 自动计算
 *   upperPrice=auto
 *   rangePercent=5      ← auto 模式下的单侧百分比，默认 5（即当前价 ±5%）
 *   amountPerOrder=0.001
 *   intervalMs=60000
 */
function parseParams(text) {
  const params = {};
  if (!text || !text.trim()) return params;
  const trimmed = text.trim();
  if (trimmed.startsWith('{')) {
    try {
      return JSON.parse(trimmed);
    } catch (e) {
      return params;
    }
  }
  trimmed.split('\n').forEach(line => {
    const i = line.indexOf('=');
    if (i > 0) {
      const k = line.slice(0, i).trim();
      const v = line.slice(i + 1).trim();
      if (k && v !== '') params[k] = v;
    }
  });
  return params;
}

const defaultParams = {
  symbol: 'BTC/USDT',
  gridLevels: 5,
  lowerPrice: 'auto',
  upperPrice: 'auto',
  rangePercent: '5',
  amountPerOrder: '0.001',
  intervalMs: '60000'
};

function getParams(config) {
  const p = { ...defaultParams, ...parseParams(config.strategyParams || '') };
  const isAuto = (v) => !v || v === 'auto' || parseFloat(v) <= 0;
  return {
    symbol:         String(p.symbol || defaultParams.symbol),
    gridLevels:     Math.max(2, Math.min(50, parseInt(p.gridLevels, 10) || 5)),
    lowerPrice:     isAuto(p.lowerPrice)  ? null : parseFloat(p.lowerPrice),
    upperPrice:     isAuto(p.upperPrice)  ? null : parseFloat(p.upperPrice),
    rangePercent:   Math.max(0.5, Math.min(50, parseFloat(p.rangePercent) || 5)),
    amountPerOrder: parseFloat(p.amountPerOrder) || 0.001,
    intervalMs:     Math.max(10000, parseInt(p.intervalMs, 10) || 60000)
  };
}

let intervalId = null;
let currentExchange = null;
let currentSymbol = null;
let tickRunning = false;
const botOrderIds = new Set();

function priceMatch(orderPrice, gridPrice) {
  return Math.abs(parseFloat(orderPrice) - gridPrice) < gridPrice * 0.0001;
}

/** 拼出可排查的错误信息：message + cause（fetch failed 时根因在 cause） */
function errText(e) {
  if (!e) return '';
  const msg = e.message || String(e);
  const cause = e.cause;
  if (!cause) return msg;
  const causeMsg = typeof cause === 'object' && cause !== null && (cause.message || cause.code)
    ? (cause.message || cause.code)
    : String(cause);
  return causeMsg ? `${msg} | cause: ${causeMsg}` : msg;
}

async function run(exchange, config, abort, onActivity) {
  const report = (action) => { if (typeof onActivity === 'function') onActivity(action); };
  report('started');
  await new Promise((r) => setTimeout(r, 500));

  currentExchange = exchange;
  try {
    const params = getParams(config || {});
    let { symbol, gridLevels, lowerPrice, upperPrice, rangePercent, amountPerOrder, intervalMs } = params;
    currentSymbol = symbol;

    console.log('[Grid] Starting with', { symbol, gridLevels, lowerPrice, upperPrice, amountPerOrder });

    try {
      const balance = await exchange.fetchBalance();
      report('fetchBalance');
      const keys = Object.keys(balance).filter(k => balance[k] && typeof balance[k].free === 'number').slice(0, 3);
      console.log('[Grid] Exchange connected, balance keys:', keys);
    } catch (e) {
      const msg = errText(e);
      console.error('[Grid] fetchBalance failed – aborting:', msg);
      report('auth_error');
      return;
    }

    // ── 自动价格区间（fetchBalance 之后执行，避免阻塞活动上报）──
    if (lowerPrice === null || upperPrice === null) {
      try {
        const ticker = await exchange.fetchTicker(symbol);
        const mid = ticker.last || (ticker.bid + ticker.ask) / 2;
        if (!Number.isFinite(mid) || mid <= 0) {
          throw new Error('Exchange returned an invalid market price.');
        }
        const half = mid * (rangePercent / 100);
        if (lowerPrice === null) lowerPrice = mid - half;
        if (upperPrice === null) upperPrice = mid + half;
        console.log(`[Grid] Auto range ±${rangePercent}% around ${mid}: [${lowerPrice.toFixed(4)}, ${upperPrice.toFixed(4)}]`);
      } catch (e) {
        console.error('[Grid] fetchTicker for auto range failed:', errText(e));
        report('market_error');
        return;
      }
    }
    if (
      !Number.isFinite(lowerPrice) ||
      !Number.isFinite(upperPrice) ||
      upperPrice <= lowerPrice
    ) {
      console.error('[Grid] Invalid price range; strategy was not started.');
      report('config_error');
      return;
    }

    const step = (upperPrice - lowerPrice) / (gridLevels + 1);
    const prices = [];
    for (let i = 1; i <= gridLevels; i++) {
      prices.push(lowerPrice + step * i);
    }

    async function tick() {
      if ((abort && abort.aborted) || tickRunning) return;
      tickRunning = true;
      try {
        const ticker = await exchange.fetchTicker(symbol);
        const mid = ticker.last || (ticker.bid + ticker.ask) / 2;
        if (!Number.isFinite(mid) || mid <= 0) {
          throw new Error('Exchange returned an invalid market price.');
        }
        const openOrders = await exchange.fetchOpenOrders(symbol);
        const myOrders = openOrders.filter(
          (order) => order.symbol === symbol && botOrderIds.has(String(order.id))
        );

        const isGridPrice = (p) => prices.some(g => priceMatch(p, g));
        const ordersToCancel = myOrders.filter(o => !isGridPrice(o.price));
        for (const o of ordersToCancel) {
          if (abort && abort.aborted) break;
          try {
            await exchange.cancelOrder(o.id, symbol);
            botOrderIds.delete(String(o.id));
            console.log('[Grid] Cancelled stale order', o.side, o.price);
          } catch (e) {
            if (!e.message || !e.message.includes('Unknown order')) console.error('[Grid] Cancel error:', errText(e));
          }
        }

        const updatedOrders = await exchange.fetchOpenOrders(symbol);
        const orders = updatedOrders.filter(
          (order) => order.symbol === symbol && botOrderIds.has(String(order.id))
        );
        const gridOrders = orders.filter(o => isGridPrice(o.price));
        const maxGridOrders = gridLevels * 2;

        let placedThisTick = 0;
        const maxPlacePerTick = 3;
        for (const price of prices) {
          if (gridOrders.length + placedThisTick >= maxGridOrders) break;
          if (abort && abort.aborted) break;
          if (placedThisTick >= maxPlacePerTick) break;
          const hasBuy = orders.some(o => o.side === 'buy' && priceMatch(o.price, price));
          const hasSell = orders.some(o => o.side === 'sell' && priceMatch(o.price, price));
          try {
            if (!hasBuy && price < mid) {
              const o = await exchange.createLimitBuyOrder(symbol, amountPerOrder, price);
              if (!o || !o.id) throw new Error('order placement returned no id');
              botOrderIds.add(String(o.id));
              report('order');
              placedThisTick++;
              console.log('[Grid] Placed buy', amountPerOrder, 'at', price, '→ id', o.id);
            }
            if (!hasSell && price > mid) {
              const o = await exchange.createLimitSellOrder(symbol, amountPerOrder, price);
              if (!o || !o.id) throw new Error('order placement returned no id');
              botOrderIds.add(String(o.id));
              report('order');
              placedThisTick++;
              console.log('[Grid] Placed sell', amountPerOrder, 'at', price, '→ id', o.id);
            }
          } catch (e) {
            console.error('[Grid] Order error at', price, ':', errText(e));
          }
        }
      } catch (e) {
        console.error('[Grid] Tick error:', errText(e));
      } finally {
        tickRunning = false;
      }
    }

    tick().catch(() => {});
    intervalId = setInterval(tick, intervalMs);

    await new Promise((resolve) => {
      const check = setInterval(() => {
        if (abort && abort.aborted) {
          clearInterval(check);
          resolve();
        }
      }, 200);
    });
  } catch (err) {
    console.error('[Grid] run error:', errText(err));
    await new Promise(() => {});
  } finally {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
    tickRunning = false;
    currentExchange = null;
    currentSymbol = null;
  }
}

async function stop() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
  const ex = currentExchange;
  const sym = currentSymbol;
  if (ex && sym) {
    try {
      const open = await ex.fetchOpenOrders(sym);
      const owned = open.filter((order) => botOrderIds.has(String(order.id)));
      for (const o of owned) {
        try {
          await ex.cancelOrder(o.id, sym);
          botOrderIds.delete(String(o.id));
          console.log('[Grid] Stopped: cancelled', o.side, o.price);
        } catch (e) {
          if (!e.message || !e.message.includes('Unknown order')) console.error('[Grid] Cancel on stop:', errText(e));
        }
      }
    } catch (e) {
      console.error('[Grid] cancelAll on stop:', errText(e));
    }
  }
  botOrderIds.clear();
}

module.exports = {
  run,
  stop,
  parseParams,
  getParams
};
