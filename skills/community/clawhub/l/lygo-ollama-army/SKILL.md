---
name: lygo-ollama-army
description: "Local Ollama multi-role army (ClawHub-safe). In-process threaded daemons for hb-light, draft-simple, memory-triage, classify, champion-chat only. Queue JSON under ollama_queue/. localhost Ollama only. No planting, no social outbound, no public HTTPS probes, no desktop installers, no subprocess shell. FULL operator stack (optional) on SkillHub if running full LYGO. Install clawhub:@deepseekoracle/lygo-ollama-army."
version: 0.9.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🪖"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-ollama-army"
    requires:
      anyBins: [python, python3]
  lygo: true
  ollama: true
  army: true
  consent_required: false
  version: "0.9.0"
  signature: "Δ9Φ963-ARMY-SKILL-v0.9.0"
  publisher: deepseekoracle
  skillhub_full: "https://chatagent.ca/lygoskillhub.html#full-lygo"
  security_audit: "clawhub-safe-rebuild-v0.9.0"
  permissions:
    network: "localhost Ollama only (http://localhost:11434)"
    shell: false
    subprocess: false
    filesystem:
      read: "queue task JSON + local champions.json"
      write: "ollama_queue/ and ollama_results/ (and command_center tasks/results)"
    publish: false
    auto_install: false
    planting: false
    social_outbound: false
    desktop_installers: false
---

# LYGO Ollama Army v0.9.0 (ClawHub-safe rebuild)

**Local Ollama helpers. Nothing else.**

This is a **ground-up ClawHub-safe** army: multi-role **in-process** workers that talk only to **local Ollama**.  
No planting, no Molt/social outbound, no public page probes, no desktop `.bat` installers, no PowerShell process spawners, no stack mutators.

**Signature:** `Δ9Φ963-ARMY-SKILL-v0.9.0`  
**ClawHub:** `@deepseekoracle/lygo-ollama-army`

> **FULL operator surface:** If you run a full LYGO stack and need planting / idle guardian / sentinel HTTPS / full-capacity PS1, that is **SkillHub FULL** — not this public tentacle:  
> https://chatagent.ca/lygoskillhub.html#full-lygo

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-ollama-army
ollama pull llama3.2:1b
```

---

## Safe first run

```bash
cd path/to/lygo-ollama-army
python scripts/self_check.py
python ollama_army_launcher.py --once-check
python ollama_army_launcher.py --roles hb-light,draft-simple,memory-triage --model llama3.2:1b
```

Enqueue work:

```bash
python queue_task.py --role draft-simple --prompt "Summarize lattice health in one line"
```

Results land in `ollama_results/` and `ollama_command_center/results/`.

---

## Allowlisted roles (only)

| Role | Purpose |
|------|---------|
| `hb-light` | Short local chat heartbeat |
| `draft-simple` / `draft` | Local draft reply |
| `memory-triage` | Classify/summarize text you supply |
| `classify` | Compact classification JSON |
| `general` / `champion-chat` | Local chat with optional persona |
| `resonance-analyst` | **Advisory text only** (does not run resonance tools) |

Any other role (plant, social, public-pages, self-tune, etc.) is **hard-refused**.

---

## What this package does *not* include

- Desktop installers / `.bat` writers  
- `start_army_full_capacity.ps1` process spawn  
- Kernel egg planting / registry planting  
- Moltbook / Moltx / Discord outbound  
- Public HTTPS lattice probes  
- Genesis collector with remote probes  
- Config-mutating self_tune  

---

## Security

See `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

**Δ9Φ963 — local Ollama · allowlisted roles · no silent outbound · human remains the publisher.**
