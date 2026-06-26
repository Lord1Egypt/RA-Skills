"use strict";
/**
 * Simple Coreference Resolution Test (no LLM dependency)
 *
 * Tests the pattern-based coreference resolution
 */
Object.defineProperty(exports, "__esModule", { value: true });
var coreference_js_1 = require("./src/extractors/coreference.js");
console.log('\n🎯 Coreference Resolution - Simple Test Suite');
console.log('='.repeat(50));
// Test 1: Basic resolution
console.log('\n🧪 Test 1: Basic Coreference Resolution');
(0, coreference_js_1.clearEntityCache)();
(0, coreference_js_1.addToEntityCache)('Phillip', ['Phillip', 'him', 'he', 'the CEO', 'the Program Manager'], 'person');
(0, coreference_js_1.addToEntityCache)('Caroline', ['Caroline', 'her', 'she', 'the PM'], 'person');
var testInput1 = 'Phillip mentioned that he would meet with her next Tuesday.';
console.log("\n\uD83D\uDCDD Input: \"".concat(testInput1, "\""));
var result1 = (0, coreference_js_1.resolveCoreferencesSimple)(testInput1);
console.log("\u2705 Resolved: \"".concat(result1.resolvedText, "\""));
console.log("   Entity Map:", Object.fromEntries(result1.entityMap));
// Test 2: With multiple entities in context
console.log('\n\n🧪 Test 2: Multiple Entities');
var testInput2 = 'Phillip and Caroline went to the meeting. He spoke about his project.';
console.log("\uD83D\uDCDD Input: \"".concat(testInput2, "\""));
var result2 = (0, coreference_js_1.resolveCoreferencesSimple)(testInput2);
console.log("\u2705 Resolved: \"".concat(result2.resolvedText, "\""));
console.log("   Entity Map:", Object.fromEntries(result2.entityMap));
// Test 3: Test entity cache resolution
console.log('\n\n🧪 Test 3: Entity Cache Resolution');
console.log("  \"him\" -> ".concat((0, coreference_js_1.resolveEntity)('him')));
console.log("  \"her\" -> ".concat((0, coreference_js_1.resolveEntity)('her')));
console.log("  \"the CEO\" -> ".concat((0, coreference_js_1.resolveEntity)('the CEO')));
console.log("  \"the PM\" -> ".concat((0, coreference_js_1.resolveEntity)('the PM')));
console.log("  \"unknown\" -> ".concat((0, coreference_js_1.resolveEntity)('unknown')));
// Test 4: Different sentence patterns
console.log('\n\n🧪 Test 4: Different Sentence Patterns');
var tests = [
    'He told her about the project.',
    'The Program Manager said he would call.',
    'She met with the PM yesterday.',
    'Phillip called Caroline. She answered.'
];
for (var _i = 0, tests_1 = tests; _i < tests_1.length; _i++) {
    var test_1 = tests_1[_i];
    var result = (0, coreference_js_1.resolveCoreferencesSimple)(test_1);
    console.log("\n\uD83D\uDCDD \"".concat(test_1, "\""));
    console.log("\u2705 \"".concat(result.resolvedText, "\""));
}
console.log('\n\n✅ Test Suite Complete!');
