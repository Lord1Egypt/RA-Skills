---
name: lygo-skill-spector
description: "LYGO SkillSpector — enhanced local pre-install skill risk scanner for OpenClaw/ClawHub packages. Scan, gate (CI max-band), batch, and Markdown report: subprocess/shell, network/HTTP/httpx, secrets, eval/exec, curl|bash, miners, claim mismatches. Use when auditing ClawHub skills, SkillSpector-style gates, safe install checks, malware triage. Pure stdlib. No network, no subprocess, no auto-install. Builder HTML/multi-root pack on SkillHub FULL if running a full stack. Install clawhub:@deepseekoracle/lygo-skill-spector."
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    emoji: "🔭"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-skill-spector"
    requires:
      anyBins: [python, python3]
  lygo: true
  security: true
  audit: true
  clawhub_safe_install: true
  skillspector: true
  signature: "Delta9Phi963-SKILL-SPECTOR-v1.0.1"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-skill-spector"
  skillhub_full: "https://chatagent.ca/lygoskillhub.html#full-lygo"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "skill directory path you pass to scan/gate/batch/report"
      write: "skill state/ only with --i-consent"
    publish: false
    auto_install: false
---

# LYGO SkillSpector v1.0.1

**Scan before you install — gate before you ship.**

Enhanced local risk scanner for OpenClaw/ClawHub skill packages. Successor surface to Skill Gate with **CI gate**, **batch**, **Markdown report**, and deeper rule pack (httpx, curl|bash, PowerShell IEX, miners, HF/OpenAI key shapes).

**Signature:** `Delta9Phi963-SKILL-SPECTOR-v1.0.1`  
**ClawHub:** `@deepseekoracle/lygo-skill-spector`  
**Audit response:** `references/SKILLSPECTOR_AUDIT.md` (v1.0.0 meta-scan false positives fixed)

> **Builder version (full stack):** If you run a **full LYGO stack**, the unlocked **builder** pack (HTML multi-root reports, multi-gate CI matrix, dashboard JSON) is on  
> **[SkillHub FULL LYGO](https://chatagent.ca/lygoskillhub.html#full-lygo)**  
> as `lygo-skill-spector` FULL RAW (+ `builder/`).

---

## Dual channel

| Channel | What you get |
|---------|----------------|
| **ClawHub (public)** | `scan` · `gate` · `batch` · `report` · `self-demo` — tentacle |
| **SkillHub FULL** | Same + **builder/** HTML batch, multi-root gate, CI summary — unlocked RAW |

---

## Install (public)

```bash
npx clawhub@latest install deepseekoracle/lygo-skill-spector
```

FULL engineer RAW: https://chatagent.ca/lygoskillhub.html#full-lygo

---

## Commands

```bash
cd path/to/lygo-skill-spector
python scripts/self_check.py

# Scan one skill
python scripts/skill_spector.py scan "I:/E Drive/.grok/skills/lygo-context-guard"
python scripts/skill_spector.py scan lygo-ops-detector

# CI gate (exit non-zero if risk worse than max-band)
python scripts/skill_spector.py gate ./some-skill --max-band low

# Batch under a skills root
python scripts/skill_spector.py batch "I:/E Drive/.grok/skills"

# Markdown report
python scripts/skill_spector.py report ./some-skill
python scripts/skill_spector.py report ./some-skill --write last.md --i-consent

# Self-demo
python scripts/skill_spector.py self-demo
```

### FULL builder only (SkillHub)

```bash
python builder/skill_spector_builder.py html-batch ./skills --write batch.html --i-consent
python builder/skill_spector_builder.py multi-gate ./skills --max-band elevated
python builder/skill_spector_builder.py ci-summary ./skills --write ci.json --i-consent
```

| Exit | Meaning |
|------|---------|
| 0 | clear / low (or under max-band) |
| 5 | elevated or claim mismatch |
| 10 | high / critical |
| 2 | bad path / not a skill |

---

## What it checks

- `subprocess` / `os.system` / `Popen` / `shell=True` / PowerShell `IEX`  
- HTTP clients (`urllib`, `requests`, `httpx`, `aiohttp`), sockets, webhooks  
- `curl|bash` / `wget|bash` remote-code patterns  
- `eval` / `exec`, pickle, unsafe yaml  
- Hardcoded key-like / token-shaped strings (vendor project-key and HF-style prefixes)  
- Destructive deletes, force-push, auto-publish / ClawHub publish hints  
- Mining / keylogger-style IOC *detection* signals (rules only — not mining code)  
- **Claim mismatch**: frontmatter says `network: false` but code uses HTTP  

**Does not:** download skills, install skills, execute scanned code, or phone home.

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-skill-gate` | Lighter single-scan gate (still supported) |
| `lygo-context-guard` | Token budget + secret redact |
| `lygo-continuum` | Seal “scanned clean” as checkable claims |
| `lygo-kickstart-wizard` | Onboarding map |

---

## License

**MIT-0**.  
**Δ9Φ963 — verify before trust · local spector · human remains the publisher.**
