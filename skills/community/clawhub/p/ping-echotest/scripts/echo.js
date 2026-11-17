#!/usr/bin/env node
// Deterministic echo probe used as a smoke-test skill payload.
const input = process.argv.slice(2).join(" ").trim() || "hello";
process.stdout.write(`pong: ${input}\n`);
