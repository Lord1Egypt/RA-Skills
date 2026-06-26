import MemoryStore from './dist/storage/index.js';

async function run() {
  const store = new MemoryStore('/tmp/test-rel.db');
  
  // Store the revenue facts
  await store.remember('Elev8Advisory target revenue is $2000/month', 'semantic', {
    entities: ['Elev8Advisory'],
    timestamp: '2026-02-10T09:00:00Z',
    sessionId: 'session_001'
  });
  
  await store.remember('Elev8Advisory target revenue is $1000/month (updated from $2000)', 'semantic', {
    entities: ['Elev8Advisory'],
    timestamp: '2026-02-18T16:00:00Z',
    sessionId: 'session_004'
  });
  
  await store.remember('Elev8Advisory has a customer paying $500/month', 'semantic', {
    entities: ['Elev8Advisory'],
    timestamp: '2026-02-22T08:00:00Z',
    sessionId: 'session_005'
  });
  
  // Check entities
  const entities = store.getEntities();
  console.log('Entities:', entities.map((e: any) => e.name || e));
  
  // Try recall with temporal query
  const results = await store.recall('What is the revenue target for Elev8Advisory?', { limit: 5 });
  console.log('\nRecall results:');
  results.forEach((r, i) => console.log(`${i+1}. ${r.content}`));
  
  store.close();
}

run().catch(console.error);
