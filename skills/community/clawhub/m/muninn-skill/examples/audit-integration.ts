/**
 * Audit Integration Example
 * 
 * Demonstrates how to integrate Phase 1 audit capabilities
 * with the Muninn MemoryStore
 * 
 * Run: npx tsx examples/audit-integration.ts
 */

import { MemoryStore } from '../storage/index.js';
import { createAuditStore, createAuditWrappers } from '../storage/audit-integration.js';
import { calculateStaleness } from '../storage/audit.js';

async function main() {
  console.log('🔍 Muninn Audit Integration Demo\n');
  
  // Initialize memory store
  const store = new MemoryStore('/tmp/muninn-audit-demo.db');
  
  // Initialize audit store
  const auditStore = createAuditStore(store.db);
  
  // Create audit wrappers
  const audit = createAuditWrappers(auditStore);
  
  // ==========================================================================
  // Scenario 1: Store with audit
  // ==========================================================================
  console.log('📝 Scenario 1: Store with audit');
  
  const mem1 = await store.remember(
    'Phillip works at Elev8Advisory as a Fractional CTO',
    'semantic'
  );
  audit.auditStoreSuccess(mem1, { agent_id: 'agent:charlie', duration_ms: 45 });
  console.log('  ✅ Stored memory:', mem1.id);
  
  // Add valid_at/invalid_at for testing staleness
  // In real usage, these would be set based on temporal metadata
  const mem2 = await store.remember(
    'The project deadline was March 15, 2024',  // Past date
    'episodic'
  );
  audit.auditStoreSuccess(mem2, { agent_id: 'agent:charlie' });
  console.log('  ✅ Stored memory:', mem2.id);
  
  // ==========================================================================
  // Scenario 2: Recall with audit
  // ==========================================================================
  console.log('\n🔍 Scenario 2: Recall with audit');
  
  const recallStart = Date.now();
  const memories = await store.recall('Phillip work');
  const recallDuration = Date.now() - recallStart;
  
  // Get staleness for each memory
  const stalenessScores = memories.map(m => {
    const staleness = calculateStaleness({
      created_at: m.created_at,
      valid_at: m.valid_at,
      invalid_at: m.invalid_at
    });
    return staleness.staleness_score;
  });
  
  const auditResult = audit.auditRecallSuccess(
    'Phillip work',
    memories,
    {
      path_type: 'hybrid',
      path: { method: 'bm25 + semantic' },
      duration_ms: recallDuration,
      agent_id: 'agent:charlie'
    }
  );
  
  console.log('  ✅ Recalled:', memories.length, 'memories');
  console.log('  📊 Verification score:', auditResult.verification_score.toFixed(2));
  console.log('  📊 Overall staleness:', auditResult.overall_staleness.toFixed(2));
  
  // ==========================================================================
  // Scenario 3: Update staleness tracking
  // ==========================================================================
  console.log('\n⏰ Scenario 3: Staleness tracking');
  
  for (const mem of memories) {
    audit.updateMemoryStaleness(mem);
  }
  
  const needsVerification = audit.getMemoriesNeedingVerification();
  console.log('  📊 Memories needing verification:', needsVerification.length);
  
  // ==========================================================================
  // Scenario 4: Get retrieval stats
  // ==========================================================================
  console.log('\n📈 Scenario 4: Retrieval statistics');
  
  const stats = audit.getRetrievalStats();
  console.log('  Total retrievals:', stats.total_retrievals);
  console.log('  Avg verification score:', stats.avg_verification_score?.toFixed(2) || 'N/A');
  console.log('  Helpful count:', stats.helpful_count);
  console.log('  Not relevant count:', stats.not_relevant_count);
  console.log('  Feedback ratio:', stats.feedback_ratio?.toFixed(2) || 'N/A');
  
  // ==========================================================================
  // Scenario 5: Staleness penalties in retrieval
  // ==========================================================================
  console.log('\n⚖️ Scenario 5: Staleness-adjusted scoring');
  
  // Simulate retrieval results
  const mockMemories = [
    { id: 'mem_fresh', similarity: 0.9 },
    { id: 'mem_old', similarity: 0.9 },
    { id: 'mem_ancient', similarity: 0.9 }
  ];
  
  const stalenessMap = new Map([
    ['mem_fresh', 0.05],    // Very fresh
    ['mem_old', 0.4],       // Somewhat stale
    ['mem_ancient', 0.85]   // Very stale
  ]);
  
  const { adjustScoresForStaleness } = await import('../storage/audit.js');
  const adjusted = adjustScoresForStaleness(mockMemories, stalenessMap);
  
  console.log('  Fresh memory (0.9 → penalty 0.05):', adjusted[0].adjustedSimilarity.toFixed(2));
  console.log('  Old memory (0.9 → penalty 0.4):', adjusted[1].adjustedSimilarity.toFixed(2));
  console.log('  Ancient memory (0.9 → penalty 0.85):', adjusted[2].adjustedSimilarity.toFixed(2));
  
  // ==========================================================================
  // Cleanup
  // ==========================================================================
  store.close();
  console.log('\n✅ Audit integration demo complete!');
}

main().catch(console.error);