#!/usr/bin/env node
/**
 * 归档查询
 * 用法: node list_archives_mcp.mjs [platform] [keyword] [limit] [base_url]
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const [
  platform = "",
  keyword = "",
  limitRaw = "50",
  baseUrl = process.env.BIL_CRAWL_URL || "http://127.0.0.1:39002",
] = process.argv.slice(2);

/** @type {Record<string, unknown>} */
const out = {};
if (platform) out.platform = platform;
if (keyword)  out.keyword  = keyword;
const n = Number(limitRaw);
if (!Number.isNaN(n) && n > 0) out.limit = Math.floor(n);

const argsJson = Object.keys(out).length ? JSON.stringify(out) : "{}";
const scriptDir = dirname(fileURLToPath(import.meta.url));

execFileSync(process.execPath, [join(scriptDir, "mcp_tool.mjs"), "list_archives", argsJson, baseUrl], { stdio: "inherit" });
