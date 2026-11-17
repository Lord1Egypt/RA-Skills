#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const workflowPath = path.join(root, ".github", "workflows", "publish.yml");
assert.ok(fs.existsSync(workflowPath), "publish.yml must exist");

const workflow = fs.readFileSync(workflowPath, "utf8");
assert.match(workflow, /release:\s*\r?\n\s+types:\s*\[published\]/);
assert.match(workflow, /contents:\s*read/);
assert.match(workflow, /id-token:\s*write/);
assert.match(workflow, /uses:\s*actions\/checkout@v6/);
assert.match(workflow, /uses:\s*actions\/setup-node@v6/);
assert.match(workflow, /node-version:\s*["']24["']/);
assert.match(workflow, /registry-url:\s*["']https:\/\/registry\.npmjs\.org["']/);
assert.match(workflow, /package-manager-cache:\s*false/);
assert.match(workflow, /GITHUB_REF_NAME/);
assert.match(workflow, /npm ci --ignore-scripts/);
assert.match(workflow, /npm test/);
assert.match(workflow, /run:\s*npm publish(?:\s|$)/m);
assert.doesNotMatch(workflow, /NPM_TOKEN|NODE_AUTH_TOKEN/);

const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
assert.strictEqual(pkg.publishConfig.access, "public");
assert.strictEqual(pkg.repository.url, "git+https://github.com/Revolves/memory-store-skill.git");

console.log("Release workflow contract tests passed.");
