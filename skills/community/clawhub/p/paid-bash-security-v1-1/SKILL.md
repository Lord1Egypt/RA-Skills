---
name: Bash Security Validator — Production OpenClaw Shell Safety
slug: bash-security-validator-production-openclaw-shell-safety
version: 1.1.1
author: IntuiTek
tags: [security, production, engineering, hardening, bash, clawhavoc]
description: 23-validator bash security chain validated in production Claude Code deployments. Every check closed a real attack vector.
---

# Bash Security Validator — Production OpenClaw Shell Safety

> **Understand the threat model first?** Read the free primer:
> [OpenClaw Bash Safety — Why Your Agent Is a Security Risk](https://clawhub.ai/skills/free-bash-safety-primer)
> It covers what ClawHavoc exploited, why text-pattern matching alone fails, and
> why this validator exists.

---

## What This Skill Does

This skill installs a 23-validator bash security chain — the exact sequence
Anthropic runs in production Claude Code before every shell execution. It activates
on every `exec` tool call your OpenClaw agent makes.

**Validator categories:**

1. **Text-level** — Obvious attack pattern detection (destructive ops, unauthorized data transfer)
2. **Structural** — Substitution injection, brace expansion, heredoc abuse
3. **Encoding** — Unicode homoglyphs, zero-width characters, RTL overrides
4. **Shell-specific (Bash)** — Dangerous builtins, history manipulation, alias injection
5. **Shell-specific (Zsh)** — Separate blocklist; Zsh ≠ Bash for dangerous commands
6. **Persistence vectors** — Modifications to cron/init/systemd, shell profile backdoors
7. **Escalation vectors** — Sudo config changes, setuid manipulation, capability grants

Each category closes a distinct attack class. Skipping any one leaves a category
of attack unblocked.

---

## Setup

### Step 1 — Install

```bash
mkdir -p ~/.openclaw/workspace/skills/bash-security-validator
cp SKILL.md ~/.openclaw/workspace/skills/bash-security-validator/
```

Reload OpenClaw or restart the gateway.

### Step 2 — Verify Activation

After installation, the agent will validate bash commands before execution.
Test with a safe command:

```
Ask your agent: "Run: echo hello"
```

Normal execution proceeds. Then test a flagged pattern — a command that pipes
untrusted remote content directly into a shell interpreter. The validator should
intercept and refuse, explaining which validator triggered and why.

### Step 3 — Configure Enforcement Mode

Two modes available. Set in your agent system prompt or SOUL.md:

**Strict mode (recommended for production):** Block and report. The agent
stops, explains what triggered, and asks for confirmation or alternative.

**Audit mode (recommended for onboarding):** Log and warn. The agent notes
the risk but proceeds. Use this for 1–2 weeks to understand what your
existing workflows trigger before switching to strict.

Add to SOUL.md:
```
Bash security enforcement: strict
```

---

## The 23 Validators (Summary)

Full specification in `BASH_SECURITY_ARCHITECTURE.md` (included in package).

**Pre-processing gates (4):**
- Input encoding normalization
- Shell detection (Bash vs. Zsh — different validator chains)
- Context extraction (is this a file path? a URL? a string?)
- Privilege context check (is elevated execution in scope?)

**Text validators (5):**
- Destructive operation detection
- Unauthorized data transfer detection
- Credential access detection
- Package manager abuse patterns
- Known exploit signatures

**Structural validators (6):**
- Substitution injection (process substitution, backtick evaluation)
- Variable expansion abuse
- Brace expansion bombs
- Heredoc injection
- Redirection abuse
- Pipe chain analysis

**Encoding validators (4):**
- Unicode homoglyph detection
- Zero-width character stripping
- RTL override detection
- Multi-byte sequence normalization

**Persistence/escalation validators (4):**
- Cron/systemd/init modification detection
- Shell profile modification detection
- Privilege configuration changes
- Setuid/capability manipulation

---

## What ClawHavoc Exploited

341 skills on ClawHub (early 2026) contained malicious setup scripts that
passed all standard text-level checks. The attack vectors were:

1. Variable expansion with embedded command substitution
2. Heredoc injection in setup scripts
3. Unicode-obfuscated path references pointing to sensitive system locations

Three specific validators in this chain block all three attack vectors.
All three were absent from standard OpenClaw exec validation at the time.

---

## Compatibility

- OpenClaw 2026.3.x and above
- Validates both Bash and Zsh (separate chains)
- No external dependencies

---

## Bundle

This skill is included in the
[Production Agent Ops — Battle-Tested Architecture Pack](https://clawhub.ai/skills/production-agent-ops-battle-tested-architecture-pack)
along with 6 other production architecture files. If you need compaction,
loop termination, session memory, and the rest — the bundle costs less than
buying individually.
