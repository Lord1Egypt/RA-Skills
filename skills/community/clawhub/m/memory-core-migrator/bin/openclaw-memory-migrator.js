#!/usr/bin/env node

import { main } from "../lib/cli.js";
import { formatMigratorError, migratorError } from "../lib/errors.js";

const major = Number(process.versions.node.split(".", 1)[0]);
if (major < 22) {
  process.stderr.write(formatMigratorError(migratorError(
    "NODE_VERSION_UNSUPPORTED",
    `openclaw-memory-migrator requires Node.js >=22; current version is ${process.versions.node}`,
    { details: { required_major: 22, current: process.versions.node } },
  ), { json: process.argv.includes("--json-errors") }));
  process.exitCode = 2;
} else {
  process.exitCode = await main();
}
