/**
 * gamma-client.js — Gamma API Client + Polymarket Market Domain Classification
 *
 * HTTP implementation reuses the shared manual TLS/CONNECT tunnel approach,
 * does not depend on https-proxy-agent, proxy config is read from proxy-config.js.
 */

"use strict";

const tls = require("tls");
const net = require("net");
const cache = require("./cache");
const { PROXY } = require("./proxy-config");

const GAMMA_HOST = "gamma-api.polymarket.com";
const DEFAULT_BATCH = 25;
const SCAN_LIMIT = 500;
const SCAN_DELAY_MS = 150;
const MAX_RETRIES = 3; // scanByVolume max retries per page, skip after exceeding

// ── Basic GET (manual TLS + proxy CONNECT) ──
function get(urlPath, timeoutMs = 30_000) {
  return new Promise((resolve, reject) => {
    const reqLine =
      `GET ${urlPath} HTTP/1.1\r\n` +
      `Host: ${GAMMA_HOST}\r\n` +
      `User-Agent: polymarket-data-layer-skill/1.0\r\n` +
      `Accept: application/json\r\n` +
      `Connection: close\r\n\r\n`;

    function handleSocket(sock) {
      const chunks = [];
      sock.setTimeout(timeoutMs);
      sock.on("timeout", () => sock.destroy(new Error("Gamma API timeout")));
      sock.on("error", reject);
      sock.on("data", (c) => chunks.push(c));
      sock.on("end", () => {
        const raw = Buffer.concat(chunks);
        const split = raw.indexOf("\r\n\r\n");
        if (split === -1) return reject(new Error("Invalid HTTP response"));

        const headerStr = raw.slice(0, split).toString("utf-8");
        const status = parseInt(headerStr.split("\r\n")[0].split(" ")[1]);
        const chunked = headerStr
          .toLowerCase()
          .includes("transfer-encoding: chunked");

        // Chunked decoding at Buffer level to avoid offset errors from byte/character count mismatch
        let body = raw.slice(split + 4);
        if (chunked) {
          const parts = [];
          let pos = 0;
          while (pos < body.length) {
            const nl = body.indexOf("\r\n", pos);
            if (nl === -1) break;
            const sz = parseInt(body.slice(pos, nl).toString("ascii"), 16);
            if (isNaN(sz) || sz === 0) break;
            parts.push(body.slice(nl + 2, nl + 2 + sz));
            pos = nl + 2 + sz + 2;
          }
          body = Buffer.concat(parts);
        }

        const bodyStr = body.toString("utf-8");
        if (status !== 200)
          return reject(
            new Error(`Gamma API HTTP ${status}: ${bodyStr.slice(0, 120)}`),
          );
        try {
          resolve(JSON.parse(bodyStr));
        } catch (_) {
          reject(
            new Error(`Gamma API JSON parse error: ${bodyStr.slice(0, 80)}`),
          );
        }
      });
      sock.write(reqLine);
    }

    let fellBackToDirect = false;

    function connectDirect() {
      if (fellBackToDirect) return;
      fellBackToDirect = true;
      const tlsSock = tls.connect(
        {
          host: GAMMA_HOST,
          port: 443,
          servername: GAMMA_HOST,
          rejectUnauthorized: false,
        },
        () => handleSocket(tlsSock),
      );
      tlsSock.setTimeout(timeoutMs);
      tlsSock.on("timeout", () => tlsSock.destroy(new Error("TLS timeout")));
      tlsSock.on("error", reject);
    }

    if (PROXY) {
      const proxy = new URL(PROXY);
      const tcp = net.connect(
        Number(proxy.port) || 8080,
        proxy.hostname,
        () => {
          tcp.write(
            `CONNECT ${GAMMA_HOST}:443 HTTP/1.0\r\nHost: ${GAMMA_HOST}:443\r\n\r\n`,
          );
          let hdr = "";
          tcp.once("data", (chunk) => {
            hdr += chunk.toString();
            if (!hdr.includes("200")) {
              tcp.destroy();
              return connectDirect();
            }
            const tlsSock = tls.connect(
              {
                socket: tcp,
                servername: GAMMA_HOST,
                rejectUnauthorized: false,
              },
              () => handleSocket(tlsSock),
            );
            tlsSock.on("error", reject);
          });
        },
      );
      tcp.setTimeout(timeoutMs);
      tcp.on("timeout", () => tcp.destroy(new Error("TCP timeout")));
      tcp.on("error", () => connectDirect());
    } else {
      connectDirect();
    }
  });
}

// ── Batch query by condition_id ───────────────────────────────────
async function fetchByConditionIds(
  conditionIds,
  { batchSize = DEFAULT_BATCH, timeout = 30_000 } = {},
) {
  const ids = [...new Set(conditionIds)];
  const result = [];

  for (let i = 0; i < ids.length; i += batchSize) {
    const batch = ids.slice(i, i + batchSize);
    const qs = batch
      .map((id) => `condition_ids=${encodeURIComponent(id)}`)
      .join("&");
    try {
      const res = await get(`/markets?${qs}&limit=${batchSize}`, timeout);
      const list = Array.isArray(res) ? res : res.data || res.markets || [];
      result.push(...list);
    } catch (e) {
      process.stderr.write(
        `[gamma-client] fetchByConditionIds batch ${i}-${i + batchSize} failed: ${e.message}\n`,
      );
    }
    if (i + batchSize < ids.length) {
      await new Promise((r) => setTimeout(r, 250));
    }
  }
  return result;
}

// ── Scan all markets by volume ────────────────────────────────────────
// Max retries per page is MAX_RETRIES, skip this page and continue if exceeded.
async function scanByVolume({
  maxMarkets = 40_000,
  targetIds = null,
  onProgress = null,
} = {}) {
  const result = [];
  let offset = 0;

  while (offset < maxMarkets) {
    let page;
    let retries = 0;
    while (retries < MAX_RETRIES) {
      try {
        page = await get(
          `/markets?limit=${SCAN_LIMIT}&offset=${offset}&order=volumeNum&ascending=false`,
          25_000,
        );
        break;
      } catch (_) {
        retries++;
        if (retries < MAX_RETRIES)
          await new Promise((r) => setTimeout(r, 1500));
      }
    }

    // Skip this page if retries exhausted
    if (!page) {
      offset += SCAN_LIMIT;
      continue;
    }
    if (!Array.isArray(page) || page.length === 0) break;

    result.push(...page);
    offset += SCAN_LIMIT;

    if (onProgress) {
      const covered = targetIds
        ? result.filter((m) => targetIds.has(m.conditionId || m.condition_id))
            .length
        : result.length;
      onProgress(offset, covered, targetIds?.size ?? 0);
    }

    if (targetIds && targetIds.size > 0) {
      const covered = result.filter((m) =>
        targetIds.has(m.conditionId || m.condition_id),
      ).length;
      if (covered >= targetIds.size * 0.85) break;
    }

    await new Promise((r) => setTimeout(r, SCAN_DELAY_MS));
  }

  return result;
}

// ── Search active markets by keywords ────────────────────────────────────────
// Returns list of active markets matching keywords, sorted by volume descending.
// When multiple keywords are passed as array, search sequentially and deduplicate merge.
async function searchByKeyword(
  keywords,
  { limit = 30, timeout = 20_000 } = {},
) {
  const terms = Array.isArray(keywords) ? keywords : [keywords];
  const seen = new Set();
  const result = [];

  for (const kw of terms) {
    const qs = `search=${encodeURIComponent(kw)}&active=true&closed=false&limit=${limit}&order=volumeNum&ascending=false`;
    try {
      const res = await get(`/markets?${qs}`, timeout);
      const list = Array.isArray(res) ? res : res.data || res.markets || [];
      for (const m of list) {
        const cid = m.conditionId || m.condition_id;
        if (cid && !seen.has(cid)) {
          seen.add(cid);
          result.push(m);
        }
      }
    } catch (e) {
      process.stderr.write(
        `[gamma-client] searchByKeyword("${kw}") failed: ${e.message}\n`,
      );
    }
    if (terms.length > 1) await new Promise((r) => setTimeout(r, 300));
  }

  return result;
}

// ── Utilities ──────────────────────────────────────────────────────
function normalize(market) {
  return {
    conditionId: market.conditionId || market.condition_id || null,
    question: market.question || market.title || "",
    category: market.category || "",
    tags: market.tags || [],
    volume: Number(market.volumeNum || market.volume || 0),
    active: market.active ?? true,
    closed: market.closed ?? false,
  };
}

// ── Domain Classification Rules ──────────────────────────────────────────────

const TAG_ID_DOMAIN = {
  2: "POL",
  100265: "GEO",
  120: "FIN",
  21: "CRY",
  100639: "SPT",
  1401: "TEC",
  596: "CUL",
};

const TAG_SLUG_DOMAIN = {
  politics: "POL",
  "us-elections": "POL",
  elections: "POL",
  election: "POL",
  midterms: "POL",
  "gov-policy": "POL",
  trump: "POL",
  tariffs: "POL",
  legislature: "POL",
  geopolitics: "GEO",
  ukraine: "GEO",
  china: "GEO",
  israel: "GEO",
  "middle-east": "GEO",
  venezuela: "GEO",
  "global-elections": "GEO",
  mexico: "GEO",
  finance: "FIN",
  stocks: "FIN",
  equities: "FIN",
  fed: "FIN",
  economy: "FIN",
  commodities: "FIN",
  oil: "FIN",
  ipo: "FIN",
  earnings: "FIN",
  derivatives: "FIN",
  "interest-rate": "FIN",
  crypto: "CRY",
  bitcoin: "CRY",
  ethereum: "CRY",
  defi: "CRY",
  btc: "CRY",
  eth: "CRY",
  etf: "CRY",
  nft: "CRY",
  sports: "SPT",
  nfl: "SPT",
  nba: "SPT",
  ufc: "SPT",
  soccer: "SPT",
  "formula-1": "SPT",
  f1: "SPT",
  golf: "SPT",
  tennis: "SPT",
  boxing: "SPT",
  baseball: "SPT",
  chess: "SPT",
  esports: "SPT",
  olympics: "SPT",
  "premier-league": "SPT",
  tech: "TEC",
  ai: "TEC",
  spacex: "TEC",
  technology: "TEC",
  twitter: "TEC",
  culture: "CUL",
  movies: "CUL",
  oscars: "CUL",
  music: "CUL",
  tv: "CUL",
  celebrity: "CUL",
  awards: "CUL",
  entertainment: "CUL",
};

const CAT_MAP = {
  "us-current-affairs": "POL",
  politics: "POL",
  "global politics": "GEO",
  "global-politics": "GEO",
  "ukraine & russia": "GEO",
  business: "FIN",
  economics: "FIN",
  finance: "FIN",
  crypto: "CRY",
  nfts: "CRY",
  defi: "CRY",
  sports: "SPT",
  "nba playoffs": "SPT",
  nba: "SPT",
  nfl: "SPT",
  olympics: "SPT",
  chess: "SPT",
  poker: "SPT",
  tech: "TEC",
  science: "TEC",
  space: "TEC",
  "pop-culture": "CUL",
  art: "CUL",
};

const Q_RULES = [
  [
    /\b(trump|biden|harris|clinton|obama|election|president|congress|senate|democrat|republican|white house|tariff|gov.shutdown|vp |cabinet|inaugur|ballot|midterm|primary|nato|un |imf )\b/i,
    "POL",
  ],
  [
    /\b(ukraine|russia|china|israel|iran|hamas|hezbollah|nato|war|ceasefire|sanction|xi |putin|zelensky|middle.?east|taiwan|venezuela|geopolit|kim jong|north korea|south korea|india|pakistan|saudi|cartel|border|migrant|refugee)\b/i,
    "GEO",
  ],
  [
    /\b(fed |federal reserve|interest.?rate|rate.?cut|s&p|stock|nasdaq|dow |ipo |earnings|gdp|inflation|recession|oil.?price|crude|gold.?price|commodit|treasury|bond.?yield|cpi |ppi |jobs.?report|unemployment|fomc)\b/i,
    "FIN",
  ],
  [
    /\b(bitcoin|btc |eth |ethereum|crypto|solana|sol |doge|xrp|bnb |chainlink|polygon|avalanche|defi |nft |blockchain|coinbase|binance|sec.+crypto|stablecoin|altcoin|halving|layer.?2|web3)\b/i,
    "CRY",
  ],
  [
    /\b(nfl|nba|ufc|soccer|premier.?league|world.?cup|super.?bowl|wimbledon|us.?open|masters|pga|formula.?1|f1 |formula 1|moto.?gp|nascar|basketball|football|baseball|hockey|tennis|boxing|mma|chess|poker|esport|olympic|world.?series|champions.?league|euro.?cup|copa|afc|nfc|playoffs?|championship)\b/i,
    "SPT",
  ],
  [
    /\b(ai |artificial.?intelligence|openai|chatgpt|gpt.?\d|gemini|claude |anthropic|spacex|nasa|starship|rocket|elon.?musk.+tweet|twitter|x\.com|apple|google|microsoft|meta |tesla|nvidia|semiconductor|quantum|cyber|hack|data.?breach)\b/i,
    "TEC",
  ],
  [
    /\b(oscar|grammy|golden.?globe|academy.?award|bafta|emmy|vma|movie|film|box.?office|album|billboard|chart|taylor.?swift|beyonce|kanye|celebrity|kim.?kardashian|reality.?tv|tiktok.+ban|super.?bowl.+halftime)\b/i,
    "CUL",
  ],
];

function marketDomain(market) {
  const question = market.question || market.title || "";
  const category = market.category || "";

  const q = question.toLowerCase();
  for (const [re, d] of Q_RULES) {
    if (re.test(q)) return d;
  }
  if (category) {
    const c = category.trim().toLowerCase();
    if (CAT_MAP[c]) return CAT_MAP[c];
  }
  return null;
}

// ── buildDomainMap (incremental cache) ────────────────────────────────
async function buildDomainMap(
  conditionIds = [],
  { maxMarkets = 40_000, onProgress, fresh = false } = {},
) {
  const CACHE_KEY = "gamma:domain-map";
  const accumulated = (!fresh && cache.get(CACHE_KEY, { ttl: Infinity })) || {};

  const missing = conditionIds.filter((id) => !(id in accumulated));

  if (conditionIds.length > 0 && missing.length === 0) {
    return Object.fromEntries(
      conditionIds.map((id) => [id, accumulated[id]]).filter(([, v]) => v),
    );
  }

  const newResults = {};
  const missingSet = new Set(missing);

  const scanTargets = missingSet.size > 0 ? missingSet : null;
  const markets = await scanByVolume({
    maxMarkets,
    targetIds: scanTargets,
    onProgress,
  });
  for (const m of markets) {
    const cid = m.conditionId || m.condition_id;
    const domain = marketDomain(m);
    if (cid && domain) newResults[cid] = domain;
  }

  const merged = { ...accumulated, ...newResults };
  cache.set(CACHE_KEY, merged);

  if (conditionIds.length === 0) return merged;
  return Object.fromEntries(
    conditionIds.map((id) => [id, merged[id]]).filter(([, v]) => v),
  );
}

const DOMAIN_LABELS = {
  POL: "Politics",
  GEO: "Geopolitics",
  FIN: "Finance",
  CRY: "Crypto",
  SPT: "Sports",
  TEC: "Tech/AI",
  CUL: "Entertainment",
  GEN: "Generalist",
};

module.exports = {
  get,
  fetchByConditionIds,
  scanByVolume,
  searchByKeyword,
  normalize,
  marketDomain,
  buildDomainMap,
  TAG_ID_DOMAIN,
  DOMAIN_LABELS,
};
