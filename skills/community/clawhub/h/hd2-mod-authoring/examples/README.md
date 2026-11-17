# Reference diagnostics

Two read-only Bingus addons that demonstrate the memory-inspection techniques in
`SKILL.md` section 11 and `references/memory-census.md`. Both **write nothing to game
memory** — they only read and dump to `%LOCALAPPDATA%/Hd2ProjRecon/`. They are worked
examples to copy from, not general-purpose tools.

## `refscan/` — LDLD census (clone-safety)

`addon: mods/dsh/refscan`

Scans readable memory for the `LDLD\1\0\0\0` magic and dumps every Data-Library table:
every LDLD header (type hash → name), every `ProjectileSettings` record (parsed + hex),
every weapon's `+0`/`+576` projectile reference, and the raw enemy tables (binary for the
big ones).

**Use it to prove a projectile record is "referenced by nothing" before you overwrite it**
— the clone-safe technique. The three dump bugs that each cost a relaunch (type-hash
filter, descriptor offset, hexdump freeze loop) are documented in
`references/memory-census.md`.

Output: `refscan_ldld.txt`, `refscan_projectiles.txt`, `refscan_weapons.txt`,
`refscan_weapondata.txt`, `refscan_enemy.txt`, `refscan_raw_*.txt`,
`refscan_bin_*.bin`.

## `fmscan/` — fingerprint value-scan (fire-mode record)

`addon: mods/dsh/fmscan`

Scans readable memory for a **value fingerprint** — the fire-mode record's mode array
`[single=2, burst=3, none=0]` at `+0x70/+0x74/+0x78` and `TertiaryFireMode=0` at
`+0x7C` — and dumps every candidate 144-byte record. This is the section 8 value-scan
technique (find a record by its *values* when its type hash is unknown), applied to the
~144-byte fire-mode record that holds single/burst/auto + cyclic rate.

Output: `fmscan_records.txt`.

## Running either

1. Import the zip into Arsenal, enable **Bingus Shared Loader + the diagnostic only**
   (disable other Lua mods so you read stock state).
2. Drop into one mission (the value-scan / full-process walk needs a few seconds).
3. Read the dump from `Hd2ProjRecon/`.

## Packing note

`thumbnail.png` is **excluded** from this repo (it is a 2048×2048 icon, ~3 MB, and not
instructive). The `tools/pack.py` in each folder reads `thumbnail.png` for the zip — drop
any 2048×2048 PNG at the folder root before running `python3 tools/pack.py`. The Lua,
`manifest.json`, and packer are the instructive parts.
