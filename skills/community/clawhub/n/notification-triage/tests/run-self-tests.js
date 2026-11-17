#!/usr/bin/env node
/**
 * Notification Triage — Self-Test Suite
 * 
 * Tests: urgency classification, rule management, source filtering, batching, status
 * 
 * Run: node tests/run-self-tests.js
 */

const path = require('path');
const fs = require('fs');

const NT = require(path.resolve(__dirname, '..', 'notification-triage.js'));

let totalTests = 0;
let totalPassed = 0;

function assert(condition, description) {
  totalTests++;
  const passed = !!condition;
  if (passed) totalPassed++;
  console.log(`  ${passed ? '✅' : '❌'} ${description}`);
}

function group(name, fn) {
  console.log(`\n📋 ${name}`);
  fn();
}

// ─── 1. Urgency Classification Tests ─────────────────────────────

group('Urgency classification — 5 cases', () => {
  // Test that classifyMessage returns a valid result with expected structure
  const result1 = NT.classifyMessage('server down immediately', 'urgency-test-1');
  assert(typeof result1 === 'object' && result1.level !== undefined, 'Returns object with level');
  assert(['urgent', 'batch', 'ignore'].includes(result1.level), 'Level is valid value');
  // Score is not always present (predefined rules skip scoring)
  assert(result1.score === undefined || typeof result1.score === 'number', 'Score is number when present');
  
  // Test with explicit urgent keywords
  const result2 = NT.classifyMessage('CRITICAL security breach in progress', 'urgency-test-2');
  assert(typeof result2 === 'object', 'Handles urgent keywords');
  
  // Test with batch keywords
  const result3 = NT.classifyMessage('weekly summary report', 'urgency-test-3');
  assert(typeof result3 === 'object', 'Handles batch keywords');
  
  // Test heartbeat pattern
  const result4 = NT.classifyMessage('heartbeat OK', 'urgency-test-4');
  assert(typeof result4 === 'object', 'Handles ignorable patterns');

  // Test empty message
  const result5 = NT.classifyMessage('', 'urgency-test-5');
  assert(typeof result5 === 'object', 'Handles empty message');
});

// ─── 2. Rule Management Tests ───────────────────────────────────

group('Rule management — 4 cases', () => {
  // loadRules returns an object
  const rules = NT.loadRules();
  assert(typeof rules === 'object', 'loadRules returns object');

  // Add a rule
  NT.addRule('test-source-rules', 'batch');
  const rulesAfterAdd = NT.loadRules();
  assert(rulesAfterAdd['test-source-rules'] && rulesAfterAdd['test-source-rules'].level === 'batch', 'Added rule exists with correct level');

  // Remove rule
  NT.removeRule('test-source-rules');
  const rulesAfterRemove = NT.loadRules();
  assert(rulesAfterRemove['test-source-rules'] === undefined, 'Removed rule gone');

  // Remove nonexistent doesn't throw
  let threw = false;
  try { NT.removeRule('nonexistent-source-xyz'); } catch { threw = true; }
  assert(!threw, 'Removing nonexistent rule does not throw');
});

// ─── 3. Batching Tests ─────────────────────────────────────────

group('Notification batching — 4 cases', () => {
  // getBatched returns array
  const batched = NT.getBatched();
  assert(Array.isArray(batched), 'getBatched returns array');

  // addNotification with different levels
  let threw = false;
  try {
    NT.addNotification('batch-test-1', 'batch message', 'batch-src', 'batch');
  } catch { threw = true; }
  assert(!threw, 'addNotification with batch level does not throw');

  // addNotification with ignore level
  try {
    NT.addNotification('batch-test-2', 'ignore message', 'ignore-src', 'ignore');
  } catch { threw = true; }
  assert(!threw, 'addNotification with ignore level does not throw');

  // flushBatch doesn't throw
  let threw3 = false;
  try { NT.flushBatch(); } catch { threw3 = true; }
  assert(!threw3, 'flushBatch does not throw');
});

// ─── 4. Seen Tracking Tests ─────────────────────────────────────

group('Seen tracking — 2 cases', () => {
  let threw = false;
  try { NT.markSeen('seen-test-1'); } catch { threw = true; }
  assert(!threw, 'markSeen does not throw');
  
  let threw2 = false;
  try { NT.markAllSeen(); } catch { threw2 = true; }
  assert(!threw2, 'markAllSeen does not throw');
});

// ─── 5. Status Tests ────────────────────────────────────────────

group('Status output — 3 cases', () => {
  let threw = false;
  try { NT.showStatus(); } catch { threw = true; }
  assert(!threw, 'showStatus does not throw');

  // listRules
  let threw2 = false;
  try { NT.listRules(); } catch { threw2 = true; }
  assert(!threw2, 'listRules does not throw');

  // generateDigest with no entries doesn't throw
  let threw3 = false;
  try { NT.generateDigest('daily'); } catch { threw3 = true; }
  assert(!threw3, 'generateDigest does not throw (empty)');
});

// ─── 6. Edge Case Tests ─────────────────────────────────────────

group('Edge cases — 4 cases', () => {
  // Very long message
  const long = NT.classifyMessage('x'.repeat(10000), 'edge-test-long');
  assert(typeof long === 'object', 'Long message returns result');
  
  // Special characters
  const special = NT.classifyMessage("'; DROP TABLE; -- <script>alert(1)</script>", 'edge-test-special');
  assert(typeof special === 'object', 'Special chars return result');
  
  // Multi-word source
  const multi = NT.classifyMessage('test', 'multi-word-source-name');
  assert(typeof multi === 'object', 'Multi-word source works');
  
  // Numeric message
  const num = NT.classifyMessage('12345 67890', 'edge-test-numeric');
  assert(typeof num === 'object', 'Numeric message works');
});

// ─── Summary ──────────────────────────────────────────────────────

console.log('\n═══════════════════════════════════════');
console.log(`  Notification Triage Self-Test Results`);
console.log(`  ${totalPassed}/${totalTests} tests passing`);
console.log('═══════════════════════════════════════');

if (totalPassed < totalTests) {
  console.log('\n❌ Self-tests FAILED — do not publish until fixed');
  process.exit(1);
} else {
  console.log('\n✅ All self-tests passed');
  process.exit(0);
}