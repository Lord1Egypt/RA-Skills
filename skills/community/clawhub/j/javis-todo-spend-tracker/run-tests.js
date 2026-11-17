#!/usr/bin/env node
// `npm test [-- <name>...]`: runs every test/*.test.js, or only test/<name>.test.js
// for each name given, so the test plan's `npm test -- ledger`, `-- ledger-shuffle`
// and `-- chat` resolve to files (plain `node --test ledger` treats the name as a
// path and fails with "Could not find"). R0-8.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const TEST_DIR = path.join(__dirname, 'test');

function resolveTargets(args) {
  if (!args.length) {
    return fs.readdirSync(TEST_DIR).filter((f) => f.endsWith('.test.js')).sort().map((f) => path.join('test', f));
  }
  return args.map((a) => {
    if (a.startsWith('-')) return a;
    const named = path.join('test', `${a}.test.js`);
    if (fs.existsSync(path.join(__dirname, named))) return named;
    return a;
  });
}

module.exports = { resolveTargets };

if (require.main === module) {
  const r = spawnSync(process.execPath, ['--test', ...resolveTargets(process.argv.slice(2))],
    { cwd: __dirname, stdio: 'inherit' });
  process.exit(r.status == null ? 1 : r.status);
}
