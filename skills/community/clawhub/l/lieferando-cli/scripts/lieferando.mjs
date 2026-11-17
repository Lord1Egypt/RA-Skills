#!/usr/bin/env node
import { run } from './src/cli.js';

// Set exitCode instead of calling process.exit(): exit() tears the process
// down before large stdout payloads (>64 KiB) finish flushing into a pipe,
// which truncates JSON for consumers like `cli | jq` or execFile captures.
process.exitCode = await run(process.argv.slice(2));
