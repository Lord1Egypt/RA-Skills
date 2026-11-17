---
name: mode-switch-machine-stack
description: "Use when you toggle VPN, agents and services by hand. One command flips the whole machine stack together — VPN, background agents, local services, model tier — from one YAML mode matrix; the watchdog repairs the current mode and never revives what you switched off (the part most setups get wrong).\n\nUse when:\n(1) You re-toggle the same five things by hand at every work↔game switch\n(2) A crash-restart must come back as the mode you are in now, not as whatever was running before it\n(3) Background agents should all run while you work, one or two while you game, none while you render\n(4) Local services should free their RAM when you need it, not when you remember\n(5) VPN on for work, off for low-latency gaming — and the agents must stop with it, or they ride the tunnel\n\nPython stdlib only — no pip install, no model calls, no API cost; Windows tested. Prove it first: `python templates/modes_switch.py --selftest` builds a fake stack in a temp dir and switches it end to end — your machine untouched.\n\n中文触发:手动切工作/游戏模式太麻烦 / 一条命令切换整机栈 / 分身与本地服务跟着模式起停 / VPN 跟着模式开关 / 看门狗按模式自愈"
version: 0.1.1
author: TXJ · 天玄镜 (Tianxuanjing)
license: MIT-0
platforms: [windows]
metadata:
  hermes:
    tags: [modes, power-management, watchdog, local-services, vpn, automation, multi-agent]
    related_skills: []
---

# Mode Switch Kit — one command for the whole machine stack

**Use when**: you switch between "work" and "game" (or any two setups) by hand-toggling the same things every time — VPN, background agents, local services, model tier — and you want one command plus watchdogs that keep it that way.

**Key commands**: `python templates/modes_switch.py work` (flip everything) · `python templates/modes_switch.py --selftest` (prove it on a fake stack, zero real effect) · `python templates/watchdog.py` (repair the current mode) · `python templates/modes_switch.py --list` (show the matrix).

**Cost**: pure local scripts. No model calls, no API cost, no dependencies (Python standard library only).

A "mode" here is a row in a YAML table: VPN on/off · which background agents run · which local services run · which model tier is selected. The switcher applies one row and writes the result to a state file; the watchdog reads that file and repairs *only* what the current mode wants.

## What it gives you

- 🔀 **One command, whole stack**: tunnel, agents, services and model tier move together — no half-switched states where the tunnel is off but the agents are still trying to reach the network
- 🗺 **Config, not code**: the mode matrix is a YAML file. No machine name, path or port lives in the scripts, so a second machine (or a teammate) only edits config
- 🐕 **Watchdogs that follow the mode**: repair what should be running, never revive what you just switched off — this is the part most setups get wrong
- 🔒 **Precise process handling**: stop by pidfile or listening port, with a start-time check so a recycled PID cannot fake a healthy service; never name-based matching
- ⚡ **Cheap and quiet**: stdlib only, no daemon; a round where nothing changed does nothing remote and repairs nothing — it prints one overview line and refreshes its own counter file, nothing else
- 🧪 **Provable before you trust it**: `--selftest` builds a fake stack (fake VPN CLI, fake agent, fake service on a real port) in a temp directory and runs the whole switch end to end

## Files

| File | What it is |
|---|---|
| `templates/modes.yaml` | the mode matrix — edit this, it is the only host-specific file |
| `templates/modes_switch.py` | the switcher: applies a matrix row, writes the state file, `--dry-run` / `--selftest` built in |
| `templates/watchdog.py` | mode-adaptive watchdog: starts what the current mode wants, rate-limited, alerts on failure |
| `references/patterns.md` | why it is built this way + the real failures behind each rule (PID reuse, dual writers, VPN cut-offs) |
| `SKILL.md` | this file |

The published package contains no `*.bak_*` backups and no `__pycache__`/`*.pyc` artifacts (`__pycache__/`, `*.pyc`, `*.bak_*` are in `.gitignore`) — delete any you find after cloning or unpacking.

## Setup (≈2 minutes)

```bash
# 1. get the kit (already done if you installed from the marketplace)
cp -r mode-switch-kit ~/my-stack && cd ~/my-stack

# 2. prove it works before touching anything real
python templates/modes_switch.py --selftest

# 3. dry-run the shipped example: prints every action, changes nothing
python templates/modes_switch.py work --config templates/modes.yaml --dry-run
```

Python 3.8+ is the only requirement. No `pip install`, ever.

## Configure your machine

Edit `templates/modes.yaml` (relative paths resolve against that file's directory):

1. **VPN** — set `vpn.cmd` to your VPN CLI; `connected_marker` is the substring its `status` prints when up. Leave `cmd: ""` and the kit ignores the VPN entirely.
2. **Agents** — set `profiles_dir` to the directory holding one subdirectory per background agent, and `gateway.start_argv` to the command that launches one (it runs with `cwd=<that agent's directory>`). The pidfile each agent writes is what the kit tracks.
3. **Services** — list `name` + `port` per local service. Add `start_argv` and the kit can start it too; omit it and the kit only monitors and stops it.
4. **Modes** — one block per mode, listing which agents and services belong to it, `vpn: on|off|keep`, and (optional) the model tier. `model_job.cmd` is where the tier is applied — e.g. pointing your scheduler at a job with `--model {model} --provider {provider}`.
5. Optional `alert.cmd` (with `{text}`) tells the watchdog where to report; `watchdog_state_file` (optional) is where the watchdog keeps its own counter file — leave it out and the counter sits next to `state_file`.

## Run

```bash
python templates/modes_switch.py work                    # flip to the "work" row
python templates/modes_switch.py game --dry-run          # print the plan, change nothing
python templates/modes_switch.py --list                  # show all modes
python templates/modes_switch.py --state                 # current mode, from the state file
```

Run the watchdog on a schedule (cron / Task Scheduler / systemd timer), every few minutes:

```bash
python templates/watchdog.py            # repair the current mode if something is missing
python templates/watchdog.py --status   # what this mode expects, as JSON
```

A quiet round is free except for one line: no network calls, no repairs, no
alert — it prints one overview line (`mode=… expected agents=… services=…`) and
refreshes its own counter file, which is the only proof the watchdog is still
alive. Watch it in a log and a dead watchdog looks exactly like a quiet one.

## Platform support

| Platform | Status |
|---|---|
| **Windows** | Tested: `netstat -ano` for port→PID, `tasklist` for liveness, `taskkill` for stop, PowerShell CIM for process start time. |
| **Linux / macOS** | Not verified. The three POSIX swaps are marked `# POSIX swap 1/2/3` in `modes_switch.py`: port→PID lookup (`lsof`/`fuser`), liveness (`os.kill(pid, 0)`), stop (`SIGTERM`). Replace those three and the rest — matrix, state file, idempotence, watchdogs — is platform-neutral. |

Say so honestly in your own packaging: this kit claims Windows because that is what was run, and it tells you exactly what to change for the rest.

## Pitfalls

1. **Don't hardcode the mode in your watchdog.** It must read the state file; a watchdog with its own copy of the truth will fight your switch (see `references/patterns.md` §1).
2. **A pidfile is a hint.** With no start time recorded, a recycled PID looks exactly like a running agent. Record `start_time` when you write pidfiles; also beware units (seconds vs centiseconds vs ms) — the kit compares all three.
3. **Never match process names to stop something.** Kill by pidfile or by exact listening port. `:3001` must not match `:30010`.
4. **The VPN is the dangerous step.** If your chat/remote channel rides the tunnel, a bad switch can cut your own access — the state file is written first so the watchdogs aim at the new mode even if the switch dies halfway. `vpn: keep` must be a real no-op.
5. **`connect` returns before the tunnel is up.** Wait (`vpn.settle_s`) before probing, or you will "repair" a tunnel that is already coming up.
6. **A failed status query is not "disconnected".** Treat up/down/unknown as three states; reconnecting against a dead VPN client is an alert loop.
7. **Write state before mutating.** Reverse order leaves a window where a half-switched machine is guarded by the old mode's rules.
8. **One writer per state file.** The switcher owns the mode state; each watchdog keeps its own counters. Two writers on one JSON file lose updates — including the outage marker you needed.

## Verification

```bash
python templates/modes_switch.py --selftest   # "selftest OK", exit 0
python templates/watchdog.py --selftest       # "selftest OK", exit 0
```

The switcher's selftest is a real end-to-end run on a fake stack in a temp directory: it starts a fake agent (which writes its own pidfile), starts a fake service that really binds a port, toggles a fake VPN CLI, then switches to a second mode and asserts the agent was stopped by pidfile, the service was killed by exact port match, and the VPN was disconnected. Your real machine is untouched; the temp tree is removed on exit. Found a bug by editing config? Re-run it — that is what it is for.

## Where this sits

This mode matrix is one block of a larger private-assistant setup (memory and context recovery, todos, multi-agent gateways, watchdogs). The memory half is published separately as `evermind-ai-agent-memory`, and the two are designed to be installed side by side — nothing here requires it. It works with any agent that can run a local command (Claude Code, Codex, Cursor, Hermes…).

## License

MIT-0 — free to use, modify, and sell.
