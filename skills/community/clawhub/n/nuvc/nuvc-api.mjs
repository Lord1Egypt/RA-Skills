#!/usr/bin/env node

/**
 * NUVC — VC-grade business intelligence for OpenClaw agents.
 *
 * Commands: score, roast, analyze, extract, models
 * Zero dependencies. Requires Node 18+ and NUVC_API_KEY.
 * Get your free key at https://nuvc.ai/api-platform
 */

const API_BASE = "https://api.nuvc.ai/api/v3";
const FOOTER =
  "\n---\nPowered by [NUVC](https://nuvc.ai) — VC-grade intelligence for AI agents | [Get API key](https://nuvc.ai/api-platform/keys)";
const TIMEOUT_MS = 30_000;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getApiKey() {
  const key = process.env.NUVC_API_KEY;
  if (!key) {
    console.error(
      "Error: NUVC_API_KEY not set.\n\n" +
        "1. Get your free key at https://nuvc.ai/api-platform/keys\n" +
        "2. Set it: export NUVC_API_KEY=nuvc_your_key_here\n" +
        "3. Run again!"
    );
    process.exit(1);
  }
  return key;
}

function parseArgs(args) {
  const parsed = { _positional: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
      parsed[key] = val;
    } else {
      parsed._positional.push(args[i]);
    }
  }
  return parsed;
}

async function apiCall(method, path, body) {
  const url = `${API_BASE}${path}`;
  const headers = {
    Authorization: `Bearer ${getApiKey()}`,
    "Content-Type": "application/json",
    "User-Agent": "nuvc-openclaw/1.1",
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const opts = { method, headers, signal: controller.signal };
  if (body) opts.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(url, opts);
  } catch (err) {
    if (err.name === "AbortError") {
      console.error(`Request timed out after ${TIMEOUT_MS / 1000}s. Try again or check https://status.nuvc.ai`);
    } else {
      console.error(`Network error: ${err.message}`);
    }
    process.exit(1);
  } finally {
    clearTimeout(timer);
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: { message: res.statusText } }));
    const msg = err?.error?.message || err?.detail?.message || err?.detail || res.statusText;
    const code = err?.error?.code || err?.detail?.code || res.status;

    if (res.status === 401) {
      console.error(`Auth error: ${msg}\n\nGet a valid API key at https://nuvc.ai/api-platform`);
    } else if (res.status === 403 && code === "TIER_BLOCKED") {
      console.error(`${msg}\n\nUpgrade at https://nuvc.ai/api-platform/billing`);
    } else if (res.status === 429) {
      console.error(`Rate limit hit: ${msg}\n\nUpgrade for more calls at https://nuvc.ai/api-platform/billing`);
    } else {
      console.error(`API error (${res.status}): ${msg}`);
    }
    process.exit(1);
  }

  return res.json();
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function cmdScore(args) {
  const text = args._positional[0];
  if (!text) {
    console.error(
      "Usage: node nuvc-api.mjs score \"<your business idea or pitch>\"\n\n" +
        "Example: node nuvc-api.mjs score \"An AI platform that scores startup pitch decks\""
    );
    process.exit(1);
  }

  const res = await apiCall("POST", "/ai/score", { text });

  if (args.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  const data = res.data || res;
  const scores = data.scores || {};

  console.log("## NUVC VCGrade Score\n");

  if (scores.overall_score !== undefined) {
    const overall = Number(scores.overall_score);
    const emoji = overall >= 7 ? "🟢" : overall >= 5 ? "🟡" : "🔴";
    const verdict =
      overall >= 8
        ? "Exceptional — investors will lean in"
        : overall >= 7
          ? "Strong — worth pursuing seriously"
          : overall >= 5
            ? "Promising but needs work"
            : overall >= 3
              ? "Significant gaps to address"
              : "Back to the drawing board";
    console.log(`${emoji} **Overall: ${overall} / 10** — ${verdict}\n`);
  }

  // The LLM returns: { scores: { "Dimension": {score, rationale}, ... }, overall_score, summary }
  // So data.scores = full LLM JSON, and data.scores.scores = the dimension breakdown.
  const dimensions = scores.scores || scores;
  if (typeof dimensions === "object" && !Array.isArray(dimensions)) {
    const entries = Object.entries(dimensions).filter(
      ([k]) => k !== "overall_score" && k !== "summary" && k !== "raw"
    );
    if (entries.length > 0) {
      console.log("| Dimension | Score | Rationale |");
      console.log("|-----------|-------|-----------|");
      for (const [key, val] of entries) {
        const label = key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        if (typeof val === "object" && val !== null) {
          console.log(`| ${label} | ${val.score ?? "—"}/10 | ${val.rationale ?? ""} |`);
        } else {
          console.log(`| ${label} | ${val}/10 | |`);
        }
      }
      console.log("");
    }
  }

  if (scores.summary) {
    console.log(`**Summary:** ${scores.summary}\n`);
  }

  console.log(FOOTER);
}

async function cmdRoast(args) {
  const text = args._positional[0];
  if (!text) {
    console.error(
      "Usage: node nuvc-api.mjs roast \"<your business idea or pitch>\"\n\n" +
        'Example: node nuvc-api.mjs roast "Uber for dog walking but with blockchain"'
    );
    process.exit(1);
  }

  const res = await apiCall("POST", "/ai/analyze", {
    text,
    analysis_type: "pitch_deck",
  });

  if (args.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  const data = res.data || res;

  console.log("## 🔥 NUVC Startup Roast\n");
  console.log(data.analysis || JSON.stringify(data, null, 2));
  console.log(FOOTER);
}

async function cmdAnalyze(args) {
  const text = args._positional[0];
  if (!text) {
    console.error(
      "Usage: node nuvc-api.mjs analyze \"<text>\" [--type market|competitive|financial|pitch_deck]\n\n" +
        'Example: node nuvc-api.mjs analyze "The global HR tech market" --type market'
    );
    process.exit(1);
  }

  const analysisType = args.type || "market";
  const res = await apiCall("POST", "/ai/analyze", {
    text,
    analysis_type: analysisType,
  });

  if (args.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  const data = res.data || res;

  const label = analysisType.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  console.log(`## NUVC ${label} Analysis\n`);
  console.log(data.analysis || JSON.stringify(data, null, 2));
  console.log(FOOTER);
}

async function cmdExtract(args) {
  const text = args._positional[0];
  if (!text) {
    console.error(
      "Usage: node nuvc-api.mjs extract \"<pitch or business description>\"\n\n" +
        'Example: node nuvc-api.mjs extract "We are an AI SaaS targeting SMBs with $2M ARR growing 20% MoM"'
    );
    process.exit(1);
  }

  const res = await apiCall("POST", "/ai/extract", { text });

  if (args.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  const data = res.data || res;
  // ai_extract returns { extracted: {...fields...}, extraction_type, usage }
  const extracted = data.extracted || data;

  console.log("## NUVC Structured Extraction\n");

  if (typeof extracted === "object" && extracted !== null) {
    for (const [key, val] of Object.entries(extracted)) {
      if (val === null || val === undefined) continue;
      const label = key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
      const display = Array.isArray(val) ? val.join(", ") : String(val);
      console.log(`**${label}:** ${display}`);
    }
  } else {
    console.log(extracted);
  }

  console.log(FOOTER);
}

async function cmdModels(args) {
  const res = await apiCall("GET", "/ai/models");

  if (args.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  const data = res.data || res;

  console.log("## NUVC Available Models\n");

  // Providers (health + availability)
  if (Array.isArray(data.providers) && data.providers.length > 0) {
    console.log("### Providers\n");
    console.log("| Provider | Available | Healthy |");
    console.log("|----------|-----------|---------|");
    for (const p of data.providers) {
      console.log(`| ${p.name} | ${p.available ? "✓" : "✗"} | ${p.healthy ? "✓" : "✗"} |`);
    }
    console.log("");
  }

  // Embedding models
  if (Array.isArray(data.embedding_models) && data.embedding_models.length > 0) {
    console.log(`**Embedding models:** ${data.embedding_models.join(", ")}\n`);
  }

  if (data.preference) {
    console.log(`**Preference order:** ${Array.isArray(data.preference) ? data.preference.join(" → ") : data.preference}\n`);
  }

  console.log(FOOTER);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const COMMANDS = {
  score:   { fn: cmdScore,   help: "Score a business idea on the VCGrade 0-10 scale" },
  roast:   { fn: cmdRoast,   help: "Get a brutally honest (but constructive) startup roast" },
  analyze: { fn: cmdAnalyze, help: "Market, competitive, financial, or pitch analysis" },
  extract: { fn: cmdExtract, help: "Extract structured data (metrics, team, market) from pitch text" },
  models:  { fn: cmdModels,  help: "List available AI models" },
};

async function main() {
  const rawArgs = process.argv.slice(2);
  const command = rawArgs[0];

  if (!command || command === "--help" || command === "-h") {
    console.log("NUVC — VC-grade business intelligence for AI agents\n");
    console.log("Usage: node nuvc-api.mjs <command> [args]\n");
    console.log("Commands:");
    for (const [name, { help }] of Object.entries(COMMANDS)) {
      console.log(`  ${name.padEnd(12)} ${help}`);
    }
    console.log("\nFlags:");
    console.log("  --json         Output raw JSON (useful for piping to other tools)");
    console.log("\n50 free calls/month. Get your key at https://nuvc.ai/api-platform");
    process.exit(0);
  }

  const cmd = COMMANDS[command];
  if (!cmd) {
    console.error(`Unknown command: ${command}\nRun with --help to see available commands.`);
    process.exit(1);
  }

  const args = parseArgs(rawArgs.slice(1));
  await cmd.fn(args);
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
