#!/usr/bin/env node
/**
 * Quick security smoke test for spawn-with-fallback.
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const testModule = require('../src/spawn-with-fallback');

console.log('\n── Quick Security Validation ──');

try {
  testModule.validateFilePath('../../../etc/passwd');
  console.log('  ❌ FAIL: Path traversal should be blocked');
} catch (err) {
  if (err.message.includes('Path traversal')) {
    console.log('  ✅ Blocks path traversal attempts');
  } else {
    console.log(`  ⚠️  Unexpected error: ${err.message}`);
  }
}

try {
  testModule.validateFilePath('/etc/passwd');
  console.log('  ❌ FAIL: System directory access should be blocked');
} catch (err) {
  if (err.message.includes('system path')) {
    console.log('  ✅ Blocks system directory access');
  } else {
    console.log(`  ⚠️  Unexpected error: ${err.message}`);
  }
}

const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'paperclip-resilience-quick-'));
const testFile = path.join(tempDir, 'security-test.txt');
fs.writeFileSync(testFile, 'test content');

try {
  testModule.validateFilePath(testFile);
  console.log('  ✅ Allows valid temp file access');
} catch (err) {
  console.log(`  ❌ FAIL: Should allow valid temp files: ${err.message}`);
}

try {
  testModule.validateSpawnArgs('invalid-mode', null);
  console.log('  ❌ FAIL: Invalid mode should be blocked');
} catch (err) {
  if (err.message.includes('Invalid mode')) {
    console.log('  ✅ Blocks invalid spawn modes');
  } else {
    console.log(`  ⚠️  Unexpected error: ${err.message}`);
  }
}

try {
  testModule.validateModelInput('openrouter/z-ai/glm-4.5-air:free');
  console.log('  ✅ Allows valid model names with provider suffixes');
} catch (err) {
  console.log(`  ❌ FAIL: Valid model should be allowed: ${err.message}`);
}

try {
  testModule.validateModelInput('invalid/model/with/../path');
  console.log('  ❌ FAIL: Invalid model path should be blocked');
} catch (err) {
  if (err.message.includes('path traversal')) {
    console.log('  ✅ Blocks invalid model path traversal segments');
  } else {
    console.log(`  ⚠️  Unexpected error: ${err.message}`);
  }
}

fs.rmSync(tempDir, { recursive: true, force: true });

console.log('\n✅ Security validation complete');
console.log('Note: Run node tests/test-security.js for the full suite');
