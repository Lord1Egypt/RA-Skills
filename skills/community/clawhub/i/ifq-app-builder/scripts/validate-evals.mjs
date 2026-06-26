#!/usr/bin/env node
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateEvalSuite } from './lib/evals-validator.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const failures = validateEvalSuite(root);

if (failures.length) {
  console.error('eval validation failed:');
  for (const failure of failures) console.error(`  - ${failure}`);
  process.exit(1);
}

console.log('✓ evals: 12 platform scenarios and first-run evidence are valid');
