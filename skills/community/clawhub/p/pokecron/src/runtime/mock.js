// In-memory runtime backend for tests.
//
// Implements the poke runtime interface (see src/runtime/index.js). All
// calls are recorded on `runtime.calls` — an array of { method, payload, ts }
// entries — so tests can assert "deliver was called exactly once with these
// args" without spinning up a fake openclaw bin.
//
// Activate with POKE_RUNTIME_BACKEND=mock.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const MOCK_RUNTIME_REGISTRY = new Map();

function ensureDir(d) { fs.mkdirSync(d, { recursive: true }); }

function defaultStateDir(options = {}) {
  if (options.preferredStateDir) return options.preferredStateDir;
  if (process.env.POKE_RUNTIME_MOCK_STATE_DIR) return process.env.POKE_RUNTIME_MOCK_STATE_DIR;
  return fs.mkdtempSync(path.join(os.tmpdir(), "poke-runtime-mock-"));
}

export function createMockRuntime(options = {}) {
  const home = options.preferredHome || os.homedir();
  const stateDir = defaultStateDir(options);
  ensureDir(stateDir);

  const calls = [];

  const runtime = {
    id: "mock",
    home,
    stateDir,
    configPath: path.join(stateDir, "openclaw.json"),
    bin: null,
    compatDir: path.join(stateDir, "openclaw-compat"),

    deliver(payload) {
      calls.push({ method: "deliver", payload, ts: Date.now() });
      return "";
    },

    localAgent(payload) {
      calls.push({ method: "localAgent", payload, ts: Date.now() });
      // Default heuristic-only response: classifier should not match.
      return JSON.stringify({ match_id: "none", action: "ignore", reason: "mock" });
    },

    defaultAgentId() {
      calls.push({ method: "defaultAgentId", ts: Date.now() });
      return options.defaultAgentId || "mock-agent";
    },

    // Test introspection.
    get calls() { return calls; },
    clearCalls() { calls.length = 0; }
  };

  // Registry so tests holding only a stateDir can introspect calls.
  MOCK_RUNTIME_REGISTRY.set(stateDir, runtime);
  return runtime;
}

export function getMockRuntimeByStateDir(stateDir) {
  return MOCK_RUNTIME_REGISTRY.get(stateDir) || null;
}
