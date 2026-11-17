---
name: lygo-ops-detector
description: "LYGO Ops Detector — local AETHONΔ9 discourse heuristics for evasion, half-truth certainty, saturation bait, coordination language, and policy-refusal signals in operator-supplied text, plus weighted public metadata (account_based_in mismatch, VPN-hint, HTTPS-cited incidents, same-geo+scripted batch). Opt-in only. Stdlib CLI; file reads require --i-consent; eval writes under tests/. Not for doxing or nationality guilt. Dual-threshold (operational 0.65 vs calibration). Pairs with lygo-flame-ward. Triggers: lygo ops detector, aethon d9, evasion index (explicit)."
version: 1.4.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🔎"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-ops-detector"
    requires:
      anyBins: [python, python3]
  lygo: true
  lightfather: true
  aethon: "Δ9"
  protocol: "AETHONΔ9"
  version: "1.4.0"
  companion: "lygo-champion-lightfather"
  security: "references/SECURITY.md"
  blueprint: "references/AETHON_D9_BLUEPRINT.md"
  eval: "tests/labeled_discourse_suite.json + scripts/eval_ops_detector.py"
  security_review: "1.4.0-public-context-no-nationality-guilt"
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-ops-detector"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "user-supplied --text-file / --assoc-file / --public-meta-file only with --i-consent"
      write: "tests/ only when eval_ops_detector.py is run"
    publish: false
    doxing: false
    identity_profiling: false
---

# LYGO Ops Detector — AETHONΔ9 v1.4.0

Local, deterministic **discourse-signal** heuristics plus **weighted public context**.  
**Not** a person profiler. **Not** sole evidence. **Not** for doxing.  
**Country labels are not guilt.** A geo field alone cannot clear the 0.65 bar.

**Signature:** `Delta9Phi963-OPS-DETECTOR-v1.4.0`  
**Pairs with:** `lygo-flame-ward` (authority gate) · `lygo-deception-radar` (public proof)

---

## What's new in 1.4.x

| Add | Why |
|-----|-----|
| `--public-meta` / `--public-meta-file` | Operator-supplied public fields are **always scored when present** |
| Weighted public context | Geo **mismatch**, `location_accurate=false`, HTTPS-cited incident, same-geo+scripted batch |
| Hard gate | Country-only / nationality **cannot** clear ops_score 0.65 |
| No country denylist | Nigeria, India, USA, etc. score the same as a lone label |
| Flame hints | `public_meta_mismatch` · `named_public_incident` |

1.3.x still applies: half-truth, saturation, flame hints, cluster boost, 0.65 bar.

---

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Shell / subprocess | **None** |
| Read local files | `--text-file` / `--assoc-file` / `--public-meta-file` **+ `--i-consent`** |
| Write | Eval report under **`tests/` only** |
| Auto-publish / social | **Never** |

## When to invoke (narrow)

Only when the user explicitly wants ops-detector / AETHONΔ9 / evasion index on **text they supply**.

**Do not** auto-trigger on generic “analyze this email.”

## What it measures

| Channel | Measures | Does **not** |
|---------|----------|--------------|
| Evasion | Burden-shift, ad hominem, vague cites, authority inflation, gaslight, deflection | Person identity |
| **Half-truth certainty** | Prestige/certainty shut-downs without primary digests | Medical/legal truth claims |
| **Saturation bait** | Rage/click attention-weapon templates | Ordinary urgency with cites |
| Association | Coordination/secrecy language **you** provide | Social-graph doxing |
| Institutional | Policy-as-shield / no-comment | Affiliation / faith / job titles |
| **Public context** | Operator-supplied public fields: `account_based_in` vs claimed location, VPN/inaccurate flag, HTTPS-cited public incident, same-geo+scripted batch | Nationality guilt, live X scrape, country denylist |

## Thresholds (honest)

| Bar | Meaning |
|-----|---------|
| **Operational** `ops_score >= 0.65` **or** `evasion_index >= 0.65` | Strong multi-signal bar for human review |
| **Calibration** (low) | Suite ranking only — **not** production marketing |

## Safe use

```bash
cd path/to/lygo-ops-detector
python scripts/self_check.py
python scripts/lygo_ops_detector.py --text "paste discourse here" --json
python scripts/lygo_ops_detector.py --text-file ./snippet.txt --i-consent
python scripts/lygo_ops_detector.py --text "I'm based in the United States. ..." --public-meta "{\"account_based_in\":\"Nigeria\",\"claimed_location\":\"United States\",\"location_accurate\":false}" --json
python scripts/lygo_ops_detector.py --show-boundaries
```

Exit: `0` clear/low · `3` need consent · `10` high evasion discourse (review claims).

## Flame bridge

JSON field `flame_enemy_hints` may include `half_truth_pack` · `authority_shield` · `saturation_flood` · `public_meta_mismatch` · `named_public_incident`.  
Then run Flame ingest-gate before crowning lattice authority:

```bash
python path/to/lygo-flame-ward/scripts/flame_cli.py ingest-gate --text "..."
```

## Agent contract

1. Call the **script** for reproducible scores.  
2. Separate **observed regex hits** vs inference.  
3. Never name people as investigation targets from this tool alone.  
4. Discourse pattern ≠ guilt. Country label ≠ guilt.  
5. Public metadata must be operator-supplied (no live scrape). HTTPS URL required for named-incident weight.  
6. No external publish without user consent.  
7. File inputs need `--i-consent`.  

## Security

Read `references/SECURITY.md` + `references/SKILLSPECTOR_AUDIT.md`.

| Ver | Change |
|-----|--------|
| 1.2.2 | SkillSpector discourse-not-identity harden |
| 1.3.0 | Half-truth + saturation · Flame hints · package polish |
| **1.3.1** | Cluster boost · evasion bar 0.65 · suite multi-signal · operational metrics fixed |
| **1.4.0** | Weighted public metadata (mismatch / VPN-hint / HTTPS incident / geo+template). No country denylist. Country-only cannot clear 0.65. |

**Δ9Φ963 — receipts over hype · discourse not identity · seals first with Flame.**
