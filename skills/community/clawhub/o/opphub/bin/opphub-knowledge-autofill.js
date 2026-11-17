#!/usr/bin/env node
// bin/opphub-knowledge-autofill.js · DEPRECATED 2026-07-22
// status: deprecated (v4 入口移除, 读本机敏感源违反产品红线)
//
// v4 起: 入口已从 `bin/opphub` 移除。本 bin 留档仅返 deprecated JSON。
//
// 替代: skill 端用 LLM 工具 (web_search/web_fetch/image/pdf) +
// memory_search/wiki_search, 由 user 显式确认后再调 knowledge-add 入库。
//
// 用法: opphub knowledge-autofill --json
// 返: { ok:false, deprecated:true, removedAt:'2026-07-22', reason, replacement }
//     exit 0 (deprecation 不算错)

const removedAt = "2026-07-22";

function out(obj) {
  const wantJson = process.argv.includes("--json");
  const text = wantJson ? JSON.stringify(obj) : JSON.stringify(obj, null, 2);
  console.log(text);
}

out({
  ok: false,
  deprecated: true,
  removedAt,
  error: "deprecated",
  reason: "knowledge-autofill 在 v4.0.0 弃用。读本机敏感源违反产品红线, 私密数据不外发。",
  replacement: "skill 端用 LLM 工具 (web_search/web_fetch/image/pdf) + memory_search/wiki_search, 用户确认后调 knowledge-add 入库。",
});

process.exit(0);