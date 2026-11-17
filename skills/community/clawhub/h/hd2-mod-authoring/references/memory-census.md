# Read-only memory census (refscan) — LDLD table scan + clone-safety verification

The throwaway addon that dumps game memory to `Hd2ProjRecon/` so a projectile record can
be proven "referenced by NOTHING" before cloning (SKILL section 11). Writes nothing to
game memory. Verified 2026-10-06 across four revisions (diag-1 → diag-4).

## LDLD table format (memory)

Every Data-Library table starts with the 8-byte magic `LDLD\1\0\0\0` (`0x4C 0x44 0x4C
0x44 0x01 0x00 0x00 0x00`). The 24-byte header follows at the table base (call it
`magic`):

- `magic+4`  u32 version (= 1)
- `magic+8`  u32 type hash = `dlsum(type_name)` — see install-and-format.md
- `magic+12` u32 size (payload bytes, excludes the 24-byte header)
- `magic+24` u64  DLArray descriptor field 1
- `magic+32` u64  DLArray descriptor field 2

Three array shapes follow the header:

- **settings-array** (ProjectileSettings, DamageSettings): `magic+24` = `{u64 ptr, u64
  count}`; `stride = (size - 16) / count`; records at `ptr` (absolute when `> 0x10000`,
  else `magic+24+ptr`).
- **keyed / bucket-array** (ProjectileWeapon, WeaponData, and EVERY enemy table): a
  bucket array of 16-byte entries `{u64 entity, u32 slot, u32 pad}` — walk while
  `pad == 0 and slot <= 100000` — then fixed-stride records.
- **hashmap** (WeaponMagazine, HealthComponentData): capacity at +136; records elsewhere.

The read-only scanner walks readable committed regions (`VirtualQuery` state==4096) in
256 KB chunks with 16-byte overlap, finding the magic. Record the header for the census;
parse only the tables you need.

## Three bugs that each cost a game relaunch (fixed in diag-4)

- **Type-hash filter.** Real table hashes are full 32-bit and most are `> 0x10000000`
  (`0xBD4042C2` ProjectileSettings, `0x88E4DBB1` WeaponData, `0x45171B68` ProjectileWeapon).
  A sanity filter `type < 0x10000000` silently drops every table you care about and keeps
  only small string/enum tables. Only filter on `type ~= 0`.
- **Descriptor read offset.** The DLArray descriptor is at `magic+24`/`magic+32`, NOT at
  `HEADER_BYTES+12/+24/+32`. Reading 12 bytes late makes `(size-16)/count` garbage and the
  resolver returns nil (no records dumped). Read size at `magic+12` (1-based 13), ptr at
  `magic+24` (25), count at `magic+32` (33).
- **Hexdump freeze loop.** Hexdumping full payloads of the big tables (~70 MB of hex text,
  written synchronously in one frame) froze the game ~30 s; because the resolver had
  failed, the mod never reached `state.done` and re-dumped every ~10 s. Fix both: reach
  `done` after one pass, and dump tables > 256 KB as **raw binary** (`io.open(...,'wb')`),
  never hex text — binary is ~60 ms, hexdump is the freeze. Keep hexdump only for small
  tables you will eyeball.

The memory walk itself is spread across frames (`SCAN_BUDGET` ≈ 4 ms every other frame)
and does NOT freeze; only the dump does.

## Enemy data is NOT a standalone LDLD table

The enemy-weapon component `0xd25fc7f7` = `WeaponDataComponent` (and siblings `SpreadInfo`
0xf916ed4b, `SensorEyeComponent` 0xb4789330, `DamageInfo` 0x260cbe2b) are **component
types embedded inside enemy archetype records** — they do NOT appear as top-level LDLD
tables. An in-mission census found 326 table types and none was `0xd25fc7f7`. Enemy data
loads **only in-mission** (absent at the ship) as ~16 keyed hash tables (e.g. `0x6062C233`
15 MB entity table, `0x8D419C7A` 7 MB). So "dump the enemy-weapon component by LDLD
header scan" is wrong. To read enemy projectile references, locate the enemy archetype
keyed table and parse the component offsets inside it (or read enemyov's per-enemy patch
logic, `/tmp/enemyov/options_<faction>_<enemy>_*.lua`). The component type hashes remain
correct as *names* (reverse-dlsum), just not as top-level table keys.

## Enumerate references by exact offset, never by scanning type values

Finding which records are referenced by NOTHING cannot be done by scanning records for u32
values in the `ProjectileType` range (1–350): small-integer fields (counts, enum indices,
flags) collide with the range and produce mass false positives — ExplosionSettings alone
"references" all 350 types by accident. Enumerate from the known reference offsets instead
(ProjectileWeapon +0 default and +576 alternate, WeaponRounds +64 re-arm source, ExplosionSettings shrapnel +84,
enemy archetype component offsets), then set-difference against the record table. Fire modes do
NOT reference projectiles — they are single/burst/auto enums in the weapon's own
WeaponData record (0x88E4DBB1, +140/+144/+148/+152 — SKILL section 4).

## Current census facts (2026-10-06)

- 350 projectile records, ALL live: 350 distinct non-zero types, zero `type==0` slots, zero
  duplicates. No free record exists — a clone overwrites a referenced record, so the
  three-way proof is mandatory, not a nicety.
- 71 records carry `name==0` (enemy/special-effect signature — NOT "dormant").
- Enemy roster = 37 types (9 Terminid, 17 Automaton, 11 Illuminate).
- Reference census (weapon `+0`/`+576` + WeaponRounds `+64` + shrapnel `+84`): **172 types
  referenced**, leaving 178 unreferenced = 29 `name==0` (enemy-only) + **149 `name!=0`
  clone-candidate records**.

### diag-5 dumps the bucket array — join it offline, do not extend refscan again

`refscan_pwbuckets.txt` is one line per bucket: `entity_lo`, `entity_hi`, `slot`.
Join `slot` to `refscan_weapons.txt` (`projtype` at record +0) and that type to
`refscan_projectiles.txt` (name hash, speed, mass, drag, gravity, arming, damage
type). All-zero buckets are hash holes, not failed rows. A census that has
`refscan_weapons.txt` but no `refscan_pwbuckets.txt` is diag-4 or older; that
older file cannot recover entity→type. Do not re-patch refscan to add the dump.

Run the census with only refscan loaded. It is read-only, but another weapon-stat
mod leaves its edits in the fingerprint. Confirmed 2026-10-07 (Bingus: 1 loaded):
542 buckets, 271 live entities, 272 ProjectileWeapon records, 350 projectiles.
`refscan_enemy.txt` still does not appear in a mission — enemy weapon components
are not a top-level LDLD table (above). Do not wait on that file.

## The `name==0` rule is statistically confirmed, not just documented

Scanning the in-mission enemy tables (16 keyed hash tables) for every u32 in the
ProjectileType range shows `name==0` types appear **3.25× more often** than `name!=0`
types (normalized for their 71-vs-279 counts). That bias is the enemy projectile
reference: enemy attacks point at unnamed rounds, so a `name!=0` record is outside the
enemy reference set. A concrete clone target (type 206, the dead Eruptor near-duplicate)
appeared 231 times across the enemy tables — **7× below** the `name==0` referenced rate
(avg 1672) and consistent with false-positive small-int background, not a real reference.
This is the offline proof that closes the enemy leg without parsing the enemy archetype
component offsets (which remain unresolved — the enemy data is hash-keyed with a layout
the stride scan could not cleanly isolate). The statistical bias is the evidence; it is
not a single "clean offset" proof.
