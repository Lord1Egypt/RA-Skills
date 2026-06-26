# OOT

OOT is a practical OpenClaw skill for cutting token waste across day-to-day agent work.

It keeps sessions cheaper by reducing unnecessary context, routing simple tasks away from expensive models, tightening heartbeat behavior, and tracking budget locally. When paired with RTK, it also helps reduce the shell-output side of token waste.

[![ClawHub](https://img.shields.io/badge/ClawHub-oot-blue)](https://clawhub.ai/Cloud-Dark/oot)
[![Version](https://img.shields.io/badge/version-1.4.2-green)](https://github.com/Cloud-Dark/oot/blob/main/CHANGELOG.md)
[![License: MIT--0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/license/mit-0/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple)](https://openclaw.ai)

---

## Core Idea

Most token waste in agent workflows comes from two places:

- too much context loaded too early
- too much noisy tool output sent back to the model

OOT focuses on the first problem directly:

- recommend smaller context bundles
- route tasks to cheaper model tiers when possible
- reduce heartbeat churn
- track usage against a daily budget

If you also use RTK, you cover the second problem too by shrinking command output from tools like `git`, `rg`, `cargo test`, `pytest`, and log commands.

---

## What You Get

### Smaller Context

`context_optimizer.py` helps avoid loading large piles of files when the task does not need them.

### Smarter Model Use

`model_router.py` classifies work and suggests a cheaper or more appropriate model tier.

### Lower Heartbeat Cost

`heartbeat_optimizer.py` reduces unnecessary checks and supports cache-TTL-aware intervals.

### Budget Awareness

`token_tracker.py` tracks usage locally and helps prevent runaway session cost.

### Better Results with RTK

For shell-heavy workflows, RTK can compress verbose command output before it reaches the model. OOT now includes companion guidance for that pattern.

---

## OOT + RTK

OOT and RTK are complementary, not competing.

- `OOT` reduces context, model, heartbeat, and budget waste
- `RTK` reduces shell output waste

Use OOT when the problem is agent-side cost discipline. Use RTK when the problem is huge command output.

Typical combined flow:

```bash
python3 scripts/model_router.py "review this diff and summarize failing tests"
rtk git diff
rtk cargo test
python3 scripts/token_tracker.py check
```

Useful RTK commands in this workflow:

```bash
rtk git status
rtk git diff
rtk rg "pattern" .
rtk pytest
rtk cargo test
rtk docker logs my-container
```

### Install RTK

Homebrew:

```bash
brew install rtk
```

Linux/macOS quick install:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

Cargo:

```bash
cargo install --git https://github.com/rtk-ai/rtk
```

Verify install:

```bash
rtk --version
rtk gain
```

If you want RTK to actively help in coding sessions, initialize it after install:

```bash
rtk init -g
```

For Codex-style usage:

```bash
rtk init -g --codex
```

More detail: [references/RTK.md](references/RTK.md)

---

## Install

### ClawHub

```bash
clawhub install Cloud-Dark/oot
```

Listing: [clawhub.ai/Cloud-Dark/oot](https://clawhub.ai/Cloud-Dark/oot)

### Manual

```bash
git clone https://github.com/Cloud-Dark/oot.git \
  ~/.openclaw/skills/oot
```

Add the skill path to `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["~/.openclaw/skills/oot"]
    }
  }
}
```

One-line prompt:

> "Install the OOT skill from https://clawhub.ai/Cloud-Dark/oot or, if ClawHub isn't available, clone https://github.com/Cloud-Dark/oot and add the path to skills.load.extraDirs in openclaw.json"

---

## Quick Usage

Recommend context:

```bash
python3 scripts/context_optimizer.py recommend "debug this error"
```

Route a task:

```bash
python3 scripts/model_router.py "design a service architecture"
python3 scripts/model_router.py "thanks!"
```

Install heartbeat template:

```bash
cp assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md
python3 scripts/heartbeat_optimizer.py plan
```

Check budget:

```bash
python3 scripts/token_tracker.py check
```

Check whether RTK is a good fit for a task:

```bash
python3 scripts/token_tracker.py rtk "git diff and cargo test"
```

Show RTK companion guidance from the wrapper:

```bash
./scripts/optimize.sh rtk
```

---

## Built for Real Agent Work

OOT is useful when:

- your workspace injects too many files by default
- agents spend too much time on expensive models
- heartbeat sessions happen too often
- shell-heavy coding sessions inflate token usage
- you want local budget visibility without external services

It is especially effective in OpenClaw setups that mix normal chat, coding tasks, and routine monitoring flows.

---

## Native OpenClaw Alignment

OOT is designed to work well with modern OpenClaw capabilities such as:

- context pruning
- bootstrap size limits
- cache retention tuning
- built-in usage diagnostics

Useful built-ins:

```text
/context list
/context detail
/usage tokens
/usage cost
/status
```

OOT does not replace those features. It helps you use them more effectively and fills the gaps with local scripts.

---

## Files

```text
oot/
|-- SKILL.md
|-- SECURITY.md
|-- CHANGELOG.md
|-- .clawhubsafe
|-- .clawhubignore
|-- scripts/
|-- assets/
`-- references/
```

Important pieces:

- `scripts/context_optimizer.py`
- `scripts/model_router.py`
- `scripts/heartbeat_optimizer.py`
- `scripts/token_tracker.py`
- `scripts/optimize.sh`
- `references/RTK.md`

---

## Safety

The executable scripts in this repository are local-only.

- no network requests
- no subprocess spawning from the Python tools
- no system modification outside their intended local files

Full audit: [SECURITY.md](SECURITY.md)

Integrity check:

```bash
cd ~/.openclaw/skills/oot
sha256sum -c .clawhubsafe
```

---

## Links

- **ClawHub:** https://clawhub.ai/Cloud-Dark/oot
- **GitHub:** https://github.com/Cloud-Dark/oot
- **OpenClaw Docs:** https://docs.openclaw.ai
- **RTK Guide:** [references/RTK.md](references/RTK.md)
- **License:** MIT-0
- **Author:** [Cloud-Dark](https://github.com/Cloud-Dark)
