#!/usr/bin/env node

import {
  readJSON,
  writeJSON,
  todayStr,
  currentMonth,
  usagePath,
} from "./lib/storage.mjs";

const API_KEYS = ["tavily_search", "tavily_extract", "hackernews", "xpoz"];

function usage() {
  console.error(
    `Usage: track-usage.mjs <command> [options]

Commands:
  record   Record API usage for a push slot
  today    Show today's usage
  monthly  Show current month's total usage
  forecast Predict end-of-month usage based on daily average

Record options:
  --slot <slot>              Push slot (required for record)
  --tavily-search <n>        Tavily Search API calls
  --tavily-extract <n>       Tavily Extract API calls
  --hackernews <n>           Hacker News API calls
  --xpoz <n>                 Xpoz MCP calls

Examples:
  node track-usage.mjs record --slot morning --tavily-search 3 --tavily-extract 2 --hackernews 1 --xpoz 2
  node track-usage.mjs today
  node track-usage.mjs monthly
  node track-usage.mjs forecast`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const command = args[0];

function parseRecordArgs() {
  let slot = null;
  const counts = { tavily_search: 0, tavily_extract: 0, hackernews: 0, xpoz: 0 };

  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    if (a === "--slot") { slot = args[++i]; continue; }
    if (a === "--tavily-search") { counts.tavily_search = Number.parseInt(args[++i] ?? "0", 10); continue; }
    if (a === "--tavily-extract") { counts.tavily_extract = Number.parseInt(args[++i] ?? "0", 10); continue; }
    if (a === "--hackernews") { counts.hackernews = Number.parseInt(args[++i] ?? "0", 10); continue; }
    if (a === "--xpoz") { counts.xpoz = Number.parseInt(args[++i] ?? "0", 10); continue; }
    console.error(`Unknown arg: ${a}`);
    usage();
  }

  if (!slot || !["morning", "noon", "evening"].includes(slot)) {
    console.error(`Error: --slot is required (morning|noon|evening). Got: "${slot}"`);
    process.exit(1);
  }

  return { slot, counts };
}

function loadMonth(ym) {
  const file = usagePath(ym);
  return readJSON(file) ?? { month: ym, daily: {}, totals: {} };
}

function saveMonth(data) {
  writeJSON(usagePath(data.month), data);
}

function addToTotals(totals, counts) {
  for (const key of API_KEYS) {
    totals[key] = (totals[key] ?? 0) + (counts[key] ?? 0);
  }
}

function zeroUsage() {
  return Object.fromEntries(API_KEYS.map((k) => [k, 0]));
}

function daysInMonth(ym) {
  const [y, m] = ym.split("-").map(Number);
  return new Date(y, m, 0).getDate();
}

function dayOfMonth() {
  return new Date().getDate();
}

if (command === "record") {
  const { slot, counts } = parseRecordArgs();
  const ym = currentMonth();
  const today = todayStr();
  const data = loadMonth(ym);

  if (!data.daily[today]) data.daily[today] = {};
  const existing = data.daily[today][slot] ?? zeroUsage();
  for (const key of API_KEYS) {
    existing[key] = (existing[key] ?? 0) + (counts[key] ?? 0);
  }
  data.daily[today][slot] = existing;

  data.totals = {};
  for (const day of Object.values(data.daily)) {
    for (const slotData of Object.values(day)) {
      if (slotData) addToTotals(data.totals, slotData);
    }
  }

  saveMonth(data);

  console.log("## Usage Recorded\n");
  console.log(`- **Date**: ${today}`);
  console.log(`- **Slot**: ${slot}`);
  for (const key of API_KEYS) {
    if (counts[key] > 0) console.log(`- **${key}**: +${counts[key]}`);
  }
  console.log(`- **Path**: ${usagePath(ym)}`);

} else if (command === "today") {
  const ym = currentMonth();
  const today = todayStr();
  const data = loadMonth(ym);
  const dayData = data.daily[today];

  console.log(`## API Usage — ${today}\n`);

  if (!dayData || Object.keys(dayData).length === 0) {
    console.log("No usage recorded today.");
  } else {
    console.log("| Slot | Tavily Search | Tavily Extract | HN | Xpoz |");
    console.log("|------|--------------|---------------|-----|------|");
    const dayTotals = zeroUsage();
    for (const slot of ["morning", "noon", "evening"]) {
      const s = dayData[slot];
      if (s) {
        console.log(`| ${slot} | ${s.tavily_search ?? 0} | ${s.tavily_extract ?? 0} | ${s.hackernews ?? 0} | ${s.xpoz ?? 0} |`);
        addToTotals(dayTotals, s);
      } else {
        console.log(`| ${slot} | - | - | - | - |`);
      }
    }
    console.log(`| **Total** | **${dayTotals.tavily_search}** | **${dayTotals.tavily_extract}** | **${dayTotals.hackernews}** | **${dayTotals.xpoz}** |`);
  }

} else if (command === "monthly") {
  const ym = currentMonth();
  const data = loadMonth(ym);
  const t = data.totals ?? {};
  const activeDays = Object.keys(data.daily).length;

  console.log(`## API Monthly Usage — ${ym}\n`);
  console.log(`Active days: ${activeDays}\n`);
  console.log("| API | Total |");
  console.log("|-----|-------|");
  for (const key of API_KEYS) {
    console.log(`| ${key} | ${t[key] ?? 0} |`);
  }

} else if (command === "forecast") {
  const ym = currentMonth();
  const data = loadMonth(ym);
  const t = data.totals ?? {};
  const activeDays = Object.keys(data.daily).length;
  const totalDays = daysInMonth(ym);
  const currentDay = dayOfMonth();
  const remainingDays = totalDays - currentDay;

  console.log(`## API 月度用量预测 (${ym})\n`);

  if (activeDays === 0) {
    console.log("No usage data yet this month. Run some pushes first.");
  } else {
    console.log(`统计天数: ${activeDays} | 本月总天数: ${totalDays} | 剩余: ${remainingDays}\n`);
    console.log("| API | 本月已用 | 日均 | 预计月末 |");
    console.log("|-----|---------|------|---------|");
    for (const key of API_KEYS) {
      const used = t[key] ?? 0;
      const avg = activeDays > 0 ? (used / activeDays).toFixed(1) : "0";
      const projected = activeDays > 0 ? Math.round((used / activeDays) * totalDays) : 0;
      console.log(`| ${key} | ${used} | ${avg} | ~${projected} |`);
    }
  }

} else {
  console.error(`Unknown command: ${command}`);
  usage();
}
