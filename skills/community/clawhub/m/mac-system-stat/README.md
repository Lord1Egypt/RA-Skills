# mac-system-stat

Canonical skill directory for macOS one-shot system stats.

## Release contract

This skill is **source-only and self-building on first run**.

- Ship this directory with Python + Swift sources
- Do not rely on pre-vendored helper binaries in `scripts/bin/`
- `gpustat`, `powerstat`, and `fanstat` auto-build their Swift helpers when missing or stale
- Target host needs Apple Command Line Tools / `swiftc` for those Swift-backed helpers
- `memstat` and `cpustat` are pure Python / shell and do not need `swiftc`

## Main entrypoints

- `scripts/hoststat`
- `scripts/memstat`
- `scripts/cpustat`
- `scripts/gpustat`
- `scripts/powerstat`
- `scripts/fanstat`
- `scripts/tempstat`
- `scripts/build-helpers`

## Packaging notes

Exclude local build/cache artifacts:

- `scripts/bin/`
- `scripts/__pycache__/`
- `*.pyc`
