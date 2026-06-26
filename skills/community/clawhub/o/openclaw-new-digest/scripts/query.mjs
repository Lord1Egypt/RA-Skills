#!/usr/bin/env node

import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import {
  readJSON,
  todayStr,
  pushPath,
  pushDir,
  feedbackPath,
  feedbackDir,
  listDates,
  getDataDir,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: query.mjs <command> [options]

Commands:
  pushes    View push records
  feedback  View feedback records
  search    Search across pushes by keyword

Options:
  --date <YYYY-MM-DD>   Target date (default: today)
  --slot <slot>         Filter by slot: morning, noon, evening
  --days <n>            Look back n days (default: 1, for search default: 7)
  --keyword <kw>        Keyword to search for (search command only)

Examples:
  node query.mjs pushes --date 2026-03-06 --slot morning
  node query.mjs pushes --days 3
  node query.mjs feedback --date 2026-03-06
  node query.mjs feedback --days 3
  node query.mjs search --keyword "bitcoin" --days 7`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const command = args[0];
let date = null;
let slot = null;
let days = null;
let keyword = null;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "--date") { date = args[++i]; continue; }
  if (a === "--slot") { slot = args[++i]; continue; }
  if (a === "--days") { days = Number.parseInt(args[++i] ?? "1", 10); continue; }
  if (a === "--keyword") { keyword = args[++i]; continue; }
  if (a.startsWith("-")) {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
}

const SLOTS = ["morning", "noon", "evening"];

function dateRange(numDays) {
  const dates = [];
  const now = new Date();
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

function resolveDates() {
  if (date) return [date];
  const n = days ?? 1;
  return dateRange(n);
}

function printPush(record) {
  if (!record) return;
  console.log(`### ${record.id} — ${record.topic} (${record.slot})`);
  console.log(`- **Time**: ${record.push_time}`);
  console.log(`- **Items**: ${record.item_count ?? record.items?.length ?? 0}`);
  if (record.keywords?.length) {
    console.log(`- **Keywords**: ${record.keywords.join(", ")}`);
  }
  console.log();
  for (const item of record.items ?? []) {
    console.log(
      `  ${item.id}. [${item.category || item.source}] **${item.title}**`
    );
    if (item.summary) {
      console.log(`  ${item.summary.slice(0, 200)}${item.summary.length > 200 ? "..." : ""}`);
    }
    if (item.url) {
      console.log(`  ${item.url}`);
    }
    console.log();
  }
  console.log("---\n");
}

function printFeedback(record, dateLabel) {
  if (!record || !record.feedbacks?.length) return;
  console.log(`### Feedback for ${record.push_id}`);
  for (const fb of record.feedbacks) {
    const itemTag = fb.item_id ? ` [${fb.item_id}]` : "";
    console.log(`- ${fb.created_at}${itemTag}: ${fb.text}`);
  }
  console.log();
}

if (command === "pushes") {
  const dates = resolveDates();
  const slots = slot ? [slot] : SLOTS;
  let found = false;

  console.log(`## Push Records\n`);
  for (const d of dates) {
    for (const s of slots) {
      const record = readJSON(pushPath(d, s));
      if (record) {
        printPush(record);
        found = true;
      }
    }
  }
  if (!found) {
    console.log("No push records found for the specified criteria.");
  }
} else if (command === "feedback") {
  const defaultDays = days ?? (date ? 1 : 3);
  const dates = date ? [date] : dateRange(defaultDays);
  const slots = slot ? [slot] : SLOTS;
  let found = false;

  console.log(`## Feedback Records\n`);
  for (const d of dates) {
    for (const s of slots) {
      const record = readJSON(feedbackPath(d, s));
      if (record && record.feedbacks?.length) {
        printFeedback(record, d);
        found = true;
      }
    }
  }
  if (!found) {
    console.log("No feedback found for the specified criteria.");
  }
} else if (command === "search") {
  if (!keyword) {
    console.error("Error: --keyword is required for search.");
    process.exit(1);
  }

  const searchDays = days ?? 7;
  const dates = dateRange(searchDays);
  const kw = keyword.toLowerCase();
  let matchCount = 0;

  console.log(`## Search Results for "${keyword}" (last ${searchDays} days)\n`);

  for (const d of dates) {
    for (const s of SLOTS) {
      const record = readJSON(pushPath(d, s));
      if (!record) continue;

      const matchingItems = (record.items ?? []).filter((item) => {
        const haystack = [
          item.title,
          item.summary,
          item.category,
          item.author,
          item.raw_excerpt,
        ]
          .join(" ")
          .toLowerCase();
        return haystack.includes(kw);
      });

      if (matchingItems.length > 0) {
        console.log(`### ${d} / ${s} (${record.topic})\n`);
        for (const item of matchingItems) {
          console.log(
            `- [${item.category || item.source}] **${item.title}**`
          );
          if (item.summary) {
            console.log(`  ${item.summary.slice(0, 200)}...`);
          }
          if (item.url) console.log(`  ${item.url}`);
          console.log();
          matchCount++;
        }
      }
    }
  }

  if (matchCount === 0) {
    console.log(`No items matching "${keyword}" found.`);
  } else {
    console.log(`---\n\nTotal: ${matchCount} matching items.`);
  }
} else {
  console.error(`Unknown command: ${command}`);
  usage();
}
