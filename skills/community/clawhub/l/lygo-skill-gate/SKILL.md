---
name: lygo-skill-gate
description: "LYGO Skill Gate — local pre-install skill risk scanner for OpenClaw/ClawHub packages. Scan any skill folder before you install or trust it: subprocess/shell, network/HTTP, secrets in source, eval/exec, webhook/exfil hints, permission-claim mismatches. Use when auditing ClawHub skills, reviewing SKILL.md safety, safe install checks, malware triage, or SkillSpector-style local gates. Pure stdlib. No network, no subprocess, no auto-install. Install clawhub:@deepseekoracle/lygo-skill-gate."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🛂"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-skill-gate"
    requires:
      anyBins: [python, python3]
  lygo: true
  security: true
  audit: true
  clawhub_safe_install: true
  signature: "Delta9Phi963-SKILL-GATE-v1.0.0"
  publisher: deepseekoracle
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "skill directory path you pass to scan"
      write: "skill state/ only with --i-consent"
    publish: false
    auto_install: false
---

# LYGO Skill Gate v1.0.0

**Scan before you install.**  

After ClawHavoc-style incidents, every human and every agent needs a **local** gate that reads a skill package and scores risk — without calling home, without running the skill.

**Signature:** `Delta9Phi963-SKILL-GATE-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-skill-gate`

---

## Problem this solves

| Who | Need |
|-----|------|
| **Humans** | “Is this ClawHub skill safe to install?” |
| **Agents** | “Before I load a skill tree, does code match its no-network / no-subprocess claims?” |
| **Operators** | Reproducible risk band + findings list for audit logs |

Searches: *skill security, audit skill, safe install, clawhub malware, skillspector local, scan SKILL.md*.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-skill-gate
```

---

## Commands

```bash
cd path/to/lygo-skill-gate
python scripts/self_check.py

# Scan a skill by path
python scripts/skill_gate.py scan "I:/E Drive/.grok/skills/lygo-context-guard"

# Or by slug (searches common skill roots)
python scripts/skill_gate.py scan lygo-ops-detector

# Self-demo (scan this package)
python scripts/skill_gate.py self-demo

# Write report under state/ (consent)
python scripts/skill_gate.py scan ./some-skill --write last_scan.json --i-consent
```

| Exit | Meaning |
|------|---------|
| 0 | clear / low |
| 5 | elevated or claim mismatch |
| 10 | high / critical — do not install casually |
| 2 | bad path / not a skill |

---

## What it checks

- `subprocess` / `os.system` / `Popen` / `shell=True`  
- HTTP clients, sockets, webhooks  
- `eval` / `exec`, pickle, unsafe yaml  
- Hardcoded key-like strings  
- Destructive deletes, git push / auto-publish hints  
- **Claim mismatch**: frontmatter says `network: false` but code uses `urlopen`  

**Does not:** download skills, install skills, execute scanned code, or phone home.

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-context-guard` | Token budget + secret redact for prompts |
| `lygo-ops-detector` | Discourse signal heuristics |
| `lygo-kickstart-wizard` | Onboarding map |

---

## License

**MIT-0**.  
**Δ9Φ963 — verify before trust · local gate · human remains the publisher.**
