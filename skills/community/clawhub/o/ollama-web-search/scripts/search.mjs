#!/usr/bin/env node

function usage() {
  console.error(`Usage: search.mjs "query" [-n 5] [--max-results 5]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let n = 5;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "-n" || a === "--max-results") {
    n = Number.parseInt(args[i + 1] ?? "5", 10);
    i++;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.OLLAMA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing OLLAMA_API_KEY");
  process.exit(1);
}

const body = {
  query,
  max_results: Math.max(1, Math.min(n, 10)),
};

const resp = await fetch("https://ollama.com/api/web_search", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Ollama web_search failed (${resp.status}): ${text}`);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
