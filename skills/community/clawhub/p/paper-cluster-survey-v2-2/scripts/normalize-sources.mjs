#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

function printHelp() {
  console.log(`Usage:
  node scripts/normalize-sources.mjs [--stdin] [--out FILE] <source...>

Normalize local paper PDFs and paper URLs into a JSON manifest.
`);
}

function isHttpUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function normalizeUrl(value) {
  const url = new URL(value);
  if (url.hostname === "arxiv.org" && url.pathname.startsWith("/pdf/")) {
    url.pathname = url.pathname.replace(/^\/pdf\//, "/abs/").replace(/\.pdf$/i, "");
  }
  url.hash = "";
  return url.toString();
}

function inferKind(value) {
  if (isHttpUrl(value)) {
    const lower = value.toLowerCase();
    if (lower.includes("arxiv.org") || lower.endsWith(".pdf")) {
      return "paper_url";
    }
    return "url";
  }
  if (value.toLowerCase().endsWith(".pdf")) {
    return "pdf";
  }
  return "path";
}

function titleHintFromPath(value) {
  return path.basename(value, path.extname(value))
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeSource(value, index) {
  const kind = inferKind(value);
  const record = {
    source_id: `paper-${String(index + 1).padStart(3, "0")}`,
    original: value,
    kind,
  };

  if (kind === "pdf" || kind === "path") {
    record.path = path.resolve(value);
    record.exists = fs.existsSync(record.path);
    record.title_hint = titleHintFromPath(value);
    return record;
  }

  record.url = normalizeUrl(value);
  record.title_hint = "";
  return record;
}

async function readStdinLines() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function parseArgs(argv) {
  const args = [];
  let readStdin = false;
  let outFile = "";

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help") {
      printHelp();
      process.exit(0);
    }
    if (arg === "--stdin") {
      readStdin = true;
      continue;
    }
    if (arg === "--out") {
      outFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    args.push(arg);
  }

  return { args, readStdin, outFile };
}

async function main() {
  const { args, readStdin, outFile } = parseArgs(process.argv.slice(2));
  const stdinValues = readStdin ? await readStdinLines() : [];
  const inputs = [...args, ...stdinValues];

  if (inputs.length === 0) {
    printHelp();
    process.exit(1);
  }

  const manifest = {
    generated_at: new Date().toISOString(),
    total_sources: inputs.length,
    sources: inputs.map(normalizeSource),
  };

  const payload = `${JSON.stringify(manifest, null, 2)}\n`;
  if (outFile) {
    fs.writeFileSync(outFile, payload, "utf8");
  } else {
    process.stdout.write(payload);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
