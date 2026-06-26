#!/usr/bin/env node

import { main } from '../src/index.js';

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
