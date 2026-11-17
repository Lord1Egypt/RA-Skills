# Security — lygo-continuum-integrator

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Subprocess / shell | **None** |
| Filesystem write | **Off** unless `--write` **and** `--i-consent` |
| Publish (git/HF/ClawHub/social/Star Chart) | **None** |

## Guarantees

- Pure local advisor (stdlib only)
- Collapse refused by default
- Chaos treated as constructive interference only (`--allow-destructive` to relax)
- No auto-publish

## Agent rules

1. Run `python scripts/self_check.py` before trust.
2. Prefer stdout receipts; write to disk only with explicit human `--i-consent`.
3. Pair with `lygo-geodesic-sealer` for dual-ledger locks; this skill does not phone home.
