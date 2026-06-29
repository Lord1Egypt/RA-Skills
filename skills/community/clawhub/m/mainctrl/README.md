# mainctrl

Stop `main` from shooting itself in the foot.

I kept telling main "don't write code yourself" — and it kept ignoring me.
`tools.deny` seemed like the answer, but it had two fatal flaws: deny rules
cascade to sub-agents, so coder gets blocked too. And changing the config
meant a restart, which is the last thing you want when main's mid-flow.
So I built mainctrl: a way to pull main back to its senses anytime it tries
to do someone else's job.

mainctrl blocks destructive tool calls for agents you choose. By default it
watches `main` — the agent that orchestrates, not executes. When `main` tries
to write a file or run a shell command, mainctrl says no and tells it to
delegate to a sub-agent instead.

## Plugin + Skill

mainctrl is two independent parts that work together:

- **Plugin** — a `before_tool_call` hook that intercepts tool calls. Reads
  `state.json` on every invocation.
- **Skill** (this repo) — the management side. Provides the CLI script
  (`mainctrl.sh`) and agent instructions (`SKILL.md`).

Both talk through `scripts/state.json`: the CLI writes it, the plugin reads
it. No sockets, no RPC, no restarts. One synchronous filesystem read per call.

**Both must be installed:**

```bash
openclaw plugins install clawhub:mainctrl
openclaw skills install clawhub:mainctrl
```

## Install from source

```bash
./scripts/mainctrl.sh plugin install
openclaw gateway restart
./scripts/mainctrl.sh status    # verify: should show "safety: OFF"
./scripts/mainctrl.sh on        # turn it on
```

## vi Mode Analogy

mainctrl gives the agent two modes, like vi's V and I:

- **Visual mode** (`mainctrl on`) — inspect, search, read. No modifications.
- **Insert mode** (`mainctrl off`) — write files, run commands, full access.

Switch instantly — no restarts.

## Use

```bash
./scripts/mainctrl.sh on          # start blocking
./scripts/mainctrl.sh off         # emergency off — everything passes through
./scripts/mainctrl.sh status      # see what's happening

./scripts/mainctrl.sh agents '["main","auditor"]'   # JSON array
./scripts/mainctrl.sh agents '[]'                    # clear all (falls back to default)

./scripts/mainctrl.sh tools                    # see what's blocked
./scripts/mainctrl.sh tools '["write","exec"]' # set blocked tools (JSON array)
./scripts/mainctrl.sh tools '[]'                     # no tools blocked

./scripts/mainctrl.sh allow-except '{"find":["-exec","-ok","-delete","-fprint","|","$(",">",">>"],"ls":[">",">>","|"],"pwd":[">",">>","|"],"sed":[">",">>","|",".java",".py",".js",".html",".css"],"cat":[">",">>","|"]}'
./scripts/mainctrl.sh allow-except '{}'              # no exec exceptions, all exec blocked

./scripts/mainctrl.sh refresh-memory    # snapshot status into MEMORY.md
```

`status` output:

```
mainctrl status:
  safety:            ON  (blocking is active)
  controlled agents: main

  Tool          Status
  ------------  --------
  write           BLOCKED
  edit            BLOCKED
  exec            BLOCKED
  process         BLOCKED
  apply_patch     BLOCKED
  exec allow-except:
    ls: [">", ">>", "|"]
    pwd: [">", ">>", "|"]
    find: ["-exec", "-ok", "-delete", "-fprint", "|", "$(", ">", ">>"]
    sed: [">", ">>", "|", ".java", ".py", ".js", ".html", ".css"]
    cat: [">", ">>", "|"]
```

## How it works

Every tool call hits the hook. Four checks, one file read:

1. `enabled` true? No → let it through.
2. Caller is a controlled agent? No → let it through.
3. Tool is on the blocked list? Yes → block. No → let it through.
4. For `exec`: command in `execAllowExcept` keys → check allow-except patterns.
   If any allow-except pattern matches the command line → block. Otherwise → allow.

Five tools blocked by default: `write`, `edit`, `exec`, `process`,
`apply_patch`. Read-only tools always pass through.

State lives in `scripts/state.json`:

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

Changes take effect on the next tool call. If the file is missing or
corrupted, the plugin falls back to permissive mode (everything allowed).

## Exec allow-except

`execAllowExcept` only takes effect when `exec` is in `blockedTools`. If `exec` is not blocked, all commands pass through regardless of this config.

When `exec` is blocked, safe read-only commands (`ls`, `find`, `pwd`) are
allowed through — unless the command contains an allow-except pattern like
`>`, `>>`, `|`, or (for `find`) `-exec`, `-delete`, etc.

Configure via `execAllowExcept` in `state.json`. See `./scripts/mainctrl.sh status`
for current allow-except settings.

## Why not `tools.deny`?

`tools.deny` cascades to sub-agents — block `write` on `main` and `coder`
loses it too. mainctrl checks who's calling and only intercepts named agents.
Sub-agents keep full access. Plus, `tools.deny` needs a gateway restart to
change; mainctrl takes effect on the very next call.

## Files

```
skills/mainctrl/
├── README.md                # this file
├── SKILL.md                 # agent-facing instructions
├── scripts/
│   ├── mainctrl.sh          # CLI: on, off, status, agents, tools, allow-except, plugin
│   └── state.json           # runtime config — CLI writes, plugin reads
└── plugin/
    ├── index.js             # before_tool_call hook
    ├── package.json
    └── openclaw.plugin.json
```
