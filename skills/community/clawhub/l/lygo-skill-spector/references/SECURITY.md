# Security — LYGO SkillSpector v1.0.1

## Defaults

| Capability | Status |
|------------|--------|
| Network | **None** — never downloads or installs skills |
| Subprocess | **None** — never executes the scanned skill |
| Read | Path you pass to `scan` / `gate` / `batch` / `report` |
| Write | `state/` only with `--i-consent` |

## Dual channel

| Package | Surface |
|---------|---------|
| ClawHub public | Core scanner + gate/batch/report |
| SkillHub FULL builder | + `builder/` HTML batch, multi-gate, CI summary |

Builder tools keep the same defaults (no network, no subprocess). Review FULL zip independently if you download it.

## Meta-scan hygiene (v1.0.1)

Rule tables that match miner / secret *shapes* are built from **string fragments** so third-party scanners do not treat the detector as the threat. `self_check` fixtures assemble synthetic dirty samples at runtime only (temp dir).

See `references/SKILLSPECTOR_AUDIT.md` for the v1.0.0 audit response.

## Ethics

- Best-effort static heuristics — not a guarantee of safety  
- Absence of findings ≠ trusted code  
- High findings ≠ proven malware (could be legitimate operator tools)  
- Snippets printed from scanned files may include secrets already present there — do not share reports carelessly  
- Human decides install  

**Δ9Φ963 — verify before trust.**
