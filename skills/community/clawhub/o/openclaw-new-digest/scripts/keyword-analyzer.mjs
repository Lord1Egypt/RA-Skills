#!/usr/bin/env node

/**
 * Keyword Analyzer
 * Analyzes recent push results to extract content for AI analysis.
 * Helps identify potential new keywords based on what content has been captured.
 *
 * Usage:
 *   node keyword-analyzer.mjs --slot morning --days 7
 *   node keyword-analyzer.mjs --date 2026-03-06 --slot morning
 */

import {
  readJSON,
  pushPath,
  listDates,
  loadConfig,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: keyword-analyzer.mjs [options]

Options:
  --slot <slot>     Slot name: morning, noon, evening (required)
  --date <date>     Target date (YYYY-MM-DD), defaults to today
  --days <n>        Look back n days (default: 7)

Examples:
  node keyword-analyzer.mjs --slot morning --days 7
  node keyword-analyzer.mjs --date 2026-03-06 --slot morning
`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let slot = null;
let date = null;
let days = 7;

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--slot") {
    slot = args[++i];
    continue;
  }
  if (a === "--date") {
    date = args[++i];
    continue;
  }
  if (a === "--days") {
    days = Number.parseInt(args[++i] ?? "7", 10);
    continue;
  }
  if (a.startsWith("-")) {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
}

if (!slot) {
  console.error("Error: --slot is required.");
  usage();
}

// Load current config to get existing keywords
const config = loadConfig();
const slotConfig = config?.slots?.find((s) => s.name === slot);
const currentKeywords = slotConfig?.keywords ?? [];

function dateRange(numDays, targetDate = null) {
  const dates = [];
  const now = targetDate ? new Date(targetDate) : new Date();
  for (let i = 0; i < numDays; i++) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    dates.push(`${y}-${m}-${day}`);
  }
  return dates;
}

function analyzeContent(records) {
  const allItems = [];

  for (const record of records) {
    if (!record?.items) continue;

    for (const item of record.items) {
      allItems.push({
        date: record.date,
        slot: record.slot,
        source: item.category || item.source || "unknown",
        title: item.title || "",
        summary: item.summary || "",
        url: item.url || "",
        // Extract meaningful text content
        content: [
          item.title,
          item.summary,
          item.raw_excerpt,
          item.category,
          item.author,
        ]
          .filter(Boolean)
          .join(" | "),
      });
    }
  }

  return allItems;
}

function extractTopics(items) {
  // Simple keyword/topic extraction based on content
  const topics = new Map();

  for (const item of items) {
    const text = (item.title + " " + (item.summary || "")).toLowerCase();

    // Common tech/finance keywords to look for
    const patterns = [
      /\b(ai|artificial intelligence|machine learning|llm|large language model|gpt|claude|openai|anthropic)\b/gi,
      /\b(crypto|bitcoin|btc|ethereum|eth|defi|blockchain|web3|nft)\b/gi,
      /\b(stock|market|trading|invest|finance|economy|fed|interest rate)\b/gi,
      /\b(tech|technology|software|startup|venture|funding)\b/gi,
      /\b(agent|agentic|auto gpt|autonomous|automation)\b/gi,
    ];

    for (const pattern of patterns) {
      const matches = text.match(pattern);
      if (matches) {
        for (const match of matches) {
          const kw = match.toLowerCase();
          const count = topics.get(kw) || { count: 0, sources: new Set(), dates: new Set() };
          count.count++;
          count.sources.add(item.source);
          count.dates.add(item.date);
          topics.set(kw, count);
        }
      }
    }
  }

  // Convert to sorted array
  const sorted = Array.from(topics.entries())
    .map(([keyword, data]) => ({
      keyword,
      count: data.count,
      sources: Array.from(data.sources),
      dates: Array.from(data.dates),
    }))
    .sort((a, b) => b.count - a.count);

  return sorted;
}

// Main execution
const dates = date ? [date] : dateRange(days);
const records = [];

console.log(`## Keyword Analysis for "${slot}"\n`);
console.log(`Date range: ${dates[dates.length - 1]} to ${dates[0]}`);
console.log(`Current keywords: ${currentKeywords.join(", ") || "(none)"}\n`);

// Collect push records
for (const d of dates) {
  const path = pushPath(d, slot);
  const record = readJSON(path);
  if (record) {
    records.push({ ...record, date: d, slot });
  }
}

if (records.length === 0) {
  console.log("No push records found for the specified criteria.");
  process.exit(0);
}

console.log(`Found ${records.length} push records.\n`);

// Analyze content
const allItems = analyzeContent(records);

console.log(`Total items analyzed: ${allItems.length}\n`);

// Output structured data for AI consumption
const output = {
  meta: {
    slot,
    date_range: { start: dates[dates.length - 1], end: dates[0] },
    current_keywords: currentKeywords,
    push_count: records.length,
    total_items: allItems.length,
  },
  // Top items by source for AI to review
  sample_items: allItems.slice(0, 50).map((item) => ({
    date: item.date,
    source: item.source,
    title: item.title,
    summary: item.summary?.slice(0, 200),
    url: item.url,
  })),
  // All items for deeper analysis
  all_items: allItems.map((item) => ({
    date: item.date,
    source: item.source,
    content: item.content,
  })),
};

console.log("### Structured Output (for AI analysis)\n");
console.log(JSON.stringify(output, null, 2));
