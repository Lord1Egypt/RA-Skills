#!/usr/bin/env node
// bin/opphub-knowledge-status.js · v4.0.0
// status: implemented (v4 P2-6: GET 改 v2 路径 /api/knowledge?userId=...)
//
//
// v4.0.0 P2-6: 路径统一 v2
//   旧: GET /api/user/knowledge/status
//   新: GET /api/knowledge?userId=...&entryType=...
//   POST /api/knowledge/ingest 暂未合并 (server 端保持 /api/user/knowledge/ingest)
//
// 用法: bot 调 `opphub knowledge-status --json`
// 返 { ok, entries: [{id, sourceType, rawText, chunkCount, visibility, lastKnowledgeAt}], knowledgeCount, lastKnowledgeAt }
// skill 拿到后:
//   - entries.length > 0 → 跳过录入, 引导追加新条目
//   - entries.length = 0 → 触发 Step 6.2 手动录入 / 6.3 自动抓取

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

import { readToken as pluginReadToken } from "../lib/opphub-plugin-client.js";

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";
const TOKEN_FILE = join(homedir(), ".opphub-plugin/token.json");

async function readToken() {
  // 原代码直读 ~/.opphub-plugin/token.json (Linux fallback), mac 下永远是空 → 返 need_login
  try {
    return await pluginReadToken();
  } catch {
    return null;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const wantJson = args.includes("--json");

  const token = await readToken();
  if (!token?.access_token) {
    const result = {
      ok: false,
      error: "need_login",
      message: "先跑偶合登录",
      hint: "@bot 偶合登录 走 device flow",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error("✗ 未登录");
    process.exit(1);
  }

  // v4.0.0 P2-6: 改 v2 路径 GET /api/knowledge?userId=...
  // (v3.1 旧路径 /api/user/knowledge/status 已被 v2 替代, server 端实测已支持)
  // user_id 缺失 → 用 'me' alias (server 端 /api/knowledge/route.ts:21 支持)
  const userIdParam = token.user_id && token.user_id.length > 0
    ? encodeURIComponent(token.user_id)
    : "me";
  const url = `${API_BASE}/api/knowledge?userId=${userIdParam}`;
  let resp;
  try {
    resp = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token.access_token}`,
      },
    });
  } catch (e) {
    const result = {
      ok: false,
      error: "network_failed",
      message: `GET ${url} 失败: ${e?.message ?? String(e)}`,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  if (!resp.ok) {
    // server 端如果还没实现 (opphub-server 团队活)
    if (resp.status === 404 || resp.status === 501) {
      const result = {
        ok: true,
        entries: [],
        knowledgeCount: 0,
        lastKnowledgeAt: null,
        hint: "server 端 /api/knowledge v2 GET 已支持 (7/22 实测), skill 端已迁移",
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }
    const text = await resp.text().catch(() => "");
    const result = {
      ok: false,
      error: `http_${resp.status}`,
      message: `${url}: ${text.trim().slice(0, 200)}`,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  let data = {};
  try {
    data = await resp.json();
  } catch {}
  // server 端 v2 响应: { ok: true, data: Capability[], total, pagination }
  // v3.1 旧响应: { ok: true, entries: [...], knowledgeCount, lastKnowledgeAt }
  // 兼容两者
  const entries = data.entries ?? data.data ?? [];
  const result = {
    ok: true,
    entries: Array.isArray(entries) ? entries : [],
    knowledgeCount: data.knowledgeCount ?? data.total ?? entries.length ?? 0,
    lastKnowledgeAt: data.lastKnowledgeAt ?? entries[0]?.createdAt ?? entries[0]?.updatedAt ?? null,
  };
  if (wantJson) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`知识库条目: ${result.knowledgeCount} 条`);
    if (result.lastKnowledgeAt) console.log(`最近更新: ${result.lastKnowledgeAt}`);
  }
}

main().catch((e) => {
  console.log(JSON.stringify({ ok: false, error: "unknown", message: e?.message ?? String(e) }, null, 2));
  process.exit(1);
});