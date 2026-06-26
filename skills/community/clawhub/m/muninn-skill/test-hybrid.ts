import MemoryStore from './dist/storage/index.js';

async function run() {
  const store = new MemoryStore('/tmp/test-hybrid.db');
  
  // Store test memories
  await store.remember('Phillip lives in Brisbane, Australia', 'semantic');
  await store.remember('Muninn uses SQLite and Nomic embeddings', 'semantic');
  await store.remember('OpenClaw runs on port 18789', 'semantic');
  await store.remember('KakāpōHiko is the strategic agent', 'semantic');
  await store.remember('Elev8Advisory is an HR tool', 'semantic');
  
  // Test recall
  console.log('Testing recall...');
  const results = await store.recall('What port does OpenClaw use?', { limit: 3 });
  console.log('Query: What port does OpenClaw use?');
  results.forEach((r, i) => {
    const score = (r as any)._finalScore || (r as any)._rrfScore || 'N/A';
    console.log(`  ${i+1}. [score=${score}] ${r.content.slice(0, 60)}...`);
  });
  
  store.close();
}

run().catch(console.error);
