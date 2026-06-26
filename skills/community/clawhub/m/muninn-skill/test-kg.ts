import MemoryStore from './dist/storage/index.js';

async function run() {
  const store = new MemoryStore('/tmp/test-kg.db');
  
  // Store revenue targets with timestamps
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
  console.log('Entities:', entities.length);
  
  // Check relationships
  const relStore = store.getRelationshipStore();
  const rels = relStore.getAllRelationships();
  console.log('Relationships:', rels.length);
  
  // Query for revenue history
  try {
    const history = store.getEntityHistory('Elev8Advisory');
    console.log('Elev8Advisory History:', JSON.stringify(history, null, 2));
  } catch (e: any) {
    console.log('History error:', e.message);
  }
  
  store.close();
}

run().catch(console.error);
