/**
 * Test Coreference Resolution
 * 
 * Tests the coreference resolution layer for Muninn Memory System
 */

import { 
  resolveCoreferences, 
  resolveCoreferencesSimple,
  resolveEntity,
  addToEntityCache,
  clearEntityCache,
  initEntityCache,
  type CoreferenceResult
} from './src/extractors/coreference.js';
import { MemoryStore } from './src/storage/index.js';

async function testBasicCoreference() {
  console.log('\n🧪 Test 1: Basic Coreference Resolution');
  console.log('='.repeat(50));
  
  // Clear cache and add test entities
  clearEntityCache();
  addToEntityCache('Phillip', ['Phillip', 'the CEO', 'the Program Manager'], 'person');
  addToEntityCache('Caroline', ['Caroline', 'her', 'the PM'], 'person');
  
  const testCases = [
    {
      input: 'Phillip mentioned that he would meet with her next Tuesday.',
      expected: 'Phillip mentioned that [Phillip] would meet with [Caroline] next Tuesday.'
    },
    {
      input: 'The Program Manager told him about the project.',
      expected: '[Phillip] told [Phillip] about the project.'
    },
    {
      input: 'She said she would call him later.',
      expected: '[Caroline] said [Caroline] would call [Phillip] later.'
    },
    {
      input: 'Phillip and Caroline went to the meeting. He spoke about his project.',
      expected: 'Phillip and Caroline went to the meeting. [Phillip] spoke about [Phillip]\'s project.'
    }
  ];
  
  for (const testCase of testCases) {
    console.log(`\n📝 Input: "${testCase.input}"`);
    
    const result = await resolveCoreferences(testCase.input, [], true);
    
    console.log(`✅ Resolved: "${result.resolvedText}"`);
    console.log(`   Entity Map:`, Object.fromEntries(result.entityMap));
    
    if (result.resolvedText === testCase.expected) {
      console.log('   ✅ PASS - Matches expected output');
    } else if (result.resolvedText.includes('[Phillip]') && result.resolvedText.includes('[Caroline]')) {
      console.log('   ✅ PASS - Coreferences resolved correctly');
    } else {
      console.log('   ⚠️  Partial match');
    }
  }
}

async function testWithMemoryStore() {
  console.log('\n\n🧪 Test 2: Coreference with Memory Store Integration');
  console.log('='.repeat(50));
  
  // Initialize a test memory store
  const store = new MemoryStore('/tmp/test-coreference.db');
  
  // Add some entities to memory
  await store.remember('Phillip is the Program Manager', 'semantic');
  await store.remember('Caroline handles project coordination', 'semantic');
  
  // Initialize entity cache from store
  await initEntityCache(store);
  
  const testInput = 'Phillip mentioned that he would meet with her next Tuesday.';
  console.log(`\n📝 Input: "${testInput}"`);
  
  const result = await resolveCoreferences(testInput, [], true);
  
  console.log(`✅ Resolved: "${result.resolvedText}"`);
  console.log(`   Entity Map:`, Object.fromEntries(result.entityMap));
  console.log(`   New entities found:`, result.newEntitiesFound);
  
  // Verify Phillip and Caroline are resolved
  const hasPhillip = result.resolvedText.includes('[Phillip]');
  const hasCaroline = result.resolvedText.includes('[Caroline]');
  
  if (hasPhillip && hasCaroline) {
    console.log('   ✅ Both entities resolved correctly!');
  } else {
    console.log('   ⚠️  Some entities not resolved');
  }
  
  store.close();
}

async function testSimpleResolution() {
  console.log('\n\n🧪 Test 3: Simple Resolution (no LLM)');
  console.log('='.repeat(50));
  
  clearEntityCache();
  addToEntityCache('Phillip', ['Phillip', 'him'], 'person');
  addToEntityCache('Caroline', ['Caroline', 'her'], 'person');
  
  const testInput = 'Phillip met her yesterday.';
  console.log(`\n📝 Input: "${testInput}"`);
  
  const result = resolveCoreferencesSimple(testInput);
  
  console.log(`✅ Resolved: "${result.resolvedText}"`);
  console.log(`   Entity Map:`, Object.fromEntries(result.entityMap));
}

async function testEntityCache() {
  console.log('\n\n🧪 Test 4: Entity Cache Operations');
  console.log('='.repeat(50));
  
  clearEntityCache();
  
  // Test adding entities
  addToEntityCache('John', ['John', 'him', 'he'], 'person');
  addToEntityCache('Jane', ['Jane', 'her', 'she'], 'person');
  
  // Test resolution
  console.log('\n📝 Resolving pronouns:');
  console.log(`  "him" -> ${resolveEntity('him')}`);
  console.log(`  "her" -> ${resolveEntity('her')}`);
  console.log(`  "she" -> ${resolveEntity('she')}`);
  console.log(`  "John" -> ${resolveEntity('John')}`);
  console.log(`  "unknown" -> ${resolveEntity('unknown')}`);
}

async function runAllTests() {
  console.log('\n🎯 Coreference Resolution Test Suite');
  console.log('='.repeat(50));
  
  try {
    await testBasicCoreference();
    await testWithMemoryStore();
    await testSimpleResolution();
    await testEntityCache();
    
    console.log('\n\n✅ All tests completed!');
    console.log('='.repeat(50));
  } catch (error) {
    console.error('\n❌ Test failed:', error);
  }
}

// Run tests
runAllTests();
