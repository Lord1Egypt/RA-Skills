/**
 * Multi-Hop Path Finding Tests
 * 
 * Tests the BFS path finding algorithm for multi-hop queries.
 * 
 * Run with: npx tsx src/tests/multi-hop-paths.test.ts
 */

import Database from 'better-sqlite3';
import { EntityStore } from '../storage/entity-store.js';
import { RelationshipStore } from '../storage/relationship-store.js';
import { findPaths, findPathsByName, scorePath, rankPaths, Path } from '../retrieval/graph-traversal.js';

// ============================================================================
// TEST HELPERS
// ============================================================================

let testsPassed = 0;
let testsFailed = 0;

function assert(condition: boolean, message: string) {
  if (condition) {
    console.log(`  ✓ ${message}`);
    testsPassed++;
  } else {
    console.error(`  ✗ ${message}`);
    testsFailed++;
  }
}

function assertEqual<T>(actual: T, expected: T, message: string) {
  if (actual === expected) {
    console.log(`  ✓ ${message}`);
    testsPassed++;
  } else {
    console.error(`  ✗ ${message} (expected: ${JSON.stringify(expected)}, got: ${JSON.stringify(actual)})`);
    testsFailed++;
  }
}

function assertGreaterThan(actual: number, min: number, message: string) {
  if (actual > min) {
    console.log(`  ✓ ${message}`);
    testsPassed++;
  } else {
    console.error(`  ✗ ${message} (expected: > ${min}, got: ${actual})`);
    testsFailed++;
  }
}

function assertGreaterOrEqual(actual: number, min: number, message: string) {
  if (actual >= min) {
    console.log(`  ✓ ${message}`);
    testsPassed++;
  } else {
    console.error(`  ✗ ${message} (expected: >= ${min}, got: ${actual})`);
    testsFailed++;
  }
}

// ============================================================================
// ISOLATED TEST RUNNER
// ============================================================================

function runTest(name: string, testFn: () => void | Promise<void>) {
  console.log(`\n--- ${name} ---`);
  try {
    const result = testFn();
    if (result instanceof Promise) {
      result.catch((error) => {
        console.error(`  ✗ Test threw error: ${error}`);
        testsFailed++;
      });
    }
  } catch (error) {
    console.error(`  ✗ Test threw error: ${error}`);
    testsFailed++;
  }
}

function createTestStores(): { db: Database.Database; entityStore: EntityStore; relationshipStore: RelationshipStore } {
  const db = new Database(':memory:');
  const entityStore = new EntityStore(db);
  const relationshipStore = new RelationshipStore(db);
  return { db, entityStore, relationshipStore };
}

// ============================================================================
// TESTS
// ============================================================================

function testDirectPath() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, bob.id, relationshipStore);
  
  assertEqual(paths.length, 1, 'Should find 1 path');
  assertEqual(paths[0].length, 1, 'Path should be 1 hop');
  assertEqual(paths[0].segments[0].type, 'knows', 'Relationship type should be knows');
}

function testTwoHopPath() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const carol = entityStore.addEntity({ name: 'Carol', type: 'person' });
  
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: carol.id,
    type: 'works_at',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, carol.id, relationshipStore);
  
  assertGreaterThan(paths.length, 0, 'Should find at least 1 path');
  assertEqual(paths[0].length, 2, 'Shortest path should be 2 hops');
  
  // Verify path: Alice -> Bob -> Carol
  const firstPath = paths[0];
  assertEqual(firstPath.segments[0].source, alice.id, 'First segment starts from Alice');
  assertEqual(firstPath.segments[0].target, bob.id, 'First segment goes to Bob');
  assertEqual(firstPath.segments[1].source, bob.id, 'Second segment starts from Bob');
  assertEqual(firstPath.segments[1].target, carol.id, 'Second segment goes to Carol');
}

function testThreeHopPath() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup: Alice -> Bob -> David (2 hops)
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const david = entityStore.addEntity({ name: 'David', type: 'person' });
  
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: david.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, david.id, relationshipStore, { maxHops: 3 });
  
  assertGreaterThan(paths.length, 0, 'Should find path to David');
  
  // Should find the shorter path first
  const shortestPath = paths[0];
  assertEqual(shortestPath.length, 2, 'Shortest path should be 2 hops via Bob');
}

function testNoPath() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup: Two disconnected entities
  const carol = entityStore.addEntity({ name: 'Carol', type: 'person' });
  const david = entityStore.addEntity({ name: 'David', type: 'person' });
  const acme = entityStore.addEntity({ name: 'Acme Corp', type: 'organization' });
  
  // Carol works at Acme
  relationshipStore.addRelationship({
    source: carol.id,
    target: acme.id,
    type: 'works_at',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // David is disconnected
  // Test
  const paths = findPaths(carol.id, david.id, relationshipStore);
  
  assertEqual(paths.length, 0, 'Should find no paths between disconnected entities');
}

function testContradictedRelationship() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const ent1 = entityStore.addEntity({ name: 'TestPerson1', type: 'person' });
  const ent2 = entityStore.addEntity({ name: 'TestPerson2', type: 'person' });
  
  // Add initial relationship
  const result1 = relationshipStore.addRelationship({
    source: ent1.id,
    target: ent2.id,
    type: 'knows',
    value: 'old-value',
    timestamp: '2025-01-01T00:00:00Z',
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Add contradicting relationship (different value, same type, newer)
  relationshipStore.addRelationship({
    source: ent1.id,
    target: ent2.id,
    type: 'knows',
    value: 'new-value',
    timestamp: '2026-01-01T00:00:00Z',
    sessionId: 'test',
    confidence: 1.0
  });
  
  // The first relationship should now be superseded
  const supersededRel = relationshipStore.getById(result1.relationship.id);
  assert(supersededRel?.supersededBy !== undefined, 'Old relationship should be superseded');
  
  // Find paths - should skip the superseded relationship
  // But we should still find a path via the new (non-superseded) relationship
  // Note: Since both relationships have same source/target, we need at least one valid path
  // Actually wait - the new relationship was added AFTER the old, so it has the NEW id
  // Let me trace through:
  // - Add rel1 with id=rel_xxx1
  // - Add rel2 with id=rel_xxx2, which finds rel1 as contradiction
  // - UPDATE rel1 SET superseded_by = rel_xxx2 WHERE id = rel_xxx1
  
  // So rel1 is superseded, rel2 is not
  // getBySource(ent1.id) returns BOTH
  // My code filters rel.supersededBy, so it should skip rel1
  
  const paths = findPaths(ent1.id, ent2.id, relationshipStore);
  
  // Should still find a path via the new (non-superseded) relationship
  assertGreaterOrEqual(paths.length, 1, 'Should find path with non-superseded relationship');
}

function testMaxHopsLimit() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const david = entityStore.addEntity({ name: 'David', type: 'person' });
  
  // Alice -> Bob -> David (2 hops)
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: david.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths1 = findPaths(alice.id, david.id, relationshipStore, { maxHops: 1 });
  assertEqual(paths1.length, 0, 'Should not find path with maxHops=1');
  
  const paths2 = findPaths(alice.id, david.id, relationshipStore, { maxHops: 2 });
  assertGreaterThan(paths2.length, 0, 'Should find path with maxHops=2');
}

function testMaxPathsLimit() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup: Multiple paths to the same target
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const carol = entityStore.addEntity({ name: 'Carol', type: 'person' });
  const david = entityStore.addEntity({ name: 'David', type: 'person' });
  
  // Path 1: Alice -> Bob -> David
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: david.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Path 2: Alice -> Carol -> David
  relationshipStore.addRelationship({
    source: alice.id,
    target: carol.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: carol.id,
    target: david.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, david.id, relationshipStore, { maxHops: 3, maxPaths: 2 });
  
  // Should limit to maxPaths
  assert(paths.length <= 2, 'Should limit to maxPaths');
}

function testPathScoring() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const carol = entityStore.addEntity({ name: 'Carol', type: 'person' });
  
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 0.5  // Low confidence
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: carol.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, carol.id, relationshipStore);
  
  if (paths.length > 0) {
    const score = scorePath(paths[0], relationshipStore, entityStore);
    assertGreaterThan(score, 0, 'Score should be positive');
    console.log(`    Path score: ${score.toFixed(4)}`);
  } else {
    console.log('    (No paths found, skipping score test)');
    testsFailed++; // Should have found a path
  }
}

function testFindPathsByName() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPathsByName('Alice', 'Bob', entityStore, relationshipStore);
  
  assertEqual(paths.length, 1, 'Should find 1 path by name');
  assertEqual(paths[0].length, 1, 'Path should be 1 hop');
}

function testRankPaths() {
  const { entityStore, relationshipStore } = createTestStores();
  
  // Setup: Multiple paths of different lengths
  const alice = entityStore.addEntity({ name: 'Alice', type: 'person' });
  const bob = entityStore.addEntity({ name: 'Bob', type: 'person' });
  const carol = entityStore.addEntity({ name: 'Carol', type: 'person' });
  const david = entityStore.addEntity({ name: 'David', type: 'person' });
  
  // Short path (2 hops): Alice -> Bob -> David
  relationshipStore.addRelationship({
    source: alice.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: bob.id,
    target: david.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Long path (3 hops): Alice -> Carol -> Bob -> David
  relationshipStore.addRelationship({
    source: alice.id,
    target: carol.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  relationshipStore.addRelationship({
    source: carol.id,
    target: bob.id,
    type: 'knows',
    timestamp: new Date().toISOString(),
    sessionId: 'test',
    confidence: 1.0
  });
  
  // Test
  const paths = findPaths(alice.id, david.id, relationshipStore, { maxHops: 3 });
  const rankedPaths = rankPaths(paths, relationshipStore, entityStore);
  
  // Shorter paths should be ranked higher
  if (rankedPaths.length > 1) {
    assert(rankedPaths[0].length <= rankedPaths[1].length, 'Shorter paths should be ranked first');
  }
}

// ============================================================================
// COREFERENCE TESTS
// ============================================================================

async function testCoreferenceResolution() {
  // Dynamic import for ES module - fix path
  const coreferenceModule = await import('../../dist/extractors/coreference.js');
  const { resolveCoreferences } = coreferenceModule;
  
  console.log('\n--- Test: Coreference Resolution ---');
  
  // Simple test - resolve she -> Caroline
  const knownEntities = new Map([
    ['caroline', 'Caroline'],
    ['sarah', 'Sarah'],
  ]);
  
  const result = resolveCoreferences(
    'Caroline said she is interested in AI.',
    knownEntities
  );
  
  assert(result.resolutions.length > 0, 'Should find at least one resolution');
  assert(
    result.resolvedText.includes('Caroline') && !result.resolvedText.includes(' she '),
    'Should replace she with Caroline'
  );
}

// ============================================================================
// RUN ALL TESTS
// ============================================================================

async function runTests() {
  console.log('========================================');
  console.log('Multi-Hop Path Finding Tests');
  console.log('========================================');
  
  // Path finding tests
  runTest('Direct Path (1-hop)', testDirectPath);
  runTest('2-Hop Path', testTwoHopPath);
  runTest('3-Hop Path', testThreeHopPath);
  runTest('No Path Exists', testNoPath);
  runTest('Contradicted Relationship', testContradictedRelationship);
  runTest('Max Hops Limit', testMaxHopsLimit);
  runTest('Max Paths Limit', testMaxPathsLimit);
  runTest('Path Scoring', testPathScoring);
  runTest('Find Paths By Name', testFindPathsByName);
  runTest('Rank Paths', testRankPaths);
  
  // Coreference tests
  runTest('Coreference Resolution', testCoreferenceResolution);
  
  // Summary
  console.log('\n========================================');
  console.log(`Tests Passed: ${testsPassed}`);
  console.log(`Tests Failed: ${testsFailed}`);
  console.log('========================================');
  
  // Exit with error code if tests failed
  if (testsFailed > 0) {
    process.exit(1);
  }
}

runTests();
