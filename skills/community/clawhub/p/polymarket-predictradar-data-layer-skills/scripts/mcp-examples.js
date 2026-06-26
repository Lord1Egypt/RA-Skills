/**
 * mcp-examples.js — PredicTradar MCP client examples
 *
 * Usage:
 *   node scripts/mcp-examples.js           # run all examples
 *   node scripts/mcp-examples.js health    # only health + handshake
 *   node scripts/mcp-examples.js query     # schema + preview SQL examples
 *   node scripts/mcp-examples.js tools     # tool catalog + high-level tools
 *   node scripts/mcp-examples.js addr 0x.. # inspect a trader
 */

"use strict";

const mcp = require("./mcp-client");

function formatNumber(n, decimals = 2) {
  if (n === null || n === undefined) return "-";
  const num = parseFloat(n);
  if (Number.isNaN(num)) return n;
  if (Math.abs(num) >= 1e9) return (num / 1e9).toFixed(decimals) + "B";
  if (Math.abs(num) >= 1e6) return (num / 1e6).toFixed(decimals) + "M";
  if (Math.abs(num) >= 1e3) return (num / 1e3).toFixed(decimals) + "K";
  return num.toFixed(decimals);
}

function printSection(title) {
  console.log("\n" + "=".repeat(64));
  console.log(`  ${title}`);
  console.log("=".repeat(64));
}

async function exampleHealth() {
  printSection("Health And Session Handshake");

  console.log("\n1. MCP ping:");
  const pingOk = await mcp.ping();
  console.log(`   Status: ${pingOk ? "OK" : "FAILED"}`);

  console.log("\n2. REST health endpoint:");
  const health = await mcp.health();
  if (health) {
    console.log(`   Service: ${health.service}`);
    console.log(`   Version: ${health.version}`);
    console.log(`   Protocol: ${health.protocolVersion}`);
    console.log(`   Active Sessions: ${health.activeSessions}`);
  } else {
    console.log("   Health check failed");
  }

  console.log("\n3. MCP initialize:");
  const info = await mcp.initialize();
  console.log(`   Session ID: ${info.sessionId}`);
  console.log(`   Server: ${info.serverInfo.name} v${info.serverInfo.version}`);
  console.log(`   Tools enabled: ${info.capabilities.tools ? "yes" : "no"}`);
  console.log(`   Batch enabled: ${info.capabilities.batch?.enabled ? "yes" : "no"}`);
}

async function exampleListTools() {
  printSection("Available Tools");

  const tools = await mcp.listTools();
  console.log(`\nTotal tools: ${tools.length}\n`);

  for (const tool of tools) {
    const params = Object.keys(tool.inputSchema?.properties || {});
    console.log(`  - ${tool.name}`);
    console.log(`    ${tool.description}`);
    console.log(`    params: ${params.join(", ") || "(none)"}`);
  }
}

async function exampleQuery() {
  printSection("Schema And Query Examples");

  console.log("\n1. Trading tables:");
  const tables = await mcp.listTables("trading");
  for (const table of tables) {
    console.log(`   - ${table.name}: ${formatNumber(table.rowCount, 0)} rows`);
    console.log(`     ${table.description}`);
  }

  console.log("\n2. trades schema preview:");
  const tradesSchema = await mcp.describeTable("trades", true);
  console.log(`   Columns: ${tradesSchema.columnCount}`);
  console.log(
    `   Key fields: ${tradesSchema.columns
      .slice(0, 10)
      .map((c) => c.name)
      .join(", ")}`,
  );

  console.log("\n3. 24h trade preview:");
  const stats24h = await mcp.query(`
    SELECT
      count(*) AS total_trades,
      SUM(amount) AS total_volume,
      COUNT(DISTINCT wallet_address) AS unique_traders
    FROM trades
    WHERE traded_at >= now() - INTERVAL 1 DAY
      AND type = 'trade'
  `);
  const s = stats24h[0] || {};
  console.log(`   Trades: ${formatNumber(s.total_trades, 0)}`);
  console.log(`   Volume: $${formatNumber(s.total_volume)}`);
  console.log(`   Unique Traders: ${formatNumber(s.unique_traders, 0)}`);

  console.log("\n4. Stream export preview:");
  const stream = await mcp.openQueryStream(
    `
    SELECT condition_id, SUM(amount) AS volume_24h
    FROM trades
    WHERE traded_at >= now() - INTERVAL 1 DAY
      AND type = 'trade'
    GROUP BY condition_id
    ORDER BY volume_24h DESC
    LIMIT 5
  `,
    { previewRows: 3, format: "ndjson" },
  );
  console.log(`   Stream URL: ${stream.streamUrl}`);
  console.log(`   Expires At: ${stream.expiresAt}`);
  console.log(`   Preview Rows: ${stream.preview?.length || 0}`);
}

async function exampleHighLevelTools() {
  printSection("High-Level Tool Examples");

  console.log("\n1. get_market_stats:");
  const stats = await mcp.getMarketStats("24h");
  console.log(`   Total Markets: ${formatNumber(stats.markets.total, 0)}`);
  console.log(`   Active Markets: ${formatNumber(stats.markets.active, 0)}`);
  console.log(`   Total Traders: ${formatNumber(stats.traders.total, 0)}`);
  console.log(`   24h Volume: $${formatNumber(stats.volume.last24h)}`);

  if (stats.hotMarkets?.length) {
    console.log("\n   Hot markets:");
    for (const market of stats.hotMarkets.slice(0, 3)) {
      console.log(`   - ${market.question.slice(0, 60)}...`);
      console.log(`     24h Volume: $${formatNumber(market.volume24h)}`);
    }
  }

  console.log("\n2. get_leaderboard:");
  const leaderboard = await mcp.getLeaderboard({
    period: "7d",
    rankBy: "pnl",
    limit: 5,
  });
  for (const item of leaderboard.list || []) {
    const trader = item.trader || {};
    const summary = item.stats || {};
    console.log(
      `   #${item.rank} ${trader.username || trader.walletAddress?.slice(0, 10) + "..."} | PnL $${formatNumber(summary.totalPnl)} | Win Rate ${summary.winRate}%`,
    );
  }

  console.log("\n3. get_traders:");
  const traders = await mcp.getTraders({
    sortBy: "pnl_7d",
    order: "desc",
    limit: 3,
  });
  for (const trader of traders.list || []) {
    const statsRow = Array.isArray(trader.stats) ? trader.stats[0] : trader.stats;
    console.log(
      `   - ${trader.username || trader.walletAddress?.slice(0, 10) + "..."} | PnL $${formatNumber(statsRow?.totalPnl)} | Win Rate ${statsRow?.winRate ?? "-"}`,
    );
  }

  console.log("\n4. get_market_detail:");
  const markets = await mcp.getMarkets({ status: "active", limit: 1 });
  const first = Array.isArray(markets.list) ? markets.list[0] : markets[0];
  const conditionId = first?.conditionId || first?.condition_id;
  if (conditionId) {
    const detail = await mcp.getMarketDetail(conditionId);
    console.log(`   Condition ID: ${conditionId}`);
    console.log(`   Question: ${detail.question || detail.market?.question || "-"}`);
  } else {
    console.log("   No active market returned to inspect");
  }
}

async function exampleAddressQuery(address) {
  printSection(`Trader Detail: ${address.slice(0, 10)}...`);

  console.log("\n1. get_trader_detail:");
  try {
    const detail = await mcp.getTraderDetail(address);
    const trader = detail.trader || {};
    const stats = detail.stats || {};
    console.log(`   Username: ${trader.username || "-"}`);
    console.log(`   Platform: ${trader.platform || "-"}`);
    console.log(`   Smart Money: ${trader.isSmartMoney ? "Yes" : "No"}`);
    console.log(`   Total PnL: $${formatNumber(stats.totalPnl)}`);
    console.log(`   Win Rate: ${stats.winRate ?? "-"}%`);
    console.log(`   Total Volume: $${formatNumber(stats.totalVolume)}`);
  } catch (error) {
    console.log(`   Error: ${error.message}`);
  }

  console.log("\n2. positions preview:");
  const positions = await mcp.query(`
    SELECT
      market_id,
      outcome_side,
      size,
      current_value,
      unrealized_pnl,
      is_closed
    FROM positions
    WHERE lower(wallet_address) = lower('${address}')
      AND is_closed = 0
    ORDER BY current_value DESC
    LIMIT 5
  `);

  if (!positions.length) {
    console.log("   No open positions found");
    return;
  }

  for (const position of positions) {
    console.log(`   - Market: ${position.market_id?.slice(0, 12) || "-"}...`);
    console.log(
      `     Side: ${position.outcome_side} | Value: $${formatNumber(position.current_value)} | PnL: $${formatNumber(position.unrealized_pnl)}`,
    );
  }
}

async function main() {
  const cmd = process.argv[2];

  console.log("PredicTradar MCP Client Examples");
  console.log(`Server: ${mcp.MCP_BASE_URL}`);

  try {
    if (!cmd || cmd === "health") {
      await exampleHealth();
    }

    if (!cmd || cmd === "tools") {
      await exampleListTools();
      await exampleHighLevelTools();
    }

    if (!cmd || cmd === "query") {
      await exampleQuery();
    }

    if (cmd === "addr" && process.argv[3]) {
      await exampleAddressQuery(process.argv[3]);
    }

    console.log("\nOK: all examples completed\n");
  } catch (error) {
    console.error(`\nFAILED: ${error.message}`);
    process.exit(1);
  }
}

main();
