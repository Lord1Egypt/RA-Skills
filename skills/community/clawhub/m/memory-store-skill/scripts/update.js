#!/usr/bin/env node
"use strict";

const { main: runInstaller } = require("./install.js");

function printHelp() {
  console.log(`
Memory Store Skill Updater

Usage:
  memory-store-update                  Sync detected existing installations
  memory-store-update --agent codex    Sync one or more installed platforms
  memory-store-update --target <path>  Sync an existing custom installation
  memory-store-update --all            Sync all detected existing installations
  memory-store-update --dry-run        Preview without changing files

This command copies files from the currently installed npm package. It does not
download or execute remote code, create new Agent installations, or modify memory data.

To update to the latest published package first:
  npm i memory-store-skill@latest
  npx memory-store-update

One-shot explicit update:
  npx --yes --package memory-store-skill@latest memory-store-install --update
`);
}

async function main(args = process.argv.slice(2)) {
  if (args.includes("--help") || args.includes("-h")) {
    printHelp();
    return;
  }
  console.log("Syncing from the currently installed memory-store-skill package...");
  await runInstaller(["--update", ...args]);
}

if (require.main === module) {
  main().catch((error) => {
    console.error(`Update failed: ${error.message}`);
    process.exitCode = 1;
  });
}

module.exports = { main };
