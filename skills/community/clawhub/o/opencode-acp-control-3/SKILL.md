---
name: opencode-acp-control
description: Use when an AI agent needs to start, drive, or monitor an OpenCode CLI session programmatically over the Agent Client Protocol (ACP). Triggers include requests to "spawn OpenCode", "control OpenCode from another agent", "automate OpenCode over JSON-RPC", "resume an OpenCode session", or any task that requires the agent to act as an ACP client rather than an interactive user. Provides the JSON-RPC 2.0 framing, session lifecycle, polling strategy, permission-request handling, and update detection needed to wrap OpenCode from inside another AI agent.
metadata:
  version: "0.3.0"
  author: "Bastian Berrios <berriosbastian@gmail.com>"
  license: "MIT"
  github_url: "https://github.com/berriosb/Opencode-Acp-Control"
---

# OpenCode ACP Skill

Drive an OpenCode CLI session over the Agent Client Protocol (ACP).

## When to use this skill

Use it when the calling agent must:

- Start an OpenCode process and talk to it programmatically (not as a human at
  a terminal).
- Drive multi-turn coding sessions, including prompt → stream → cancel loops.
- Resume a previous OpenCode session by ID.
- Detect and trigger OpenCode auto-updates.

Do **not** use it for direct file editing, one-off shell commands, or any
task that does not require the Agent Client Protocol.

## Quick Reference

| Action | Generic tool call |
|---|---|
| Start OpenCode | `terminal(command: "opencode acp --cwd /path/to/project", background: true)` |
| Send JSON-RPC frame | `process.write(processId, "<frame>\n")` |
| Read available output | `process.poll(processId)` (repeat every ~2s) |
| Stop OpenCode | `process.kill(processId)` |
| List past sessions | `terminal(command: "opencode session list", workdir: "<project>")` |
| Get current version | `terminal(command: "opencode --version")` |
| Prompt the user | `ask_user(question, options)` |

The calling agent must map these generic names to its own platform (Hermes,
Clawdbot, etc.). See `README.md` for the mapping table.

## Protocol Rules

- Wire format: **JSON-RPC 2.0**, **newline-delimited** (one JSON object per
  line, each frame terminated by `\n`). Not LSP `Content-Length`.
- Direction: requests are agent → OpenCode (stdin). Responses and server
  notifications arrive on stdout.
- IDs: every request carries an integer `id`; the calling agent increments
  monotonically starting at 0. Notifications have no `id` and never produce a
  response.
- Sessions are opaque: the `sessionId` returned by `session/new` is the only
  reference; treat it as a string.
- Capabilities: declare `fs.readTextFile`, `fs.writeTextFile`, and `terminal`
  in the `initialize` handshake.

## Standard Workflow

### 1. Start

```
terminal(
  command: "opencode acp --cwd /path/to/project",
  background: true,
  workdir: "/path/to/project"
)
```

Save the returned `processId`. All subsequent frames go through it.

### 2. Initialize

```json
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{
  "protocolVersion":1,
  "clientCapabilities":{
    "fs":{"readTextFile":true,"writeTextFile":true},
    "terminal":true
  },
  "clientInfo":{
    "name":"opencode-acp-control",
    "title":"OpenCode ACP Control",
    "version":"0.3.0"
  }
}}
```

Expect `result.protocolVersion: 1`.

### 3. Create session

```json
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{
  "cwd":"/path/to/project",
  "mcpServers":[]
}}
```

Save `result.sessionId` (e.g. `"sess_abc123"`).

### 4. Send prompt

```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{
  "sessionId":"sess_abc123",
  "prompt":[{"type":"text","text":"List the TypeScript files in this repo."}]
}}
```

### 5. Stream the response

Poll stdout every ~2s until a response arrives whose `id` matches your request
and whose `result.stopReason` is set. While polling you will also receive
notifications:

```json
{"jsonrpc":"2.0","method":"session/update","params":{...}}
```

Collect them in order — they make up the agent's streamed output.

### 6. Cancel (when needed)

```json
{"jsonrpc":"2.0","method":"session/cancel","params":{"sessionId":"sess_abc123"}}
```

No response is sent for a cancel — it is a notification.

### 7. Handle permission requests

OpenCode asks for confirmation before running shell commands or editing files
by sending a server-to-client request:

```json
{"jsonrpc":"2.0","id":12,"method":"requestPermission","params":{
  "sessionId":"sess_abc123",
  "toolCall":{"toolCallId":"call_1","status":"pending",
              "title":"bash","rawInput":{"command":"npm install"},"kind":"bash"}
}}
```

Prompt the user, then respond with the matching `id`:

```json
{"jsonrpc":"2.0","id":12,"result":{"reply":"once"}}      // allow once
{"jsonrpc":"2.0","id":12,"result":{"reply":"always"}}    // allow for the session
{"jsonrpc":"2.0","id":12,"result":{"reply":"reject"}}    // deny
```

## State to Track

For each OpenCode instance the calling agent holds:

| Field | Source |
|---|---|
| `processId` | Returned by the `terminal(background:true)` call |
| `sessionId` | Returned by `session/new` (OpenCode-internal) |
| `nextId` | Integer counter for the next request, starting at 0 |
| `stopReason` | Last terminal reason observed (`end_turn`, `cancelled`, `max_tokens`) |

## Polling and Timeout Strategy

- Interval: **2 seconds** between `process.poll` calls.
- Maximum wait per prompt: **5 minutes** (150 polls). Treat as timeout beyond.
- An empty poll response means the agent is still thinking — keep polling.
- A malformed line on stdout is logged and skipped; do not abort on parse
  errors alone.

## Resume Session

1. `terminal("opencode session list", workdir: "<project>")` returns a table of
   `{id, updated, messages}`.
2. `ask_user` to pick one.
3. `terminal("opencode acp --cwd <project>", background:true)` to restart.
4. `initialize` (id=0).
5. `session/load` with the chosen id, plus `cwd` and `mcpServers`:

   ```json
   {"jsonrpc":"2.0","id":1,"method":"session/load","params":{
     "sessionId":"sess_abc123","cwd":"/path/to/project","mcpServers":[]
   }}
   ```

OpenCode streams the full conversation history back through `session/update`
notifications.

## Failure Modes

| Symptom | Likely cause | Action |
|---|---|---|
| Empty polls for >5 min | Long agent thinking, model stall, or network drop | Cancel + restart |
| `parse error` on stdout | Garbled binary output or partial frame | Skip the line, continue |
| Process exits unexpectedly | OpenCode crashed | Inspect stderr, restart |
| `initialize` rejects `protocolVersion` | OpenCode < v1.1.0 or client drift | Upgrade OpenCode, align `clientInfo.version` |
| `requestPermission` keeps arriving | Session is in a tool-call loop | Cancel, narrow the prompt |
| `session/load` 404s | Stale or deleted session id | Fall back to `session/new` |

## Update Procedure

OpenCode auto-updates on restart. To check and trigger an update:

1. `terminal("opencode --version")` → current version.
2. `web_fetch("https://github.com/sst/opencode/releases/latest")` → latest tag
   in the redirect URL.
3. Compare versions. If newer:
   - `process(action:"list")` to find every running `opencode acp` process.
   - `process.kill(processId)` for each.
   - Wait ~2 seconds.
   - `terminal("opencode acp", background:true)` to restart and trigger the
     auto-download.
4. Verify with `opencode --version` again. If still old, fall back to a manual
   install (review the installer script before piping `curl | bash`):

   ```
   curl -fsSL https://opencode.ai/install | bash
   ```

## Implementation Notes

- `cwd` must be absolute; normalize before sending.
- Serialize JSON deterministically (`sort_keys=True` if possible) to make log
  diffs stable.
- Treat stderr separately from stdout if your platform exposes it — ACP
  frames never appear on stderr.
- When the host agent runs in a sandbox, `cwd` must be inside the sandbox;
  the ACP server inherits the calling agent's filesystem access.
- Session ids are opaque strings; do not parse them.
- The first `initialize` after a process start must complete before any
  other request — JSON-RPC servers reject out-of-order calls.

## See also

- `examples/acp_demo.py` — runnable end-to-end demo with `--dry-run` and
  `--no-prompt` modes.
- `README.md` — quick start and tool-platform mapping.
- `CHANGELOG.md` — release notes.
- ACP spec: <https://agentclientprotocol.com/llms.txt>
- OpenCode: <https://opencode.ai>