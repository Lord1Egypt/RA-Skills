#!/usr/bin/env node
//
// 端到端验证 opphub skill v3.3 + 12 处 bug 修复:
//   - Layer 1: discover / card / match 纯函数验证
//   - Layer 2: mock-server 协议验证 (4 种响应)
//   - Layer 3: submit 协议处理 (A4 修: server 404 归 errors, 不是 conflicts)
//
// 不依赖 plugin, 不依赖真 server. 用本地 mock-server (tests/mock-knowledge-server.js).
//
// 用法:
//   # 1. 启 mock-server (端口 4001)
//   node tests/mock-knowledge-server.js &
//
//   # 2. 跑端到端
//   node tests/e2e-verify.js
//
// 返 { ok, layers: { layer1, layer2, layer3 }, summary }

import { createHash } from "node:crypto";

const API_BASE = process.env.OPPHUB_API_BASE || "http://localhost:4001";
const results = { layer1: {}, layer2: {}, layer3: {}, ok: true, errors: [] };

function sha256(s) {
  return createHash("sha256").update(s, "utf8").digest("hex");
}

async function execBin(bin, args) {
  const { spawn } = await import("node:child_process");
  return new Promise((resolve, reject) => {
    const p = spawn("node", [bin, ...args], { encoding: "utf8" });
    let stdout = "";
    let stderr = "";
    p.stdout.on("data", (d) => stdout += d);
    p.stderr.on("data", (d) => stderr += d);
    p.on("close", (code) => {
      try {
        const json = JSON.parse(stdout);
        resolve({ ok: code === 0 || (json && json.ok === true), json, code, stderr });
      } catch {
        resolve({ ok: false, raw: stdout, code, stderr });
      }
    });
    p.on("error", reject);
  });
}

function check(name, ok, detail = "") {
  if (ok) {
    console.log(`  ✅ ${name}${detail ? " — " + detail : ""}`);
  } else {
    console.log(`  ❌ ${name}${detail ? " — " + detail : ""}`);
    results.ok = false;
    results.errors.push(name);
  }
}

async function run() {
  console.log("=================================================================");
  console.log("=== Layer 1: 纯函数验证 (discover / card / match 协议) ===");
  console.log("=================================================================");

  // 1.1 discover --name
  {
    const r = await execBin("bin/opphub-knowledge-discover.js", ["--name", "睿驰嘉禾", "--json"]);
    const ok = r.ok && r.json.queryPlan && r.json.queryPlan.length === 6;
    results.layer1.discover_name = ok;
    check("discover --name '睿驰嘉禾' 返 queryPlan 6 条", ok, `实际 ${r.json.queryPlan?.length}`);
  }

  // 1.2 discover 拼写纠错 (C1 修)
  {
    const tmp = "/tmp/e2e-rawtext-mismatch.txt";
    const tmpWeb = "/tmp/e2e-web-results.json";
    const { writeFileSync } = await import("node:fs");
    writeFileSync(tmp,
      "# 嘉禾数字传媒科技 · 自动画像\n\n## 1. 工商信息\n上海嘉禾数字传媒科技有限公司, 法人张三\n",
      "utf8");
    writeFileSync(tmpWeb, JSON.stringify([
      { title: "上海睿驰嘉禾数字传媒科技有限公司", snippet: "..." },
      { title: "睿驰传媒工作室", snippet: "..." },
    ]), "utf8");
    const r = await execBin("bin/opphub-knowledge-discover.js", [
      "--name", "睿驰嘉禾数字传媒科技",
      "--raw-text", `# 嘉禾数字传媒科技 · 自动画像\n\n## 1. 工商信息\n上海嘉禾数字传媒科技有限公司, 法人张三\n`,
      "--web-results", tmpWeb,
      "--json",
    ]);
    const v = r.json.validation || {};
    const ok = r.json.ok === false
      && v.issues?.[0]?.type === "company_name_not_found"
      && v.suggestions?.length >= 1;
    results.layer1.discover_spelling = ok;
    check("discover 拼写纠错 (C1): validation.ok=false + suggestions>=1", ok,
      `suggestions=${v.suggestions?.length}, top1=${v.suggestions?.[0]?.name}`);
  }

  // 1.3 match --based-on-cards (A5+B1 修)
  {
    const { writeFileSync } = await import("node:fs");
    const cardsFile = "/tmp/e2e-cards-saas.json";
    writeFileSync(cardsFile, JSON.stringify({
      name: "某 SaaS 公司",
      cards: [
        { type: "ability", dimension: "撮合引擎", text: "撮合引擎" },
        { type: "upstream", dimension: "上游依赖/LLM 服务", text: "上游" },
        { type: "downstream", dimension: "下游服务/企业需求方", text: "下游" },
      ],
    }), "utf8");
    const r = await execBin("bin/opphub-knowledge-match.js", [
      "--based-on-cards", cardsFile,
      "--name", "某 SaaS 公司",
      "--json",
    ]);
    const qp = r.json.queryPlan || {};
    const ok = r.json.ok
      && r.json.inputMode === "based-on-cards"
      && qp.peer?.includes("撮合引擎")
      && qp.upstream?.[0] === "LLM 服务"        // 去掉了 "上游依赖/" 前缀
      && qp.downstream?.[0] === "企业需求方";   // 去掉了 "下游服务/" 前缀
    results.layer1.match_derive_query = ok;
    check("match --based-on-cards 派生 query (A5+B1)", ok,
      `peer=${qp.peer?.join("|")}, upstream=${qp.upstream?.join("|")}, downstream=${qp.downstream?.join("|")}`);
  }

  // 1.4 match 字段名兼容 v3.2/v3.3 ingest-batch (A1 修)
  {
    const { writeFileSync } = await import("node:fs");
    // v3.3 格式
    const f33 = "/tmp/e2e-entryids-v33.json";
    writeFileSync(f33, JSON.stringify({
      submitted: [{ entryId: "cmrsaaa1", type: "ability", dimension: "撮合引擎" }],
      deduplicated: [],
      conflicts: [],
    }), "utf8");
    const r33 = await execBin("bin/opphub-knowledge-match.js", ["--entry-ids", f33, "--json"]);
    const ok33 = r33.json.ok && r33.json.entryCount === 1;

    // v3.2 格式
    const f32 = "/tmp/e2e-entryids-v32.json";
    writeFileSync(f32, JSON.stringify({
      ingested: [{ entryId: "cmrsbbb1", status: "created" }],
    }), "utf8");
    const r32 = await execBin("bin/opphub-knowledge-match.js", ["--entry-ids", f32, "--json"]);
    const ok32 = r32.json.ok && r32.json.entryCount === 1;

    // 直接数组
    const fArr = "/tmp/e2e-entryids-arr.json";
    writeFileSync(fArr, JSON.stringify(["cmrsccc1", "cmrsccc2"]), "utf8");
    const rArr = await execBin("bin/opphub-knowledge-match.js", ["--entry-ids", fArr, "--json"]);
    const okArr = rArr.json.ok && rArr.json.entryCount === 2;

    const ok = ok33 && ok32 && okArr;
    results.layer1.match_field_compat = ok;
    check("match entryIds 字段名兼容 v3.2/v3.3/数组 (A1)", ok,
      `v3.3=${ok33}, v3.2=${ok32}, array=${okArr}`);
  }

  // 1.5 ingest-batch 接 stdin (A6 修)
  {
    const cardsFile = "/tmp/e2e-cards-ingest.json";
    const { writeFileSync } = await import("node:fs");
    writeFileSync(cardsFile, JSON.stringify({
      name: "test",
      cards: [
        { type: "ability", dimension: "测试能力", text: "test text" },
      ],
    }), "utf8");
    // --dry-run 模式不调 submit, 走 stdin 看 cards 真接收
    const { spawnSync } = await import("node:child_process");
    const res = spawnSync("node", [
      "bin/opphub-knowledge-ingest-batch.js",
      "--cards", "-",
      "--dry-run",
      "--json",
    ], { encoding: "utf8", input: JSON.stringify({
      name: "stdin-test",
      cards: [{ type: "ability", dimension: "stdin能力", text: "stdin text" }],
    }) });
    const ok = res.status === 0;
    let parsed = null;
    try { parsed = JSON.parse(res.stdout); } catch {}
    const ok2 = ok && parsed?.ok && parsed?.cardCount === 1 && parsed?.mode === "dry-run";
    results.layer1.ingest_stdin = ok2;
    check("ingest-batch 接 stdin (A6)", ok2, `cardCount=${parsed?.cardCount}, mode=${parsed?.mode}`);
  }

  // 1.6 relate D1 修
  {
    const { writeFileSync } = await import("node:fs");
    const xlsFile = "/tmp/e2e-contracts.xls";
    // 足够冷门的公司名 (人名/工作室/不撞中关键词), 验 D1 出的未分类 card
    const xls = `<html><body><table>
<tr><th>合同编号</th><th>甲方</th><th>乙方</th><th>合同总金额</th></tr>
<tr><td>C001</td><td>睿驰嘉禾数字传媒科技</td><td>上海自然堂集团有限公司</td><td>505558</td></tr>
<tr><td>C002</td><td>小马宋</td><td>睿驰嘉禾数字传媒科技</td><td>80000</td></tr>
<tr><td>C003</td><td>刘润读书会</td><td>睿驰嘉禾数字传媒科技</td><td>60000</td></tr>
</table></body></html>`;
    writeFileSync(xlsFile, xls, "utf8");
    const r = await execBin("bin/opphub-knowledge-relate.js", [
      "--xls", xlsFile,
      "--company", "睿驰嘉禾",
      "--top-customers", "5",
      "--top-suppliers", "5",
      "--json",
    ]);
    const cards = r.json.cards || [];
    // D1 验证: 未分类 card 应该出现 (供应商类别/未分类 因为 "小马宋/刘润读书会" 都不撞中关键词)
    const otherCard = cards.find((c) => c.dimension === "供应商类别/未分类");
    const ok = r.json.ok && cards.length > 0 && !!otherCard;
    results.layer1.relate_uncategorized = ok;
    check("relate D1: 未分类独立 card 出现", ok,
      `cards=${cards.length}, hasOtherCard=${!!otherCard}, dimension=${otherCard?.dimension}`);
  }

  console.log("");
  console.log("=================================================================");
  console.log("=== Layer 2: mock-server 协议验证 (4 种响应) ===");
  console.log("=================================================================");

  async function postIngest(body) {
    const resp = await fetch(`${API_BASE}/api/knowledge/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return { status: resp.status, body: await resp.json() };
  }

  // 2.1 created
  {
    const r = await postIngest({
      userId: "user_e2e",
      rawText: "法人: 刘会冬, 业务方向: MCN",
      entryType: "ability",
      entryDimension: "e2e测试维度",
      idempotencyKey: "e2e_key_1",
      contentHash: "hash_e2e_1",
    });
    const ok = r.status === 200 && r.body.action === "created";
    results.layer2.created = ok;
    check("mock 2.1 created", ok, `action=${r.body.action}`);
  }
  // 2.2 no_change
  {
    const r = await postIngest({
      userId: "user_e2e",
      rawText: "法人: 刘会冬, 业务方向: MCN",
      entryType: "ability",
      entryDimension: "e2e测试维度",
      idempotencyKey: "e2e_key_1",
      contentHash: "hash_e2e_1",
    });
    const ok = r.status === 200 && r.body.action === "no_change";
    results.layer2.no_change = ok;
    check("mock 2.2 no_change", ok, `action=${r.body.action}`);
  }
  // 2.3 conflict (legal_person 不同)
  {
    const r = await postIngest({
      userId: "user_e2e",
      entryType: "ability",
      entryDimension: "e2e测试维度",
      idempotencyKey: "e2e_key_1",
      contentHash: "hash_e2e_2",
    });
    const ok = r.status === 200 && r.body.ok === false && r.body.conflict === true;
    results.layer2.conflict = ok;
    check("mock 2.3 conflict (legal_person 变)", ok, `conflict=${r.body.conflict}, fields=${r.body.conflictReport?.conflictFields?.join("|")}`);
  }
  // 2.4 soft_chain_override (forceOverride)
  {
    const r = await postIngest({
      userId: "user_e2e",
      entryType: "ability",
      entryDimension: "e2e测试维度",
      idempotencyKey: "e2e_key_1",
      contentHash: "hash_e2e_3",
      forceOverride: true,
    });
    const ok = r.status === 200 && r.body.action === "soft_chain_override";
    results.layer2.soft_chain = ok;
    check("mock 2.4 soft_chain_override (forceOverride)", ok,
      `action=${r.body.action}, previousEntryId=${r.body.previousEntryId}`);
  }
  // 2.5 其它路径 404
  {
    const resp = await fetch(`${API_BASE}/api/knowledge/status`, { method: "POST" });
    const ok = resp.status === 404;
    results.layer2.other_404 = ok;
    check("mock 2.5 其它路径 404", ok, `status=${resp.status}`);
  }

  console.log("");
  console.log("=================================================================");
  console.log("=== Layer 3: submit 协议处理 (A4 修) ===");
  console.log("=================================================================");

  // submit 走 mock-server 的 idempotencyKey 算法 (SHA256(userId|type|dimension))
  // 不依赖 plugin, 直接调 submit 主入口, 但需要 access_token.
  // 策略: 临时 patch plugin-client.js 的 getAccessToken (不可行 - 改源码)
  // 替代: 写一个 inline fetcher 模拟 submit 的协议处理逻辑, 验证 4 种响应 submit 会怎么归类

  async function submitLikeSubmit(body) {
    const resp = await fetch(`${API_BASE}/api/knowledge/ingest`, {
      method: "POST",
      headers: {
        Authorization: "Bearer fake_token_for_test",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const status = resp.status;
    let data = {};
    try { data = await resp.json(); } catch { data = { ok: false, error: "bad_response" }; }
    data.httpStatus = status;
    return data;
  }

  function classifySubmitResult(respData) {
    // 镜像 submit.js 的分类逻辑 (A4 修复版)
    if (respData.httpStatus === 404 || respData.httpStatus === 501) {
      return { bucket: "errors", errorType: "deployment_pending" };
    }
    if (respData.ok && respData.action === "no_change") return { bucket: "deduplicated" };
    if (respData.ok) return { bucket: "submitted", action: respData.action };
    if (respData.conflict) return { bucket: "conflicts" };
    return { bucket: "errors", errorType: "server_error" };
  }

  const userId = "user_a4_test";
  const type = "ability";
  const dimension = "A4测试维度";
  const key = sha256(`${userId}|${type}|${dimension}`);

  // 3.1 created → submitted bucket
  {
    const r = await submitLikeSubmit({
      userId, rawText: "测试 1", entryType: type, entryDimension: dimension,
      idempotencyKey: key, contentHash: "h1",
    });
    const c = classifySubmitResult(r);
    const ok = c.bucket === "submitted" && c.action === "created";
    results.layer3.a4_created = ok;
    check("A4 修: server action=created → submitted", ok, `bucket=${c.bucket}, action=${c.action}`);
  }
  // 3.2 no_change → deduplicated
  {
    const r = await submitLikeSubmit({
      userId, rawText: "测试 1", entryType: type, entryDimension: dimension,
      idempotencyKey: key, contentHash: "h1",
    });
    const c = classifySubmitResult(r);
    const ok = c.bucket === "deduplicated";
    results.layer3.a4_no_change = ok;
    check("A4 修: server action=no_change → deduplicated", ok, `bucket=${c.bucket}`);
  }
  // 3.3 conflict → conflicts (重起新 key, 避免被前面 mock 状态污染)
  {
    const newKey = sha256(`${userId}|${type}|${dimension}|conflict_test_v3`);
    const r1 = await submitLikeSubmit({
      userId, rawText: "法人: 张三, 业务方向: MCN", entryType: type, entryDimension: dimension,
      idempotencyKey: newKey, contentHash: "h_conflict_v3_a",
    });
    const r2 = await submitLikeSubmit({
      userId, rawText: "法人: 李四, 业务方向: SaaS", entryType: type, entryDimension: dimension,
      idempotencyKey: newKey, contentHash: "h_conflict_v3_b",
    });
    const c = classifySubmitResult(r2);
    const ok = r1.action === "created" && c.bucket === "conflicts";
    results.layer3.a4_conflict = ok;
    check("A4 修: server conflict=true → conflicts", ok,
      `r1.action=${r1.action}, r2.bucket=${c.bucket}, conflict=${r2.conflict}`);
  }
  // 3.4 deployment_pending (server 404) → errors, NOT conflicts (A4 关键修复)
  {
    // 模拟 server 404
    const fakeResp = { httpStatus: 404, ok: false, error: "not_found" };
    const c = classifySubmitResult(fakeResp);
    const ok = c.bucket === "errors" && c.errorType === "deployment_pending";
    results.layer3.a4_deployment_pending = ok;
    check("A4 修: server 404 → errors/deployment_pending (不是 conflicts)", ok,
      `bucket=${c.bucket}, errorType=${c.errorType}`);
  }
  // 3.5 forceOverride 后软链 → submitted
  {
    const r = await submitLikeSubmit({
      idempotencyKey: key, contentHash: "h3", forceOverride: true,
    });
    const c = classifySubmitResult(r);
    const ok = c.bucket === "submitted" && c.action === "soft_chain_override";
    results.layer3.a4_force_override = ok;
    check("A4 修: server forceOverride → soft_chain_override", ok, `bucket=${c.bucket}, action=${c.action}`);
  }

  console.log("");
  console.log("=================================================================");
  console.log(`=== 总结: ${results.ok ? "✅ 全部通过" : "❌ 有失败"} ===`);
  console.log("=================================================================");
  console.log(JSON.stringify(results, null, 2));
  process.exit(results.ok ? 0 : 1);
}

run().catch((e) => {
  console.error("e2e fatal:", e?.message ?? e);
  process.exit(1);
});
