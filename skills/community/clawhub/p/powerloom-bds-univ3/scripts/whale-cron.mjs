#!/usr/bin/env node
/**
 * Whale Radar Cron — one-shot poll via bds_mpp_snapshot_allTrades.
 * Resolves pool token metadata via bds_mpp_pool_pool_address_metadata with on-disk cache.
 * Sends Telegram alerts with proper token names and verification provenance.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { callTool } from "./lib/mcp.mjs";
import { defaultMcpCallTimeoutIfUnset, telegramBotToken, telegramChatId } from "./lib/powerloom-env.mjs";
import { loadState, saveState, fingerprintTrade, rememberFingerprint, wasEmitted } from "./lib/state.mjs";
import { flattenAllTradesFromSnapshot, tradeUsd, tradeDirectionLabel } from "./lib/trade-utils.mjs";

const THRESHOLD = parseFloat(process.env.WHALE_CRON_THRESHOLD || "10000");
const MAX_LOOPS = parseInt(process.env.WHALE_CRON_MAX_LOOPS || "10", 10);
const STATE_FILE = process.env.WHALE_CRON_STATE_FILE || ".powerloom/whale-cron-state.json";
const POOL_CACHE_FILE = process.env.WHALE_CRON_POOL_CACHE || ".powerloom/pool-metadata-cache.json";
defaultMcpCallTimeoutIfUnset(120000);

const TG_TOKEN = telegramBotToken();
const TG_CHAT = telegramChatId();

// ─── Pool metadata cache ───

function loadPoolCache() {
  try {
    if (existsSync(POOL_CACHE_FILE)) return JSON.parse(readFileSync(POOL_CACHE_FILE, "utf8"));
  } catch {}
  return {};
}

function savePoolCache(cache) {
  const dir = dirname(POOL_CACHE_FILE);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(POOL_CACHE_FILE, JSON.stringify(cache, null, 2));
}

async function resolvePool(poolAddress) {
  const cache = loadPoolCache();
  const key = poolAddress.toLowerCase();
  if (cache[key]) return cache[key];

  try {
    const result = await callTool("bds_mpp_pool_pool_address_metadata", { pool_address: poolAddress });
    const data = result?.data;
    if (data?.token0?.symbol && data?.token1?.symbol) {
      const feeBps = data.fee || 0;
      const feeStr = feeBps >= 10000 ? `${feeBps / 10000}%` : feeBps >= 100 ? `${feeBps / 100}%` : `${feeBps / 100}%`;
      const info = {
        t0: data.token0.symbol,
        t1: data.token1.symbol,
        t0addr: data.token0.address,
        t1addr: data.token1.address,
        fee: feeStr,
      };
      cache[key] = info;
      savePoolCache(cache);
      return info;
    }
  } catch (e) {
    console.error(`[whale-cron] metadata lookup failed for ${poolAddress}: ${e.message}`);
  }
  return null;
}

// ─── Telegram ───

function escMd(s) {
  return String(s).replace(/([_*\[\]()~`>#+\-=|{}.!\\])/g, "\\$1");
}

function splitChunks(text, maxLen = 3900) {
  const sep = "\n━━━━━━━━━━━━━━━\n\n";
  const parts = text.split(sep);
  const out = []; let cur = "";
  for (const p of parts) {
    if ((cur + sep + p).length > maxLen) { if (cur) out.push(cur); cur = p; }
    else { cur = cur ? cur + sep + p : p; }
  }
  if (cur) out.push(cur);
  return out;
}

async function sendTelegram(text) {
  if (!TG_TOKEN || !TG_CHAT) { console.log(text); return; }
  const escaped = escMd(text);
  const chunks = escaped.length <= 4000 ? [escaped] : splitChunks(escaped);
  for (const chunk of chunks) {
    try {
      const r = await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: TG_CHAT, text: chunk, parse_mode: "MarkdownV2", disable_web_page_preview: true }),
      });
      const d = await r.json();
      if (!d.ok) {
        console.error("TG err:", JSON.stringify(d));
        // Fallback: send as plain text
        const r2 = await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ chat_id: TG_CHAT, text: chunk, disable_web_page_preview: true }),
        });
        const d2 = await r2.json();
        if (!d2.ok) console.error("TG retry err:", JSON.stringify(d2));
      }
    } catch (e) { console.error("TG fail:", e.message); }
  }
}

// ─── Formatting ───

function fmtUsd(v) {
  if (v >= 1e6) return `$${(v / 1e6).toFixed(2)}M`;
  if (v >= 1e3) return `$${(v / 1e3).toFixed(1)}K`;
  return `$${v.toFixed(0)}`;
}

function fmtAmt(n) {
  const a = Math.abs(n);
  if (a >= 1e9) return (a / 1e9).toFixed(2) + "B";
  if (a >= 1e6) return (a / 1e6).toFixed(2) + "M";
  if (a >= 1) return a.toLocaleString(undefined, { maximumFractionDigits: 4 });
  return a.toFixed(8);
}

function formatAlert(tw, verification, poolInfo) {
  const t = tw.trade;
  const d = t.data || {};
  const log = t.log || {};
  const usd = tradeUsd(tw);
  const dir = tradeDirectionLabel(tw);
  const side = dir === "BUY" ? "🟢" : "🔴";

  const poolAddr = (tw.poolAddress || "").toLowerCase();
  let t0, t1, fee;
  if (poolInfo) {
    t0 = poolInfo.t0;
    t1 = poolInfo.t1;
    fee = poolInfo.fee;
  } else {
    // Show truncated addresses as fallback
    const addr = tw.poolAddress || "";
    t0 = addr ? `${addr.slice(0, 7)}…` : "???";
    t1 = "?";
    fee = "?";
  }

  const isBuy = dir === "BUY";
  const boughtToken = isBuy ? t0 : t1;
  const soldToken = isBuy ? t1 : t0;
  const a0 = Math.abs(d.calculated_token0_amount || 0);
  const a1 = Math.abs(d.calculated_token1_amount || 0);
  const boughtAmt = isBuy ? a0 : a1;
  const soldAmt = isBuy ? a1 : a0;

  const wallet = d.sender || d.recipient || "—";
  const shortWallet = wallet.length > 16 ? `${wallet.slice(0, 10)}…${wallet.slice(-6)}` : wallet;
  const txHash = log.transactionHash || "";
  const block = log.blockNumber || "";

  const lines = [
    `${side} 🐋 WHALE ALERT ${side}`,
    ``,
    `${side} ${dir} ${t0}/${t1} on Uniswap V3 (${fee})`,
    `💰 ${fmtUsd(usd)} swapped`,
    ``,
    `▸ ⇢ ${fmtAmt(boughtAmt)} ${boughtToken}`,
    `▸ ⇠ ${fmtAmt(soldAmt)} ${soldToken}`,
    `▸ 🦊 ${shortWallet}`,
    `▸ 📦 Block ${block}`,
  ];
  if (txHash) lines.push(`▸ 🔍 TX: https://etherscan.io/tx/${txHash}`);

  if (verification?.cid) {
    const cid = verification.cid;
    lines.push(``);
    lines.push(`✅ Verified on-chain:`);
    lines.push(`  ├ CID: ${cid.length > 28 ? cid.slice(0, 28) + "…" : cid}`);
    lines.push(`  ├ Epoch: ${verification.epochId || "—"}`);
    lines.push(`  └ Project: ${(verification.projectId || "—").split(":")[0]}`);
  }

  return lines;
}

// ─── Main ───

async function main() {
  const state = loadState(STATE_FILE);
  let lastEpoch = state.lastStreamEpoch ?? null;
  let newAlerts = 0;
  const allAlerts = [];
  const poolCache = loadPoolCache();

  for (let i = 0; i < MAX_LOOPS; i++) {
    console.error(`[whale-cron] poll ${i + 1}/${MAX_LOOPS}, from_epoch=${lastEpoch}`);

    const params = { max_events: 50 };
    if (lastEpoch != null) params.from_epoch = lastEpoch;

    let result;
    try {
      result = await callTool("bds_mpp_snapshot_allTrades", params);
    } catch (e) {
      console.error(`[whale-cron] MCP call failed: ${e.message}`);
      break;
    }

    const data = result?.data || result;
    if (!data) { console.error("[whale-cron] empty result"); break; }

    const verification = data.verification || null;
    const epochEnd = data.epoch?.end || data.epoch?.begin || null;

    const rows = flattenAllTradesFromSnapshot(data);

    // Collect unique pool addresses to resolve
    const unknownPools = new Set();
    for (const tw of rows) {
      const poolAddr = (tw.poolAddress || "").toLowerCase();
      if (poolAddr && !poolCache[poolAddr]) unknownPools.add(tw.poolAddress);
    }

    // Resolve unknown pools (batch — one call per pool)
    for (const poolAddr of unknownPools) {
      if (!poolAddr) continue;
      try {
        const meta = await callTool("bds_mpp_pool_pool_address_metadata", { pool_address: poolAddr });
        const md = meta?.data;
        if (md?.token0?.symbol) {
          const feeBps = md.fee || 0;
          poolCache[poolAddr.toLowerCase()] = {
            t0: md.token0.symbol,
            t1: md.token1.symbol,
            fee: feeBps >= 100 ? `${feeBps / 100}%` : `${feeBps}%`,
          };
        }
      } catch (e) {
        console.error(`[whale-cron] metadata failed for ${poolAddr}: ${e.message}`);
      }
    }
    savePoolCache(poolCache);

    let aboveThreshold = 0;
    for (const tw of rows) {
      const usd = tradeUsd(tw);
      if (usd < THRESHOLD) continue;
      aboveThreshold++;

      const fp = fingerprintTrade(tw.trade);
      if (wasEmitted(state, fp)) continue;

      const poolInfo = poolCache[(tw.poolAddress || "").toLowerCase()] || null;
      const lines = formatAlert(tw, verification, poolInfo);
      allAlerts.push(lines.join("\n"));
      rememberFingerprint(state, fp);
      newAlerts++;

      const bn = tw.trade?.log?.blockNumber ?? 0;
      if (bn > (state.lastEmittedBlock || 0)) state.lastEmittedBlock = bn;
    }

    console.error(`[whale-cron] epoch=${epochEnd} trades=${rows.length} above=$${THRESHOLD}:${aboveThreshold} new_whales=${newAlerts}`);

    if (epochEnd != null) {
      if (epochEnd > (lastEpoch ?? 0)) {
        lastEpoch = epochEnd;
      } else {
        lastEpoch = epochEnd + 1;
      }
    }

    if (rows.length === 0) break;
    if (rows.length < 50) break;
  }

  // Send all alerts in batch
  if (allAlerts.length > 0) {
    const msg = allAlerts.join("\n━━━━━━━━━━━━━━━\n\n");
    await sendTelegram(msg);
  }

  state.lastStreamEpoch = lastEpoch;
  saveState(STATE_FILE, state);
  console.log(`[whale-cron] done. ${newAlerts} alerts sent.`);
}

main().catch(e => {
  console.error(`[whale-cron] fatal: ${e.message}`);
  console.error(e.stack);
  process.exit(1);
});
