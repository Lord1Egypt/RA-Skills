import test from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { buildEmailMessage } from "../src/delivery/build-email-message.js";
import { sendEmail } from "../src/delivery/send-email.js";

test("buildEmailMessage creates a multipart email", () => {
  const message = buildEmailMessage({
    from: "mindkeeper@example.com",
    to: "alex@example.com",
    subject: "Mindkeeper Daily Brief",
    textBody: "Plain body",
    htmlBody: "<p>HTML body</p>",
  });

  assert.match(message, /multipart\/alternative/);
  assert.match(message, /Subject: Mindkeeper Daily Brief/);
  assert.match(message, /HTML body/);
});

test("sendEmail can write an .eml file", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-email-"));
  const outPath = path.join(tempDir, "brief.eml");
  const message = buildEmailMessage({
    from: "mindkeeper@example.com",
    to: "alex@example.com",
    subject: "Mindkeeper Daily Brief",
    textBody: "Plain body",
    htmlBody: "<p>HTML body</p>",
  });

  const result = await sendEmail({ mode: "file", emailMessage: message, outPath });
  const file = await readFile(outPath, "utf8");

  assert.equal(result.mode, "file");
  assert.match(file, /Subject: Mindkeeper Daily Brief/);
  assert.match(file, /HTML body/);
});

test("sendEmail can invoke NexLink mail send via a CLI script", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-nexlink-"));
  const logPath = path.join(tempDir, "nexlink-log.json");
  const scriptPath = path.join(tempDir, "fake-nexlink.py");

  await writeFile(scriptPath, `import json, os, sys\nwith open(os.environ['MINDKEEPER_FAKE_NEXLINK_LOG'], 'w') as f:\n    json.dump(sys.argv[1:], f)\n`, "utf8");

  const result = await sendEmail({
    mode: "nexlink",
    to: "alex@example.com",
    subject: "Mindkeeper Daily Brief",
    textBody: "Plain body",
    htmlBody: "<p>HTML body</p>",
    nexlinkCliPath: scriptPath,
    pythonBin: "python3",
    env: { ...process.env, MINDKEEPER_FAKE_NEXLINK_LOG: logPath },
  });

  const loggedArgs = JSON.parse(await readFile(logPath, "utf8"));
  assert.equal(result.mode, "nexlink");
  assert.deepEqual(loggedArgs.slice(0, 2), ["mail", "send"]);
  assert.ok(loggedArgs.includes("--html"));
  assert.ok(loggedArgs.includes("alex@example.com"));
});
