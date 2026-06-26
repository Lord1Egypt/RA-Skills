/**
 * Quick test for OpenClaw Memory System
 */

import { MemoryStore } from './src/storage/index.js';

async function test() {
  console.log('🧪 Testing OpenClaw Memory System...\n');
  
  const store = new MemoryStore('/tmp/test-memory.db');
  
  // Test 1: Store some memories
  console.log('📝 Test 1: Storing memories...');
  
  const mem1 = await store.remember(
    'User prefers TypeScript over JavaScript for all projects',
    'semantic',
    { title: 'Language preference', entities: ['TypeScript', 'JavaScript'], topics: ['programming', 'preference'] }
  );
  console.log('  ✅ Stored semantic memory:', mem1.id);
  
  const mem2 = await store.remember(
    'Had a meeting with the team about the new OpenClaw memory system architecture',
    'episodic',
    { title: 'Team meeting', entities: ['OpenClaw', 'Team'], topics: ['architecture', 'planning'] }
  );
  console.log('  ✅ Stored episodic memory:', mem2.id);
  
  const mem3 = await store.remember(
    'Remember to review pull requests daily and test changes before merging',
    'semantic',
    { title: 'Code review habit', topics: ['workflow', 'best-practices'] }
  );
  console.log('  ✅ Stored semantic memory:', mem3.id);
  
  // Test 2: Create a procedure
  console.log('\n📋 Test 2: Creating procedure...');
  
  const proc = await store.createProcedure(
    'Deploy to production',
    [
      'Run tests locally',
      'Create pull request',
      'Get code review approval',
      'Merge to main',
      'Deploy via CI/CD'
    ],
    'Standard deployment workflow'
  );
  console.log('  ✅ Created procedure:', proc.id, 'v' + proc.version);
  
  // Test 3: Recall memories
  console.log('\n🔍 Test 3: Recalling memories...');
  
  const results = await store.recall('programming language preferences', { limit: 5 });
  console.log('  Found', results.length, 'memories for "programming language preferences":');
  results.forEach((m, i) => {
    console.log(`    ${i + 1}. [${m.type}] ${m.content.slice(0, 60)}...`);
  });
  
  // Test 4: Get stats
  console.log('\n📊 Test 4: Getting stats...');
  
  const stats = store.getStats();
  console.log('  Total memories:', stats.total);
  console.log('  By type:', stats.byType);
  console.log('  Procedures:', stats.procedures);
  console.log('  Entities:', stats.entities);
  
  // Test 5: Get entities
  console.log('\n🏷️  Test 5: Getting entities...');
  
  const entities = store.getEntities();
  console.log('  Tracked entities:', entities.map(e => e.name + ` (${e.memory_count})`).join(', '));
  
  // Test 6: Procedure feedback (success)
  console.log('\n✅ Test 6: Recording procedure success...');
  
  const updatedProc1 = await store.procedureFeedback(proc.id, true);
  console.log('  Success count:', updatedProc1.success_count, '| Version:', updatedProc1.version, '| Reliable:', updatedProc1.is_reliable);
  
  // Test 7: Procedure feedback (failure)
  console.log('\n❌ Test 7: Recording procedure failure...');
  
  const updatedProc2 = await store.procedureFeedback(proc.id, false, 3, 'Timeout during deployment');
  console.log('  Failure count:', updatedProc2.failure_count, '| New version:', updatedProc2.version);
  console.log('  Evolution log:', updatedProc2.evolution_log[updatedProc2.evolution_log.length - 1]?.change);
  
  // Test 8: Get neighbors (graph)
  console.log('\n🔗 Test 8: Testing graph connections...');
  
  store.connect(mem1.id, mem2.id, 'related_to');
  const neighbors = store.getNeighbors(mem1.id, 1);
  console.log('  Neighbors of mem1:', neighbors.map(n => n.id).join(', '));
  
  // Clean up
  store.close();
  
  console.log('\n🎉 All tests passed!');
}

test().catch(console.error);
