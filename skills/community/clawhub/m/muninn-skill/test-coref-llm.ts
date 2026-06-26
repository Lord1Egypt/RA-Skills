/**
 * Test Coreference Resolution with LLM
 * 
 * Tests the LLM-based coreference resolution
 */

import { 
  resolveCoreferences,
  resolveCoreferencesSimple,
  resolveEntity,
  addToEntityCache,
  clearEntityCache,
  type CoreferenceResult
} from './src/extractors/coreference.js';

console.log('\n🎯 Coreference Resolution - LLM Test Suite');
console.log('='.repeat(50));

// Clear and set up entity cache
clearEntityCache();
addToEntityCache('Phillip', ['Phillip', 'him', 'he', 'the CEO', 'the Program Manager'], 'person');
addToEntityCache('Caroline', ['Caroline', 'her', 'she', 'the PM', 'the Program Manager'], 'person');

async function testLLMResolution() {
  console.log('\n🧪 Test: LLM-Based Coreference Resolution');
  
  const tests = [
    'Phillip mentioned that he would meet with her next Tuesday.',
    'The Program Manager told him about the project.',
    'She said she would call him later.',
    'Phillip and Caroline went to the meeting. He spoke about his project.',
    'John talked to Mary. He told her about the new product launch.'
  ];
  
  for (const test of tests) {
    console.log(`\n📝 Input: "${test}"`);
    
    try {
      const result = await resolveCoreferences(test, [], true);
      console.log(`✅ Resolved: "${result.resolvedText}"`);
      console.log(`   Entity Map:`, Object.fromEntries(result.entityMap));
    } catch (error) {
      console.log(`❌ Error:`, error);
    }
  }
}

async function testSimpleComparison() {
  console.log('\n\n🧪 Test: Simple vs LLM Comparison');
  
  const test = 'Phillip mentioned that he would meet with her next Tuesday.';
  console.log(`\n📝 Input: "${test}"`);
  
  console.log('\n--- Simple Resolution ---');
  const simpleResult = resolveCoreferencesSimple(test);
  console.log(`✅ "${simpleResult.resolvedText}"`);
  
  console.log('\n--- LLM Resolution ---');
  const llmResult = await resolveCoreferences(test, [], true);
  console.log(`✅ "${llmResult.resolvedText}"`);
}

async function main() {
  await testLLMResolution();
  await testSimpleComparison();
  console.log('\n\n✅ Test Suite Complete!');
}

main().catch(console.error);
