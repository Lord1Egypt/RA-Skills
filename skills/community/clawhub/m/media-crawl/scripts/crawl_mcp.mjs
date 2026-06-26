#!/usr/bin/env node
/**
 * 通过 MCP 搜集（仅支持带 url 的工具）
 * 用法: node crawl_mcp.mjs <tool_name> <target_url> [base_url]
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { print_error } from "./stdio_utf8.mjs";

const SUPPORTED = ["crawl_bilibili", "crawl_douyin", "crawl_youtube", "crawl_zhihu"];

const [tool, targetUrl, baseUrl = process.env.BIL_CRAWL_URL || "http://127.0.0.1:39002"] = process.argv.slice(2);

if (!tool || !targetUrl) {
  print_error(
    `Usage: node crawl_mcp.mjs <${SUPPORTED.join("|")}> <target_url> [base_url]`
  );
  process.exit(2);
}

if (!SUPPORTED.includes(tool)) {
  print_error(`Unsupported tool: ${tool}`);
  print_error(
    "Use mcp_tool.mjs for: bilibili_search / bilibili_uploader / bilibili_popular / bilibili_weekly / bilibili_history"
  );
  process.exit(2);
}

const argsJson = JSON.stringify({ url: targetUrl });
const scriptDir = dirname(fileURLToPath(import.meta.url));

execFileSync(process.execPath, [join(scriptDir, "mcp_tool.mjs"), tool, argsJson, baseUrl], { stdio: "inherit" });
