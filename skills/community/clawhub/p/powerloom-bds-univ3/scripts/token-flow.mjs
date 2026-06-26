#!/usr/bin/env node
/**
 * Token-Flow — per-pool snapshot polls for all pools that list a token (`bds_mpp_snapshot_trades_pool_address`).
 * **Default:** one round over all pools for the token, then **exit** (cron-friendly). Use **`--daemon`** to loop with `heartbeat.interval_seconds` between rounds.
 */

import { callTool } from "./lib/mcp.mjs";
import { loadRecipe } from "./lib/recipe-config.mjs";
import {
  tradeUsd,
  tradeDirectionLabel,
  buildPoolAllowlistFromTokenPoolsResponse,
} from "./lib/trade-utils.mjs";
import {
  loadState,
  saveState,
  fingerprintTrade,
  rememberFingerprint,
  wasEmitted,
} from "./lib/state.mjs";
import { dispatchLines } from "./lib/dispatch.mjs";
import { defaultMcpCallTimeoutIfUnset } from "./lib/powerloom-env.mjs";

const USDC_MAINNET = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";

const arg = (name) => {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
};

const defaults = {
  name: "token-flow",
  heartbeat: { interval_seconds: 30 },
  filters: { token_address: USDC_MAINNET, min_usd: 0, pools: "auto" },
  client: { call_timeout_ms: 120000 },
  dispatch: { channel: "stdout" },
};

const cfg = loadRecipe("token-flow.yaml", defaults);
const token =
  (arg("--token") || cfg.filters?.token_address || USDC_MAINNET).toLowerCase();
const minUsd = parseFloat(String(cfg.filters?.min_usd ?? 0));
const stateFile =
  arg("--state-file") ||
  process.env.TOKEN_FLOW_STATE_FILE ||
  ".powerloom/token-flow-state.json";
const channel = cfg.dispatch?.channel || "stdout";
const daemon = process.argv.includes("--daemon");

function collectPoolAddresses(obj) {
  const raw = buildPoolAllowlistFromTokenPoolsResponse({ data: obj });
  if (raw.size) return raw;
  const set = new Set();
  const walk = (v) => {
    if (!v) return;
    if (typeof v === "string" && /^0x[a-fA-F]{40}$/.test(v)) {
      set.add(v.toLowerCase());
    } else if (Array.isArray(v)) v.forEach(walk);
    else if (typeof v === "object") Object.values(v).forEach(walk);
  };
  walk(obj);
  return set;
}

async function loadPoolsForToken() {
  const name = "bds_mpp_token_token_address_pools";
  const tryParams = [{ token_address: token }, { tokenAddress: token }];
  for (const p of tryParams) {
    try {
      const resp = await callTool(name, p);
      const body = resp?.data ?? resp;
      const set = collectPoolAddresses(body);
      if (set.size) return set;
    } catch {
      /* try next */
    }
  }
  return new Set();
}

function formatTokenAlert(tw, verification) {
  const t = tw.trade;
  const d = t.data || {};
  const log = t.log || {};
  const usd = tradeUsd(tw).toFixed(2);
  const dir = tradeDirectionLabel(tw);
  const t0 = Math.abs(parseFloat(String(d.calculated_token0_amount || 0))).toFixed(4);
  const t1 = Math.abs(parseFloat(String(d.calculated_token1_amount || 0))).toFixed(4);
  const pool = tw.poolAddress || "?";
  const tx = log.transactionHash || "";
  const block = log.blockNumber ?? "";
  const lines = [
    `TOKEN-FLOW | pool ${pool}`,
    `${dir}  $${usd}  (t0 ${t0} / t1 ${t1})`,
    `tx  ${tx}`,
    `block  ${block}`,
  ];
  if (verification?.cid && verification.epochId != null && verification.projectId) {
    lines.push(
      `provenance  cid ${verification.cid}  epoch_id ${verification.epochId}  project_id ${verification.projectId}`
    );
  }
  lines.push("---");
  return lines;
}

async function runPoll() {
  const poolSet = await loadPoolsForToken();
  if (!poolSet.size) {
    console.error(`[token-flow] No pools for token ${token}`);
    process.exit(2);
  }
  const intervalSec = cfg.heartbeat?.interval_seconds || 30;
  let state = loadState(stateFile);
  defaultMcpCallTimeoutIfUnset(cfg.client?.call_timeout_ms || 60000);
  console.error(`[token-flow] pools=${poolSet.size} token=${token} daemon=${daemon}`);

  async function oneRound() {
    for (const pool of poolSet) {
      let resp;
      try {
        resp = await callTool("bds_mpp_snapshot_trades_pool_address", {
          pool_address: pool,
        });
      } catch (e) {
        console.error("[token-flow] poll error", pool, e.message);
        continue;
      }
      const data = resp.data || resp;
      const trades = data.trades || [];
      const verification = data.verification || null;
      const rows = trades.map((t) => ({ poolAddress: pool, trade: t }));
      for (const tw of rows) {
        if (tradeUsd(tw) < minUsd) continue;
        const fp = fingerprintTrade(tw.trade);
        if (wasEmitted(state, fp)) continue;
        await dispatchLines(formatTokenAlert(tw, verification), channel);
        rememberFingerprint(state, fp);
      }
    }
    saveState(stateFile, state);
  }

  await oneRound();
  if (!daemon) return;

  for (;;) {
    await new Promise((r) => setTimeout(r, intervalSec * 1000));
    await oneRound();
  }
}

runPoll().catch((e) => {
  console.error(e);
  process.exit(1);
});
