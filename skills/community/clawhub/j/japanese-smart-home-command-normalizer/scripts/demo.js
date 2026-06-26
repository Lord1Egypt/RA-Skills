#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { classify } from '../lib/normalize.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixturesPath = path.resolve(__dirname, '../fixtures/samples.json');
const arg = process.argv.slice(2).join(' ').trim();

if (arg) {
  console.log(JSON.stringify(classify(arg), null, 2));
  process.exit(0);
}

const samples = JSON.parse(fs.readFileSync(fixturesPath, 'utf8'));
for (const sample of samples) {
  console.log(`\n# ${sample.text}`);
  console.log(JSON.stringify(classify(sample.text), null, 2));
}
