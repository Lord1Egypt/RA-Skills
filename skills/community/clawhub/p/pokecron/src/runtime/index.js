// Runtime interface — the abstraction poke uses to talk to whatever harness
// it lives in. The OpenClaw backend is the default; the mock backend is
// for tests; a future harness would add a sibling backend file and route
// POKE_RUNTIME_BACKEND to it.
//
// **Interface (every backend MUST implement):**
//
//   .id           — string tag, e.g. "openclaw" | "mock"
//   .home         — string, home directory the runtime treats as canonical
//   .stateDir     — string, where the runtime stores its own state (used by
//                   poke's isBusyLane to inspect sessions.json)
//   .configPath   — string, path to the runtime's config (informational)
//   .bin          — string|null, path to the runtime binary (informational)
//
//   .deliver({ agent, channel, target, prompt, sessionHint?, thinking? })
//        — spawn an agent, run the prompt, AND deliver its output to
//          (channel, target). This is Law #1 — the only path that touches
//          the user. No static-message variant exists.
//
//   .localAgent({ agent, prompt, sessionHint?, thinking? }) -> string
//        — run an agent with the prompt and return its stdout. Used for
//          inline classification (reply intent matching). Does NOT deliver.
//
//   .defaultAgentId() -> string
//        — pick a sensible default agent if none was specified at create
//          time. Empty string is acceptable; callers handle that.

import { createOpenClawRuntime } from "./openclaw.js";
import { createMockRuntime } from "./mock.js";

export function loadRuntime(options = {}) {
  const backend = options.backend || process.env.POKE_RUNTIME_BACKEND || "openclaw";
  if (backend === "mock") return createMockRuntime(options);
  if (backend === "openclaw") return createOpenClawRuntime(options);
  throw new Error(`Unknown POKE_RUNTIME_BACKEND: ${backend}`);
}

export { createOpenClawRuntime, createMockRuntime };
