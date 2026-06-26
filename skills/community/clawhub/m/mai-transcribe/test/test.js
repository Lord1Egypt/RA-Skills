const assert = require('assert');
const { extractTranscript, parseArgs } = require('../scripts/common');

assert.equal(
  extractTranscript({ combinedPhrases: [{ text: 'hello' }, { text: 'world' }] }),
  'hello\nworld'
);

assert.equal(
  extractTranscript({ phrases: [{ text: 'fallback phrase' }] }),
  'fallback phrase'
);

assert.equal(
  extractTranscript({ text: 'plain text' }),
  'plain text'
);

assert.equal(
  extractTranscript({}),
  ''
);

const args = parseArgs(['file.wav', '--json', '--language=en-GB', '--out', '/tmp/x.txt']);
assert.equal(args._[0], 'file.wav');
assert.equal(args.json, true);
assert.equal(args.language, 'en-GB');
assert.equal(args.out, '/tmp/x.txt');

console.log('ok');
