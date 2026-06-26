#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { homedir } from "node:os";
import { dirname, resolve } from "node:path";

type ContractSide = "YES" | "NO";
type ExecutionAction = "BUY" | "SELL";
type MarkMethod = "mid" | "bid" | "last_trade" | "settlement" | "unknown";
type MarketStatus = "open" | "closed" | "finalized";
type KalshiApiMarketStatus = "active" | "closed" | "finalized" | "settled" | string;
type KalshiMarketPayload = {
  ticker?: string;
  event_ticker?: string;
  status?: KalshiApiMarketStatus;
  close_time?: string | null;
  yes_bid?: number | null;
  yes_ask?: number | null;
  no_bid?: number | null;
  no_ask?: number | null;
  last_price?: number | null;
  yes_bid_dollars?: string | number | null;
  yes_ask_dollars?: string | number | null;
  no_bid_dollars?: string | number | null;
  no_ask_dollars?: string | number | null;
  last_price_dollars?: string | number | null;
  result?: string | null;
};

type CliMap = {
  _: string[];
  [key: string]: string | boolean | string[];
};

type AccountRow = {
  id: string;
  name: string;
  base_currency: string;
  starting_balance_usd: number;
  created_at: string;
};

type ExecutionRow = {
  market_ticker: string;
  event_ticker: string | null;
  series_ticker: string | null;
  contract_side: ContractSide;
  action: ExecutionAction;
  contracts: number;
  price_cents: number;
  fee_usd: number;
  created_at: string;
};

type OpenPosition = {
  marketTicker: string;
  eventTicker: string | null;
  seriesTicker: string | null;
  contractSide: ContractSide;
  contracts: number;
  avgEntryCents: number;
  openFeesRemainingUsd: number;
};

type PositionMetrics = {
  realizedPnlUsd: number;
  closedCount: number;
  wins: number;
  losses: number;
};

type MarketMark = {
  marketTicker: string;
  status: MarketStatus;
  closeTimeUtc: string | null;
  settlementSide: ContractSide | null;
  yesBidCents: number | null;
  yesAskCents: number | null;
  lastYesTradeCents: number | null;
  markMethod: MarkMethod;
  markCents: number | null;
  updatedAt: string;
};

const DEFAULT_DB = `${homedir()}/.openclaw/kalshi-paper.db`;

function nowIso(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function parseArgs(argv: string[]): CliMap {
  const out: CliMap = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      out._.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out[key] = true;
      continue;
    }

    out[key] = next;
    i += 1;
  }
  return out;
}

function asString(value: unknown, field: string): string {
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`${field} is required`);
  }
  return value.trim();
}

function asNumber(value: unknown, field: string): number {
  const num = Number(value);
  if (!Number.isFinite(num)) {
    throw new Error(`${field} must be a number`);
  }
  return num;
}

function asOptionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function parseContractSide(value: unknown): ContractSide {
  const side = asString(value, "side").toUpperCase();
  if (side !== "YES" && side !== "NO") {
    throw new Error("side must be YES or NO");
  }
  return side;
}

function parseMarketStatus(value: unknown, field = "status"): MarketStatus {
  const status = asString(value, field).toLowerCase();
  if (status !== "open" && status !== "closed" && status !== "finalized") {
    throw new Error(`${field} must be open, closed, or finalized`);
  }
  return status;
}

function parseMarkMethod(value: unknown): MarkMethod {
  const method = asString(value, "mark-method").toLowerCase();
  if (
    method !== "mid" &&
    method !== "bid" &&
    method !== "last_trade" &&
    method !== "settlement" &&
    method !== "unknown"
  ) {
    throw new Error("mark-method must be mid, bid, last_trade, settlement, or unknown");
  }
  return method;
}

function printJson(value: unknown, pretty = false): void {
  console.log(JSON.stringify(value, null, pretty ? 2 : undefined));
}

function asInteger(value: unknown, field: string): number {
  const num = asNumber(value, field);
  if (!Number.isInteger(num)) {
    throw new Error(`${field} must be an integer`);
  }
  return num;
}

function validatePriceCents(priceCents: number, field = "price-cents"): void {
  if (!Number.isInteger(priceCents)) {
    throw new Error(`${field} must be an integer`);
  }
  if (priceCents < 0 || priceCents > 100) {
    throw new Error(`${field} must be between 0 and 100`);
  }
}

function parsePriceFieldToCents(
  rawValue: string | number | null | undefined,
  fallbackValue: string | number | null | undefined,
): number | null {
  if (rawValue != null && rawValue !== "") {
    const parsed = Number(rawValue);
    if (!Number.isFinite(parsed)) {
      return null;
    }
    return parsed;
  }

  if (fallbackValue != null && fallbackValue !== "") {
    const parsed = Number(fallbackValue);
    if (!Number.isFinite(parsed)) {
      return null;
    }
    return Math.round(parsed * 100);
  }

  return null;
}

function positionKey(marketTicker: string, contractSide: ContractSide): string {
  return `${marketTicker.toUpperCase()}:${contractSide}`;
}

function getDbPath(args: CliMap): string {
  const raw = (args.db as string | undefined) ?? DEFAULT_DB;
  return resolve(raw.replace(/^~\//, `${homedir()}/`));
}

function getKalshiBaseUrl(args: CliMap): string {
  const raw =
    (args["kalshi-base-url"] as string | undefined) ??
    process.env.KALSHI_BASE_URL ??
    "https://api.elections.kalshi.com/trade-api/v2";
  return raw.replace(/\/+$/, "");
}

function inferSeriesTicker(marketTicker: string, eventTicker: string | null): string | null {
  const source = eventTicker || marketTicker;
  const idx = source.indexOf("-");
  if (idx <= 0) return null;
  return source.slice(0, idx).toUpperCase();
}

async function fetchJson(url: string): Promise<unknown> {
  const res = await fetch(url, {
    method: "GET",
    headers: {
      accept: "application/json",
      "user-agent": "openclaw-skills-kalshi-paper-trading/1.0",
    },
  });
  const text = await res.text();
  let json: unknown;
  try {
    json = JSON.parse(text);
  } catch {
    json = { raw: text };
  }

  if (!res.ok) {
    throw new Error(`HTTP ${res.status} for ${url}: ${typeof json === "object" ? JSON.stringify(json) : String(json)}`);
  }
  return json;
}

async function fetchKalshiMarket(
  marketTicker: string,
  args: CliMap,
): Promise<{ market: KalshiMarketPayload; sourceUrl: string; rawResponse: unknown }> {
  const baseUrl = getKalshiBaseUrl(args);
  const url = `${baseUrl}/markets/${encodeURIComponent(marketTicker)}`;
  const response = await fetchJson(url) as { market?: KalshiMarketPayload };
  if (!response.market) {
    throw new Error(`market payload missing for ${marketTicker}`);
  }
  return {
    market: response.market,
    sourceUrl: url,
    rawResponse: response,
  };
}

function normalizeKalshiStatus(status: KalshiApiMarketStatus): MarketStatus {
  const value = String(status || "").toLowerCase();
  if (value === "finalized" || value === "settled") {
    return "finalized";
  }
  if (value === "closed") {
    return "closed";
  }
  return "open";
}

function inferSettlementSide(market: {
  status?: KalshiApiMarketStatus;
  result?: string;
  yes_bid?: number;
  yes_ask?: number;
  last_price?: number;
  yes_bid_dollars?: string | number | null;
  yes_ask_dollars?: string | number | null;
  last_price_dollars?: string | number | null;
}): ContractSide | null {
  const result = String(market.result || "").trim().toLowerCase();
  if (result === "yes") return "YES";
  if (result === "no") return "NO";

  if (normalizeKalshiStatus(market.status ?? "") !== "finalized") {
    return null;
  }

  const yesBidCents = parsePriceFieldToCents(market.yes_bid, market.yes_bid_dollars);
  const yesAskCents = parsePriceFieldToCents(market.yes_ask, market.yes_ask_dollars);
  const lastPriceCents = parsePriceFieldToCents(market.last_price, market.last_price_dollars);

  if (yesBidCents === 100 || yesAskCents === 100 || lastPriceCents === 100) {
    return "YES";
  }
  if (yesBidCents === 0 || yesAskCents === 0 || lastPriceCents === 0) {
    return "NO";
  }
  return null;
}

function computeMarkFromQuote(params: {
  status: MarketStatus;
  settlementSide: ContractSide | null;
  yesBidCents: number | null;
  yesAskCents: number | null;
  lastYesTradeCents: number | null;
}): { markMethod: MarkMethod; markCents: number | null } {
  if (params.status === "finalized") {
    if (!params.settlementSide) {
      throw new Error("finalized market is missing settlement side");
    }
    return {
      markMethod: "settlement",
      markCents: params.settlementSide === "YES" ? 100 : 0,
    };
  }

  if (params.yesBidCents != null && params.yesAskCents != null) {
    return {
      markMethod: "mid",
      markCents: Math.round((params.yesBidCents + params.yesAskCents) / 2),
    };
  }
  if (params.yesBidCents != null) {
    return {
      markMethod: "bid",
      markCents: params.yesBidCents,
    };
  }
  if (params.lastYesTradeCents != null) {
    return {
      markMethod: "last_trade",
      markCents: params.lastYesTradeCents,
    };
  }
  return {
    markMethod: "unknown",
    markCents: null,
  };
}

function openDb(path: string): DatabaseSync {
  mkdirSync(dirname(path), { recursive: true });
  const db = new DatabaseSync(path);
  db.exec("PRAGMA foreign_keys = ON;");
  db.exec(`
    CREATE TABLE IF NOT EXISTS accounts (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      base_currency TEXT NOT NULL DEFAULT 'USD',
      starting_balance_usd REAL NOT NULL,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS executions (
      id TEXT PRIMARY KEY,
      account_id TEXT NOT NULL,
      market_ticker TEXT NOT NULL,
      event_ticker TEXT,
      series_ticker TEXT,
      contract_side TEXT NOT NULL,
      action TEXT NOT NULL,
      contracts REAL NOT NULL,
      price_cents INTEGER NOT NULL,
      fee_usd REAL NOT NULL DEFAULT 0,
      source TEXT NOT NULL,
      note TEXT,
      meta_json TEXT,
      created_at TEXT NOT NULL,
      FOREIGN KEY(account_id) REFERENCES accounts(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_executions_account_time
      ON executions(account_id, created_at);

    CREATE INDEX IF NOT EXISTS idx_executions_account_market_side
      ON executions(account_id, market_ticker, contract_side, created_at);

    CREATE TABLE IF NOT EXISTS market_marks (
      market_ticker TEXT PRIMARY KEY,
      status TEXT NOT NULL,
      close_time_utc TEXT,
      settlement_side TEXT,
      yes_bid_cents INTEGER,
      yes_ask_cents INTEGER,
      last_yes_trade_cents INTEGER,
      mark_method TEXT NOT NULL,
      mark_cents INTEGER,
      raw_json TEXT,
      updated_at TEXT NOT NULL
    );
  `);
  return db;
}

function requireAccount(db: DatabaseSync, accountId: string): AccountRow {
  const row = db
    .prepare(
      "SELECT id, name, base_currency, starting_balance_usd, created_at FROM accounts WHERE id = ?",
    )
    .get(accountId) as AccountRow | undefined;
  if (!row) {
    throw new Error(`account '${accountId}' not found; run init first`);
  }
  return row;
}

function addExecution(
  db: DatabaseSync,
  params: {
    accountId: string;
    marketTicker: string;
    eventTicker?: string;
    seriesTicker?: string;
    contractSide: ContractSide;
    action: ExecutionAction;
    contracts: number;
    priceCents: number;
    feeUsd?: number;
    source: string;
    note?: string;
    meta?: Record<string, unknown>;
  },
): string {
  const id = randomUUID();
  db.prepare(
    `INSERT INTO executions (
      id, account_id, market_ticker, event_ticker, series_ticker, contract_side,
      action, contracts, price_cents, fee_usd, source, note, meta_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    id,
    params.accountId,
    params.marketTicker.toUpperCase(),
    params.eventTicker ?? null,
    params.seriesTicker ?? null,
    params.contractSide,
    params.action,
    params.contracts,
    params.priceCents,
    params.feeUsd ?? 0,
    params.source,
    params.note ?? null,
    params.meta ? JSON.stringify(params.meta) : null,
    nowIso(),
  );
  return id;
}

function upsertMarketMark(
  db: DatabaseSync,
  params: {
    marketTicker: string;
    status: MarketStatus;
    closeTimeUtc?: string | null;
    settlementSide?: ContractSide | null;
    yesBidCents?: number | null;
    yesAskCents?: number | null;
    lastYesTradeCents?: number | null;
    markMethod: MarkMethod;
    markCents?: number | null;
    rawJson?: string | null;
  },
): void {
  db.prepare(
    `INSERT INTO market_marks (
      market_ticker, status, close_time_utc, settlement_side, yes_bid_cents,
      yes_ask_cents, last_yes_trade_cents, mark_method, mark_cents, raw_json, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(market_ticker) DO UPDATE SET
      status = excluded.status,
      close_time_utc = excluded.close_time_utc,
      settlement_side = excluded.settlement_side,
      yes_bid_cents = excluded.yes_bid_cents,
      yes_ask_cents = excluded.yes_ask_cents,
      last_yes_trade_cents = excluded.last_yes_trade_cents,
      mark_method = excluded.mark_method,
      mark_cents = excluded.mark_cents,
      raw_json = excluded.raw_json,
      updated_at = excluded.updated_at`,
  ).run(
    params.marketTicker.toUpperCase(),
    params.status,
    params.closeTimeUtc ?? null,
    params.settlementSide ?? null,
    params.yesBidCents ?? null,
    params.yesAskCents ?? null,
    params.lastYesTradeCents ?? null,
    params.markMethod,
    params.markCents ?? null,
    params.rawJson ?? null,
    nowIso(),
  );
}

function replay(
  db: DatabaseSync,
  accountId: string,
): { positions: Map<string, OpenPosition>; metrics: PositionMetrics } {
  const rows = db
    .prepare(
      `SELECT market_ticker, event_ticker, series_ticker, contract_side, action, contracts, price_cents, fee_usd, created_at
       FROM executions
       WHERE account_id = ?
       ORDER BY created_at ASC, rowid ASC`,
    )
    .all(accountId) as ExecutionRow[];

  const positions = new Map<string, OpenPosition>();
  const metrics: PositionMetrics = { realizedPnlUsd: 0, closedCount: 0, wins: 0, losses: 0 };

  for (const row of rows) {
    const marketTicker = row.market_ticker.toUpperCase();
    const side = row.contract_side;
    const key = positionKey(marketTicker, side);
    const contracts = Number(row.contracts ?? 0);
    const priceCents = Number(row.price_cents ?? 0);
    const feeUsd = Number(row.fee_usd ?? 0);
    if (contracts <= 0) continue;

    if (row.action === "BUY") {
      const existing = positions.get(key);
      if (!existing) {
        positions.set(key, {
          marketTicker,
          eventTicker: row.event_ticker ?? null,
          seriesTicker: row.series_ticker ?? null,
          contractSide: side,
          contracts,
          avgEntryCents: priceCents,
          openFeesRemainingUsd: feeUsd,
        });
        continue;
      }

      const nextContracts = existing.contracts + contracts;
      existing.avgEntryCents =
        (existing.avgEntryCents * existing.contracts + priceCents * contracts) /
        nextContracts;
      existing.contracts = nextContracts;
      existing.openFeesRemainingUsd += feeUsd;
      existing.eventTicker = existing.eventTicker ?? row.event_ticker ?? null;
      existing.seriesTicker = existing.seriesTicker ?? row.series_ticker ?? null;
      continue;
    }

    if (row.action === "SELL") {
      const existing = positions.get(key);
      if (!existing || existing.contracts <= 0) {
        continue;
      }
      const closeContracts = Math.min(contracts, existing.contracts);
      if (closeContracts <= 0) continue;

      let feeAllocUsd = 0;
      if (existing.openFeesRemainingUsd > 0 && existing.contracts > 0) {
        feeAllocUsd = existing.openFeesRemainingUsd * (closeContracts / existing.contracts);
        existing.openFeesRemainingUsd -= feeAllocUsd;
      }

      const realized =
        (closeContracts * (priceCents - existing.avgEntryCents)) / 100 -
        feeAllocUsd -
        feeUsd;

      metrics.realizedPnlUsd += realized;
      metrics.closedCount += 1;
      if (realized > 0) metrics.wins += 1;
      else if (realized < 0) metrics.losses += 1;

      existing.contracts -= closeContracts;
      if (existing.contracts <= 1e-12) {
        positions.delete(key);
      }
    }
  }

  return { positions, metrics };
}

function getLatestMarks(db: DatabaseSync): Map<string, MarketMark> {
  const rows = db
    .prepare(
      `SELECT market_ticker, status, close_time_utc, settlement_side, yes_bid_cents, yes_ask_cents,
              last_yes_trade_cents, mark_method, mark_cents, updated_at
       FROM market_marks`,
    )
    .all() as Array<{
    market_ticker: string;
    status: MarketStatus;
    close_time_utc: string | null;
    settlement_side: ContractSide | null;
    yes_bid_cents: number | null;
    yes_ask_cents: number | null;
    last_yes_trade_cents: number | null;
    mark_method: MarkMethod;
    mark_cents: number | null;
    updated_at: string;
  }>;

  const marks = new Map<string, MarketMark>();
  for (const row of rows) {
    marks.set(row.market_ticker.toUpperCase(), {
      marketTicker: row.market_ticker.toUpperCase(),
      status: row.status,
      closeTimeUtc: row.close_time_utc,
      settlementSide: row.settlement_side,
      yesBidCents: row.yes_bid_cents,
      yesAskCents: row.yes_ask_cents,
      lastYesTradeCents: row.last_yes_trade_cents,
      markMethod: row.mark_method,
      markCents: row.mark_cents,
      updatedAt: row.updated_at,
    });
  }
  return marks;
}

function derivePositionMarkCents(position: OpenPosition, mark: MarketMark | undefined): number | null {
  if (!mark || mark.markCents == null) {
    return null;
  }
  if (position.contractSide === "YES") {
    return mark.markCents;
  }
  return 100 - mark.markCents;
}

function sumOpenCostBasisUsd(positions: Map<string, OpenPosition>): number {
  let total = 0;
  for (const position of positions.values()) {
    total += (position.contracts * position.avgEntryCents) / 100;
  }
  return total;
}

function computeCashUsd(
  account: AccountRow,
  db: DatabaseSync,
  accountId: string,
): number {
  const rows = db
    .prepare(
      "SELECT action, contracts, price_cents, fee_usd FROM executions WHERE account_id = ? ORDER BY created_at ASC, rowid ASC",
    )
    .all(accountId) as Array<{
    action: ExecutionAction;
    contracts: number;
    price_cents: number;
    fee_usd: number;
  }>;

  let cash = Number(account.starting_balance_usd);
  for (const row of rows) {
    const contracts = Number(row.contracts ?? 0);
    const priceUsd = Number(row.price_cents ?? 0) / 100;
    const feeUsd = Number(row.fee_usd ?? 0);
    if (row.action === "BUY") {
      cash -= contracts * priceUsd + feeUsd;
    } else {
      cash += contracts * priceUsd - feeUsd;
    }
  }
  return cash;
}

function buildStatus(db: DatabaseSync, accountId: string) {
  const account = requireAccount(db, accountId);
  const { positions, metrics } = replay(db, accountId);
  const marks = getLatestMarks(db);
  const cashUsd = computeCashUsd(account, db, accountId);
  const openCostBasisUsd = sumOpenCostBasisUsd(positions);

  let openMarkValueUsd = 0;
  let unrealizedPnlUsd = 0;
  let maxLossRemainingUsd = 0;

  const rows = [...positions.values()]
    .sort((a, b) =>
      `${a.marketTicker}:${a.contractSide}`.localeCompare(`${b.marketTicker}:${b.contractSide}`),
    )
    .map((position) => {
      const mark = marks.get(position.marketTicker);
      const markCents = derivePositionMarkCents(position, mark);
      const markValueUsd = markCents == null ? null : (position.contracts * markCents) / 100;
      const costBasisUsd = (position.contracts * position.avgEntryCents) / 100;
      const unrealizedPnl =
        markValueUsd == null ? null : markValueUsd - costBasisUsd - position.openFeesRemainingUsd;
      const maxLossRemaining = position.contractSide === "YES"
        ? (position.contracts * (100 - position.avgEntryCents)) / 100
        : (position.contracts * position.avgEntryCents) / 100;

      if (markValueUsd != null) openMarkValueUsd += markValueUsd;
      if (unrealizedPnl != null) unrealizedPnlUsd += unrealizedPnl;
      maxLossRemainingUsd += maxLossRemaining;

      return {
        marketTicker: position.marketTicker,
        eventTicker: position.eventTicker,
        seriesTicker: position.seriesTicker,
        contractSide: position.contractSide,
        contracts: position.contracts,
        avgEntryCents: position.avgEntryCents,
        avgEntryDollars: position.avgEntryCents / 100,
        costBasisUsd,
        markCents,
        markDollars: markCents == null ? null : markCents / 100,
        markValueUsd,
        unrealizedPnlUsd: unrealizedPnl,
        openFeesRemainingUsd: position.openFeesRemainingUsd,
        markStatus: mark?.status ?? null,
        markMethod: mark?.markMethod ?? null,
        markUpdatedAt: mark?.updatedAt ?? null,
        staleMark: markCents == null,
      };
    });

  const equityUsd = cashUsd + openMarkValueUsd;

  return {
    account: {
      id: account.id,
      name: account.name,
      baseCurrency: account.base_currency,
      startingBalanceUsd: Number(account.starting_balance_usd),
      createdAt: account.created_at,
    },
    summary: {
      cashUsd,
      realizedPnlUsd: metrics.realizedPnlUsd,
      unrealizedPnlUsd,
      openCostBasisUsd,
      openMarkValueUsd,
      maxLossRemainingUsd,
      equityUsd,
      openPositions: rows.length,
      closedTrades: metrics.closedCount,
      wins: metrics.wins,
      losses: metrics.losses,
      winRate: metrics.closedCount > 0 ? (metrics.wins / metrics.closedCount) * 100 : null,
    },
    positions: rows,
  };
}

function cmdInit(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const name = (args.name as string) ?? "Kalshi Paper";
  const baseCurrency = ((args["base-currency"] as string) ?? "USD").toUpperCase();
  const startingBalanceUsd = asNumber(
    args["starting-balance-usd"] ?? args["starting-balance"],
    "starting-balance-usd",
  );

  const exists = db.prepare("SELECT 1 AS ok FROM accounts WHERE id = ?").get(accountId) as
    | { ok: 1 }
    | undefined;
  if (exists) {
    throw new Error(`account '${accountId}' already exists`);
  }

  db.prepare(
    "INSERT INTO accounts (id, name, base_currency, starting_balance_usd, created_at) VALUES (?, ?, ?, ?, ?)",
  ).run(accountId, name, baseCurrency, startingBalanceUsd, nowIso());

  console.log(`initialized account=${accountId}`);
}

function validateTradeInput(
  marketTicker: string,
  contracts: number,
  priceCents: number,
  feeUsd: number,
): void {
  if (!marketTicker.trim()) {
    throw new Error("market is required");
  }
  if (!Number.isFinite(contracts) || contracts <= 0) {
    throw new Error("contracts must be > 0");
  }
  validatePriceCents(priceCents);
  if (!Number.isFinite(feeUsd) || feeUsd < 0) {
    throw new Error("fee-usd must be >= 0");
  }
}

function cmdBuy(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const marketTicker = asString(args.market, "market").toUpperCase();
  const eventTicker = asOptionalString(args.event)?.toUpperCase();
  const seriesTicker = asOptionalString(args.series)?.toUpperCase();
  const contractSide = parseContractSide(args.side);
  const contracts = asNumber(args.contracts, "contracts");
  const priceCents = asInteger(args["price-cents"], "price-cents");
  const feeUsd = args["fee-usd"] == null ? 0 : asNumber(args["fee-usd"], "fee-usd");
  const note = asOptionalString(args.note);

  requireAccount(db, accountId);
  validateTradeInput(marketTicker, contracts, priceCents, feeUsd);

  const id = addExecution(db, {
    accountId,
    marketTicker,
    eventTicker,
    seriesTicker,
    contractSide,
    action: "BUY",
    contracts,
    priceCents,
    feeUsd,
    source: "manual",
    note,
    meta: { command: "buy" },
  });

  console.log(`bought execution=${id} ${contractSide} ${contracts} ${marketTicker} @ ${priceCents}c`);
}

function cmdSell(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const marketTicker = asString(args.market, "market").toUpperCase();
  const contractSide = parseContractSide(args.side);
  const contracts = asNumber(args.contracts, "contracts");
  const priceCents = asInteger(args["price-cents"], "price-cents");
  const feeUsd = args["fee-usd"] == null ? 0 : asNumber(args["fee-usd"], "fee-usd");
  const note = asOptionalString(args.note);

  requireAccount(db, accountId);
  validateTradeInput(marketTicker, contracts, priceCents, feeUsd);
  const { positions } = replay(db, accountId);
  const existing = positions.get(positionKey(marketTicker, contractSide));
  if (!existing || existing.contracts <= 0) {
    throw new Error(`no open ${contractSide} position for ${marketTicker}`);
  }
  if (contracts > existing.contracts + 1e-12) {
    throw new Error(`cannot sell ${contracts} contracts; only ${existing.contracts} open`);
  }

  const id = addExecution(db, {
    accountId,
    marketTicker,
    eventTicker: existing.eventTicker ?? undefined,
    seriesTicker: existing.seriesTicker ?? undefined,
    contractSide,
    action: "SELL",
    contracts,
    priceCents,
    feeUsd,
    source: "manual",
    note,
    meta: { command: "sell" },
  });

  console.log(`sold execution=${id} ${contractSide} ${contracts} ${marketTicker} @ ${priceCents}c`);
}

function cmdMark(db: DatabaseSync, args: CliMap): void {
  const marketTicker = asString(args.market, "market").toUpperCase();
  const status = parseMarketStatus(args.status ?? "open");
  const yesBidCents =
    args["yes-bid-cents"] == null ? null : asInteger(args["yes-bid-cents"], "yes-bid-cents");
  const yesAskCents =
    args["yes-ask-cents"] == null ? null : asInteger(args["yes-ask-cents"], "yes-ask-cents");
  const lastYesTradeCents =
    args["last-yes-trade-cents"] == null
      ? null
      : asInteger(args["last-yes-trade-cents"], "last-yes-trade-cents");
  const closeTimeUtc = asOptionalString(args["close-time-utc"]) ?? null;
  const settlementSide =
    args["settlement-side"] == null ? null : parseContractSide(args["settlement-side"]);

  if (yesBidCents != null) validatePriceCents(yesBidCents, "yes-bid-cents");
  if (yesAskCents != null) validatePriceCents(yesAskCents, "yes-ask-cents");
  if (lastYesTradeCents != null) validatePriceCents(lastYesTradeCents, "last-yes-trade-cents");

  const { markMethod, markCents } = computeMarkFromQuote({
    status,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
  });

  upsertMarketMark(db, {
    marketTicker,
    status,
    closeTimeUtc,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
    markMethod,
    markCents,
    rawJson: asOptionalString(args["raw-json"]) ?? null,
  });

  console.log(
    `marked ${marketTicker} status=${status} mark=${markCents == null ? "n/a" : `${markCents}c`} method=${markMethod}`,
  );
}

async function cmdSyncMarket(db: DatabaseSync, args: CliMap): Promise<void> {
  const marketTicker = asString(args.market, "market").toUpperCase();
  const pretty = Boolean(args.pretty);
  const format = (args.format as string) ?? "text";
  const { market, sourceUrl, rawResponse } = await fetchKalshiMarket(marketTicker, args);

  const status = normalizeKalshiStatus(market.status ?? "active");
  const yesBidCents = parsePriceFieldToCents(market.yes_bid, market.yes_bid_dollars);
  const yesAskCents = parsePriceFieldToCents(market.yes_ask, market.yes_ask_dollars);
  const lastYesTradeCents = parsePriceFieldToCents(market.last_price, market.last_price_dollars);
  const settlementSide = inferSettlementSide(market);

  if (yesBidCents != null) validatePriceCents(yesBidCents, "yes_bid");
  if (yesAskCents != null) validatePriceCents(yesAskCents, "yes_ask");
  if (lastYesTradeCents != null) validatePriceCents(lastYesTradeCents, "last_price");

  const { markMethod, markCents } = computeMarkFromQuote({
    status,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
  });

  upsertMarketMark(db, {
    marketTicker,
    status,
    closeTimeUtc: market.close_time ?? null,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
    markMethod,
    markCents,
    rawJson: JSON.stringify(rawResponse),
  });

  const payload = {
    marketTicker,
    eventTicker: market.event_ticker ?? null,
    status,
    closeTimeUtc: market.close_time ?? null,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
    markMethod,
    markCents,
    sourceUrl,
  };

  if (format === "json") {
    printJson(payload, pretty);
    return;
  }

  console.log(
    `synced ${marketTicker} status=${status} yes_bid=${yesBidCents ?? "n/a"} yes_ask=${yesAskCents ?? "n/a"} last=${lastYesTradeCents ?? "n/a"} mark=${markCents == null ? "n/a" : `${markCents}c`} method=${markMethod}`,
  );
}

async function cmdBuyFromMarket(db: DatabaseSync, args: CliMap): Promise<void> {
  const accountId = (args.account as string) ?? "kalshi";
  const marketTicker = asString(args.market, "market").toUpperCase();
  const contractSide = parseContractSide(args.side);
  const contracts = asNumber(args.contracts, "contracts");
  const feeUsd = args["fee-usd"] == null ? 0 : asNumber(args["fee-usd"], "fee-usd");
  const note = asOptionalString(args.note);
  const pretty = Boolean(args.pretty);
  const format = (args.format as string) ?? "json";

  requireAccount(db, accountId);

  const { market, sourceUrl, rawResponse } = await fetchKalshiMarket(marketTicker, args);

  const status = normalizeKalshiStatus(market.status ?? "active");
  const yesBidCents = parsePriceFieldToCents(market.yes_bid, market.yes_bid_dollars);
  const yesAskCents = parsePriceFieldToCents(market.yes_ask, market.yes_ask_dollars);
  const noAskCents = parsePriceFieldToCents(market.no_ask, market.no_ask_dollars);
  const lastYesTradeCents = parsePriceFieldToCents(market.last_price, market.last_price_dollars);
  const settlementSide = inferSettlementSide(market);

  if (yesBidCents != null) validatePriceCents(yesBidCents, "yes_bid");
  if (yesAskCents != null) validatePriceCents(yesAskCents, "yes_ask");
  if (noAskCents != null) validatePriceCents(noAskCents, "no_ask");
  if (lastYesTradeCents != null) validatePriceCents(lastYesTradeCents, "last_price");

  const { markMethod, markCents } = computeMarkFromQuote({
    status,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
  });

  upsertMarketMark(db, {
    marketTicker,
    status,
    closeTimeUtc: market.close_time ?? null,
    settlementSide,
    yesBidCents,
    yesAskCents,
    lastYesTradeCents,
    markMethod,
    markCents,
    rawJson: JSON.stringify(rawResponse),
  });

  const priceCents = contractSide === "YES" ? yesAskCents : noAskCents;
  if (priceCents == null) {
    throw new Error(`missing ${contractSide.toLowerCase()} ask for ${marketTicker}`);
  }

  validateTradeInput(marketTicker, contracts, priceCents, feeUsd);

  const eventTicker = market.event_ticker?.toUpperCase() ?? undefined;
  const seriesTicker = inferSeriesTicker(marketTicker, market.event_ticker ?? null) ?? undefined;
  const executionId = addExecution(db, {
    accountId,
    marketTicker,
    eventTicker,
    seriesTicker,
    contractSide,
    action: "BUY",
    contracts,
    priceCents,
    feeUsd,
    source: "sync-market",
    note,
    meta: {
      command: "buy-from-market",
      sourceUrl,
      status,
      yesBidCents,
      yesAskCents,
      noAskCents,
      lastYesTradeCents,
      markCents,
      markMethod,
    },
  });

  const statusPayload = buildStatus(db, accountId);
  const out = {
    trade: {
      executionId,
      accountId,
      marketTicker,
      eventTicker: eventTicker ?? null,
      seriesTicker: seriesTicker ?? null,
      contractSide,
      contracts,
      priceCents,
      priceDollars: priceCents / 100,
      feeUsd,
      sourceUrl,
    },
    mark: {
      status,
      yesBidCents,
      yesAskCents,
      noAskCents,
      lastYesTradeCents,
      markMethod,
      markCents,
      settlementSide,
      closeTimeUtc: market.close_time ?? null,
    },
    status: statusPayload,
  };

  if (format === "json") {
    printJson(out, pretty);
    return;
  }

  console.log(
    `bought-from-market execution=${executionId} ${contractSide} ${contracts} ${marketTicker} @ ${priceCents}c mark=${markCents == null ? "n/a" : `${markCents}c`} method=${markMethod}`,
  );
  cmdStatus(db, { _: ["status"], account: accountId, format, pretty });
}

function cmdReconcile(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const marketTicker = asString(args.market, "market").toUpperCase();
  const status = parseMarketStatus(args.status ?? "finalized");
  const winningSide = parseContractSide(args["winning-side"]);

  requireAccount(db, accountId);
  upsertMarketMark(db, {
    marketTicker,
    status,
    settlementSide: winningSide,
    markMethod: "settlement",
    markCents: winningSide === "YES" ? 100 : 0,
    closeTimeUtc: asOptionalString(args["close-time-utc"]) ?? null,
    rawJson: asOptionalString(args["raw-json"]) ?? null,
  });

  const { positions } = replay(db, accountId);
  const closed: string[] = [];

  for (const side of ["YES", "NO"] as const) {
    const existing = positions.get(positionKey(marketTicker, side));
    if (!existing || existing.contracts <= 0) continue;
    const settlementCents = side === winningSide ? 100 : 0;
    addExecution(db, {
      accountId,
      marketTicker,
      eventTicker: existing.eventTicker ?? undefined,
      seriesTicker: existing.seriesTicker ?? undefined,
      contractSide: side,
      action: "SELL",
      contracts: existing.contracts,
      priceCents: settlementCents,
      feeUsd: 0,
      source: "reconcile",
      note: `settlement ${winningSide}`,
      meta: { command: "reconcile", winningSide },
    });
    closed.push(`${side}:${existing.contracts}@${settlementCents}c`);
  }

  if (closed.length === 0) {
    console.log(`reconciled ${marketTicker}; no open positions to settle`);
    return;
  }

  console.log(`reconciled ${marketTicker}; settled ${closed.join(", ")}`);
}

function cmdStatus(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const format = (args.format as string) ?? "text";
  const pretty = Boolean(args.pretty);
  const payload = buildStatus(db, accountId);

  if (format === "json") {
    console.log(JSON.stringify(payload, null, pretty ? 2 : undefined));
    return;
  }

  const s = payload.summary;
  console.log(`account=${payload.account.id} equity_usd=${s.equityUsd.toFixed(2)} cash_usd=${s.cashUsd.toFixed(2)}`);
  console.log(
    `realized_pnl_usd=${s.realizedPnlUsd.toFixed(2)} unrealized_pnl_usd=${s.unrealizedPnlUsd.toFixed(
      2,
    )} open_positions=${s.openPositions} closed_trades=${s.closedTrades}`,
  );
  if (s.winRate != null) {
    console.log(`win_rate=${s.winRate.toFixed(2)}% (${s.wins}/${s.closedTrades})`);
  }
  if (payload.positions.length > 0) {
    console.log("positions:");
    for (const p of payload.positions) {
      const mark = p.markCents == null ? "n/a" : `${p.markCents}c`;
      const unrealized =
        p.unrealizedPnlUsd == null ? "n/a" : p.unrealizedPnlUsd.toFixed(2);
      console.log(
        `- ${p.marketTicker} ${p.contractSide} contracts=${p.contracts.toFixed(2)} avg=${p.avgEntryCents.toFixed(
          2,
        )}c mark=${mark} unrealized_usd=${unrealized}${p.staleMark ? " stale_mark=true" : ""}`,
      );
    }
  }
}

function cmdReview(db: DatabaseSync, args: CliMap): void {
  const accountId = (args.account as string) ?? "kalshi";
  const format = (args.format as string) ?? "text";
  const pretty = Boolean(args.pretty);
  const payload = buildStatus(db, accountId);
  const expectancy =
    payload.summary.closedTrades > 0
      ? payload.summary.realizedPnlUsd / payload.summary.closedTrades
      : 0;

  const out = {
    summary: payload.summary,
    expectancyPerClosedTradeUsd: expectancy,
  };

  if (format === "json") {
    console.log(JSON.stringify(out, null, pretty ? 2 : undefined));
    return;
  }

  console.log(`closed_trades=${payload.summary.closedTrades} realized_usd=${payload.summary.realizedPnlUsd.toFixed(2)}`);
  console.log(`expectancy_per_closed_trade_usd=${expectancy.toFixed(2)}`);
}

function printHelp(): void {
  console.log(`kalshi_paper.ts - Kalshi-native SQLite paper trading CLI

Usage:
  node --experimental-strip-types kalshi_paper.ts [--db <path>] <command> [options]

Commands:
  init --starting-balance-usd <n> [--account kalshi] [--name <name>] [--base-currency USD]
  buy --account kalshi --market <ticker> [--event <ticker>] [--series <ticker>] --side YES|NO --contracts <n> --price-cents <0-100> [--fee-usd 0] [--note <text>]
  buy-from-market --account kalshi --market <ticker> --side YES|NO --contracts <n> [--fee-usd 0] [--note <text>] [--kalshi-base-url <url>] [--format text|json] [--pretty]
  sell --account kalshi --market <ticker> --side YES|NO --contracts <n> --price-cents <0-100> [--fee-usd 0] [--note <text>]
  mark --market <ticker> [--status open|closed|finalized] [--yes-bid-cents <n>] [--yes-ask-cents <n>] [--last-yes-trade-cents <n>] [--settlement-side YES|NO] [--close-time-utc <iso>]
  sync-market --market <ticker> [--kalshi-base-url <url>] [--format text|json] [--pretty]
  reconcile --account kalshi --market <ticker> --winning-side YES|NO [--status finalized] [--close-time-utc <iso>]
  status [--account kalshi] [--format text|json] [--pretty]
  review [--account kalshi] [--format text|json] [--pretty]
`);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command || command === "help" || command === "--help") {
    printHelp();
    return;
  }

  const db = openDb(getDbPath(args));
  try {
    switch (command) {
      case "init":
        cmdInit(db, args);
        break;
      case "buy":
        cmdBuy(db, args);
        break;
      case "buy-from-market":
        await cmdBuyFromMarket(db, args);
        break;
      case "sell":
        cmdSell(db, args);
        break;
      case "mark":
        cmdMark(db, args);
        break;
      case "sync-market":
        await cmdSyncMarket(db, args);
        break;
      case "reconcile":
        cmdReconcile(db, args);
        break;
      case "status":
        cmdStatus(db, args);
        break;
      case "review":
        cmdReview(db, args);
        break;
      default:
        throw new Error(`unknown command '${command}'`);
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  } finally {
    db.close();
  }
}

void main();
