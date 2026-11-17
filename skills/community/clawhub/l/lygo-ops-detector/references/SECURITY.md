# LYGO Ops Detector — SECURITY & ETHICS v1.4.0

## Declared permissions

| Capability | Status |
|------------|--------|
| Network | **None** (stdlib local only) |
| Shell / subprocess | **None** |
| Read files | Opt-in `--text-file` / `--assoc-file` / `--public-meta-file` **only with `--i-consent`** |
| Write files | `eval_ops_detector.py` writes **only under skill `tests/`** |
| Env harvesting | **No** |
| Publish / social | **No** |

## v1.4.0 note

Public metadata is a **weighted context channel**. Operator supplies fields (`account_based_in`, `claimed_location`, `location_accurate`, HTTPS-cited `named_public_incident`, batch). There is **no country denylist**. A geo label alone cannot clear ops_score 0.65. JSON may emit `public_meta_mismatch` / `named_public_incident` flame hints — still **not** identity verdicts.

v1.3.0 still applies: half-truth + saturation channels.

## Core mandate

Heuristic **discourse** analysis of evasion and coordination *signals* in text the operator supplies.

It is **not**:

- A doxing tool  
- An identity, profession, or affiliation profiler  
- A sole-evidence engine for accusations  
- A warrant to scan private mail/logs without consent  
- A social-graph crawler  

## Non-negotiables

1. **Text over identity** — unit of analysis is statement/log content, not personhood.  
2. **Consent** for private communications and association lists (`--i-consent` on file paths).  
3. **Receipts** — high scores require cited pattern hits; never “trust the detector.”  
4. **No affiliation / bare job-title dictionaries** — no fraternity/brotherhood/lodge; no bare military/intelligence/agency scoring.  
5. **Public fields are context, not guilt** — no nationality table; named incidents need an `https://` RESOURCE URL; no live scrape of X or other sessions.  
6. **Operational bar honesty** — `ops_score≥0.65` (or high evasion) for strong language; country-only is gated below that bar.  
7. **Human review** before any reputational, employment, legal, or social action.  
8. **Least-privilege writes** — eval reports cannot escape skill `tests/`.  

## Failure modes to reject

- Treating low scores as “innocent person” or high scores as “guilty person”  
- Using affiliation/religion/job title **or nationality** as a proxy for ops  
- Feeding outputs to social pile-ons  
- Advertising calibration metrics as production performance  
- Arbitrary `--out` paths outside `tests/`  

## Agent contract

- Invoke only when the user asks for ops-detector / AETHONΔ9 / evasion-index style analysis.  
- Do not auto-scan session email/logs without explicit intent + consent.  
- Prefer `--text` paste; file paths require `--i-consent`.  

**Δ9Φ963**
