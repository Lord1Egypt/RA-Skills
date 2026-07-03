---
name: "nvimclaw"
description: "Bridge to Neovim over OpenClaw's node plugin. nvim.*: buffer R/W, Ex commands (surgical :substitute), cursor/selection/diagnostics, chat-to-session messaging."
requires:
  nvimclaw: ">=0.1.0"
---

# nvimclaw — talk to a Neovim instance over the OpenClaw bridge

Use this skill whenever the user wants the agent to read, edit, or inspect something in their **live Neovim**. The bridge gives the agent access to buffers, the Ex command line (notably `:substitute`), cursor state, selections, and diagnostics — directly, without copy/paste or asking where files are.

nvimclaw is the **Neovim equivalent of `vscode.openclaw`**: it registers a Neovim instance as an *OpenClaw node* and exposes a `nvim.*` command surface the agent can invoke. It also exposes a **surface** (a chat buffer inside Neovim) so the user can summon the same agent session from inside the editor. Session, persona, and memory carry across surfaces.

The tool surface covers any file in any configured workspace — Markdown, Lua, Python, prose, configuration files, or anything else Neovim is editing live.

## When this skill applies

Trigger on any of:

- "edit this file in my Neovim", "fix this in Vim", "rename X to Y in Neovim"
- "what's open in my Neovim", "what file am I on", "what's focused in Vim"
- "run a substitution in Neovim", "do `:s/.../.../g` in my buffer"
- "send a message from Neovim to my session", "open the Neovim chat"
- "what's the cursor position in Neovim", "show me the diagnostics for this file"
- "open this file in Neovim", "make this the active buffer"

Do **not** use for files outside Neovim's `workspace_root` — read them locally with `read` instead.

## Setup, once — never re-derive this

nvimclaw is a Neovim plugin that connects to the OpenClaw gateway with two roles:

- an operator-scoped chat surface for `sessions.send`
- a node-scoped tool surface for `node.invoke.request`

Operator chat can connect with the local gateway token. The node tool surface also needs gateway trust: `gateway.nodes.allowCommands` must include the `nvim.*` command names, and the `nvimclaw node` pairing must be approved once before commands become effective.

1. **Install the plugin** (lazy.nvim):
   ```lua
   -- lua/plugins/nvimclaw.lua
   return {
     "utrumsit/nvimclaw",
     event = "VeryLazy",
     config = function()
       require("nvimclaw").setup({
         -- session to send messages to; default is "agent:main"
         session = "agent:main",
       })
     end,
   }
   ```

2. **Install the skill** (this file, as an agent):
   ```bash
   openclaw skills install nvimclaw
   ```

3. **Gateway token.** The plugin reads the OpenClaw gateway token from the default location (`~/.openclaw/openclaw.json`, the standard `openclaw` CLI config) or the `OPENCLAW_GATEWAY_TOKEN` env var.

4. **First launch.** On first run the plugin generates an Ed25519 device-identity keypair at `~/.local/state/nvimclaw/identity.json` (mode 0600), opens an operator WebSocket for chat, then opens a node-role WebSocket for tools after registering commands.

5. **Node approval and command allowlist.** If `openclaw nodes status` says `approval pending`, the user or operator must run the displayed `openclaw nodes approve <requestId>`. If `nodes invoke` says `node command not allowed`, the gateway config needs `gateway.nodes.allowCommands` entries for the `nvim.*` commands. After changing that config, restart the gateway.

6. **Multiple Neovim instances** coexist fine. Pick the right one from `openclaw nodes status` and confirm with `nvim.describe`.

## Health check — always do this first

Before invoking any `nvim.*` command, verify the node is live.

Inside Neovim:

```vim
:OpenClawStatus
```

This shows separate chat and node connection states, `node_id`, gateway host, and current session. Healthy means `chat: connected`, `node: connected`, and a populated `node_id`.

From the shell:

```bash
openclaw nodes status
```

Look for the nvimclaw node entry with `paired · connected · approved` and cap `nvim`. Capture its `nodeId` once and reuse it; **nodeIds rotate only when the identity keypair is wiped, which doesn't happen on normal restarts.**

If `Connected: 0` or the node is missing:

1. **Stop and tell the user.** Don't try to invoke; you will get cryptic `gateway_timeout` or `auth_expired` errors.
2. Likely causes: Neovim closed, gateway down, token rotated, or `~/.local/state/nvimclaw/identity.json` was deleted.
3. The fix is usually `:OpenClawReconnect` inside Neovim, restarting Neovim, approving a pending node pairing, or adding missing `nvim.*` commands to `gateway.nodes.allowCommands`.

## The one pattern: invoke

All buffer/file/editor commands go through one gateway call:

```bash
openclaw nodes invoke \
  --node <NODE_ID> \
  --command nvim.<command> \
  --params '<json>'
```

`--params` is a JSON object. The plugin returns JSON wrapped in `{ok, nodeId, command, payload, payloadJSON}`. Read `payload` for the answer.

Discover which node is the right one with `nvim.describe` (see §Discovery). Never hardcode a `nodeId` in agent prompts — call `openclaw nodes status` each session.

## The `nvim.*` tool surface

Every command takes a JSON params object and returns a JSON result. Tools are split into two tiers:

- **`safe` — read-only. Available by default after pairing.** No opt-in required.
- **`privileged` — mutating. Requires `setup({ tools = { tier = "privileged" } })` or `:OpenClawTools privileged` per session.**

**Unknown params are rejected** (strict schema). Unknown commands return `{error: "unknown_command", command}`. The normative error enum is in §Gotchas.

### Tier summary

| Tier | Commands |
|---|---|
| safe | `nvim.buffer.current`, `nvim.buffer.read`, `nvim.search`, `nvim.cursor.get`, `nvim.selection.get`, `nvim.diagnostics.get`, `nvim.describe` |
| privileged | `nvim.buffer.write`, `nvim.buffer.replace_lines`, `nvim.buffer.open`, `nvim.buffer.reload`, `nvim.ex.command`, `nvim.ex.substitute`, `nvim.cursor.set` |

### Current-buffer rule

When the user says "this file", "the buffer", "what I'm looking at", or does not name an exact path, **call `nvim.buffer.current` first**. Do not infer from `cat`, process lists, cwd, or similarly named files. If the user's cursor is in the `nvimclaw://chat` split, the plugin returns the last normal file buffer as the agent target instead of the chat buffer. Use the returned `buffer_id`, `path`, `changedtick`, and `cursor` for the next operation.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.current \
  --params '{"include_content": true, "max_lines": 200}'
```

If `path` is non-empty, prefer it for later calls. If `path` is empty, the buffer is unnamed or scratch-like; use the returned `buffer_id` for later calls. If the current buffer is large, call `nvim.buffer.current` without `include_content`, then call `nvim.buffer.read` with the returned `path` or `buffer_id`.

### `nvim.buffer.read` (safe)

Read a buffer's contents from disk or Neovim's in-memory copy. Use this for prose, code, and any file in the workspace.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.read \
  --params '{"path": "drafts/example.md"}'

# For unnamed buffers:
openclaw nodes invoke --node <N> --command nvim.buffer.read \
  --params '{"buffer_id": 1}'
```

Params: `{path?: string, buffer_id?: number}` — `path` is relative to `workspace_root`; use `buffer_id` for unnamed buffers. Returns:

```json
{
  "buffer_id": 7,
  "path": "drafts/example.md",
  "content": "Schopenhauer is hilarius. ...",
  "lines": 142,
  "language": "markdown",
  "changedtick": 17
}
```

`changedtick` is the optimistic-lock token — pass it back as `expected_changedtick` on any privileged write.

If both `path` and `buffer_id` are omitted, `nvim.buffer.read` reads the current agent target buffer.

### `nvim.buffer.write` (privileged)

Full-buffer overwrite. Alias for `replace_lines(0, -1, lines)` with the same conflict semantics. Provided for agents trained on `vscode.file.write`; **prefer `nvim.ex.substitute` or `nvim.buffer.replace_lines` when possible** — they preserve Vim's undo history per edit.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.write \
  --params '{
    "path": "drafts/example.md",
    "content": "Schopenhauer is hilarious. ...",
    "expected_changedtick": 17
  }'
```

For unnamed buffers, pass `"buffer_id": <id>` instead of `path`.

Params: `{path?: string, buffer_id?: number, content?: string, lines?: [string], expected_changedtick?: number, expected_line_hash?: string}`.

Returns `{ok: true}` on success or `{ok: false, error: {code: "conflict", current_changedtick, sample_lines}}` on tick mismatch (see §Conflict handling).

### `nvim.buffer.replace_lines` (privileged)

Targeted line-range replace. Best for surgical edits with hard bounds.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.replace_lines \
  --params '{
    "path": "drafts/example.md",
    "start": 0, "end": 2,
    "lines": ["Schopenhauer is hilarious.", "He wrote The World as Will..."],
    "expected_changedtick": 17,
    "expected_line_hash": "a3f2..."
  }'
```

For unnamed buffers, pass `"buffer_id": <id>` instead of `path`.

Params: `{path?, buffer_id?, start: int, end: int, lines: [string], expected_changedtick?, expected_line_hash?}`.

Returns `{ok: true}` or a conflict. `expected_line_hash` is the SHA256 of the affected line range joined by `\n` — use it for higher-stakes edits where the tick alone is not authoritative enough (see §Gotchas).

### Appending Text

To append a paragraph, do **not** use `nvim.ex.command` or `:bufdo`. Use `nvim.buffer.replace_lines` with the insertion point at the end of the buffer.

1. Call `nvim.buffer.current` or `nvim.buffer.read`.
2. Keep `buffer_id`, `path`, `line_count`, and `changedtick`.
3. Insert at `start = line_count`, `end = line_count`.
4. For a new paragraph after existing text, include a blank line before the paragraph.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.replace_lines \
  --params '{
    "buffer_id": 1,
    "start": 1,
    "end": 1,
    "lines": ["", "A new paragraph goes here."],
    "expected_changedtick": 17
  }'
```

For a named buffer, use `"path": "drafts/example.md"` instead of `buffer_id`. For an unnamed buffer, use `buffer_id`; `path` will be empty.

### `nvim.buffer.open` (privileged)

Open a path in Neovim, making it the active buffer. Use to load a file from a session-message context into the editor so the user can see what the agent is about to edit.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.open \
  --params '{"path": "drafts/example.md"}'
```

Params: `{path: string}`. Returns `{ok: true, buffer_id: 7}`.

### `nvim.buffer.reload` (privileged)

Reload a buffer from disk after an external fallback edit. Prefer real buffer tools first; they update Neovim live and do not need reload.

```bash
openclaw nodes invoke --node <N> --command nvim.buffer.reload \
  --params '{"path": "test.txt", "force": true}'
```

Params: `{path?: string, buffer_id?: number, force?: boolean}`. If `path` and `buffer_id` are omitted, reloads the current agent target buffer. `force=true` runs `:edit!`; otherwise it runs `:checktime`.

### `nvim.ex.command` (privileged)

Run an arbitrary Ex command. **This is the most powerful tool.** Pair it with `confirm: true` for destructive commands — the plugin will prompt in Neovim before running.

```bash
openclaw nodes invoke --node <N> --command nvim.ex.command \
  --params '{"cmd": "write", "confirm": false}'
```

Params: `{cmd: string, confirm?: boolean, preserve_layout?: boolean}`. `preserve_layout` defaults to `true`, so commands that temporarily switch buffers should leave existing windows showing the buffers they showed before. Returns `{ok: true, output: ""}` or `{ok: false, declined: true}` if the user dismissed the prompt.

### `nvim.ex.substitute` (privileged — the centerpiece)

Run Vim's `:substitute` against a buffer. **This is the surgical-edit primitive for prose and code.** Supports `dry_run` for a transparent preflight.

**Pattern A — dry-run preflight (always do this first for essays):**

```bash
openclaw nodes invoke --node <N> --command nvim.ex.substitute \
  --params '{
    "path": "drafts/example.md",
    "pattern": "hilarius",
    "replacement": "hilarious",
    "flags": "g",
    "dry_run": true
  }'
```

For unnamed buffers, pass `"buffer_id": <id>` instead of `path`.

Returns:

```json
{
  "matches": 1,
  "line_hash": "a3f2...",
  "sample_lines": [{"line": 1, "text": "Schopenhauer is hilarius. He wrote..."}]
}
```

**Pattern B — commit with optimistic lock:**

```bash
openclaw nodes invoke --node <N> --command nvim.ex.substitute \
  --params '{
    "path": "drafts/example.md",
    "pattern": "hilarius",
    "replacement": "hilarious",
    "flags": "g",
    "expected_changedtick": 17,
    "expected_line_hash": "a3f2..."
  }'
```

Returns `{ok: true, matches: 1, replaced: 1}`.

For unnamed buffers, pass `"buffer_id": <id>` instead of `path`.

Params: `{path?, buffer_id?, pattern, replacement, flags, expected_changedtick?, expected_line_hash?, dry_run?}`.

`flags` is the Ex flag string: `g` (global), `c` (confirm), `i` (case-insensitive), `e` (suppress errors), combinations like `"gi"`. Without flags, substitute only replaces the first match on the first matching line — pass `"g"` for "every match in the buffer".

### `nvim.search` (safe)

Find matches for a Vim regex pattern across a buffer. Returns line, column, and match text.

```bash
openclaw nodes invoke --node <N> --command nvim.search \
  --params '{"path": "drafts/example.md", "pattern": "Schopenhauer"}'
```

Params: `{path: string, pattern: string}`. Returns `{matches: [{line: 1, col: 1, text: "Schopenhauer is hilarius..."}]}`.

### `nvim.cursor.get` (safe)

Get current cursor position (line, col — both 1-indexed).

```bash
openclaw nodes invoke --node <N> --command nvim.cursor.get \
  --params '{"path": "drafts/example.md"}'
```

Params: `{path: string}`. Returns `{line: 1, col: 1}`.

### `nvim.cursor.set` (privileged)

Move the cursor. Privileged because it changes the user's view.

```bash
openclaw nodes invoke --node <N> --command nvim.cursor.set \
  --params '{"path": "drafts/example.md", "line": 12, "col": 5}'
```

Params: `{path: string, line: int, col: int}` (both 1-indexed). Returns `{ok: true}`.

### `nvim.selection.get` (safe)

Return the active visual selection (line/col inclusive ranges and the selected text).

```bash
openclaw nodes invoke --node <N> --command nvim.selection.get --params '{}'
```

Params: `{}`. Returns `{start: {line, col}, finish: {line, col}, lines: ["selected text..."]}`.

### `nvim.diagnostics.get` (safe)

Surface Vim/Neovim diagnostics for a buffer (LSP errors, warnings, syntax). Mirrors what the user sees in the sign column.

```bash
openclaw nodes invoke --node <N> --command nvim.diagnostics.get \
  --params '{"path": "src/services/coach.py"}'
```

Params: `{path: string}`. Returns `{diagnostics: [{lnum, col, severity, message, source}]}`. `severity` is 1=ERROR, 2=WARN, 3=INFO, 4=HINT.

### `nvim.describe` (safe — the discovery command)

Introspect the node: which plugin version, which protocol version, which tools are available, which surface and node IDs are bound, what is `cwd`, what is `workspace_root`.

```bash
openclaw nodes invoke --node <N> --command nvim.describe --params '{}'
```

Returns:

```json
{
  "plugin_version": "0.1.0",
  "protocol_version": 1,
  "surface_id": "nvim:mba.local:8f3a6f6c",
  "node_id": "nvim-abc123...",
  "gateway": "ws://127.0.0.1:18789",
  "cwd": "/home/user/project",
  "workspace_root": "/home/user/project",
  "tools": {
    "safe": ["buffer.current", "buffer.read", "search", "cursor.get", "selection.get", "diagnostics.get", "describe"],
    "privileged": ["buffer.write", "buffer.replace_lines", "buffer.open", "buffer.reload", "ex.command", "ex.substitute", "cursor.set"]
  }
}
```

Use this to confirm a node is *nvimclaw* (not `vscode.openclaw` or something else), check `workspace_root` before issuing relative paths, and confirm the tool list. Then call `nvim.buffer.current` to discover what the user is actually looking at.

## Conflict handling

Every mutating command (`nvim.buffer.write`, `nvim.buffer.replace_lines`, `nvim.ex.substitute`) accepts **two optimistic-lock preconditions**:

- `expected_changedtick` — Neovim's buffer-tick counter. Increments on every buffer modification.
- `expected_line_hash` — SHA256 of the affected line range joined by `\n`. Stronger than the tick alone; guards against undo/redo and unrelated edits that bump the tick.

The plugin applies the edit **only if both supplied preconditions match the current buffer state.** Otherwise it returns:

```json
{
  "ok": false,
  "error": {
    "code": "conflict",
    "current_changedtick": 18,
    "current_line_hash": "b91d...",
    "sample_lines": [
      {"line": 1, "text": "Schopenhauer is hilarius. He wrote..."},
      {"line": 2, "text": "The user's new sentence here."}
    ]
  }
}
```

**Always handle conflicts by re-reading, not by retrying blindly:**

1. The agent receives a conflict response. The `sample_lines` show the current text in the affected range.
2. Re-call `nvim.buffer.read` (with the same path) to get the full current content if needed.
3. Decide whether the new content changes the intent of the edit. If yes, abort and tell the user. If no, retry with the new `current_changedtick` and `current_line_hash` from the conflict response.
4. Never assume last-write-wins. The whole point of the optimistic lock is to prevent destructive overwrites.

`expected_line_hash` is optional but **strongly recommended for prose edits** where a tick bump might come from an unrelated cursor move during the agent's preflight.

## Discovery

For an agent to find an nvimclaw node attached to a given Neovim instance:

```bash
# 1. List all connected nodes
openclaw nodes status
# 2. Confirm a node is nvimclaw (vs vscode.openclaw or others)
openclaw nodes invoke --node <NODE_ID> --command nvim.describe --params '{}'
# 3. Ask the node what the user is actually looking at.
openclaw nodes invoke --node <NODE_ID> --command nvim.buffer.current --params '{}'
```

If multiple Neovim instances are connected, prefer the node whose current buffer/workspace matches the user's request. Do not assume a path from shell state when `nvim.buffer.current` is available.

When in doubt, **ask the user which one** rather than guessing. Similar workspaces can be reachable from multiple machines; only the `surface_id` tells you which Neovim process the user is sitting in front of.

## Send-from-Neovim (the surface capability)

The inverse direction: Neovim → agent session. The user types into the chat buffer inside Neovim, and the same session (e.g. `agent:main`) receives the message.

- Inside Neovim: `<space>oc` opens the chat buffer (`nvimclaw://chat`) in a vertical split (right side, 40% wide). The current buffer is auto-attached as attachment context (path, line count, language, changedtick).
- `<CR>` sends a normal user turn. `<C-c>` cancels the outbound send **before** the gateway has accepted it; it cannot cancel in-flight agent work.
- The session is the same `agent:main` that webchat, VSCodium, and any other surface also bind to. **Memory, persona, and conversation history carry across surfaces.**
- v0.1 ships request/response chat (one full assistant turn per send). Token streaming lands in v1.1; the internal callback shape is already event-based to make the swap a UI change, not an architecture rewrite.

Multi-surface rule of thumb: if you (the agent) just sent a message from webchat, the Neovim chat buffer will not stream it in unless that Neovim process is subscribed and that subscription is for the same `surface_id`. In practice, **the Neovim chat buffer shows only messages originating from that Neovim process**, plus the responses they trigger. A user-turn sent from webchat appears on the webchat surface only.

## Gotchas

- **`path_denied` (`{code, path, workspace_root}`)** — the buffer path resolves outside `setup({workspace_root})` (default: `vim.fn.getcwd()`). The plugin refuses to read or write anything outside the workspace boundary. Absolute paths are a quick way to trip this; always pass paths relative to the workspace root.
- **`tier_denied` (`{code, message}`)** — you tried a privileged tool while the session is on the `safe` tier. Either ask the user to run `:OpenClawTools privileged` in Neovim, or set `setup({ tools = { tier = "privileged" } })` once in `init.lua`.
- **`unknown_param` (`{code, param}`)** — every tool validates params strictly. Extra or mistyped fields are rejected, not ignored. Copy-paste from the table above; do not improvise field names.
- **`unknown_command` (`{code, command}`)** — `nvim.describe` is your friend; it lists every command the plugin currently exposes, grouped by tier.
- **`expected_changedtick` mismatch** returns a `conflict`, not a `tier_denied`. The two are unrelated — see §Conflict handling.
- **`gateway_timeout` (`{code, retryable: true}`)** — slow or remote gateway. The plugin does not auto-retry mutating tools (it cannot know whether the previous attempt applied); the agent must re-read state and retry.
- **`auth_expired` (`{code, retryable: true}`)** — the deviceToken rotated mid-session. The plugin attempts one reconnect automatically; if it fails, surface this to the user with `:OpenClawReconnect` suggested.
- **`buffer_not_found`** — the path doesn't correspond to an open Neovim buffer. For files on disk, open it first with `nvim.buffer.open` (privileged) or ask the user to open it.
- **`file_missing`** — the path doesn't exist on disk either. Don't guess. Open or read nearby to confirm.
- **`expected_line_hash` is available** on `nvim.buffer.write`, `nvim.buffer.replace_lines`, and `nvim.ex.substitute` for higher-stakes writes. Compute it by reading the buffer with `nvim.buffer.read` (which can also return it on `nvim.diagnostics.get` adjacency queries — the skill plan reserves a future `nvim.buffer.hash` command) and pass it back on commit.
- **No `nvim.session.send` tool** by design. Sending a user message to the active session is a *surface* primitive, not a *node* tool — it's wired to the chat buffer's `<CR>`, not exposed as an `nvim.*` command. A node could in principle craft user-turns on the user's behalf and bypass persona/memory validation; the surface split is what prevents that.
- **Avoid broad Ex workarounds like `:bufdo` for normal edits.** Use `buffer_id` with `nvim.buffer.write`, `nvim.buffer.replace_lines`, or `nvim.ex.substitute` for unnamed buffers. `nvim.ex.command` preserves the window layout by default, but it is still the escape hatch, not the routine edit path.
- **`nvim.ex.command` accepts `confirm: true`** for any destructive Ex call. Use it for `:write`, `:bdelete`, `:q`, `:!rm …`. The user dismisses with `q` or `n` to decline.
- **Poll cost.** Don't poll `nvim.describe` repeatedly. One call per session, cached in memory, is enough.
- **Two Neovim processes on one host** have different `surface_id`s and `node_id`s (`boot_uuid` differs) but the same `cwd`. The right one to invoke is the one whose `surface_id` matches the user-turn's `surface_id`. When the user is not in the middle of a conversation, any connected nvimclaw node is a valid target.

## Compatibility

- **Plugin:** requires `nvimclaw >= 0.1.0`. Plugin and skill are published atomically with matching versions.
- **Protocol:** `nvim.describe.payload.protocol_version` is the wire-protocol version, currently `1`. Bump it only on backward-incompatible tool-surface changes.
- **Discovery of versions:** `nvim.describe` is the single source of truth for "what does this plugin support?" — call it before relying on a tool that may not exist in older releases.
- **Skill frontmatter declares:** `requires: nvimclaw: ">=0.1.0"`. A newer skill with an older plugin installed will hit `unknown_command` or `unknown_param` and surface a clear error.

## Related

- [Plugin repo](https://github.com/utrumsit/nvimclaw) — `utrumsit/nvimclaw`.
- [`vscode.openclaw` extension](https://github.com/xiaoyaner-home/openclaw-vscode/) — the reference implementation that nvimclaw mirrors. Its command surface shape (`vscode.file.*`, `vscode.editor.*`) informed the `nvim.*` split.
