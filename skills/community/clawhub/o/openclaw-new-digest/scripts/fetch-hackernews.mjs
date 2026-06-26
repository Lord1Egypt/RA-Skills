#!/usr/bin/env node

const HN_API = "https://hacker-news.firebaseio.com/v0";

function usage() {
  console.error(
    `Usage: fetch-hackernews.mjs ["query"] [-n 20] [--min-score 50] [--hours 24]

Arguments:
  "query"         Keywords to filter by (case-insensitive, OR-separated). Empty string = no filter.
  -n <count>      Max items to return (default: 20, fetches up to 200 candidates)
  --min-score <n> Minimum HN score threshold (default: 10)
  --hours <h>     Only include stories from the last h hours (default: 24)`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args[0] === "-h" || args[0] === "--help") usage();

let query = "";
let maxResults = 20;
let minScore = 10;
let hours = 24;

let positionalDone = false;
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") {
    maxResults = Number.parseInt(args[++i] ?? "20", 10);
    positionalDone = true;
    continue;
  }
  if (a === "--min-score") {
    minScore = Number.parseInt(args[++i] ?? "10", 10);
    positionalDone = true;
    continue;
  }
  if (a === "--hours") {
    hours = Number.parseInt(args[++i] ?? "24", 10);
    positionalDone = true;
    continue;
  }
  if (a.startsWith("-")) {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
  if (!positionalDone) {
    query = a;
    positionalDone = true;
  }
}

const cutoff = Math.floor(Date.now() / 1000) - hours * 3600;

const keywords = query
  .split(/\s+OR\s+/i)
  .map((k) => k.trim().toLowerCase())
  .filter(Boolean);

function matchesQuery(title) {
  if (keywords.length === 0) return true;
  const lower = title.toLowerCase();
  return keywords.some((kw) => lower.includes(kw));
}

async function fetchJSON(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HN API error: ${resp.status}`);
  return resp.json();
}

const topIds = await fetchJSON(`${HN_API}/topstories.json`);
const candidateIds = topIds.slice(0, 200);

const BATCH = 20;
const items = [];

for (let i = 0; i < candidateIds.length; i += BATCH) {
  const batch = candidateIds.slice(i, i + BATCH);
  const fetched = await Promise.all(
    batch.map((id) => fetchJSON(`${HN_API}/item/${id}.json`).catch(() => null))
  );

  for (const item of fetched) {
    if (!item || item.type !== "story" || item.dead || item.deleted) continue;
    if ((item.score ?? 0) < minScore) continue;
    if ((item.time ?? 0) < cutoff) continue;
    if (!matchesQuery(item.title ?? "")) continue;
    items.push(item);
  }

  if (items.length >= maxResults * 2) break;
}

items.sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
const selected = items.slice(0, maxResults);

if (selected.length === 0) {
  console.log(
    `## Hacker News Results\n\nNo stories found matching criteria (query="${query}", min_score=${minScore}, hours=${hours}).`
  );
  process.exit(0);
}

console.log(
  `## Hacker News Results (${selected.length} stories)\n`
);

for (const s of selected) {
  const title = s.title ?? "(untitled)";
  const url = s.url || `https://news.ycombinator.com/item?id=${s.id}`;
  const hnLink = `https://news.ycombinator.com/item?id=${s.id}`;
  const score = s.score ?? 0;
  const comments = s.descendants ?? 0;
  const age = new Date((s.time ?? 0) * 1000).toISOString();
  const by = s.by ?? "unknown";

  console.log(`- **${title}** (score: ${score}, comments: ${comments})`);
  console.log(`  By: ${by} | ${age}`);
  console.log(`  ${url}`);
  if (url !== hnLink) {
    console.log(`  HN: ${hnLink}`);
  }
  console.log();
}
