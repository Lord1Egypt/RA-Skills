#!/usr/bin/env node

import fs from "fs";
import path from "path";

function usage() {
  console.error(`Usage: crawl.mjs "url" [options]

Options:
  --depth <n>              Crawl depth (1-5, default: 1)
  --breadth <n>            Links per page (default: 20)
  --limit <n>              Total pages cap (default: 50)
  --output <dir>           Save pages to directory
  --instructions <text>    Natural language guidance
  --chunks <n>             Chunks per page (1-5, requires instructions)
  --depth-mode <mode>      Extract depth: basic or advanced (default: basic)
  --select <pattern>       Regex pattern to include
  --exclude <pattern>      Regex pattern to exclude
  --timeout <sec>          Max wait time (10-150 seconds, default: 150)
  --json                   Output raw JSON

Examples:
  crawl.mjs "https://docs.example.com"
  crawl.mjs "https://docs.example.com" --depth 2 --limit 50
  crawl.mjs "https://docs.example.com" --depth 2 --output ./docs
  crawl.mjs "https://example.com" --instructions "Find API docs" --chunks 3`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const url = args[0];
let maxDepth = 1;
let maxBreadth = 20;
let limit = 50;
let outputDir = null;
let instructions = null;
let chunksPerSource = null;
let extractDepth = "basic";
let selectPaths = null;
let excludePaths = null;
let timeout = 150;
let outputJson = false;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "--depth") {
    maxDepth = Number.parseInt(args[i + 1] ?? "1", 10);
    i++;
    continue;
  }
  if (a === "--breadth") {
    maxBreadth = Number.parseInt(args[i + 1] ?? "20", 10);
    i++;
    continue;
  }
  if (a === "--limit") {
    limit = Number.parseInt(args[i + 1] ?? "50", 10);
    i++;
    continue;
  }
  if (a === "--output") {
    outputDir = args[i + 1];
    i++;
    continue;
  }
  if (a === "--instructions") {
    instructions = args[i + 1];
    i++;
    continue;
  }
  if (a === "--chunks") {
    chunksPerSource = Number.parseInt(args[i + 1], 10);
    i++;
    continue;
  }
  if (a === "--depth-mode") {
    extractDepth = args[i + 1] ?? "basic";
    i++;
    continue;
  }
  if (a === "--select") {
    selectPaths = args[i + 1];
    i++;
    continue;
  }
  if (a === "--exclude") {
    excludePaths = args[i + 1];
    i++;
    continue;
  }
  if (a === "--timeout") {
    timeout = Number.parseFloat(args[i + 1] ?? "150", 10);
    i++;
    continue;
  }
  if (a === "--json") {
    outputJson = true;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Error: TAVILY_API_KEY not set");
  console.error("Get your API key at https://tavily.com");
  process.exit(1);
}

const body = {
  url: url,
  max_depth: maxDepth,
  max_breadth: maxBreadth,
  limit: limit,
  extract_depth: extractDepth,
};

if (instructions) body.instructions = instructions;
if (instructions && chunksPerSource) body.chunks_per_source = chunksPerSource;
if (selectPaths) body.select_paths = [selectPaths];
if (excludePaths) body.exclude_paths = [excludePaths];
if (timeout) body.timeout = timeout;

console.error(`Crawling ${url} (depth: ${maxDepth}, limit: ${limit})...`);

const resp = await fetch("https://api.tavily.com/crawl", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${apiKey}`,
  },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Tavily Crawl failed (${resp.status}): ${text}`);
}

const data = await resp.json();

if (outputJson) {
  console.log(JSON.stringify(data, null, 2));
  process.exit(0);
}

// Print results
const results = data.results ?? [];
console.error(`\nCrawled ${results.length} pages\n`);

if (outputDir) {
  // Save to files
  fs.mkdirSync(outputDir, { recursive: true });

  for (const r of results) {
    const pageUrl = String(r?.url ?? "").trim();
    const content = String(r?.raw_content ?? "").trim();

    if (!pageUrl) continue;

    // Generate filename from URL
    const urlObj = new URL(pageUrl);
    let filename = urlObj.pathname.replace(/[^a-zA-Z0-9_-]/g, "_") || "index";
    filename = filename.replace(/^_+|_+$/g, "");
    filename = filename || "index";
    filename += ".md";

    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, content, "utf-8");
    console.error(`Saved: ${filepath}`);
  }

  console.error(`\nAll pages saved to ${outputDir}/`);
} else {
  // Print to stdout
  console.log(`## Crawl Results (${results.length} pages)\n`);

  for (const r of results) {
    const pageUrl = String(r?.url ?? "").trim();
    const content = String(r?.raw_content ?? "").trim();

    if (!pageUrl) continue;

    console.log(`### ${pageUrl}\n`);
    if (content) {
      console.log(content);
    }
    console.log("\n---\n");
  }
}

if (data.response_time) {
  console.error(`\nResponse time: ${data.response_time}s`);
}