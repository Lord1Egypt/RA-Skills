#!/usr/bin/env node

/**
 * Test runner script for heartbeat-cron skill
 * 
 * Usage:
 *   node run-tests.js           # Run all tests
 *   node run-tests.js --unit    # Run unit tests only
 *   node run-tests.js --integration  # Run integration tests only
 *   node run-tests.js --e2e     # Run e2e tests only
 *   node run-tests.js --coverage  # Run with coverage
 */

import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
const jestPath = join(__dirname, 'node_modules/jest/bin/jest.js');

let command = 'node';
let jestArgs = [];

// Check if node_modules exists, if not install dependencies
try {
  execSync('node --version', { stdio: 'pipe' });
} catch (error) {
  console.error('Node.js is required to run tests');
  process.exit(1);
}

// Build jest command
jestArgs.push(jestPath);

if (args.includes('--unit')) {
  jestArgs.push('tests/unit');
} else if (args.includes('--integration')) {
  jestArgs.push('tests/integration');
} else if (args.includes('--e2e')) {
  jestArgs.push('tests/e2e');
}

if (args.includes('--coverage')) {
  jestArgs.push('--coverage');
  jestArgs.push('--coverageDirectory=coverage');
  jestArgs.push('--coverageReporters=text');
  jestArgs.push('--coverageReporters=text-summary');
  jestArgs.push('--coverageReporters=html');
}

if (args.includes('--verbose') || args.includes('-v')) {
  jestArgs.push('--verbose');
}

if (args.includes('--watch') || args.includes('-w')) {
  jestArgs.push('--watch');
}

// Add any remaining args
const remainingArgs = args.filter(
  arg => !['--unit', '--integration', '--e2e', '--coverage', '--verbose', '-v', '--watch', '-w'].includes(arg)
);
jestArgs.push(...remainingArgs);

console.log('Running tests...\n');
console.log(`Command: ${command} ${jestArgs.join(' ')}\n`);

try {
  execSync(`${command} ${jestArgs.join(' ')}`, {
    stdio: 'inherit',
    cwd: __dirname
  });
  
  console.log('\n✅ Tests completed successfully!');
} catch (error) {
  console.error('\n❌ Tests failed!');
  process.exit(1);
}
