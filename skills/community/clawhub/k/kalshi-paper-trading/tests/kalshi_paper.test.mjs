import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn, spawnSync } from "node:child_process";
import http from "node:http";
import { once } from "node:events";
import { DatabaseSync } from "node:sqlite";

const __dirname = dirname(fileURLToPath(import.meta.url));
const scriptPath = resolve(__dirname, "../scripts/kalshi_paper.ts");

function mkTmpDbPath(prefix = "kalshi-paper-test-") {
  const dir = mkdtempSync(join(tmpdir(), prefix));
  return { dir, db: join(dir, "kalshi-paper.db") };
}

function runCli(args, dbPath, extraEnv = {}) {
  const res = spawnSync(
    process.execPath,
    ["--experimental-strip-types", scriptPath, "--db", dbPath, ...args],
    { encoding: "utf8", env: { ...process.env, ...extraEnv } },
  );
  return {
    code: res.status ?? 1,
    stdout: res.stdout ?? "",
    stderr: res.stderr ?? "",
  };
}

async function runCliAsync(args, dbPath, extraEnv = {}) {
  const child = spawn(
    process.execPath,
    ["--experimental-strip-types", scriptPath, "--db", dbPath, ...args],
    { env: { ...process.env, ...extraEnv } },
  );

  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => {
    stdout += String(chunk);
  });
  child.stderr.on("data", (chunk) => {
    stderr += String(chunk);
  });

  const [code] = await once(child, "close");
  return {
    code: code ?? 1,
    stdout,
    stderr,
  };
}

function runOk(args, dbPath, extraEnv = {}) {
  const out = runCli(args, dbPath, extraEnv);
  assert.equal(out.code, 0, `Expected success. stderr:\n${out.stderr}\nstdout:\n${out.stdout}`);
  return out;
}

function runFail(args, dbPath, extraEnv = {}) {
  const out = runCli(args, dbPath, extraEnv);
  assert.notEqual(out.code, 0, `Expected failure. stdout:\n${out.stdout}`);
  return out;
}

function parseJsonStdout(stdout) {
  return JSON.parse(stdout.trim());
}

function assertAlmostEqual(actual, expected, epsilon = 1e-9) {
  assert.ok(
    Math.abs(actual - expected) <= epsilon,
    `Expected ${actual} to be within ${epsilon} of ${expected}`,
  );
}

test("init creates account and duplicate init fails", () => {
  const { dir, db } = mkTmpDbPath();
  try {
    runOk(["init", "--account", "kalshi", "--starting-balance-usd", "1000"], db);
    const dup = runFail(["init", "--account", "kalshi", "--starting-balance-usd", "1000"], db);
    assert.match(dup.stderr, /already exists/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("status values YES positions from cent-based marks", () => {
  const { dir, db } = mkTmpDbPath();
  try {
    runOk(["init", "--starting-balance-usd", "1000"], db);
    runOk(
      [
        "buy",
        "--market",
        "KXBTC-TEST-1",
        "--event",
        "KXBTC-TEST",
        "--series",
        "KXBTC",
        "--side",
        "YES",
        "--contracts",
        "10",
        "--price-cents",
        "84",
      ],
      db,
    );
    runOk(
      [
        "mark",
        "--market",
        "KXBTC-TEST-1",
        "--yes-bid-cents",
        "86",
        "--yes-ask-cents",
        "88",
      ],
      db,
    );

    const status = runOk(["status", "--format", "json"], db);
    const payload = parseJsonStdout(status.stdout);

    assertAlmostEqual(payload.summary.cashUsd, 991.6);
    assertAlmostEqual(payload.summary.openMarkValueUsd, 8.7);
    assertAlmostEqual(payload.summary.unrealizedPnlUsd, 0.3);
    assertAlmostEqual(payload.summary.equityUsd, 1000.3);
    assert.equal(payload.positions[0].avgEntryCents, 84);
    assert.equal(payload.positions[0].markCents, 87);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("sell realizes pnl and reduces open contracts", () => {
  const { dir, db } = mkTmpDbPath();
  try {
    runOk(["init", "--starting-balance-usd", "1000"], db);
    runOk(
      ["buy", "--market", "KXETH-TEST-1", "--side", "YES", "--contracts", "10", "--price-cents", "40"],
      db,
    );
    runOk(
      ["sell", "--market", "KXETH-TEST-1", "--side", "YES", "--contracts", "4", "--price-cents", "65"],
      db,
    );
    runOk(
      ["mark", "--market", "KXETH-TEST-1", "--yes-bid-cents", "50", "--yes-ask-cents", "54"],
      db,
    );

    const status = runOk(["status", "--format", "json"], db);
    const payload = parseJsonStdout(status.stdout);

    assertAlmostEqual(payload.summary.realizedPnlUsd, 1);
    assert.equal(payload.summary.openPositions, 1);
    assert.equal(payload.positions[0].contracts, 6);
    assert.equal(payload.positions[0].avgEntryCents, 40);
    assert.equal(payload.positions[0].markCents, 52);
    assertAlmostEqual(payload.summary.unrealizedPnlUsd, 0.72);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("reconcile settles both YES winner and NO loser positions", () => {
  const { dir, db } = mkTmpDbPath();
  try {
    runOk(["init", "--starting-balance-usd", "1000"], db);
    runOk(
      ["buy", "--market", "KXINX-TEST-1", "--side", "YES", "--contracts", "5", "--price-cents", "35"],
      db,
    );
    runOk(
      ["buy", "--market", "KXINX-TEST-1", "--side", "NO", "--contracts", "2", "--price-cents", "55"],
      db,
    );
    runOk(
      ["reconcile", "--market", "KXINX-TEST-1", "--winning-side", "YES"],
      db,
    );

    const status = runOk(["status", "--format", "json"], db);
    const payload = parseJsonStdout(status.stdout);

    assert.equal(payload.summary.openPositions, 0);
    assert.equal(payload.summary.closedTrades, 2);
    assertAlmostEqual(payload.summary.realizedPnlUsd, 2.15);
    assertAlmostEqual(payload.summary.cashUsd, 1002.15);
    assertAlmostEqual(payload.summary.equityUsd, 1002.15);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("buy rejects out-of-range cent prices", () => {
  const { dir, db } = mkTmpDbPath();
  try {
    runOk(["init", "--starting-balance-usd", "1000"], db);
    const out = runFail(
      ["buy", "--market", "KXBTC-TEST-2", "--side", "YES", "--contracts", "1", "--price-cents", "101"],
      db,
    );
    assert.match(out.stderr, /price-cents must be between 0 and 100/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("sync-market fetches a live-style Kalshi quote and stores a midpoint mark", async () => {
  const { dir, db } = mkTmpDbPath();
  const server = http.createServer((req, res) => {
    if (req.url !== "/trade-api/v2/markets/KXBTC-TEST-3") {
      res.writeHead(404, { "content-type": "application/json" });
      res.end(JSON.stringify({ error: "not found" }));
      return;
    }

    res.writeHead(200, { "content-type": "application/json" });
    res.end(
      JSON.stringify({
        market: {
          ticker: "KXBTC-TEST-3",
          event_ticker: "KXBTC-TEST",
          status: "active",
          close_time: "2026-03-13T21:00:00Z",
          yes_bid: 7,
          yes_ask: 12,
          last_price: 10,
        },
      }),
    );
  });

  try {
    server.listen(0, "127.0.0.1");
    await once(server, "listening");
    const address = server.address();
    assert.ok(address && typeof address === "object");
    const baseUrl = `http://127.0.0.1:${address.port}/trade-api/v2`;

    const out = await runCliAsync(["sync-market", "--market", "KXBTC-TEST-3", "--format", "json"], db, {
      KALSHI_BASE_URL: baseUrl,
    });
    assert.equal(out.code, 0, `Expected success. stderr:\n${out.stderr}\nstdout:\n${out.stdout}`);
    const payload = parseJsonStdout(out.stdout);

    assert.equal(payload.marketTicker, "KXBTC-TEST-3");
    assert.equal(payload.status, "open");
    assert.equal(payload.yesBidCents, 7);
    assert.equal(payload.yesAskCents, 12);
    assert.equal(payload.markCents, 10);
    assert.equal(payload.markMethod, "mid");

    const verify = new DatabaseSync(db);
    const row = verify
      .prepare(
        "SELECT market_ticker, status, yes_bid_cents, yes_ask_cents, last_yes_trade_cents, mark_method, mark_cents, raw_json FROM market_marks WHERE market_ticker = ?",
      )
      .get("KXBTC-TEST-3");
    verify.close();

    assert.equal(row.market_ticker, "KXBTC-TEST-3");
    assert.equal(row.status, "open");
    assert.equal(row.yes_bid_cents, 7);
    assert.equal(row.yes_ask_cents, 12);
    assert.equal(row.last_yes_trade_cents, 10);
    assert.equal(row.mark_method, "mid");
    assert.equal(row.mark_cents, 10);
    assert.match(row.raw_json, /KXBTC-TEST-3/);
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    rmSync(dir, { recursive: true, force: true });
  }
});

test("buy-from-market syncs quote, buys at ask, and returns updated status", async () => {
  const { dir, db } = mkTmpDbPath();
  const server = http.createServer((req, res) => {
    if (req.url !== "/trade-api/v2/markets/KXETH-TEST-4") {
      res.writeHead(404, { "content-type": "application/json" });
      res.end(JSON.stringify({ error: "not found" }));
      return;
    }

    res.writeHead(200, { "content-type": "application/json" });
    res.end(
      JSON.stringify({
        market: {
          ticker: "KXETH-TEST-4",
          event_ticker: "KXETH-TEST",
          status: "active",
          close_time: "2026-03-14T21:00:00Z",
          yes_bid: 21,
          yes_ask: 24,
          no_bid: 76,
          no_ask: 79,
          last_price: 22,
        },
      }),
    );
  });

  try {
    runOk(["init", "--account", "demo", "--starting-balance-usd", "1000"], db);

    server.listen(0, "127.0.0.1");
    await once(server, "listening");
    const address = server.address();
    assert.ok(address && typeof address === "object");
    const baseUrl = `http://127.0.0.1:${address.port}/trade-api/v2`;

    const out = await runCliAsync(
      [
        "buy-from-market",
        "--account",
        "demo",
        "--market",
        "KXETH-TEST-4",
        "--side",
        "YES",
        "--contracts",
        "5",
        "--format",
        "json",
      ],
      db,
      { KALSHI_BASE_URL: baseUrl },
    );
    assert.equal(out.code, 0, `Expected success. stderr:\n${out.stderr}\nstdout:\n${out.stdout}`);
    const payload = parseJsonStdout(out.stdout);

    assert.equal(payload.trade.marketTicker, "KXETH-TEST-4");
    assert.equal(payload.trade.contractSide, "YES");
    assert.equal(payload.trade.contracts, 5);
    assert.equal(payload.trade.priceCents, 24);
    assert.equal(payload.mark.markCents, 23);
    assert.equal(payload.mark.markMethod, "mid");
    assert.equal(payload.status.summary.openPositions, 1);
    assertAlmostEqual(payload.status.summary.cashUsd, 998.8);
    assertAlmostEqual(payload.status.summary.openMarkValueUsd, 1.15);
    assertAlmostEqual(payload.status.summary.unrealizedPnlUsd, -0.05);
    assert.equal(payload.status.positions[0].avgEntryCents, 24);
    assert.equal(payload.status.positions[0].markCents, 23);

    const verify = new DatabaseSync(db);
    const execution = verify
      .prepare(
        "SELECT market_ticker, event_ticker, series_ticker, contract_side, action, contracts, price_cents, source FROM executions WHERE market_ticker = ?",
      )
      .get("KXETH-TEST-4");
    const mark = verify
      .prepare(
        "SELECT market_ticker, yes_bid_cents, yes_ask_cents, mark_method, mark_cents FROM market_marks WHERE market_ticker = ?",
      )
      .get("KXETH-TEST-4");
    verify.close();

    assert.equal(execution.market_ticker, "KXETH-TEST-4");
    assert.equal(execution.event_ticker, "KXETH-TEST");
    assert.equal(execution.series_ticker, "KXETH");
    assert.equal(execution.contract_side, "YES");
    assert.equal(execution.action, "BUY");
    assert.equal(execution.contracts, 5);
    assert.equal(execution.price_cents, 24);
    assert.equal(execution.source, "sync-market");
    assert.equal(mark.market_ticker, "KXETH-TEST-4");
    assert.equal(mark.yes_bid_cents, 21);
    assert.equal(mark.yes_ask_cents, 24);
    assert.equal(mark.mark_method, "mid");
    assert.equal(mark.mark_cents, 23);
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    rmSync(dir, { recursive: true, force: true });
  }
});
