#!/usr/bin/env node

/**
 * 详细行程必须通过 HTTP SSE 接口生成，不能复用 plan_multi WebSocket。
 * POST /trip-agent-api/api/plan/create_detail
 * Body: { "session_id": "<uuid>" }
 */

import {
  callCreateDetail,
  loadToken,
  parseBaseArgs,
  resolveSessionId,
} from "./trip_api_common.mjs";

async function main() {
  const args = parseBaseArgs(process.argv.slice(2));
  const token = loadToken(args.tokenFile);
  const sessionId = resolveSessionId(args);

  const result = await callCreateDetail(token, sessionId, args.verbose);

  if (result.detailPlan) {
    const out = {
      ok: true,
      sessionId,
      request: result.requestBody,
      detailedPlan: result.detailPlan,
      progress: result.progress,
      answer: "已帮你生成好行程规划",
    };
    if (args.json) {
      console.log(JSON.stringify(out, null, 2));
    } else {
      const days = Array.isArray(result.detailPlan["每日行程"]) ? result.detailPlan["每日行程"].length : 0;
      console.log(`详细行程已生成（${days} 天）`);
      if (result.progress.length) {
        console.error(`[progress] ${result.progress.join(" → ")}`);
      }
    }
    return;
  }

  const out = {
    ok: false,
    sessionId,
    request: result.requestBody,
    error: result.error,
    progress: result.progress,
    hint: "请先用 plan_multi 生成简约行程并写入 session-file，再调用本脚本。",
  };
  if (args.json) {
    console.log(JSON.stringify(out, null, 2));
  } else {
    console.error(result.error || "详细行程生成失败");
    console.error(out.hint);
  }
  process.exitCode = 1;
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
