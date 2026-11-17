/**
 * Example: Using @primo-studio/memoria-core standalone
 * 
 * This demonstrates using Memoria without OpenClaw.
 * Run with: node --loader ts-node/esm example.ts
 */

import { Memoria } from './index.js';

async function main() {
  console.log('🧠 Initializing Memoria core...\n');

  // Initialize with Ollama (local, free)
  const memoria = await Memoria.init({
    dbPath: './example-memoria.db',
    provider: 'ollama',
    model: 'qwen3.5:4b',
    embeddingModel: 'nomic-embed-text-v2-moe',
    recallLimit: 5,
    debug: true
  });

  console.log('\n✅ Memoria initialized!\n');

  // Store some facts
  console.log('📝 Storing facts...\n');
  
  await memoria.store('User prefers dark mode in all applications', 'preference', 0.95);
  await memoria.store('User is located in New York, USA', 'savoir', 0.9);
  await memoria.store('User favorite programming language is TypeScript', 'preference', 0.85);
  await memoria.store('Project deadline is April 15, 2026', 'chronologie', 0.9);
  await memoria.store('User dislikes verbose error messages', 'preference', 0.8);

  console.log('✅ 5 facts stored!\n');

  // Recall facts
  console.log('🔍 Recalling: "What are the user preferences?"\n');
  const results = await memoria.recall('What are the user preferences?', { limit: 3 });
  
  console.log(`Found ${results.totalFound} facts:\n`);
  for (const fact of results.facts) {
    console.log(`  • [${fact.category}] ${fact.fact}`);
    console.log(`    Confidence: ${fact.confidence}, Score: ${fact.score.toFixed(2)}\n`);
  }

  // Natural language query
  console.log('💬 Query: "Tell me about the user"\n');
  const answer = await memoria.query('Tell me about the user');
  console.log(answer);
  console.log('');

  // Stats
  console.log('📊 Memory statistics:\n');
  const stats = await memoria.stats();
  console.log(`  Total facts: ${stats.totalFacts}`);
  console.log(`  Total embeddings: ${stats.totalEmbeddings}`);
  console.log(`  Total relations: ${stats.totalRelations}`);
  console.log(`  Total topics: ${stats.totalTopics}`);
  console.log(`  Total patterns: ${stats.totalPatterns}`);
  console.log(`  Total observations: ${stats.totalObservations}\n`);

  if (Object.keys(stats.categoryCounts).length > 0) {
    console.log('  By category:');
    for (const [cat, count] of Object.entries(stats.categoryCounts)) {
      console.log(`    ${cat}: ${count}`);
    }
    console.log('');
  }

  // Close
  memoria.close();
  console.log('✅ Memoria closed. Database saved.\n');
}

main().catch(console.error);
