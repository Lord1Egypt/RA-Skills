#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
import { z } from "zod";
// ─── Configuration ───────────────────────────────────────────────────────────
// The Graph Gateway API key (required — pay per query)
const API_KEY = process.env.GRAPH_API_KEY;
if (!API_KEY) {
    console.error("Error: GRAPH_API_KEY environment variable is required.\n" +
        "Get your API key at https://thegraph.com/studio/apikeys/\n" +
        "See: https://thegraph.com/docs/en/subgraphs/querying/managing-api-keys/");
    process.exit(1);
}
// Published subgraph IDs on The Graph Network
const SUBGRAPH_IDS = {
    orderbook: "89T2Z1tzwRB7obJZ8Mpo8N6eiBnsG1hM69VCMkfccEAZ",
    positions: "CC7fzcAvcDr1Wt2SGJzj8aYsVYbN5sr7v42ysiqLPzhd",
    yield: "96B2b2LtkgcurXTEnrSAUN5jr4T1BrfV3s5sPXNdnER8",
};
const ENDPOINTS = {
    orderbook: `https://gateway.thegraph.com/api/${API_KEY}/subgraphs/id/${SUBGRAPH_IDS.orderbook}`,
    positions: `https://gateway.thegraph.com/api/${API_KEY}/subgraphs/id/${SUBGRAPH_IDS.positions}`,
    yield: `https://gateway.thegraph.com/api/${API_KEY}/subgraphs/id/${SUBGRAPH_IDS.yield}`,
};
// ─── GraphQL Helper ──────────────────────────────────────────────────────────
async function query(endpoint, gql) {
    const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: gql }),
    });
    const json = await res.json();
    if (json.errors && !json.data) {
        throw new Error(json.errors.map((e) => e.message).join("; "));
    }
    return json.data;
}
// ─── Formatting Helpers ──────────────────────────────────────────────────────
function fmtUsd(val) {
    const n = parseFloat(val);
    if (n >= 1_000_000)
        return `$${(n / 1_000_000).toFixed(2)}M`;
    if (n >= 1_000)
        return `$${(n / 1_000).toFixed(2)}K`;
    return `$${n.toFixed(2)}`;
}
function fmtDate(timestamp) {
    return new Date(parseInt(timestamp) * 1000).toISOString().slice(0, 19) + "Z";
}
function fmtAddr(addr) {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
}
// Resolve condition/market IDs to human-readable names via NegRisk data
async function resolveMarketNames(conditionIds) {
    const names = new Map();
    if (conditionIds.length === 0)
        return names;
    // Try to find as NegRisk questions (most markets are NegRisk)
    const qFilter = conditionIds.map((id) => `"${id}"`).join(", ");
    try {
        const data = await query(ENDPOINTS.orderbook, `{ negRiskQuestions(where: { id_in: [${qFilter}] }) { id question market { id title } } negRiskMarkets(where: { id_in: [${qFilter}] }) { id title } }`);
        for (const q of data.negRiskQuestions || []) {
            names.set(q.id, q.question || q.market?.title || fmtAddr(q.id));
        }
        for (const m of data.negRiskMarkets || []) {
            if (m.title)
                names.set(m.id, m.title);
        }
    }
    catch {
        // Fallback: names stay empty, we'll show truncated IDs
    }
    return names;
}
function marketLabel(id, names) {
    return names.get(id) || fmtAddr(id);
}
// ─── Meta-Tool Constants ────────────────────────────────────────────────────
const PERSONA_THRESHOLDS = {
    whale_oi_pct: 0.10, // >10% of market OI
    whale_low_splits: 50, // market has < 50 splits
    arb_min_trades: 100,
    arb_taker_ratio: 0.70,
    early_mover_window: 86400, // 24h in seconds
    sniper_window: 172800, // 48h in seconds
    resolution_fast: 604800, // 7 days
    resolution_medium: 2592000, // 30 days
    resolution_slow: 7776000, // 90 days
    liquidity_deep_tpd: 10, // trades per day
    liquidity_thin_tpd: 1,
    dormant_seconds: 604800, // 7 days
    concentrated_top3_pct: 0.50,
};
function nowUnix() {
    return Math.floor(Date.now() / 1000);
}
function classifyResolutionLatency(createdAt, resolvedAt, resolved) {
    if (resolved && resolvedAt) {
        const s = resolvedAt - createdAt;
        const tag = s < PERSONA_THRESHOLDS.resolution_fast ? "fast" :
            s < PERSONA_THRESHOLDS.resolution_medium ? "medium" :
                s < PERSONA_THRESHOLDS.resolution_slow ? "slow" : "stale";
        return { tag, seconds: s };
    }
    const age = nowUnix() - createdAt;
    const tag = age < PERSONA_THRESHOLDS.resolution_fast ? "pending_fast" :
        age < PERSONA_THRESHOLDS.resolution_medium ? "pending_medium" :
            age < PERSONA_THRESHOLDS.resolution_slow ? "pending_slow" : "potentially_stale";
    return { tag, seconds: age };
}
function classifyLiquidity(tradeCount, volume, createdAt, lastTradeAt) {
    const ageInDays = Math.max((nowUnix() - createdAt) / 86400, 1);
    const tradesPerDay = tradeCount / ageInDays;
    const volumePerTrade = tradeCount > 0 ? volume / tradeCount : 0;
    const daysSinceLastTrade = (nowUnix() - lastTradeAt) / 86400;
    let tag;
    if (daysSinceLastTrade > 7)
        tag = "dormant";
    else if (tradesPerDay >= PERSONA_THRESHOLDS.liquidity_deep_tpd)
        tag = "deep";
    else if (tradesPerDay >= PERSONA_THRESHOLDS.liquidity_thin_tpd)
        tag = "moderate";
    else
        tag = "thin";
    return { tag, tradesPerDay: Math.round(tradesPerDay * 100) / 100, volumePerTrade: Math.round(volumePerTrade * 100) / 100, daysSinceLastTrade: Math.round(daysSinceLastTrade * 10) / 10 };
}
// ─── MCP Server ──────────────────────────────────────────────────────────────
const server = new McpServer({
    name: "predictfun-mcp",
    version: "0.1.0",
});
// ─── Tool: Platform Overview ─────────────────────────────────────────────────
server.tool("get_platform_stats", "Get Predict.fun platform-wide stats: total volume, trades, open interest, yield, and active markets", {}, async () => {
    const [ob, pos, yld] = await Promise.all([
        query(ENDPOINTS.orderbook, `{ globals { totalTrades totalVolume totalFees uniqueTraders activeMarkets tradingPaused } _meta { block { number } hasIndexingErrors } }`),
        query(ENDPOINTS.positions, `{ globals { totalSplits totalMerges totalRedemptions totalSplitVolume totalMergeVolume totalPayouts totalOpenInterest activeConditions } _meta { block { number } hasIndexingErrors } }`),
        query(ENDPOINTS.yield, `{ yieldGlobals { totalYieldClaimed totalVTokenMinted totalUnderlyingRedeemed totalRewardsClaimed yieldClaimCount rewardClaimCount } _meta { block { number } hasIndexingErrors } }`),
    ]);
    const obGlobal = ob?.globals?.[0];
    const posGlobal = pos.globals[0];
    const yldGlobal = yld.yieldGlobals[0];
    const netInVenus = parseFloat(yldGlobal.totalVTokenMinted) -
        parseFloat(yldGlobal.totalUnderlyingRedeemed);
    const lines = [
        "# Predict.fun Platform Overview",
        "",
        "## Trading",
        `- Total Trades: ${parseInt(obGlobal?.totalTrades || "0").toLocaleString()}`,
        `- Total Volume: ${fmtUsd(obGlobal?.totalVolume || "0")}`,
        `- Total Fees: ${fmtUsd(obGlobal?.totalFees || "0")}`,
        `- Unique Traders: ${parseInt(obGlobal?.uniqueTraders || "0").toLocaleString()}`,
        `- Active Markets: ${obGlobal?.activeMarkets || "N/A"}`,
        `- Trading Paused: ${obGlobal?.tradingPaused || false}`,
        "",
        "## Positions & Open Interest",
        `- Total Open Interest: ${fmtUsd(posGlobal.totalOpenInterest)}`,
        `- Active Conditions: ${posGlobal.activeConditions}`,
        `- Total Splits: ${parseInt(posGlobal.totalSplits).toLocaleString()} (${fmtUsd(posGlobal.totalSplitVolume)})`,
        `- Total Merges: ${parseInt(posGlobal.totalMerges).toLocaleString()} (${fmtUsd(posGlobal.totalMergeVolume)})`,
        `- Total Redemptions: ${parseInt(posGlobal.totalRedemptions).toLocaleString()} (${fmtUsd(posGlobal.totalPayouts)})`,
        "",
        "## Yield (Venus Protocol)",
        `- Deposited into Venus: ${fmtUsd(yldGlobal.totalVTokenMinted)}`,
        `- Redeemed from Venus: ${fmtUsd(yldGlobal.totalUnderlyingRedeemed)}`,
        `- Net Currently in Venus: ${fmtUsd(netInVenus.toString())}`,
        `- Total Yield Claimed: ${fmtUsd(yldGlobal.totalYieldClaimed)}`,
        `- Yield Claims: ${yldGlobal.yieldClaimCount}`,
        "",
        "## Sync Status",
        `- Orderbook: block ${ob?._meta?.block?.number || "N/A"} ${ob?._meta?.hasIndexingErrors ? "(has errors)" : "(healthy)"}`,
        `- Positions: block ${pos._meta.block.number} ${pos._meta.hasIndexingErrors ? "(has errors)" : "(healthy)"}`,
        `- Yield: block ${yld._meta.block.number} ${yld._meta.hasIndexingErrors ? "(has errors)" : "(healthy)"}`,
    ];
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Top Markets ───────────────────────────────────────────────────────
server.tool("get_top_markets", "Get the top prediction markets ranked by volume, open interest, or trade count", {
    rank_by: z
        .enum(["volume", "open_interest", "trades"])
        .default("volume")
        .describe("How to rank markets"),
    limit: z
        .number()
        .min(1)
        .max(50)
        .default(10)
        .describe("Number of markets to return"),
}, async ({ rank_by, limit }) => {
    let lines = [];
    if (rank_by === "open_interest") {
        const data = await query(ENDPOINTS.positions, `{ conditions(first: ${limit}, orderBy: openInterest, orderDirection: desc, where: { openInterest_gt: "0" }) { id openInterest splitCount mergeCount resolved source outcomeSlotCount } }`);
        const ids = data.conditions.map((c) => c.id);
        const names = await resolveMarketNames(ids);
        lines.push(`# Top ${limit} Markets by Open Interest\n`);
        lines.push("| # | Market | Open Interest | Splits | Merges | Resolved |");
        lines.push("|---|---|---|---|---|---|");
        data.conditions.forEach((c, i) => {
            lines.push(`| ${i + 1} | ${marketLabel(c.id, names)} | ${fmtUsd(c.openInterest)} | ${c.splitCount} | ${c.mergeCount} | ${c.resolved ? "Yes" : "No"} |`);
        });
    }
    else {
        const orderBy = rank_by === "trades" ? "tradeCount" : "volume";
        const data = await query(ENDPOINTS.orderbook, `{ markets(first: ${limit}, orderBy: ${orderBy}, orderDirection: desc) { id volume tradeCount fees exchange } }`);
        const ids = (data?.markets || []).map((m) => m.id);
        const names = await resolveMarketNames(ids);
        const label = rank_by === "trades" ? "Trade Count" : "Volume";
        lines.push(`# Top ${limit} Markets by ${label}\n`);
        lines.push("| # | Market | Volume | Trades | Fees | Exchange |");
        lines.push("|---|---|---|---|---|---|");
        (data?.markets || []).forEach((m, i) => {
            lines.push(`| ${i + 1} | ${marketLabel(m.id, names)} | ${fmtUsd(m.volume)} | ${parseInt(m.tradeCount).toLocaleString()} | ${fmtUsd(m.fees)} | ${m.exchange} |`);
        });
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Market Details ────────────────────────────────────────────────────
server.tool("get_market_details", "Get full details for a specific market/condition: volume, OI, resolution status, recent trades, top holders", {
    condition_id: z
        .string()
        .describe("The conditionId (0x hex string) of the market"),
}, async ({ condition_id }) => {
    const id = condition_id.toLowerCase();
    const [posData, obData] = await Promise.all([
        query(ENDPOINTS.positions, `{ condition(id: "${id}") { id oracle questionId outcomeSlotCount resolved payoutNumerators openInterest splitCount mergeCount createdAt resolvedAt source } marketOpenInterest(id: "${id}") { amount splitCount mergeCount lastUpdated } userPositions(first: 5, orderBy: netQuantity, orderDirection: desc, where: { condition: "${id}", netQuantity_gt: "0" }) { id user { id } netQuantity totalSplit totalMerged } }`),
        query(ENDPOINTS.orderbook, `{ market(id: "${id}") { id volume tradeCount fees exchange createdAt lastTradeAt } }`),
    ]);
    const cond = posData.condition;
    const market = obData?.market;
    const oi = posData.marketOpenInterest;
    const lines = [];
    if (!cond && !market) {
        return {
            content: [
                { type: "text", text: `No market found for conditionId: ${condition_id}` },
            ],
        };
    }
    const names = await resolveMarketNames([id]);
    const title = names.get(id);
    lines.push(`# ${title ? title : `Market ${fmtAddr(condition_id)}`}\n`);
    if (cond) {
        lines.push("## Condition");
        lines.push(`- Status: ${cond.resolved ? "**Resolved**" : "**Active**"}`);
        lines.push(`- Outcomes: ${cond.outcomeSlotCount}`);
        lines.push(`- Source: ${cond.source}`);
        lines.push(`- Oracle: ${fmtAddr(cond.oracle)}`);
        lines.push(`- Created: ${fmtDate(cond.createdAt)}`);
        if (cond.resolved) {
            lines.push(`- Resolved: ${fmtDate(cond.resolvedAt)}`);
            lines.push(`- Payouts: [${cond.payoutNumerators.join(", ")}]`);
        }
        lines.push(`- Open Interest: ${fmtUsd(cond.openInterest)}`);
        lines.push(`- Splits: ${cond.splitCount} | Merges: ${cond.mergeCount}`);
    }
    if (market) {
        lines.push("\n## Orderbook");
        lines.push(`- Volume: ${fmtUsd(market.volume)}`);
        lines.push(`- Trades: ${parseInt(market.tradeCount).toLocaleString()}`);
        lines.push(`- Fees: ${fmtUsd(market.fees)}`);
        lines.push(`- Exchange: ${market.exchange}`);
        lines.push(`- Last Trade: ${fmtDate(market.lastTradeAt)}`);
    }
    if (posData.userPositions.length > 0) {
        lines.push("\n## Top Holders");
        lines.push("| Address | Net Position | Total Split | Total Merged |");
        lines.push("|---|---|---|---|");
        posData.userPositions.forEach((p) => {
            lines.push(`| ${fmtAddr(p.user.id)} | ${fmtUsd(p.netQuantity)} | ${fmtUsd(p.totalSplit)} | ${fmtUsd(p.totalMerged)} |`);
        });
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Trader Profile ────────────────────────────────────────────────────
server.tool("get_trader_profile", "Get a trader's full profile: trading history, positions, P&L, and reward claims", {
    address: z
        .string()
        .describe("Trader wallet address (0x...)"),
}, async ({ address }) => {
    const addr = address.toLowerCase();
    const [obData, posData, yldData] = await Promise.all([
        query(ENDPOINTS.orderbook, `{ account(id: "${addr}") { id totalTrades totalVolume totalFees makerTrades takerTrades makerVolume takerVolume firstTradeAt lastTradeAt } }`),
        query(ENDPOINTS.positions, `{ account(id: "${addr}") { id splitCount mergeCount redeemCount totalSplitVolume totalMergeVolume totalPayouts firstSeenAt lastActiveAt } userPositions(first: 10, orderBy: netQuantity, orderDirection: desc, where: { user: "${addr}", netQuantity_gt: "0" }) { id netQuantity totalSplit totalMerged realizedPayout condition { id openInterest resolved } } }`),
        query(ENDPOINTS.yield, `{ yieldAccount(id: "${addr}") { id totalRewardsClaimed rewardClaimCount firstSeenAt lastActiveAt } }`),
    ]);
    const obAcct = obData?.account;
    const posAcct = posData.account;
    const yldAcct = yldData.yieldAccount;
    if (!obAcct && !posAcct && !yldAcct) {
        return {
            content: [
                { type: "text", text: `No activity found for address: ${address}` },
            ],
        };
    }
    const lines = [`# Trader ${fmtAddr(address)}\n`];
    if (obAcct) {
        const netPnl = parseFloat(posAcct?.totalPayouts || "0") -
            parseFloat(posAcct?.totalSplitVolume || "0") +
            parseFloat(posAcct?.totalMergeVolume || "0");
        lines.push("## Trading Activity");
        lines.push(`- Total Trades: ${parseInt(obAcct.totalTrades).toLocaleString()}`);
        lines.push(`- Total Volume: ${fmtUsd(obAcct.totalVolume)}`);
        lines.push(`- Fees Paid: ${fmtUsd(obAcct.totalFees)}`);
        lines.push(`- Maker: ${parseInt(obAcct.makerTrades).toLocaleString()} trades (${fmtUsd(obAcct.makerVolume)})`);
        lines.push(`- Taker: ${parseInt(obAcct.takerTrades).toLocaleString()} trades (${fmtUsd(obAcct.takerVolume)})`);
        lines.push(`- First Trade: ${fmtDate(obAcct.firstTradeAt)}`);
        lines.push(`- Last Trade: ${fmtDate(obAcct.lastTradeAt)}`);
        if (posAcct) {
            lines.push(`\n## P&L Summary`);
            lines.push(`- Total Split (bought): ${fmtUsd(posAcct.totalSplitVolume)}`);
            lines.push(`- Total Merged (sold back): ${fmtUsd(posAcct.totalMergeVolume)}`);
            lines.push(`- Realized Payouts: ${fmtUsd(posAcct.totalPayouts)}`);
            lines.push(`- Estimated Net P&L: ${fmtUsd(netPnl.toString())}`);
        }
    }
    if (posData.userPositions.length > 0) {
        const posIds = posData.userPositions.map((p) => p.condition.id);
        const posNames = await resolveMarketNames(posIds);
        lines.push("\n## Active Positions");
        lines.push("| Market | Net Position | Invested | Merged | Resolved |");
        lines.push("|---|---|---|---|---|");
        posData.userPositions.forEach((p) => {
            lines.push(`| ${marketLabel(p.condition.id, posNames)} | ${fmtUsd(p.netQuantity)} | ${fmtUsd(p.totalSplit)} | ${fmtUsd(p.totalMerged)} | ${p.condition.resolved ? "Yes" : "No"} |`);
        });
    }
    if (yldAcct) {
        lines.push("\n## Yield Rewards");
        lines.push(`- Total Rewards Claimed: ${fmtUsd(yldAcct.totalRewardsClaimed)}`);
        lines.push(`- Claim Count: ${yldAcct.rewardClaimCount}`);
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Recent Activity ──────────────────────────────────────────────────
server.tool("get_recent_activity", "Get recent activity on Predict.fun: latest trades, splits, merges, redemptions, or yield events", {
    event_type: z
        .enum(["trades", "splits", "merges", "redemptions", "yield_claims"])
        .describe("Type of activity to fetch"),
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Number of events"),
}, async ({ event_type, limit }) => {
    const lines = [];
    switch (event_type) {
        case "trades": {
            const data = await query(ENDPOINTS.orderbook, `{ orderFilledEvents(first: ${limit}, orderBy: timestamp, orderDirection: desc) { id maker { id } taker { id } makerAmountFilled takerAmountFilled fee price side exchange timestamp transactionHash } }`);
            lines.push(`# Recent ${limit} Trades\n`);
            lines.push("| Time | Side | Price | Maker Amt | Taker Amt | Fee | Exchange |");
            lines.push("|---|---|---|---|---|---|---|");
            (data?.orderFilledEvents || []).forEach((e) => {
                lines.push(`| ${fmtDate(e.timestamp)} | ${e.side} | $${parseFloat(e.price).toFixed(4)} | ${fmtUsd(e.makerAmountFilled)} | ${fmtUsd(e.takerAmountFilled)} | ${fmtUsd(e.fee)} | ${e.exchange} |`);
            });
            break;
        }
        case "splits": {
            const data = await query(ENDPOINTS.positions, `{ splitEvents(first: ${limit}, orderBy: timestamp, orderDirection: desc) { id stakeholder amount source timestamp condition { id resolved } } }`);
            const splitIds = data.splitEvents.map((e) => e.condition.id);
            const splitNames = await resolveMarketNames(splitIds);
            lines.push(`# Recent ${limit} Position Splits\n`);
            lines.push("| Time | User | Amount | Market |");
            lines.push("|---|---|---|---|");
            data.splitEvents.forEach((e) => {
                lines.push(`| ${fmtDate(e.timestamp)} | ${fmtAddr(e.stakeholder)} | ${fmtUsd(e.amount)} | ${marketLabel(e.condition.id, splitNames)} |`);
            });
            break;
        }
        case "merges": {
            const data = await query(ENDPOINTS.positions, `{ mergeEvents(first: ${limit}, orderBy: timestamp, orderDirection: desc) { id stakeholder amount source timestamp condition { id resolved } } }`);
            const mergeIds = data.mergeEvents.map((e) => e.condition.id);
            const mergeNames = await resolveMarketNames(mergeIds);
            lines.push(`# Recent ${limit} Position Merges\n`);
            lines.push("| Time | User | Amount | Market |");
            lines.push("|---|---|---|---|");
            data.mergeEvents.forEach((e) => {
                lines.push(`| ${fmtDate(e.timestamp)} | ${fmtAddr(e.stakeholder)} | ${fmtUsd(e.amount)} | ${marketLabel(e.condition.id, mergeNames)} |`);
            });
            break;
        }
        case "redemptions": {
            const data = await query(ENDPOINTS.positions, `{ redemptionEvents(first: ${limit}, orderBy: timestamp, orderDirection: desc) { id redeemer payout source timestamp condition { id payoutNumerators } } }`);
            const redeemIds = data.redemptionEvents.map((e) => e.condition.id);
            const redeemNames = await resolveMarketNames(redeemIds);
            lines.push(`# Recent ${limit} Redemptions\n`);
            lines.push("| Time | Redeemer | Payout | Market | Winner |");
            lines.push("|---|---|---|---|---|");
            data.redemptionEvents.forEach((e) => {
                const winner = e.condition.payoutNumerators
                    ? e.condition.payoutNumerators.indexOf("1") === 0
                        ? "Yes"
                        : "No"
                    : "N/A";
                lines.push(`| ${fmtDate(e.timestamp)} | ${fmtAddr(e.redeemer)} | ${fmtUsd(e.payout)} | ${marketLabel(e.condition.id, redeemNames)} | ${winner} |`);
            });
            break;
        }
        case "yield_claims": {
            const data = await query(ENDPOINTS.yield, `{ yieldClaimEvents(first: ${limit}, orderBy: timestamp, orderDirection: desc) { id underlying vToken vTokenAmount underlyingAmount timestamp transactionHash } }`);
            lines.push(`# Recent ${limit} Yield Claims\n`);
            lines.push("| Time | Underlying Amount | vToken Amount | Tx |");
            lines.push("|---|---|---|---|");
            data.yieldClaimEvents.forEach((e) => {
                lines.push(`| ${fmtDate(e.timestamp)} | ${fmtUsd(e.underlyingAmount)} | ${e.vTokenAmount} | ${fmtAddr(e.transactionHash)} |`);
            });
            break;
        }
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Yield Overview ────────────────────────────────────────────────────
server.tool("get_yield_overview", "Get Venus Protocol yield stats: deposits, redemptions, net balance, yield claims, and token mappings", {}, async () => {
    const data = await query(ENDPOINTS.yield, `{ yieldGlobals { totalYieldClaimed totalVTokenMinted totalUnderlyingRedeemed totalRewardsClaimed yieldClaimCount rewardClaimCount totalOracleRequests totalOracleSettlements } tokenMappings(first: 10) { underlying vToken enabled totalDeposited totalYieldClaimed totalVTokenMinted totalRedeemed } yieldClaimEvents(first: 5, orderBy: timestamp, orderDirection: desc) { underlyingAmount timestamp transactionHash } }`);
    const g = data.yieldGlobals[0];
    const net = parseFloat(g.totalVTokenMinted) -
        parseFloat(g.totalUnderlyingRedeemed);
    const lines = [
        "# Predict.fun Yield Overview (Venus Protocol)\n",
        "## Global Stats",
        `- Total Deposited to Venus: ${fmtUsd(g.totalVTokenMinted)}`,
        `- Total Redeemed: ${fmtUsd(g.totalUnderlyingRedeemed)}`,
        `- **Net in Venus: ${fmtUsd(net.toString())}**`,
        `- Total Yield Claimed: ${fmtUsd(g.totalYieldClaimed)}`,
        `- Yield Claim Events: ${g.yieldClaimCount}`,
        `- Reward Claims: ${g.rewardClaimCount} (${fmtUsd(g.totalRewardsClaimed)})`,
        `- Oracle Requests: ${g.totalOracleRequests}`,
        `- Oracle Settlements: ${g.totalOracleSettlements}`,
    ];
    if (data.tokenMappings.length > 0) {
        lines.push("\n## Token Mappings");
        data.tokenMappings.forEach((tm) => {
            lines.push(`\n### ${fmtAddr(tm.underlying)} → ${fmtAddr(tm.vToken)}`);
            lines.push(`- Enabled: ${tm.enabled}`);
            lines.push(`- Total Minted: ${fmtUsd(tm.totalVTokenMinted)}`);
            lines.push(`- Total Redeemed: ${fmtUsd(tm.totalRedeemed)}`);
            lines.push(`- Yield Claimed: ${fmtUsd(tm.totalYieldClaimed)}`);
        });
    }
    if (data.yieldClaimEvents.length > 0) {
        lines.push("\n## Recent Yield Claims");
        lines.push("| Time | Amount | Tx |");
        lines.push("|---|---|---|");
        data.yieldClaimEvents.forEach((e) => {
            lines.push(`| ${fmtDate(e.timestamp)} | ${fmtUsd(e.underlyingAmount)} | ${fmtAddr(e.transactionHash)} |`);
        });
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Whale Watch ──────────────────────────────────────────────────────
server.tool("get_whale_positions", "Find the largest position holders across all Predict.fun markets", {
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Number of positions to return"),
    min_position: z
        .number()
        .default(1000)
        .describe("Minimum position size in USD"),
}, async ({ limit, min_position }) => {
    const data = await query(ENDPOINTS.positions, `{ userPositions(first: ${limit}, orderBy: netQuantity, orderDirection: desc, where: { netQuantity_gt: "${min_position}" }) { id user { id totalSplitVolume totalPayouts } netQuantity totalSplit totalMerged realizedPayout condition { id openInterest resolved source } } }`);
    const whaleIds = data.userPositions.map((p) => p.condition.id);
    const whaleNames = await resolveMarketNames(whaleIds);
    const lines = [
        `# Whale Positions (min ${fmtUsd(min_position.toString())})\n`,
        "| # | Trader | Position | Market | Market OI | % of OI |",
        "|---|---|---|---|---|---|",
    ];
    data.userPositions.forEach((p, i) => {
        const pctOi = parseFloat(p.condition.openInterest) > 0
            ? ((parseFloat(p.netQuantity) /
                parseFloat(p.condition.openInterest)) *
                100).toFixed(1)
            : "N/A";
        lines.push(`| ${i + 1} | ${fmtAddr(p.user.id)} | ${fmtUsd(p.netQuantity)} | ${marketLabel(p.condition.id, whaleNames)} | ${fmtUsd(p.condition.openInterest)} | ${pctOi}% |`);
    });
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Market Leaderboard ────────────────────────────────────────────────
server.tool("get_leaderboard", "Get the top traders on Predict.fun by volume, P&L, or trade count", {
    rank_by: z
        .enum(["volume", "payouts", "trades"])
        .default("volume")
        .describe("How to rank traders"),
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Number of traders"),
}, async ({ rank_by, limit }) => {
    const lines = [];
    if (rank_by === "payouts") {
        const data = await query(ENDPOINTS.positions, `{ accounts(first: ${limit}, orderBy: totalPayouts, orderDirection: desc, where: { totalPayouts_gt: "0" }) { id splitCount mergeCount redeemCount totalSplitVolume totalMergeVolume totalPayouts } }`);
        lines.push(`# Top ${limit} Traders by Payouts\n`);
        lines.push("| # | Trader | Payouts | Invested | Merged | Redemptions | Est. P&L |");
        lines.push("|---|---|---|---|---|---|---|");
        data.accounts.forEach((a, i) => {
            const pnl = parseFloat(a.totalPayouts) +
                parseFloat(a.totalMergeVolume) -
                parseFloat(a.totalSplitVolume);
            lines.push(`| ${i + 1} | ${fmtAddr(a.id)} | ${fmtUsd(a.totalPayouts)} | ${fmtUsd(a.totalSplitVolume)} | ${fmtUsd(a.totalMergeVolume)} | ${a.redeemCount} | ${fmtUsd(pnl.toString())} |`);
        });
    }
    else {
        const orderBy = rank_by === "trades" ? "totalTrades" : "totalVolume";
        const data = await query(ENDPOINTS.orderbook, `{ accounts(first: ${limit}, orderBy: ${orderBy}, orderDirection: desc) { id totalTrades totalVolume totalFees makerTrades takerTrades } }`);
        const label = rank_by === "trades" ? "Trades" : "Volume";
        lines.push(`# Top ${limit} Traders by ${label}\n`);
        lines.push("| # | Trader | Volume | Trades | Fees | Maker | Taker |");
        lines.push("|---|---|---|---|---|---|---|");
        (data?.accounts || []).forEach((a, i) => {
            lines.push(`| ${i + 1} | ${fmtAddr(a.id)} | ${fmtUsd(a.totalVolume)} | ${parseInt(a.totalTrades).toLocaleString()} | ${fmtUsd(a.totalFees)} | ${parseInt(a.makerTrades).toLocaleString()} | ${parseInt(a.takerTrades).toLocaleString()} |`);
        });
    }
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Resolved Markets ─────────────────────────────────────────────────
server.tool("get_resolved_markets", "Get recently resolved markets with their outcomes and payout info", {
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Number of resolved markets"),
}, async ({ limit }) => {
    const data = await query(ENDPOINTS.positions, `{ conditions(first: ${limit}, orderBy: resolvedAt, orderDirection: desc, where: { resolved: true }) { id outcomeSlotCount payoutNumerators openInterest splitCount mergeCount createdAt resolvedAt source } }`);
    const resolvedIds = data.conditions.map((c) => c.id);
    const resolvedNames = await resolveMarketNames(resolvedIds);
    const lines = [
        `# Recently Resolved Markets\n`,
        "| # | Market | Winning | OI at Resolution | Splits | Resolved At |",
        "|---|---|---|---|---|---|",
    ];
    data.conditions.forEach((c, i) => {
        const winIdx = c.payoutNumerators.indexOf("1");
        const winner = winIdx === 0 ? "Outcome A (Yes)" : winIdx === 1 ? "Outcome B (No)" : `Outcome ${winIdx}`;
        lines.push(`| ${i + 1} | ${marketLabel(c.id, resolvedNames)} | ${winner} | ${fmtUsd(c.openInterest)} | ${c.splitCount} | ${fmtDate(c.resolvedAt)} |`);
    });
    return { content: [{ type: "text", text: lines.join("\n") }] };
});
// ─── Tool: Custom Query ──────────────────────────────────────────────────────
server.tool("query_subgraph", "Run a custom GraphQL query against any Predict.fun subgraph. Use this for advanced queries not covered by other tools.", {
    subgraph: z
        .enum(["orderbook", "positions", "yield"])
        .describe("Which subgraph to query"),
    graphql_query: z
        .string()
        .describe("The GraphQL query string"),
}, async ({ subgraph, graphql_query }) => {
    const endpoint = ENDPOINTS[subgraph];
    const data = await query(endpoint, graphql_query);
    return {
        content: [
            { type: "text", text: JSON.stringify(data, null, 2) },
        ],
    };
});
// ─── Meta-Tool: Find Trader Persona ─────────────────────────────────────────
server.tool("find_trader_persona", "Classify a trader into behavioral archetypes: whale_accumulator, yield_farmer, arbitrageur, early_mover, or resolution_sniper. Returns structured JSON with matched personas and supporting metrics.", {
    address: z.string().describe("Trader wallet address (0x...)"),
}, async ({ address }) => {
    const addr = address.toLowerCase();
    // Parallel queries across all 3 subgraphs
    const [obData, posData, yldData, positionsData] = await Promise.all([
        query(ENDPOINTS.orderbook, `{ account(id: "${addr}") { id totalTrades totalVolume totalFees makerTrades takerTrades makerVolume takerVolume firstTradeAt lastTradeAt } }`),
        query(ENDPOINTS.positions, `{ account(id: "${addr}") { id splitCount mergeCount redeemCount totalSplitVolume totalMergeVolume totalPayouts firstSeenAt lastActiveAt } }`),
        query(ENDPOINTS.yield, `{ yieldAccount(id: "${addr}") { id totalRewardsClaimed rewardClaimCount } }`),
        query(ENDPOINTS.positions, `{ userPositions(first: 50, orderBy: netQuantity, orderDirection: desc, where: { user: "${addr}", netQuantity_gt: "0" }) { id netQuantity totalSplit condition { id openInterest resolved splitCount createdAt resolvedAt } } }`),
    ]);
    const obAcct = obData?.account;
    const posAcct = posData?.account;
    const yldAcct = yldData?.yieldAccount;
    const positions = positionsData?.userPositions || [];
    if (!obAcct && !posAcct && !yldAcct) {
        return {
            content: [{ type: "text", text: JSON.stringify({ error: "No activity found", address }) }],
        };
    }
    const personas = [];
    // 1. Whale Accumulator: >10% of market OI in low-activity markets
    for (const p of positions) {
        const oi = parseFloat(p.condition.openInterest);
        const net = parseFloat(p.netQuantity);
        if (oi > 0) {
            const pctOi = net / oi;
            const splits = parseInt(p.condition.splitCount);
            if (pctOi >= PERSONA_THRESHOLDS.whale_oi_pct && splits < PERSONA_THRESHOLDS.whale_low_splits) {
                personas.push({
                    persona: "whale_accumulator",
                    confidence: pctOi > 0.25 ? "high" : "medium",
                    evidence: {
                        condition_id: p.condition.id,
                        position_size: net,
                        market_oi: oi,
                        pct_of_oi: Math.round(pctOi * 1000) / 10,
                        market_splits: splits,
                    },
                });
                break; // One match is enough
            }
        }
    }
    // 2. Yield Farmer: active reward claims
    if (yldAcct && parseInt(yldAcct.rewardClaimCount) > 2 && parseFloat(yldAcct.totalRewardsClaimed) > 0) {
        personas.push({
            persona: "yield_farmer",
            confidence: parseInt(yldAcct.rewardClaimCount) > 10 ? "high" : "medium",
            evidence: {
                total_rewards_claimed: parseFloat(yldAcct.totalRewardsClaimed),
                claim_count: parseInt(yldAcct.rewardClaimCount),
            },
        });
    }
    // 3. Arbitrageur: high frequency, small avg size, taker-heavy
    if (obAcct) {
        const trades = parseInt(obAcct.totalTrades);
        const volume = parseFloat(obAcct.totalVolume);
        const takerTrades = parseInt(obAcct.takerTrades);
        if (trades >= PERSONA_THRESHOLDS.arb_min_trades) {
            const avgSize = volume / trades;
            const takerRatio = takerTrades / trades;
            if (takerRatio >= PERSONA_THRESHOLDS.arb_taker_ratio && avgSize < 500) {
                personas.push({
                    persona: "arbitrageur",
                    confidence: trades > 500 && takerRatio > 0.85 ? "high" : "medium",
                    evidence: {
                        total_trades: trades,
                        avg_trade_size: Math.round(avgSize * 100) / 100,
                        taker_ratio: Math.round(takerRatio * 1000) / 10,
                        total_volume: volume,
                    },
                });
            }
        }
    }
    // 4. Early Mover: entered positions within 24h of market creation
    for (const p of positions) {
        if (parseFloat(p.totalSplit) > 0) {
            // Check if there are splits from this user near market creation
            try {
                const splitData = await query(ENDPOINTS.positions, `{ splitEvents(first: 1, orderBy: timestamp, orderDirection: asc, where: { stakeholder: "${addr}", condition: "${p.condition.id}" }) { timestamp } }`);
                const firstSplit = splitData?.splitEvents?.[0];
                if (firstSplit) {
                    const condCreated = parseInt(p.condition.createdAt);
                    const splitTime = parseInt(firstSplit.timestamp);
                    const delta = splitTime - condCreated;
                    if (delta >= 0 && delta <= PERSONA_THRESHOLDS.early_mover_window) {
                        personas.push({
                            persona: "early_mover",
                            confidence: delta < 3600 ? "high" : "medium",
                            evidence: {
                                condition_id: p.condition.id,
                                market_created_at: condCreated,
                                first_split_at: splitTime,
                                seconds_after_creation: delta,
                            },
                        });
                        break;
                    }
                }
            }
            catch {
                // Skip if query fails
            }
        }
    }
    // 5. Resolution Sniper: large splits within 48h before resolution
    const resolvedPositions = positions.filter((p) => p.condition.resolved && p.condition.resolvedAt);
    for (const p of resolvedPositions.slice(0, 5)) {
        const resolvedAt = parseInt(p.condition.resolvedAt);
        const windowStart = resolvedAt - PERSONA_THRESHOLDS.sniper_window;
        try {
            const splitData = await query(ENDPOINTS.positions, `{ splitEvents(first: 3, orderBy: amount, orderDirection: desc, where: { stakeholder: "${addr}", condition: "${p.condition.id}", timestamp_gt: "${windowStart}", timestamp_lt: "${resolvedAt}" }) { amount timestamp } }`);
            if (splitData?.splitEvents?.length > 0) {
                const totalLateSplits = splitData.splitEvents.reduce((sum, s) => sum + parseFloat(s.amount), 0);
                if (totalLateSplits > 100) {
                    personas.push({
                        persona: "resolution_sniper",
                        confidence: totalLateSplits > 1000 ? "high" : "medium",
                        evidence: {
                            condition_id: p.condition.id,
                            resolved_at: resolvedAt,
                            late_split_volume: Math.round(totalLateSplits * 100) / 100,
                            splits_in_window: splitData.splitEvents.length,
                        },
                    });
                    break;
                }
            }
        }
        catch {
            // Skip
        }
    }
    const result = {
        address: addr,
        personas_matched: personas.length,
        personas,
        summary: {
            total_trades: obAcct ? parseInt(obAcct.totalTrades) : 0,
            total_volume: obAcct ? parseFloat(obAcct.totalVolume) : 0,
            active_positions: positions.length,
            has_yield_activity: !!yldAcct,
        },
    };
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
});
// ─── Meta-Tool: Scan Trader Personas ────────────────────────────────────────
server.tool("scan_trader_personas", "Find traders matching a specific behavioral archetype across the platform. Returns structured JSON with matching traders and evidence.", {
    persona: z
        .enum(["whale_accumulator", "yield_farmer", "arbitrageur", "early_mover", "resolution_sniper"])
        .describe("The trader archetype to scan for"),
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Max number of traders to return"),
}, async ({ persona, limit }) => {
    const results = [];
    switch (persona) {
        case "whale_accumulator": {
            const data = await query(ENDPOINTS.positions, `{ userPositions(first: 50, orderBy: netQuantity, orderDirection: desc, where: { netQuantity_gt: "1000" }) { user { id } netQuantity condition { id openInterest splitCount } } }`);
            for (const p of data?.userPositions || []) {
                if (results.length >= limit)
                    break;
                const oi = parseFloat(p.condition.openInterest);
                const net = parseFloat(p.netQuantity);
                const splits = parseInt(p.condition.splitCount);
                if (oi > 0 && net / oi >= PERSONA_THRESHOLDS.whale_oi_pct && splits < PERSONA_THRESHOLDS.whale_low_splits) {
                    results.push({
                        address: p.user.id,
                        evidence: {
                            position_size: net,
                            market_oi: oi,
                            pct_of_oi: Math.round((net / oi) * 1000) / 10,
                            condition_id: p.condition.id,
                            market_splits: splits,
                        },
                    });
                }
            }
            break;
        }
        case "yield_farmer": {
            const data = await query(ENDPOINTS.yield, `{ yieldAccounts(first: ${limit}, orderBy: totalRewardsClaimed, orderDirection: desc, where: { rewardClaimCount_gt: "1" }) { id totalRewardsClaimed rewardClaimCount } }`);
            for (const a of data?.yieldAccounts || []) {
                results.push({
                    address: a.id,
                    evidence: {
                        total_rewards_claimed: parseFloat(a.totalRewardsClaimed),
                        claim_count: parseInt(a.rewardClaimCount),
                    },
                });
            }
            break;
        }
        case "arbitrageur": {
            const data = await query(ENDPOINTS.orderbook, `{ accounts(first: 50, orderBy: totalTrades, orderDirection: desc) { id totalTrades totalVolume takerTrades } }`);
            for (const a of data?.accounts || []) {
                if (results.length >= limit)
                    break;
                const trades = parseInt(a.totalTrades);
                const volume = parseFloat(a.totalVolume);
                const takerTrades = parseInt(a.takerTrades);
                if (trades >= PERSONA_THRESHOLDS.arb_min_trades) {
                    const avgSize = volume / trades;
                    const takerRatio = takerTrades / trades;
                    if (takerRatio >= PERSONA_THRESHOLDS.arb_taker_ratio && avgSize < 500) {
                        results.push({
                            address: a.id,
                            evidence: {
                                total_trades: trades,
                                avg_trade_size: Math.round(avgSize * 100) / 100,
                                taker_ratio: Math.round(takerRatio * 1000) / 10,
                                total_volume: volume,
                            },
                        });
                    }
                }
            }
            break;
        }
        case "early_mover": {
            // Find recently created markets and their first participants
            const now = nowUnix();
            const recentCutoff = now - 30 * 86400; // last 30 days
            const condData = await query(ENDPOINTS.positions, `{ conditions(first: 20, orderBy: createdAt, orderDirection: desc, where: { createdAt_gt: "${recentCutoff}" }) { id createdAt } }`);
            const seen = new Set();
            for (const cond of condData?.conditions || []) {
                if (results.length >= limit)
                    break;
                const splitData = await query(ENDPOINTS.positions, `{ splitEvents(first: 5, orderBy: timestamp, orderDirection: asc, where: { condition: "${cond.id}", timestamp_lt: "${parseInt(cond.createdAt) + PERSONA_THRESHOLDS.early_mover_window}" }) { stakeholder timestamp amount } }`);
                for (const s of splitData?.splitEvents || []) {
                    if (results.length >= limit)
                        break;
                    if (seen.has(s.stakeholder))
                        continue;
                    seen.add(s.stakeholder);
                    results.push({
                        address: s.stakeholder,
                        evidence: {
                            condition_id: cond.id,
                            market_created_at: parseInt(cond.createdAt),
                            split_at: parseInt(s.timestamp),
                            seconds_after_creation: parseInt(s.timestamp) - parseInt(cond.createdAt),
                            amount: parseFloat(s.amount),
                        },
                    });
                }
            }
            break;
        }
        case "resolution_sniper": {
            const condData = await query(ENDPOINTS.positions, `{ conditions(first: 20, orderBy: resolvedAt, orderDirection: desc, where: { resolved: true }) { id resolvedAt } }`);
            const seen = new Set();
            for (const cond of condData?.conditions || []) {
                if (results.length >= limit)
                    break;
                const resolvedAt = parseInt(cond.resolvedAt);
                const windowStart = resolvedAt - PERSONA_THRESHOLDS.sniper_window;
                const splitData = await query(ENDPOINTS.positions, `{ splitEvents(first: 10, orderBy: amount, orderDirection: desc, where: { condition: "${cond.id}", timestamp_gt: "${windowStart}", timestamp_lt: "${resolvedAt}" }) { stakeholder amount timestamp } }`);
                for (const s of splitData?.splitEvents || []) {
                    if (results.length >= limit)
                        break;
                    if (seen.has(s.stakeholder))
                        continue;
                    seen.add(s.stakeholder);
                    if (parseFloat(s.amount) > 100) {
                        results.push({
                            address: s.stakeholder,
                            evidence: {
                                condition_id: cond.id,
                                resolved_at: resolvedAt,
                                split_amount: parseFloat(s.amount),
                                seconds_before_resolution: resolvedAt - parseInt(s.timestamp),
                            },
                        });
                    }
                }
            }
            break;
        }
    }
    const output = {
        persona,
        traders_found: results.length,
        traders: results,
    };
    return { content: [{ type: "text", text: JSON.stringify(output, null, 2) }] };
});
// ─── Meta-Tool: Tag Market Structure ────────────────────────────────────────
server.tool("tag_market_structure", "Classify a market by structural features: resolution latency, liquidity profile, oracle type, and tail-risk indicators. Returns structured JSON.", {
    condition_id: z.string().describe("The conditionId (0x hex string) of the market"),
}, async ({ condition_id }) => {
    const id = condition_id.toLowerCase();
    // Parallel queries across subgraphs
    const [posData, obData, topHolders] = await Promise.all([
        query(ENDPOINTS.positions, `{ condition(id: "${id}") { id oracle questionId outcomeSlotCount resolved openInterest splitCount mergeCount createdAt resolvedAt source } }`),
        query(ENDPOINTS.orderbook, `{ market(id: "${id}") { id volume tradeCount fees createdAt lastTradeAt exchange } }`),
        query(ENDPOINTS.positions, `{ userPositions(first: 5, orderBy: netQuantity, orderDirection: desc, where: { condition: "${id}", netQuantity_gt: "0" }) { user { id } netQuantity } }`),
    ]);
    const cond = posData?.condition;
    const market = obData?.market;
    const holders = topHolders?.userPositions || [];
    if (!cond && !market) {
        return {
            content: [{ type: "text", text: JSON.stringify({ error: "Market not found", condition_id }) }],
        };
    }
    const tags = {};
    // 1. Resolution Latency
    if (cond) {
        const createdAt = parseInt(cond.createdAt);
        const resolvedAt = cond.resolvedAt ? parseInt(cond.resolvedAt) : null;
        const latency = classifyResolutionLatency(createdAt, resolvedAt, cond.resolved);
        tags.resolution_latency = {
            tag: latency.tag,
            resolved: cond.resolved,
            age_seconds: latency.seconds,
            age_days: latency.seconds ? Math.round((latency.seconds / 86400) * 10) / 10 : null,
            created_at: createdAt,
            resolved_at: resolvedAt,
        };
    }
    // 2. Liquidity Profile
    if (market) {
        const liquidity = classifyLiquidity(parseInt(market.tradeCount), parseFloat(market.volume), parseInt(market.createdAt), parseInt(market.lastTradeAt));
        tags.liquidity_profile = {
            tag: liquidity.tag,
            trades_per_day: liquidity.tradesPerDay,
            volume_per_trade: liquidity.volumePerTrade,
            days_since_last_trade: liquidity.daysSinceLastTrade,
            total_trades: parseInt(market.tradeCount),
            total_volume: parseFloat(market.volume),
            total_fees: parseFloat(market.fees),
        };
    }
    // 3. Oracle Type
    if (cond) {
        let oracleTag = "standard";
        if (cond.source.includes("NegRisk")) {
            oracleTag = "neg_risk";
        }
        // Check if oracle is a UMA oracle by looking for oracle requests
        try {
            const oracleData = await query(ENDPOINTS.yield, `{ oracleRequests(first: 1, where: { requester: "${cond.oracle}" }) { id settled } }`);
            if (oracleData?.oracleRequests?.length > 0) {
                oracleTag = "uma_oracle";
            }
        }
        catch {
            // Keep existing tag
        }
        tags.oracle_type = {
            tag: oracleTag,
            oracle_address: cond.oracle,
            source: cond.source,
            outcome_slots: parseInt(cond.outcomeSlotCount),
        };
    }
    // 4. Tail-Risk Indicators
    if (cond) {
        const oi = parseFloat(cond.openInterest);
        const volume = market ? parseFloat(market.volume) : 0;
        // OI concentration: top 3 holders share
        let top3Pct = 0;
        if (oi > 0 && holders.length > 0) {
            const top3Sum = holders
                .slice(0, 3)
                .reduce((sum, h) => sum + parseFloat(h.netQuantity), 0);
            top3Pct = top3Sum / oi;
        }
        const oiVolumeRatio = volume > 0 ? oi / volume : null;
        const concentrated = top3Pct >= PERSONA_THRESHOLDS.concentrated_top3_pct;
        tags.tail_risk = {
            concentrated_oi: concentrated,
            top_3_holders_pct: Math.round(top3Pct * 1000) / 10,
            top_holders: holders.slice(0, 3).map((h) => ({
                address: h.user.id,
                position: parseFloat(h.netQuantity),
            })),
            oi_volume_ratio: oiVolumeRatio ? Math.round(oiVolumeRatio * 1000) / 1000 : null,
            open_interest: oi,
            flags: [
                ...(concentrated ? ["concentrated_oi"] : []),
                ...(oiVolumeRatio && oiVolumeRatio > 1 ? ["illiquid_exit"] : []),
            ],
        };
    }
    const result = {
        condition_id: id,
        market_name: (await resolveMarketNames([id])).get(id) || null,
        tags,
    };
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
});
// ─── Meta-Tool: Scan Markets by Structure ───────────────────────────────────
server.tool("scan_markets_by_structure", "Find markets matching structural criteria: resolution speed, liquidity depth, oracle type, or tail-risk flags. Returns structured JSON.", {
    filter: z
        .enum([
        "fast_resolution", "slow_resolution", "stale",
        "deep_liquidity", "thin_liquidity", "dormant",
        "uma_oracle", "concentrated_oi", "high_tail_risk",
    ])
        .describe("Structural filter to apply"),
    resolved_only: z
        .boolean()
        .default(false)
        .describe("Only include resolved markets (required for resolution filters)"),
    limit: z
        .number()
        .min(1)
        .max(25)
        .default(10)
        .describe("Number of markets to return"),
}, async ({ filter, resolved_only, limit }) => {
    const markets = [];
    switch (filter) {
        case "fast_resolution":
        case "slow_resolution":
        case "stale": {
            const data = await query(ENDPOINTS.positions, `{ conditions(first: 50, orderBy: resolvedAt, orderDirection: desc, where: { resolved: true }) { id createdAt resolvedAt openInterest splitCount source } }`);
            const targetRange = filter === "fast_resolution" ? [0, PERSONA_THRESHOLDS.resolution_fast] :
                filter === "slow_resolution" ? [PERSONA_THRESHOLDS.resolution_medium, PERSONA_THRESHOLDS.resolution_slow] :
                    [PERSONA_THRESHOLDS.resolution_slow, Infinity];
            const matched = (data?.conditions || []).filter((c) => {
                const latency = parseInt(c.resolvedAt) - parseInt(c.createdAt);
                return latency >= targetRange[0] && latency < targetRange[1];
            });
            const ids = matched.slice(0, limit).map((c) => c.id);
            const names = await resolveMarketNames(ids);
            for (const c of matched.slice(0, limit)) {
                const latency = parseInt(c.resolvedAt) - parseInt(c.createdAt);
                markets.push({
                    condition_id: c.id,
                    name: names.get(c.id) || null,
                    metrics: {
                        resolution_days: Math.round((latency / 86400) * 10) / 10,
                        open_interest: parseFloat(c.openInterest),
                        splits: parseInt(c.splitCount),
                        source: c.source,
                    },
                });
            }
            break;
        }
        case "deep_liquidity":
        case "thin_liquidity":
        case "dormant": {
            const orderBy = filter === "deep_liquidity" ? "tradeCount" : "createdAt";
            const direction = filter === "deep_liquidity" ? "desc" : "desc";
            const data = await query(ENDPOINTS.orderbook, `{ markets(first: 50, orderBy: ${orderBy}, orderDirection: ${direction}) { id volume tradeCount fees createdAt lastTradeAt } }`);
            for (const m of data?.markets || []) {
                if (markets.length >= limit)
                    break;
                const liq = classifyLiquidity(parseInt(m.tradeCount), parseFloat(m.volume), parseInt(m.createdAt), parseInt(m.lastTradeAt));
                if ((filter === "deep_liquidity" && liq.tag === "deep") ||
                    (filter === "thin_liquidity" && liq.tag === "thin") ||
                    (filter === "dormant" && liq.tag === "dormant")) {
                    markets.push({
                        condition_id: m.id,
                        name: null, // resolved below
                        metrics: {
                            liquidity_tag: liq.tag,
                            trades_per_day: liq.tradesPerDay,
                            volume_per_trade: liq.volumePerTrade,
                            days_since_last_trade: liq.daysSinceLastTrade,
                            total_volume: parseFloat(m.volume),
                            total_trades: parseInt(m.tradeCount),
                        },
                    });
                }
            }
            // Resolve names
            const ids = markets.map((m) => m.condition_id);
            const names = await resolveMarketNames(ids);
            for (const m of markets) {
                m.name = names.get(m.condition_id) || null;
            }
            break;
        }
        case "uma_oracle": {
            // Find oracle addresses from yield subgraph, then match to conditions
            const oracleData = await query(ENDPOINTS.yield, `{ oracleRequests(first: 50, orderBy: createdAt, orderDirection: desc) { id requester settled settledAt } }`);
            const oracleAddresses = [...new Set((oracleData?.oracleRequests || []).map((o) => o.requester))];
            if (oracleAddresses.length > 0) {
                const oracleFilter = oracleAddresses.slice(0, 10).map((a) => `"${a}"`).join(", ");
                const condData = await query(ENDPOINTS.positions, `{ conditions(first: ${limit}, orderBy: openInterest, orderDirection: desc, where: { oracle_in: [${oracleFilter}]${resolved_only ? ", resolved: true" : ""} }) { id oracle openInterest resolved splitCount createdAt resolvedAt } }`);
                const ids = (condData?.conditions || []).map((c) => c.id);
                const names = await resolveMarketNames(ids);
                for (const c of condData?.conditions || []) {
                    markets.push({
                        condition_id: c.id,
                        name: names.get(c.id) || null,
                        metrics: {
                            oracle_address: c.oracle,
                            open_interest: parseFloat(c.openInterest),
                            resolved: c.resolved,
                            splits: parseInt(c.splitCount),
                        },
                    });
                }
            }
            break;
        }
        case "concentrated_oi":
        case "high_tail_risk": {
            const condData = await query(ENDPOINTS.positions, `{ conditions(first: 30, orderBy: openInterest, orderDirection: desc, where: { openInterest_gt: "100"${resolved_only ? ", resolved: true" : ""} }) { id openInterest splitCount source } }`);
            for (const cond of condData?.conditions || []) {
                if (markets.length >= limit)
                    break;
                const oi = parseFloat(cond.openInterest);
                const holdersData = await query(ENDPOINTS.positions, `{ userPositions(first: 3, orderBy: netQuantity, orderDirection: desc, where: { condition: "${cond.id}", netQuantity_gt: "0" }) { user { id } netQuantity } }`);
                const holders = holdersData?.userPositions || [];
                const top3Sum = holders.reduce((sum, h) => sum + parseFloat(h.netQuantity), 0);
                const top3Pct = oi > 0 ? top3Sum / oi : 0;
                const isConcentrated = top3Pct >= PERSONA_THRESHOLDS.concentrated_top3_pct;
                if (filter === "concentrated_oi" && isConcentrated) {
                    markets.push({
                        condition_id: cond.id,
                        name: null,
                        metrics: {
                            top_3_holders_pct: Math.round(top3Pct * 1000) / 10,
                            open_interest: oi,
                            top_holders: holders.map((h) => ({
                                address: h.user.id,
                                position: parseFloat(h.netQuantity),
                            })),
                        },
                    });
                }
                else if (filter === "high_tail_risk") {
                    // Check both concentration and OI/volume ratio
                    let obMarket = null;
                    try {
                        const obData = await query(ENDPOINTS.orderbook, `{ market(id: "${cond.id}") { volume } }`);
                        obMarket = obData?.market;
                    }
                    catch { /* skip */ }
                    const volume = obMarket ? parseFloat(obMarket.volume) : 0;
                    const oiVolumeRatio = volume > 0 ? oi / volume : 999;
                    if (isConcentrated || oiVolumeRatio > 1) {
                        markets.push({
                            condition_id: cond.id,
                            name: null,
                            metrics: {
                                top_3_holders_pct: Math.round(top3Pct * 1000) / 10,
                                oi_volume_ratio: Math.round(oiVolumeRatio * 1000) / 1000,
                                open_interest: oi,
                                volume,
                                risk_flags: [
                                    ...(isConcentrated ? ["concentrated_oi"] : []),
                                    ...(oiVolumeRatio > 1 ? ["illiquid_exit"] : []),
                                ],
                            },
                        });
                    }
                }
            }
            // Resolve names
            const allIds = markets.map((m) => m.condition_id);
            if (allIds.length > 0) {
                const names = await resolveMarketNames(allIds);
                for (const m of markets) {
                    m.name = names.get(m.condition_id) || null;
                }
            }
            break;
        }
    }
    const output = {
        filter,
        resolved_only,
        markets_found: markets.length,
        markets,
    };
    return { content: [{ type: "text", text: JSON.stringify(output, null, 2) }] };
});
// ─── Prompts ─────────────────────────────────────────────────────────────────
server.prompt("platform_overview", "Get a full overview of the Predict.fun platform", () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: "Give me a full overview of Predict.fun — platform stats, top markets, biggest whales, and yield status. Use get_platform_stats, get_top_markets, get_whale_positions, and get_yield_overview.",
            },
        },
    ],
}));
server.prompt("analyze_trader", "Analyze a specific trader's activity and P&L", { address: z.string().describe("Trader wallet address (0x...)") }, ({ address }) => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: `Analyze trader ${address} on Predict.fun. Use get_trader_profile to get their full trading history, positions, and P&L. Then check if they appear on the leaderboard with get_leaderboard. Summarize whether they're profitable, what markets they're active in, and their trading style (maker vs taker).`,
            },
        },
    ],
}));
server.prompt("market_deep_dive", "Deep dive into a specific prediction market", { condition_id: z.string().describe("Market conditionId (0x...)") }, ({ condition_id }) => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: `Do a deep dive on Predict.fun market ${condition_id}. Use get_market_details for the full picture — volume, open interest, resolution status, and top holders. Then use get_recent_activity with type "trades" to see latest activity. Analyze: Is this market active? Who are the biggest participants? Is the OI growing or shrinking?`,
            },
        },
    ],
}));
server.prompt("yield_analysis", "Analyze Predict.fun's Venus Protocol yield mechanics", () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: "Analyze Predict.fun's yield-bearing mechanics. Use get_yield_overview to see Venus Protocol deposits, redemptions, and yield claims. Also use get_platform_stats for context on total OI vs yield deposits. Calculate the yield APY based on the claim data. How much of the platform's collateral is earning yield?",
            },
        },
    ],
}));
server.prompt("whale_alert", "Find the biggest players and their market positions", () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: "Show me the whales on Predict.fun. Use get_whale_positions with a minimum of $10,000. Then use get_leaderboard ranked by payouts to find the most profitable traders. For the top 3 whales, use get_trader_profile to understand their strategies. Are they concentrated in specific markets or diversified?",
            },
        },
    ],
}));
server.prompt("market_scanner", "Scan for interesting markets — highest volume, most OI, recently resolved", () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: "Scan the Predict.fun markets for me. Use get_top_markets ranked by volume (top 10), then by open_interest (top 10), then by trades (top 10). Also use get_resolved_markets to see the 5 most recently resolved markets and their outcomes. Which markets are the most active right now? Any with unusually high OI relative to volume?",
            },
        },
    ],
}));
server.prompt("custom_query_examples", "Show example GraphQL queries for each Predict.fun subgraph", () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: `Show me example custom GraphQL queries I can run with query_subgraph. Here are some useful ones:

**Orderbook** — Recent large trades (>$1000):
\`\`\`graphql
{ orderFilledEvents(first: 10, orderBy: timestamp, orderDirection: desc, where: { makerAmountFilled_gt: "1000" }) { maker { id } taker { id } makerAmountFilled price side exchange timestamp } }
\`\`\`

**Positions** — All positions for a specific market:
\`\`\`graphql
{ userPositions(first: 50, where: { condition: "0x1141...", netQuantity_gt: "0" }, orderBy: netQuantity, orderDirection: desc) { user { id } netQuantity totalSplit totalMerged } }
\`\`\`

**Positions** — Markets created in the last 24 hours:
\`\`\`graphql
{ conditions(first: 20, orderBy: createdAt, orderDirection: desc, where: { createdAt_gt: "UNIX_TIMESTAMP" }) { id outcomeSlotCount openInterest source createdAt } }
\`\`\`

**Yield** — Token mapping details:
\`\`\`graphql
{ tokenMappings { underlying vToken enabled totalVTokenMinted totalRedeemed totalYieldClaimed } }
\`\`\`

**Positions** — NegRisk conversion events:
\`\`\`graphql
{ negRiskConversionEvents(first: 10, orderBy: timestamp, orderDirection: desc) { stakeholder marketId indexSet amount source timestamp } }
\`\`\`

Run any of these with the query_subgraph tool, specifying the subgraph name and the query.`,
            },
        },
    ],
}));
server.prompt("trader_persona_analysis", "Classify traders by behavioral archetypes and find similar traders", { address: z.string().optional().describe("Optional: specific trader address to classify") }, ({ address }) => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: address
                    ? `Classify trader ${address} into behavioral archetypes on Predict.fun. Use find_trader_persona to detect if they match: whale_accumulator, yield_farmer, arbitrageur, early_mover, or resolution_sniper. Then use get_trader_profile for their full trading history. Based on their persona, use scan_trader_personas to find similar traders. Summarize their strategy and how they compare to others.`
                    : `Scan the Predict.fun platform for interesting trader archetypes. Use scan_trader_personas for each persona type: whale_accumulator, yield_farmer, arbitrageur, early_mover, and resolution_sniper. Compare the results — which personas are most common? Are there traders who appear in multiple categories? Use get_trader_profile on the most interesting ones to build a full picture.`,
            },
        },
    ],
}));
server.prompt("market_quality_scan", "Scan markets by structural quality indicators to find opportunities or risks", {}, () => ({
    messages: [
        {
            role: "user",
            content: {
                type: "text",
                text: `Perform a structural quality scan of Predict.fun markets. Run these scans in sequence:

1. Use scan_markets_by_structure with filter "deep_liquidity" to find the most actively traded markets.
2. Use scan_markets_by_structure with filter "concentrated_oi" to find markets where a few whales dominate.
3. Use scan_markets_by_structure with filter "high_tail_risk" to identify markets with exit liquidity concerns.
4. Use scan_markets_by_structure with filter "dormant" to find markets that may be abandoned.
5. Use scan_markets_by_structure with filter "fast_resolution" to see which markets resolved quickly.

For the most interesting markets from each scan, use tag_market_structure to get the full structural breakdown. Summarize: Which markets are highest quality (deep liquidity, distributed OI, active trading)? Which are risky (concentrated, illiquid, stale)?`,
            },
        },
    ],
}));
// ─── HTTP/SSE Transport ─────────────────────────────────────────────────────
function startHttpTransport(port) {
    const app = express();
    const sessions = new Map();
    app.get("/sse", async (req, res) => {
        const transport = new SSEServerTransport("/messages", res);
        sessions.set(transport.sessionId, transport);
        res.on("close", () => {
            sessions.delete(transport.sessionId);
        });
        await server.connect(transport);
    });
    app.post("/messages", async (req, res) => {
        const sessionId = req.query.sessionId;
        const transport = sessions.get(sessionId);
        if (!transport) {
            res.status(400).json({ error: "Invalid or expired session" });
            return;
        }
        await transport.handlePostMessage(req, res);
    });
    app.get("/health", (_req, res) => {
        res.json({ status: "ok", server: "predictfun-mcp" });
    });
    app.listen(port, () => {
        console.error(`SSE transport listening on http://localhost:${port}/sse`);
    });
}
// ─── Start Server ────────────────────────────────────────────────────────────
async function main() {
    const httpPort = process.env.MCP_HTTP_PORT || (process.argv.includes("--http") ? "3850" : null);
    const httpOnly = process.argv.includes("--http-only");
    if (httpPort || httpOnly) {
        const port = parseInt(httpPort || "3850", 10);
        startHttpTransport(port);
    }
    if (!httpOnly) {
        const transport = new StdioServerTransport();
        await server.connect(transport);
    }
    console.error("predictfun-mcp running");
}
main().catch(console.error);
