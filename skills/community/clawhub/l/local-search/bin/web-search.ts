#!/usr/bin/env tsx
/**
 * Local web-search CLI.
 *
 * Runs entirely on the user's machine; no cloud SDK is involved.
 *
 * Usage:
 *   tsx bin/web-search.ts <query> [options]
 *
 * Options:
 *   --num, -n <N>          Number of results (default: 10, max: 50)
 *   --engine, -e <id>      brave | duckduckgo | bing | google | auto  (default: auto)
 *   --recency-days, -r <N> Restrict to results from last N days
 *   --locale <BCP-47>      Result locale (default: auto-detect from query;
 *                          e.g. en-US, zh-CN, ja-JP, ko-KR, ru-RU)
 *   --timeout <ms>         Per-engine timeout in ms (default: 8000)
 *   --json                  Emit results as JSON (default: human-readable)
 *   --output, -o <path>     Write JSON to file instead of stdout
 *   --pretty                Pretty-print JSON (default when --json, no effect otherwise)
 *   --quiet, -q             Suppress engine-info banner; only print results
 *   --help, -h              Show help
 *
 * Examples:
 *   tsx bin/web-search.ts "artificial intelligence"
 *   tsx bin/web-search.ts "machine learning" --num 5 --engine duckduckgo
 *   tsx bin/web-search.ts "AI breakthroughs" --recency-days 7 --json -o ai_news.json
 */
import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { search, type SearchEngineId, type SearchOutcome } from "../src/index.js";

interface ParsedArgs {
  query: string;
  num: number;
  engine: SearchEngineId | "auto";
  recencyDays: number;
  locale: string;
  timeoutMs: number;
  json: boolean;
  pretty: boolean;
  output?: string;
  quiet: boolean;
  help: boolean;
}

function parseArgs(argv: string[]): ParsedArgs {
  const args = argv.slice(2);
  const out: ParsedArgs = {
    query: "",
    num: 10,
    engine: "auto",
    recencyDays: 0,
    locale: "",  // empty = auto-detect from query
    timeoutMs: 8000,
    json: false,
    pretty: true,
    quiet: false,
    help: false,
  };

  // Positional = query. We support both "quoted single arg" and
  // "multiple words until first --flag" so users don't have to quote.
  const positional: string[] = [];

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    switch (a) {
      case "-h":
      case "--help":
        out.help = true;
        break;
      case "--json":
        out.json = true;
        break;
      case "--pretty":
        out.pretty = true;
        break;
      case "-q":
      case "--quiet":
        out.quiet = true;
        break;
      case "-n":
      case "--num":
        out.num = parseInt(args[++i] ?? "", 10);
        if (Number.isNaN(out.num)) {
          throw new Error(`Invalid value for ${a}`);
        }
        break;
      case "-e":
      case "--engine": {
        const v = (args[++i] ?? "").toLowerCase();
        if (!["auto", "brave", "duckduckgo", "bing", "google"].includes(v)) {
          throw new Error(`Invalid engine: ${v}`);
        }
        out.engine = v as SearchEngineId | "auto";
        break;
      }
      case "-r":
      case "--recency-days":
        out.recencyDays = parseInt(args[++i] ?? "", 10);
        if (Number.isNaN(out.recencyDays)) {
          throw new Error(`Invalid value for ${a}`);
        }
        break;
      case "--locale":
        out.locale = args[++i] ?? "";
        if (out.locale && !/^[a-z]{2,3}-[A-Z]{2,3}$/i.test(out.locale)) {
          throw new Error(`Invalid locale "${out.locale}". Use BCP-47 like en-US, zh-CN, ja-JP, or leave empty for auto-detect.`);
        }
        break;
      case "--timeout":
        out.timeoutMs = parseInt(args[++i] ?? "", 10);
        if (Number.isNaN(out.timeoutMs)) {
          throw new Error(`Invalid value for ${a}`);
        }
        break;
      case "-o":
      case "--output":
        out.output = args[++i];
        if (!out.output) {
          throw new Error(`Missing path for ${a}`);
        }
        break;
      default:
        if (a.startsWith("--")) {
          throw new Error(`Unknown option: ${a}`);
        }
        positional.push(a);
        break;
    }
  }

  out.query = positional.join(" ").trim();
  return out;
}

const HELP = `local-search CLI — local web search with automatic engine fallback

Usage:
  tsx bin/web-search.ts <query> [options]

Options:
  --num, -n <N>          Number of results (default: 10, max: 50)
  --engine, -e <id>      brave | duckduckgo | bing | google | auto  (default: auto)
  --recency-days, -r <N> Restrict to results from last N days
  --locale <BCP-47>      Result locale (default: auto-detect from query;
                          e.g. en-US, zh-CN, ja-JP, ko-KR, ru-RU)
  --timeout <ms>         Per-engine timeout in ms (default: 8000)
  --json                  Emit JSON output (default: human-readable)
  --output, -o <path>     Write JSON to file instead of stdout
  --pretty                Pretty-print JSON (default on)
  --quiet, -q             Suppress engine-info banner
  --help, -h              Show this help

Examples:
  tsx bin/web-search.ts "artificial intelligence"
  tsx bin/web-search.ts "machine learning" --num 5 --engine duckduckgo
  tsx bin/web-search.ts "AI breakthroughs" --recency-days 7 --json -o ai_news.json
  tsx bin/web-search.ts "人工智能" --engine bing   (locale auto-detects zh-CN)
`;

function renderHuman(outcome: SearchOutcome & { success: true }, quiet: boolean): string {
  const lines: string[] = [];
  if (!quiet) {
    const engineLabel = outcome.engine === "auto" ? "auto (merged)" : outcome.engine;
    lines.push(`Engine: ${engineLabel}  |  locale: ${outcome.locale}  |  quality: ${outcome.quality}/100  |  tried: ${outcome.enginesTried.join(" → ")}  |  ${outcome.elapsedMs}ms  |  ${outcome.results.length} result(s)`);
    lines.push("=".repeat(72));
    if (outcome.warnings.length > 0) {
      for (const w of outcome.warnings) {
        lines.push(`⚠  ${w}`);
      }
      lines.push("");
    }
  }
  outcome.results.forEach((item, i) => {
    lines.push(`${i + 1}. ${item.name}`);
    lines.push(`   URL:     ${item.url}`);
    lines.push(`   Host:    ${item.host_name}`);
    if (item.date && item.date !== "N/A") lines.push(`   Date:    ${item.date}`);
    lines.push(`   Snippet: ${item.snippet}`);
    if (typeof item.score === "number") lines.push(`   Score:   ${item.score}/100  (engine: ${item.source_engine})`);
    lines.push("");
  });
  return lines.join("\n");
}

async function main() {
  let parsed: ParsedArgs;
  try {
    parsed = parseArgs(process.argv);
  } catch (err) {
    console.error(`Error: ${(err as Error).message}\n`);
    console.error(HELP);
    process.exit(2);
  }

  if (parsed.help) {
    console.log(HELP);
    return;
  }

  if (!parsed.query) {
    console.error("Error: query is required.\n");
    console.error(HELP);
    process.exit(2);
  }

  const outcome = await search(parsed.query, {
    num: parsed.num,
    engine: parsed.engine,
    recency_days: parsed.recencyDays,
    locale: parsed.locale || undefined,
    timeoutMs: parsed.timeoutMs,
  });

  if (!outcome.success) {
    if (!parsed.quiet) {
      console.error(`Search failed after ${outcome.elapsedMs}ms:`);
    }
    console.error(outcome.error);
    if (parsed.json || parsed.output) {
      const payload = JSON.stringify(outcome, null, parsed.pretty ? 2 : 0);
      if (parsed.output) {
        writeFileSync(resolve(parsed.output), payload, "utf8");
        console.error(`(error outcome written to ${parsed.output})`);
      } else {
        console.log(payload);
      }
    }
    process.exit(1);
  }

  if (parsed.output) {
    const payload = JSON.stringify(outcome, null, parsed.pretty ? 2 : 0);
    writeFileSync(resolve(parsed.output), payload, "utf8");
    console.error(`Wrote ${outcome.results.length} result(s) to ${parsed.output}`);
    return;
  }

  if (parsed.json) {
    console.log(JSON.stringify(outcome, null, parsed.pretty ? 2 : 0));
    return;
  }

  console.log(renderHuman(outcome, parsed.quiet));
}

main().catch((err) => {
  console.error("Fatal:", err?.stack || err);
  process.exit(1);
});
