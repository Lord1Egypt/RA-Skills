# SkillSpector / ClawHub audit — lygo-mint-verifier v1.1.1

**Signature:** `Delta9Phi963-MINT-VERIFIER-v1.1.1`  
**Audit page:** https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier/security-audit  
**Live version target:** 1.1.1

## Finding: subprocess module call (Medium) — **FIXED** (1.1.0)

| Was | Now |
|-----|-----|
| `mint_pack_local.py` called `subprocess.run` on external `tools/lygo_mint` | In-process canonicalize + SHA-256 in `mint_cli.py` |
| Bundle incomplete without workspace tools | Self-contained skill |

## Finding: Undeclared permissions / Lp3 (Medium) — **FIXED** (1.1.0)

Declared in `SKILL.md` metadata + `claw.json`: network false, subprocess false, consent-gated writes.

## Finding: Intent-Code Divergence (Medium) — **FIXED** (1.1.1)

ClawHub SkillSpector (~97% confidence):

> The wrapper defeats the tool's stated explicit-consent control by silently appending `--i-consent` whenever it is absent.

**Root cause:** `scripts/backfill_anchors.py` appended `--i-consent` if missing.

**Fix:** Pass-through only — `sys.argv = [prog, "backfill", *sys.argv[1:]]`. No consent injection.

## Finding: Description-Behavior Mismatch (Medium) — **FIXED** (1.1.1)

Same root cause / fix. Manifest advertises `ledger writes need --i-consent`; wrappers must not undermine that gate.

## Proof

```bash
python scripts/self_check.py
# ast_clean true · consent_wrapper_honest true · mint/verify/snippet/backfill ok
```

Static analysis expectation after republish: no remaining Medium findings for consent bypass.
