#!/usr/bin/env node

import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const vendorCliPath = path.join(scriptDir, "vendor", "cli.mjs");

const child = spawn(process.execPath, [vendorCliPath, ...process.argv.slice(2)], {
  stdio: "inherit",
});

child.on("close", (code, signal) => {
  if (typeof code === "number") {
    process.exit(code);
    return;
  }
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(1);
});

child.on("error", (error) => {
  console.error(error instanceof Error ? error.message : "Failed to launch bundled KMind CLI.");
  process.exit(1);
});
