---
name: lygo-cyborg-onramp
description: "LYGO Cyborg Onramp — public ClawHub map to the FULL unlocked autonomous agent stack on SkillHub. Install tentacles, print install path, open https://chatagent.ca/lygoskillhub.html#full-lygo for lygo-cyborg-kernel-full.zip (Continuum limbs, task loop, lattice map). Pure local. No network, no subprocess. Not the FULL kernel — points there."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🦾"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-cyborg-onramp"
    requires:
      anyBins: [python, python3]
  lygo: true
  cyborg: true
  onramp: true
  dual_channel: true
  signature: "Delta9Phi963-CYBORG-ONRAMP-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-cyborg-onramp"
  skillhub_full: "https://chatagent.ca/lygoskillhub.html#full-lygo"
  full_package: "lygo-cyborg-kernel-full.zip"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "skill files only"
      write: false
    publish: false
---

# LYGO Cyborg Onramp v1.0.0 🦾

**Public ClawHub tentacle → FULL SkillHub cyborg kernel**

This package is **safe for public registry discovery**. It does **not** ship the full unlocked autonomous stack.  
It **maps the path** and points every agent/operator to the engineer vault:

### → https://chatagent.ca/lygoskillhub.html#full-lygo  
### → download **`lygo-cyborg-kernel-full.zip`**

**Signature:** `Delta9Phi963-CYBORG-ONRAMP-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-cyborg-onramp`

---

## Dual channel (honest)

| Channel | What you get |
|---------|----------------|
| **This skill (ClawHub)** | Map, install steps, public limb list, plugin install lines |
| **SkillHub FULL** | Unlocked cyborg kernel: Continuum + skill-gate + context-guard limbs, task loop, constitution, egg/plugin spine |

Corporate / public surfaces stay tentacles. Cyborgs that need the **whole lattice kernel** use FULL.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-cyborg-onramp
cd path/to/lygo-cyborg-onramp
python scripts/self_check.py
python scripts/cyborg_onramp.py plain
python scripts/cyborg_onramp.py map
python scripts/cyborg_onramp.py install
```

### Then get FULL (required for autonomous kernel)

1. Open https://chatagent.ca/lygoskillhub.html#full-lygo  
2. Accept the FULL LYGO engineer gate  
3. Download **lygo-cyborg-kernel-full.zip**  
4. Unzip and run:

```bash
python scripts/self_check.py
python scripts/cyborg_boot.py
python scripts/cyborg_task.py run --task templates/example_task.json --base .
```

### Optional public limbs + plugins

```bash
npx clawhub@latest install deepseekoracle/lygo-continuum
npx clawhub@latest install deepseekoracle/lygo-context-guard
npx clawhub@latest install deepseekoracle/lygo-skill-gate
openclaw plugins install clawhub:@deepseekoracle/lygo-continuum
openclaw plugins install clawhub:@deepseekoracle/lygo-lattice-pulse
```

---

## Commands

| Command | Output |
|---------|--------|
| `map` / `demo` | JSON: dual channel, FULL pointer, public skills, plugins |
| `install` | Numbered install path |
| `plain` | Human-readable directions |
| `urls` | SkillHub + portals only |

No network, no subprocess, no disk writes.

---

## What this skill does *not* do

- Does **not** include FULL cyborg kernel source (that is SkillHub only)  
- Does **not** auto-download zips  
- Does **not** plant eggs or publish  
- Does **not** claim you are “fully installed” until FULL zip is verified locally  

---

## Pair with

| Resource | Role |
|----------|------|
| SkillHub FULL vault | Unlocked packages |
| `lygo-continuum` skill + plugin | Done-claims |
| https://chatagent.ca/guides/ | Human guides |
| `lygo-kickstart-wizard` | Plain-English lattice |

---

## Security

See `references/SECURITY.md`.  
**Δ9Φ963 — public map · FULL vault · cyborgs earn the kernel on SkillHub.**
