import assert from "node:assert/strict";
import { mkdir, mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { loadConfig, resolveAgentCli } from "../config";

test("loadConfig returns empty object when config.json does not exist", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-config-"));
  const config = await loadConfig(projectDir);
  assert.deepEqual(config, {});
});

test("loadConfig reads and parses config.json", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-config-"));
  const nexumDir = path.join(projectDir, "nexum");
  await mkdir(nexumDir, { recursive: true });

  const configData = {
    notify: { target: "telegram", botToken: "abc123" },
    agents: {
      "claude-agent": { cli: "claude" as const, model: "claude-sonnet-4-6" },
      "codex-agent": { cli: "codex" as const },
    },
  };

  await writeFile(
    path.join(nexumDir, "config.json"),
    JSON.stringify(configData, null, 2),
    "utf8"
  );

  const config = await loadConfig(projectDir);
  assert.deepEqual(config, configData);
});

test("resolveAgentCli returns cli from config when agent exists", () => {
  const config = {
    agents: {
      "my-agent": { cli: "claude" as const },
    },
  };
  assert.equal(resolveAgentCli(config, "my-agent"), "claude");
});

test("resolveAgentCli defaults to codex when agent not in config", () => {
  const config = {};
  assert.equal(resolveAgentCli(config, "unknown-agent"), "codex");
});

test("resolveAgentCli defaults to codex when agents map is empty", () => {
  const config = { agents: {} };
  assert.equal(resolveAgentCli(config, "any-agent"), "codex");
});
