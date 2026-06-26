import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import os from "node:os";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { createLcmFixtureDb } from "./helpers/create-lcm-fixture.js";

const execFileAsync = promisify(execFile);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixture = path.join(__dirname, "fixtures", "2026-04-09.md");
const entry = path.join(__dirname, "..", "src", "index.js");

test("CLI can export html output to a file", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-"));
  const outFile = path.join(tempDir, "brief.html");

  const { stdout } = await execFileAsync("node", [
    entry,
    "--date",
    "2026-04-09",
    "--memory-file",
    fixture,
    "--format",
    "html",
    "--out",
    outFile,
  ]);

  const html = await readFile(outFile, "utf8");
  assert.match(stdout, /Wrote output .* to/);
  assert.match(html, /Mindkeeper Daily Brief/);
  assert.match(html, /Built for teams using/);
  assert.match(html, /Hybrid report/);
  assert.match(html, /Firma de AI/);
});

test("CLI can auto-focus from prompt and write an email file", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-"));
  const emailFile = path.join(tempDir, "brief.eml");

  const { stdout } = await execFileAsync("node", [
    entry,
    "--date",
    "2026-04-09",
    "--memory-file",
    fixture,
    "--prompt",
    "Focus on lossless-claw and openclaw-mindkeeper naming",
    "--email-to",
    "alex@example.com",
    "--email-from",
    "mindkeeper@example.com",
    "--email-out",
    emailFile,
    "--format",
    "text",
  ]);

  const eml = await readFile(emailFile, "utf8");
  assert.match(stdout, /Email delivery/);
  assert.match(stdout, /openclaw-mindkeeper|lossless-claw|focusTerms/);
  assert.match(eml, /Subject: Mindkeeper .* Brief/);
  assert.match(eml, /multipart\/alternative/);
});

test("CLI can route email delivery through NexLink", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-nexlink-cli-"));
  const logPath = path.join(tempDir, "nexlink-log.json");
  const scriptPath = path.join(tempDir, "fake-nexlink.py");

  await writeFile(scriptPath, `import json, os, sys\nwith open(os.environ['MINDKEEPER_FAKE_NEXLINK_LOG'], 'w') as f:\n    json.dump(sys.argv[1:], f)\n`, "utf8");

  const { stdout } = await execFileAsync("node", [
    entry,
    "--date",
    "2026-04-09",
    "--memory-file",
    fixture,
    "--prompt",
    "Focus on lossless-claw and openclaw-mindkeeper naming",
    "--email-mode",
    "nexlink",
    "--nexlink-cli",
    scriptPath,
    "--python-bin",
    "python3",
    "--email-to",
    "alex@example.com",
    "--format",
    "text",
  ], {
    env: { ...process.env, MINDKEEPER_FAKE_NEXLINK_LOG: logPath },
  });

  const loggedArgs = JSON.parse(await readFile(logPath, "utf8"));
  assert.match(stdout, /Email delivery/);
  assert.deepEqual(loggedArgs.slice(0, 2), ["mail", "send"]);
  assert.ok(loggedArgs.includes("--html"));
});

test("CLI compare-pair can write hybrid and lossless-only email files", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-compare-"));
  const emailFile = path.join(tempDir, "brief.eml");
  const dbPath = await createLcmFixtureDb();

  const { stdout } = await execFileAsync("node", [
    entry,
    "--date",
    "2026-04-09",
    "--compare-pair",
    "--memory-file",
    fixture,
    "--use-lcm",
    "--lcm-db",
    dbPath,
    "--session-key",
    "agent:main:main",
    "--email-to",
    "alex@example.com",
    "--email-from",
    "mindkeeper@example.com",
    "--email-out",
    emailFile,
    "--format",
    "text",
  ]);

  const hybridEml = await readFile(path.join(tempDir, "brief-hybrid.eml"), "utf8");
  const losslessEml = await readFile(path.join(tempDir, "brief-lossless-only.eml"), "utf8");
  assert.match(stdout, /Email delivery \(hybrid\)/);
  assert.match(stdout, /Email delivery \(lossless-only\)/);
  assert.match(hybridEml, /Subject: Mindkeeper Hybrid Brief/);
  assert.match(losslessEml, /Subject: Mindkeeper Lossless-Only Brief/);
});

test("CLI compare-pair requires LCM", async () => {
  await assert.rejects(
    execFileAsync("node", [
      entry,
      "--date",
      "2026-04-09",
      "--compare-pair",
      "--memory-file",
      fixture,
    ]),
    /compare-pair mode requires --use-lcm/,
  );
});
