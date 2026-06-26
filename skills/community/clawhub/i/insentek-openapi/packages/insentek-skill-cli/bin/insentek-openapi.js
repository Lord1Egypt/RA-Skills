#!/usr/bin/env node

import { runCli } from '../lib/cli.js';
import { argvHasJsonFlag, writeJsonError } from '../lib/output.js';

runCli(process.argv).catch((error) => {
  if (argvHasJsonFlag(process.argv)) {
    writeJsonError(error);
  } else {
    console.error(`\n✖ ${error.message}`);
  }
  process.exit(1);
});
