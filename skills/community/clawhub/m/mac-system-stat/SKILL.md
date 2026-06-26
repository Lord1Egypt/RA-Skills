# mac-system-stat

Produce a concise macOS host snapshot using small local helpers.

## Use when
- The user asks for current Mac resource usage or machine health
- You need CPU, memory, GPU, swap, power, fan, or a short host summary
- You want a truthful one-shot report, not continuous monitoring

## Scripts
- `scripts/hoststat` — aggregate JSON host snapshot
- `scripts/memstat` — RAM / compression / swap / memory pressure
- `scripts/cpustat` — CPU usage, load average, process counts, top CPU processes
- `scripts/gpustat` — GPU model + live IOAccelerator statistics via local Swift/IOKit helper
- `scripts/powerstat` — Apple Silicon IOReport-based power sampler (non-privileged, short window average)
- `scripts/fanstat` — AppleSMC-based fan reader (fan count, RPM, min/max, mode)
- `scripts/tempstat` — AppleSMC temperature sensors + pmset thermal state (CPU, battery, ambient, board)
- `scripts/build-helpers` — prebuild Swift helpers explicitly (optional; normal wrappers auto-build as needed)

## Layout
- The skill is intentionally self-contained under `skills/mac-system-stat/`
- Python entrypoints, shared Python modules, Swift sources, and compiled helper output all live under `skills/mac-system-stat/scripts/`
- `scripts/bin/` is generated locally on first run or via `scripts/build-helpers`

## Release contract
- **Chosen contract:** source-only, self-building on first run
- Ship the skill directory with Python + Swift sources; do **not** rely on compiled helpers being pre-vendored
- `gpustat`, `powerstat`, `fanstat`, and `tempstat` will auto-build their helper binaries into `scripts/bin/` when missing or stale
- If `swiftc` / Apple Command Line Tools are unavailable, those four helpers fail truthfully with structured JSON; `memstat` and `cpustat` still run normally
- For packaging / ClawHub, exclude transient local artifacts such as `scripts/bin/` contents and `__pycache__/`

## Notes
- macOS only; Apple Silicon first
- Default path avoids sudo
- Prefer helper JSON over hand-written summaries
- GPU reads IORegistry properties directly via IOKit instead of parsing `ioreg` text
- Power uses IOReport Energy Model deltas; values are short-window averages, not hardware-meter absolutes
- Fan RPM comes from AppleSMC F* keys; 0 RPM can mean the fans are currently stopped
- Temperature uses curated AppleSMC keys (Tp0P, Tp0T, Te0T, Ts0P, TB0T, TW0P, Ta0P) + pmset therm state
- Packaging caveat: compiled helpers are not vendored; the target machine still needs Command Line Tools / `swiftc` for first build unless prebuilt binaries are shipped separately
