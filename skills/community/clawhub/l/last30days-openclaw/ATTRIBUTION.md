# Attribution and Provenance

This OpenClaw skill is adapted from:
- **Project:** `last30days-skill`
- **Author:** [@mvanhorn](https://github.com/mvanhorn)
- **Source:** <https://github.com/mvanhorn/last30days-skill>
- **License:** MIT

## Provenance summary

- `scripts/`, `fixtures/`, and `variants/` were sourced from the upstream repository.
- OpenClaw adaptation files created here:
  - `skill.json`
  - `SKILL.md`
  - `README.md`
  - `ATTRIBUTION.md`
  - `scripts/setup_openclaw_env.sh`
  - `scripts/openclaw_watchlist_run.sh`
- OpenClaw-specific path and secret handling updates were applied in:
  - `scripts/lib/env.py`
  - `scripts/store.py`
  - `scripts/briefing.py`
  - `scripts/lib/render.py`
  - `scripts/lib/ui.py`
  - `scripts/last30days.py`

## Third-party vendored component

- `scripts/lib/vendor/bird-search/*`
  - Upstream package: `@steipete/bird` subset
  - License: MIT
  - License file included at: `scripts/lib/vendor/bird-search/LICENSE`

## Representation policy

This adaptation must be described as an **OpenClaw packaging/integration layer** over @mvanhorn's original work, not as a new original research engine.
