#!/usr/bin/env node

/**
 * Fetches scalp report list for an authorized user.
 *
 * Usage:
 *   node fetch-report-list.js [authToken] [--day <1-90>]
 *
 * Output:
 *   JSON to stdout:
 *   {
 *     day,
 *     total,
 *     reports,
 *     rawData
 *   }
 */

import { getDataApiBaseUrl, jsonOutput, errorExit } from "./utils.js";
import { loadStoredAuthToken } from "./auth-token.js";

const MAX_DAY = 90;
const REPORT_TIME_KEYS = [
  "detectTime",
  "createTime",
  "createdAt",
  "reportTime",
  "createtime",
];

function parseArgs(argv) {
  const args = argv.slice(2);
  let authToken = null;
  let day = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (!arg) {
      continue;
    }
    if (!arg.startsWith("--") && !authToken) {
      authToken = arg;
      continue;
    }
    if (arg === "--day" && i + 1 < args.length) {
      day = args[i + 1];
      i += 1;
      continue;
    }
    if (arg.startsWith("--day=")) {
      day = arg.slice("--day=".length);
    }
  }

  const dayRaw = String(day ?? "").trim();
  const dayValue =
    dayRaw === ""
      ? null
      : /^\d+$/.test(dayRaw)
        ? Number.parseInt(dayRaw, 10)
        : Number.NaN;

  if (dayValue !== null) {
    if (!Number.isInteger(dayValue) || dayValue <= 0 || dayValue > MAX_DAY) {
      errorExit(`参数 day 非法，需为 1-${MAX_DAY} 的整数`);
    }
  }

  return {
    authToken: authToken ? String(authToken) : null,
    day: dayValue,
  };
}

function normalizeReportList(data) {
  if (Array.isArray(data)) {
    return data;
  }
  if (!data || typeof data !== "object") {
    return [];
  }

  const candidates = [
    data.list,
    data.items,
    data.records,
    data.rows,
    data.dataList,
    data.reportList,
  ];

  for (const candidate of candidates) {
    if (Array.isArray(candidate)) {
      return candidate;
    }
  }

  return [];
}

function pickFirstString(obj, keys) {
  if (!obj || typeof obj !== "object") {
    return null;
  }
  for (const key of keys) {
    const value = obj[key];
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }
  return null;
}

function pickFirstValue(obj, keys) {
  if (!obj || typeof obj !== "object") {
    return null;
  }
  for (const key of keys) {
    if (obj[key] !== undefined && obj[key] !== null && obj[key] !== "") {
      return obj[key];
    }
  }
  return null;
}

function withSchemeName(item) {
  const schemeName = pickFirstString(item, [
    "schemeName",
    "scheme_name",
    "planName",
    "plan_name",
    "scheme",
    "plan",
  ]);
  return {
    ...item,
    schemeName: schemeName ?? null,
  };
}

function toReportSchemeEntry(item) {
  const reportId = pickFirstValue(item, [
    "reportId",
    "reportid",
    "id",
    "reportCode",
    "code",
  ]);
  const detectTime = pickFirstString(item, [
    ...REPORT_TIME_KEYS,
  ]);
  return {
    reportId: reportId ?? null,
    detectTime: detectTime ?? null,
    schemeName: item.schemeName ?? null,
  };
}

function getLatestReportWithScheme(reports) {
  const candidates = reports.filter((item) => !!item.schemeName);
  if (candidates.length === 0) {
    return null;
  }

  const sorted = [...candidates].sort((a, b) => {
    const ta = Date.parse(pickFirstString(a, REPORT_TIME_KEYS) || "");
    const tb = Date.parse(pickFirstString(b, REPORT_TIME_KEYS) || "");
    if (Number.isNaN(ta) && Number.isNaN(tb)) {
      return 0;
    }
    if (Number.isNaN(ta)) {
      return 1;
    }
    if (Number.isNaN(tb)) {
      return -1;
    }
    return tb - ta;
  });

  return sorted[0] || null;
}

function buildResult(json, day) {
  const rawData = json?.data ?? null;
  const reports = normalizeReportList(rawData).map(withSchemeName);
  const reportSchemeMap = reports
    .map(toReportSchemeEntry)
    .filter((item) => !!item.schemeName);
  const latestWithScheme = getLatestReportWithScheme(reports);

  return {
    day,
    total: reports.length,
    latestSchemeName: latestWithScheme?.schemeName || null,
    reportSchemeMap,
    reports,
    rawData,
  };
}

async function fetchReportList({ authToken, day }) {
  const baseUrl = getDataApiBaseUrl();
  const path = `/auth/dt/${encodeURIComponent(authToken)}/list`;
  const url = new URL(`${baseUrl}${path}`);
  if (day !== null) {
    url.searchParams.set("day", String(day));
  }

  const resp = await fetch(url, {
    method: "GET",
    signal: AbortSignal.timeout(12000),
  });

  if (!resp.ok) {
    if (resp.status === 401 || resp.status === 403) {
      errorExit("鉴权失败，授权已失效，请重新绑定。");
    }
    const body = await resp.text().catch(() => "");
    errorExit(`获取检测报告列表失败 (HTTP ${resp.status}): ${body || "未知错误"}`);
  }

  let json;
  try {
    json = await resp.json();
  } catch {
    errorExit("检测报告接口返回了非 JSON 数据。");
  }

  jsonOutput(buildResult(json, day));
}

async function main() {
  try {
    const input = parseArgs(process.argv);
    const authToken = input.authToken || (await loadStoredAuthToken());
    if (!authToken) {
      errorExit("未检测到有效授权，请先完成账号绑定。");
    }
    await fetchReportList({ authToken, day: input.day });
  } catch (err) {
    const causeCode = err?.cause?.code;
    if (
      causeCode === "ECONNREFUSED" ||
      causeCode === "ENOTFOUND" ||
      causeCode === "EHOSTUNREACH" ||
      causeCode === "ETIMEDOUT" ||
      causeCode === "ECONNRESET"
    ) {
      errorExit("无法连接到报告服务，请检查网络或确认环境地址可达。");
    }
    if (err.name === "TimeoutError" || err.name === "AbortError") {
      errorExit("报告服务请求超时，请稍后重试。");
    }
    if (err.message === "fetch failed") {
      errorExit("报告服务请求失败，请检查网络后重试。");
    }
    errorExit(err.message || "获取检测报告列表失败。");
  }
}

main();
