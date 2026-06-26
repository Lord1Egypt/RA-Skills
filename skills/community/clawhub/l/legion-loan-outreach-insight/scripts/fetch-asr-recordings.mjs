#!/usr/bin/env node
/**
 * 拉取 ASR 已完成录音。须先通过意图解析；若需反问则 ok=false 且不请求 hardware。
 */
import { resolveUserIntent } from "./resolve-user-intent.mjs";
import { isThemeRelatedToTranscripts } from "./parse-analysis-focus.mjs";

const DEFAULT_BASE_URL = "http://192.168.109.50:8900";
const MAX_RECORDS_HINT = Number.parseInt(process.env.LEGION_MAX_RECORDS_HINT ?? "80", 10);

function isHttpBaseUrl(value) {
  return /^https?:\/\//i.test(String(value ?? "").trim());
}

function normalizeBaseUrl(value) {
  if (!isHttpBaseUrl(value)) {
    return DEFAULT_BASE_URL;
  }
  return String(value).trim().replace(/\/+$/, "");
}

function extractBearerToken(raw) {
  if (!raw || typeof raw !== "string") {
    return null;
  }
  const v = raw.trim();
  if (/^Bearer\s+/i.test(v)) {
    return v.slice(7).trim();
  }
  return v;
}

function resolveToken() {
  const fromEnv =
    process.env.LEGION_AUTH_TOKEN ||
    process.env.AUTHORIZATION ||
    process.env.HTTP_AUTHORIZATION;
  if (fromEnv) {
    return extractBearerToken(fromEnv);
  }
  return null;
}

async function readRequestBody() {
  if (process.stdin.isTTY) {
    return null;
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const text = Buffer.concat(chunks).toString("utf8").trim();
  if (!text) {
    return null;
  }
  return JSON.parse(text);
}

function resolveBaseUrl(argvBase) {
  if (isHttpBaseUrl(argvBase)) {
    return normalizeBaseUrl(argvBase);
  }
  const fromEnv = process.env.LEGION_HARDWARE_BASE_URL?.trim();
  if (isHttpBaseUrl(fromEnv)) {
    return normalizeBaseUrl(fromEnv);
  }
  return DEFAULT_BASE_URL;
}

function resolveInput(argv, body) {
  const [, rawArgvBase, argUserId, argOrgId, argToken] = argv;
  const baseUrl = resolveBaseUrl(rawArgvBase);
  if (argUserId && argOrgId) {
    return {
      baseUrl,
      body: {
        userId: String(argUserId).trim(),
        orgId: String(argOrgId).trim(),
        userMessage: process.env.LEGION_USER_MESSAGE?.trim() || "",
        skipClarification: process.env.LEGION_SKIP_CLARIFICATION === "1",
      },
      token: extractBearerToken(argToken) || resolveToken(),
    };
  }
  return {
    baseUrl,
    body: body && typeof body === "object" ? body : {},
    token: resolveToken(),
  };
}

function normalizeRecords(apiBody) {
  const data = apiBody?.data;
  if (Array.isArray(data)) {
    return data;
  }
  if (data && Array.isArray(data.records)) {
    return data.records;
  }
  return [];
}

async function fetchRecordings(root, { userId, orgId, startTime, endTime, token }) {
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/json",
  };

  const getUrl = new URL(`${root}/api/recordings/asr-completed`);
  getUrl.searchParams.set("userId", userId);
  getUrl.searchParams.set("orgId", orgId);
  getUrl.searchParams.set("startTime", startTime);
  getUrl.searchParams.set("endTime", endTime);

  let res = await fetch(getUrl, { method: "GET", headers });
  if (res.status !== 405) {
    return { res, method: "GET" };
  }

  res = await fetch(`${root}/api/recordings/asr-completed`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ userId, orgId, startTime, endTime }),
  });
  return { res, method: "POST" };
}

const stdinBody = await readRequestBody();
const { baseUrl, body, token } = resolveInput(process.argv, stdinBody);
const userId = body.userId != null ? String(body.userId).trim() : null;
const orgId = body.orgId != null ? String(body.orgId).trim() : null;

if (!userId || !orgId) {
  console.error(
    JSON.stringify({
      ok: false,
      error: "userId 与 orgId 必须从请求体 JSON 提供（字段 userId、orgId）",
    }),
  );
  process.exit(1);
}
if (!token) {
  console.error(
    JSON.stringify({
      ok: false,
      error: "token 必须从 Authorization（Bearer）或 LEGION_AUTH_TOKEN 提供，勿使用 body.token",
    }),
  );
  process.exit(1);
}

const intent = resolveUserIntent(body);

if (intent.needClarification) {
  console.log(
    JSON.stringify({
      ok: false,
      needClarification: true,
      userMessage: intent.userMessage,
      timeRange: intent.timeRange,
      analysisFocus: intent.analysisFocus,
      outputFormat: intent.outputFormat,
      clarification: intent.clarification,
      reportPlan: intent.reportPlan,
    }),
  );
  process.exit(0);
}

const { timeRange, analysisFocus, outputFormat, reportPlan } = intent;
const root = normalizeBaseUrl(baseUrl);

const { res, method } = await fetchRecordings(root, {
  userId,
  orgId,
  startTime: timeRange.startTime,
  endTime: timeRange.endTime,
  token,
});

const bodyText = await res.text();
let apiBody;
try {
  apiBody = JSON.parse(bodyText);
} catch {
  console.error(JSON.stringify({ ok: false, httpStatus: res.status, raw: bodyText }));
  process.exit(2);
}

const records = normalizeRecords(apiBody);
const combinedAsrText = records.map((r) => r?.asrText ?? "").join("\n");
const themeRelated = analysisFocus.explicit
  ? isThemeRelatedToTranscripts(combinedAsrText, analysisFocus)
  : true;

const payload = {
  ok: res.ok && apiBody?.code === 0,
  httpStatus: res.status,
  apiCode: apiBody?.code,
  apiMsg: apiBody?.msg,
  baseUrl: root,
  httpMethod: method,
  userMessage: intent.userMessage,
  outputFormat,
  query: {
    userId,
    orgId,
    startTime: timeRange.startTime,
    endTime: timeRange.endTime,
    timeZone: timeRange.timeZone,
    timeSource: timeRange.source,
    timeConfidence: timeRange.confidence,
    timeLabel: timeRange.label,
    timeNotice: reportPlan.timeNotice,
  },
  analysisFocus,
  themeRelated,
  reportPlan: {
    ...reportPlan,
    themeUnrelated: analysisFocus.explicit && !themeRelated,
    themeUnrelatedMessage:
      analysisFocus.explicit && !themeRelated
        ? `在所查时间窗内，转写内容未涉及「${analysisFocus.theme ?? analysisFocus.rawPhrase}」，仅输出：无相关内容。`
        : null,
  },
  recordCount: records.length,
  recordsTruncated: records.length > MAX_RECORDS_HINT,
  recordsHint:
    records.length > MAX_RECORDS_HINT
      ? `记录数 ${records.length} 超过建议上限 ${MAX_RECORDS_HINT}，分析时请优先近期样本并抽样摘录。`
      : null,
  records,
};

console.log(JSON.stringify(payload));
