<div align="right"><sub><a href="README.md">中文</a> · <b>English</b></sub></div>

<h1 align="center">env-doctor</h1>

<p align="center">
  <b>Other cleaners ask "which folder is big?" — this one asks "are you still using that tool?"</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-a855f7?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/platform-macOS_·_Linux-6d28d9?style=flat-square&logo=apple&logoColor=white" alt="platform">
  <img src="https://img.shields.io/badge/shell-bash_3.2%2B-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="bash">
  <img src="https://img.shields.io/badge/dependencies-none-3f8a82?style=flat-square" alt="zero dependencies">
  <img src="https://img.shields.io/badge/scan-read--only-179?style=flat-square" alt="read only">
  <img src="https://img.shields.io/badge/license-MIT-b88a3e?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/github/stars/huiyonghkw/hekouwang-env-doctor-skill?style=flat-square&color=ff8a3d" alt="stars">
</p>

<p align="center">
  <img src="demo/env-doctor.gif?v=2" alt="Running the health check inside Claude Code: disk usage sorted into leftovers, cache, and data" width="100%">
</p>

> ℹ️ The demo recordings are in Chinese, but the skill works in whatever language you talk to Claude in.

---

## The short version

When your Mac runs out of space you go delete photos and videos. Meanwhile the real hogs are the things your dev tools quietly pile up where you never look. And the single worst offender is the one nobody scans for: **the tool you switched away from and never uninstalled.**

Measured on the author's machine: `~/.nvm` was sitting on **9.8 GB** — while `node` had been coming from fnm for over a year and that directory hadn't been touched since. **Acting on the report freed roughly 10 GB.**

## Why it finds what size-based scanners can't

Size is something you measure. **Identity is something you have to infer.** To decide whether nvm is a leftover, you have to cross-check four signals at once:

| Signal | What it checks | Weight |
|---|---|---|
| `shell_loaded` | Whether your shell config actually sources it (comments don't count) | High |
| `cmd_in_path` | Whether the command is still on your PATH | High |
| `runtime owner` | Which tool **actually provides** `node` / `python` right now | Highest |
| `last_modified` | How long since anything touched the directory | Supporting |

Real output:

```
nvm    9.8 GB   not loaded  not on PATH  node comes from fnm    last touched 2025-03  → leftover ✅ safe to remove
fnm    1.7 GB   loaded      on PATH      node comes from it     last touched 2026-05  → active   ⛔ leave alone
pyenv  121 MB   not loaded  not on PATH  python comes from brew last touched 2024-07  → leftover ✅ safe to remove
```

It also catches something nobody flags: **the same version stored twice by two different managers** — on the author's machine `v16.20.2` existed under both nvm and fnm.

### How it differs from typical cleaners

| | Typical Mac cleaner | env-doctor |
|---|---|---|
| Decides by | Directory size | **Tool identity** (still in use or not) |
| Detects "switched but never uninstalled" | ✗ | ✅ Core feature |
| The biggest directory | First thing it suggests deleting | **Often the one you must not touch** (model weights) |
| Deletion | Bulk delete after one confirm | Item-by-item opt-in; data entries can't be selected at all |
| Aftermath | Not its problem | Reminds you to clean the init lines in your shell config |

## Install

```bash
git clone https://github.com/huiyonghkw/hekouwang-env-doctor-skill.git \
  ~/.claude/skills/hekouwang-env-doctor-skill
```

Start a new Claude Code session and it loads automatically. No configuration. **Zero dependencies** — it only uses `du`, `df`, and `grep`, and it runs on the bash 3.2 that ships with macOS.

## Usage

Just say it in Claude Code:

```
My disk is full, help me find what's eating the space
```

Or run the scripts directly:

```bash
bash scripts/scan.sh              # Health check (read-only, full)
bash scripts/scan.sh --quick      # Health check (read-only, fast)
bash scripts/clean.sh --dry-run   # Cleanup selector, shows without executing ← start here
bash scripts/clean.sh             # Cleanup selector, executes what you tick
```

Results come back in three groups — 🟠 **leftovers** / 🟡 **cache** / 🔴 **data** — presented **one group at a time**, each entry carrying: what it is, how big, why it was classified that way, the official command, and what it costs you.

### The cleanup selector

<p align="center">
  <img src="demo/selector.gif?v=2" alt="Cleanup selector: tick per item, data entries locked, confirmation before anything runs" width="100%">
</p>

`Space` toggle · `↑↓` move · `a` select all · `n` select none · `Enter` confirm · `q` quit

## Safety by design

This tool can delete things, so the boundaries are written down in [`references/safety.md`](references/safety.md) and enforced in code:

1. **Nothing is pre-selected** — there is no path where mashing Enter wipes everything
2. **Data entries are 🔒 locked** — model weights, container volumes, Ollama models; Space won't tick them
3. **Only whitelisted, hard-coded commands run** — paths and commands live in a fixed array, never assembled from input
4. **The confirmation screen lists every command and its cost; you must type `yes`**
5. **`--dry-run` is always available**
6. **It never edits your `.zshrc`** — after removing a version manager it only *reminds* you to clean the init lines, because silently rewriting shell config is more dangerous than deleting a directory

Also: `scan.sh` is **read-only end to end** — deletion happens only in `clean.sh`. Nothing is sent anywhere; **no network calls, no telemetry**.

## Coverage

**Version managers**　nvm · fnm · volta · pyenv · rbenv · rvm · asdf · mise · sdkman · jenv · conda
**Package caches**　npm · yarn · pnpm · bun · pip · uv · cargo · go · maven · gradle
**Containers & simulators**　Docker · CoreSimulator · Xcode DerivedData / iOS DeviceSupport
**AI model caches**　huggingface · ollama · torch

**Out of scope**: system caches, photos, mail, chat apps — leave those to macOS Storage settings.

## FAQ

**Are the cleanup commands trustworthy?**　Every one was verified against official docs or the tool's own `--help`, with sources recorded in [`references/rules.md`](references/rules.md). The nvm removal steps, for instance, come straight from the Manual Uninstall section of its official README.

**Why isn't the biggest directory the first to go?**　On the author's machine the biggest is `~/.cache/huggingface` — 7.3 GB of model weights that would take hours to re-download. **Sorting by size means your very first cut is the wrong one.**

**What if it classifies something wrong?**　When signals conflict, it files the entry under "uncertain" and explains the conflict instead of forcing a verdict. Nothing gets removed unless you tick it.

**Will the rules go stale?**　Yes. The ecosystem keeps moving (nvm→fnm→mise, pip→uv), so the rule library is versioned. Issues adding new tools are very welcome.

## Layout

```
SKILL.md                 # Router + iron rules
scripts/
  scan.sh                # Read-only scanner
  clean.sh               # Cleanup selector (the only place deletion happens, whitelist-driven)
references/
  rules.md               # Leftover-signature rule library (tool → dir → liveness test → official command → cost)
  report.md              # Report format and conversation flow
  safety.md              # Iron rules and pre-ship checklist
demo/                    # Two real-machine recordings
```

## Contributing

Rules for new tools are the most welcome contribution. In your PR, fill all five columns — **directory / identity / liveness signature / official command / cost** — and cite where the command came from (doc link or `--help` output).

## License

MIT · © 2026 [@huiyonghkw](https://github.com/huiyonghkw)

<sub>The doctor family: [claude-md-doctor](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill) (checks your config) · [skill-doctor](https://github.com/huiyonghkw/hekouwang-claude-skill-doctor-skill) (checks your skills) · **env-doctor** (checks your machine)</sub>
