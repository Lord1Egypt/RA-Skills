const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const {
  long_context_shell_run,
  long_context_shell_peek,
  long_context_shell_scan,
  long_context_shell_stop
} = require("./handler");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForStatus(sessionId, statuses, timeoutMs = 5000) {
  const expected = new Set(statuses);
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    const card = await long_context_shell_peek({ sessionId, tailLines: 20 });
    if (expected.has(card.status)) {
      return card;
    }
    await sleep(100);
  }

  return long_context_shell_peek({ sessionId, tailLines: 20 });
}

test("captures short command output and success state", async () => {
  const card = await long_context_shell_run({
    command: `node -e "console.log('hello-from-test')"`,
    waitMs: 300
  });
  const settled = await waitForStatus(card.sessionId, ["success"]);

  assert.equal(settled.status, "success");
  assert.equal(settled.background, false);
  assert.match(settled.preview, /hello-from-test/);
  assert.ok(fs.existsSync(settled.logPath));
});

test("scans failed command output and supports time queries", async () => {
  const card = await long_context_shell_run({
    command: `node -e "console.log('before-failure'); console.error('fatal: boom'); process.exit(2)"`,
    waitMs: 300
  });
  const settled = await waitForStatus(card.sessionId, ["failed"]);
  const scan = await long_context_shell_scan({ sessionId: card.sessionId, limit: 5 });
  const peekByTime = await long_context_shell_peek({
    sessionId: card.sessionId,
    timeQuery: settled.startedAt.slice(0, 16)
  });

  assert.equal(settled.status, "failed");
  assert.equal(settled.exitCode, 2);
  assert.ok(scan.matchedCount >= 1);
  assert.ok((scan.severityCounts.critical || 0) >= 1);
  assert.match(scan.matches[0].line, /fatal: boom/i);
  assert.ok(peekByTime.timeMatches.length >= 1);
});

test("runs background monitoring sessions and stops them cleanly", async () => {
  const card = await long_context_shell_run({
    command: `node -e "let count = 0; setInterval(() => console.log('tick-' + (++count)), 100)"`,
    background: true,
    waitMs: 100
  });

  assert.equal(card.background, true);
  assert.equal(card.status, "running");

  await sleep(500);
  const running = await long_context_shell_peek({ sessionId: card.sessionId, tailLines: 10 });
  const stopped = await long_context_shell_stop({ sessionId: card.sessionId });
  const finalCard = await waitForStatus(card.sessionId, ["stopped"]);

  assert.equal(running.status, "running");
  assert.ok(running.lineCount >= 1);
  assert.equal(stopped.status, "stopped");
  assert.equal(finalCard.status, "stopped");
  assert.match(finalCard.preview, /tick-/);
});
