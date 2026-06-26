#!/usr/bin/env node

import fs from "node:fs";
import process from "node:process";

function printHelp() {
  console.log(`Usage:
  node scripts/render-formal-review-template.mjs --in FILE [--out FILE] [--per-category]

Render a flexible academic-review scaffold from structured paper records.
Expected input: a JSON array of paper records or an object with a "papers" array.
`);
}

function parseArgs(argv) {
  let inputFile = "";
  let outFile = "";
  let perCategory = false;

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help") {
      printHelp();
      process.exit(0);
    }
    if (arg === "--in") {
      inputFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--out") {
      outFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--per-category") {
      perCategory = true;
    }
  }

  if (!inputFile) {
    printHelp();
    process.exit(1);
  }

  return { inputFile, outFile, perCategory };
}

function readRecords(inputFile) {
  const raw = fs.readFileSync(inputFile, "utf8");
  const parsed = JSON.parse(raw);
  if (Array.isArray(parsed)) {
    return parsed;
  }
  if (Array.isArray(parsed.papers)) {
    return parsed.papers;
  }
  throw new Error("Input JSON must be an array or an object with a papers array.");
}

function groupByCategory(records) {
  const grouped = new Map();
  for (const record of records) {
    const category = record.category || "Uncategorized";
    if (!grouped.has(category)) {
      grouped.set(category, []);
    }
    grouped.get(category).push(record);
  }
  return grouped;
}

function renderClassificationTable(records) {
  const lines = [];
  lines.push("## 分类表");
  lines.push("| 论文 | 年份 | 分类 | 分类理由 | 依据 |");
  lines.push("| --- | --- | --- | --- | --- |");
  for (const record of records) {
    lines.push(`| ${record.title || "Untitled"} | ${record.year || ""} | ${record.category || "Uncategorized"} | ${record.classification_rationale || record.rationale || ""} | ${(record.evidence || record.extraction_notes || []).join("；")} |`);
  }
  lines.push("");
  return lines;
}

function renderReviewSkeleton(title) {
  return [
    `# ${title}`,
    "",
    "## 摘要",
    "",
    "## 关键词",
    "关键词1；关键词2；关键词3",
    "",
    "## 引言",
    "",
    "## 主体部分",
    "### 研究现状与问题脉络",
    "",
    "### 代表性方法、理论与成果",
    "",
    "### 共同点、分歧与不足",
    "",
    "## 讨论与结论",
    "",
    "## 未来方向",
    "",
    "## 参考文献",
    "[1] ",
    "",
  ];
}

function renderIntegratedReview(records) {
  const lines = [];
  lines.push("# Corpus Summary");
  lines.push(`- Total papers: ${records.length}`);
  lines.push(`- Categories: ${groupByCategory(records).size}`);
  lines.push("");
  lines.push(...renderClassificationTable(records));
  lines.push(...renderReviewSkeleton("基于给定文献语料的综述"));
  return `${lines.join("\n")}\n`;
}

function renderPerCategoryReviews(records) {
  const lines = [];
  const grouped = groupByCategory(records);
  lines.push("# Corpus Summary");
  lines.push(`- Total papers: ${records.length}`);
  lines.push(`- Categories: ${grouped.size}`);
  lines.push("");
  lines.push(...renderClassificationTable(records));

  for (const [category, items] of grouped.entries()) {
    lines.push(...renderReviewSkeleton(`${category}研究综述`));
    lines.push("### 附：本类论文");
    for (const item of items) {
      lines.push(`- ${item.title || "Untitled"}${item.year ? ` (${item.year})` : ""}`);
    }
    lines.push("");
  }

  return `${lines.join("\n")}\n`;
}

function main() {
  const { inputFile, outFile, perCategory } = parseArgs(process.argv.slice(2));
  const records = readRecords(inputFile);
  const markdown = perCategory ? renderPerCategoryReviews(records) : renderIntegratedReview(records);

  if (outFile) {
    fs.writeFileSync(outFile, markdown, "utf8");
  } else {
    process.stdout.write(markdown);
  }
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
