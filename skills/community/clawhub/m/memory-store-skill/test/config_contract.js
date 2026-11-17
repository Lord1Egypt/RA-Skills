#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const CLI = path.join(ROOT, "scripts", "memory_cli.js");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "memory-store-config-contract-"));
const tempHome = path.join(tempRoot, "home");
const workspace = path.join(tempRoot, "workspace");
fs.mkdirSync(tempHome, { recursive: true });
fs.mkdirSync(workspace, { recursive: true });

const env = { ...process.env, HOME: tempHome, USERPROFILE: tempHome };

function run(args, expectedStatus = 0) {
  const result = spawnSync(process.execPath, [CLI, ...args], {
    cwd: workspace,
    env,
    encoding: "utf8",
  });
  const output = `${result.stdout || ""}${result.stderr || ""}`;
  assert.strictEqual(result.status, expectedStatus, output);
  return result.stdout || "";
}

function json(args) {
  return JSON.parse(run([...args, "--stdout"]));
}

try {
  const defaults = json(["config", "show"]);
  assert.strictEqual(defaults.profile, "explicit");
  assert.strictEqual(defaults.source, "default");
  assert.strictEqual(defaults.auto_store, "explicit");

  run(["config", "set", "--profile", "balanced", "--scope", "global"]);
  const globalConfig = json(["config", "show", "--scope", "global"]);
  assert.strictEqual(globalConfig.profile, "balanced");
  assert.strictEqual(globalConfig.max_automatic_memories_per_conversation, 3);

  run(["config", "set", "--profile", "off", "--scope", "workspace"]);
  const effective = json(["config", "show"]);
  assert.strictEqual(effective.profile, "off");
  assert.strictEqual(effective.source, "workspace");

  const workspaceStore = path.join(workspace, ".agents", "memory-store");
  assert.strictEqual(
    run([
      "store", "--type", "decision", "--title", "Blocked automatic write",
      "--summary", "This automatic write must be rejected", "--scope", "workspace",
      "--store-path", workspaceStore, "--intent", "automatic", "--source-conv-id", "conv-1",
    ], 1),
    ""
  );
  run([
    "search", "--query", "anything", "--scope", "workspace",
    "--store-path", workspaceStore, "--intent", "automatic", "--stdout",
  ], 1);

  run(["config", "set", "--profile", "balanced", "--scope", "workspace"]);
  run([
    "store", "--type", "decision", "--title", "Allowed automatic write",
    "--summary", "Balanced mode permits durable decisions", "--scope", "workspace",
    "--intent", "automatic", "--source-conv-id", "conv-1",
  ]);
  run([
    "store", "--type", "fact", "--title", "Blocked broad fact",
    "--summary", "Balanced mode does not automatically retain broad facts", "--scope", "workspace",
    "--intent", "automatic", "--source-conv-id", "conv-1",
  ], 1);
  for (const suffix of ["two", "three"]) {
    run([
      "store", "--type", "decision", "--title", `Automatic ${suffix}`,
      "--summary", "Balanced mode permits up to three automatic memories", "--scope", "workspace",
      "--intent", "automatic", "--source-conv-id", "conv-1",
    ]);
  }
  run([
    "store", "--type", "decision", "--title", "Blocked fourth automatic write",
    "--summary", "Balanced mode must enforce its per-conversation limit", "--scope", "workspace",
    "--intent", "automatic", "--source-conv-id", "conv-1",
  ], 1);
  const automaticSearch = json([
    "search", "--query", "Allowed", "--scope", "workspace", "--intent", "automatic",
  ]);
  assert.ok(automaticSearch.length >= 1);

  run(["config", "reset", "--scope", "workspace"]);
  assert.strictEqual(json(["config", "show"]).profile, "balanced");

  console.log("Memory policy configuration contract tests passed.");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
