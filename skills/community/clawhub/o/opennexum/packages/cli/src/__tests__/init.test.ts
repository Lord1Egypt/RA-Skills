import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

async function exists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

test("runInit creates AGENTS.md as the callback protocol source of truth", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-init-test-"));
  const { runInit } = await import(`../commands/init.ts?init=${Date.now()}`);

  await runInit(projectDir, true);

  const agentsPath = path.join(projectDir, "AGENTS.md");
  const claudePath = path.join(projectDir, "CLAUDE.md");
  const agents = await readFile(agentsPath, "utf8");

  assert.equal(await exists(agentsPath), true);
  assert.equal(await exists(claudePath), false);
  assert.match(agents, /nexum callback <taskId>/);
  assert.match(agents, /# AGENTS\.md/);
});
