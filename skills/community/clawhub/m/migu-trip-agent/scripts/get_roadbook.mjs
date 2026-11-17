#!/usr/bin/env node

import {
  ROADBOOK_PATH,
  callCreateDetail,
  loadToken,
  parseBaseArgs,
  postJson,
  redact,
  resolveSessionId,
} from "./trip_api_common.mjs";


function explainRoadbookFailure(result, sessionId) {
  const code = result.json?.code;
  const msg = result.json?.msg || "";
  if (code === 400) {
    return `会话不存在或已失效（session_id=${sessionId}）。服务端: ${msg}`;
  }
  if (code === -1) {
    return "路书生成失败（code=-1）：该 session 尚未生成详细行程，请先执行 scripts/create_detail.mjs";
  }
  return `路书接口失败: ${redact(result.raw || JSON.stringify(result.json))}`;
}

async function makeRoadbook(token, sessionId, verbose) {
  const body = { session_id: sessionId };
  if (verbose) {
    console.error(`[roadbook] POST ${ROADBOOK_PATH}`);
    console.error(`[roadbook] body=${JSON.stringify(body)}`);
  }
  const result = await postJson(ROADBOOK_PATH, token, body);
  if (verbose) console.error(`[roadbook] HTTP ${result.statusCode} resp=${redact(result.raw)}`);
  return { ...result, requestBody: body };
}

async function main() {
  const args = parseBaseArgs(process.argv.slice(2), { skipCreateDetail: false });
  const token = loadToken(args.tokenFile);
  const sessionId = resolveSessionId(args);

  if (!args.skipCreateDetail) {
    const detail = await callCreateDetail(token, sessionId, args.verbose);
    if (!detail.detailPlan) {
      const msg = detail.error || "详细行程生成失败，无法继续生成路书";
      if (args.json) {
        console.log(JSON.stringify({ ok: false, stage: "create_detail", sessionId, error: msg }, null, 2));
      } else {
        console.error(msg);
      }
      process.exitCode = 1;
      return;
    }
  }

  const road = await makeRoadbook(token, sessionId, args.verbose);
  const { json } = road;

  if (json?.code === 0 && json?.data) {
    const out = {
      ok: true,
      sessionId,
      request: road.requestBody,
      rb_name: json.data.rb_name,
      rb_image_url: json.data.rb_image_url,
    };
    if (args.json) {
      console.log(JSON.stringify(out, null, 2));
    } else {
      console.log(`路书名称：${json.data.rb_name}`);
      console.log(`路书图片：${json.data.rb_image_url}`);
    }
    return;
  }

  const err = explainRoadbookFailure(road, sessionId);
  if (args.json) {
    console.log(
      JSON.stringify({ ok: false, sessionId, request: road.requestBody, response: json, error: err }, null, 2),
    );
  } else {
    console.error(err);
  }
  process.exitCode = 1;
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
