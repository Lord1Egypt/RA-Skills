import MemoryStore from './dist/storage/index.js';
import { getValueWithHistory } from './dist/reasoning/contradiction.js';

async function run() {
  const store = new MemoryStore('/tmp/test-kg2.db');
  
  // Store revenue facts
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
  
  // Get entity store and relationship store
  const entityStore = store.getEntityStore();
  const relStore = store.getRelationshipStore();
  
  // Find entity
  const entity = entityStore.findEntity('Elev8Advisory');
  console.log('Entity:', entity);
  
  // Get relationships
  if (entity) {
    const history = getValueWithHistory(relStore, entityStore, 'Elev8Advisory');
    console.log('\nValue History:', JSON.stringify(history, null, 2));
  }
  
  // Try recall
  const results = await store.recall('What is the revenue target for Elev8Advisory?', { limit: 5 });
  console.log('\nRecall results:');
  results.forEach((r, i) => console.log(`${i+1}. ${r.content}`));
  
  store.close();
}

run().catch(console.error);
