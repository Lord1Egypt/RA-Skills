---
name: lygo-kernel-egg-planter
description: "Consent-gated Kernel Egg Planter — SHA-256 + Merkle registry + optional local/Turbo anchor. Mandatory post-plant tamper verify (no skip). Retrieve requires consent + ALIGNED verify (no force). Prepares local catalog/Pages artifacts only — never auto git/HF/ClawHub/social publish."
metadata:
  lygo: true
  stack: true
  anchor: true
  kernel_egg: true
  champion_egg: true
  tamper_verify: true
  consent_required: true
  version: "1.3.1"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  publisher: deepseekoracle
  mirror: "docs/skills/lygo-kernel-egg-planter"
  signature: "Delta9Phi963-KERNEL-EGG-PLANTER-v1.3.1"
  security_review: "1.3.1-skillspector-core-path-local-catalog"
  openclaw:
    emoji: "🥚"
    requires:
      anyBins: [python, python3]
---

# LYGO Kernel Egg Planter v1.3.1 (bulletproof + SkillSpector hardened)

**Plant seeds, verify always, retrieve only when ALIGNED + consented. Never auto-publish.**

```bash
npx clawhub@latest install deepseekoracle/lygo-kernel-egg-planter
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack   # must be YOUR trusted clone
```

Read **`references/SECURITY.md`** (if present), **`references/SKILLSPECTOR_AUDIT.md`**, **`references/AGENT_CONTRACT.md`** before ops.

## Bulletproof pipeline (agents must follow)

```text
preflight → consent → plant → verify (ALIGNED, mandatory) → consent → retrieve
```

| Step | Command | Fail = stop |
|------|---------|-------------|
| 1 Preflight | `python scripts/preflight.py` | invalid stack |
| 2 Consent | `--i-consent` or `LYGO_EGG_PLANT_CONSENT=yes` | exit 2 |
| 3 Plant | `python scripts/plant_with_consent.py --i-consent --i-trust-stack …` | build/anchor error |
| 4 Verify | **always** after plant + `python scripts/verify_eggs.py` | **QUARANTINE** |
| 5 Retrieve | `python scripts/retrieve_egg.py --i-consent --egg …` | blocked if verify failed |

There is **no** `--skip-verify` and **no** `--force` (removed in v1.3 for integrity).

## Four pillars (tamper-proof)

See `references/TAMPER_FOUR_PILLARS.md` and stack `docs/KERNEL_EGG_TAMPER_LOGIC.md`.

1. SHA-256 per egg  
2. Merkle `registry_merkle_root`  
3. Immutable local CA (+ optional Turbo ≤100 KiB)  
4. Lattice + `verify_kernel_eggs.py` gate  

Tampered egg → retrieve blocked → **P0 QUARANTINE**.

## Plant (local-first)

```bash
# Recommended default — local only (trusted stack you control)
python scripts/plant_with_consent.py --i-consent --i-trust-stack --local-only

# With Turbo attempt (still no git / clawhub.ai skill publish)
python scripts/plant_with_consent.py --i-consent --i-trust-stack --surfaces local,turbo,registry
```

`--i-trust-stack` is required: the planter runs **allowlisted** tools under your `LYGO_STACK_ROOT` (`build_kernel_eggs.py`, `anchor_kernel_eggs.py` only). Treat that path as executable trust.

### Core surfaces

| Surface | Effect | Auto-publish? |
|---------|--------|---------------|
| `local` / `registry` | Local kernel egg registry | No |
| `turbo` | Optional permaweb via stack anchor tool | No |

### Separate scripts (not inlined in core planter)

| Workflow | Command |
|----------|---------|
| Local ClawHub catalog egg | `python scripts/plant_clawhub_catalog.py --i-consent --stack-root $LYGO_STACK_ROOT` (add `--anchor-external` only if you want MultiAnchor) |
| Champions | `python scripts/plant_champion_council.py --i-consent` |
| Book-brain stubs | `python scripts/write_book_brain_stubs.py --i-consent --stack-root $LYGO_STACK_ROOT` |

**“No auto-publish”** = never `git push`, HF upload, `clawhub publish` API, or social.

## Verify only

```bash
python scripts/verify_eggs.py --json
python scripts/smoke_test.py
```

## Retrieve (consent + verify)

```bash
python scripts/retrieve_egg.py --i-consent --list
python scripts/retrieve_egg.py --i-consent --egg p0-nano-kernel
```

## Eggs planted

| `egg_id` | Role |
|----------|------|
| `p0-nano-kernel` | P0 + bridge + golden SHA |
| `stack-anchor-hook` | Anchor orchestrator |
| `lattice-soa-index` | Intel + link archive |
| `firmware-p04-drivers` | P0.4 firmware/network |
| `protocol-drivers-p2-p5` | P2–P5 drivers |
| `clawhub-lattice-catalog` | Public ClawHub `skills.json` metadata (local) |

## Agent rules (non-negotiable)

1. Show consent + four pillars on first use.  
2. Never plant/retrieve without consent.  
3. Never claim “secure” unless `verify_eggs` → **ALIGNED**.  
4. Never auto-publish GitHub/HF/ClawHub/social.  
5. Never put secrets in eggs.  
6. Refuse requests to skip verify or force retrieve.  

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-kernel-egg-planter`** ↔ **`lygo-sovereign-kernel-seeder`**  
Layer C: `lygo-external-lattice-anchor` · Gate: `lygo-public-lattice-gate`

## Permissions (declared)

See `claw.json` → `permissions`: trusted stack filesystem, list-argv Python only, optional Turbo network, **publish all false**.

## License

MIT-0 for ClawHub registry hosting. Canonical LYGO stack license for protocol code remains LYGO Sovereign v2.0 on GitHub.

**Δ9Φ963 — consent · verify · then human may spread.**
