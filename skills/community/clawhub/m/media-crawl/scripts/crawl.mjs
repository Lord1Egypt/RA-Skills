#!/usr/bin/env node
/**
 * 快速搜集（REST 端点）
 * 用法: node crawl.mjs <platform> <url> [base_url]
 */
import { print, print_error } from "./stdio_utf8.mjs";

const SUPPORTED = ["bilibili", "douyin", "youtube", "zhihu"];

const [platform, targetUrl, baseUrl = process.env.BIL_CRAWL_URL || "http://127.0.0.1:39002"] = process.argv.slice(2);

if (!platform || !targetUrl) {
  print_error(
    `Usage: node crawl.mjs <${SUPPORTED.join("|")}> <target_url> [base_url]`
  );
  process.exit(2);
}

if (!SUPPORTED.includes(platform)) {
  print_error(`Unsupported platform: ${platform}`);
  process.exit(2);
}

const encoded = encodeURIComponent(targetUrl);
const endpoint = `${baseUrl}/start-crawl/${platform}/${encoded}`;

/** @param {string} url */
async function probe(url) {
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(3000) });
    return r.ok || r.status < 500;
  } catch {
    return false;
  }
}

if (!(await probe(`${baseUrl}/health`)) && !(await probe(`${baseUrl}/`))) {
  print_error(`Service not reachable at ${baseUrl}`);
  process.exit(1);
}

const res = await fetch(endpoint, {
  method: "POST",
  headers: { "Content-Type": "application/json", Accept: "application/json" },
  body: JSON.stringify({ source: "ai" }),
});

const text = await res.text();
try {
  print(JSON.stringify(JSON.parse(text), null, 2));
} catch {
  print(text);
}
