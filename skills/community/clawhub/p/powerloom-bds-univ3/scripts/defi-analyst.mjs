#!/usr/bin/env node
/**
 * Autonomous DeFi Analyst — default: multi-pool via `bds_mpp_snapshot_allTrades` + token all-pools volume.
 * `filters.scope: single_pool` → one pool snapshots only. **Default:** one round then exit (cron). **`--daemon`** → repeat every `heartbeat.interval_seconds`.
 */

import { callTool } from "./lib/mcp.mjs";
import { loadRecipe } from "./lib/recipe-config.mjs";
import { tradeUsd, flattenAllTradesFromSnapshot } from "./lib/trade-utils.mjs";
import { loadState, saveState } from "./lib/state.mjs";
import { dispatchLines } from "./lib/dispatch.mjs";
import { defaultMcpCallTimeoutIfUnset } from "./lib/powerloom-env.mjs";

const USDC_MAINNET = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";

const arg = (name) => {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
};

const defaults = {
  name: "defi-analyst",
  heartbeat: { interval_seconds: 300 },
  filters: {
    scope: "multi",
    volume_token_address: USDC_MAINNET,
    pool_address: "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
    project_id: "uniswapv3.eth-usdc-0.05",
  },
  client: { call_timeout_ms: 90000, snapshot_max_events: 50 },
  verification: { mode: "sampled", sample_probability: 0.2 },
  dispatch: { channel: "stdout" },
};

const cfg = loadRecipe("defi-analyst.yaml", defaults);
const scope = (cfg.filters?.scope || "multi").toLowerCase();
const pool = cfg.filters?.pool_address || defaults.filters.pool_address;
const projectId = cfg.filters?.project_id || defaults.filters.project_id;
const volumeToken =
  (cfg.filters?.volume_token_address || USDC_MAINNET).toLowerCase();
const intervalSec = cfg.heartbeat?.interval_seconds || 300;
const pVerify = Math.min(
  1,
  Math.max(0, cfg.verification?.sample_probability ?? 0.2)
);
const channel = cfg.dispatch?.channel || "stdout";
const snapshotMaxEvents = cfg.client?.snapshot_max_events ?? 50;
const stateFile =
  arg("--state-file") ||
  process.env.DEFI_ANALYST_STATE_FILE ||
  ".powerloom/defi-analyst-state.json";

function epochIdFromSnapshot(data) {
  const e = data?.epoch;
  if (e && typeof e.end === "number") return e.end;
  if (e && typeof e.begin === "number") return e.begin;
  return null;
}

function pickTopTrade(trades) {
  let best = null;
  let bestUsd = -1;
  for (const t of trades || []) {
    const w = { trade: t };
    const u = tradeUsd(w);
    if (u > bestUsd) {
      bestUsd = u;
      best = t;
    }
  }
  return best;
}

function tradeDirection(t) {
  const a0 = parseFloat(String(t.data?.amount0 ?? "0"));
  return a0 < 0 ? "sell" : "buy";
}

async function oneRoundMulti() {
  defaultMcpCallTimeoutIfUnset(cfg.client?.call_timeout_ms || 90000);

  let vol;
  try {
    vol = await callTool("bds_mpp_tradeVolumeAllPools_token_address_time_interval", {
      token_address: volumeToken,
      time_interval: 3600,
    });
  } catch (e) {
    vol = { error: e.message };
  }

  const eth = await callTool("bds_mpp_ethPrice", {});
  let state = loadState(stateFile);
  const params = { max_events: snapshotMaxEvents };
  if (state.lastStreamEpoch != null) params.from_epoch = state.lastStreamEpoch;

  let result;
  try {
    result = await callTool("bds_mpp_snapshot_allTrades", params);
  } catch (e) {
    await dispatchLines(
      [
        `Powerloom DeFi Analyst (multi-pool) — ${new Date().toISOString()}`,
        `bds_mpp_snapshot_allTrades error: ${e.message}`,
      ],
      channel,
    );
    return;
  }

  const data = result?.data ?? result;
  if (!data) {
    await dispatchLines(
      [
        `Powerloom DeFi Analyst (multi-pool) — ${new Date().toISOString()}`,
        "empty snapshot",
      ],
      channel,
    );
    return;
  }

  const verificationTop = data.verification || null;
  const epochEnd = data.epoch?.end ?? data.epoch?.begin ?? null;
  const rows = flattenAllTradesFromSnapshot(data);

  let bestTw = null;
  let bestUsd = -1;
  for (const tw of rows) {
    const u = tradeUsd(tw);
    if (u > bestUsd) {
      bestUsd = u;
      bestTw = tw;
    }
  }

  if (epochEnd != null && typeof epochEnd === "number") {
    if (epochEnd > (state.lastStreamEpoch ?? 0)) {
      state.lastStreamEpoch = epochEnd;
    } else {
      state.lastStreamEpoch = epochEnd + 1;
    }
    saveState(stateFile, state);
  }

  const volData = vol?.data ?? vol;
  const ethData = eth.data || eth;
  const lines = [
    `Powerloom DeFi Analyst (multi-pool) — ${new Date().toISOString()}`,
    `scope  snapshot_allTrades  max_events=${snapshotMaxEvents}  (all indexed pools)`,
    `volume_token  ${volumeToken}  (1h all-pools)`,
    `volume_1h  ${JSON.stringify(volData?.tradeVolume ?? volData ?? {})}`,
    `eth_price  ${JSON.stringify(ethData?.price ?? ethData ?? {})}`,
  ];

  if (bestTw) {
    const t = bestTw.trade;
    const pAddr = bestTw.poolAddress || "?";
    lines.push(
      `top_trade_in_snapshot  pool ${pAddr}  ${tradeDirection(t)}  $${tradeUsd(bestTw).toFixed(2)}  tx ${t?.log?.transactionHash || ""}`
    );
  } else {
    lines.push("top_trade_in_snapshot  (no trades in this snapshot)");
  }

  const top = bestTw?.trade;
  const doVerify = Math.random() < pVerify && top;
  if (doVerify && top?.log?.cid) {
    const eid =
      verificationTop?.epochId ??
      epochIdFromSnapshot(data) ??
      null;
    if (eid != null) {
      try {
        const vr = await callTool("verify_data_provenance", {
          cid: top.log.cid,
          epoch_id: eid,
          project_id: projectId,
        });
        lines.push("verification_probe");
        lines.push(JSON.stringify(vr, null, 2));
      } catch (e) {
        lines.push(`verification_probe  error: ${e.message}`);
      }
    } else {
      lines.push(
        "verification_probe  skipped (could not derive epoch_id from snapshot)",
      );
    }
  } else if (doVerify) {
    lines.push(
      "verification_probe  skipped (no cid on trade log in snapshot)",
    );
  }

  await dispatchLines(lines, channel);
}

async function oneRoundSinglePool() {
  defaultMcpCallTimeoutIfUnset(90000);

  const vol = await callTool("bds_mpp_tradeVolume_pool_address_time_interval", {
    pool_address: pool,
    time_interval: 3600,
  });
  const eth = await callTool("bds_mpp_ethPrice", {});
  const snap = await callTool("bds_mpp_snapshot_trades_pool_address", {
    pool_address: pool,
  });

  const data = snap.data || snap;
  const trades = data.trades || [];
  const top = pickTopTrade(trades);
  const volData = vol.data || vol;
  const ethData = eth.data || eth;

  const lines = [
    `Powerloom DeFi Analyst (single-pool) — ${new Date().toISOString()}`,
    `pool       ${pool}`,
    `volume_1h  ${JSON.stringify(volData?.tradeVolume ?? volData ?? {})}`,
    `eth_price  ${JSON.stringify(ethData?.price ?? ethData ?? {})}`,
  ];
  if (top) {
    const d = top.data || {};
    lines.push(
      `top_trade  ${tradeDirection(top)}  $${tradeUsd({ trade: top }).toFixed(2)}  tx ${top.log?.transactionHash || ""}`
    );
  }

  const doVerify = Math.random() < pVerify;
  if (doVerify && top?.log?.cid) {
    const eid = epochIdFromSnapshot(data);
    if (eid != null) {
      try {
        const vr = await callTool("verify_data_provenance", {
          cid: top.log.cid,
          epoch_id: eid,
          project_id: projectId,
        });
        lines.push("verification_probe");
        lines.push(JSON.stringify(vr, null, 2));
      } catch (e) {
        lines.push(`verification_probe  error: ${e.message}`);
      }
    } else {
      lines.push(
        "verification_probe  skipped (could not derive epoch_id from snapshot; check pool snapshot shape)"
      );
    }
  } else if (doVerify) {
    lines.push(
      "verification_probe  skipped (no cid on trade log — upstream snapshot may omit it)"
    );
  }

  await dispatchLines(lines, channel);
}

async function oneRound() {
  if (scope === "single_pool") {
    await oneRoundSinglePool();
  } else {
    await oneRoundMulti();
  }
}

async function main() {
  const daemon = process.argv.includes("--daemon");
  await oneRound();
  if (!daemon) return;
  setInterval(() => {
    oneRound().catch((e) => console.error("[defi-analyst]", e.message));
  }, intervalSec * 1000);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
