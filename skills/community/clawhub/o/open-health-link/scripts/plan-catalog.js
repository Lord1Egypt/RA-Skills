#!/usr/bin/env node

/**
 * Resolves scalp care plan details from CSV knowledge base.
 *
 * Default source is remote CSV:
 *   https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv
 *
 * Usage:
 *   node plan-catalog.js "<schemeName>" [--view summary|full] [--url <csv_url>] [--csv <path>]
 *   node plan-catalog.js --list [--url <csv_url>] [--csv <path>]
 */

import { jsonOutput, errorExit } from "./utils.js";
import { loadCatalogTextFromFile } from "./catalog-file-source.js";

const DEFAULT_CSV_URL =
  "https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv";
const REMOTE_FETCH_TIMEOUT_MS = 15000;
const MAX_CSV_BYTES = 2 * 1024 * 1024;
const ALLOWED_CSV_HOST = "breo-obs.obs.cn-south-1.myhuaweicloud.com";
const ALLOWED_CSV_PATH = "/agents/plan-catalog.csv";

const CIRCLED_NUM_MAP = {
  "①": "1",
  "②": "2",
  "③": "3",
  "④": "4",
  "⑤": "5",
  "⑥": "6",
  "⑦": "7",
  "⑧": "8",
  "⑨": "9",
  "⑩": "10",
};

function parseArgs(argv) {
  const args = argv.slice(2);
  let schemeName = null;
  let view = "summary";
  let csvPath = null;
  let csvUrl = DEFAULT_CSV_URL;
  let listOnly = false;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (!arg) {
      continue;
    }
    if (arg === "--list") {
      listOnly = true;
      continue;
    }
    if (arg === "--view" && i + 1 < args.length) {
      view = args[i + 1];
      i += 1;
      continue;
    }
    if (arg.startsWith("--view=")) {
      view = arg.slice("--view=".length);
      continue;
    }
    if (arg === "--csv" && i + 1 < args.length) {
      csvPath = args[i + 1];
      i += 1;
      continue;
    }
    if (arg.startsWith("--csv=")) {
      csvPath = arg.slice("--csv=".length);
      continue;
    }
    if (arg === "--url" && i + 1 < args.length) {
      csvUrl = args[i + 1];
      i += 1;
      continue;
    }
    if (arg.startsWith("--url=")) {
      csvUrl = arg.slice("--url=".length);
      continue;
    }
    if (!schemeName) {
      schemeName = arg;
    }
  }

  const normalizedView = String(view || "summary").toLowerCase();
  if (normalizedView !== "summary" && normalizedView !== "full") {
    errorExit("参数 --view 仅支持 summary 或 full。");
  }

  if (!listOnly && !schemeName) {
    errorExit(
      'Usage: node plan-catalog.js "<schemeName>" [--view summary|full] [--url <csv_url>] [--csv <path>]'
    );
  }

  return {
    schemeName,
    view: normalizedView,
    csvPath: csvPath ? csvPath.trim() : null,
    csvUrl: String(csvUrl || "").trim(),
    listOnly,
  };
}

function parseCsv(rawText) {
  const text = String(rawText || "").replace(/^\uFEFF/, "");
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];

    if (ch === '"') {
      if (inQuotes && text[i + 1] === '"') {
        cell += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (ch === "," && !inQuotes) {
      row.push(cell);
      cell = "";
      continue;
    }

    if ((ch === "\n" || ch === "\r") && !inQuotes) {
      if (ch === "\r" && text[i + 1] === "\n") {
        i += 1;
      }
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
      continue;
    }

    cell += ch;
  }

  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }

  return rows;
}

function dedupeHeaders(headers) {
  const countMap = new Map();
  return headers.map((header) => {
    const key = String(header || "").trim() || "unnamed";
    const current = countMap.get(key) || 0;
    countMap.set(key, current + 1);
    if (current === 0) {
      return key;
    }
    return `${key}#${current + 1}`;
  });
}

function normalizeCatalogRows(rows) {
  const headerRowIndex = rows.findIndex((row) =>
    row.some((cell) => String(cell || "").trim() === "对应方案")
  );
  if (headerRowIndex < 0) {
    throw new Error("CSV 未找到表头（缺少“对应方案”列）。");
  }

  const headers = dedupeHeaders(rows[headerRowIndex]);
  const result = [];

  for (let i = headerRowIndex + 1; i < rows.length; i += 1) {
    const row = rows[i];
    if (!row || row.every((cell) => !String(cell || "").trim())) {
      continue;
    }
    const item = {};
    for (let c = 0; c < headers.length; c += 1) {
      item[headers[c]] = String(row[c] ?? "").trim();
    }

    const schemeName = item["对应方案"];
    if (!schemeName) {
      continue;
    }
    result.push(item);
  }

  return result;
}

function normalizeSchemeName(value) {
  const raw = String(value || "").trim();
  if (!raw) {
    return "";
  }
  let normalized = "";
  for (const ch of raw) {
    normalized += CIRCLED_NUM_MAP[ch] || ch;
  }
  return normalized
    .toLowerCase()
    .replace(/[\s\u3000]/g, "")
    .replace(/[()（）\[\]【】《》<>]/g, "")
    .replace(/[,.，。:：;；'’"“”`·\-—_]/g, "");
}

function findBestMatch(items, querySchemeName) {
  const queryRaw = String(querySchemeName || "").trim();
  const queryNormalized = normalizeSchemeName(queryRaw);
  if (!queryRaw) {
    return null;
  }

  for (const item of items) {
    if (String(item["对应方案"] || "").trim() === queryRaw) {
      return { item, matchType: "exact" };
    }
  }

  for (const item of items) {
    if (normalizeSchemeName(item["对应方案"]) === queryNormalized) {
      return { item, matchType: "normalized" };
    }
  }

  // Guard against empty normalized queries: avoid matching everything.
  if (!queryNormalized) {
    return null;
  }

  for (const item of items) {
    const candidate = normalizeSchemeName(item["对应方案"]);
    if (candidate && (candidate.includes(queryNormalized) || queryNormalized.includes(candidate))) {
      return { item, matchType: "fuzzy_contains" };
    }
  }

  return null;
}

function buildSteps(item) {
  const stepDefs = [
    { titleKey: "第一步", detailKey: "步骤说明" },
    { titleKey: "第二步", detailKey: "步骤说明#2" },
    { titleKey: "第三步", detailKey: "步骤说明#3" },
    { titleKey: "第四步", detailKey: "步骤说明#4" },
  ];

  return stepDefs
    .map((def) => ({
      title: item[def.titleKey] || "",
      detail: item[def.detailKey] || "",
    }))
    .filter((step) => !!(step.title || step.detail));
}

function buildSummary(item) {
  const steps = buildSteps(item).slice(0, 3);
  return {
    schemeName: item["对应方案"] || null,
    topIssue: item["对应top问题"] || null,
    topIssueDescription: item["top问题说明"] || null,
    modeIntro: item["模式简介"] || null,
    massageDuration: item["按摩时长"] || null,
    planOverview: item["方案概述"] || null,
    steps,
  };
}

function buildFull(item) {
  return {
    schemeName: item["对应方案"] || null,
    topIssue: item["对应top问题"] || null,
    topIssueDescription: item["top问题说明"] || null,
    modeIntro: item["模式简介"] || null,
    lightDescription: item["光能介绍"] || null,
    lightSubtitle: item["光能副标题"] || null,
    introDescription: item["介绍说明"] || null,
    massageDuration: item["按摩时长"] || null,
    massageMode: item["头皮按摩"] || null,
    massageDescription: item["按摩说明"] || null,
    pairingSuggestion: item["搭配建议"] || null,
    pairingDescription: item["搭配说明"] || null,
    planOverview: item["方案概述"] || null,
    steps: buildSteps(item),
    background: item["方案背景"] || null,
    tips: item["tips"] || null,
    qaQuestion: item["专研模式详细解答-问题"] || null,
    qaAnswer: item["专研模式详细解答-答案"] || null,
    moreAdvice: item["更多养护建议"] || null,
    warmTips: item["温馨提示"] || null,
    references: item["参考文献"] || null,
  };
}

async function fetchRemoteCsv(csvUrl) {
  if (!csvUrl) {
    throw new Error("方案知识库 URL 为空。");
  }
  let parsed;
  try {
    parsed = new URL(csvUrl);
  } catch {
    throw new Error("方案知识库 URL 格式不正确。");
  }
  if (parsed.protocol !== "https:") {
    throw new Error("方案知识库仅支持 HTTPS 地址。");
  }
  if (parsed.hostname !== ALLOWED_CSV_HOST || parsed.pathname !== ALLOWED_CSV_PATH) {
    throw new Error("方案知识库来源不受信任。");
  }

  const resp = await fetch(csvUrl, {
    method: "GET",
    signal: AbortSignal.timeout(REMOTE_FETCH_TIMEOUT_MS),
  });
  if (!resp.ok) {
    throw new Error(`远程方案知识库请求失败 (HTTP ${resp.status})`);
  }
  const contentLength = Number.parseInt(resp.headers.get("content-length") || "", 10);
  if (Number.isFinite(contentLength) && contentLength > MAX_CSV_BYTES) {
    throw new Error("远程方案知识库体积超限，请联系管理员检查数据源。");
  }
  const text = await resp.text();
  if (Buffer.byteLength(text, "utf-8") > MAX_CSV_BYTES) {
    throw new Error("远程方案知识库体积超限，请联系管理员检查数据源。");
  }
  return text;
}

async function loadCatalog({ csvPath, csvUrl }) {
  const raw = csvPath
    ? await loadCatalogTextFromFile(csvPath)
    : await fetchRemoteCsv(csvUrl);
  const rows = parseCsv(raw);
  return normalizeCatalogRows(rows);
}

async function main() {
  try {
    const args = parseArgs(process.argv);
    const items = await loadCatalog({ csvPath: args.csvPath, csvUrl: args.csvUrl });

    if (args.listOnly) {
      jsonOutput({
        total: items.length,
        schemes: items.map((item) => item["对应方案"]).filter(Boolean),
      });
      return;
    }

    const match = findBestMatch(items, args.schemeName);
    if (!match) {
      jsonOutput({
        found: false,
        querySchemeName: args.schemeName,
        candidates: items
          .map((item) => item["对应方案"])
          .filter(Boolean)
          .slice(0, 20),
      });
      return;
    }

    const summary = buildSummary(match.item);
    const full = buildFull(match.item);
    const payload = {
      found: true,
      querySchemeName: args.schemeName,
      matchedSchemeName: match.item["对应方案"] || null,
      matchType: match.matchType,
      view: args.view,
      summary,
      ...(args.view === "full" ? { full } : {}),
    };

    jsonOutput(payload);
  } catch (err) {
    if (err.code === "ENOENT") {
      errorExit("方案知识库文件不存在，请检查 CSV 路径。");
    }
    if (err.name === "TimeoutError" || err.name === "AbortError") {
      errorExit("远程方案知识库请求超时，请稍后重试。");
    }
    errorExit(err.message || "读取护理方案知识库失败。");
  }
}

main();
