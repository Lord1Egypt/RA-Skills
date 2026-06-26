import { URL } from "url";
import https from "https";

const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36";
const REFERER = "https://quote.eastmoney.com";
const TIMEOUT_KLINE_MS = 15000;
const TIMEOUT_DEFAULT_MS = 10000;

function num(v) {
  if (v === null || v === undefined || v === "" || v === "-") return null;
  const n = typeof v === "number" ? v : parseFloat(String(v).replace(/,/g, ""));
  return Number.isFinite(n) ? n : null;
}

function div100(v) {
  const n = num(v);
  return n === null ? null : n / 100;
}

function request(urlString, timeoutMs) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlString);
    const opts = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: "GET",
      headers: {
        "User-Agent": UA,
        Referer: REFERER,
      },
    };
    const req = https.request(opts, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (ch) => {
        body += ch;
      });
      res.on("end", () => resolve(body));
    });
    req.on("error", reject);
    req.setTimeout(timeoutMs, () => {
      req.destroy();
      reject(new Error("timeout"));
    });
    req.end();
  });
}

function parseJsonLoose(text) {
  const t = String(text).trim();
  try {
    return JSON.parse(t);
  } catch {
    const i = t.indexOf("{");
    const j = t.lastIndexOf("}");
    if (i >= 0 && j > i) {
      try {
        return JSON.parse(t.slice(i, j + 1));
      } catch {
        return null;
      }
    }
    return null;
  }
}

function ymd(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
}

export function resolveSecid(code) {
  const c = String(code).trim();
  if (c.startsWith("6")) return `1.${c}`;
  if (c.startsWith("0") || c.startsWith("3") || c.startsWith("8") || c.startsWith("4")) return `0.${c}`;
  return `0.${c}`;
}

export function resolveTencentPrefix(code) {
  const c = String(code).trim();
  if (c.startsWith("6")) return "sh";
  return "sz";
}

async function eastQuote(code) {
  const secid = resolveSecid(code);
  const fields = "f43,f44,f45,f46,f47,f48,f50,f57,f58,f60,f116,f117,f162,f167,f170";
  const url = `https://push2.eastmoney.com/api/qt/stock/get?secid=${encodeURIComponent(secid)}&fields=${fields}`;
  const text = await request(url, TIMEOUT_DEFAULT_MS);
  const j = parseJsonLoose(text);
  const d = j && j.data;
  if (!d || d.f43 === undefined || d.f43 === null) return null;
  const latest_price = div100(d.f43);
  const high = div100(d.f44);
  const low = div100(d.f45);
  const open = div100(d.f46);
  const volume = num(d.f47);
  const amount = num(d.f48);
  const volume_ratio = div100(d.f50);
  const name = d.f58 != null ? String(d.f58) : "";
  const c = d.f57 != null ? String(d.f57) : String(code).trim();
  const pe = div100(d.f162);
  const pb = div100(d.f167);
  const change_pct = div100(d.f170);
  const market_cap = num(d.f116);
  const circulating_cap = num(d.f117);
  if (latest_price === null) return null;
  return {
    latest_price,
    open,
    high,
    low,
    volume,
    amount,
    volume_ratio,
    change_pct,
    pe,
    pb,
    market_cap,
    circulating_cap,
    name,
    code: c,
    source: "eastmoney",
  };
}

function parseTencentQuoteCompound(part35) {
  if (!part35 || typeof part35 !== "string" || !part35.includes("/")) return { amount: null };
  const segs = part35.split("/");
  const amount = num(segs[2]);
  return { amount };
}

async function tencentQuote(code) {
  const p = resolveTencentPrefix(code);
  const c = String(code).trim();
  const url = `https://qt.gtimg.cn/q=${p}${c}`;
  const text = await request(url, TIMEOUT_DEFAULT_MS);
  const m = text.match(/="([^"]*)"/);
  if (!m) return null;
  const parts = m[1].split("~");
  const name = parts[1] != null ? String(parts[1]) : "";
  const latest_price = num(parts[3]);
  const prev = num(parts[4]);
  const open = num(parts[5]);
  const volume = num(parts[6]);
  const high = num(parts[33]);
  const low = num(parts[34]);
  let change_pct = num(parts[32]);
  if (change_pct === null && latest_price !== null && prev !== null && prev !== 0) {
    change_pct = ((latest_price - prev) / prev) * 100;
  }
  const { amount } = parseTencentQuoteCompound(parts[35]);
  if (latest_price === null) return null;
  return {
    latest_price,
    open,
    high: high !== null ? high : latest_price,
    low: low !== null ? low : latest_price,
    volume,
    amount,
    volume_ratio: null,
    change_pct,
    pe: null,
    pb: null,
    market_cap: null,
    circulating_cap: null,
    name,
    code: c,
    source: "tencent",
  };
}

export async function fetchQuote(code) {
  try {
    const em = await eastQuote(code);
    if (em) return em;
  } catch {
  }
  try {
    const t = await tencentQuote(code);
    if (t) return t;
  } catch {
  }
  return null;
}

function parseEastKlineBar(line) {
  const p = String(line).split(",");
  if (p.length < 6) return null;
  return {
    d: p[0],
    o: num(p[1]),
    c: num(p[2]),
    h: num(p[3]),
    l: num(p[4]),
    v: num(p[5]),
    amount: p[6] !== undefined ? num(p[6]) : null,
    amplitude: p[7] !== undefined ? num(p[7]) : null,
    change_pct: p[8] !== undefined ? num(p[8]) : null,
    change: p[9] !== undefined ? num(p[9]) : null,
    turnover: p[10] !== undefined ? num(p[10]) : null,
  };
}

async function eastKline(code, klt, beg, end) {
  const secid = resolveSecid(code);
  const fields1 = "f1,f2,f3,f4,f5,f6";
  const fields2 = "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61";
  const url =
    `https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=${encodeURIComponent(secid)}` +
    `&fields1=${fields1}&fields2=${fields2}&klt=${encodeURIComponent(String(klt))}&fqt=1` +
    `&beg=${encodeURIComponent(beg)}&end=${encodeURIComponent(end)}`;
  const text = await request(url, TIMEOUT_KLINE_MS);
  const j = parseJsonLoose(text);
  const lines = j && j.data && Array.isArray(j.data.klines) ? j.data.klines : null;
  if (!lines || lines.length === 0) return null;
  const bars = [];
  for (const line of lines) {
    const b = parseEastKlineBar(line);
    if (b) bars.push(b);
  }
  if (bars.length === 0) return null;
  return { bars, source: "eastmoney" };
}

function parseTencentKlineRow(row) {
  if (!Array.isArray(row) || row.length < 6) return null;
  const d = String(row[0]).replace(/-/g, "");
  const o = num(row[1]);
  const c = num(row[2]);
  const h = num(row[3]);
  const l = num(row[4]);
  const v = num(row[5]);
  if (!d) return null;
  return {
    d,
    o,
    c,
    h,
    l,
    v,
    amount: null,
    amplitude: null,
    change_pct: null,
    change: null,
    turnover: null,
  };
}

async function tencentKline(code, days) {
  const p = resolveTencentPrefix(code);
  const c = String(code).trim();
  const n = Math.max(1, Math.min(2000, Math.floor(Number(days) || 520)));
  const param = `${p}${c},day,,,${n},qfq`;
  const url = `https://ifzq.gtimg.cn/appstock/app/fqkline/get?param=${encodeURIComponent(param)}`;
  const text = await request(url, TIMEOUT_KLINE_MS);
  const j = parseJsonLoose(text);
  if (!j || !j.data) return null;
  const block = j.data[`${p}${c}`];
  if (!block) return null;
  const rows = block.qfqday || block.day;
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const bars = [];
  for (const row of rows) {
    const b = parseTencentKlineRow(row);
    if (b) bars.push(b);
  }
  if (bars.length === 0) return null;
  return { bars, source: "tencent" };
}

export async function fetchKline(code, { klt = 101, days = 520, beg, end } = {}) {
  const endD = end ? String(end) : ymd(new Date());
  let begD = beg ? String(beg) : null;
  if (!begD) {
    const ed = /^\d{8}$/.test(endD)
      ? new Date(
          parseInt(endD.slice(0, 4), 10),
          parseInt(endD.slice(4, 6), 10) - 1,
          parseInt(endD.slice(6, 8), 10),
        )
      : new Date();
    const bd = new Date(ed);
    bd.setDate(bd.getDate() - Math.max(1, Math.floor(Number(days) || 520)));
    begD = ymd(bd);
  }
  try {
    const em = await eastKline(code, klt, begD, endD);
    if (em) return em;
  } catch {
  }
  if (Number(klt) !== 101) return null;
  try {
    const t = await tencentKline(code, days);
    if (t) return t;
  } catch {
  }
  return null;
}

function parseMoneyFlowLine(line) {
  const p = String(line).split(",");
  if (p.length < 6) return null;
  return {
    d: p[0],
    main_net: num(p[1]),
    small_net: num(p[2]),
    mid_net: num(p[3]),
    large_net: num(p[4]),
    super_net: num(p[5]),
  };
}

export async function fetchMoneyFlow(code, { days = 20 } = {}) {
  try {
    const secid = resolveSecid(code);
    const lmt = Math.max(1, Math.min(200, Math.floor(Number(days) || 20)));
    const fields1 = "f1,f2,f3,f7";
    const fields2 = "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65";
    const url =
      `https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid=${encodeURIComponent(secid)}` +
      `&fields1=${fields1}&fields2=${fields2}&klt=101&lmt=${encodeURIComponent(String(lmt))}`;
    const text = await request(url, TIMEOUT_DEFAULT_MS);
    const j = parseJsonLoose(text);
    const lines = j && j.data && Array.isArray(j.data.klines) ? j.data.klines : null;
    if (!lines || lines.length === 0) return null;
    const flows = [];
    for (const line of lines) {
      const f = parseMoneyFlowLine(line);
      if (f) flows.push(f);
    }
    if (flows.length === 0) return null;
    return { flows, source: "eastmoney" };
  } catch {
    return null;
  }
}

export async function fetchSectorConstituents(sectorCode, { limit = 50 } = {}) {
  try {
    const fs = `b:${String(sectorCode).trim()}`;
    const pz = Math.max(1, Math.min(500, Math.floor(Number(limit) || 50)));
    const fields = "f2,f3,f4,f12,f14,f15,f16,f17";
    const url =
      `https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=${encodeURIComponent(String(pz))}` +
      `&po=1&np=1&fltt=2&invt=2&fid=f3&fs=${encodeURIComponent(fs)}&fields=${fields}`;
    const text = await request(url, TIMEOUT_DEFAULT_MS);
    const j = parseJsonLoose(text);
    const data = j && j.data;
    const diff = data && Array.isArray(data.diff) ? data.diff : null;
    if (!diff) return null;
    const stocks = [];
    for (const row of diff) {
      stocks.push({
        code: row.f12 != null ? String(row.f12) : "",
        name: row.f14 != null ? String(row.f14) : "",
        price: num(row.f2),
        change_pct: num(row.f3),
        high: num(row.f15),
        low: num(row.f16),
        open: num(row.f17),
      });
    }
    const total = num(data.total);
    return {
      stocks,
      total: total !== null ? total : stocks.length,
      source: "eastmoney",
    };
  } catch {
    return null;
  }
}

export async function fetchConceptSectors({ limit = 30 } = {}) {
  try {
    const pz = Math.max(1, Math.min(200, Math.floor(Number(limit) || 30)));
    const fields = "f2,f3,f4,f8,f12,f14,f20,f104,f105";
    const url =
      `https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=${encodeURIComponent(String(pz))}` +
      `&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=${fields}`;
    const text = await request(url, TIMEOUT_DEFAULT_MS);
    const j = parseJsonLoose(text);
    const data = j && j.data;
    const diff = data && Array.isArray(data.diff) ? data.diff : null;
    if (!diff) return null;
    const sectors = [];
    for (const row of diff) {
      sectors.push({
        code: row.f12 != null ? String(row.f12) : "",
        name: row.f14 != null ? String(row.f14) : "",
        change_pct: num(row.f3),
        up_count: row.f104 != null && row.f104 !== "" ? Math.floor(Number(row.f104)) : null,
        down_count: row.f105 != null && row.f105 !== "" ? Math.floor(Number(row.f105)) : null,
      });
    }
    return { sectors, source: "eastmoney" };
  } catch {
    return null;
  }
}
