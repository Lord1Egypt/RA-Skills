import { serialize, deserialize, test, OmegaPacket } from './omega-notation';

// Run built-in round-trip test
console.log('--- Round-Trip Test ---');
const passed = test();

// Token comparison test
console.log('\n--- Token Cost Comparison ---');
const verboseJSON = JSON.stringify({
  type: 'eval',
  confidence: 0.95,
  directive: 'proceed',
  category: 'finance',
  timestamp: '2026-03-20T12:00:00Z',
  source: 'monitoring-agent',
  details: 'Evaluation complete with high confidence. Proceeding with the recommended action based on current analysis.',
}, null, 2);

const omegaEquiv = serialize({
  version: 1,
  dict: 'auto',
  messages: [{
    type: 'eval',
    confidence: 0.95,
    directive: 'proceed',
    tags: [{ cat: 'cat', val: 'finance' }, { cat: 'src', val: 'monitor' }],
  }],
});

console.log(`Verbose JSON: ${verboseJSON.length} chars`);
console.log(`Omega:        ${omegaEquiv.length} chars`);
console.log(`Reduction:    ${((1 - omegaEquiv.length / verboseJSON.length) * 100).toFixed(1)}%`);

// Multi-message test
console.log('\n--- Multi-Message Test ---');
const multi: OmegaPacket = {
  version: 1,
  dict: 'auto',
  messages: [
    { type: 'eval', confidence: 0.92, directive: 'hold', tags: [{ cat: 'cat', val: 'trading' }] },
    { type: 'decision', name: 'btc-position', fitness: 0.87, deltaFitness: -0.05 },
    { type: 'tier', fromTier: 1, toTier: 2, reason: 'regime-shift' },
  ],
};
const multiSerialized = serialize(multi);
const multiDeserialized = deserialize(multiSerialized);
console.log(multiSerialized);
console.log(`\nMessages in: ${multi.messages.length}, Messages out: ${multiDeserialized.messages.length}`);
console.log(multiDeserialized.messages.length === multi.messages.length ? '✅ Multi-message pass' : '❌ Multi-message FAIL');

// Final
console.log(`\n${'='.repeat(40)}`);
console.log(passed ? '✅ ALL TESTS PASSED' : '❌ TESTS FAILED');
