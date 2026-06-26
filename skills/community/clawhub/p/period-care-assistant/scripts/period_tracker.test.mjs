import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { execute } from "./period_tracker.mjs";

function tempStore() {
  return path.join(fs.mkdtempSync(path.join(os.tmpdir(), "period-care-")), "tracker.enc");
}

const secret = "unit-test-secret";

test("record stores data and predicts next start", () => {
  const storePath = tempStore();

  execute(["record", "--user", "demo:alice", "--date", "2026-01-01"], { storePath, secret });
  execute(["record", "--user", "demo:alice", "--date", "2026-01-29"], { storePath, secret });
  const result = execute(["status", "--user", "demo:alice", "--today", "2026-02-10"], {
    storePath,
    secret,
  }).output.result;

  assert.equal(result.lastStartDate, "2026-01-29");
  assert.equal(result.predictedNextStart, "2026-02-26");
  assert.equal(result.currentPhase.label, "卵泡期");
});

test("duplicate record does not create a second entry", () => {
  const storePath = tempStore();

  execute(["record", "--user", "demo:bob", "--date", "2026-03-01"], { storePath, secret });
  const duplicate = execute(["record", "--user", "demo:bob", "--date", "2026-03-01"], {
    storePath,
    secret,
  }).output;
  const history = execute(["history", "--user", "demo:bob"], { storePath, secret }).output.records;

  assert.equal(duplicate.duplicate, true);
  assert.equal(history.length, 1);
});

test("configure reminder plan generates a deterministic job", () => {
  const storePath = tempStore();

  execute(["record", "--user", "demo:carol", "--date", "2026-02-01"], { storePath, secret });
  execute(["record", "--user", "demo:carol", "--date", "2026-03-01"], { storePath, secret });
  execute(
    [
      "configure",
      "--user",
      "demo:carol",
      "--timezone",
      "Asia/Shanghai",
      "--reminder-days",
      "5",
      "--delivery-mode",
      "webhook",
      "--delivery-webhook",
      "https://example.invalid/dingtalk",
    ],
    { storePath, secret },
  );

  const plan = execute(["reminder-plan", "--user", "demo:carol"], { storePath, secret }).output.plan;

  assert.equal(plan.jobName.startsWith("period-reminder-"), true);
  assert.equal(plan.predictedNextStart, "2026-03-29");
  assert.equal(plan.reminderDate, "2026-03-24");
  assert.equal(plan.delivery.mode, "webhook");
  assert.equal(plan.delivery.webhook, "https://example.invalid/dingtalk");
  assert.equal(plan.deliveryReady, true);
});
