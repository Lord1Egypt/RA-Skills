#!/usr/bin/env node
// bin/opphub-knowledge-search.js · v4.0
// status: implemented (向量召回, v3.1)
//
//
// 用法: bot 调
//   opphub knowledge-search --q "公司主营业务" --json
//   opphub knowledge-search --q "Ollama 本地嵌入" --limit 5 --json
//   opphub knowledge-search --q "联系人" --min-score 0.6 --json
// 返 { ok, query, count, results: [{chunkId, entryId, score, text, sourceType, sourceUrl, createdAt}] }
// skill 拿到后出飞书 card 列出 top chunks, 引导用户引用 / 追问

import { join } from "node:path";
import { homedir } from "node:os";

import { getAccessToken as pluginGetAccessToken } from "../lib/opphub-plugin-client.js";

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";

async function getAccessToken() {
  try {
    const accessToken = await pluginGetAccessToken();
    return accessToken ? { access_token: accessToken } : null;
  } catch {
    return null;
  }
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--q" || a === "--query") args.q = argv[++i];
    else if (a === "--limit") args.limit = argv[++i];
    else if (a === "--min-score") args.minScore = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  if (!args.q || args.q.trim().length === 0) {
    const result = { ok: false, error: "missing_query", message: "需要 --q \"你的问题\"" };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  const limit = args.limit ? Math.min(Math.max(parseInt(args.limit, 10) || 10, 1), 50) : 10;
  const minScore = args.minScore ? parseFloat(args.minScore) : undefined;

  const token = await getAccessToken();
  if (!token?.access_token) {
    const result = {
      ok: false,
      error: "need_login",
      message: "需要先偶合登录 (调 opphub-login 或 device flow)",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  // 调 server /api/user/knowledge/search
  const url = new URL(`${API_BASE}/api/user/knowledge/search`);
  url.searchParams.set("q", args.q);
  url.searchParams.set("limit", String(limit));
  if (minScore !== undefined && !isNaN(minScore)) {
    url.searchParams.set("min_score", String(Math.max(0, Math.min(minScore, 1))));
  }

  let resp;
  try {
    resp = await fetch(url, {
      headers: { Authorization: `Bearer ${token.access_token}` },
      signal: AbortSignal.timeout(30_000),
    });
  } catch (e) {
    const result = {
      ok: false,
      error: "network_failed",
      message: e?.message ?? String(e),
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(2);
  }

  if (resp.status === 404 || resp.status === 501) {
    const result = {
      ok: false,
      error: "server_not_deployed",
      message: `server 返 ${resp.status}: /api/user/knowledge/search endpoint 未部署`,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }
  if (resp.status === 401) {
    const result = {
      ok: false,
      error: "unauthorized",
      message: "token 无效, 需重新偶合登录",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }
  if (!resp.ok) {
    const txt = await resp.text().catch(() => "");
    const result = {
      ok: false,
      error: `http_${resp.status}`,
      message: txt.slice(0, 200),
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  const data = await resp.json();
  if (wantJson) {
    console.log(JSON.stringify(data, null, 2));
    process.exit(0);
  }

  // 人类友好输出
  console.log(`query: "${data.query}"  count: ${data.count}  minScore: ${data.minScore ?? "default"}`);
  if (data.count === 0) {
    console.log("  (没召回, 试试降低 min_score 或换 query)");
  }
  for (const r of data.results) {
    console.log(`\n  [${r.score.toFixed(3)}] entry=${r.entryId}`);
    console.log(`    ${r.text.slice(0, 200)}${r.text.length > 200 ? "..." : ""}`);
  }
}

main().catch((e) => {
  console.error("opphub-knowledge-search fatal:", e?.message ?? e);
  process.exit(1);
});