#!/usr/bin/env node
/* 一键用最新 report.html 重新生成 4 款中文样例 + 1 款英文外壳样例 PDF */
"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "assets", "report.html");
const OUTDIR = path.join(ROOT, "evals", "samples");
const MAKE = path.join(ROOT, "assets", "make-pdf.js");

/* 中文样例：仅切换 DATA.style（lang 保持默认 zh） */
const ZH_TARGETS = [
  { style: "a", name: "style-a-official" },
  { style: "b", name: "style-b-lab" },
  { style: "c", name: "style-c-modern" },
  { style: "d", name: "style-d-academic" }
];

/* 英文外壳样例：整段替换 DATA 为英文示例（lang="en"，A 款官方检验报告） */
const EN_NAME = "style-a-en";
const DATA_RE = /const DATA = \{[\s\S]*?\n\};/;
const EN_DATA = `
const DATA = {
  /* style: a=official b=lab c=modern d=academic */
  style: "a",
  /* lang: zh=Chinese shell en=English shell */
  lang: "en",
  publisher: "Tianjin Weishu Artificial Intelligence Technology Co., Ltd.",
  reportNo: "ontoAI-QC-20261011-002",
  date: "2026-10-11",
  product: "2026Q3 Product Launch Copy.docx",
  modality: "H1 Image+Text / W1 Word",
  scenario: "S2 Public Release",
  ruleLevel: "L1-L3, L7",
  basis: "ontoAI Quality Inspector SKILL.md v1.4.3 - Universal Dimensions D1-D6 - English Residue Rules RZE",
  verdict: { code:"modify", label:"Release After Revision", emoji:"🟡", note:"Publish after fixing the 2 must-fix items" },
  counts: { must:2, should:3, doubt:1, pass:7 },
  byDimension: [
    { dim:"Residue D1", must:1, should:2, doubt:0 },
    { dim:"Authenticity D2", must:1, should:0, doubt:1 },
    { dim:"Consistency D3", must:0, should:1, doubt:0 },
    { dim:"Completeness D4", must:0, should:0, doubt:0 },
    { dim:"Compliance D5", must:0, should:0, doubt:0 },
    { dim:"Adaptability D6", must:0, should:0, doubt:0 }
  ],
  must: [
    { no:1, loc:"Last paragraph, p.8", issue:"Trailing conversational tail", rule:"RZE-01",
      quote:"Let me know if you would like me to generate another version.",
      consequence:"Reader immediately recognizes AI output; overall credibility collapses",
      fix:"Delete the sentence" },
    { no:2, loc:"p.3, para 2", issue:"Unsourced statistical claim", rule:"D2.4",
      quote:"According to 2025 industry statistics, the market grew by 37%",
      consequence:"Cannot answer when challenged; factual error in a bid or publication",
      fix:"Add a real source (publisher + year + page), or delete and use qualitative wording" }
  ],
  should: [
    { no:1, loc:"p.2", issue:"Three rule-of-three triads in a row", rule:"RZE-11", advice:"Keep the three points, drop the triad shell" },
    { no:2, loc:"p.4", issue:"Two buzzwords: empower / closed-loop", rule:"RZE-07", advice:"Replace with concrete actions" },
    { no:3, loc:"Figure 3", issue:"Inconsistent with body wording", rule:"D3.7", advice:"Unify as year-over-year growth" }
  ],
  doubt: [
    { no:1, loc:"p.5", point:"Citation of an XX Industry White Paper",
      reason:"No such report found; cannot confirm whether it exists", action:"Treat as unusable" }
  ],
  passed: [
    { dim:"Residue", item:"No prompt leakage, no placeholders, no AI self-reference (except 1 above)" },
    { dim:"Authenticity", item:"All 23 figures cross-checked consistent (except 1 above)" },
    { dim:"Consistency", item:"Terms consistent; person/voice does not shift" },
    { dim:"Completeness", item:"All sections present; no truncation; captions complete" },
    { dim:"Compliance", item:"No superlatives, no key leakage, no private info" },
    { dim:"Adaptability", item:"Length fits public-account spec; image sizes compliant" },
    { dim:"Cross-modal", item:"All 5 figures match body description (anchor alignment 11/11)" }
  ],
  next: "Shall I apply the must-fix revisions? (Only these 2 items; the rest unchanged)"
};
`;

const html = fs.readFileSync(SRC, "utf8");

function buildAndPrint(name, bodyHtml) {
  const outHtml = path.join(OUTDIR, name + ".html");
  const outPdf = path.join(OUTDIR, name + ".pdf");
  fs.writeFileSync(outHtml, bodyHtml, "utf8");
  console.log("写入 HTML：" + outHtml);

  // 先删旧 PDF，避免轮询到旧文件造成“假成功”
  try { if (fs.existsSync(outPdf)) fs.unlinkSync(outPdf); }
  catch (e) { console.error("⚠️ 无法删除旧 PDF（可能被占用/正在打开）：" + outPdf + " —— " + e.code); }

  const r = spawnSync(process.argv[0], [MAKE, outHtml, outPdf], { stdio: "inherit" });
  if (r.status !== 0) {
    console.error("❌ 生成失败：" + name + " exit=" + r.status);
    process.exitCode = 1;
    return;
  }
  const okNew = fs.existsSync(outPdf) && (Date.now() - fs.statSync(outPdf).mtimeMs < 120000);
  console.log(okNew ? "✔ 已刷新 PDF：" + outPdf : "⚠️ PDF 未刷新（可能被占用）：" + outPdf);
}

/* —— 中文 4 款 —— */
for (const t of ZH_TARGETS) {
  const patched = html.replace(/(\n\s*style:\s*")a(",)/, `$1${t.style}$2`);
  if (t.style !== "a" && patched === html) {
    console.error("⚠️ 未能在源码中定位 DATA.style，跳过 " + t.name);
    continue;
  }
  buildAndPrint(t.name, patched);
}

/* —— 英文外壳 1 款 —— */
if (!DATA_RE.test(html)) {
  console.error("⚠️ 未能在源码中定位 const DATA 块，跳过 " + EN_NAME);
} else {
  const enHtml = html.replace(DATA_RE, EN_DATA);
  buildAndPrint(EN_NAME, enHtml);
}

console.log("全部完成。");
