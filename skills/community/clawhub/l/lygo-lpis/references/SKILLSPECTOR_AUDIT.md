# SkillSpector audit response — lygo-lpis v1.1

**Signature:** Δ9Φ963-LPIS-SKILLSPECTOR-v1.1

NVIDIA SkillSpector (ClawHub Inspector) reviewed v1.0 and reported **3 medium findings** (no malware; VirusTotal 64/64 clean). This revision addresses documentation, triggers, and ingest consent.

## Findings → mitigations

| Finding | Severity | Mitigation (v1.1) |
|---------|----------|-------------------|
| **Vague Triggers** | Medium | Replaced marketing phrases with **explicit when-to-use** (4 concrete triggers) and **when-NOT-to-use** (5 exclusion rules) in `SKILL.md`. Description metadata lists required skill names/CLI only. |
| **Missing User Warnings** | Medium | Prominent **Security notice** block at top of `SKILL.md`; expanded `references/SECURITY.md` with authorization, prohibited sources, data limits, and incident response. |
| **SSD-3 (sensitive collection)** | Medium | Ingest requires **`--i-authorize`** or `LYGO_LPIS_INGEST_AUTHORIZED=yes` (`lygo_lpis/consent.py` + CLI gate). Data boundary table documents local-only vault; no auto-upload. Tagline changed from "map the leak" to "map the pattern". Prohibits leaked/third-party confidential ingest in skill + security docs. |

## Code controls

| Control | Location |
|---------|----------|
| Ingest consent gate | `lygo_lpis/consent.py`, `framework.ingest(authorized=…)` |
| CLI `--i-authorize` | `tools/lygo_lpis.py ingest` |
| P0 size/quarantine | `lygo_lpis/gatekeeper.py` |
| Advisory implant only | `lygo_lpis/harmony.py`, `framework.implant` |
| Self-check | `scripts/self_check.py` |

## Operator checklist

1. Read `SKILL.md` security notice and `references/SECURITY.md`.
2. Run `python scripts/self_check.py` from skill directory (with `LYGO_STACK_ROOT` set).
3. Ingest **only** with user attestation: `--i-authorize`.
4. Review sovereign variants locally before manual implant.
5. Plant egg only with `python tools/lpis_planter.py --i-consent`.
6. Never commit `data/prompt_vault/*.txt` bodies to public git.

## Re-audit expectation

- **Vague Triggers:** bounded invoke conditions + exclusions present in skill markdown.
- **User Warnings:** first-screen notice + SECURITY.md depth.
- **SSD-3:** consent-gated ingest + explicit prohibition on unauthorized/leaked sources + local-only storage documented.