#!/usr/bin/env node

const baseUrl = (process.argv[2] || 'https://marsedge.vip').replace(/\/$/, '');
const url = `${baseUrl}/api/probboard/latest`;

try {
  const res = await fetch(url, {
    headers: {
      'accept': 'application/json',
      'user-agent': 'marsedge-probboard-skill/1.0'
    }
  });

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    console.error(JSON.stringify({ ok: false, url, error: 'Non-JSON response', body: text.slice(0, 500) }, null, 2));
    process.exit(1);
  }

  if (!res.ok || data.ok === false) {
    console.error(JSON.stringify({ ok: false, url, status: res.status, data }, null, 2));
    process.exit(1);
  }

  const items = Array.isArray(data.items) ? data.items.map((item) => ({
    symbol: item.symbol,
    ts: item.ts,
    rem_secs: item.rem_secs,
    p_up_pct: item.p_up_pct,
    p_down_pct: item.p_down_pct,
    up_bid: item.up_bid,
    up_ask: item.up_ask,
    down_bid: item.down_bid,
    down_ask: item.down_ask,
  })) : [];

  console.log(JSON.stringify({
    ok: true,
    url,
    plan: data.plan,
    refreshMs: data.refreshMs,
    updatedAt: data.updatedAt,
    itemCount: items.length,
    items,
  }, null, 2));
} catch (error) {
  console.error(JSON.stringify({ ok: false, url, error: error.message }, null, 2));
  process.exit(1);
}
