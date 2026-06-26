import MemoryStore from './dist/storage/index.js';

async function run() {
  const store = new MemoryStore('/tmp/test-embed.db');
  
  // Store some test memories
  await store.remember('Phillip lives in Brisbane, Australia (timezone AEST)', 'semantic');
  await store.remember('Muninn is a memory system using SQLite and Nomic embeddings', 'semantic');
  await store.remember('OpenClaw gateway runs on port 18789', 'semantic');
  
  // Test recall
  const results = await store.recall('What port does OpenClaw use?', { limit: 3 });
  console.log('Query: What port does OpenClaw use?');
  console.log('Results:');
  results.forEach((r, i) => console.log(`  ${i+1}. ${r.content}`));
  
  store.close();
}

run().catch(console.error);
