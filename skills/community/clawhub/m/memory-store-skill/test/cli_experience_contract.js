#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const CLI = path.join(ROOT, "scripts", "memory_cli.js");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "memory-store-cli-experience-"));
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
    timeout: 5000,
  });
  const output = `${result.stdout || ""}${result.stderr || ""}`;
  assert.notStrictEqual(result.error?.code, "ETIMEDOUT", "CLI must never wait in a non-TTY environment");
  assert.strictEqual(result.status, expectedStatus, output);
  return output;
}

async function test() {
try {
  const compactHelp = run([]);
  assert.ok(compactHelp.trim().split(/\r?\n/).length <= 10, "default help must stay within 10 lines");
  assert.match(compactHelp, /remember/);
  assert.match(compactHelp, /recall/);
  assert.doesNotMatch(compactHelp, /\bcompress\b/);

  const advancedHelp = run(["help", "--advanced"]);
  assert.match(advancedHelp, /store search recall list update delete merge archive/);
  assert.match(advancedHelp, /compress migrate/);

  const initialMode = JSON.parse(run(["mode", "--json"]));
  assert.strictEqual(initialMode.profile, "explicit");
  run(["mode", "balanced", "--global", "--json"]);
  assert.strictEqual(JSON.parse(run(["mode", "--json"])).profile, "balanced");
  run(["mode", "explicit", "--workspace", "--json"]);
  assert.strictEqual(JSON.parse(run(["mode", "--json"])).profile, "explicit");

  const remembered = run([
    "remember", "decision", "Database choice", "Use SQLite for the local single-user workflow",
    "--workspace",
  ]);
  const memoryId = remembered.match(/\[(mem_[^\]]+)\]/)?.[1];
  assert.ok(memoryId, remembered);
  const searchResults = JSON.parse(run(["recall", "Database choice", "--json"]));
  assert.strictEqual(searchResults[0].id, memoryId);
  const recalled = JSON.parse(run(["recall", memoryId, "--json"]));
  assert.strictEqual(recalled.title, "Database choice");

  const status = JSON.parse(run(["status", "--json"]));
  assert.strictEqual(status.profile.profile, "explicit");
  assert.strictEqual(status.memories.total, 1);
  assert.ok(status.paths.global);
  assert.ok(status.paths.workspace);

  const preview = JSON.parse(run(["maintain", "--json"]));
  assert.strictEqual(preview.applied, false);
  assert.ok(Number.isInteger(preview.candidates));

  const setupTarget = path.join(tempRoot, "setup-target");
  assert.match(run(["setup"], 1), /requires --agent, --target, or --all/);
  assert.match(run(["setup", "--list"]), /No AI agent platforms detected|Detected \d+ AI agent platform/);
  const setupPreview = run(["setup", "--target", setupTarget, "--mode", "balanced", "--dry-run"]);
  assert.match(setupPreview, /Would copy and verify/);
  assert.match(setupPreview, /Would set memory profile 'balanced'/);
  assert.ok(!fs.existsSync(setupTarget), "setup --dry-run must not create an installation target");

  const originalHome = process.env.HOME;
  const originalUserProfile = process.env.USERPROFILE;
  const originalCwd = process.cwd();
  process.env.HOME = tempHome;
  process.env.USERPROFILE = tempHome;
  process.chdir(workspace);
  const { runInteractive } = require(CLI);
  const answers = ["5", "4", "2", "3", "", "6", "0"];
  const transcript = [];
  await runInteractive({
    ask: async (question) => {
      transcript.push(question);
      return answers.shift() ?? "0";
    },
    write: (text) => transcript.push(text),
  });
  const interactiveOutput = transcript.join("");
  assert.match(interactiveOutput, /Memory Store v/);
  assert.match(interactiveOutput, /Change cancelled/);
  assert.match(interactiveOutput, /Maintenance preview/);
  assert.strictEqual(answers.length, 0, "interactive flow must consume the scripted choices exactly");

  const memoryFile = path.join(workspace, ".agents", "memory-store", "memories.json");
  const beforeCancelledAdd = fs.readFileSync(memoryFile, "utf8");
  const addAnswers = ["3", "1", "Cancelled memory", "This must not be persisted", "1", "", "0"];
  await runInteractive({ ask: async () => addAnswers.shift() ?? "0", write: () => {} });
  assert.strictEqual(fs.readFileSync(memoryFile, "utf8"), beforeCancelledAdd, "Enter at confirmation must cancel a write");
  assert.strictEqual(addAnswers.length, 0);

  const setupAnswers = ["1", "1", "1", "", "", "0"];
  const setupTranscript = [];
  await runInteractive({
    ask: async (question) => {
      setupTranscript.push(question);
      return setupAnswers.shift() ?? "0";
    },
    write: (text) => setupTranscript.push(text),
  });
  assert.match(setupTranscript.join(""), /1\. Codex/);
  assert.match(setupTranscript.join(""), /Setup cancelled/);
  assert.strictEqual(setupAnswers.length, 0);

  process.chdir(originalCwd);
  process.env.HOME = originalHome;
  process.env.USERPROFILE = originalUserProfile;

  console.log("CLI experience contract tests passed.");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
}

test().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
