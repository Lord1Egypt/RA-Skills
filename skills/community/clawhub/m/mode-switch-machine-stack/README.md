# Mode Switch Kit

**One command flips your whole machine stack — VPN, background agents, local services, model tier — driven by a single YAML mode matrix. The watchdogs repair the current mode, and never revive what you switched off.**

![version](https://img.shields.io/badge/version-0.1.1-blue)
![license](https://img.shields.io/badge/license-MIT--0-green)
![platform](https://img.shields.io/badge/platform-Windows%20(tested)-lightgrey)
![deps](https://img.shields.io/badge/deps-stdlib%20only-orange)

## The problem

Every work↔game switch is the same five manual toggles: VPN on/off, which background agents run, which local services hold RAM, which model tier is selected, and what the watchdog should keep alive. Do it by hand and you forget one. Worse: let the machine crash-restart and your watchdog happily brings back **everything that was running before** — including the pieces you deliberately switched off.

## What this does

A **mode** is a row in a YAML table: VPN on/off · which background agents run · which local services run · which model tier is selected.

- `modes_switch.py <mode>` applies one row and writes the result to a state file.
- `watchdog.py` reads that state file and repairs **only** what the current mode wants. Anything the current mode does not list stays down, no matter what it was doing before the crash.

The state file is the single source of truth. That is the whole design.

## Quick start

```bash
git clone https://github.com/ccy123abcd/mode-switch-machine-stack.git
cd mode-switch-machine-stack

python templates/modes_switch.py --list        # show the mode matrix
python templates/modes_switch.py --selftest    # prove it on a fake stack — your machine untouched
python templates/modes_switch.py work          # flip the real machine
python templates/watchdog.py --selftest        # watchdog selftest
```

**Start with `--selftest`.** It builds a fake stack in a temp directory — a fake agent that writes its own pidfile, a fake service that really binds a port, a fake VPN CLI — switches it end to end, and asserts the agent was stopped by pidfile, the service by exact port match, and the VPN disconnected. Zero effect on your real machine; the temp tree is removed on exit.

Then edit `templates/modes.yaml` to describe *your* stack.

## The part most setups get wrong

1. **A crash-restart must come back as the mode you are in now** — not as whatever happened to be running when it died. Watchdogs that only "start the missing things" get this wrong.
2. **A failed status query is not "disconnected".** Treat up / down / unknown as three states. Reconnecting against a dead VPN client is an alert loop.
3. **Write state before mutating.** The reverse order leaves a window where a half-switched machine is guarded by the old mode's rules.
4. **One writer per state file.** The switcher owns the mode state; each watchdog keeps its own counters. Two writers on one JSON file lose updates — including the outage marker you needed.

## Cost

Pure Python standard library. No `pip install`, no model calls, no API cost. Scripts exit with meaningful codes (`0` ok / `2` blocked / `3` refused).

## Files

| Path | What |
|---|---|
| `SKILL.md` | The skill definition (works with Claude Code, Codex, Cursor, Hermes, OpenClaw) |
| `templates/modes_switch.py` | The switcher (`work` / `--list` / `--state` / `--selftest`) |
| `templates/watchdog.py` | Mode-adaptive watchdog (`--selftest`) |
| `templates/modes.yaml` | Your mode matrix — edit this |
| `references/patterns.md` | Design notes, pitfalls, and the three places to change for Linux/macOS |

Windows is what we run and test. The code is plain `subprocess` + `psutil`-free process handling; `references/patterns.md` names the three platform-specific spots.

## Where this sits

This mode matrix is one block of a larger private-assistant setup (memory and context recovery, todos, multi-agent gateways, watchdogs). The memory half is published separately as **[evermind-ai-agent-memory](https://github.com/ccy123abcd/evermind-ai-agent-memory)** — cross-session memory recovery for AI agents — and the two are designed to be installed side by side. Neither requires the other.

More of this setup will be published as separate single-purpose skills, and eventually as one package. Installing one is the cheap way to see whether the rest is for you.

## Also by TXJ · 天玄镜 (Tianxuanjing)

- **[evermind-ai-agent-memory](https://github.com/ccy123abcd/evermind-ai-agent-memory)** — cross-session memory recovery: restore agent state in ~70% fewer tokens, and switch contexts at any task boundary without losing your memory.
- **Mode Switch Kit** (this repo) — one command for the whole machine stack.

## License

MIT-0 — free to use, modify, and sell. No attribution required.
