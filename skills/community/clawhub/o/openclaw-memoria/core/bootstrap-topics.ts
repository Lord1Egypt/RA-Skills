/**
 * Bootstrap: tag all untagged facts and run topic emergence scan.
 * Run once to seed the system.
 */
import { MemoriaDB } from "./db.js";
import { OllamaLLM } from "./providers/ollama.js";
import { OllamaEmbed } from "./providers/ollama.js";
import { TopicManager } from "./topics.js";

const WORKSPACE = process.env.HOME + "/.openclaw/workspace";

async function main() {
  const db = new MemoriaDB(WORKSPACE);
  const llm = new OllamaLLM("http://localhost:11434", "gemma3:4b");
  const embedder = new OllamaEmbed("http://localhost:11434", "nomic-embed-text-v2-moe", 768);
  const topicMgr = new TopicManager(db, llm, embedder, {
    emergenceThreshold: 3,
    scanInterval: 999, // We'll manually scan
  });

  // Get all untagged, active facts
  const untagged = db.raw.prepare(
    "SELECT id, fact, category FROM facts WHERE (tags = '[]' OR tags IS NULL) AND superseded = 0 ORDER BY created_at DESC"
  ).all() as Array<{ id: string; fact: string; category: string }>;

  console.log(`\n🏷️  Tagging ${untagged.length} untagged facts...\n`);

  let tagged = 0;
  let failed = 0;
  const batchSize = 10;
  
  for (let i = 0; i < untagged.length; i += batchSize) {
    const batch = untagged.slice(i, i + batchSize);
    const promises = batch.map(async (f) => {
      try {
        const { keywords, topics } = await topicMgr.onFactCaptured(f.id, f.fact, f.category);
        if (keywords.length > 0) {
          tagged++;
          if (tagged % 50 === 0 || tagged <= 5) {
            console.log(`  [${tagged}/${untagged.length}] "${f.fact.slice(0, 50)}..." → [${keywords.join(", ")}]`);
          }
        } else {
          failed++;
        }
      } catch (e) {
        failed++;
      }
    });

    // Process batch sequentially to avoid hammering Ollama
    for (const p of promises) await p;

    // Progress
    if ((i + batchSize) % 100 === 0) {
      console.log(`  Progress: ${Math.min(i + batchSize, untagged.length)}/${untagged.length} (${tagged} tagged, ${failed} failed)`);
    }
  }

  console.log(`\n✅ Tagging done: ${tagged} tagged, ${failed} failed\n`);

  // Now run the emergence scan
  console.log("🔍 Running topic emergence scan...\n");
  const scanResult = await topicMgr.scanAndEmerge();
  console.log(`  Created: ${scanResult.created} topics`);
  console.log(`  Merged: ${scanResult.merged} topics`);
  console.log(`  Sub-topics: ${scanResult.subtopics}`);

  // Show results
  const stats = topicMgr.stats();
  console.log(`\n📊 Final stats:`);
  console.log(`  Total topics: ${stats.totalTopics}`);
  console.log(`  Top-level: ${stats.topLevelTopics}`);
  console.log(`  Sub-topics: ${stats.subTopics}`);
  console.log(`  Orphan facts: ${stats.orphanFacts}`);
  console.log(`  Avg facts/topic: ${stats.avgFactsPerTopic}`);

  // Show topic list
  const topics = db.raw.prepare("SELECT name, keywords, fact_count, importance_score FROM topics ORDER BY importance_score DESC LIMIT 20").all() as any[];
  console.log(`\n🏷️  Top topics:`);
  for (const t of topics) {
    const kw = JSON.parse(t.keywords).slice(0, 5).join(", ");
    console.log(`  ${t.name} (${t.fact_count} facts, score ${t.importance_score.toFixed(1)}) — [${kw}]`);
  }

  db.raw.close();
}

main().catch(console.error);
