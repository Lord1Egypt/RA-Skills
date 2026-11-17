#!/usr/bin/env node
// bin/opphub-knowledge-match.js · v4.0
// status: implemented (关联匹配, v3.2)
//
//   入库完跑 1 次撮合匹配 (上下游 + 同业)
//   用 opphub-knowledge-search 拉 opphub 里其他 OPC 的条目
//
// 用法: bot 调
//   opphub knowledge-match --based-on-cards /tmp/cards.json --name "睿驰嘉禾" --json  (推荐)
//   opphub knowledge-match --entry-ids /tmp/entryIds.json --name "睿驰嘉禾" --json      (兼容老姿势)
//   opphub knowledge-match --based-on-cards /tmp/cards.json --entry-ids /tmp/ids.json --json (组合)
// 返 { ok, name, inputMode, queryPlan, upstream: [...], downstream: [...], peer: [...], insufficient, summary }
//
//   - A1: ingest-batch v3.2 (`ingested`) / v3.3 (`submitted` / `deduplicated`) 字段名兼容
//   - A5: 新加 --based-on-cards, 从 cards.json 反推 query (取代硬编码关键词)
//   - B1: 去硬编码 UPSTREAM_QUERIES/DOWNSTREAM_QUERIES/PEER_QUERIES (v3.2 写死, 不准录 SaaS/律所)
//
// 不做的事:
//   - 不入库 (纯查询)
//   - 不调 LLM (skill turn 的活)

import { readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SEARCH_BIN = join(__dirname, "opphub-knowledge-search.js");

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--entry-ids") args.entryIds = argv[++i];
    else if (a === "--based-on-cards") args.basedOnCards = argv[++i];
    else if (a === "--name") args.name = argv[++i];
    else if (a === "--min-score") args.minScore = argv[++i];
    else if (a === "--limit") args.limit = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

// 通用输出 helper: 当 wantJson 时打 JSON, 不然打 stderr 一行说明 + 用 stdout 打同一 JSON
function out(obj, wantJson) {
  const txt = JSON.stringify(obj, null, 2);
  if (wantJson) {
    console.log(txt);
  } else {
    if (obj.ok) {
      console.log(txt); // 人类输出也走 JSON, 跟其他 bin 一致
    } else {
      console.error(`✗ ${obj.error}: ${obj.message}`);
      console.error(JSON.stringify(obj, null, 2));
    }
  }
}

// 从 cards.json 拆 (type, dimension) pairs, 按 type 分桶返 3 类 query:
//   - upstream / upstream_category   → 搜 "提供 X"  (对方视角是 downstream)
//   - downstream / downstream_category → 搜 "需要 X"  (对方视角是 upstream)
//   - ability / peer                  → 搜 "也提供 X" (同业)
// 其它 type (e.g. industry v3.3 还没接) 直接忽略, 不出 query
// dimension 处理: 去掉 relate 流程的 "供应商/..." / "客户/..." / "客户类别/..." / "供应商类别/..." /
// "上游依赖/..." / "下游服务/..." 这些前缀, 留末段作为 query
function deriveQueriesFromCards(cards) {
  const upstreamQueries = [];
  const downstreamQueries = [];
  const peerQueries = [];

  const stripRelatePrefix = (dim) => {
    const m = dim.match(/^(?:上游依赖|下游服务|供应商|客户|供应商类别|客户类别)\/(.+)$/);
    return m ? m[1].trim() : dim;
  };

  const seenUp = new Set();
  const seenDown = new Set();
  const seenPeer = new Set();

  const pushUnique = (set, arr, v) => {
    if (set.has(v)) return;
    set.add(v);
    arr.push(v);
  };

  for (const c of cards) {
    if (!c) continue;
    const type = (c.type || "").toLowerCase();
    let dim = (c.dimension || "").trim();
    if (!dim) continue;
    dim = stripRelatePrefix(dim);
    if (!dim) continue;

    if (type === "upstream" || type === "upstream_category") {
      pushUnique(seenUp, upstreamQueries, dim);
    } else if (type === "downstream" || type === "downstream_category") {
      pushUnique(seenDown, downstreamQueries, dim);
    } else if (type === "ability" || type === "peer") {
      pushUnique(seenPeer, peerQueries, dim);
    }
    // industry / other: v3.3 不出 query
  }
  return { upstream: upstreamQueries, downstream: downstreamQueries, peer: peerQueries };
}

// 用 search bin 查 opphub 知识库
function searchOpc(query, limit, minScore) {
  const sargs = [
    SEARCH_BIN,
    "--q", query,
    "--limit", String(limit || 3),
    "--json",
  ];
  if (minScore) sargs.push("--min-score", String(minScore));
  // spawnSync node <search-script> (ClawHub audit flagged dangerous_exec)
  // 安全设计: 仅 spawn("node", argv), stdio pipe, timeout 30s
  // 业务必需: 调用 knowledge-search 做向量召回
  const res = spawnSync("node", sargs, { encoding: "utf8", timeout: 30_000 });
  if (res.error || res.status !== 0) {
    return { ok: false, error: res.error?.message || res.stderr || "search failed" };
  }
  try {
    return JSON.parse(res.stdout);
  } catch {
    return { ok: false, error: "invalid search response" };
  }
}

// 兼容 ingest-batch 各版本字段名:
//   v3.2 老接口: { ingested: [{cardIndex, entryId, status}] }
//   v3.3 新接口: { submitted: [...], deduplicated: [...], conflicts: [...] }
// 只为"小计 + 校验召回"用, --based-on-cards 模式不需要
function extractEntryIds(entryIdsData) {
  if (Array.isArray(entryIdsData)) return entryIdsData.filter(Boolean);
  if (entryIdsData && typeof entryIdsData === "object") {
    const pool = entryIdsData.submitted ?? entryIdsData.ingested ?? entryIdsData.deduplicated ?? [];
    const ids = pool.map((r) => r?.entryId).filter(Boolean);
    if (ids.length > 0) return ids;
  }
  return [];
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  // 两种姿势兼容: --based-on-cards 优先 (推荐), --entry-ids 老姿势仍支持, 二者都给也行
  if (!args.basedOnCards && !args.entryIds) {
    out({
      ok: false,
      error: "missing_input",
      message: "需要 --based-on-cards <cards.json> (推荐) 或 --entry-ids <entryIds.json> (兼容老姿势)",
    }, wantJson);
    process.exit(1);
  }

  // (a) --based-on-cards 路径
  let cards = null;
  if (args.basedOnCards) {
    if (!existsSync(args.basedOnCards)) {
      out({
        ok: false,
        error: "based_on_cards_not_found",
        message: `cards 文件不存在: ${args.basedOnCards}`,
      }, wantJson);
      process.exit(1);
    }
    let cardsDoc;
    try {
      cardsDoc = JSON.parse(readFileSync(args.basedOnCards, "utf8"));
    } catch (e) {
      out({
        ok: false,
        error: "based_on_cards_invalid_json",
        message: e?.message ?? String(e),
      }, wantJson);
      process.exit(1);
    }
    cards = Array.isArray(cardsDoc) ? cardsDoc : (cardsDoc.cards ?? []);
    if (!Array.isArray(cards) || cards.length === 0) {
      out({
        ok: false,
        error: "no_cards",
        message: "--based-on-cards 传入的 cards 数组为空",
      }, wantJson);
      process.exit(1);
    }
  }

  // (b) --entry-ids 路径 (兼容老姿势, 只为小计 + 校验召回)
  let entryIdsData = null;
  if (args.entryIds) {
    if (!existsSync(args.entryIds)) {
      out({
        ok: false,
        error: "entry_ids_not_found",
        message: `entryIds 文件不存在: ${args.entryIds}`,
      }, wantJson);
      process.exit(1);
    }
    try {
      entryIdsData = JSON.parse(readFileSync(args.entryIds, "utf8"));
    } catch (e) {
      out({
        ok: false,
        error: "invalid_entry_ids_json",
        message: e?.message ?? String(e),
      }, wantJson);
      process.exit(1);
    }
  }

  // 抽 entryIds (兼容 ingest-batch v3.2/v3.3 字段名)
  // --based-on-cards 模式下 cards 没 entryId 字段, 这里只取 args.entryIds 路径的 entryIds
  const entryIds = extractEntryIds(entryIdsData);
  // entryIds 在 --based-on-cards 路径是空, 是正常的 (cards 还没入库, 没 entryId)
  // entryIds 在 --entry-Ids 路径不能空 (v3.2/v3.3 ingest-batch 至少返一个 entryId)
  if (!cards && entryIds.length === 0) {
    out({
      ok: false,
      error: "no_entry_ids",
      message: "entryIds 为空 (请改用 --based-on-cards)",
      hint: "推荐姿势: opphub knowledge-match --based-on-cards /tmp/cards.json --json",
    }, wantJson);
    process.exit(1);
  }

  const name = args.name || "(未指定)";
  const minScore = args.minScore ? parseFloat(args.minScore) : 0.5;
  const limit = args.limit ? parseInt(args.limit, 10) : 3;

  // 反推 query (来自 cards 直接派生, 干掉了 v3.2 写死的 UPSTREAM_QUERIES 等)
  // 没 cards 时 (只传 --entry-ids 老姿势) → 退化为空 query, 命中 0, 提示用户改 --based-on-cards
  const queries = cards
    ? deriveQueriesFromCards(cards)
    : { upstream: [], downstream: [], peer: [] };

  const t0 = Date.now();

  const upstreamResults = [];
  for (const q of queries.upstream) {
    const r = searchOpc(q, limit, minScore);
    if (r.ok && r.results && r.results.length > 0) {
      upstreamResults.push({ query: q, results: r.results.slice(0, limit) });
    }
  }

  const downstreamResults = [];
  for (const q of queries.downstream) {
    const r = searchOpc(q, limit, minScore);
    if (r.ok && r.results && r.results.length > 0) {
      downstreamResults.push({ query: q, results: r.results.slice(0, limit) });
    }
  }

  const peerResults = [];
  for (const q of queries.peer) {
    const r = searchOpc(q, limit, minScore);
    if (r.ok && r.results && r.results.length > 0) {
      peerResults.push({ query: q, results: r.results.slice(0, limit) });
    }
  }

  // 启发式: 召回结果去重 entryId, 不同 entry 数 < 5 视为不足
  // 精确判断需 server 端 API 查 user 总数, v3.3 schema 红线 (等 server 接)
  const allHits = [
    ...upstreamResults.flatMap((r) => r.results),
    ...downstreamResults.flatMap((r) => r.results),
    ...peerResults.flatMap((r) => r.results),
  ];
  const uniqueEntries = new Set(allHits.map((r) => r.entryId));
  const insufficient = uniqueEntries.size < 5;
  const totalHits = allHits.length;

  const result = {
    ok: true,
    name,
    inputMode: cards && entryIds.length > 0 ? "based-on-cards+entry-ids" : (cards ? "based-on-cards" : "entry-ids"),
    cardCount: cards ? cards.length : 0,
    entryCount: entryIds.length,
    queryPlan: queries,
    upstream: upstreamResults,
    downstream: downstreamResults,
    peer: peerResults,
    uniqueHitEntries: uniqueEntries.size,
    upstreamHitCount: upstreamResults.reduce((a, b) => a + b.results.length, 0),
    downstreamHitCount: downstreamResults.reduce((a, b) => a + b.results.length, 0),
    peerHitCount: peerResults.reduce((a, b) => a + b.results.length, 0),
    insufficient,
    warning: cards
      ? null
      : "用了 --entry-ids 老姿势, query 为空 (请改用 --based-on-cards 拿 query 命中)",
    message: insufficient
      ? `知识库匹配有限 (${uniqueEntries.size} 个唯一 entry 命中, < 5), 建议邀请更多 OPC 录入后再跑匹配`
      : "匹配完成",
    nextStep: insufficient
      ? "邀请更多 OPC 录入后再跑匹配"
      : (totalHits === 0 ? "知识库暂无相关 OPC, 录入更多 OPC 后再跑" : "匹配完成, 可去 server 端 /admin 查撮合详情"),
    durationMs: Date.now() - t0,
  };

  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`📊 ${name} · 匹配结果 (输入姿势: ${result.inputMode})\n`);
    console.log(`cards: ${result.cardCount} 条, entryIds: ${result.entryCount} 条`);
    console.log(`query 计划: upstream=${queries.upstream.length}, downstream=${queries.downstream.length}, peer=${queries.peer.length}`);
    if (queries.upstream.length > 0) console.log(`  upstream queries: ${queries.upstream.join(", ")}`);
    if (queries.downstream.length > 0) console.log(`  downstream queries: ${queries.downstream.join(", ")}`);
    if (queries.peer.length > 0) console.log(`  peer queries: ${queries.peer.join(", ")}`);
    console.log();
    if (insufficient) console.log(`💡 ${result.message}\n`);

    if (upstreamResults.length > 0) {
      console.log(`【上游命中】(你需要, opphub 里有)`);
      for (const r of upstreamResults) {
        console.log(`  🎯 ${r.query}`);
        for (const hit of r.results.slice(0, 2)) {
          console.log(`     [${hit.score?.toFixed(3) ?? "?"}] ${hit.text?.slice(0, 60)}...`);
        }
      }
    } else {
      console.log(`【上游命中】(无)`);
    }

    if (downstreamResults.length > 0) {
      console.log(`【下游命中】(你能提供, opphub 里有)`);
      for (const r of downstreamResults) {
        console.log(`  🎯 ${r.query}`);
        for (const hit of r.results.slice(0, 2)) {
          console.log(`     [${hit.score?.toFixed(3) ?? "?"}] ${hit.text?.slice(0, 60)}...`);
        }
      }
    } else {
      console.log(`【下游命中】(无)`);
    }

    if (peerResults.length > 0) {
      console.log(`【同业关联】(能力重叠)`);
      for (const r of peerResults) {
        console.log(`  ⚠️ ${r.query}`);
        for (const hit of r.results.slice(0, 2)) {
          console.log(`     [${hit.score?.toFixed(3) ?? "?"}] ${hit.text?.slice(0, 60)}...`);
        }
      }
    } else {
      console.log(`【同业关联】(无)`);
    }

    console.log(`\n下一步: ${result.nextStep}`);
  }
}

main().catch((e) => {
  console.error("opphub-knowledge-match fatal:", e?.message ?? e);
  process.exit(1);
});
