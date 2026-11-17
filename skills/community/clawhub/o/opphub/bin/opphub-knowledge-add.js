#!/usr/bin/env node
// bin/opphub-knowledge-add.js · v4.0
// status: implemented (单条入库, v3.1)
//
//
// 用法: bot 调
//   opphub knowledge-add --raw-text "..." --source-type manual --json
//   opphub knowledge-add --raw-text "..." --source-type auto --json
//   opphub knowledge-add --file /path/to/bp.pdf --source-type upload --json
//   opphub knowledge-add --url https://zhuanlan.zhihu.com/xxx --source-type url --json
// 返 { ok, entryId, chunkCount, embeddingModel, embeddingVersion, tags }
// skill 拿到后出飞书 card 告诉用户入库成功

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

import { getAccessToken as pluginGetAccessToken } from "../lib/opphub-plugin-client.js";

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";
const TOKEN_FILE = join(homedir(), ".opphub-plugin/token.json");

async function getAccessToken() {
  // 用 getAccessToken (不是 readToken) 让 plugin 自动 refresh 过期的 access_token
  // getAccessToken() 返回的是 access_token 字符串 (不是 {access_token} 对象),
  // 拋 NeedAuthorizationError 时 (plugin 不在, refresh_token 也过期) catch 返 null
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
    else if (a === "--raw-text") args.rawText = argv[++i];
    else if (a === "--file") args.file = argv[++i];
    else if (a === "--url") args.url = argv[++i];
    else if (a === "--source-type") args.sourceType = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  // 校验参数
  if (!args.rawText && !args.file && !args.url) {
    const result = {
      ok: false,
      error: "missing_content",
      message: "需要 --raw-text / --file / --url 之一",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }
  const sourceType = args.sourceType || (args.rawText ? "manual" : args.file ? "upload" : "url");
  if (!["manual", "auto", "url", "upload", "llm-augmented"].includes(sourceType)) {
    const result = {
      ok: false,
      error: "invalid_source_type",
      message: `source_type 必须是 manual/auto/url/upload/llm-augmented, 收到 ${sourceType}`,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  // 拿 token (走 plugin getAccessToken 自动 refresh)
  const token = await getAccessToken();
  if (!token?.access_token) {
    const result = {
      ok: false,
      error: "need_login",
      message: "先跑偶合登录",
      hint: "@bot 偶合登录 走 device flow",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  // 准备 rawText (file / url 走 server 端 fetch, skill 这边不重复)
  let rawText = args.rawText;
  let sourceUrl = args.url || null;

  if (args.file) {
    if (!existsSync(args.file)) {
      const result = {
        ok: false,
        error: "file_not_found",
        message: `${args.file} 不存在`,
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
    rawText = readFileSync(args.file, "utf8");
  }

  // (server 端: 切片 + BGE-M3 embedding + tsvector 全文 + distilledTags)
  const url = `${API_BASE}/api/user/knowledge/ingest`;
  let resp;
  try {
    resp = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        rawText,
        sourceType,
        sourceUrl,
      }),
    });
  } catch (e) {
    const result = {
      ok: false,
      error: "network_failed",
      message: `POST ${url} 失败: ${e?.message ?? String(e)}`,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  if (!resp.ok) {
    if (resp.status === 404 || resp.status === 501) {
      const result = {
        ok: false,
        error: "server_not_deployed",
        message: `server 返 ${resp.status}: /api/user/knowledge/ingest endpoint 未部署 (schema migration 没跑)`,
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
  const result = {
    ok: true,
    entryId: data.entryId,
    chunkCount: data.chunkCount,
    embeddingModel: data.embeddingModel,
    embeddingVersion: data.embeddingVersion,
    tags: data.tags ?? [],
  };
  if (wantJson) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`✅ 入库成功: entryId=${result.entryId}, chunks=${result.chunkCount}`);
  }
}

main().catch((e) => {
  console.log(JSON.stringify({ ok: false, error: "unknown", message: e?.message ?? String(e) }, null, 2));
  process.exit(1);
});
