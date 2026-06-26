import assert from "node:assert/strict";
import test from "node:test";

test("spawnAcpSession returns a stub session record", async () => {
  const { spawnAcpSession } = await import(`../spawn.ts?spawn=${Date.now()}`);
  const record = await spawnAcpSession({
    taskId: "NX-002",
    agentId: "codex-gen-01",
    promptFile: "/tmp/prompt.md",
    cwd: "/tmp/project",
    mode: "run",
    label: "nx-002-codex",
  });

  assert.equal(record.taskId, "NX-002");
  assert.equal(record.sessionKey, "codex-gen-01");
  assert.equal(record.agentId, "codex-gen-01");
  assert.equal(record.status, "running");
  assert.ok(Number.isFinite(Date.parse(record.startedAt)));
});

test("resolveCliName infers cliName from explicit cli or agentId prefix", async () => {
  const { resolveCliName } = await import(`../spawn.ts?spawn-prefix=${Date.now()}`);

  assert.equal(resolveCliName("codex-gen-01"), "codex");
  assert.equal(resolveCliName("claude-gen-01"), "claude");
  assert.equal(resolveCliName("unknown"), "codex");
  assert.equal(resolveCliName("codex-gen-01", "claude"), "claude");
});
