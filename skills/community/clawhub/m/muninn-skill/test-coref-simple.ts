/**
 * Simple Coreference Resolution Test (no LLM dependency)
 * 
 * Tests the pattern-based coreference resolution
 */

import { 
  resolveCoreferencesSimple,
  resolveEntity,
  addToEntityCache,
  clearEntityCache,
  type CoreferenceResult
} from './src/extractors/coreference.js';

console.log('\n🎯 Coreference Resolution - Simple Test Suite');
console.log('='.repeat(50));

// Test 1: Basic resolution
console.log('\n🧪 Test 1: Basic Coreference Resolution');
clearEntityCache();
addToEntityCache('Phillip', ['Phillip', 'him', 'he', 'the CEO', 'the Program Manager'], 'person');
addToEntityCache('Caroline', ['Caroline', 'her', 'she', 'the PM'], 'person');

const testInput1 = 'Phillip mentioned that he would meet with her next Tuesday.';
console.log(`\n📝 Input: "${testInput1}"`);

const result1 = resolveCoreferencesSimple(testInput1);
console.log(`✅ Resolved: "${result1.resolvedText}"`);
console.log(`   Entity Map:`, Object.fromEntries(result1.entityMap));

// Test 2: With multiple entities in context
console.log('\n\n🧪 Test 2: Multiple Entities');
const testInput2 = 'Phillip and Caroline went to the meeting. He spoke about his project.';
console.log(`📝 Input: "${testInput2}"`);

const result2 = resolveCoreferencesSimple(testInput2);
console.log(`✅ Resolved: "${result2.resolvedText}"`);
console.log(`   Entity Map:`, Object.fromEntries(result2.entityMap));

// Test 3: Test entity cache resolution
console.log('\n\n🧪 Test 3: Entity Cache Resolution');
console.log(`  "him" -> ${resolveEntity('him')}`);
console.log(`  "her" -> ${resolveEntity('her')}`);
console.log(`  "the CEO" -> ${resolveEntity('the CEO')}`);
console.log(`  "the PM" -> ${resolveEntity('the PM')}`);
console.log(`  "unknown" -> ${resolveEntity('unknown')}`);

// Test 4: Different sentence patterns
console.log('\n\n🧪 Test 4: Different Sentence Patterns');
const tests = [
  'He told her about the project.',
  'The Program Manager said he would call.',
  'She met with the PM yesterday.',
  'Phillip called Caroline. She answered.'
];

for (const test of tests) {
  const result = resolveCoreferencesSimple(test);
  console.log(`\n📝 "${test}"`);
  console.log(`✅ "${result.resolvedText}"`);
}

console.log('\n\n✅ Test Suite Complete!');
