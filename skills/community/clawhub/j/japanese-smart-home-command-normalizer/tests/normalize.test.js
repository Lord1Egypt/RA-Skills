import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { classify } from '../lib/normalize.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixturesPath = path.resolve(__dirname, '../fixtures/samples.json');
const fixtures = JSON.parse(fs.readFileSync(fixturesPath, 'utf8'));

for (const fixture of fixtures) {
  test(`classify: ${fixture.text}`, () => {
    const result = classify(fixture.text);
    assert.equal(result.intent, fixture.intent);
    assert.equal(result.needsConfirmation, fixture.needsConfirmation);
  });
}
