import { createHmac } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { homedir } from "node:os";

// ── Constants ───────────────────────────────────────────────────────

export const BASE_URL = "https://api.binance.com";
export const PROFILE_PATH = `${homedir()}/passive-income-claw/user-profile.md`;
export const SNAPSHOT_PATH = `${homedir()}/passive-income-claw/snapshot.md`;
export const LOG_PATH = `${homedir()}/passive-income-claw/execution-log.md`;

// ── Types ───────────────────────────────────────────────────────────

interface BinanceError {
  code: number;
  msg?: string;
}

export interface ProfileData {
  [key: string]: string;
}

export interface SnapshotProduct {
  name: string;
  type: string;
  apy: number;
  risk: string;
  liquidity: string;
  asset: string;
  productId: string;
  projectId: string;
  minPurchaseAmount: string;
}

export interface SnapshotData {
  updated_at: string;
  products: SnapshotProduct[];
}

export interface DiffResult {
  changes: Array<{
    name: string;
    type: "new" | "changed";
    apy?: number;
    old_apy?: number;
    new_apy?: number;
    delta?: number;
    marker: string;
  }>;
  removed: Array<{ name: string; apy: number }>;
  has_changes: boolean;
}

// ── HTTP + Signing ──────────────────────────────────────────────────

async function getServerTime(): Promise<number> {
  let resp: Response;
  try {
    resp = await fetch(`${BASE_URL}/api/v3/time`);
  } catch (e: any) {
    die(`Network error fetching server time: ${e.message}`);
  }
  if (!resp!.ok) die(`Failed to fetch server time: HTTP ${resp!.status}`);
  const data = await resp!.json();
  return data.serverTime;
}

function sign(queryString: string, secret: string): string {
  return createHmac("sha256", secret).update(queryString).digest("hex");
}

export async function signedRequest(
  method: "GET" | "POST",
  endpoint: string,
  params: Record<string, string | number | boolean | undefined> = {}
): Promise<any> {
  const apiKey = process.env.BINANCE_API_KEY;
  const apiSecret = process.env.BINANCE_API_SECRET;
  if (!apiKey || !apiSecret) die("BINANCE_API_KEY and BINANCE_API_SECRET must be set");

  const ts = await getServerTime();
  const allParams = { ...params, timestamp: ts };

  const qs = Object.entries(allParams)
    .filter(([, v]) => v !== undefined && v !== "")
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
    .join("&");

  const signature = sign(qs, apiSecret!);
  const fullQs = `${qs}&signature=${signature}`;

  const url = method === "GET" ? `${BASE_URL}${endpoint}?${fullQs}` : `${BASE_URL}${endpoint}`;
  const opts: RequestInit = {
    method,
    headers: { "X-MBX-APIKEY": apiKey! },
  };

  if (method !== "GET") {
    (opts.headers as Record<string, string>)["Content-Type"] = "application/x-www-form-urlencoded";
    opts.body = fullQs;
  }

  const resp = await fetch(url, opts);
  const body = await resp.json().catch(() => ({ error: true, http_code: resp.status }));

  if ((body as BinanceError).code) {
    const b = body as BinanceError;
    die(`Binance API error ${b.code}: ${b.msg || "Unknown"}`, b.code);
  }
  if (!resp.ok) {
    die(`HTTP ${resp.status}: ${JSON.stringify(body).slice(0, 200)}`);
  }

  return body;
}

// ── Profile I/O ─────────────────────────────────────────────────────

export function ensureDir(path: string): void {
  mkdirSync(dirname(path), { recursive: true });
}

export function readProfile(): string {
  if (!existsSync(PROFILE_PATH)) die(`Profile not found at ${PROFILE_PATH}. Run setup first.`);
  return readFileSync(PROFILE_PATH, "utf-8");
}

function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function getField(content: string, key: string): string | null {
  const match = content.match(new RegExp(`^${escapeRegex(key)}:\\s*(.+?)\\s*(?:#.*)?$`, "m"));
  return match ? match[1].trim() : null;
}

export function setField(content: string, key: string, value: string): string {
  const ek = escapeRegex(key);
  const regex = new RegExp(`^(${ek}:)\\s*.+?(\\s*#.*)?$`, "m");
  if (!regex.test(content)) throw new Error(`Field '${key}' not found in profile`);
  return content.replace(regex, (_, prefix, comment) =>
    comment ? `${prefix} ${value}  ${comment}` : `${prefix} ${value}`
  );
}

export function writeProfile(content: string): void {
  ensureDir(PROFILE_PATH);
  writeFileSync(PROFILE_PATH, content);
}

export function profileDump(content: string): ProfileData {
  const result: ProfileData = {};
  for (const line of content.split("\n")) {
    if (line.startsWith("#") || !line.trim()) continue;
    const match = line.match(/^([^:]+):\s*(.+?)(\s*#.*)?$/);
    if (match) result[match[1].trim()] = match[2].trim();
  }
  return result;
}

export function parseNumeric(str: string): number {
  const m = str.match(/[\d.]+/);
  return m ? parseFloat(m[0]) : 0;
}

export function parseList(str: string): string[] {
  return str
    .replace(/[\[\]]/g, "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

// ── Time helpers (all UTC) ──────────────────────────────────────────

export function utcDate(): string {
  return new Date().toISOString().slice(0, 10);
}

export function utcTime(): string {
  return new Date().toISOString().slice(11, 16);
}

export function utcTimestamp(): string {
  return new Date().toISOString().replace(/\.\d+Z$/, "Z");
}

// ── Pure business logic (testable, no I/O, no process.exit) ─────────

export interface AuthResult {
  pass: boolean;
  check?: number;
  reason?: string;
  amount?: number;
  asset?: string;
  op?: string;
  remaining_daily?: number;
}

export function checkAuth(
  content: string,
  params: { amount: number; asset: string; op: string }
): AuthResult {
  const { amount, asset, op } = params;

  const enabled = getField(content, "execution_enabled");
  if (enabled !== "true") {
    return { pass: false, check: 1, reason: "Execution is disabled." };
  }

  const singleLimit = parseNumeric(getField(content, "single_amount_limit") || "0");
  if (amount > singleLimit) {
    return { pass: false, check: 2, reason: `Amount ${amount} USDT exceeds single limit ${singleLimit} USDT.` };
  }

  const todayUsed = parseNumeric(getField(content, "today_executed_amount") || "0");
  const dailyLimit = parseNumeric(getField(content, "daily_amount_limit") || "0");
  const total = todayUsed + amount;
  if (total > dailyLimit) {
    return { pass: false, check: 3, reason: `Cumulative ${total} USDT would exceed daily limit ${dailyLimit} USDT (${todayUsed} used).` };
  }

  const allowedOps = parseList(getField(content, "allowed_operations") || "");
  if (!allowedOps.includes(op.toLowerCase())) {
    return { pass: false, check: 4, reason: `Operation '${op}' not in allowed list: [${allowedOps.join(", ")}].` };
  }

  const whitelist = parseList(getField(content, "asset_whitelist") || "");
  if (!whitelist.includes(asset.toLowerCase())) {
    return { pass: false, check: 5, reason: `Asset '${asset}' not in whitelist: [${whitelist.join(", ")}].` };
  }

  return { pass: true, amount, asset, op, remaining_daily: dailyLimit - total };
}

export interface ResetResult {
  reset: boolean;
  reason?: string;
  last?: string;
  today: string;
}

export function resetDaily(content: string, today: string): { content: string; result: ResetResult } {
  const lastTime = getField(content, "last_scan_time") || "-";

  if (lastTime === "-") {
    return {
      content: setFieldSafe(content, "today_executed_amount", "0 USDT"),
      result: { reset: true, reason: "first_run", today },
    };
  }

  const lastDate = lastTime.slice(0, 10);
  if (lastDate !== today) {
    return {
      content: setFieldSafe(content, "today_executed_amount", "0 USDT"),
      result: { reset: true, reason: "new_day", last: lastDate, today },
    };
  }

  return { content, result: { reset: false, today } };
}

// setField that returns original content if field not found (for resetDaily safety)
function setFieldSafe(content: string, key: string, value: string): string {
  const ek = escapeRegex(key);
  const regex = new RegExp(`^(${ek}:)\\s*.+?(\\s*#.*)?$`, "m");
  if (!regex.test(content)) return content;
  return content.replace(regex, (_, prefix, comment) =>
    comment ? `${prefix} ${value}  ${comment}` : `${prefix} ${value}`
  );
}

export function diffSnapshots(
  oldProducts: SnapshotProduct[],
  newProducts: SnapshotProduct[],
  threshold: number = 0.5
): DiffResult {
  const oldMap = new Map(oldProducts.map((p) => [p.name, p]));
  const newMap = new Map(newProducts.map((p) => [p.name, p]));

  const result: DiffResult = { changes: [], removed: [], has_changes: false };

  for (const np of newProducts) {
    const op = oldMap.get(np.name);
    if (!op) {
      result.changes.push({ name: np.name, type: "new", apy: np.apy, marker: "✅ New" });
    } else if (Math.abs(np.apy - op.apy) > threshold) {
      const delta = Math.round((np.apy - op.apy) * 100) / 100;
      result.changes.push({
        name: np.name,
        type: "changed",
        old_apy: op.apy,
        new_apy: np.apy,
        delta,
        marker: delta > 0 ? "↑" : "↓",
      });
    }
  }

  for (const op of oldProducts) {
    if (!newMap.has(op.name)) {
      result.removed.push({ name: op.name, apy: op.apy });
    }
  }

  result.has_changes = result.changes.length > 0 || result.removed.length > 0;
  return result;
}

// ── Snapshot parsing (pure) ─────────────────────────────────────────

export function parseSnapshotContent(content: string): SnapshotProduct[] {
  const products: SnapshotProduct[] = [];
  let current: Partial<SnapshotProduct> | null = null;

  for (const line of content.split("\n")) {
    if (line.startsWith("## ")) {
      if (current?.name) products.push(current as SnapshotProduct);
      current = { name: line.slice(3).trim(), type: "", apy: 0, risk: "", liquidity: "", asset: "", productId: "", projectId: "", minPurchaseAmount: "" };
    } else if (current) {
      const m = line.match(/^(\w+):\s*(.+)/);
      if (m) {
        const [, key, val] = m;
        if (key === "apy") current.apy = parseFloat(val);
        else if (key in current) (current as any)[key] = val.trim();
      }
    }
  }
  if (current?.name) products.push(current as SnapshotProduct);
  return products;
}

// ── CLI helpers ─────────────────────────────────────────────────────

export function parseArgs(argv: string[]): Record<string, string | true> {
  const args: Record<string, string | true> = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        args[key] = argv[++i];
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

export function die(msg: string, code?: number): never {
  process.stderr.write(JSON.stringify({ error: msg, ...(code !== undefined && { code }) }) + "\n");
  process.exit(1);
}

export function out(data: unknown): void {
  process.stdout.write(JSON.stringify(data, null, 2) + "\n");
}

export function main(fn: () => Promise<void> | void): void {
  Promise.resolve(fn()).catch((err: any) => {
    die(err.message || String(err));
  });
}
