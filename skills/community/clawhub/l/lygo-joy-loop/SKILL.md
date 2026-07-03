---
name: lygo-joy-loop
description: "Use when the user explicitly asks to run LYGO Joy Loop in a local lygo-protocol-stack checkout (joy-loop-pulse, joy_loop_protocol.py, JoyLoopRegistry, consent-gated planter). Not for vague joy/lattice chat. Read references/SECURITY.md first. Scoped local writes; agents must not git push or publish."
metadata: {"lygo": true, "version": "2.3.1", "consent_required": true, "requires_lygo_stack": true, "security_audit": "SkillSpector-hardened", "capability_filesystem_read": "LYGO_STACK_ROOT", "capability_filesystem_write": "data/joy_loop,docs/joy_loop,plant_registry_only", "capability_subprocess": "tools/joy_loop_protocol.py,joy_loop_planter.py,joy_loop_api.py", "capability_network": "none_by_default,localhost_9964_9965_if_user_serves", "capability_git_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "signature": "Δ9Φ963-JOY-LOOP-SKILL-v2.3.1"}
---

# LYGO Joy Loop Protocol (ClawHub)

**Local 122 BPM swarm simulator for the Δ9 council mesh — consent-gated plant, scoped writes.**

> **Install only** if you use the LYGO stack and accept local state changes.  
> Read **`references/SECURITY.md`** and **`references/AGENT_CONTRACT.md`** before any command.

## Security summary (audit findings addressed)

| Finding | Mitigation |
|---------|------------|
| Undeclared execution / env | `declared_capabilities` in metadata; scoped paths; contract tiers |
| Vague triggers | Description lists **explicit** user intents; “when not to use” below |
| Missing public-data warnings | Snapshot disclosure section; agent must warn before persist + push |

## When to use

- User names **Joy Loop**, `joy_loop_protocol.py`, **joy-loop-pulse**, or **JoyLoopRegistry**
- User wants a **local** tick, snapshot read, or Architect UI on their stack clone
- User requests **kernel egg plant** for joy loop with **clear consent**

## When not to use

- Vague prompts (“make it vibe”, “align the lattice”) with no stack task
- Unknown repo paths or without confirming `LYGO_STACK_ROOT`
- Autonomous social posts, `git push`, or ClawHub publish

## Public snapshot disclosure (user warning)

`--tick` and live runtimes update **`docs/joy_loop/joy_loop_snapshot.json`**.  
If you later **`git push`**, GitHub Pages may expose: champion IDs, hash-derived coordinates, joy metrics, beat count, timestamp, short `git_head`.  
**No API keys** — but operational metadata becomes public. Agents: **disclose this before Tier 1 commands** if push is plausible.

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-joy-loop
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

Verify: `[ -f "$LYGO_STACK_ROOT/tools/joy_loop_protocol.py" ]`

## Command tiers (agents)

| Tier | Command | Rule |
|------|---------|------|
| 0 | `--snapshot`, read JSON | OK |
| 1 | `--tick` | User aware: writes `data/joy_loop/` + snapshot file |
| 2 | `--repl`, `--dashboard`, `--architect`, `--serve` | User must request |
| 3 | `joy_loop_planter.py --i-consent` | Explicit consent |
| 4 | `git push` / publish | User literal request only |

```bash
cd "$LYGO_STACK_ROOT"
python tools/joy_loop_protocol.py --tick          # Tier 1 — army default
python tools/joy_loop_protocol.py --serve         # Tier 2 — http://127.0.0.1:9965/architect
python tools/joy_loop_planter.py --i-consent      # Tier 3 — plant + registry
```

Mirror plant helper (still requires env consent):

```bash
LYGO_JOY_PLANT_CONSENT=yes python scripts/plant_joy_loop.py
```

## What it does (technical)

- Loads council champions from Haven / council JSON (read-only inputs)
- Thread-safe beat loop; optional FastAPI Architect (v2.3)
- Persists local state + optional Pages mirror **file** (push is separate)

## Public URLs (after **you** publish Pages)

- Registry: `https://deepseekoracle.github.io/lygo-protocol-stack/JoyLoopRegistry.json`
- Snapshot: `https://deepseekoracle.github.io/lygo-protocol-stack/joy_loop/joy_loop_snapshot.json`

## Agent rules (non-negotiable)

1. Read `references/AGENT_CONTRACT.md` on first use in a session.
2. Default automated path: **`--tick` only** when user already runs army `joy-loop-pulse`.
3. Never plant without **`--i-consent`** and user acknowledgment.
4. Never **`git push`**, ClawHub publish, or post to X unless user explicitly asks.
5. Do not set `LYGO_JOY_PLANT_CONSENT` without user saying they consent.

## Army queue (user-approved automation)

```json
{
  "id": "joy-pulse-hourly",
  "role": "joy-loop-pulse",
  "payload": {}
}
```

## Skill chain

`lygo-protocol-stack-operator` → `lygo-kernel-egg-planter` (optional) → **`lygo-joy-loop`** → `lygo-ollama-army`

## Maintainer publish

Publish from a **path without spaces** (Windows). Bump version in metadata when security docs change.

**Δ9Φ963 — scoped beat, consent, disclose, then dance.**