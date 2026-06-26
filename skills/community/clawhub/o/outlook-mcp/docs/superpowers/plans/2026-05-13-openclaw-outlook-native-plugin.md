# Native OpenClaw Outlook Plugin (Bridge over `outlook-mcp`) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a native OpenClaw plugin at `~/ClaudeCode/openclaw-outlook-plugin/` that exposes the ~50 Outlook tools from `~/ClaudeCode/outlook-mcp` (Python FastMCP, v1.5.3) to the OpenClaw agent's `tools[]` array — bypassing the broken `mcp.servers` integration in OpenClaw 5.x.

**Architecture:** Bridge approach. The new plugin is a thin TypeScript wrapper that spawns `uv run outlook-mcp` as a child process, performs the JSON-RPC initialize/list/call handshake itself, and registers each Outlook tool through OpenClaw's native `api.registerTool()` API (which is *proven working* — `cost-tracker` and `web_search` already reach `tools[]` this way). The Python `outlook-mcp` repo stays the single source of truth for Graph API logic; the new plugin owns only the bridge.

**Tech Stack:** TypeScript ESM, Node 22+, `definePluginEntry` from `openclaw/plugin-sdk/plugin-entry`, child_process stdio, JSON-RPC 2.0, `vitest` for tests.

---

## Architectural decision and rationale

Three options were considered:

| | (A) Bridge | (B) Port | (C) Hybrid |
|---|---|---|---|
| Effort | ~4–6 hrs | ~10–15 hrs | ~6–10 hrs |
| Reuses 403 passing tests | ✅ | ❌ | partial |
| Single source of truth for Graph logic | ✅ | ❌ | ❌ |
| Removes Python dependency | ❌ | ✅ | partial |
| Risk of new bugs | low | medium-high | medium |

**Choosing (A) Bridge** because:

1. **The known-broken layer is `mcp.servers` — NOT `api.registerTool()`.** Our wire captures prove built-in tools (`read`, `write`, `exec`, `web_search`) reach `tools[]` fine through the native registration path. The bridge plugs into the working path; it does **not** re-implement what's broken upstream.
2. Michael's constraint: no duplicate Graph logic. (B) violates this; (A) preserves it.
3. The Python `outlook-mcp` continues to serve Claude Code, Cursor, Codex, and any other MCP client via the standard `mcp.servers` registration. Killing it would harm those use cases.
4. The bridge is small (~200 lines of TS) and disposable — if OpenClaw fixes the MCP bug, we can remove the bridge and switch back to `mcp.servers` with zero loss.

## File structure

```
~/ClaudeCode/openclaw-outlook-plugin/
├── package.json                       # npm-publishable, ESM, "openclaw" peerDep
├── openclaw.plugin.json               # manifest, lists all 50 outlook_* tool names in contracts.tools
├── tsconfig.json                      # strict, target ES2022, module NodeNext
├── README.md                          # install, dev workflow, design notes
├── .gitignore                         # node_modules, dist
├── src/
│   ├── index.ts                       # entry point — definePluginEntry, register tools dynamically
│   ├── bridge.ts                      # MCPBridge class — spawn, initialize, tools/list, tools/call
│   ├── tool-catalog.ts                # static list of expected tool names (fallback when bridge probe fails)
│   └── types.ts                       # TS types for JSON-RPC request/response shapes
├── test/
│   ├── bridge.test.ts                 # vitest unit tests for bridge with mocked child
│   ├── catalog.test.ts                # snapshot test for tool name list
│   └── integration.test.ts            # spawn real outlook-mcp, do an unauthed `outlook_auth_status` round-trip
└── dist/                              # build output (gitignored)
```

The plugin lives in a **new sibling repository** to `outlook-mcp`. It is its own npm package (`@mpalermiti/openclaw-outlook`) so it can be published independently to ClawHub later.

## What happens to the existing Python `outlook-mcp`

**Unchanged.** It stays at `~/ClaudeCode/outlook-mcp`, continues to be the MCP server for:
- Claude Code (via its native MCP client)
- Cursor, Codex, any other MCP-compliant client
- This new openclaw plugin (via subprocess)

No files in `outlook-mcp/` are modified by this plan. The new plugin's child process invocation is:
```bash
/Users/neo/.local/bin/uv --directory /Users/neo/ClaudeCode/outlook-mcp run outlook-mcp
```
…which is identical to how it's currently configured under `mcp.servers.outlook` in `~/.openclaw/openclaw.json`.

## Auth handling

The Python `outlook-mcp` reads its OAuth state from `~/.outlook-mcp/auth_record.json` and `config.json`. The new plugin doesn't touch auth itself — the subprocess inherits the host env, finds the cache, and authenticates as before. **Zero re-auth needed.** Token refresh is handled inside the Python child by `azure-identity`, identically to today.

If the cache is missing or expired, `outlook_auth_status` returns `authenticated: false` with `action_required: "Run \`outlook-mcp auth\` on the host..."`. That behavior is preserved verbatim.

## Lifecycle

- **Lazy spawn:** child process is started on the first `execute()` call, not at plugin load. This avoids paying Azure-auth latency for sessions that don't touch Outlook.
- **Long-lived:** once spawned, the child stays alive for the gateway process lifetime. Subsequent tool calls reuse the same JSON-RPC channel.
- **Shutdown:** plugin's `runtime.dispose` hook (if available) closes stdin and waits up to 5s for graceful exit, then SIGKILL.
- **Crash recovery:** if the child exits unexpectedly, the next `execute()` re-spawns. Pending requests are rejected with `tool_unavailable`.

## Self-review check before posting (deferred to maintainer)

After writing this plan I checked it for: completeness against the goal, no TBD/placeholder steps, type consistency (`MCPBridge` named consistently, `ToolDescriptor` shape matches SDK across tasks), every spec requirement (10 numbered items in the original prompt) has at least one task.

---

## Task 1: Bootstrap the new repository

**Files:**
- Create: `~/ClaudeCode/openclaw-outlook-plugin/package.json`
- Create: `~/ClaudeCode/openclaw-outlook-plugin/openclaw.plugin.json`
- Create: `~/ClaudeCode/openclaw-outlook-plugin/tsconfig.json`
- Create: `~/ClaudeCode/openclaw-outlook-plugin/.gitignore`
- Create: `~/ClaudeCode/openclaw-outlook-plugin/README.md`

- [ ] **Step 1: Create directory and init git**

```bash
mkdir -p ~/ClaudeCode/openclaw-outlook-plugin
cd ~/ClaudeCode/openclaw-outlook-plugin
git init -b main
```

- [ ] **Step 2: Write `package.json`**

```bash
cat > package.json <<'EOF'
{
  "name": "@mpalermiti/openclaw-outlook",
  "version": "0.1.0",
  "description": "Native OpenClaw plugin that bridges to the Python outlook-mcp server, exposing Microsoft Outlook tools (mail, calendar, contacts, tasks, drafts) to OpenClaw agents.",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist", "openclaw.plugin.json", "README.md", "LICENSE"],
  "openclaw": {
    "extensions": ["./dist/index.js"]
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit -p tsconfig.json",
    "prepublishOnly": "npm run build"
  },
  "peerDependencies": {
    "openclaw": ">=2026.5.7"
  },
  "devDependencies": {
    "@sinclair/typebox": "^0.32.0",
    "@types/node": "^22.0.0",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0"
  },
  "engines": {
    "node": ">=22"
  },
  "license": "MIT"
}
EOF
```

- [ ] **Step 3: Write `openclaw.plugin.json` with all expected tool names**

```bash
cat > openclaw.plugin.json <<'EOF'
{
  "id": "outlook",
  "name": "Outlook",
  "description": "Microsoft Outlook tools (mail, calendar, contacts, tasks) bridged from the outlook-mcp Python server. Spawns uv run outlook-mcp as a subprocess on first tool call.",
  "version": "0.1.0",
  "activation": {
    "onStartup": false
  },
  "contracts": {
    "tools": [
      "outlook_auth_status",
      "outlook_list_inbox",
      "outlook_read_message",
      "outlook_search_mail",
      "outlook_list_folders",
      "outlook_list_thread",
      "outlook_send_message",
      "outlook_reply",
      "outlook_forward",
      "outlook_move_message",
      "outlook_delete_message",
      "outlook_mark_read",
      "outlook_flag_message",
      "outlook_categorize_message",
      "outlook_reclassify_message",
      "outlook_create_folder",
      "outlook_rename_folder",
      "outlook_delete_folder",
      "outlook_list_drafts",
      "outlook_create_draft",
      "outlook_update_draft",
      "outlook_send_draft",
      "outlook_delete_draft",
      "outlook_list_attachments",
      "outlook_download_attachment",
      "outlook_send_with_attachments",
      "outlook_batch_triage",
      "outlook_copy_message",
      "outlook_list_calendars",
      "outlook_list_events",
      "outlook_get_event",
      "outlook_create_event",
      "outlook_update_event",
      "outlook_delete_event",
      "outlook_rsvp",
      "outlook_list_task_lists",
      "outlook_list_tasks",
      "outlook_create_task",
      "outlook_update_task",
      "outlook_complete_task",
      "outlook_delete_task",
      "outlook_list_contacts",
      "outlook_get_contact",
      "outlook_search_contacts",
      "outlook_create_contact",
      "outlook_update_contact",
      "outlook_delete_contact",
      "outlook_list_accounts",
      "outlook_switch_account",
      "outlook_whoami",
      "outlook_list_categories",
      "outlook_get_mail_tips"
    ]
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "outlookMcpPath": {
        "type": "string",
        "description": "Absolute path to the outlook-mcp source directory. Defaults to ~/ClaudeCode/outlook-mcp."
      },
      "uvPath": {
        "type": "string",
        "description": "Absolute path to the uv binary. Defaults to ~/.local/bin/uv."
      },
      "spawnTimeoutMs": {
        "type": "integer",
        "minimum": 1000,
        "default": 30000,
        "description": "How long to wait for the subprocess initialize handshake before giving up."
      }
    }
  }
}
EOF
```

- [ ] **Step 4: Write `tsconfig.json`**

```bash
cat > tsconfig.json <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "test"]
}
EOF
```

- [ ] **Step 5: Write `.gitignore`**

```bash
cat > .gitignore <<'EOF'
node_modules/
dist/
*.tsbuildinfo
.DS_Store
.env
.env.local
coverage/
EOF
```

- [ ] **Step 6: Write minimal `README.md`**

```bash
cat > README.md <<'EOF'
# @mpalermiti/openclaw-outlook

Native OpenClaw plugin that bridges to the Python `outlook-mcp` server, exposing Microsoft Outlook tools (mail, calendar, contacts, tasks) to OpenClaw agents.

## Why this exists

OpenClaw's `mcp.servers` integration has a regression (see https://github.com/openclaw/openclaw/issues/80909) that causes configured MCP server tools to never reach the agent's outbound `tools[]` array. This plugin sidesteps the bug by registering Outlook tools through OpenClaw's native `api.registerTool()` API — which is proven working for built-in tools like `read`, `write`, `exec`, and `web_search`.

## Install (local dev)

```bash
git clone https://github.com/mpalermiti/openclaw-outlook-plugin.git
cd openclaw-outlook-plugin
npm install
npm run build
openclaw plugins install --link .
openclaw gateway restart
```

## Verify

```bash
openclaw plugins inspect outlook
```

Status should be `loaded`.

## Auth

The plugin spawns `uv run outlook-mcp` from `~/ClaudeCode/outlook-mcp` as a child process and inherits the existing `~/.outlook-mcp/auth_record.json` token cache. No re-auth needed if outlook-mcp was already authenticated.
EOF
```

- [ ] **Step 7: Run `npm install` to populate node_modules and lock file**

```bash
cd ~/ClaudeCode/openclaw-outlook-plugin
npm install
```

Expected: installs typescript, vitest, typebox, @types/node, and openclaw as peerDep (which is already global).

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: bootstrap openclaw-outlook-plugin package"
```

---

## Task 2: Failing smoke test for plugin entry

**Files:**
- Create: `test/index.test.ts`

- [ ] **Step 1: Write the failing test**

```bash
cat > test/index.test.ts <<'EOF'
import { describe, it, expect } from "vitest";

describe("plugin entry", () => {
  it("exports a default with id 'outlook'", async () => {
    const mod = await import("../src/index.js");
    const entry = mod.default as any;
    expect(entry).toBeDefined();
    expect(entry.id).toBe("outlook");
    expect(typeof entry.register).toBe("function");
  });
});
EOF
```

- [ ] **Step 2: Run test to verify it fails**

```bash
npx vitest run test/index.test.ts
```

Expected: FAIL with "Cannot find module '../src/index.js'" (no entry file yet).

- [ ] **Step 3: Write minimal `src/index.ts`**

```bash
mkdir -p src
cat > src/index.ts <<'EOF'
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "outlook",
  name: "Outlook",
  description: "Outlook tools bridged from the outlook-mcp Python server.",
  register(_api) {
    // Real tool registration arrives in Task 6. For now, no-op.
  },
});
EOF
```

- [ ] **Step 4: Build and run the test**

```bash
npm run build
npx vitest run test/index.test.ts
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "test: entry exports id=outlook and register fn"
```

---

## Task 3: Bridge class — `tools/list` flow with mocked child

**Files:**
- Create: `src/types.ts`
- Create: `src/bridge.ts`
- Create: `test/bridge.test.ts`

- [ ] **Step 1: Write `src/types.ts` with JSON-RPC and MCP message shapes**

```bash
cat > src/types.ts <<'EOF'
export interface JsonRpcRequest {
  jsonrpc: "2.0";
  id: number;
  method: string;
  params?: unknown;
}

export interface JsonRpcNotification {
  jsonrpc: "2.0";
  method: string;
  params?: unknown;
}

export interface JsonRpcResponseOk<T = unknown> {
  jsonrpc: "2.0";
  id: number;
  result: T;
}

export interface JsonRpcResponseErr {
  jsonrpc: "2.0";
  id: number;
  error: { code: number; message: string; data?: unknown };
}

export type JsonRpcResponse<T = unknown> = JsonRpcResponseOk<T> | JsonRpcResponseErr;

export interface McpToolDescriptor {
  name: string;
  description?: string;
  inputSchema: Record<string, unknown>;
}

export interface McpToolsListResult {
  tools: McpToolDescriptor[];
}

export interface McpContentBlock {
  type: string;
  text?: string;
  data?: string;
  [key: string]: unknown;
}

export interface McpToolsCallResult {
  content: McpContentBlock[];
  isError?: boolean;
}

export interface BridgeOptions {
  uvPath: string;
  outlookMcpPath: string;
  spawnTimeoutMs: number;
  logger?: { info?: (msg: string) => void; warn?: (msg: string) => void; error?: (msg: string) => void };
}
EOF
```

- [ ] **Step 2: Write the failing test for `MCPBridge.listTools()`**

```bash
cat > test/bridge.test.ts <<'EOF'
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { EventEmitter } from "node:events";

// Hoisted mock for child_process.spawn so the bridge code uses our fake.
const spawnMock = vi.fn();
vi.mock("node:child_process", () => ({ spawn: spawnMock }));

import { MCPBridge } from "../src/bridge.js";

function makeFakeChild() {
  const child = new EventEmitter() as any;
  child.stdin = { write: vi.fn(), end: vi.fn() };
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  child.kill = vi.fn();
  child.pid = 12345;
  return child;
}

describe("MCPBridge.listTools", () => {
  beforeEach(() => spawnMock.mockReset());
  afterEach(() => vi.useRealTimers());

  it("performs initialize handshake then returns tools[]", async () => {
    const child = makeFakeChild();
    spawnMock.mockReturnValue(child);

    const bridge = new MCPBridge({
      uvPath: "/fake/uv",
      outlookMcpPath: "/fake/outlook-mcp",
      spawnTimeoutMs: 1000,
    });

    const listPromise = bridge.listTools();

    // Drive the handshake by emitting responses on stdout.
    // Bridge will send initialize (id 1), notifications/initialized (no id),
    // then tools/list (id 2). We respond to ids 1 and 2.
    setTimeout(() => {
      child.stdout.emit("data", JSON.stringify({
        jsonrpc: "2.0", id: 1,
        result: { protocolVersion: "2025-06-18", capabilities: {}, serverInfo: { name: "outlook-mcp", version: "1.5.3" } }
      }) + "\n");
      child.stdout.emit("data", JSON.stringify({
        jsonrpc: "2.0", id: 2,
        result: { tools: [
          { name: "outlook_whoami", description: "test", inputSchema: { type: "object", properties: {} } }
        ]}
      }) + "\n");
    }, 5);

    const tools = await listPromise;
    expect(tools).toHaveLength(1);
    expect(tools[0].name).toBe("outlook_whoami");
    expect(spawnMock).toHaveBeenCalledOnce();
    expect(spawnMock.mock.calls[0][0]).toBe("/fake/uv");
    expect(spawnMock.mock.calls[0][1]).toEqual(["--directory", "/fake/outlook-mcp", "run", "outlook-mcp"]);
  });
});
EOF
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
npx vitest run test/bridge.test.ts
```

Expected: FAIL with "Cannot find module '../src/bridge.js'".

- [ ] **Step 4: Implement `src/bridge.ts`**

```bash
cat > src/bridge.ts <<'EOF'
import { spawn, type ChildProcessByStdio } from "node:child_process";
import type { Readable, Writable } from "node:stream";
import type {
  BridgeOptions,
  JsonRpcResponse,
  McpToolDescriptor,
  McpToolsCallResult,
  McpToolsListResult,
} from "./types.js";

type Pending = {
  resolve: (value: unknown) => void;
  reject: (err: Error) => void;
};

export class MCPBridge {
  private opts: BridgeOptions;
  private child: ChildProcessByStdio<Writable, Readable, Readable> | null = null;
  private nextId = 1;
  private pending = new Map<number, Pending>();
  private readBuf = "";
  private initialized = false;
  private initPromise: Promise<void> | null = null;

  constructor(opts: BridgeOptions) {
    this.opts = opts;
  }

  async listTools(): Promise<McpToolDescriptor[]> {
    await this.ensureInitialized();
    const res = (await this.request("tools/list", {})) as McpToolsListResult;
    return res.tools;
  }

  async callTool(name: string, args: Record<string, unknown>): Promise<McpToolsCallResult> {
    await this.ensureInitialized();
    return (await this.request("tools/call", { name, arguments: args })) as McpToolsCallResult;
  }

  async dispose(): Promise<void> {
    if (!this.child) return;
    try {
      this.child.stdin.end();
    } catch {}
    await new Promise<void>((resolve) => {
      const t = setTimeout(() => {
        try {
          this.child?.kill("SIGKILL");
        } catch {}
        resolve();
      }, 5000);
      this.child!.once("exit", () => {
        clearTimeout(t);
        resolve();
      });
    });
    this.child = null;
    this.initialized = false;
    this.initPromise = null;
  }

  private async ensureInitialized(): Promise<void> {
    if (this.initialized) return;
    if (this.initPromise) return this.initPromise;
    this.initPromise = this.doInitialize();
    return this.initPromise;
  }

  private async doInitialize(): Promise<void> {
    this.spawn();
    const initResult = await this.request("initialize", {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "openclaw-outlook-plugin", version: "0.1.0" },
    });
    this.opts.logger?.info?.(`outlook bridge initialized: ${JSON.stringify((initResult as any)?.serverInfo ?? {})}`);
    this.send({ jsonrpc: "2.0", method: "notifications/initialized", params: {} });
    this.initialized = true;
  }

  private spawn(): void {
    if (this.child) return;
    const child = spawn(
      this.opts.uvPath,
      ["--directory", this.opts.outlookMcpPath, "run", "outlook-mcp"],
      { stdio: ["pipe", "pipe", "pipe"] },
    ) as ChildProcessByStdio<Writable, Readable, Readable>;
    this.child = child;

    child.stdout.setEncoding("utf-8");
    child.stdout.on("data", (chunk: string) => this.onStdoutData(chunk));
    child.stderr.setEncoding("utf-8");
    child.stderr.on("data", (chunk: string) => {
      this.opts.logger?.warn?.(`outlook-mcp stderr: ${chunk.trimEnd()}`);
    });
    child.on("exit", (code, signal) => {
      this.opts.logger?.warn?.(`outlook-mcp exited code=${code} signal=${signal}`);
      this.rejectAllPending(new Error(`outlook-mcp child exited (code=${code}, signal=${signal})`));
      this.child = null;
      this.initialized = false;
      this.initPromise = null;
    });
    child.on("error", (err) => {
      this.opts.logger?.error?.(`outlook-mcp spawn error: ${err.message}`);
      this.rejectAllPending(err);
    });
  }

  private onStdoutData(chunk: string): void {
    this.readBuf += chunk;
    while (true) {
      const nl = this.readBuf.indexOf("\n");
      if (nl < 0) break;
      const line = this.readBuf.slice(0, nl).trim();
      this.readBuf = this.readBuf.slice(nl + 1);
      if (!line) continue;
      let msg: JsonRpcResponse;
      try {
        msg = JSON.parse(line);
      } catch {
        this.opts.logger?.warn?.(`outlook-mcp non-JSON line: ${line.slice(0, 200)}`);
        continue;
      }
      if (typeof msg.id !== "number") continue; // ignore notifications from server
      const pending = this.pending.get(msg.id);
      if (!pending) continue;
      this.pending.delete(msg.id);
      if ("error" in msg) {
        pending.reject(new Error(`outlook-mcp error: ${msg.error.message}`));
      } else {
        pending.resolve(msg.result);
      }
    }
  }

  private send(payload: unknown): void {
    if (!this.child) throw new Error("outlook-mcp child not spawned");
    this.child.stdin.write(JSON.stringify(payload) + "\n");
  }

  private request(method: string, params: unknown): Promise<unknown> {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      this.pending.set(id, { resolve, reject });
      try {
        this.send({ jsonrpc: "2.0", id, method, params });
      } catch (err) {
        this.pending.delete(id);
        reject(err as Error);
        return;
      }
      const timeout = setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`outlook-mcp request ${method} (id ${id}) timed out after ${this.opts.spawnTimeoutMs}ms`));
        }
      }, this.opts.spawnTimeoutMs);
      const existing = this.pending.get(id);
      if (existing) {
        const origResolve = existing.resolve;
        const origReject = existing.reject;
        this.pending.set(id, {
          resolve: (v) => { clearTimeout(timeout); origResolve(v); },
          reject: (e) => { clearTimeout(timeout); origReject(e); },
        });
      }
    });
  }

  private rejectAllPending(err: Error): void {
    for (const [, pending] of this.pending) pending.reject(err);
    this.pending.clear();
  }
}
EOF
```

- [ ] **Step 5: Build and run the test**

```bash
npm run build
npx vitest run test/bridge.test.ts
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(bridge): MCPBridge.listTools with initialize handshake (mocked)"
```

---

## Task 4: Bridge `callTool` — forward request and return content

**Files:**
- Modify: `test/bridge.test.ts` (append)

(`callTool` is already implemented in `bridge.ts` — this task just adds the test.)

- [ ] **Step 1: Append failing `callTool` test**

```bash
cat >> test/bridge.test.ts <<'EOF'

describe("MCPBridge.callTool", () => {
  beforeEach(() => spawnMock.mockReset());

  it("forwards tools/call and returns content blocks", async () => {
    const child = makeFakeChild();
    spawnMock.mockReturnValue(child);

    const bridge = new MCPBridge({
      uvPath: "/fake/uv",
      outlookMcpPath: "/fake/outlook-mcp",
      spawnTimeoutMs: 1000,
    });

    const callPromise = bridge.callTool("outlook_whoami", {});

    setTimeout(() => {
      // initialize
      child.stdout.emit("data", JSON.stringify({
        jsonrpc: "2.0", id: 1, result: { protocolVersion: "2025-06-18", capabilities: {}, serverInfo: {} }
      }) + "\n");
      // tools/call (id 2)
      child.stdout.emit("data", JSON.stringify({
        jsonrpc: "2.0", id: 2,
        result: { content: [{ type: "text", text: '{"email":"test@example.com"}' }], isError: false }
      }) + "\n");
    }, 5);

    const result = await callPromise;
    expect(result.isError).toBe(false);
    expect(result.content[0].text).toContain("test@example.com");
  });
});
EOF
```

- [ ] **Step 2: Run the test (already passes — `callTool` is implemented)**

```bash
npx vitest run test/bridge.test.ts
```

Expected: both tests PASS.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "test(bridge): callTool forwards tools/call and returns content"
```

---

## Task 5: Static tool catalog fallback (for offline plugin load)

**Files:**
- Create: `src/tool-catalog.ts`
- Create: `test/catalog.test.ts`

- [ ] **Step 1: Write failing snapshot test for `STATIC_TOOLS`**

```bash
cat > test/catalog.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { STATIC_TOOLS } from "../src/tool-catalog.js";

describe("STATIC_TOOLS", () => {
  it("contains all 52 expected outlook_ tool names", () => {
    expect(STATIC_TOOLS).toHaveLength(52);
    for (const name of STATIC_TOOLS) {
      expect(name).toMatch(/^outlook_/);
    }
  });

  it("matches contracts.tools in manifest", async () => {
    const manifest = await import("../openclaw.plugin.json", { assert: { type: "json" } });
    const declared = (manifest.default as any).contracts.tools as string[];
    expect(new Set(STATIC_TOOLS)).toEqual(new Set(declared));
  });
});
EOF
```

- [ ] **Step 2: Run test — expect FAIL (no `tool-catalog.ts` yet)**

```bash
npx vitest run test/catalog.test.ts
```

Expected: FAIL with "Cannot find module '../src/tool-catalog.js'".

- [ ] **Step 3: Write `src/tool-catalog.ts` with the 52 names from the manifest**

```bash
cat > src/tool-catalog.ts <<'EOF'
// Static list of tool names exposed by outlook-mcp v1.5.3.
// Source of truth: openclaw.plugin.json `contracts.tools`.
// Used as fallback when the bridge probe fails at plugin-load time.
// Schemas for these tools are discovered at runtime via tools/list.

export const STATIC_TOOLS = [
  "outlook_auth_status",
  "outlook_list_inbox",
  "outlook_read_message",
  "outlook_search_mail",
  "outlook_list_folders",
  "outlook_list_thread",
  "outlook_send_message",
  "outlook_reply",
  "outlook_forward",
  "outlook_move_message",
  "outlook_delete_message",
  "outlook_mark_read",
  "outlook_flag_message",
  "outlook_categorize_message",
  "outlook_reclassify_message",
  "outlook_create_folder",
  "outlook_rename_folder",
  "outlook_delete_folder",
  "outlook_list_drafts",
  "outlook_create_draft",
  "outlook_update_draft",
  "outlook_send_draft",
  "outlook_delete_draft",
  "outlook_list_attachments",
  "outlook_download_attachment",
  "outlook_send_with_attachments",
  "outlook_batch_triage",
  "outlook_copy_message",
  "outlook_list_calendars",
  "outlook_list_events",
  "outlook_get_event",
  "outlook_create_event",
  "outlook_update_event",
  "outlook_delete_event",
  "outlook_rsvp",
  "outlook_list_task_lists",
  "outlook_list_tasks",
  "outlook_create_task",
  "outlook_update_task",
  "outlook_complete_task",
  "outlook_delete_task",
  "outlook_list_contacts",
  "outlook_get_contact",
  "outlook_search_contacts",
  "outlook_create_contact",
  "outlook_update_contact",
  "outlook_delete_contact",
  "outlook_list_accounts",
  "outlook_switch_account",
  "outlook_whoami",
  "outlook_list_categories",
  "outlook_get_mail_tips",
] as const;

export type StaticToolName = (typeof STATIC_TOOLS)[number];
EOF
```

- [ ] **Step 4: Run the test**

```bash
npm run build
npx vitest run test/catalog.test.ts
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: static tool name list mirrors manifest contracts.tools"
```

---

## Task 6: Wire bridge into plugin entry with dynamic tool registration

**Files:**
- Modify: `src/index.ts` (full replacement)
- Modify: `test/index.test.ts` (extend)

- [ ] **Step 1: Extend the entry test for tool registration**

```bash
cat > test/index.test.ts <<'EOF'
import { describe, it, expect, vi } from "vitest";

describe("plugin entry", () => {
  it("exports a default with id 'outlook'", async () => {
    const mod = await import("../src/index.js");
    const entry = mod.default as any;
    expect(entry).toBeDefined();
    expect(entry.id).toBe("outlook");
    expect(typeof entry.register).toBe("function");
  });

  it("calls registerTool for every static tool name when register() runs", async () => {
    const mod = await import("../src/index.js");
    const entry = mod.default as any;

    const registered: string[] = [];
    const fakeApi = {
      pluginConfig: {},
      logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn() },
      registerTool: (descriptor: any) => {
        registered.push(descriptor.name);
      },
      on: vi.fn(),
    };

    entry.register(fakeApi);

    const { STATIC_TOOLS } = await import("../src/tool-catalog.js");
    expect(registered.sort()).toEqual([...STATIC_TOOLS].sort());
  });
});
EOF
```

- [ ] **Step 2: Run — expect FAIL (current index.ts is a no-op)**

```bash
npx vitest run test/index.test.ts
```

Expected: FAIL (second test). First test still passes.

- [ ] **Step 3: Rewrite `src/index.ts` to register all static tools, deferring schema discovery and execution to the bridge**

```bash
cat > src/index.ts <<'EOF'
import path from "node:path";
import os from "node:os";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { MCPBridge } from "./bridge.js";
import { STATIC_TOOLS } from "./tool-catalog.js";
import type { McpToolDescriptor } from "./types.js";

const DEFAULT_OUTLOOK_MCP_PATH = path.join(os.homedir(), "ClaudeCode", "outlook-mcp");
const DEFAULT_UV_PATH = path.join(os.homedir(), ".local", "bin", "uv");

export default definePluginEntry({
  id: "outlook",
  name: "Outlook",
  description: "Outlook tools bridged from the outlook-mcp Python server.",
  register(api) {
    const cfg = (api.pluginConfig ?? {}) as {
      outlookMcpPath?: string;
      uvPath?: string;
      spawnTimeoutMs?: number;
    };

    const bridge = new MCPBridge({
      uvPath: cfg.uvPath || DEFAULT_UV_PATH,
      outlookMcpPath: cfg.outlookMcpPath || DEFAULT_OUTLOOK_MCP_PATH,
      spawnTimeoutMs: cfg.spawnTimeoutMs ?? 30000,
      logger: {
        info: (m) => api.logger?.info?.(`[outlook] ${m}`),
        warn: (m) => api.logger?.warn?.(`[outlook] ${m}`),
        error: (m) => api.logger?.error?.(`[outlook] ${m}`),
      },
    });

    // Schemas are discovered the first time the agent uses any outlook tool.
    // Until then, we register every tool with an empty pass-through schema so the
    // names show up in `openclaw plugins inspect outlook` and in the agent's tools[].
    let schemaCache: Map<string, McpToolDescriptor> | null = null;
    let schemaPromise: Promise<Map<string, McpToolDescriptor>> | null = null;

    const loadSchemas = async (): Promise<Map<string, McpToolDescriptor>> => {
      if (schemaCache) return schemaCache;
      if (schemaPromise) return schemaPromise;
      schemaPromise = (async () => {
        const tools = await bridge.listTools();
        const map = new Map<string, McpToolDescriptor>();
        for (const t of tools) map.set(t.name, t);
        schemaCache = map;
        return map;
      })();
      return schemaPromise;
    };

    for (const name of STATIC_TOOLS) {
      api.registerTool({
        name,
        description: `Outlook tool (${name}). Detailed parameters discovered at first call.`,
        parameters: { type: "object", additionalProperties: true, properties: {} },
        async execute(_id: string, params: Record<string, unknown>) {
          // Best-effort schema warmup; failures here don't block the call.
          try {
            await loadSchemas();
          } catch (err) {
            api.logger?.warn?.(`[outlook] schema warmup failed: ${(err as Error).message}`);
          }
          const result = await bridge.callTool(name, params ?? {});
          return {
            content: result.content,
            isError: !!result.isError,
          };
        },
      });
    }

    api.logger?.info?.(`[outlook] registered ${STATIC_TOOLS.length} tools`);
  },
});
EOF
```

- [ ] **Step 4: Build and run all tests**

```bash
npm run build
npx vitest run
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: register all 52 outlook_* tools at plugin load; bridge calls on demand"
```

---

## Task 7: Integration test against the real outlook-mcp subprocess

**Files:**
- Create: `test/integration.test.ts`

- [ ] **Step 1: Write integration test that hits `outlook_auth_status` (no auth needed; tool returns whether we are authed)**

```bash
cat > test/integration.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

import { MCPBridge } from "../src/bridge.js";

const UV_PATH = path.join(os.homedir(), ".local", "bin", "uv");
const OUTLOOK_MCP_PATH = path.join(os.homedir(), "ClaudeCode", "outlook-mcp");

const canRun = fs.existsSync(UV_PATH) && fs.existsSync(OUTLOOK_MCP_PATH);

describe.skipIf(!canRun)("integration: real outlook-mcp subprocess", () => {
  it("lists tools/list and reports outlook_auth_status without crashing", async () => {
    const bridge = new MCPBridge({
      uvPath: UV_PATH,
      outlookMcpPath: OUTLOOK_MCP_PATH,
      spawnTimeoutMs: 30_000,
    });

    try {
      const tools = await bridge.listTools();
      expect(tools.length).toBeGreaterThanOrEqual(50);

      const result = await bridge.callTool("outlook_auth_status", {});
      expect(result.isError).toBe(false);
      expect(result.content[0].type).toBe("text");
      const parsed = JSON.parse(result.content[0].text!);
      expect(typeof parsed.authenticated).toBe("boolean");
    } finally {
      await bridge.dispose();
    }
  }, 60_000);
});
EOF
```

- [ ] **Step 2: Run the integration test**

```bash
npx vitest run test/integration.test.ts
```

Expected: PASS if `uv` and `outlook-mcp` are present (the test self-skips otherwise).

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "test: integration roundtrip — spawn real outlook-mcp, list tools, call auth_status"
```

---

## Task 8: Install in local openclaw via `plugins install --link`

**Files:** (none — install via CLI)

- [ ] **Step 1: Build the plugin**

```bash
cd ~/ClaudeCode/openclaw-outlook-plugin
npm run build
```

Expected: `dist/index.js`, `dist/bridge.js`, `dist/tool-catalog.js`, `dist/types.js` created.

- [ ] **Step 2: Install as linked dev plugin**

```bash
openclaw plugins install --link ~/ClaudeCode/openclaw-outlook-plugin
```

Expected output includes `Installed plugin: outlook`.

- [ ] **Step 3: Restart the gateway**

```bash
openclaw gateway restart
sleep 12
```

- [ ] **Step 4: Verify plugin is loaded**

```bash
openclaw plugins inspect outlook
```

Expected: `Status: loaded`, `Origin: linked` or similar, 52 tools listed under capabilities.

- [ ] **Step 5: Remove the conflicting `mcp.servers.outlook` entry so there are not two registrations**

Edit `~/.openclaw/openclaw.json` and remove the `outlook` key from `mcp.servers`, leaving any other servers (e.g. `gmail`) intact.

```bash
python3 - <<'PY'
import json
p = "/Users/neo/.openclaw/openclaw.json"
d = json.load(open(p))
servers = d.get("mcp", {}).get("servers", {})
if "outlook" in servers:
    del servers["outlook"]
    json.dump(d, open(p, "w"), indent=2)
    print("removed mcp.servers.outlook")
else:
    print("already removed")
PY
openclaw gateway restart
sleep 12
```

- [ ] **Step 6: Confirm `mcp list` no longer mentions outlook and `plugins inspect outlook` still shows loaded**

```bash
openclaw mcp list
openclaw plugins inspect outlook
```

Expected: `mcp list` shows only remaining MCP servers (e.g. `gmail`); `plugins inspect outlook` still `Status: loaded`.

- [ ] **Step 7: Commit (capture install steps in README for repeatability)**

```bash
cd ~/ClaudeCode/openclaw-outlook-plugin
# README already documents this — no code change. No commit needed unless README updated.
```

(No-op step if README is already current. Skip the commit.)

---

## Task 9: End-to-end agent verification — wire capture proof

**Files:** (none — test via the agent + debug proxy)

- [ ] **Step 1: Re-enable the OpenClaw debug proxy as established earlier in this conversation**

```bash
openclaw proxy start --port 18790 > /tmp/oc-proxy-final.log 2>&1 &
sleep 4
cat >> /Users/neo/.openclaw/service-env/ai.openclaw.gateway.env <<'EOF'
export OPENCLAW_DEBUG_PROXY_ENABLED='1'
export OPENCLAW_DEBUG_PROXY_URL='http://127.0.0.1:18790'
EOF
launchctl bootout gui/501/ai.openclaw.gateway
sleep 2
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
sleep 15
curl -s -m 5 -o /dev/null -w "gateway: %{http_code}\n" http://127.0.0.1:18789/
```

Expected: `gateway: 200`.

- [ ] **Step 2: Trigger a single agent turn requesting Outlook**

Send Neo via iMessage:

> "What are my 5 most recent inbox emails?"

Wait ~90 seconds for the agent to process.

- [ ] **Step 3: Inspect the captured outbound request body for `outlook_*` entries**

```bash
LAST_BLOB=$(sqlite3 ~/.openclaw/debug-proxy/capture.sqlite "
SELECT data_blob_id FROM capture_events
WHERE host LIKE '%openrouter%' AND direction='outbound' AND kind='request' AND data_blob_id != ''
ORDER BY ts DESC LIMIT 1;")
echo "blob: $LAST_BLOB"
gunzip -c ~/.openclaw/debug-proxy/blobs/${LAST_BLOB}.bin.gz > /tmp/wire-final.json
python3 - <<'PY'
import json
b = json.load(open("/tmp/wire-final.json"))
names = [t["function"]["name"] for t in b.get("tools", [])]
outlook = [n for n in names if n.startswith("outlook_")]
print(f"total tools: {len(names)}")
print(f"outlook_*  : {len(outlook)}")
print("first 5 outlook tools:", outlook[:5])
PY
```

Expected: `outlook_*` count is ≥ 50. This is the proof.

- [ ] **Step 4: Tear down the debug proxy**

```bash
PID=$(lsof -nP -iTCP:18790 -sTCP:LISTEN | awk 'NR==2 {print $2}')
[ -n "$PID" ] && kill "$PID"
sed -i.bak '/OPENCLAW_DEBUG_PROXY/d' /Users/neo/.openclaw/service-env/ai.openclaw.gateway.env
rm /Users/neo/.openclaw/service-env/ai.openclaw.gateway.env.bak
launchctl bootout gui/501/ai.openclaw.gateway
sleep 2
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
sleep 12
curl -s -m 5 -o /dev/null -w "gateway clean: %{http_code}\n" http://127.0.0.1:18789/
```

Expected: `gateway clean: 200`.

- [ ] **Step 5: No commit needed — verification only.**

---

## Task 10: Write LESSONS.md note + post to issue #80909

**Files:**
- Create: `LESSONS.md` (in the plugin repo)
- Comment: GitHub issue #80909

- [ ] **Step 1: Write the lessons file**

```bash
cat > ~/ClaudeCode/openclaw-outlook-plugin/LESSONS.md <<'EOF'
# Lessons learned

## Why this plugin exists

OpenClaw 5.x (`2026.4.26 → 2026.5.7` confirmed) drops configured `mcp.servers` tools from the agent's outbound `tools[]` array. Issue: https://github.com/openclaw/openclaw/issues/80909.

## Why the bridge approach works

OpenClaw's native `api.registerTool()` path is **not** broken. Built-in tools (`read`, `write`, `exec`, `web_search`) appear in `tools[]` reliably across all tested versions. This plugin uses `api.registerTool()` directly and manages its own JSON-RPC subprocess — the broken `mcp.servers` bridge is never involved.

## Architectural alternative considered

A pure TypeScript port of `outlook-mcp` was considered (option B in the original plan) but rejected because:
- Maintaining two implementations splits the Graph API surface.
- The Python `outlook-mcp` already has 403 passing tests and is in use by Claude Code / Cursor / Codex.
- A port doesn't add capability — only language consistency — and the bridge is ~200 lines of glue.

## When this plugin should be retired

If OpenClaw fixes the `mcp.servers → tools[]` regression, this plugin can be deprecated in favor of the original `mcp.servers.outlook` entry. The wrapper adds latency (subprocess spawn per gateway start, single fork) but no functional capability over the native MCP path.
EOF
git -C ~/ClaudeCode/openclaw-outlook-plugin add LESSONS.md
git -C ~/ClaudeCode/openclaw-outlook-plugin commit -m "docs: lessons learned and retirement criteria"
```

- [ ] **Step 2: Post a status comment on issue #80909**

Draft body:

```
Update for anyone hitting this: I built a small bridge plugin (`@mpalermiti/openclaw-outlook`) that exposes the same `outlook_*` tools through OpenClaw's native `api.registerTool()` path. Wire capture confirms 50+ `outlook_*` entries now appear in the agent's outbound `tools[]`. Plugin source: https://github.com/mpalermiti/openclaw-outlook-plugin. This is a workaround, not a fix — the `mcp.servers` regression is still real. Leaving here in case it helps other users while #80909 awaits triage.
```

```bash
gh issue comment 80909 --repo openclaw/openclaw --body-file - <<'EOF'
Update for anyone hitting this: I built a small bridge plugin (`@mpalermiti/openclaw-outlook`) that exposes the same `outlook_*` tools through OpenClaw's native `api.registerTool()` path. Wire capture confirms 50+ `outlook_*` entries now appear in the agent's outbound `tools[]`. Plugin source: https://github.com/mpalermiti/openclaw-outlook-plugin. This is a workaround, not a fix — the `mcp.servers` regression is still real. Leaving here in case it helps other users while #80909 awaits triage.
EOF
```

- [ ] **Step 3: Push to GitHub**

```bash
cd ~/ClaudeCode/openclaw-outlook-plugin
gh repo create mpalermiti/openclaw-outlook-plugin --public --source=. --remote=origin --push
```

Expected: repo created on GitHub, main branch pushed.

---

## Optional follow-up tasks (not part of MVP)

These are deliberately **not** in the MVP plan. Open separate plans if/when warranted:

- **Publish to ClawHub** — `clawhub package publish ...` once the plugin has been used for a week without regressions.
- **Subprocess pool / multi-instance** — currently one subprocess per gateway. If multiple agents need parallel Outlook calls, pool would help. Not needed yet.
- **Schema-cache prewarm** — fetch `tools/list` at plugin load and replace the empty pass-through schemas with the real ones immediately. Currently warmup happens on first call. Only matters if model behavior is sensitive to detailed parameter schemas.
- **Native TypeScript port** — kept as an option. The bridge keeps it cheap to switch later.

## Risks and unknowns

| Risk | Likelihood | Mitigation |
|---|---|---|
| OpenClaw `api.registerTool` interface drift across 5.x patches | medium | Pin `peerDependencies.openclaw >= 2026.5.7`; CI runs against the latest stable on a schedule |
| Pass-through `parameters: {additionalProperties: true}` confuses the model | low | Real schemas are loaded lazily via `loadSchemas()`. If quality drops, switch to eager loading (move warmup into `register()`). |
| Subprocess token cache race on first auth | low | Single subprocess per gateway makes races impossible. If pooled later, use a file lock. |
| `uv run outlook-mcp` cold-start latency on first call | known | Tolerable — sub-second on warm token, ~3s on cold token. Document in README; pre-warm option available. |
| OpenClaw fixes `mcp.servers` upstream and renders this plugin redundant | desired | Plugin can be cleanly uninstalled via `openclaw plugins uninstall outlook` and the original `mcp.servers.outlook` entry restored. |

## Acceptance criteria

The MVP is done when **all** of these hold:

1. `npm run test` is green (all unit + integration tests pass).
2. `openclaw plugins inspect outlook` shows `Status: loaded` and 52 tools.
3. A single agent turn requesting Outlook content triggers a `tools/call` to the subprocess (cost-tracker shows ≥2 LLM calls per run — one to emit `tool_use`, one to synthesize).
4. A debug-proxy wire capture shows `outlook_*` tool names in `body.tools[]`.
5. Plugin uninstall (`openclaw plugins uninstall outlook`) is clean — no residue in `~/.openclaw/openclaw.json`.
