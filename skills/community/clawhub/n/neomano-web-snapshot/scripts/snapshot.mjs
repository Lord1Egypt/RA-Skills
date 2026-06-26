#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

function parseArgs(argv) {
  const args = { url: null, out: null, fullPage: false, waitMs: 0, timeoutMs: 30000 };
  const rest = [...argv];
  args.url = rest.shift();
  while (rest.length) {
    const a = rest.shift();
    if (a === "--out") args.out = rest.shift();
    else if (a === "--full-page") args.fullPage = true;
    else if (a === "--wait-ms") args.waitMs = parseInt(rest.shift(), 10);
    else if (a === "--timeout-ms") args.timeoutMs = parseInt(rest.shift(), 10);
    else throw new Error(`Unknown arg: ${a}`);
  }
  if (!args.url) throw new Error("Missing url");
  if (!args.out) {
    const safe = args.url.replace(/[^a-z0-9]+/gi, "-").replace(/^-+|-+$/g, "").toLowerCase();
    args.out = `./snapshots/${safe || "site"}.png`;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const outPath = path.resolve(args.out);
fs.mkdirSync(path.dirname(outPath), { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1365, height: 768 } });

await page.goto(args.url, { waitUntil: "networkidle", timeout: args.timeoutMs });
if (args.waitMs > 0) await page.waitForTimeout(args.waitMs);
await page.screenshot({ path: outPath, fullPage: args.fullPage });

await browser.close();
console.log(outPath);
