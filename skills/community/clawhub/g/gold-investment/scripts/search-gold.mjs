#!/usr/bin/env node

/**
 * Gold Analysis Search Script
 * 获取黄金相关信息
 */

function usage() {
  console.error(`Usage: search-gold.mjs "query" [-n 5] [--deep] [--type price|news|technical|all]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let query = "";
let n = 5;
let searchDepth = "basic";
let type = "all";

// 解析参数
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") {
    n = Number.parseInt(args[i + 1] ?? "5", 10);
    i++;
    continue;
  }
  if (a === "--deep") {
    searchDepth = "advanced";
    continue;
  }
  if (a === "--type") {
    type = args[i + 1] ?? "all";
    i++;
    continue;
  }
  if (!a.startsWith("--")) {
    query = a;
  }
}

// 备用查询（当没有传入 query 时使用）
const defaultQueries = {
  price: ["黄金价格走势 2026年3月", "现货黄金 美元 盎司"],
  news: ["黄金新闻 2026年3月", "黄金市场分析"],
  technical: ["黄金技术分析 RSI MACD", "黄金支撑位 阻力位"],
  all: ["黄金价格走势分析 2026年3月", "黄金投资分析"]
};

const queries = query ? [query] : (defaultQueries[type] || defaultQueries.all);

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

async function searchTavily(q) {
  const body = {
    api_key: apiKey,
    query: q,
    search_depth: searchDepth,
    topic: "general",
    max_results: Math.max(1, Math.min(n, 20)),
    include_answer: true,
    include_raw_content: false,
  };

  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Tavily Search failed (${resp.status}): ${text}`);
  }

  return resp.json();
}

// 主搜索
(async () => {
  try {
    const q = queries[0];
    const data = await searchTavily(q);
    
    // Print AI-generated answer if available
    if (data.answer) {
      console.log("## Answer\n");
      console.log(data.answer);
      console.log("\n---\n");
    }

    // Print results
    const results = (data.results ?? []).slice(0, n);
    console.log("## Sources\n");

    for (const r of results) {
      const title = String(r?.title ?? "").trim();
      const url = String(r?.url ?? "").trim();
      const content = String(r?.content ?? "").trim();
      const score = r?.score ? ` (relevance: ${(r.score * 100).toFixed(0)}%)` : "";
      
      if (!title || !url) continue;
      console.log(`- **${title}**${score}`);
      console.log(`  ${url}`);
      if (content) {
        console.log(`  ${content.slice(0, 300)}${content.length > 300 ? "..." : ""}`);
      }
      console.log();
    }
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
})();
