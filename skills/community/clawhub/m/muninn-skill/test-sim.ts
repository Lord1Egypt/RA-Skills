import MemoryStore from './dist/storage/index.js';

async function run() {
  const store = new MemoryStore('/tmp/test-sim.db');
  
  // Store test memories
  await store.remember('Phillip lives in Brisbane, Australia', 'semantic');
  await store.remember('Muninn uses SQLite and Nomic embeddings', 'semantic');
  await store.remember('OpenClaw runs on port 18789', 'semantic');
  
  // Test with debug
  const results = await store.recall('What port does OpenClaw use?', { limit: 3 });
  console.log('Query: What port does OpenClaw use?');
  results.forEach((r, i) => {
    console.log(`  ${i+1}. [score=${(r as any).similarity?.toFixed(3) || 'N/A'}] ${r.content}`);
  });
  
  store.close();
}

run().catch(console.error);
