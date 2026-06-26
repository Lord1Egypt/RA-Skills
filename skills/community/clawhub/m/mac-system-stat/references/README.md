# mac-system-stat references

This skill is now designed to run from its own directory.

## Current structure

- `skills/mac-system-stat/scripts/*.py` — canonical Python helper entrypoints and shared modules
- `skills/mac-system-stat/scripts/swift/` — canonical Swift helper sources
- `skills/mac-system-stat/scripts/bin/` — locally generated helper binaries
- `skills/mac-system-stat/scripts/build-helpers` — convenience wrapper for explicit prebuilds

## Build behavior

- Release contract: **source-only, self-building on first run**
- `gpustat`, `powerstat`, and `fanstat` auto-build their Swift helpers when missing or stale
- `scripts/build-helpers` can prebuild all Swift helpers, or one named helper
- Normal use from the skill folder does not depend on `projects/mac-system-stat/scripts/`
- If `swiftc` is unavailable, Swift-backed helpers fail explicitly; this is a runtime prerequisite, not a hidden packaging step

## Packaging guidance

- Treat `skills/mac-system-stat/` as the canonical publishable unit
- Do not rely on checked-in `scripts/bin/` artifacts; they are local build output
- Exclude transient local artifacts such as `scripts/bin/*` and `scripts/__pycache__/` when packaging

## Remaining dev-only bits

- The project-level `projects/mac-system-stat/scripts/` tree still exists as a parallel dev copy; it is no longer required by the skill at runtime
