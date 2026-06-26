/**
 * P7 Comprehensive Test
 * Tests spreading activation, temporal decay, and session priming
 */

import { MemoryStore } from './dist/storage/index.js';
import { TemporalDecayScorer } from './dist/retrieval/temporal-decay.js';
import { simpleCohesionQuery } from './dist/retrieval/session-priming.js';

async function testP7Comprehensive() {
  console.log('🧪 P7 Comprehensive Test');
  console.log('='.repeat(50));
  
  const store = new MemoryStore('/tmp/p7-comprehensive.db');
  
  // Test 1: Temporal Decay
  console.log('\n📊 Test 1: Temporal Decay Scorer');
  console.log('-'.repeat(30));
  
  const now = new Date();
  const memories = [
    { id: '1', content: 'Recent memory', created_at: now.toISOString(), salience: 0.8, entities: ['Muninn'] },
    { id: '2', content: 'Week-old memory', created_at: new Date(now - 7 * 24 * 60 * 60 * 1000).toISOString(), salience: 0.8, entities: ['Muninn'] },
    { id: '3', content: 'Month-old memory', created_at: new Date(now - 30 * 24 * 60 * 60 * 1000).toISOString(), salience: 0.8, entities: ['Muninn'] },
    { id: '4', content: 'Old memory', created_at: new Date(now - 60 * 24 * 60 * 60 * 1000).toISOString(), salience: 0.8, entities: ['Muninn'] },
  ];
  
  const scorer = new TemporalDecayScorer({ halfLifeDays: 30 });
  
  for (const mem of memories) {
    const score = scorer.score(mem);
    console.log(`  ${mem.content}: ${score.toFixed(3)}`);
  }
  
  // Test 2: Entity Store with Mentions
  console.log('\n📊 Test 2: Entity Store');
  console.log('-'.repeat(30));
  
  // Add entities with multiple mentions
  const entityStore = store.getEntityStore();
  
  // Manually add entities (simulating multiple session mentions)
  entityStore.addEntity({ name: 'Muninn', type: 'project', aliases: [] });
  entityStore.addEntity({ name: 'OpenClaw', type: 'organization', aliases: [] });
  entityStore.addEntity({ name: 'Phillip', type: 'person', aliases: [] });
  
  const entities = entityStore.getAll();
  console.log(`  Entities: ${entities.map(e => `${e.name}(${e.mentions})`).join(', ')}`);
  
  // Test 3: Session Priming (stale but important)
  console.log('\n📊 Test 3: Session Priming');
  console.log('-'.repeat(30));
  
  // Get all memories for simple cohesion query
  const allMemories = await store.recall('', { limit: 50 });
  const relStore = store.getRelationshipStore();
  
  const priming = await simpleCohesionQuery(entityStore, relStore, allMemories, {
    minMentions: 1,  // Low threshold for testing
    staleHours: 0,   // Consider all as stale for test
    maxEntities: 5
  });
  
  console.log(`  Stale entities: ${priming.staleEntities.length}`);
  console.log(`  Primed memories: ${priming.primedMemories.length}`);
  
  // Test 4: Recall with P7 Options
  console.log('\n📊 Test 4: Recall with P7 Options');
  console.log('-'.repeat(30));
  
  await store.remember('Muninn is the memory system project', 'semantic', { sessionId: 'test' });
  await store.remember('Phillip works on Muninn', 'semantic', { sessionId: 'test' });
  await store.remember('OpenClaw uses Muninn for memory', 'semantic', { sessionId: 'test' });
  
  const tests = [
    { name: 'Baseline', opts: {} },
    { name: 'Spreading', opts: { enableSpreading: true } },
    { name: 'Temporal', opts: { enableTemporalDecay: true } },
    { name: 'Full P7', opts: { enableSpreading: true, enableTemporalDecay: true } },
  ];
  
  for (const t of tests) {
    const results = await store.recall('Tell me about Muninn', { limit: 3, ...t.opts });
    console.log(`  ${t.name}: ${results.length} results`);
  }
  
  console.log('\n✅ P7 Comprehensive Test Complete');
  
  store.close();
}

testP7Comprehensive().catch(console.error);
