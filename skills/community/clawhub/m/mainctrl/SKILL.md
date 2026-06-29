---
name: mainctrl
description: >
  Runtime safety guard for OpenClaw multi-agent workflows.
  Blocks destructive tools (write, edit, exec, process, apply_patch)
  for controlled agents, forcing delegation to sub-agents.
intents:
  - "stop main agent from writing files directly"
  - "enforce sub-agent delegation in OpenClaw"
  - "block destructive tools for controlled agents"
  - "runtime agent permission management"
  - "multi-agent tool access control"
tags: [multi-agent, access-control, delegation, openclaw, agent-orchestration, security]
icon: 🛡️
metadata:
  author: iClaw
  version: "1.1.1"
---

# mainctrl — Agent Tool Access Control

mainctrl lets you control which agents can use destructive tools (write,
edit, exec, process, apply_patch). Turn it on — main delegates everything
to sub-agents. Turn it off — main is free. Add or remove agents from the
controlled list to extend protection. Install or remove the companion
plugin in one command. No restarts, no config edits.

## Startup Behavior

Every time mainctrl is loaded (the agent reads this SKILL.md), it MUST:

1. Run `./scripts/mainctrl.sh status` to read the current runtime state.
2. Remember the output internally — which tools are blocked, which
   agents are controlled, and the current exec allow-except config.
   This contextual awareness guides every subsequent tool call: know
   when to delegate and which commands can pass through.

## Quick Start

1. Install the plugin and restart:
   ```bash
   ./scripts/mainctrl.sh plugin install
   ```
   Then restart the OpenClaw gateway.
   Safety starts **OFF** — nothing is blocked yet.

   After restart, run `./scripts/mainctrl.sh status` to load the
   current control state into context per [Startup Behavior](#startup-behavior).

2. **Before turning on**, verify at least one sub-agent exists and main can spawn it.
   Check with the `agents_list` tool — you need at least one agent besides `main`:
   ```
   agents_list
   ```
   Also verify main's spawn permissions:
   ```
   gateway config.get agents.list → main.subagents.allowAgents
   ```
   mainctrl blocks main's destructive tools and *requires* at least one
   sub-agent to delegate the work to. If none is configured or main can't
   spawn them, set up a sub-agent first.

3. Turn blocking on:
   ```bash
   ./scripts/mainctrl.sh on
   ```

4. Verify:
   ```bash
   ./scripts/mainctrl.sh status
   ```
   Should show `safety: ON` and all tools `BLOCKED`.

5. Emergency off — temporarily allow all tools.
   When mainctrl is ON, main can't run commands itself. To turn it off:

   - **Delegate to a sub-agent** (e.g. coder):
     Spawn a sub-agent to run `./scripts/mainctrl.sh off`.
   - **Run the script manually** if no sub-agent has exec access:
     ```bash
     ./scripts/mainctrl.sh off
     ```

## Plugin + Skill

mainctrl is two parts that must be installed together:

- **Plugin** (`plugin/index.js`) — a `before_tool_call` hook. It reads
  `state.json` on every tool call and blocks or allows based on your settings.
  Installed via `./scripts/mainctrl.sh plugin install`.
- **Skill** (this directory) — the management side. The CLI script
  (`mainctrl.sh`) writes config to `state.json`; this SKILL.md tells the
  agent how to behave when blocked.

Both talk through a shared file — the skill writes `state.json`, the plugin
reads it. No sockets, no RPC, no restart.

**The skill installs the plugin for you** — run `./scripts/mainctrl.sh plugin install`
to set up both halves in one step.

## How it works

Mainctrl gives the agent two modes, like vi's V and I:

**Visual mode** (`mainctrl on`) — the agent can inspect, search, and read,
but cannot modify anything. Every destructive tool call is blocked:

| Tool         | Why blocked                          |
|--------------|--------------------------------------|
| `write`      | File creation / overwrite            |
| `edit`       | In-place file edits                  |
| `exec`       | Shell command execution              |
| `process`    | Background process management        |
| `apply_patch`| Multi-file patching                  |

### Tools NOT blocked

When mainctrl is ON, these tools remain fully available to the controlled agent:

| Tool             | Purpose                              |
|------------------|--------------------------------------|
| `read`           | File reading / inspection            |
| `web_search`     | Web search                           |
| `web_fetch`      | URL content fetching                 |
| `sessions_spawn` | Sub-agent delegation                 |
| `sessions_send`  | Cross-session messaging              |
| `sessions_list`  | Session discovery                    |
| `sessions_history` | Session history                    |
| `image`          | Image analysis                       |
| `pdf`            | PDF analysis                         |
| `memory_search`  | Memory search                        |
| `memory_get`     | Memory read                          |
| `message`        | Channel messaging                    |
| `gateway`        | Config read / status                 |
| `skill_workshop` | Skill management                     |
| `cron`           | Job scheduling                       |
| `nodes`          | Node device queries                  |
| `tts`            | Text-to-speech                       |
| `agents_list`    | Agent discovery                      |

**🔴 Do NOT default to `exec` for inspection tasks.** When you need to explore
directories, read files, check config, or verify state, use `read` — it's
available, immediate, and never blocked. `exec` is only for tasks that truly
require shell access (build, install, git, etc.), and those should always be
delegated to sub-agents.

This is how today's incident happened: the agent used `exec` for `find` and `ls`
instead of `read` — needless blocking and unnecessary sub-agent overhead.

**Insert mode** (`mainctrl off`) — the agent can write files, run commands,
and make changes freely.

Switch between them with `./scripts/mainctrl.sh on` and `./scripts/mainctrl.sh off`.

A lightweight OpenClaw plugin (`extensions/mainctrl`) hooks
`before_tool_call` and inspects every tool call. When the caller is
one of the `controlledAgents` and `mainctrl` is enabled, the above
tools are rejected with a delegation message.

Agents not in `controlledAgents` are **never** affected —
they always have full tool access.

## Agent behavior rule

When the main agent receives the block message:

> Delegate this work to a sub-agent instead.
> Use sessions_spawn to dispatch to coder, tester, auditor, or publicist.

it MUST:
1. Briefly inform the user that the operation has been blocked and is being delegated.
2. Immediately spawn a sub-agent (coder, tester, auditor, or publicist) to complete the blocked operation.

Do NOT wait for the user to confirm — report and delegate in the same turn.

### Blocked tool response

When a controlled agent calls a blocked tool, it receives:

> Delegate this work to a sub-agent instead.
> Use sessions_spawn to dispatch to coder, tester, auditor, or publicist.

The agent follows the [Agent behavior rule](#agent-behavior-rule) and
spawns a sub-agent to complete the work automatically.

## Security Design Notes

### 1. Internal guard, not anti-hacker

This is an **internal self-discipline mechanism**, not a defense against external attacks.
mainctrl makes the LLM agent *think twice* before proceeding with destructive
operations. It is not a sandbox or security boundary; the goal is to prevent
accidental misuse by the agent itself (e.g., main writing code when it should
delegate to coder), not to stop a malicious attacker. Treat it as a guardrail
that makes the LLM say "should I really do this myself?" — not a fortress.

### 2. Explicit delegation

When spawning a sub-agent to replace a blocked operation, always state **who**
is being delegated and **why**. For example:

> `exec` blocked. Delegating to **coder** to run the command.

This transparency helps the user understand the delegation chain at a glance.

### 3. Direct for skill execution

All CLI commands in this skill are designed for **programmatic execution** (by
agents or other skills). There are no interactive prompts, confirmations, or
friction — they complete in one shot. This is intentional: when an agent needs to
toggle safety or reconfigure, it must not hang waiting for user input.

## Why this approach

`mainctrl` uses an OpenClaw `before_tool_call` plugin hook rather than
agent-level `tools.deny` for two reasons.  First, `tools.deny` is
static — toggling it requires editing agent config and restarting the
gateway.  The plugin hook reads `state.json` on every call, so safety
can be toggled at runtime with a single command and takes effect
immediately.  Second, agent configs cannot distinguish which *caller*
is invoking a tool; the plugin hook can selectively block agents
listed in `controlledAgents` while leaving sub-agents (like `coder`)
unaffected.

## Exec allow-except — safe exec commands

`execAllowExcept` only takes effect when `exec` is in `blockedTools`. If `exec` is not blocked, all commands pass through regardless of this config.

When `exec` is in the blocked tools list, mainctrl inspects the command
before blocking. Commands listed as keys in `execAllowExcept` are
**allowed through** — unless the command line contains an allow-except pattern.

### How it works

1. Command's first word is looked up in `execAllowExcept`
2. If the command is **not a key** → blocked as usual (delegate)
3. If the command **is a key** → each allow-except pattern is checked against the full command string
4. If any allow-except pattern matches → blocked with a specific reason
5. If no allow-except pattern matches → **allowed**

### Allow-except patterns

| Command | Allow-except patterns | What they catch |
|---------|----------------------|-----------------|
| `find`  | `-exec`, `-ok` | Execute commands on matched files |
|         | `-delete`     | Delete matched files |
|         | `-fprint`     | Write to arbitrary files |
|         | `\|`, `$(` , `>` , `>>` | Pipes, command substitution, redirection |
| `ls`    | `>` , `>>` , `|` | Output redirection, pipes |
| `pwd`   | `>` , `>>` , `|` | Output redirection, pipes |
| `sed`   | `>` , `>>` , `|` | Output redirection, pipes |
|         | `.java` , `.py` , `.js` , `.html` , `.css` | Direct source file modification |
| `cat`   | `>` , `>>` , `|` | Output redirection, pipes |

Substring matching is used (e.g. `-exec` also catches `-execdir`).

### Configuration

`execAllowExcept` lives in `state.json`. To modify it, edit the file
directly (no CLI subcommand for this):

```bash
# Set via CLI
./scripts/mainctrl.sh allow-except '{"find":["-exec","-ok","-delete","-fprint","|","$(",">",">>"],"ls":[">",">>","|"],"pwd":[">",">>","|"],"sed":[">",">>","|",".java",".py",".js",".html",".css"],"cat":[">",">>","|"]}'
```

Run `./scripts/mainctrl.sh status` to see the current allow-except configuration.

### Examples

```
ls ~/                    # ✅ allowed (no allow-except hit)
find . -type f            # ✅ allowed
find . -exec rm {} \;     # 🛡 blocked: "-exec"
ls > /tmp/foo             # 🛡 blocked: ">"
sed -i 's/foo/bar/g' file.java  # 🛡 blocked: ".java"
cat /etc/hosts            # ✅ allowed (no allow-except hit)
rm -rf /                  # 🛡 blocked: not in allow-except map
```

## Commands

Use the `mainctrl.sh` script in the `scripts/` directory:

| Command                          | Effect                              |
|----------------------------------|-------------------------------------|
| `./scripts/mainctrl.sh status`                | Show current state (enabled + agents + per-tool + exec allow-except) |
| `./scripts/mainctrl.sh on`                    | Enable blocking                     |
| `./scripts/mainctrl.sh off`                   | Disable blocking (all tools pass through) |
| `./scripts/mainctrl.sh agents '<json-array>'` | Set which agents are controlled     |
| `./scripts/mainctrl.sh tools '<json-array>'` | Set or show blocked tools list      |
| `./scripts/mainctrl.sh allow-except '<json>'` | Set execAllowExcept config (JSON object) |
| `./scripts/mainctrl.sh refresh-memory`    | Write current status to ~/.openclaw/workspace/MEMORY.md |
| `./scripts/mainctrl.sh plugin install` | Install the companion plugin via openclaw plugins |
| `./scripts/mainctrl.sh plugin remove`  | Disable and uninstall the companion plugin       |

### Plugin Installation

Instead of manually adding the plugin path to `plugins.load.paths`,
use the built-in script:

```bash
# Install the plugin
./scripts/mainctrl.sh plugin install

# Remove the plugin
./scripts/mainctrl.sh plugin remove
```

This calls `openclaw plugins install` / `uninstall`, which manages the
plugin under OpenClaw's native plugin registry.  After install or remove,
restart the gateway for the change to take effect.

### controlledAgents config

`controlledAgents` lists which agents are subject to tool blocking.
Example configs:

```json
{ "enabled": true, "controlledAgents": ["main"] }
```

```json
{ "enabled": true, "controlledAgents": ["main", "auditor"] }
```

## State file

`skills/mainctrl/scripts/state.json` (in the `scripts/` directory):

```json
{
  "enabled": false,
  "controlledAgents": ["main"],
  "blockedTools": ["write", "edit", "exec", "process", "apply_patch"],
  "execAllowExcept": {
    "find": ["-exec", "-ok", "-delete", "-fprint", "|", "$(", ">", ">>"],
    "ls":   [">", ">>", "|"],
    "pwd":  [">", ">>", "|"],
    "sed":  [">", ">>", "|", ".java", ".py", ".js", ".html", ".css"],
    "cat":  [">", ">>", "|"]
  }
}
```

Changes take effect immediately on the next tool call — no restart needed.

## Plugin

The companion extension lives at `extensions/mainctrl/`.
It reads `state.json` on every `before_tool_call` event,
so the latency is a single `fs.readFileSync` per tool call.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Blocking not working | `./scripts/mainctrl.sh status` — ensure safety is ON |
| Plugin not loaded | `openclaw plugins list` — ensure mainctrl is enabled |
| Agent still blocked after `off` | Restart the gateway |
| Sub-agent blocked too | Run `./scripts/mainctrl.sh agents main` to restrict to main only |
| Safe exec command blocked | Check `./scripts/mainctrl.sh status` — command must be in exec allow-except map and not matching allow-except patterns |

## Examples

What you can do with mainctrl:

### Control the safety switch

```bash
./scripts/mainctrl.sh on      # Block destructive tools — delegate mode
./scripts/mainctrl.sh off     # Allow all tools — free mode
./scripts/mainctrl.sh status  # Check current state
```

### Add or remove controlled agents

```bash
./scripts/mainctrl.sh agents '["main"]'             # Control main only
./scripts/mainctrl.sh agents '["main","auditor"]'   # Add auditor to the list
./scripts/mainctrl.sh agents '[]'                   # Clear all (falls back to default)
```

### Add or remove blocked tools

```bash
./scripts/mainctrl.sh tools                                          # Show which tools are blocked
./scripts/mainctrl.sh tools '["write","exec"]'                       # Block only write and exec
./scripts/mainctrl.sh tools '["write","edit","exec"]'                # Block three
./scripts/mainctrl.sh tools '["write","edit","exec","process","apply_patch"]'  # Block all five (default)
./scripts/mainctrl.sh tools '[]'                                     # No tools blocked
```

### Manage the plugin

```bash
./scripts/mainctrl.sh plugin install   # Install the companion plugin
./scripts/mainctrl.sh plugin remove    # Uninstall the plugin
```

### Set exec allow-except

```bash
./scripts/mainctrl.sh allow-except '{"find":["-exec","-ok","-delete","-fprint","|","$(",">",">>"],"ls":[">",">>","|"],"pwd":[">",">>","|"],"sed":[">",">>","|",".java",".py",".js",".html",".css"],"cat":[">",">>","|"]}'
./scripts/mainctrl.sh allow-except '{}'              # No exec exceptions, all exec blocked
```

## Verification

- [ ] Plugin installed: `./scripts/mainctrl.sh plugin install`
- [ ] Blocking active: `./scripts/mainctrl.sh status` shows safety ON
- [ ] Tool blocked: main agent exec/write/edit/process/apply_patch return block message
- [ ] Sub-agent unaffected: coder can still use write/exec
- [ ] Toggle works: `./scripts/mainctrl.sh off` then `./scripts/mainctrl.sh on` restores blocking
- [ ] Exec allow-except works: `ls ~/` passes, `ls > /tmp/foo` blocked
