#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const pkg = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));

assert.ok(
  !Object.prototype.hasOwnProperty.call(pkg.scripts || {}, "postinstall"),
  "npm install must not run a package lifecycle installer"
);
assert.ok(
  !(pkg.files || []).includes("scripts/postinstall.js"),
  "the published package must not include an automatic postinstall script"
);
assert.ok((pkg.files || []).includes("SECURITY.md"), "the published package must disclose its security model");

const productionScripts = [
  pkg.bin["memory-store"],
  pkg.bin["memory-store-install"],
  pkg.bin["memory-store-update"],
].map((relativePath) => path.join(ROOT, relativePath));

for (const scriptPath of productionScripts) {
  const source = fs.readFileSync(scriptPath, "utf8");
  assert.doesNotMatch(
    source,
    /(?:node:)?child_process|\b(?:exec|execFile|execSync|execFileSync|spawn|spawnSync)\s*\(/,
    `${path.relative(ROOT, scriptPath)} must not execute child processes`
  );
}

console.log("Security contract passed: install is explicit and production scripts do not spawn processes.");
