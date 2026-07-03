/**
 * Quick-start example for the local-search skill.
 *
 * Run with:
 *   tsx scripts/web_search.ts                # default query
 *   tsx scripts/web_search.ts "your query" 5  # custom query + num
 *
 * This script intentionally stays tiny — it's a smoke-test you can
 * eyeball, not a feature showcase. For the full CLI see `bin/web-search.ts`.
 */
import { search, type SearchFunctionResultItem } from "../src/index.js";

async function main(query: string, num: number = 10) {
  const outcome = await search(query, { num, engine: "auto" });

  if (!outcome.success) {
    console.error("Web search failed:", outcome.error);
    process.exit(1);
  }

  console.log("Search Results:");
  console.log("================\n");
  console.log(
    `(engine: ${outcome.engine}, tried: ${outcome.enginesTried.join(" → ")}, ${outcome.elapsedMs}ms)\n`
  );

  outcome.results.forEach((item: SearchFunctionResultItem, index: number) => {
    console.log(`${index + 1}. ${item.name}`);
    console.log(`   URL:     ${item.url}`);
    console.log(`   Host:    ${item.host_name}`);
    if (item.date && item.date !== "N/A") console.log(`   Date:    ${item.date}`);
    console.log(`   Snippet: ${item.snippet}`);
    console.log(`   Engine:  ${item.source_engine}${typeof item.score === "number" ? `  (score ${item.score})` : ""}`);
    console.log("");
  });

  console.log(`\nTotal results: ${outcome.results.length}`);
}

const query = process.argv[2] ?? "What is the capital of France?";
const num = process.argv[3] ? parseInt(process.argv[3], 10) : 5;
main(query, num).catch((err) => {
  console.error("Fatal:", err?.stack || err);
  process.exit(1);
});
