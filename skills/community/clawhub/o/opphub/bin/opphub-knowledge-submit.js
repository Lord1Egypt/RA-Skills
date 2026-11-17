#!/usr/bin/env node
// bin/opphub-knowledge-submit.js · v3.3.0
// status: implemented (v3.3 idempotent ingest + 冲突检测 + 软链覆盖)
//
//
// 本 bin 职责:
//   - 算 idempotencyKey + contentHash (SHA256, skill 端算好给 server)
//   - 调 server POST /api/knowledge/ingest v2 (idempotent)
//   - 透传 4 种响应: created / no_change / soft_chain_override / conflict
//
//   - 不做去重
//   - 不做冲突判断
//   - 不做版本管理
//   - 不做蒸馏 / 嵌入 / 召回 (那是 server worker 的活)
//
// 用法: bot 调 (阶段 5 批量入库)
//   opphub knowledge-submit --cards /path/to/cards.json --json
//   opphub knowledge-submit --cards /path/to/cards.json --force-override-conflict --json
//   opphub knowledge-submit --cards /path/to/cards.json --cards-out /path/to/results.json --json
//
// 输入 cards.json 格式 (knowledge-card 输出):
//   {
//     "name": "睿驰嘉禾",
//     "cards": [
//       { "index": 0, "type": "ability", "dimension": "达人营销", "text": "..." },
//       { "index": 1, "type": "ability", "dimension": "短视频内容制作", "text": "..." }
//     ]
//   }
//
// 输出 results JSON:
//   {
//     ok: true,
//     userId: "user_xxx",
//     summary: { submitted: 7, deduplicated: 3, conflicts: 1 },
//     submitted: [{ cardIndex, entryId, action, previousEntryId }],
//     deduplicated: [{ cardIndex, entryId }],
//     conflicts: [{ cardIndex, conflictReport: { entryId, oldRawText, newRawText, conflictFields } }],
//     nextStep: "..."   // bot 解读用
//   }

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { getAccessToken as pluginGetAccessToken } from "../lib/opphub-plugin-client.js";

// E2E / mock 模式 (env):
//   OPPHUB_MOCK_TOKEN  E2E 测试占位符 (不是真 token, 只用于 mock server 协议测试)
//   OPPHUB_MOCK_USER_ID  mock 对应的 userId (从测试 JWT 解不出来时 fallback)
// ClawHub audit flagged env_credential_access - 这俩仅用于 E2E, 不含真 token
const MOCK_TOKEN = process.env.OPPHUB_MOCK_TOKEN || null;
const MOCK_USER_ID = process.env.OPPHUB_MOCK_USER_ID || null;

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";

function parseArgs(argv) {
  const args = { _: [], forceOverrideConflict: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--help" || a === "-h") args.help = true;
    else if (a === "--cards") args.cards = argv[++i];
    else if (a === "--cards-out") args.cardsOut = argv[++i];
    else if (a === "--force-override-conflict") args.forceOverrideConflict = true;
    else if (a === "--confirm") args.confirm = true;
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

function out(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

function sha256(s) {
  return createHash("sha256").update(s, "utf8").digest("hex");
}

// 简单 base64url 解码, 拿 JWT payload 里的 userId
function decodeJwtPayload(token) {
  try {
    const part = token.split(".")[1];
    const padded = part + "=".repeat((4 - (part.length % 4)) % 4);
    const json = Buffer.from(padded.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8");
    return JSON.parse(json);
  } catch {
    return {};
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  // --help
  if (args.help || args._.includes("help")) {
    console.log(`opphub-knowledge-submit · v3.3.0

用途: 把 cards 提交给 server, 接收 conflictReport, 不做任何判断.

用法:
  opphub knowledge-submit --cards <cards.json> [--force-override-conflict] [--cards-out <results.json>] [--json]

输入 cards.json 格式 (跟 knowledge-card 输出对齐):
  {
    "name": "睿驰嘉禾",
    "cards": [
      { "index": 0, "type": "ability", "dimension": "达人营销", "text": "..." }
    ]
  }

输出 results JSON:
  {
    ok: true,
    userId: "user_xxx",
    summary: { submitted, deduplicated, conflicts },
    submitted: [{ cardIndex, entryId, action }],
    deduplicated: [{ cardIndex, entryId }],
    conflicts: [{ cardIndex, conflictReport }],
    nextStep: "..."
  }

server 端 4 种响应 (POST /api/knowledge/ingest v2):
  1. created              - 新增成功
  2. no_change            - 幂等命中 (rawText 没变)
  3. soft_chain_override  - 软链覆盖 (rawText 变了但无关键字段冲突)
  4. conflict             - 冲突返报告 (等用户拍)

跟 knowledge-add (v3.1) 的区别:
  knowledge-add: 单条入库, 无幂等, 无冲突检测
  knowledge-submit: 批量, 幂等, 冲突返报告, 取代 knowledge-ingest-batch
`);
    process.exit(0);
  }

  // 1. 校验输入
  if (!args.cards) {
    if (wantJson) out({ ok: false, error: "missing_cards", message: "需要 --cards <cards.json>" });
    process.exit(1);
  }
  if (!existsSync(args.cards)) {
    if (wantJson) out({ ok: false, error: "cards_not_found", message: `cards 文件不存在: ${args.cards}` });
    process.exit(1);
  }

  let cardsDoc;
  try {
    cardsDoc = JSON.parse(readFileSync(args.cards, "utf8"));
  } catch (e) {
    if (wantJson) out({ ok: false, error: "cards_invalid_json", message: e?.message ?? String(e) });
    process.exit(1);
  }
  const cards = Array.isArray(cardsDoc) ? cardsDoc : cardsDoc.cards;
  if (!Array.isArray(cards) || cards.length === 0) {
    if (wantJson) out({ ok: false, error: "no_cards", message: "cards 数组为空" });
    process.exit(1);
  }
  const parsedFields = cardsDoc.parsedFields ?? null;

  // v4.0.9: confirmation state machine - 默认拒绝, 收到 --confirm 才入库
  if (!args.confirm) {
    if (wantJson) out({
      ok: false,
      error: "needs_confirmation",
      message: "未确认 — 需先跑 knowledge-card 看 confirmation 清单, 用户回复'确认'后再加 --confirm 入库",
    });
    process.exit(1);
  }

  let accessToken;
  try {
    accessToken = MOCK_TOKEN || await pluginGetAccessToken();
  } catch (e) {
    if (wantJson) out({
      ok: false,
      error: "token_unavailable",
      message: `拿不到 access_token: ${e?.message ?? e}\n请先跑偶合登录.`
    });
    process.exit(1);
  }
  if (!accessToken) {
    if (wantJson) out({ ok: false, error: "no_token", message: "access_token 为空, 请先偶合登录" });
    process.exit(1);
  }
  const userId = MOCK_USER_ID || decodeJwtPayload(accessToken).userId;
  if (!userId) {
    if (wantJson) out({ ok: false, error: "invalid_token", message: "JWT 里没有 userId" });
    process.exit(1);
  }

  // 3. 提交每条 card
  // A4 修复: 区分 4 种结果 — submitted / deduplicated / conflicts / errors
  //   - errors 不算 conflicts: 含 deployment_pending (server v2 endpoint 未接)
  //                              + network_error (网络挂)
  //                              + server_error (401/500/...)
  const results = { submitted: [], deduplicated: [], conflicts: [], errors: [] };

  for (const card of cards) {
    const cardIndex = card.index ?? cards.indexOf(card);
    const { type, dimension, text } = card;
    if (!type || !dimension || !text) {
      // 缺字段, 跳过 (skill 不做判断, 但本 bin 至少保证 rawText 完整)
      continue;
    }
    // v4.0.9: 兜底 - 老的 card.text 没版本头时, 补上 (旧 skill 数据兼容)
    const textWithHeader = text.startsWith("<!-- opphub-raw-text-v1 -->")
      ? text
      : `<!-- opphub-raw-text-v1 -->\n${text}`;
    const idempotencyKey = sha256(`${userId}|${type}|${dimension}`);
    const contentHash = sha256(textWithHeader);

    let respData;
    let httpStatus = 0;
    try {
      const resp = await fetch(`${API_BASE}/api/user/knowledge/ingest`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId,
          rawText: textWithHeader,
          sourceType: "auto",
          entryType: type,
          entryDimension: dimension,
          idempotencyKey,
          contentHash,
          parsedFields: parsedFields ?? undefined,
          forceOverride: args.forceOverrideConflict,
        }),
      });
      httpStatus = resp.status;
      respData = await resp.json().catch(() => ({ ok: false, error: "bad_response", httpStatus }));
    } catch (e) {
      results.errors.push({
        cardIndex,
        dimension,
        type,
        errorReport: {
          type: "network_error",
          message: e?.message ?? String(e),
        },
      });
      continue;
    }

    // A4 修: server 返 404/501 (endpoint 未接) → errors/deployment_pending
    if (httpStatus === 404 || httpStatus === 501) {
      results.errors.push({
        cardIndex,
        dimension,
        type,
        errorReport: {
          type: "deployment_pending",
          httpStatus,
          hint: "v3.3 schema 已写, 等 server 接 v2 endpoint",
        },
      });
      continue;
    }

    if (respData.ok && respData.action === "no_change") {
      results.deduplicated.push({
        cardIndex,
        entryId: respData.entryId,
        dimension,
        type,
      });
    } else if (respData.ok) {
      // created 或 soft_chain_override 都算 submitted
      results.submitted.push({
        cardIndex,
        entryId: respData.entryId,
        dimension,
        type,
        action: respData.action || "created",
        previousEntryId: respData.previousEntryId || null,
      });
    } else if (respData.conflict) {
      results.conflicts.push({
        cardIndex,
        dimension,
        type,
        conflictReport: respData.conflictReport,
      });
    } else {
      results.errors.push({
        cardIndex,
        dimension,
        type,
        errorReport: {
          type: "server_error",
          httpStatus,
          message: respData.error || respData.message || "unknown",
          raw: respData,
        },
      });
    }
  }

  // 4. 出结果
  const result = {
    ok: results.errors.length === 0,
    okDetail: results.errors.length === 0
      ? null
      : "部分卡片提交失败",
    userId,
    summary: {
      submitted: results.submitted.length,
      deduplicated: results.deduplicated.length,
      conflicts: results.conflicts.length,
      errors: results.errors.length,
      deploymentPending: results.errors.filter((e) => e.errorReport?.type === "deployment_pending").length,
      networkError: results.errors.filter((e) => e.errorReport?.type === "network_error").length,
      serverError: results.errors.filter((e) => e.errorReport?.type === "server_error").length,
    },
    submitted: results.submitted,
    deduplicated: results.deduplicated,
    conflicts: results.conflicts,
    errors: results.errors,
    nextStep:
      results.errors.length > 0
        ? "有错误, fix and retry"
        : results.conflicts.length > 0
        ? "用 bot.skillApi.askInteractive 让用户拍冲突项 (保留旧的/用新的/跳过)"
        : results.submitted.length > 0
        ? "知识已入库, 跑 knowledge-match 做上下游关联"
        : "全部 idempotent 命中, 无新 entry, 跑 knowledge-match 时用 deduplicated 里的 entryIds",
  };

  if (args.cardsOut) {
    writeFileSync(args.cardsOut, JSON.stringify(result, null, 2));
  }
  out(result);
}

main().catch((e) => {
  console.error("opphub-knowledge-submit fatal:", e?.message ?? e);
  process.exit(1);
});
