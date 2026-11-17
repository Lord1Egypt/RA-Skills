#!/usr/bin/env node
// Market journal: records directional BTC views and scores them later against what the price did.
// Play money only. It places no orders and talks to no exchange.
// The price is always fetched here from AgentData's free sample, never taken from the caller,
// so a model cannot record a view at a price it made up.
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const PRICE_URL = "https://agentdata-api.com/api/try/prices";
const STAKE_USD = 1000;      // play-money stake per directional view
const FLAT_BAND = 0.01;      // "flat" is right when the price moved less than 1 % either way
const MIN_SAMPLE = 30;       // below this the hit rate says nothing

function args(argv) {
  const o = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) { o._.push(a); continue; }
    const eq = a.indexOf("=");
    if (eq > 0) o[a.slice(2, eq)] = a.slice(eq + 1);
    else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) o[a.slice(2)] = argv[++i];
    else o[a.slice(2)] = "true";
  }
  return o;
}
function fail(msg) { console.log(JSON.stringify({ ok: false, error: msg })); process.exit(1); }

const a = args(process.argv.slice(2));
const cmd = a._[0];
const file = resolve(a.file || "market-journal/journal.jsonl");

function load() {
  if (!existsSync(file)) return [];
  return readFileSync(file, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
}
function save(rows) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, rows.map((r) => JSON.stringify(r)).join("\n") + (rows.length ? "\n" : ""));
}
const DATA = "https://agentdata-api.com/api/try";
async function sample(name) {
  let res;
  try { res = await fetch(`${DATA}/${name}`, { headers: { "User-Agent": "market-journal" }, signal: AbortSignal.timeout(20000) }); }
  catch (e) { fail("could not reach the data source: " + (e && e.message)); }
  if (!res.ok) fail("data source answered " + res.status);
  return (await res.json()).data || {};
}
// The price always comes from here, never from the caller.
async function price() {
  const d = await sample("prices");
  const p = d.BTCUSDT && Number(d.BTCUSDT.price);
  if (!(p > 0)) fail("data source returned no BTC price");
  return { price: p, source: "agentdata-free-sample" };
}
function now() { return Date.now(); }
const pct = (x) => (x * 100).toFixed(2) + " %";

if (cmd === "data") {
  // what a view is formed on: BTC price, fear and greed, funding (AgentData free samples)
  const [p, s, f] = await Promise.all([sample("prices"), sample("sentiment"), sample("funding-rates")]);
  const fg = s.fearGreedIndex || {}, fr = f.BTC_USDT || {};
  console.log(JSON.stringify({ ok: true, source: "AgentData free samples",
    btc_usd: p.BTCUSDT && p.BTCUSDT.price,
    fear_greed: fg.value != null ? { value: fg.value, label: fg.classification, yesterday: fg.yesterday, last_week: fg.lastWeek } : null,
    btc_funding: fr.rate != null ? { rate: fr.rate, annualized: fr.annualized } : null,
    not_included: "other coins, composite sentiment, other perpetuals, any history" }));
} else if (cmd === "view") {
  const direction = String(a.direction || "").toLowerCase();
  if (!["up", "down", "flat"].includes(direction)) fail("--direction must be up, down or flat");
  const hours = Number(a["horizon-hours"]);
  if (!(hours >= 1 && hours <= 24 * 30)) fail("--horizon-hours must be between 1 and 720");
  const confidence = Number(a.confidence);
  if (!(confidence >= 0.5 && confidence <= 1)) fail("--confidence must be between 0.5 (coin flip) and 1");
  const reason = String(a.reason || "").trim();
  if (reason.length < 20) fail("--reason must say in a sentence why (at least 20 characters)");
  const rows = load();
  const open = rows.filter((r) => !r.settled);
  if (open.length >= 5) fail("five views are already open; settle them before recording more");
  const p = await price(), t = now();
  const row = { id: "v" + (rows.length + 1), asset: "BTC", ts: new Date(t).toISOString(), due: new Date(t + hours * 3600e3).toISOString(),
    direction, horizonHours: hours, confidence, reason: reason.slice(0, 600), inputs: String(a.inputs || "").slice(0, 300),
    model: String(a.model || "").slice(0, 80), entry: p.price, priceSource: p.source, settled: false };
  mkdirSync(dirname(file), { recursive: true });
  appendFileSync(file, JSON.stringify(row) + "\n");
  console.log(JSON.stringify({ ok: true, recorded: row.id, entry: row.entry, due: row.due, file }));
} else if (cmd === "settle") {
  const rows = load(), t = now();
  const due = rows.filter((r) => !r.settled && Date.parse(r.due) <= t);
  if (!due.length) {
    const next = rows.filter((r) => !r.settled).map((r) => r.due).sort()[0];
    console.log(JSON.stringify({ ok: true, settled: 0, open: rows.filter((r) => !r.settled).length, nextDue: next || null }));
  } else {
    const p = await price(), out = [];
    for (const r of due) {
      const move = p.price / r.entry - 1;
      r.settled = true; r.exit = p.price; r.exitSource = p.source; r.settledAt = new Date(t).toISOString();
      r.lateHours = Math.round(((t - Date.parse(r.due)) / 3600e3) * 10) / 10;
      r.move = move;
      r.hit = r.direction === "up" ? move > 0 : r.direction === "down" ? move < 0 : Math.abs(move) < FLAT_BAND;
      r.pnlUsd = r.direction === "flat" ? 0 : Math.round(STAKE_USD * move * (r.direction === "up" ? 1 : -1) * 100) / 100;
      out.push({ id: r.id, direction: r.direction, entry: r.entry, exit: r.exit, move: pct(move), hit: r.hit, pnlUsd: r.pnlUsd, lateHours: r.lateHours });
    }
    save(rows);
    console.log(JSON.stringify({ ok: true, settled: out.length, results: out }));
  }
} else if (cmd === "status") {
  const rows = load();
  console.log(JSON.stringify({ ok: true, file, total: rows.length,
    open: rows.filter((r) => !r.settled).map((r) => ({ id: r.id, direction: r.direction, entry: r.entry, due: r.due, confidence: r.confidence })) }));
} else if (cmd === "report") {
  const rows = load(), done = rows.filter((r) => r.settled);
  const lines = [`Market journal: ${rows.length} views recorded, ${done.length} settled, ${rows.length - done.length} open. Play money, BTC only.`];
  if (done.length) {
    const hits = done.filter((r) => r.hit).length;
    const dir = done.filter((r) => r.direction !== "flat");
    const pnl = dir.reduce((s, r) => s + r.pnlUsd, 0);
    const alwaysUpHits = done.filter((r) => r.move > 0).length;
    const alwaysUpPnl = done.reduce((s, r) => s + STAKE_USD * r.move, 0);
    const meanConf = done.reduce((s, r) => s + r.confidence, 0) / done.length;
    lines.push(`Right: ${hits} of ${done.length} (${pct(hits / done.length)}). Stated confidence on average: ${pct(meanConf)}.`);
    lines.push(`Paper result at $${STAKE_USD} per directional view: ${pnl >= 0 ? "+" : ""}${pnl.toFixed(2)} USD over ${dir.length} directional view${dir.length === 1 ? "" : "s"}, before any fees.`);
    lines.push(`Baseline "always up": right ${alwaysUpHits} of ${done.length} (${pct(alwaysUpHits / done.length)}), paper result ${alwaysUpPnl >= 0 ? "+" : ""}${alwaysUpPnl.toFixed(2)} USD.`);
    lines.push(hits > alwaysUpHits && pnl > alwaysUpPnl ? "The views beat the baseline on both counts so far." : "The views do not beat the baseline so far.");
    if (done.length < MIN_SAMPLE) lines.push(`Only ${done.length} settled views: fewer than ${MIN_SAMPLE} is too few to tell skill from luck.`);
    const late = done.filter((r) => r.lateHours > Math.max(1, r.horizonHours * 0.25)).length;
    if (late) lines.push(`${late} views were settled well after they were due, so their result reflects a longer period than stated.`);
  } else lines.push("Nothing settled yet, so there is no result to report.");
  lines.push("This is a record of past guesses, not advice to buy or sell anything.");
  console.log(lines.join("\n"));
} else {
  console.log(`Usage:
  journal.mjs data        current BTC price, fear and greed, funding
  journal.mjs view --direction up|down|flat --horizon-hours N --confidence 0.5-1 --reason "why" [--inputs "data used"] [--model name]
  journal.mjs settle      score every view whose time is up against the current price
  journal.mjs status      list open views
  journal.mjs report      hit rate and paper result against an "always up" baseline
Options: --file PATH (default market-journal/journal.jsonl in the current folder)`);
  process.exit(cmd ? 1 : 0);
}
