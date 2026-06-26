#!/usr/bin/env node

import { readFileSync } from "node:fs";
import {
  readJSON,
  writeJSON,
  todayStr,
  nowISO,
  pushPath,
  currentMonth,
  usagePath,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: store-push.mjs [--slot morning|noon|evening] [--input file.json]

Reads push data from stdin (default) or a file, then persists it.

The JSON input must have: slot, topic, items[].
If --slot is given, it overrides the slot in the JSON.

Example:
  echo '{"slot":"morning","topic":"finance","items":[...]}' | node store-push.mjs
  node store-push.mjs --slot morning --input push-data.json`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args[0] === "-h" || args[0] === "--help") usage();

let slotOverride = null;
let inputFile = null;

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--slot") {
    slotOverride = args[++i];
    continue;
  }
  if (a === "--input") {
    inputFile = args[++i];
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

let rawJSON;
if (inputFile) {
  rawJSON = readFileSync(inputFile, "utf-8");
} else {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  rawJSON = Buffer.concat(chunks).toString("utf-8");
}

if (!rawJSON.trim()) {
  console.error("Error: empty input. Provide JSON via stdin or --input.");
  process.exit(1);
}

let pushData;
try {
  pushData = JSON.parse(rawJSON);
} catch (e) {
  console.error(`Error: invalid JSON — ${e.message}`);
  process.exit(1);
}

const slot = slotOverride || pushData.slot;
if (!slot || !["morning", "noon", "evening"].includes(slot)) {
  console.error(
    `Error: slot must be one of: morning, noon, evening. Got: "${slot}"`
  );
  process.exit(1);
}

const today = todayStr();
const dateCompact = today.replace(/-/g, "");
const pushId = `push-${dateCompact}-${slot}`;

const items = (pushData.items ?? []).map((item, idx) => ({
  id: item.id || `item-${String(idx + 1).padStart(3, "0")}`,
  source: item.source ?? "unknown",
  category: item.category ?? "",
  title: item.title ?? "",
  url: item.url ?? "",
  author: item.author ?? "",
  influence_score: item.influence_score ?? 0,
  raw_excerpt: item.raw_excerpt ?? "",
  summary: item.summary ?? "",
  metadata: item.metadata ?? {},
}));

const usageData = pushData.usage ?? null;

const record = {
  id: pushId,
  slot,
  topic: pushData.topic ?? slot,
  keywords: pushData.keywords ?? [],
  push_time: nowISO(),
  items,
  item_count: items.length,
  usage: usageData,
  created_at: nowISO(),
};

const filePath = pushPath(today, slot);

const existing = readJSON(filePath);
if (existing) {
  record.created_at = existing.created_at;
  record.updated_at = nowISO();
}

writeJSON(filePath, record);

if (usageData) {
  const API_KEYS = ["tavily_search", "tavily_extract", "hackernews", "xpoz"];
  const ym = currentMonth();
  const monthFile = usagePath(ym);
  const monthData = readJSON(monthFile) ?? { month: ym, daily: {}, totals: {} };

  if (!monthData.daily[today]) monthData.daily[today] = {};
  const existing = monthData.daily[today][slot] ?? Object.fromEntries(API_KEYS.map((k) => [k, 0]));
  for (const key of API_KEYS) {
    existing[key] = (existing[key] ?? 0) + (usageData[key] ?? 0);
  }
  monthData.daily[today][slot] = existing;

  monthData.totals = {};
  for (const day of Object.values(monthData.daily)) {
    for (const slotData of Object.values(day)) {
      if (slotData) {
        for (const key of API_KEYS) {
          monthData.totals[key] = (monthData.totals[key] ?? 0) + (slotData[key] ?? 0);
        }
      }
    }
  }

  writeJSON(monthFile, monthData);
}

console.log(`## Push Stored\n`);
console.log(`- **ID**: ${pushId}`);
console.log(`- **Slot**: ${slot}`);
console.log(`- **Topic**: ${record.topic}`);
console.log(`- **Items**: ${items.length}`);
if (usageData) {
  const parts = Object.entries(usageData).filter(([, v]) => v > 0).map(([k, v]) => `${k} ×${v}`);
  if (parts.length > 0) console.log(`- **Usage**: ${parts.join(" | ")}`);
}
console.log(`- **Path**: ${filePath}`);
