---
name: hd2-mod-authoring
description: "Helldivers 2 mod, Arsenal install, Bingus lua patch, Wwise sound-bank swap, Nexus unlink, an HD2 Mod Manager install that dies on the manifest Name, translating on-screen text in a glyph-atlas HUD, drawing a live HUD overlay with the game font, a bundled .patch_0 whose type at 0x50 is not Lua, the whole HUD freezes after the stratagem list and death does not clear it, Bingus reports more than 200 local variables or more than 60 upvalues, the realistic log says 4 spare magazines while the gun still shows 6, the weapon search ends a round at 256 MB after ProjectileWeapon, the magazine write refuses because capacity reads 0, the log says explosion table not found, the log says explosion on impact 0 -> 388 while a close SAFE shot still detonates, black squares after the impact id moves onto a spare explosion slot, the Dominator thumbnail still lists only the 380 m/s specs, a pytest check of the magazine index or explosion tail without launching the game, or statically vetting a downloaded HD2 mod manager/tool for malware before running it: classify the install, conflict-check writers of the same value, then edit, pack, and verify from the game log."
homepage: "https://github.com/Cavadus/hd2-mod-authoring"
---

# HD2 mod authoring

## ⚠️ Safety boundary — read this first

Every technique in this skill reads and rewrites another process's memory at
runtime — the game's own. That is invasive, high-risk work. Hard rules:

- **Your own game process only.** One machine you own, one copy of Helldivers 2
  you launched, for modding your own game. Never patch another person's process,
  a system process, or any process you did not start yourself.
- **It will crash and can corrupt.** A wrong offset or a loose value match
  corrupts game state (black screen, silent close) or the whole process. Develop
  against a disposable loadout; back up first.
- **Read before write, roll back on mismatch.** Locate, verify against vanilla
  values, write, then read back — in that order, every time. No write to an
  address you have not first read and identified.
- **Not a cheat or malware toolkit.** Memory scanning, hooking and value patching
  are the same primitives cheats and malware use. They are legitimate only here:
  modding a game you own. Do not reuse them on other software or people, and do
  not ship a mod that reads or writes another player's process or data.

Work from a mod source directory (e.g. `~/hd2-mods/<mod>/`). The live install is `~/.config/hd2arsenal/mods`. Offsets and the 2026-10-01 overlap list are in `references/install-and-format.md`. Re-read that file at the step that cites it. Re-check any layout a game update could move.

## 1. Classify the install before editing

List `~/.config/hd2arsenal/mods`. For each `.patch_0`, find the payload. A Lua patch starts at byte 200. A Wwise bank's `BKHD` is later (the Dixie bank starts at 320). Search for `BKHD` before treating byte 200 as the payload.

- Lua runtime patch: the bytes at 200 contain `HD2-Addon:` or a Lua `function`, and the type at `0x50` is the Lua type in the reference. These need Bingus Shared Loader.
- Binary resource patch: no `HD2-Addon:` and no Lua `function`, or the file contains `BKHD`. `.gpu_resources` and `.stream` sidecars belong to archive patches. Copy those bytes. Do not pack them as Lua.
- The same `HD2-Addon:` id in two mod folders means both versions are installed. Different ids still stack when they write the same field.
- A language patch is a Lua patch that edits nothing. Recognize it before treating it as a stat editor: addon id ends `_zh_cn` (or the manifest `Name` carries `简体中文`), the `Description` says it loads after the original ("需要在原版之后加载"), and the body only hooks `stingray.Gui.text` / `text_extents` (draw/measure) with zero `WriteProcessMemory` / `ReadProcessMemory`. It cannot fight a value writer — the real editor is a different addon (`mods/shodan/stat_editor`).

Done when the reply names the patch kind and any duplicate addon id.

## 2. Refuse a second writer of the same value

Read the overlap list in `references/install-and-format.md`, then re-scan. A folder under `mods/` is only the library. What loads is `hd2a_data.json` → `modsList[<selectedProfile>].mods` with `enabled: true`, and which suboption is on. The Patriot and Lumberer ammo pairs were library-only; they were not in the profile. Exosuit Rebalance (`mods/recon/exosuit_ammo`) is the writer for those magazines and for armor (+1); the standalone `exo45_armor` was folded into it. Do not put the ammo mods or the standalone armor mod back — armor would double-apply. Bingus does not dedupe different addon ids.

Name the installed mod that already writes the field. Stop unless the operator asked to replace it. To remove one, move the folder to a `_retired/` area outside the live mods tree and delete that uuid from both `modsLibrary` and the profile. Copy `hd2a_data.json` aside first. It is indent-2 JSON.

Done when the reply names the overlap, or says there is none.

## 3. Edit the source tree, then make the text agree

The mods this playbook was built from are listed here as worked examples — the addon ids and layouts are real, but read the live folder from `hd2a_data.json` each time rather than trusting these paths:

- `hd2-mods/dominator-rechambered/` — addon `mods/dsh/dominator_bolt_pistol`, source `jar5_dominator_rechambered.lua`.
- `hd2-mods/exosuit-ammo/` — addon `mods/recon/exosuit_ammo`, source `exosuit_ammo.lua`. Kept local (not distributed with this skill).
- `hd2-mods/m1000/` — addon `mods/recon/m1000`, source `m1000.lua`. Arsenal folder `m1000_combined`. Gameplay is one scan. Sights and sounds stay the original archive patches.
- `hd2-mods/realistic-weapons/` — one scanner, addon `mods/recon/realistic_weapons`. The weapon checkboxes are flags, not scanners. Ids are in the reference.
- `hd2-mods/dixie-horn/` — Wwise bank, not Lua. No `REVISION`. The bank procedure is in the reference.
- `hd2-mods/mech-part-hud/` — read-only glyph-atlas HUD, addon `mods/recon/mech_part_hud`. Not a writer of health or ammo. A spatial arm link stays; do not wipe it every poll. The label procedure is below; the fit and the walk are in the reference.

### Translating on-screen text

Decode as UTF-8 before counting CJK. A UTF-16LE decode of ASCII reports Chinese in every Lua file. That scan was wrong.

Grep the draw function for strings it passes to the glyph renderer. A `zh` field or label table that nothing reads is not on screen.

If those glyphs are pre-rasterized rects, the generator charset is the only letters that draw. Regenerate the font section for the new strings. The silhouette bytes before `["fonts"]` must stay identical. Measure the label against the panel first. The Mech Part HUD fit, and the fact that its `tools/build.py` imports `lupa` (not installed), are in `references/install-and-format.md`. Pack with that mod's `archive_writer.py` and check the assembly with `/tmp/luavenv/bin/luaparser`.

Replacing the `.patch_0` leaves `README.md` and `Source/` that Arsenal unpacked beside it. Overwrite those from the new package. A copyright name inside a bundled license is not a label.

Done when the installed patch and the installed README have no CJK in a UTF-8 decode, luaparser exits 0, and the silhouette prefix matches. `deployed: false` means the panel has not been seen in game.

Drawing a live overlay with the game font (not the glyph atlas) and reading game-object state are in `references/hud-overlay.md`: the `Gui.text` recipe, the `sr.Vector2` callable-table and `App.worlds` pitfalls, and the `game_object_field` unknown-name hang.

Before another behavior edit, read the game log named in the source. Its revision line must already match the build you believe is loaded. A previous revision means Arsenal moved the folder or the game did not restart.

Copy the current Lua to a backup before editing, and keep old versioned sources and superseded zips in an `archive/` subfolder inside that mod folder (not the mod root or a shared top-level pile). Name the backup `.v<old-revision>.lua.bak`. Change `REVISION` only when that behavior is the one being shipped. A rejected experiment keeps the last shipped `REVISION` and puts a distinct token in the log line the source already prints, so the log proves which build ran. Do not mint the next release number per test. Current Dominator release numbers are in `references/install-and-format.md`. A ricochet experiment does not get the next number. A close SAFE shot is a dud when impact stays on explosion 388 and the profile arming write is in the payload (v3.4.7, confirmed in mission). v3.4.8 pointed that impact at spare slot 216 and the operator saw black squares; the 152-byte row already matched 388 except the id and the radius floats. The graphic is the tail hash in section 9, not a reason to leave the impact on 388 forever. The line `explosion on impact 0 -> 388` is the pistol row, not the id written onto SAFE (section 7). Make `manifest.json` describe the shipped behavior, not the experiment. If the opening comment disagrees with `REVISION` and the manifest, fix the comment in the same edit. The Dominator comment has claimed "original range" after the range cap changed. Trust `REVISION` and the manifest.

An alternate behavior of a mod that is already shipped stays on that mod. Same Guid, same addon id. Pack each behavior as a pick-one suboption (section 6): same addon id, the profile stamp is the only difference, and the behavior the last release already had is the default suboption. A second folder with a new Guid and a v1.x number is a second writer of the same projectile. Disable it. v3.4.0 replaced v3.3.5 this way; Regular is the v3.3.5 gun. The Arsenal `Name`, the manifest `Name`, and the folder stay `v3.4.0` so the path does not move. Do not mint a public version label for a fix that has not been confirmed in a mission. The Lua `REVISION` is only the string the log prints, so a behavior change still bumps it; a rejected experiment does not. Current numbers are in `references/install-and-format.md`.

Done when the backup exists and `REVISION`, the manifest, and the opening comment match.

## 4. Patch memory the way the failed builds taught

**High-risk: live process-memory patching.** See the safety boundary at the top of this file before writing anything.

Guard the file with `rawget` / `rawset` on one global so it loads once.

Never scan process memory in one frame. One scan, then set `state.done`. `maintain` is one read-back of the cached address, not another scan. A full rescan every few seconds is what put the Dominator on Mod Lag Watchdog.

A second table that only one profile needs stays in the scan predicate after the first table is found. `if not table_info then scan else apply` drops the Realistic explosion search the moment the projectile table is found. That predicate is already shipped, and it is not sufficient. ExplosionSettings (`0x2AEA2592`, stride 152) is inline rows: a 16-byte header, the count u32 at payload +8, and the records at payload +16 (`references/mods-catalog.md`). SHODAN v2.5 marks that type `tail = true` and parses it with `parse_rows`, not `parse_keyed`. `validate_block` only accepts a pointer descriptor whose `(size - 16)` divides into an exact stride, so a tail, or rows that are not behind that pointer, never becomes `explosion_info`. The log then stays `explosion table not found; pistol blast left in place` on every drop. Accept the block when version is 1, the u32 at payload +8 is inside the record-count range, and the payload size is at least `16 + count * 152`. Probe those inline rows. Do not require an exact division and do not follow the descriptor pointer. Do not shrink explosion 388 in place. A spare settings row does not carry the pistol effect until its tail hash is copied (section 9). Accepting the block is not the clone. v3.4.3 logged count 422 and tail 3640 only after the warhead copy, and the pistol blast stayed. v3.4.4 sets `state.applied = false` in `blast_maintain` and reclones. The mission log is `explosion table found`, then `blast: clone 216: inner 1 m / outer 2 m (pistol was 1.0 / 3.5 / 5 / 6)`. Slot 216 is legal only when its damage type is 285, its radii are 0.1 / 0.2 / 1 / 2, and no projectile points at it. That same life spawned the Realistic gun at 4/4 with the wheel. That clone log is already confirmed. Do not repack only to see `blast: clone 216` again. v3.4.5 wrote slot 216 onto SAFE impact and expiry, and a close SAFE shot still detonated. v3.4.7 left SAFE on 388 (impact 388, expiry 0, arming 15) and the operator confirmed a close SAFE shot is a dud. v3.4.8 set SAFE impact to 216 and left expiry at 0; the operator then saw black squares. A live diff of row 216 against 388 differed only at +0 and the floats +20, +24, and +32. The u64 at +56 matched, and +40 on both rows still pointed at row 92's tail slot. The per-row effect hash is section 9. Copying the 152-byte settings row does not write it. v3.4.10 copies that hash, leaves expiry at 0, and points both modes' impact at 216. That play confirmed it: the log has `blast: effect hash copied from row 92 onto row 205`, `SAFE round written: impact 216, expiry 0, arming 15.00 m`, `spare magazines 6 -> 4`, the wheel, and full auto, and the operator said the session nailed it. Round 1 of that same log still stopped at 1792 MB; round 2 found the weapon tables at 394 MB. A revision packed while that client was already running is not that log.

Spare magazines are not that optional table. Recoil, the projectile-weapon record, and the trait row end the weapon walk only for a profile that leaves spares at 6. Realistic owes a 6→4 write, and the magazine table is later on the same walk. Stopping at those three leaves the gun on stock 6 while the log banner already says `spares=4` (2026-10-12: realistic loaded, ballistics applied, recoil search still on round 1, no magazine line). Requiring `mag.record` with no byte cap never ends the round: a 4 ms step then walks the rest of memory for the session, and `WSCAN_MAX_ROUNDS` does not help. After the three are in hand, keep walking only while this profile still owes the spare write, only for a capped tail. The 2026-10-12 pack caps the tail at 768 MB and uses 4 ms steps only during that tail; 768 MB was not measured as the distance to the table. The write is the two spare u32s at +16 and +20 on WeaponMagazineComponentData (`0xFB8D88A3`, stride 160), and only while +8 is still 15 and both are still 6. Leave +8 at 15. Do not touch the unknown u32 4 at +12. Those are not the exosuit capacity fields at +136. Four spares plus the 15 in the gun is 75 rounds, not 60. The Dominator row is the words `0, 0, 15, 4, 6, 6`. `locate_keyed` (count == 2 * live, and the remainder divisible by the stride) is the wrong end of this index: on the live 52000-byte block it matched 8 rows (128 bytes) early, +8 read 0, and the write refused. That early boundary is the 8640-byte split in the reference, and the bytes there are zeros. Walk index rows until `pad ~= 0` or `slot > 100000`, then use `count * 16 + slot * stride`. That offset was the real row (slot 220). Use it for this magazine table only. WeaponData stays on `locate_keyed`; SAFE, UNSAFE, and full-auto on the wheel are that record. Do not retarget it, and do not treat a capacity of 0 as a wrong weapon. A refused write is final only when that row really starts `0, 0, 15, 4` and the two spare fields are not both 6. A read of the already-running game's own `/proc/<pid>/mem`, after boot, is how the row was checked. Do not put that walk in the mod, and do not start any memory walk during the boot window in section 9. Done when the log shows the shipped `REVISION` and `spare magazines 6 -> 4`. That line was confirmed on v3.4.2. The gun already in hand keeps the count it spawned with: a fresh client is 6/6 until the search lands, then the counter can read 6/4, and only a weapon swap or death builds one at 4/4. SAFE, UNSAFE, and full-auto show on that new gun. A 6/4 HUD after the log line is not a missed write. A death does nothing when that line was never logged and the search already stopped (section 9).

Layout math that does not need the game is `hd2-mods/dominator-rechambered/tests/test_layout.py`. Run `python3 -m pytest` on that file. It locks the two shapes that already shipped wrong: `locate_keyed` stopping 128 bytes early on this magazine index, and an ExplosionSettings payload whose tail is not an exact stride. A pass does not prove a HUD count, a blast radius, or that Bingus loaded the chunk. Do not add a test that reads the process. A request to delete unused locals or retune the scan on a build that already loads is not a behavior change: that tidy is what crosses the 200-local cap in section 9. Leave the chunk alone unless a log line is wrong.

The same discipline applies to locating a record inside an already-found table on a
hot path. Cache the record's address keyed on the table's identity (the records
pointer or block address), and re-validate with one field read (e.g. the type u32 at
+0); only re-walk the table when that identity changed (map reload). The Dominator
wheel's `ammo_apply` runs ~10×/sec and used to re-walk all ~350 projectile records
every call to re-find the alternate round it had already located — caching the
address (keyed on the table's records pointer) and re-validating with one type read
cut it to a single 4-byte read per call. Cue: a per-cycle `for i = 0, count-1`
searching a table you already located.

Anchor only on vanilla values. Never match a record by the value this mod writes. Compare before write, read the bytes back, and restore page protection.

Re-verify offsets after a game update. The layouts checked against the game data, and how to find a component type for a field you have not patched before, are in `references/install-and-format.md`.

- Emancipator autocannon is the exosuit branch that must not require `magazines_max == 0`. The other four weapons do. Requiring max 0 for all of them drops the autocannon.
- Patriot missiles are two identical capacity-14 records. `MISSILE_PICK` writes one. If the Patriot still shows 14, flip it.
- Fire modes live in the weapon's OWN WeaponData record (`0x88E4DBB1`, stride 1232 — the same record that holds recoil and `function_info`): `num_burst` @ +140 (=3), `primary` @ +144 (=Single 2), `secondary` @ +148 (=None 0), `tertiary` @ +152 (=None 0). FireMode enum: None=0/Automatic=1/Single=2/Burst=3. The fire-mode enum is READ LIVE — writing `secondary=Burst(3)` + `tertiary=Automatic(1)` adds Single/Burst/Automatic to the selector. Only `fire_ability` (+940, Dominator 2660 = phoenix) is cached at weapon construction. The cyclic rate is NOT live per shot, but it is NOT permanently baked either: `rounds_per_minute` is three f32 slots in the weapon's OWN ProjectileWeapon record at +4 (X) / +8 (Y) / +12 (Z), Y = the default (`weapon.fire_rate`). It is `instantiationOnly` — the game copies the slots into the weapon when it BUILDS it, so a write applies to weapons built AFTER it (redeploy, reinforce, re-equip), not to one already in hand. HD2Runtime live-proved this (MG-206 `fire_rate.modes` alone; AR-23 Liberator `fire_rate.modes` + `weapon_function.left = rate_of_fire`). TCO 2.6.13 proved the same spawn-copy for reload (`WeaponReloadComponentData` `0x991D454E`, duration at +56) and that WeaponData ergonomics at +356 is not live handling: the table write and the live copies changed the stored number and not the weapon already in hand. Do not hunt live copies of +356. To add a selector, fill X and/or Z AND bind an unbound input to `rate_of_fire` (2) in one transaction; selector order Y→Z→X, menu order X,Y,Z. `function_info` (+184 left / +188 right) is the SELECTOR-BINDING enum (which input toggles fire mode), not the mode itself — that is why a write to +184/+188 does not change the modes. **Do not locate the modes by another mod's value fingerprint.** The JAR-5 Buff Pack (joelc) matched `[3,2,3]` (num_burst=3, primary=single=2, secondary=BURST=3) in a ~144-byte record, but that is the Buff Pack's POST-EDIT state — the stock Dominator is `[3,2,0,0]` (secondary=None), so the fingerprint never matches the stock record and the write lands nowhere. This cost three builds (v3.3/3.3.1/3.3.2) before re-reading our own dbp-3.x diagnostic dumps (which had already pinned +140/+144/+148/+152) fixed it in v3.3.3. A value fingerprint from a third-party mod reflects that mod's edited state, not stock — verify it against a stock read before trusting it. The same pack patches reload via a passive stat array (type 0x63CE0FEB, stat id 13 → f32 1.36, repointing every armor passive block and skipping ordinal 0), not a weapon field. The mod writes a float at projectile +160 and logs it as arming distance. SHODAN's projectile rows and HD2 Runtime's attack-output slots do not name that member. Runtime's proven explosion links are +144 impact and +156 expiry. The unproven floats beside the impact id are +148 and +152, and Runtime says no row has a proven delayed-explosion member. A log line `arming distance 0.10 -> 15.0 m` only means the payload contained 15. That write plus impact 388 and expiry 0 is the confirmed close-range dud (v3.4.7). v3.4.5 wrote 216 onto impact and expiry and a close shot still detonated. v3.4.10 wrote impact 216, expiry 0, the tail hash, and arming 15, and that is the confirmed gun (section 9). Do not move impact back to 388 because an older 216 write failed. The wheel's alternate is section 11 (the type-206 clone). The Dominator's own row is the SAFE round.
- A projectile-field patch does not change the armory's AP or Explosive label. The
  label is a **presentation** field, not native code: it is writable through
  HD2Runtime `hd2.fields.presentation.armor_penetration` / `presentation.traits`,
  backed by `LoadoutEntryComponentData` +12 (section 10). Flagged
  `allow_unverified_effect`, and menus build their labels when they open. **The
  reverse also holds:** a `presentation.traits` write that puts **ANTI-TANK** under
  WEAPONS TRAITS only relabels the card — it is a localization string id in those +12
  slots, and no gameplay reader reads them, so it never changes damage or
  penetration. Real anti-tank is a separate `damage.ap_*` edit on the projectile (or
  explosion) DamageInfo. A streamer showing a laser rifle "made anti-tank" may have
  only relabeled it; confirm the `ap_*` write before believing the trait tag.
- **Impact sound is not a projectile-record field either.** It resolves through
  `surface_impact_type` (+168) / `ricochet_impact_type` (+172) — `SurfaceImpactType`
  enum values — into a separate `PhysicsImpactEffectComponentData` lookup whose
  `PhysicsImpactEffectInfo` carries `audio_effect_id`, `camera_effect_id`,
  `shake_effect_id`, `decal_sheet`, `quake_effect`. A warhead swap (damage type +
  explosion) therefore leaves the surface-impact SOUND unchanged: the Dominator
  and the P/40-K already share `surface_impact_type` 4, so they thud identically.
  The audible change from a rechamber is the explosion the record now points at
  (`explosion_on_impact` 0→388), not the impact thud. If a round sounds wrong,
  check that explosion, not an impact-sound field that does not exist on the
  projectile record. Tightening that explosion's radius is not a write to outer
  +20. Inner +16 and outer +20 are real. HD2 Runtime names +24 `shockwave_radius`
  (5.0 on explosion 388). +32 is not in that layout (6.0 on the same row). The live values, and the stale type ids that used to label them,
  are in `references/mods-catalog.md`. Do not edit the shared explosion record.
  A spare ExplosionSettings row does not carry the effect by itself. The
  graphic is the tail hash in section 9. Leaving the impact id on 388 avoids
  the squares and also keeps the pistol radii. Field names for unknown offsets
  are discovered the same way as type names (filediver json tags, see the reference).
- Two Lua files that share one scanner and differ only by `move_done` / `dmg_done` are one scan, not two. Read those flags before copying a function. The free-movement file's `patch_damage` also writes damage to 90, and `dmg_done` starts true so that writer never runs. The AP4 file writes `4/4/4/0` only. The combined mod uses the AP-only writer with both flags false.
- Do not write Dominator `max_ricochets` or the angle fields at offsets 136 and 180 to stop a tree or rock bounce. Those writes were logged in game and reverted. The measured results are in `references/install-and-format.md`.

Done when `/tmp/luavenv/bin/luaparser` exits 0 on the source file. There is no system `lua` or `node`.

## 5. Copy binary patches verbatim

The Lumberer Cremator flame is `0a4bd8a1833f11b2.patch_0` and `1577e917ad1f287d.patch_0`. They are byte-identical. Copy them. Do not rename, re-hash, or run them through the Lua packer. Keep the empty `.gpu_resources` and `.stream` sidecars beside them.

Done when `cmp` against the previous bytes reports nothing.

A firing-sound bank is a full-bank replacement of one weapon's audio bank, and its HIRC event ids are **per-weapon** — so you can never give weapon A weapon B's report by swapping in B's bank wholesale. Verified 2026-10-05: the Dominator's firing bank `content/audio/wep_jar5_dominator` has 249 WEMs and 16 event ids; the shipped "Space Marine II" bolter bank has the SAME 16 event ids and SAME 249 WEM ids (only the WEM audio differs), which is why a full-bank swap works there. A different weapon's bank (e.g. the broomhandle sidearm, 193 WEMs, 14 event ids) shares ZERO event ids with the Dominator — the game posts the Dominator's event ids, and a foreign bank does not contain them. To add weapon B's firing report to weapon A, splice B's "fire" WEM into A's bank and keep A's HIRC/event ids; this splice is not only for the staleness case below.

A full-bank swap also goes stale when the game adds events. Before shipping another copy of an old `.bnk`, extract the current bank and diff HIRC type-4 event ids. If vanilla has an event the patch lacks, splice only the replaced WEM into the current bank and keep vanilla HIRC. List banks with filediver before scanning `data/bundles.*`. The FRV result, the Dixie container fields, and the raw-bank extraction flags are in `references/install-and-format.md`. Done when every vanilla event id is still in the patched bank and only the intended WEM size changed.

A firing-sound swap never touches gain. The mod replaces the whole bank byte-for-byte, so any loudness or timing difference between shots — "the first shot is much louder" is the recurring report — is authored inside the bank, not a mod bug. Gun banks use the standard Wwise **first-shot attack + quieter tail** design: the first round of a burst is the full report and rapid follow-ups play a lower-gain tail loop, so the first-shot/tail gap is a per-bank authoring choice. Diagnose the bank, don't blame the Lua. A `.patch_0` bank is `BKHD` (header) + `DIDX` (WEM id/offset/size index) + `DATA` (the WEM audio) + `HIRC` (event and gain graph); compare the banks' `HIRC` vs `DATA` vs `DIDX` hashes to tell whether they differ in structure or only in samples — 249 WEMs / 16 events is the Dominator's shape. The WEMs are Wwise Vorbis, which ffprobe/ffmpeg cannot decode (`codec_name=unknown`); measuring dB needs vgmstream. To quiet a hot bank, splice a quieter pre-encoded donor WEM; when no quieter donor WEM exists (SM2's fire report is a layered composite, no clean source), the container-rebuild procedure, the WEM `hash`-chunk caveat, and the PCM re-encode fallback are in `references/install-and-format.md`.

## 6. Pack and replace the Arsenal copy

Container offsets are in `references/install-and-format.md`. On a single-payload patch (u32 at byte 4 equals 1), the type at `0x50` says whether the payload is Lua. A bundle (u32 at byte 4 equals 4) is a type table; classify it in section 13 before editing, and do not resize it. The filename `9ba626afa44a3aa3.patch_0` is a shared slot name, not a per-mod id.

The packer script is not in the mod folder. Reuse the script that wrote the current `Addon/*.patch_0`. If it is gone, rebuild the header from the three structs in `references/install-and-format.md`; the `length` field is `192 + len(payload)`, not rounded to 16. Before editing, write the packer and run it on the UNMODIFIED source first — it must reproduce the current `Addon/*.patch_0` byte-for-byte (`cmp` clean) — and only then edit and repack. That proves the header is right before your edits are in the way. Then check `len(patch) == 200 + len(lua)` and `patch[200:]` equals the source bytes. Offset `0x68` is MurmurHash64A of the addon-id string, seed 0. That matched `mods/maxigun/ap4_public` and `mods/dsh/dominator_bolt_pistol`. Offset `0xA0` is the Lua size plus 8. Leaving the old hash on a new addon id ships a header that names the wrong mod.

A single-option Lua mod is `manifest.json`, `thumbnail.png`, and `Addon/`. A multi-option mod uses named Include folders. Top-level options can all be on. Suboptions are pick-one. Put the suboption that is enabled now first, so a reimport does not flip it. A bank that is the whole mod has no Options key: `manifest.json`, `thumbnail.png`, and the `.patch_0` at the archive root. That is how SEAF-Chan is installed. Do not move that patch into `Addon/`.

**Nested pick-one suboptions (Hotshot Customisation is the reference).** For a top-level option that is a checkbox whose expansion offers a pick-one choice, the top-level option declares `Include: ["Parent"]` AND `SubOptions`, where each suboption declares `Include: ["Parent/Child"]` — the child is a subfolder inside the parent folder. The parent folder is only a container (holds the subfolders, no patch of its own); each child subfolder holds its own `.patch_0`. In `hd2a_data.json` the selected suboption carries `enabled: true` and the rest `false` (one per group). This is the pattern for mutually-exclusive binary swaps — e.g. four firing-sound banks under one "Firing sound" option — where each is a full-bank replace of the same slot, so only one may be active.

A firing-sound bank is not part of the Lua Include, even when the filename is `9ba626afa44a3aa3.patch_0`. Classify it by the type at `0x50` and by whether byte 200 is Lua. The Dominator sound's type and folder are in `references/install-and-format.md`. Copy those bytes. Give it its own top-level option so it can be off while the gameplay option stays on. The manifest has no enabled field. On a mod that is already installed, set that option `enabled: true` in both `modsLibrary` and the selected profile. Copy `hd2a_data.json` aside first. Set the profile entry `enabled: true`, `deployed: false`, `changed: true` until Arsenal deploys.

Read that mod's `path` from `hd2a_data.json` immediately before the copy. Arsenal changes the `_AR` suffix; the suffix in the reference is not the live folder. Copying into the remembered path leaves the loaded copy on the old build. Replace that folder. Do not leave the old extract next to the new one.

Rebuild the zip beside the source directory in the same edit. That zip is what gets imported. From inside the source directory, `zip -X` the files so the archive root is `manifest.json`, `thumbnail.png`, and either the Include folders or the root `.patch_0`. No parent-directory entry. Check the namelist.

A zip with no `manifest.json` imports as a second mod. The label is the filename, the description is empty, and the uuid is new. Name, description, and Nexus identity are not in the patch. They are on both `modsLibrary` and `modsList[<selectedProfile>].mods` in `hd2a_data.json`. `manifest.json` needs `Version`, `Guid`, `Name`, `Description`, and `IconPath`. Use the installed uuid as `Guid` when the zip is that mod. Do not import it again to refresh the label.

HD2 Mod Manager (the Nexus one, teutinsa) stores the mod at `Mods\{manifest.Name}` and looks for `manifest.json` at the archive root. `Name` must be a legal Windows folder: no `<>:"/\|?*`. A colon fails the copy. `JAR-5 Dominator: Rechambered` is `JAR-5 Dominator - Rechambered`. Do not wrap the zip in a folder of that name. That hides `manifest.json` and the manager reports no manifest. An option `Name` is a label. The path is its `Include`. A name-only change does not bump `REVISION` and does not require a redeploy. **Arsenal `Directories → Mods Storage Folder` pointed at a stale/transient path breaks import.** A Windows user who migrated from HD2 Mod Manager left Arsenal's Mods Storage Folder pointing at the old `Temp\Helldivers2ModManager\…` path; Arsenal extracted there and import failed with `The include path "Space Marine II" is invalid!` — the `Temp\Helldivers2ModManager\…` prefix in the error is the tell. This is a misconfigured storage path, NOT a manifest/`Include` bug: Arsenal handles spaces in `Include` paths fine when the storage is a stable, non-Temp folder. Fix: repoint Mods Storage Folder to a stable location (not a Windows `Temp` path). **Cross-manager compatibility: the V1 `manifest.json` is a shared standard.** Arsenal (rsnl-gg), DDMM (`katsyk/DemocracyDefenderModManager`), and teutinsa's HD2 Mod Manager all read the same V1 format — `Version: 1`, `Guid`, `Name`, `Description`, `IconPath`, and `Options[]` of `{Name, Description, Include, Image, SubOptions[]}` (a SubOption's `Include` is required). A manifest that parses in Arsenal also parses in DDMM and HD2MM; the only shared constraint is `Name` as a legal Windows folder (the colon rule above), because HD2MM stores the mod at `Mods\{manifest.Name}`. Spaces in `Include` paths are legal everywhere — do not rename option folders to avoid spaces, it is unnecessary. Echelon is closed-source Delphi/VCL (its `Mod Builder` generates manifests); its format is unverified but it is the same ecosystem, so the V1 manifest is the safe default.

Nexus identity is `nexusData`: `modId`, `fileId`, `version`, `updateTimestamp`. A local mod stores `null`. To disassociate, copy `hd2a_data.json` aside and set `nexusData` to `null` on both records. The mod id in the folder name is the original download name, not the link. Both Dixie records stayed `null` on a re-read while `hd2arsenal` was still running. If the Nexus badge remains, the operator quits Arsenal and opens it again.

The operator still quits Arsenal, opens it again, and deploys before a game test. `deployed: false` is not a deployed mod.

Editing `~/.config/hd2arsenal/mods/<folder>/` does not change what the game loads. Deploy copies each enabled patch into `Helldivers 2/data/` as `9ba626afa44a3aa3.patch_<N>` (plus `.gpu_resources` / `.stream` siblings). `N` is assigned at deploy time and is not stable; `patch_0` is only the first slot, not the Lua file. `~/.config/hd2arsenal/deployment_snapshot.json` `deployedFiles` lists `{name, size, modified}` for the last deploy. Match the mod's patch by size, then by a unique string. On the 2026-10-07 23:45 deploy, HD2 HUD Plus 0.2.2 (721977 bytes) was `patch_95`; `data/9ba626afa44a3aa3.patch_0` was 15672 bytes and a different file. `hd2a_data.json` `enabled: true, deployed: true, changed: false` does not prove the data file matches the mods folder — compare bytes. After an edit, copy the same bytes onto that `patch_N`, or have the operator redeploy. Bingus reads the data file once, at process start. Before saying a restart is enough, confirm the new marker is in the data file, not only in the mods folder. Toggling the mod, or an option under it, while the game is open does not reload it. `contentHash` on both the library record and the profile record is the sha256 of that mod's patch-asset bytes sorted as raw buffers (`.patch_0`, `.gpu_resources`, and `.stream` for HUD Plus matched the stored hash). Recompute it after the edit and write it on both records. Set the matching `deployedFiles` entry's `modified` to the data file's mtime in milliseconds. Leave `changed: false` and `deployed: true` only when those data-file bytes already match. Do not Nexus-update over a local patch of that bundle; a re-download replaces the edit. 0.2.2 (721977 bytes, `patch_95`) was current on 2026-10-07. A later library record named HUD Plus 0.2.4, so match the live file before reapplying that edit.

An option can be checked while the mod record's own `enabled` is false. The option does nothing then. Read the mod record, not only its options. `hd2a_data.json` can show every mod `enabled: false` while the option boxes are still ticked.

A Dominator thumbnail change follows `references/thumbnail.md`. The shipped card already has the rifle and the bottom title. Regular and Realistic are two spec cards in the top band, not a 380 m/s-only panel. Archive the png, then paint that band. Rebuild from `archive/dominator_render.png` only when the hero art itself is wrong. `branding/dominator_base_thumbnail.jpg` is not a source. Do not regenerate the card as a side effect of a Lua edit.

Done when the mods-folder payload equals the source, the matching `data/9ba626afa44a3aa3.patch_N` equals that same payload, and both records' `contentHash` is the sha256 of the sorted patch-asset bytes. A bank is done when the installed bank `cmp`s against the packed bank, each binary Include file `cmp`s clean, and the zip namelist matches those files. A Lua mod's packed `REVISION` is the shipped string.

## 7. Verify from the game log

Read the log path in the current source before looking for a file. Exosuit writes `$LOCALAPPDATA/CowboyBingus/Helldivers2/Logs/ExosuitAmmo.log`. Under Proton that prefix is `~/.steam/steam/steamapps/compatdata/553850` (this host also has it at `~/.local/share/Steam/steamapps/compatdata/553850`).

**The whole HUD freezes, CTRL opens nothing, and dying does not clear it.** That is HD2 HUD Plus halting, not a hung game thread. Read `AppData/Roaming/hd2_hud_status.txt` under that Proton prefix. `widgets stopped: update` means a widget `pcall` threw, `run()` latched `self.failed = "update"`, and the updater stopped for the rest of the process. The 3D stratagem list (`hud.stratagem3d`) calls `stratagem_list_input` and `stratagem_list_tick` on a cloned panel while the stratagem ball is held and the input mode is non-zero, and an edit sets the real stratagem group (`stratagem.group_shown`) opacity to 0. Those writes stay after death. Only a full game restart reloads the patch. The 0.2.2 note that a controller freeze in the menu is fixed is a different bug. That skip string belongs to the 0.2.2 bundle. If the live file is a different size or version (Arsenal later listed 0.2.4), re-read its `run()` and do not paste the 0.2.2 edit into it. Patch the bundle only as section 13 allows. The same-length edit, padded with spaces: in `run()`, a failed `pcall` records `failed_detail` and returns success, and does not assign `self.failed` (that assignment is what makes the status line `update` and stops every screen). Skip `invoke` and the row `carry` when `string.sub(call, 1, 15) == "stratagem_list_"` (`stratagem_list_input` and `stratagem_list_tick` only). Skip the edit whose `id` is `vanilla` (that is the opacity-0 write). A failed `widgets:put` clears `widgets.failed` and uses an empty `changed` table instead of `return fail`. Do not point an arg at a source name that is not in `GameBaked`; the reader plan returns `"source"` and the mod never starts. `string` is already allowed in that module. Do not soften `make()` the same way; its failure reason is not `"update"`. Done for this edit when the mods-folder patch and the data `patch_N` are the same size as before and both contain `local skip=string.sub(held.update.call,1,15)=="stratagem_list_"` and `edit.id~="vanilla"`. A mission after a full restart is still the check that CTRL no longer sticks.

Mod Lag Watchdog is installed (`mods/patpatpatrick/mod_lag_finder`). Absence from its cost list means the mod is under the display threshold. A stale name is the watchdog reading an empty Proton `hd2a_data.json`. Arsenal's list is `~/.config/hd2arsenal/hd2a_data.json`. A steady ms/s line **labelled `modname (+ all below it)`** is an attribution bug, not the mod's cost. The watchdog follows the update chain through direct upvalues (`previous_update`, `original_update`); a hook that stashes the previous update in a table field and calls it through a closure (`BUS.base = update; pcall(BUS.base, ...)`) cannot be followed, so the watchdog bills "the mod + everything below it" — the game's own ~0.7 ms/frame update loop — to the mod. Realistic Weapons did this with a shared `OCLAW_UPDATE_BUS` dispatcher and showed a steady ~58 ms/s that never matched its own idle log; the hitch lines proved it (`realistic_weapons (+ all below it) 0`, the 57 ms "not explained (outside update)"). Fix: replace the dispatcher with a direct upvalue hook — `local original_update = update; update = function(...) pcall(tick) return original_update(...) end` — which both lets the watchdog follow the chain and removes the `pcall(base, ...)` JIT barrier on the game's hot path. Check whether the shared bus has other users first (grep the install dir for its global name). A per-frame `os.time()` / `os.date()` call in `tick()` is a real but SMALL steady cost (microseconds, ~3 ms/s, not tens) — convert it to frame counts (`state.frame + 300/600` ≈ 5/10 s) after fixing the hook. `os.clock()` inside a search-phase budget loop is fine — that loop does not run in steady state. Realistic Weapons' hook is `mods/recon/realistic_weapons`. A line that still says `realistic_mg206` is the checkbox id from before the hook moved.

The game does not load Lua from the Arsenal mods folder. Both Lua and binary patches land in `Helldivers 2/data/` under indexed names (`9ba626afa44a3aa3.patch_95` was the 721977-byte HUD Plus bundle; `patch_118` is a different binary). Find the slot as section 6 says: size in `deployment_snapshot.json`, then a unique string. `data/9ba626afa44a3aa3.patch_0` is not that bundle.

A firing-sound option is a different patch from the Lua. "Only the sound works" on both Regular and Realistic, or stock magazines with no wheel and no full-auto, means the shared script did not apply. Do not debug the two profiles as two bugs, and do not treat a watchdog line as proof the chunk ran. If the mod's own log was not created this session, read `Local/CowboyBingus/Helldivers2/Logs/BingusSharedLoader.log` under the Proton prefix. `load failed` plus `main function has more than 200 local variables` or `function at line N has more than 60 upvalues` means LuaJIT rejected the chunk before any of it ran; the sound bank still deploys. The cited line is where the cap was crossed. The bytes the game loaded are the `data/9ba626afa44a3aa3.patch_N` that contains the addon id. `local PROFILE` and `REVISION` in that file are the running build. On 2026-10-11 that slot moved from `patch_158` to `patch_157` across redeploys; match the addon id, do not reuse the number. A log that says the warhead `APPLIED` and then `search round N came up empty` is the weapon-table pitfall in section 9, not a second profile bug. A banner that already says `spares=4`, with the warhead applied and no spare-magazine line before the weapon search finishes, is section 4: the profile loaded and the scan stopped early. A magazine line that refuses because capacity is 0 is the same section's early index match, not a wrong weapon. A log line `spare magazines 6 -> 4` while the gun still shows 6, or a 6/4 counter, is the weapon that spawned before the write. Do not debug it as a second miss. Do not re-check the Arsenal option or the profile stamp. A mods-folder patch newer than the log's `REVISION` did not load: on 2026-10-12 the folder held `v3.4.1` while the log still said `v3.4.0`. A log that ends on the region-count line and a dump from that same second is the boot-scan pitfall there. The Dominator line `warhead: ... explosion on impact 0 -> 388` prints the source pistol row (`src_rec` at +144), not the bytes written to the Dominator. On v3.4.5 `prepare_blast` had already set the SAFE payload to slot 216, and that line still said 388. Read the payload, or a log line taken from `state.expected`, before naming the explosion SAFE fires. v3.4.7 is the confirmed close-range build: `SAFE round written: impact 388, expiry 0, arming 15.00 m`, and a close SAFE shot no longer killed the operator. v3.4.8's same line with impact 216 is the black-square build: the settings row matched and the tail hash did not (section 9). v3.4.9 points both modes back at 388, then quit the weapon search after three empty rounds while those tables were resident (section 9). v3.4.10 rebuilds the region list, copies the tail hash, and is the confirmed play: impact 216, expiry 0, arming 15, spares 6 -> 4, wheel, and full auto, with round 2 finding the tables at 394 MB after round 1's 1792 MB miss. v3.4.11 then ended rounds at 256 MB after ProjectileWeapon (`ending this round`). That cutoff is before the magazine on the same walk. v3.4.12 refreshes only at the near cap. Confirmed the same day: one round, refresh after 1792 MB, tables at 419 MB, spares 6 -> 4, impact 216, expiry 0, arming 15, wheel, and full auto. The release zip is named v3.4.0 and the script inside is v3.4.12.

Done when the log line shows the shipped `REVISION` and, for an experiment that kept that revision, the test token. The in-game numbers must match the manifest, or the reply quotes the log line that failed. `deployed: false` means that check has not happened yet.

## 8. Value-scan patching (health / armor)

**High-risk: whole-process value scanning.** See the safety boundary at the top of this file before writing anything.

Some tables are found by searching memory for a known VALUE, not the LDLD type
hash — the record array address cannot be derived from the header. The exosuit
HealthComponentData is the example: scan for health values 1800 (hull), 550
(legs), 800 (arms), then walk back to the record. Offsets in the reference.

A value-scan is dangerous. A loose match ("main health 1800", or "field at +280
== 4") matches unrelated data and corrupts the game (black screen / silent
close). Require the FULL signature before writing — for the mech body: main
health 1800 AND default armor 4 AND at least one zone with a known health
(400/550/10) — then write only the confirmed zones. Read back and roll back on
every write, exactly like the type-hash path. Never match a record by a value
this mod already wrote.

A value-scan is also the launch-time cost: it walks the WHOLE process (~4 GB)
for the value, every chunk, and retries the whole pass when a separate table is
the straggler. Bound it two ways. **Stall the value-scan once its table is
passed** — the mech table is ~11 MB contiguous, so once a write has landed and N
chunks (256 ≈ 32 MB) pass with no new record, stop scanning for that value.
**Early-exit the whole scan once every subsystem reports applied** (magazine,
projtype, armor, rockets each `> 0`), instead of finishing the remaining GB and
re-running up to `MAX_ATTEMPTS` full passes. The stall/exit only stop the
search; the full-signature guard above still decides what is written.

The settle floor is the game's load order, not scan speed. The straggler tables
(WeaponMagazine/ProjectileWeapon) can be absent from memory until ~60 s after
launch — the mod retries until they appear, and no amount of scanning finds a
table that is not resident yet. When the spike is already fixed, do NOT keep
lowering the frame budget to chase a shorter settle: a smaller per-frame budget
only trades the spike back for more wall-clock duration and risks `MAX_ATTEMPTS`
expiring before the straggler loads. The remaining settle is the game loading,
not mod overhead.

## 9. Pitfalls that each cost a game test

- **Local declared after use.** A `local x` placed below the function that uses
  `x` makes it a nil global inside that function — "attempt to compare nil with
  number" at the first comparison. Declare locals before the functions that
  reference them. `luaparser` does not catch this.
- **A forward-declared local is shadowed by a later `local function` of the same
  name.** `local drain_pending` at the top of a chunk and a later `local
  function drain_pending()` are two DIFFERENT locals. Any function defined before
  the `local function` line (the ProjectileWeapon resolver, which calls
  `drain_pending()`) closes over the first, still-nil one. The call throws
  "attempt to call a nil value", and if it sits inside a `pcall` the error
  vanishes. In the Dominator this meant every weapon table seen before
  ProjectileWeapon — magazine, LoadoutEntry, WeaponData, always first in memory
  order on build 6AB3B43F — sat in a pending slot and never resolved: a stock
  first life, a vanilla first armory look, and traits landing a minute later.
  Present since v3.3.5 and masked by the second search round; v3.4.14 is the
  confirmed fix. Correct it by assigning the forward local —
  `drain_pending = function() ... end` — never `local function drain_pending()`.
  Catch the whole class with a lint that flags a column-0 `local name` later
  redeclared by `local function name(` (tools/lint_lua.py, run under LuaJIT via
  lupa). Also stop swallowing resolver errors: log the second return of
  `pcall(handler, ...)` instead of ignoring it.
- **LuaJIT 5.1: no `goto` / labels.** The game runs LuaJIT 5.1, which has no
  `goto` statement and no `::label::` (those are Lua 5.2+). A `goto`/`::continue::`
  rewrite fails the `luaparser` (5.1) gate with `'=' expected near 'continue'` —
  restructure the loop instead of using a label.
- **LuaJIT: 200 locals per function, and 60 upvalues.** Bingus reports
  `main function has more than 200 local variables` or `function at line N has
  more than 60 upvalues`, and the addon does not load. Count every name in a
  column-0 `local` (`local a, b` is two). `do`/`end` is the same function, so
  those locals still count. Do not fix the 200-local cap by nesting the tail
  in one `local function`: that function then closes over the earlier locals
  and hits the 60-upvalue cap (verified 2026-10-11, Dominator v3.4.0, the
  loader line moved from the 200-local error to `function at line 1745 has
  more than 60 upvalues`). Put the constants in one table (`local C = {}`,
  `C.OFF_SPEED = 32`) and keep the chunk flat. Leave `local PROFILE` as its
  own local when a packer stamps that line. `luaparser` does not catch either
  cap. Done when the loader log says that addon `loaded` and the mod log
  shows the shipped revision.
- **A finished weapon search is not proof the tables are absent.** A nearest-first cap of about 768 MB misses them when they sit ~1.4 GB from the projectile table, and the walk reuses the region list collected for that scan. v3.4.9 rounds 1 and 2 logged `weapon tables not loaded in the nearest 768 MB`. Round 3 read 4442 MB, logged `magazine table was not in this pass` and `search round 3 came up empty`, then stopped (`WSCAN_MAX_ROUNDS` 3). The operator died and dropped again: still 6/6, no wheel, no full auto. A later `/proc/<pid>/mem` search of that same process found the headers: magazine `0xFB8D88A3` at `0x20b91111c`, weapon data `0x88E4DBB1` at `0x20d180aec`, loadout `0x4F2CF417` at `0x20b93eea4`, projectile weapon `0x45171B68` at `0x20e4d14ec`. The projectile table was `0x26146002C`. Death does not start another round after the cap. Before saying the tables are missing, search the process for those four LDLD headers. If they are present, rebuild the region list and search again. v3.4.10 does that (fresh list each round, 1792 MB, 12 rounds). That play is confirmed: round 1 still logged the 1792 MB miss, round 2 found the tables at 394 MB, and the spare, wheel, and full-auto lines followed. Do not end the walk a fixed distance after ProjectileWeapon. v3.4.11 did, 256 MB past that record, and the log then said `weapon tables still not mapped after the refresh (256 MB); ending this round` on rounds 1 through 4. The magazine on the confirmed run was 394 MB into the walk, past that cut. Only the near-byte cap or the end of the region list means the pages are not mapped. v3.4.12 uses that rule and has not been confirmed. The 2026-10-11 empty 621 MB rounds are the same class of miss. Done when the log shows the recoil line and section 4's `spare magazines 6 -> 4`, or the reply quotes those header addresses and says the search already stopped.
- **Do not read process memory during boot.** The 2026-10-11 22:43 dump is
  `0xC0000005` in `ntdll.dll+0x39f91`, a read of `0x8d3f0000`, and
  `DominatorRechambered.log` stops at `round 1: 3840 regions`. `pcall` does
  not catch that fault. Start the walk after about 15 s (frame 900) and skip
  a region larger than 1 GB. Done when a later log line exists and the
  process is still running. The 2026-10-12 16:41 mission got past the
  region line (warhead applied, weapon search still running) with no ntdll
  fault, so keep the delay. That log's missing spare-magazine write is
  section 4, not this crash.
- **Black squares are the explosion-table tail hash, not a settings-row field.** `impact visuals: copied` with unchanged fields, including a zero disintegration particle, did nothing. v3.4.8 row 216 matched 388 except +0 and the floats +20, +24, and +32. The u64 at +56 matched. +40 on both rows pointed at row 92's tail slot, not row 205's. The tail is one u64 per row: `tail_base = u64_at(source_row, 41) - source_index * 8`. On that process it was 136 bytes after `records + count * stride`. Row 92 (id 388) and row 125 (id 158) were `be50b3e0791fddc7`. Row 205 (id 216) stayed `b965230e05d4a6c6` because the settings clone never wrote it. That leftover hash is the black-square graphic. Copy the pistol tail u64 onto the spare row and point that row's +40 at its own tail slot before pointing a projectile at the spare id. v3.4.10 did that. The mission log is `blast: effect hash copied from row 92 onto row 205` and `SAFE round written: impact 216, expiry 0, arming 15.00 m`, and the operator said that play nailed it. Do not put the projectile back on 388 just because the 152-byte rows match, and do not invent another effect field inside the settings row.
- **Arsenal overwrites direct edits while running.** Editing a mod folder and
  `hd2a_data.json` while `hd2arsenal` is open gets reverted on its next save.
  Quit Arsenal, edit, reopen, deploy — or import a rebuilt zip instead.
- **Resource hash vs entity hash.** A game object's network descriptor
  `resource` (u64) can be the same value as the table's entity key for a given
  weapon, but never assume it — verify against SHODAN's WEAPONS catalog
  (`src/stat_editor.lua`, third column) or HD2Runtime's capability catalogs.
  The Dominator's entity key AND resource are both `0x80F1A156D9FA1E36`.
  `0xB6AFF2195568767F` is the **R-36 Eruptor**, not the Dominator — an earlier
  Dominator build pointed `DOMINATOR_ENTITY` at the Eruptor and silently
  installed the ammo wheel + recoil on the wrong weapon. Compare the right one.
  **The durable fix is to derive the entity hash at runtime, not hardcode it.**
  The wheel, fire-mode, recoil, and trait lookups all key off the weapon entity
  hash; a build that reshuffles entity IDs silently kills every one of them while
  the warhead swap (keyed by `ProjectileType` + record content) keeps working.
  Derive the hash instead: find the weapon's own ProjectileWeapon record by its
  content-stable projectile type (projtype at +0, already verified by the warhead
  matcher), then read the entity hash back out of the 16-byte bucket entry
  (`{lo u32, hi u32, slot u32, pad u32}`) whose `slot` points at that record, and
  use that derived hash for the WeaponData and LoadoutEntry lookups. Ordering:
  the scan can reach WeaponData / LoadoutEntry before ProjectileWeapon, so stash
  those tables (`pending_wd` / `pending_le`) and resolve them once the entity is
  derived (a `drain_pending()` call at the end of the ProjectileWeapon resolve).
  Keep the hardcoded hash only as a diagnostic seed and log when the derived value
  differs ("build moved it"). A multi-weapon pack cannot key that lookup on the
  projectile type number alone. Match the ProjectileSettings round by name hash +
  speed/mass/drag/gravity/arming + damage-type id, and add one more content field
  when a twin still collides (the MG-206 twin matches all of those and is separated
  by the u64 at projectile +72). Require exactly one surviving weapon record and exactly one bucket
  entity. A round fired by several weapon records still counts if a field this
  mod does not write narrows them to one. Zero or two survivors means write
  nothing — do not fall back to the seed. Stash the keyed tables until both
  ProjectileSettings and ProjectileWeapon have been seen; a scan round that has
  not seen them does not count toward the give-up limit. If the log already says a fingerprint did not resolve to one entity, both tables were resident. Another mission loads the same registry and fails the same way — fix the shared-record match first. Only "projectile table not resident" can still be cured by dropping in. Realistic Weapons 1.3
  is the worked example (census 2026-10-07, build `game.dll` `6AB3B43F`): the
  One-Two grenade is shared by two weapon records and is split on +0x94/+0x98,
  and the MG-206 round is shared by five and is split on +0x30 float 180.
- **A game update can silently kill the weapon-wheel features while the warhead
  swap keeps working — check the game build before touching wheel code.** The
  Dominator's wheel (fire mode, programmable-ammo selector, recoil, armory
  traits) is located by the entity hash `DOMINATOR_ENTITY`; the warhead swap is
  located by `ProjectileType` + record content. So a post-update report of
  "rechamber works, but no full-auto / no safe-unsafe in the wheel" points at the
  entity-keyed lookups, not the wheel logic. Before re-deriving anything, confirm
  a game update landed after the last good run: diff `appmanifest_553850.acf`
  (`buildid`, `LastUpdated`) and the `Helldivers 2/data/` file mtimes against the
  mod log's mtime (path is in the source's `write_status`; the Dominator's is
  `%LOCALAPPDATA%/Hd2ProjRecon/DominatorBoltPistol.log`). A log that predates the
  update is the last good run, not proof the code broke. **First discriminator:
  does the operator reproduce it?** If the wheel works on the operator's own
  machine on the current build, the report is a reporter-side conflict (a second
  mod writing the same WeaponData fields — the guarded writes back off), not a
  build break; have the reporter disable every other mod and relaunch before
  touching code. Only a report the operator reproduces is a build break: then it
  is a stale entity hash OR a moved table stride. The durable fix for a stale
  hash is to DERIVE the entity hash at runtime instead of hardcoding it (below,
  and in `references/install-and-format.md`); do not just re-derive it every build
  with the refscan census (section 11) — that is the one-time check, not the fix.
- **Classify a mod's fragility before answering "will a game update break it".**
  To triage one mod or a whole set, rank each writer by how it LOCATES its target,
  most-robust first: (1) content identity — name hash + ballistics via
  `ProjectileType` (survives enum recycling; the Dominator warhead swap); (2)
  content-anchored value scan (exosuit armor health 1800/550/800 — offset-free but
  dangerous, section 8); (3) entity-hash-keyed table lookup (weapon entity hash —
  breaks when a build reshuffles entity IDs; fix by deriving at runtime, above);
  (4) fixed code offsets (M1000's `0x195C374` — most fragile, a binary shift kills
  it outright). A mod that *fails safe* — its keyed lookup requires "exactly one
  layout fits" plus a plausibility ceiling, so drift no-ops cleanly instead of
  corrupting — is still broken, just silently (Realistic Weapons is this class).
  Deriving an entity hash uses the fingerprint rule above, not the projectile
  type number by itself. diag-5 already writes the join to `refscan_pwbuckets.txt`
  (`references/memory-census.md`). A census without that file is the older dump
  and cannot be joined offline. Do not guess a fingerprint, and do not extend
  refscan to add a bucket dump it already writes.
- **"Raise to value" is not "+1".** Raising AV3->AV4 leaves AV4 untouched; "+1
  to all" also bumps AV4->AV5 and AV0->AV1. The "+1" version writes more fields
  and is less selective, so it needs the full signature guard; a plain raise
  was safe because it only wrote exact value 3 with exact health 550/800.
- **A maintain loop that re-asserts the whole record fights live editors on
  shared fields.** `maintain()` compared the full cached record and rewrote every
  field on any mismatch. SHODAN's projectile-speed editor writes the speed field;
  our maintain saw the record "changed" and rewrote speed to 380; SHODAN rewrote
  its value; forever — cross-process writes every ~5 s (lag spikes). This is the
  runtime twin of section 2's install-time overlap. Make maintain field-selective:
  on mismatch, diff only the fields this mod owns (warhead damage type + explosion
  on impact/expire, arming) and leave shared ballistics (speed, range) to the
  other editor, or add a config key to hand the field over — the shipped syntax
  is `speed=off` (or `speed=N` for a custom velocity), not `speed=-1`, which
  silently leaves the default: a bare `-1` passes neither the `"off"` string
  branch nor the `n > 0` numeric branch. The recognition cue is a user report of
  "it constantly goes back and forth with it."
- **A per-frame/per-second HUD poll hitches the game.** A badge that must appear
  only while a weapon is equipped still needs a poll, but the expensive walk
  (`objects_owned_by` + `game_object_is_type` per owned object + two hash-table
  walks, dozens of ReadProcessMemory calls) must not run every 60 frames. That
  caused audio buffer underruns ("sound kept cutting out") and dropped hit
  registration ("shot center mass, bot not hit") — both gone on reverting to the
  version without the HUD. Throttle the equipped-check to ~5 s (match
  `VERIFY_EVERY`), cache the game.dll base and the player avatar (invalidate on
  `net` pointer change / failed lookup), and only redraw when the equipped state
  actually changed. The Dominator badge was removed in v3.1; the ammo wheel
  (section 11) that replaced it is the native programmable-ammo selector, not an
  overlay — for a state a native UI already renders, deleting the overlay beats
  throttling it.

## 10. HD2Runtime (Skyeshade SDK) and SHODAN ecosystem

The typed-SDK alternative to hand-rolled scanners. `mods/skyeshade/hd2runtime`
is a read-only shared runtime (Bingus v15+/API 1): it owns memory access, page
protection, timers and resolution; dependent mods declare declarative
transactions instead of scanning. API shape:

```lua
local hd2 = require('mods/skyeshade/hd2runtime')
local p = hd2.weapon('AR-23 Liberator'):attack('primary'):projectile()
return hd2.ensure({ transaction = { id='x', target=p, allow_shared=true,
    changes = { { field=hd2.fields.damage.player_standard_damage, expect=90, value=120 } } }})
```

- `hd2.fields.*`, `hd2.enums`, `hd2.resources` are the discoverable constants;
  `allow_shared` + `expect`/`value` is the framework-level solution to the
  write-conflict problem section 9 documents — the runtime detects shared
  writers and refuses to fight.
- The runtime is fully open source (`SkyeShade/HD2Runtime` on GitHub, `runtime/*.lua` — the memory reader, mappers, event system, all readable), not a closed blob. The *installed* runtime ships as a 16 MB compiled bundle, but the source is public. It cross-confirms our hashes: `0xBD4042C2`
  (ProjectileSettings) x1735, `0xE0A72CF0` (DamageSettings) x1984,
  `0xFB8D88A3` (WeaponMagazine) x29, Dominator resource `0x80F1A156` x12.
- **SHODAN's chain-walk census beats byte-scanning.** The game packs its settings
  tables back to back at the start of memory allocations. Read 16 bytes at each
  region start; where a table header (`LDLD` + u32 1) sits at offset 0 or +4,
  that is a chain head. Walk header-to-header: read the 24-byte header, and the
  next table follows the payload within 16 bytes (checked at offsets 0/4/8/12/16).
  One pass enumerates every table without scanning hundreds of megabytes. Then
  hand tables to resolvers in dependency order — ProjectileWeapon FIRST, then
  WeaponData / LoadoutEntry / the magazine table — instead of resolving each
  block as it is seen. Resolve-as-seen is order-dependent and, combined with a
  single pending slot and a swallowed error, is how the Dominator lost its
  weapon writes (see section 9). A census-first, resolve-after pass is the
  robust shape; keep the byte scan as the fallback for tables a chain walk
  misses.
- **Decide live-vs-cached from the SDK's per-field `effect` model, never by guessing.**
  `sdk/PlayerWeaponAuthoringCapabilities.json` (and the ModBuilder repo's bundled
  copy) publishes, for every writable field, an `effect` block: `activeSource`,
  `appliesWhen` (`weapon_build` / `menu_build`), and `instantiationOnly`. That is
  the authoritative answer to "is this field read live or cached?":
  `instantiationOnly: true` = the game copies it into the weapon when it builds
  it, so a write applies to weapons built AFTER it (redeploy, reinforce,
  re-equip), not one already in hand; `appliesWhen: menu_build` = presentation
  (the armory label changes on reopen, not live). `sdk/LiveEvidenceCatalog.json`
  names the exact fields a user test proved in play (`live_proven`) vs
  `allow_unverified_effect`. `sdk/WeaponFireRateCapabilities.json` gives each
  weapon its rate slots, selector state, and writability. Consult these before
  writing a field whose timing you have not proven yourself — a guessed "cached
  at construction" cost the cyclic-rate mistake (corrected: `rounds_per_minute`
  is three f32 slots, `instantiationOnly`, section 4).
- **HD2Runtime has NO HealthComponentData** (`0xB3915DE3` = 0 occurrences).
  The exosuit health/armor value-scan technique (section 8) fills a gap the
  ecosystem SDK does not cover.
- **Presentation labels (the armory AP/trait display) are writable, not native
  code.** `hd2.fields.presentation.armor_penetration` (allowed `none`/`light`/
  `medium`/`heavy`/`light_anti_tank`/`anti_tank`) and `presentation.traits` both
  back onto `LoadoutEntryComponentData` at +12, storage `armor_penetration_label`
  / `trait_set`, width 20 (five trait tags); `SLOT_SETS` maps `trait_set=5`,
  `armor_penetration_label=5`. This is the fix for a mod whose warhead/damage is
  patched but whose armory label never moves. Both are flagged
  `allow_unverified_effect` ("an edited label appearing in the menus has not been
  gameplay-tested") and "menus build their labels when they open" — expect the
  change on reopen, not live. The dlsum type hash of `LoadoutEntryComponentData`
  is `0x4F2CF417`. Hand-rolled route (no HD2Runtime): the table is 386 index rows of
  16-byte `{resource u64, record u32, reserved u32}` then 193 records × 32 bytes; the
  five trait tags are the u32 localization string IDs at +12. The index is keyed by the
  weapon's resource hash — for the Dominator that equals its entity hash
  `0x80F1A156D9FA1E36`, so the same `{lo,hi,slot,pad}` walk used for WeaponData (section 4)
  resolves the record. The tags are RAW localization string IDs, not the SDK's semantic
  ids: `heavy_armor_penetrating` = `0x273E3C6D`, `explosive` = `0x4EFEA81C`,
  `medium_armor_penetrating` = `0xB7E2C047` (the Dominator's stock tag). Guard on the
  stock tag list and re-apply on map reload (worked example: Dominator v3.3.4 relabeled
  MEDIUM → HEAVY + EXPLOSIVE).
- **Enemy attack → projectile reference (the missing piece of the three-way clone
  check).** HD2Runtime 0.28.0's dev SDK (`EnemyAuthoringCapabilities.json`) addresses
  enemies by `hd2.enemy(name)` / `hd2.structure(name)`, `zone_<index>` and `slot_<n>`,
  and maps each attack role to a FIXED row: `projectile` / `spray` / `explosion_impact`
  / `explosion_expiry` → DamageInfo; `projectile_settings` → ProjectileSettings;
  `explosion_settings_impact` / `explosion_settings_expiry` → ExplosionSettings. So
  enemy projectiles ARE referenced — through the enemy class's own attack rows into
  ProjectileSettings, not a standalone enemy table (consistent with our census that
  found no top-level enemy projectile table). This is the third leg (enemy) of the
  clone-safety reference set, now reachable by typed SDK rather than reverse-engineering.
- **A projectile row has three reference slots** (`AttackOutputSlots`): `directDamage`,
  `impactExplosion`, `expiryExplosion`. A slot write targets the ROW
  (`hd2.attack_output(row)`), not a host, so it changes every entity firing that row
  (carries `allow_shared`). This is the typed-SDK equivalent of our field-selective
  warhead copy (section 11) — and its "shared row" discipline (named `SharedConsumers`,
  `SharedScopeKey`) is the typed model of our "never overwrite a record something else
  references."
- **Runtime's own clone technique** is `AttackOutputSpareTwin`: "an independent native
  row identical to its twin except its references," re-proven before every write — the
  same census-verified-dead-record discipline as our Q1 clone, only the SDK publishes
  the spare row instead of us hunting one.
- **Output families — the master "which component owns the reference" map.** A weapon
  entity owns exactly ONE output-family component: projectile → `ProjectileWeaponComponent`
  (+0 ProjectileType; also owns RPM +8, infinite ammo +36); beam → `BeamWeaponComponent`
  (+0 BeamType; fire mode +100, heat +16); arc → `ArcWeaponComponent` (+0 ArcType; RPM +4,
  infinite ammo +8); spray → `SprayWeaponComponent` (+200 DamageInfoType); melee →
  `MeleeWeaponComponent` (+12 DamageInfoType). The fire-control (WeaponData) and resource
  (Magazine/Rounds/Heat/Charge) components sit alongside. The ONLY cross-family links in
  settings data: ProjectileInfo +144/+156 → ExplosionType (impact/expiry); ExplosionInfo
  +84 → ProjectileType (shrapnel/submunitions); ExplosionInfo +120 → ArcType (an explosion
  can release an arc); BeamInfo +96 → ExplosionType. Nothing outside the beam system
  references a BeamType.
- **Status effects live on the DamageInfo row, not the weapon/projectile.** Every DamageInfo
  has four inline status slots at +44+8n (u32 StatusEffectType then f32 strength); unused
  slots are 0 and used slots are packed. 71 statuses exist; 11 are "attachable" (proven on a
  player-side attack): fire, fire_panic, burning_heavy, flamer_slowed, stun_small/medium/large,
  gas(+_2), gas_confusion(+_2). Status definitions are global 152-byte StatusEffectSettings
  rows (+40 duration, +44 tick DamageInfo). The numeric status type is NOT stable identity
  ("Stun Small" = 37 this build, 36 in filediver) — match by the stored name.
- **Package residency — why a projectile swap can go invisible.** A donor projectile/explosion
  from another weapon lives in that weapon's loadout package, loaded only while some system
  holds a reference (RefcountedPackageSystem). Items nobody carries are NOT loaded, so a swap
  without the donor equipped can spawn a purple question mark / invisible projectile. HD2Runtime
  0.27+ auto-loads the donor package through the game's own system (live-proven); a hand-rolled
  mod CANNOT — the Stingray `ResourcePackage` constructor is stripped from this build. This is a
  hard ceiling on cross-weapon projectile swaps in a Bingus mod without HD2Runtime.
- **Fire modes are a 4-slot list, not 3.** `WeaponDataComponentData`: +140 `num_burst_rounds`,
  +144 primary, +148 secondary, +152 tertiary, **+156 quaternary**. FireMode enum: None=0,
  Automatic=1, Single=2, Burst=3 (values 4–8 are charge/safety states, unnamed and read-only).
  Full-auto is "write Automatic into an empty mode slot" — no flag or bitmask. `weapon_presentation_traits`
  is still `pending` (not live-proven) in LiveEvidenceCatalog; `weapon_presentation_penetration_label`
  IS live-proven (AR-23C) — both need `allow_unverified_effect` for the Dominator.
- SHODAN Stat Editor is a dependent of HD2Runtime (its weapon/stratagem
  catalogs credit it). Its field layout is authoritative for projectile/damage
  offsets: projectile stride 272 (velocity +32, drag +40, gravity +44, pen
  slowdown +64, damage type +60, explosion +144/+156); damage stride 76 (damage
  +4, durable +8, ap_direct +12, ap_slight +16, ap_large +20, ap_extreme +24,
  demolition +28, stagger +32, push +36). Matches our verified layouts.
- The separate `SHODAN Stat Editor简体中文` download is a translation-only
  addon (`mods/shodan/stat_editor_zh_cn`); it hooks `Gui.text`/`text_extents`
  and writes no stat. The actual editor is `SHODAN-Stat-Editor` on GitHub.

## 11. Programmable ammo (weapon-wheel alternate round) — point at a real round

The Autocannon's flak/APHET selector is the game's **programmable-ammo**
function. The three writes that build it are below. The v3.0 build tried to
hand-roll a spare projectile record and shipped a game-breaking bug; the safe
fix is to borrow a real, referenced round (point the function slot at the source
round) rather than clone. Cloning an unused round IS possible, but only with
full verification — see the "clone IS possible" note at the end of step 1.

1. **Spare projectile — borrow a real round, or clone only with full verification.** The v3.0
   build "found" a spare by looking for a record referenced by no weapon
   (ProjectileWeapon +0/+576) that looked dormant (zero name hash or zero
   speed). **That heuristic is wrong.** Enemy projectiles are referenced OUTSIDE
   ProjectileWeapon — enemy attacks live in an enemy-weapon component
   `0xd25fc7f7` = `WeaponDataComponent` (the enemy counterpart to
   player WeaponDataComponentData 0x88E4DBB1, same 1232 stride), plus a spread component
   `0xf916ed4b` = `SpreadInfo` (12 bytes), a component array `0xb4789330` =
   `SensorEyeComponent` (44 bytes), and a damage table `0x260cbe2b` = `DamageInfo`
   (76 bytes, rooted at 0xe0a72cf0) — none of which a ProjectileWeapon-only scan sees. These
   four are COMPONENT TYPES embedded inside enemy archetype records, not standalone LDLD
   tables (see `references/memory-census.md`); enemy data loads only in-mission as keyed
   hash tables, so scanning for `0xd25fc7f7` as a top-level table finds nothing. Enemy
   actors are keyed by a 32-bit hash, not the weapon entity hash. They also
   legitimately carry `name==0`, so they look dormant. The Bile Titan's spit is ProjectileType
   79 — zero name — and the clone overwrote it with the Dominator's explosive
   round ("bile titans spitting bolt rounds," titans ragdolling and instakilling
   players). **You also cannot append a record — and this is why "extend the
   table" is not a memory-edit option.** The projectile registry is a
   memory-mapped `dl_bin` the game deserializes at load into a fixed 350-record
   array, and a weapon references a round by a **compiled `ProjectileType` enum
   id** (`projtype 177`), which native code resolves as `base + id * stride` —
   not by pointer. So you cannot grow the array (nothing indexes it) and you
   cannot invent a new id (the game was compiled with a bounded `0..Count-1`
   enum). Truly new content goes through the on-disk `dl_bin` / resource-patch
   route (filediver + repatcher), not a live memory edit. `name==0` / `speed==0`
   is NOT evidence of "dormant."

   **The safe alternate is a round that already exists and is already referenced.**
   For the Dominator, that is the P/40-K's own projectile — the exact round the
   rechamber copies its warhead FROM, which natively fires the explosive warhead
   at 0.1 m arming. Point the function slot straight at it: SAFE (Dominator, 12 m
   arming, 380 m/s) vs UNSAFE (P/40-K's stock round, 0.1 m arming, 350 m/s). Zero
   projectile records are cloned or overwritten, so nothing outside the Dominator's
   own record is written (the only other write is `mode_label`/`mode_icon` on the
   source round, presentation-only). That borrow is the pre-Q1 fallback. The shipped wheel does not use it: the mission log is `Q1 clone: UNSAFE round cloned into ProjectileType 206` and `function projectile slot -> alternate round 206`.

   **The clone IS possible — but only with real verification, never a dormancy guess.**
   The GL-15 Evictor Airburst mod (dsh) clones projectiles/explosions into types it
   proves are "referenced by NOTHING" three ways: no entity delta, not in ANY
   weapon's `+0`/`+576`, and not in the enemy tables (the enemy-weapon component
   `0xd25fc7f7`, section 11 note above). That is the correct clone check. Our v3.0
   bug was that we skipped all three and guessed "dormant" from `name==0` / `speed==0`,
   which matches enemy projectiles. So: cloning an unused round is a real technique,
   but the bar is "prove unreferenced by weapons + entity deltas + enemy tables,"
   not "looks empty." If both rounds must share an exact stat (e.g. both at 380 m/s),
   that is the clone path — do not take it without the full three-way check.

   **The field-selective clone (how, once a target is proven dead).** Build the clone
   payload from the DEAD record, not the source, so it keeps its own `type` (+0) and
   `name` (+4) — the function slot (+576) resolves the round BY ITS ENUM TYPE, so a full
   source copy would stamp the source's type over it and the slot would point at the wrong
   record. Overlay the source's warhead (damage +60, explosion +144/+156), set the round's
   ballistics (speed +32, arming +160, lifetime +52 = range/speed), and write the wheel
   label +12 / icon +16. Before writing, re-verify the dead record still matches its census
   identity (name + ballistics) so enum recycling cannot slip a live record under you; then
   re-verify with one type read and fall back to the borrow if it moved. Enemy rounds carry
   `name==0` (documented; statistically confirmed 2026-10-06 at 3.25× over-representation in the
   enemy tables — see `references/memory-census.md`), so a `name!=0` record unreferenced by the weapon + shrapnel +
   re-arm offsets is outside the enemy reference set — that is how the enemy leg is closed
   without parsing the enemy archetype tables. Worked example (2026-10-06): type 206 = a
   dead near-duplicate of the R-36 Eruptor round (same name 0x095D6C88 / speed 180 / mass
   100, but explosion 380 vs 158), cloned into for the Dominator's 380 m/s / 0.1 m UNSAFE
   round; type 201 was meanwhile recycled (speed 30, damage type 189) — never trust a
   remembered enum value.

   **The census is a read-only diagnostic addon, not a guess.** To find the
   provably-unreferenced record, ship a separate throwaway addon (its own addon id,
   e.g. `mods/dsh/refscan`) that WRITES NOTHING and dumps the three readable reference
   sources to `Hd2ProjRecon/`: every ProjectileSettings record (type / name / ballistics
   / arming / damage / explosion refs), every weapon's `+0`/`+576` (walk
   ProjectileWeapon), the enemy archetype keyed tables (enemy data is NOT a standalone
   LDLD table — see `references/memory-census.md`), and every LDLD header (type hash →
   name via reverse dlsum). Set-difference the weapon + enemy + shrapnel references
   against the 350-record table offline; only a type in NONE of them is a clone target.
   The projectile table is **not resident while docked** — a single memory pass from
   the ship finds nothing, so the census must re-scan on a gap (≈10 s) until it has the
   table, and the operator must actually load a mission. One pass that "found nothing"
   at the dock is not evidence the table is empty. Parse the dump offline; do not
   encode the clone target until the set-difference is checked by hand.
2. **Function-projectile slot.** `ProjectileWeaponComponentData` (`0x45171B68`)
   +576 = the alternate round's type. Programmable Ammo off fires ProjectileWeapon
   +0, the SAFE row. It fires +576 only while that function is on. A SAFE self-kill
   is the primary row, not the clone, unless the function is on.
3. **Selector binding.** `WeaponDataComponentData` (`0x88E4DBB1`, stride 1232)
   `function_info` at +184 (left) / +188 (right), u32, = 8 (`programmable_ammo`).
   Bind whichever input is currently `none` — the Dominator's left is free, its
   right is already `fire_mode` (single/burst).
4. **Ammo icons + labels** (the same regardless of where the alternate round
   comes from). The wheel renders each round's own `mode_label`
   (ProjectileSettings +12, u32 localisation id) and `mode_icon` (+16, u64 icon
   resource) — presentation fields on the projectile record itself, not on the
   weapon tables. Plain projectiles leave both zero, so a wheel with no icon/label
   writes shows blank entries for both options. The label and the icon are
   independent — set them separately, and you can swap which icon goes on which
   round freely.

   - **Label is a RAW localisation string id**, not limited to the
     `modePresentation` catalog's offered labels. Any string in the game's
     `.strings` database resolves. To make the wheel read a specific word, find
     that word's id: extract the strings and read its `Key`:
     ```bash
     filediver --gamedir "$STEAM/.../Helldivers 2" -o /tmp/str \
       --types strings --strings-language "English (US)" -i "*"
     # then grep the *.strings.json for "Value": "<word>"; its "Key" is the u32 id.
     ```
     Native standalone "Safe" = 782820489, "Unsafe" = 622682013 (title-case;
     HD2 has no all-caps SAFE/UNSAFE string). A written id localizes to the
     player's language. Do not guess a string id by hashing the word yourself —
     read the `Key` from the extracted database.
   - **Icon** is a native weapon-function icon resource from
     `modePresentation.modeIcons` → `resource` (an `0x` hex). The u64 is
     little-endian — encode with `entity_le8(hi,lo)` (hi/lo halves of the hex)
     and it matches the runtime's `resource_bytes`. Icon resources offered:
     `ammo_he` `0x081DCAF42DC2ECBB`, `ammo_aphet` `0xF8EDE5F922C05CB6`,
     `ammo_slug` `0xB7812FA260A5F64F`, etc.

   The wheel shipped SAFE = "Safe" (782820489) + `ammo_aphet` icon and
   UNSAFE = "Unsafe" (622682013) + `ammo_he` icon. The string-id and
   icon-resource values above are current as of the v3.1 source-round wheel;
   read them back from the extracted database rather than trusting memory.

Enum (u32, WeaponFunctionType at +184/+188): none=0, zeroing=1, rate_of_fire=2, fire_mode=3, magazine=4, light_mode=5, laser_guide=6,
muzzle_velocity=7, programmable_ammo=8.

**Wheel shows but both icons are blank** — the `mode_label` / `mode_icon` fields
on the projectile records are zero; write the native values (step 4), not a
rendering fix. This is distinct from "wheel does not show at all" below.

Caveat: HD2Runtime marks giving a weapon a function projectile as
`allow_unverified_effect` — "the ProgrammableAmmo fire path is proven, but giving
this weapon a function projectile has not been gameplay-tested." Log every write
and confirm the wheel shows the alternate before shipping.

**When the wheel does not show, first prove the writes landed on the right
weapon** — do not blame rendering or selector conflicts until you have. The
log's own `ammo: ProjectileWeapon record at 0x… (projtype N, function M)` line
names the weapon that actually got the selector. `projtype` is the weapon's
round: the Dominator is `projtype 177`; `projtype 40` is the R-36 Eruptor and
proves the keyed-table lookup resolved the WRONG entity hash (section 9's
resource-vs-entity pitfall) — every write (wheel, source-round function slot,
and recoil) silently landed on a different weapon while the log still printed
"selector bound". Check that `projtype` against the intended weapon before touching the
wheel logic. A weapon that natively has a fire-mode selector and no ammo selector
*may* still not render the option even with a correct hash, but that is the
second hypothesis, not the first.

## 12. Vet a downloaded mod manager / tool before running it

When handed a download (zip or exe) or a repo and asked to evaluate it, triage
statically and never execute the payload. The HD2 scene has malware fronts
dressed as "toolkits." Signals, in order of weight:

- **A setup doc that says "disable Windows Defender / add exclusions" = malware.**
  A legitimate tool never asks you to weaken AV. This alone is enough to say
  delete-and-skip, no further analysis needed.
- **Repo with no source = download funnel.** Check the recursive git tree
  (`/git/trees/main?recursive=1`) and `/languages`. A README-only repo (docs +
  images, `languages` = `{}`) with a title like "Hacks" is not a mod tool — its
  real payload is an external installer.
- **Filler payloads.** Archives bloated with `verb_number.ext` files
  (`app_107.001`, `utils_132.sdat`) that are pure random bytes (entropy ~8.0
  bits/byte) and "dll" files that are `data` with no `MZ` header are padding to
  defeat AV hash/size heuristics.
- **Packed installer.** A `Nullsoft`/Inno installer at ~8.0 entropy is
  encrypted/self-extracting — nothing readable statically. Verify the bundled
  `sha256` matches the exe, then stop; do not extract-and-run.

Fingerprint with `unzip -l`, `file`, `sha256sum`, `strings`, and a byte-entropy
check. Real tooling names its components and credits its authors (filediver/xypwn,
Bingus/cowboybingus, RaidingForPants, SkyeShade). **SkyeShade's `HD2Runtime` and
`HD2Runtime-ModBuilder` (a separate C#/.NET GUI, open source with xUnit tests and
SHA-256-pinned SDK provenance in `THIRD_PARTY.md`) are legit — do not conflate them
with the malware repo "helldivers-2-mod-toolkit" (a README-only "Hacks" funnel
into a packed installer).** Closed source is not proof of malware
(Echelon is legit Delphi/VCL with no published source), but "disable AV" +
README-only repo + random filler + packed exe together are conclusive.

**Framework → portability.** Asked "is tool X portable to Linux / what is it
built with," identify the framework from the installer, not from prose: an Inno
Setup (`<description>Inno Setup</description>`) or Nullsoft `file` tag wrapping a
binary full of Delphi RTTI strings (`TList<System.Classes.TPersistentClass>`,
`TRttiInstanceFieldClassic`) is **Delphi/VCL — Windows-only**. A closed-source
Delphi tool has no Linux port path: "convert it" means a from-scratch rewrite,
not a recompile, and the source usually is not published (a repo whose
`/languages` is `{}` and whose recursive tree is docs-only confirms it). State
that up front instead of attempting a port.

Done when the reply names the payload kind, states run/skip/delete, and nothing
was executed.

## 13. Mine third-party mods for technique

When the operator drops a folder of mod archives "to study," the goal is to
extract durable technique, not to install anything. For each archive:

1. **Extract and classify every `.patch_0` with `os.walk`, not a shallow glob.**
   Patches nest 3–4 levels deep (`options/<name>/Addon/…`), so `glob('*/*.patch_0')`
   returns zero. Read the u32s at bytes 4 and 8 before trusting offset `0x50`.

   - **Single payload** (section 6 packer): u32 at byte 4 is 1, and Lua type
     `0xA14E8DFA2CD117E2` at `0x50` marks Lua. Source starts at byte 200. The three
     shapes below apply. A non-Lua type at `0x50` on this shape is a binary patch;
     record that hash.
   - **Bundle:** u32 at byte 4 is 4 and u32 at byte 8 is a resource count. Offset
     `0x50` is only the first type-table entry. HD2 HUD Plus 0.2.2 (verified
     2026-10-08, 721977 bytes) has count 30, first type `0xcd4238c6a0c69e32`, and
     Lua type `0xA14E8DFA2CD117E2` later in the table with count 2. The Lua is a
     long printable run (the first began at offset 47703), not byte 200. Do not
     resize the file. A same-length text edit, padded with spaces, keeps the
     unread resource-size fields valid. A length change without those fields
     rewritten corrupts the bundle.

   Within single-payload Lua there are three shapes, and the `-- HD2-Addon:` header is only one of them:

   - **Source** — byte 200 begins `-- HD2-Addon:`.
   - **Compiled bytecode** — byte 200 opens on a LuaJIT chunk header (e.g.
     `J\x02\x00`) with readable string constants interleaved in the binary: the
     chunk name (`@module_bridge.lua`), module/require paths
     (`mods/codex/p11_self_heal`), loader globals (`CowboyBingusModLoader`). No
     `-- HD2-Addon:` line, but still Lua — do NOT file it under binary. Codex
     Module Bridge and P11 Self-Heal are this shape (verified by their `J\x02\x00`
     chunk headers and readable `mods/…` string constants).
   - **Obfuscated source** — byte 200 still begins `-- HD2-Addon:` but the rest is
     high-entropy (step 3).

2. **Pull single-payload Lua from byte 200; the interesting part is the tail.** For a bundle, take the printable Lua run instead. In a single-payload mod the addon
   id, `change` string, and write offsets live in the `worker.register({…})` /
   search-spec block at the END of the file. A bundle may not have that block: HD2 HUD Plus keeps the behavior in a baked widget table (`GameBaked`) and a generic `run()` updater. Grepping the middle of a single-payload file only finds the
   shared scanner framework every option reuses — not what it writes.
3. **Unreadable Lua comes in two shapes — identify which, then move on.** Do not
   burn a round trip trying to decode either:
   - **Obfuscated/encrypted source**: the `-- HD2-Addon:` header line is readable
     but the rest is high-entropy bytes (e.g. hd2lab spawn_director).
   - **Compiled bytecode**: no readable `-- HD2-Addon:` header at all; the only
     plaintext is string constants scattered through the chunk (step 1). Those
     strings still name its dependencies, so grep them for `mods/` before
     cataloging — that is how Codex Module Bridge revealed it loads
     `mods/codex/p11_self_heal` and `mods/codex/constitution_bolt_amr`.
4. **Catalog each mod** — addon id + what it taught us — in
   `references/mods-catalog.md`. Fold any correction into the section that owns
   that topic (a fire-mode or reload finding goes to section 4, not a new
   section). Note when a mod uses the OCLAW_UPDATE_BUS dispatcher (section 7
   attribution caveat) so we do not copy that part.

When asked what to ask the operator to download next, the remaining gaps are
**open-source enemy-attack / new-projectile mods with readable Lua** — we have
the enemy-weapon component's type NAME (`WeaponDataComponent`, 0xd25fc7f7, and
its SpreadInfo / SensorEyeComponent / DamageInfo sub-components, all resolved by
reverse dlsum 2026-10-05) but not the field offset where it references its
projectile — a second independent confirmation of that layout would harden it. Plain stat packs and sound swaps
are low signal. Open-source GitHub repos beat Nexus zips (readable Lua with
comments).

**Never delete the archives before finishing the full pass.** Classifying an
archive (Lua/binary/obfuscated) is NOT the same as mining it — several mods only
got classified before the folder was wiped, which lost their Lua bodies. The
whole point of this exercise is to READ every mod's code and extract technique.
Only delete after every archive has been classified AND every Lua body read AND
its technique cataloged; if in doubt, keep the folder.

Done when every archive is classified (source Lua / compiled bytecode / obfuscated / binary), every Lua body
has been READ (not just identified), mined techniques are cataloged with their
addon ids, and corrections are merged into the authoritative section rather than
duplicated.
