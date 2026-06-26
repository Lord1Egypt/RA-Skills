#!/usr/bin/env node
/* eslint-disable */
const { runOpenClawSkill } = require('../dist/index.cjs');

runOpenClawSkill().then(
  () => process.exit(0),
  (err) => {
    process.stderr.write(`fatal: ${err && err.stack ? err.stack : String(err)}\n`);
    process.exit(1);
  },
);
