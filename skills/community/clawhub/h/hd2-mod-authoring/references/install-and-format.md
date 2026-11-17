# Install audit and patch format

Snapshot of `~/.config/hd2arsenal/mods` on 2026-10-01, then the retire the same day. The first count was 57 folders and 509 `.patch_0` files (47 Lua-like, 462 binary). After moving eight folders to `_retired` and adding `m1000_combined`, re-count before quoting it. Every container starts with magic `0xF0000011`. Bingus Shared Loader v18 is installed.

## Patch container (measured)

Dominator `Addon/9ba626afa44a3aa3.patch_0`. This layout is the single-payload packer only (u32 at byte 4 equals 1). The same magic with u32 at byte 4 equal to 4 is a multi-resource bundle; do not apply these offsets. Classify and edit that shape from SKILL.md section 13.

- Byte 0: u32 magic `0xF0000011`.
- Byte `0x20`: u64 total file size.
- Byte `0x50`: u64 type `0xA14E8DFA2CD117E2` (Lua).
- Byte `0x68`: u64 MurmurHash64A of the addon-id string, seed 0.
- Byte `0xA0`: u32 Lua size plus 8.
- Byte `0xC0`: u32 Lua size.
- Byte 200: Lua source, nothing after it. `len(patch) == 200 + len(lua)`.

The header rebuilds as three little-endian structs, then payload (verified
byte-identical against the v2.7 patch on 2026-10-03):

```python
header   = struct.pack('<III20sQQ24s', 0xf0000011, 1, 1, b'', length, 0, b'')  # 72 B
type_ent = struct.pack('<IIQIIII', 0, 0, LUA_TYPE, 1, 0, 16, 16)                # 32 B
res_ent  = struct.pack('<7Q6I', murmur64(addon_id), LUA_TYPE, 192, 0,0,0,0,
                       len(payload), 0, 0, 16, 16, 0)                           # 80 B
```

72+32+80 = 184, pad to 192, then `payload = struct.pack('<II', len(source), 2) + source`.
`length = 192 + len(payload)` — it is NOT rounded to 16. `tools/archive_writer.py`'s
`(offset+len(payload)+15)//16*16` is for the arena mod and gives a wrong size field here.
`murmur64` is MurmurHash64A, seed 0, `m=0xc6a4a7935bd1e995`.

The filename `9ba626afa44a3aa3.patch_0` is a shared slot name, not a type. Lua uses type `0xA14E8DFA2CD117E2`. The Dominator Space Marine II firing sound is that same filename, 2454160 bytes, type `0x535a7bd3e650d799`, and byte 200 is not Lua. It was copied verbatim from the WWSC archive entry `Jar-5 Dominator - Bolter/Space Marine II/9ba626afa44a3aa3.patch_0` into Include folder `Space Marine II/`. Some resource patches do use other names (`0a4bd8a1833f11b2`, `1577e917ad1f287d`). Do not rename those, and do not run either kind through the Lua packer.

## Maintained mods (worked examples)

- JAR-5 Dominator - Rechambered, addon `mods/dsh/dominator_bolt_pistol`, source `hd2-mods/dominator-rechambered/jar5_dominator_rechambered.lua`. The shipping build is `v3.4.14` (Regular and Realistic; release previously carried the `v3.4.0` name). The late-traits / stock-first-life / vanilla-first-armory bug was a forward-declared `local drain_pending` shadowed by a later `local function drain_pending()` (SKILL.md section 9) — fixed in v3.4.14. The confirmed playable build is `v3.4.10` realistic (impact 216, expiry 0, arming 15, tail hash copied). `v3.4.7` is the earlier dud on explosion 388: `SAFE round written: impact 388, expiry 0, arming 15.00 m`. Round 2 still writes the spares after a 768 MB miss (v3.4.8 found them at 415 MB; the gun already in hand stays 6/4 until respawn). `v3.4.8` set impact to 216 with expiry still 0 and the operator saw black squares; the settings row matched 388 except the id and +20/+24/+32, and the tail hash did not (SKILL.md section 9). `v3.4.9` points both modes back at 388, then quit after three empty weapon-search rounds while the tables were resident. `v3.4.10` rebuilds the region list, walks 1792 MB for 12 rounds, copies the pistol tail hash onto slot 216, and points impact there with expiry left at 0. That play is confirmed: `effect hash copied from row 92 onto row 205`, `SAFE round written: impact 216, expiry 0, arming 15.00 m`, `spare magazines 6 -> 4`, the wheel, and full auto. Round 1 of that log still missed at 1792 MB; round 2 found the tables at 394 MB. `v3.4.11` ended later rounds at 256 MB after ProjectileWeapon and is the failed cutoff. `v3.4.12` refreshes only at the near cap. Confirmed the same day: one round, refresh after 1792 MB, tables at 419 MB, spares 6 -> 4, impact 216, expiry 0, arming 15, wheel, and full auto. The release zip is named v3.4.14 and the script inside matches. `v3.4.9` has not been confirmed as a playable gun. `v3.4.5` is the build that wrote 216 onto SAFE impact and expiry and still detonated at the feet. `v3.4.4` is the earlier log that first showed the clone and a gun at 4/4. `v3.4.1` added the capped spare-magazine tail and still used `locate_keyed`, so +8 read 0. `v3.4.2` uses the end of the magazine index and confirmed `spare magazines 6 -> 4` (SKILL.md section 4). `v3.4.3` accepted the explosion tail (`count=422`, `tail 3640`) only after the warhead copy and left the pistol blast. `v3.4.4` clears the applied flag and reclones. Do not treat v3.4.3 as the build still waiting on a mission. The Arsenal label and manifest `Name` are `JAR-5 Dominator - Rechambered v3.4.14`; do not rename the folder (its `_AR` suffix is the live path). Regular (the v3.3.5 gun: 380 m/s, 532 m, arming 12 m, recoil ×1.20, pistol blast) is the default Ballistics suboption. Realistic, as confirmed on v3.4.10, is 450 m/s, 360 m, arming 15 m, recoil ×0.60, spread +1, 4 spare magazines, and impact explosion 216 with expiry 0 after the tail-hash copy (SKILL.md section 9). v3.4.7's pistol explosion 388 is the earlier confirmed dud, not the current blast. A settings-row clone alone is the black-square build. Both patches use the same addon id. Manifest `Name` is `JAR-5 Dominator - Rechambered v3.4.14` (hyphen, no colon). The colon form is not a Windows folder; HD2 Mod Manager uses `Name` as the storage directory. The zip stays flat. Do not copy into a suffix remembered from this file: `hd2a_data.json` `path` is the live folder. Firing Sound is its own top-level option, pick-one, independent of Ballistics.
- Exosuit Rebalance, addon `mods/recon/exosuit_ammo`, source `hd2-mods/exosuit-ammo/exosuit_ammo.lua`, Arsenal folder suffix `_AR269359`. Not for public upload.
- M-1000, addon `mods/recon/m1000`, source `hd2-mods/m1000/m1000.lua`, Arsenal folder `m1000_combined`. Not a Nexus upload.
- Realistic Weapons v1.1, addon `mods/recon/realistic_weapons`, uuid `7c1e5a42-6b08-4d3f-9e77-1a4b8c2d6f50`, source `hd2-mods/realistic-weapons/`. One scanner. The checkboxes are `mods/recon/realistic_weapons_{onetwo,arbitrator,adjudicator,evictor,mg206}` and do not scan. Read the live folder from `hd2a_data.json`. The suffix was `_AR737561` later the same day.
- Dixie Horn, uuid `29c07aae-f32a-41db-a921-cf7f61c86fe1`, source `hd2-mods/dixie-horn/`. Wwise bank, not Lua. The folder name still contains Nexus mod id 15084. `nexusData` was set to `null` on both records on 2026-10-01.
- Mech Part HUD v1.13.0, addon `mods/recon/mech_part_hud`, uuid `1fb3e783-e499-4d32-85d4-48251e1576e9`, source `hd2-mods/mech-part-hud/`. Read-only. It does not write health or ammo, so it is not a second writer next to Exosuit Rebalance or DRIVER HUD. `nexusData` is null. Zip `hd2-mods/mech_part_hud_v1.13.0.zip`. Do not import that zip over the installed uuid. The folder name may still contain Nexus id 16514; that is not the link.

## Glyph-atlas labels (Mech Part HUD, 2026-10-01)

Drawn strings were `title.cn` and the destroyed literal. `zones.lua` `zh=` was never read. `render_mech.lua` `D.ZH` was unused. `arm_labels` was passed into `draw` and never read there.

Big charset before the English rebuild: `0123456789%-/EXO5` plus the CJK set. Small charset: `0123456789%-/损毁`.

Panel width 170. At 13px, room beside `EXO-49` and `100%` was 87.1px with Noto Sans Regular. `EMANCIPATOR` was 89.7 and did not fit. IBM Plex Sans Condensed Regular left 91.1px of room and the name was 79.5. Paths: `/usr/share/fonts/truetype/ibm-plex/IBMPlexSansCondensed-Regular.ttf` and `IBMPlexSansCondensed-Bold.ttf`. Small `DEAD` at 9px bold was 21.8px.

`gen_art.py` regenerates `src/art.lua`. The geometry before `["fonts"]`, starting at `return `, was 8192 bytes and matched the previous art. Shipped nicknames: PATRIOT, EMANCIPATOR, LUMBERER, BREACHER. Destroyed reads DEAD.

After the patch copy, the live folder still had the Chinese README (5148 bytes) and `Source/src/art.lua` (189987 bytes). Unzipping the new package over that folder replaced them. v1.13.0 deleted `LICENSE-NOTO-CJK.txt`. A UTF-8 scan of the v1.13 zip found no CJK.

A spatial arm link is kept. `if AR.spatial then AR.list=nil` rediscovered every poll (default 0.25s) and walked the Health-owner table. `spatial_validate` only re-samples positions of the suits already in the snapshot. `Arms.verify` bulk-reads the entries blob and the descriptor pointers. v1.13.0 rechecks positions every poll, calls `Arms.verify` every 5 seconds, and drops the list immediately when the error contains `SPATIAL_` or the seated suit changes. A new suit is not in the old snapshot, so the 5-second walk stays. Do not put the every-poll wipe back.

`python tools/build.py` imports `lupa.luajit21` and fails with `ModuleNotFoundError`. `tools/archive_writer.py` `archive()` does not. Lua type is still `0xA14E8DFA2CD117E2`. The assembled source starts at byte 200. The literal `HD2-Addon` is at 203 because the line begins `-- `.

## Overlaps

Removed 2026-10-01. The folders were moved to a `_retired/` area. They were in `modsLibrary` and not in the active profile:

- `mods/recon/exo45_ammo` — Patriot Ammo v1 and v1.1, same addon id, two folders
- `mods/recon/lumberer_ammo` — Lumberer Ammo v1 and v1.1, same addon id, two folders

`mods/recon/exosuit_ammo` still writes those magazine capacities. Do not put the ammo mods back.

`mods/recon/exo45_armor` (the standalone Exosuit Armor +1 fork) writes the same armor fields that are now folded into `exosuit_ammo`. Do not install the standalone `exosuit_armor_v*.zip` alongside the merged Exosuit Rebalance — it double-applies (+2 armor instead of +1). The merged mod is the single correct writer.

M-1000 is one mod, `m1000_combined`, addon `mods/recon/m1000`. The old AP4 and free-movement Lua were one scanner with opposite `*_done` flags. SUPER-GUN and AA sights stay binary options. The enabled suboptions at the merge were Crysis Hurricane Minigun and vanilla muzzle flash.

The separate SHODAN tuners (`mods/shodan/arbitrator_tuning`, `adjudicator_tuning`, `evictor_tuning`, `mg206_tuning`) are not the writers. Realistic Weapons v1.1 replaced them with `mods/recon/realistic_weapons`.

## Tables verified against game data

To find a component type you have not patched before, do not grep the on-disk `data/game/dl_library.dl_typelib` — it is encrypted (readable strings are garbage). The type names are compiled into the filediver binary. To list them, use a BROAD pattern — `'[A-Za-z]+ComponentData'` misses half the type library, e.g. `WeaponDataComponent` (no `Data`), `SpreadInfo`, `SensorEyeComponent`, `DamageInfo`, `ProjectileSettings`:
  `strings /tmp/filediver/filediver-cli/filediver | grep -oE '[A-Za-z_][A-Za-z0-9_]*(Component|Settings|Data|Info|Weapon|Attack)'`. The LDLD type hash in memory is `dlsum(type_name)` — djb2-add minus 5381, written out verbatim in the GL-15 Evictor Ammo Selector mod (codex) and verified against every hash we know:

```lua
-- djb2, the Data Library type hash. Verified 2026-10-05 against all 8 known
-- hashes (WeaponMagazine 0xFB8D88A3, DamageSettings 0xE0A72CF0,
-- ProjectileSettings 0xBD4042C2, HealthComponentData 0xB3915DE3,
-- WeaponData 0x88E4DBB1, ProjectileWeapon 0x45171B68,
-- ExplosionSettings 0x2AEA2592, WeaponRounds 0x66081072).
local function dlsum(name)
    local result = 5381
    for i = 1, #name do
        result = (result * 33 + name:byte(i)) % 4294967296
    end
    return (result - 5381) % 4294967296
end
```

Python equivalent: `r = 5381; for c in name: r = (r*33 + ord(c)) % 2**32; return (r - 5381) % 2**32`. This is how a new, never-patched component type's hash is computed from its name instead of trusting a remembered value.

**Reverse lookup (hash → name).** Given only an LDLD type hash, name it by computing `dlsum` over every candidate type name extracted with the BROAD pattern above and matching the hash — don't trust a remembered string. Verified 2026-10-05: this resolved the enemy-attack schema, which had been recorded only as hashes — `0xd25fc7f7` = `WeaponDataComponent` (the enemy counterpart to player `WeaponDataComponentData` 0x88E4DBB1, same 1232 stride), `0xf916ed4b` = `SpreadInfo`, `0xb4789330` = `SensorEyeComponent`, `0x260cbe2b` = `DamageInfo` (rooted at DamageSettings 0xe0a72cf0). These enemy-attack component hashes are TYPE NAMES, not top-level LDLD table keys: the enemy archetypes they live inside are keyed hash tables that only load in-mission, so a census scanning for `0xd25fc7f7` as a standalone table finds nothing (see `references/memory-census.md`, verified 2026-10-06 with a 326-type in-mission census).

The same binary also embeds the datalib Go **struct field names** as json tags, so
an unknown field is discovered the same way — this is how impact sound was traced:
`strings filediver | grep -oE 'json:"[a-z_0-9]+'` lists field names, and
`strings filediver | grep -iE 'ProjectileSettings|PhysicsImpact|SurfaceImpact|Explosion'`
lists struct/enum names (`PhysicsImpactEffectComponentData`, `PhysicsImpactEffectInfo`,
`SurfaceImpactSetting`, `ExplosionSettings`, `SurfaceImpactType_*`). Use the field
names to name an offset you are reverse-engineering before trusting it. Impact
effects are a SEPARATE lookup, not a projectile-record field: the projectile only
stores `surface_impact_type` / `ricochet_impact_type` enum indices; the sound,
camera shake, and decal live on `PhysicsImpactEffectInfo` (`audio_effect_id`,
`camera_effect_id`, `shake_effect_id`, `decal_sheet`, `quake_effect`, `effect_type`).

WeaponMagazineComponentData type `0xFB8D88A3`, stride 160, payload 52000 on the 2026-10-12 live block. 8640 bytes is the `2 * live` false boundary (271 strides fit after it); the index continues to the first row with `pad ~= 0` or `slot > 100000` (548 rows that session). Dominator slot 220 at that end is `0, 0, 15, 4, 6, 6`. Exosuit capacity on this stride is +136, then +140 magazines, +144 refill, +148 max, +152 threshold. Exosuit anchors on vanilla capacity plus magazines 0, refill 6, max 0, threshold 0, except the autocannon branch skips the max check. Dominator spare fields are +16 and +20, not those slots; the write rule is SKILL.md section 4.

ProjectileWeaponComponentData type `0x45171B68`, stride 616, projtype at +0, weapon function projectile at +576 (`weapon_function_projectile_type` — the programmable-ammo alternate round). Patriot entity hash `0x08F6089289C83D22`. Used for the MG-206 round swap (148 to 275), not for magazine size.

WeaponDataComponentData type `0x88E4DBB1`, stride 1232, keyed by weapon entity. The Dominator's entity hash is `0x80F1A156D9FA1E36` (lo `0xD9FA1E36`, hi `0x80F1A156`) — the SAME value as its network-descriptor resource, verified against SHODAN's WEAPONS catalog. `0xB6AFF2195568767F` is the R-36 Eruptor, not the Dominator. Holds recoil (drift +0/+4, climb +28/+32) and the weapon-function selector `function_info` at +184 (left) / +188 (right), u32 enum: none=0, zeroing=1, rate_of_fire=2, magazine=4, fire_mode=5, muzzle_velocity=7, programmable_ammo=8.

**Deriving the entity hash instead of hardcoding it (build-resilient keyed lookup).** The wheel / fire-mode / recoil / trait writes all key off the weapon entity hash. Hardcode it and a build that reshuffles entity IDs silently kills all of them while the warhead swap (keyed by `ProjectileType` + record content) keeps working. Derive it:

1. Find the weapon's own ProjectileWeapon record by its content-stable projectile type — walk the 616-byte records for the one whose `+0` (default projectile) equals the Dominator's verified `ProjectileType` (the value the warhead matcher already pinned, stored as `state.dom_type`), not by the entity hash.
2. Read the entity hash back out of the bucket entry that points at that record: each 16-byte bucket entry is `{lo u32, hi u32, slot u32, pad u32}`; find the entry whose `slot` equals the record index, and take its `lo`/`hi`.
3. Use that derived hash for the WeaponData (`locate_keyed`) and LoadoutEntry lookups. Keep the hardcoded value only as a diagnostic seed; log when the derived value differs ("build moved it").

Ordering: `wscan_block` can hit WeaponData / LoadoutEntry before ProjectileWeapon. Stash those tables (`pending_wd` / `pending_le`) when the derived hash is not ready, and resolve them from `drain_pending()` — called at the end of the ProjectileWeapon resolve — once the hash is derived. Define `resolve_wd_table` AFTER `recoil_apply` (it calls it; a forward reference to a later `local function` is a nil global, section 9).

ProjectileSettings type `0xBD4042C2`, record stride derived at runtime (hint 272). Dominator ProjectileType 177. This is the warhead and ballistics table. Projectile field offsets (Dominator `OFF_*`): mode label +12 (u32 localisation id), mode icon +16 (u64 resource, little-endian), speed +32, mass +36, drag +40, gravity +44, simulation steps +48 (u32), lifetime +52, lifetime randomness +56, damage type +60, explosion on impact +144, explosion on expire +156, arming distance +160. Before writing mass, check it against the bore. A 15×100 mm tube is about 17.7 cm³, so 178 g averages about 10 g/cm³: a solid slug with no cavity left for propellant. The stock 100 g shell is the realistic mass. "180 grain" on the 1960s Gyrojet is 11.6 g, not 178 g, and the census count of 178 unreferenced projectile types is not a gram value. Impact-visual offsets (the Dominator `VISUAL_FIELDS`, present on every projectile and identical across the 15x100mm family): disintegration effect +112/+116 (u64 lo/hi, zero on the 15x100mm rounds), decal size +164, surface impact type +168 (u32 enum, =4 on the Dominator and P/40-K), ricochet impact type +172 (u32, =3), effect damage type +220.

DamageSettings type `0xE0A72CF0`, stride 76 — the damage/durable/AP/force records. A distinct **settings-array** shape, not the hashmap (WeaponMagazine) or bucket-array (ProjectileWeapon) shapes: LDLD header (24 bytes), then a `{u64 ptr, u64 count}` pair at header+24. The record array is at `ptr` when `ptr > 0x10000`, else at `header+24+ptr` (relative). Record: id +0, damage +4, durable +8, ap_direct +12, ap_slight +16, ap_large +20, ap_extreme +24, demolition +28, stagger +32, push +36 — all u32. Identify a record by the full 9-field vanilla signature, never by id (values recur and the id is not stable). Detect "already patched" by counting records that already match the target signature against a known baseline (the EAT-17 profile already exists exactly once in a vanilla game). The exosuit EAT-17 rocket buff (1250/1250 AP 6/6/5/0 -> 2000/2000 AP 6/6/6/3) uses this.

HealthComponentData, type hash `0xB3915DE3` (dlsum("HealthComponentData")), record stride 22096 (0x5650), 502 records, hashmap 1002 slots, data at +16032. The exosuit armor + health table. Record layout:
  +0    main health (hull 1800)
  +64   default zone (a zone header: armor +216, max-armor +224, health +232)
  +520  zone array, 38 zones of 552 bytes (zone armor +216, health +232)
Real mech body zone health values: 400 (cockpit/hips), 550 (legs), 10 (lights). Body default-zone armor is 4. Arm components (main health 800, one zone of health 800) have default-zone armor 3. The record array address cannot be derived from the LDLD header; find it by scanning memory for the health values 1800/550/800.

Value-scan pitfall (this caused a game crash): matching only "main health 1800" (or "+280 == 4") writes armor into unrelated data. A value-scan MUST require the full signature before writing — main health 1800 AND default armor 4 AND at least one zone with a known health (400/550/10) — then write only the confirmed zones. "+1 to all armor" needs this; a plain "raise AV3->AV4" was safe because it only wrote exact value 3 with exact health 550/800.

Close-range bounce, tested 2026-10-01 and reverted. None of these writes are in the shipped Lua. `v2.6` only changed the `REVISION` string for the sound release:

- Offset 176 `max_ricochets`, stock 1. Writing 0 makes an unarmed hit detonate. The arming toggle still logged (`12.0 m, ricochets 0` vs `0.1 m, ricochets 1`).
- Offset 180 `ricochet_threshold_angle`, stock 83 (`0x42A60000`). Writing 180 and writing 0 did not stop tree or rock deflections. The log showed the new angle.
- Offset 136 is `explosion_threshold_angle`, stock 80 (`0x42A00000`), not the 83° field. Writing 180 changed nothing. Both 136 and 180 are `layout_ok` anchors. A write the checker does not allow fails `maintain` and reverts.
- Square ground hits were already eaten. Trees and rocks still deflect. Those two angles do not control that split. Do not retry these three writes.

Cremator flame binary patches: type hash `0xa8193123526fad64`, baked addon hash `0xe3d15622a42863c4`. Two identical files cover the Lumberer flame and the FLAM-40 sentry flame.

## Wwise bank swap

Re-list banks after a game update. If `filediver` is not on PATH, the xypwn/filediver v0.7.57 CLI is a static binary. Do not scan `Helldivers 2/data/bundles.*` (about 25 GB) until that list is empty:

```bash
filediver --gamedir "$STEAM/steamapps/common/Helldivers 2" \
  --list-format '%N %T' --include '*frv*' --types wwise_bank
```

filediver extraction flags: `--audio-format wwise` writes the raw `.bnk`; the default `ogg` decodes each WEM to a separate `.ogg` (use for listening/measurement). `-T strings -i '*'` extracts the game's localization as `.strings.json` (Key/Value pairs) — grep for a weapon's display name (e.g. `Bolt Pistol`) or designation (e.g. `P/40-K`). filediver knows only ~36% of filenames; a hashed bank still extracts by `-i '*<knownname>*'` once it is listed.

**Measuring firing-sound loudness (the "first shot is much louder" report).** The WEMs are Wwise Vorbis; ffprobe/ffmpeg cannot decode them (`codec_name=unknown`, but ffprobe still reads sample rate/channels). Decode with vgmstream, then measure with ffmpeg's volumedetect:
```bash
# no sudo: prebuilt static CLI from the release zip
curl -sL -o /tmp/vgms.zip https://github.com/vgmstream/vgmstream/releases/latest/download/vgmstream-linux.zip
cd /tmp && unzip -o vgms.zip vgmstream-cli && chmod +x vgmstream-cli
/tmp/vgmstream-cli -o out.wav in.wem        # decodes Custom Vorbis -> float WAV
ffmpeg -i out.wav -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume'
```
To isolate the actual fire reports, diff `DIDX` (the WEM id/offset/size index) across banks: the Dominator's four firing banks share all 249 WEM ids, and only 21 differ — those 21 are the fire samples; the other 228 are byte-identical shared sounds (mechanical clicks, reverb tails). Measure only the differing ids. Per-bank mastering is why the report is SM2-specific: Space Marine II's fire WEMs peak at 0.0 dB (full scale) while Boltgun/Darktide/Necromunda peak at -2.8 to -4.2 dB.

**To quiet a hot bank, splice a quieter pre-encoded WEM — do not re-encode.** Wwise Custom Vorbis has no open-source re-encoder: vgmstream decodes only, wwiser "can't modify banks", and ffmpeg/libvorbis emit standard Vorbis the game won't accept. These firing-sound mods are made by *splicing already-encoded WEMs from the donor game*, not by re-encoding — the WWSC source bank is byte-identical to the shipped one, with only the 21 fire WEMs swapped. The hot first shot is not in the donor's source either: SM2's own fire WEMs peak around -10 dB, so the 0 dB hotness was introduced during the splice. The fix is to splice a quieter fire WEM from the donor's files. Donor-game access: another Wwise game's `.pak` files are ZIP archives; weapon audio is `sounds/desktop/wpn.zip` (the WEMs) + `wpn.bnk` (the bank), and `sounds/memory_info.json` maps each WEM id to a readable name (e.g. `SFX/wpn/bolt_pistol\bolt_pistol_shoot_attack_02.wav`). SM2 ships fire in layers at different levels (attack ≈ -10 dB, bolt cycle ≈ -14 dB, tail ≈ -3 dB), so a quieter variant exists. Splice re-keys the WEM ids, so match by decoded content, not id.

**The splice path can be blocked even when a donor game exists.** For SM2 it
failed: none of the donor's source fire WEMs matched the shipped fire WEMs above
0.39 cross-correlation (the author layered/composited the fire report), so there
is no clean quieter pre-encoded WEM to splice in. When no quieter Vorbis WEM
exists, the options are (a) accept a different bank as default, or (b) re-encode
to PCM (below). Do not keep hunting for a matching source WEM once correlation is
below ~0.4 — the bank is a composite, not a re-encode of one source.

**Rebuilding a `.patch_0` bank after re-encoding a WEM (verified 2026-10-06).**
Swapping in a *resized* WEM (PCM re-encode, or any length change) requires
rebuilding the container, not copying the old header. Container layout, in order:
`BKHD` @ 320, `DIDX` @ 372 (WEM id/offset/size index), `DATA` @ 3368 (the WEM
audio payload), `HIRC` (event/gain graph, after DATA), then a 57-byte footer
holding the bank name (`content/audio/wep_jar5_dominator`). Three header length
fields are content-dependent and go stale if only the WEM bytes change:

- `+192` = `DATA_size + 58344`
- `+232` = `file_size - 48`  (the file-size field)
- `+308` = `DATA_size + 58328`

`DATA_size` is the DATA payload length, `file_size` the whole file. The `58344` /
`58328` constants are for the Dominator firing-bank shape (249 DIDX entries); for a
different bank `+232` still holds and the other two are `DATA_size + C`, reading
`C = field - DATA_size` off a fresh bank. Rebuild order: re-emit DIDX with
recomputed offsets (offsets are relative to `DATA+8`), re-emit DATA, then
recompute the three fields; HIRC and the footer stay byte-identical. Verify before
handing over: DIDX entry count unchanged, HIRC byte-identical to source,
contiguity (`DIDX` ends at `DATA` start, `DATA` ends at `HIRC` start), and
vgmstream reads a replaced WEM back. (Verified 2026-10-06 across all four
Dominator firing banks; the SM2 bank rebuilt 2454160 → 5110495 bytes with PCM fire
WEMs and passed all four checks.)

**The WEM `hash` chunk is content-dependent and is NOT MD5/SHA1.** Each WEM has a
16-byte `hash` chunk; it differs across banks, but MD5 (payload and whole-WEM),
first-16-of-SHA1, and MD5 of a `fmt`+`data` slice all failed to reproduce it. When
re-encoding a WEM, preserve the ORIGINAL `hash` bytes verbatim rather than trying
to recompute them — the algorithm is still unidentified. If the game rejects the
result, this chunk is the prime suspect.

**PCM is a fallback when no quieter Vorbis WEM exists (game acceptance
unverified).** Decode the fire WEM with vgmstream, apply gain to the PCM
(e.g. -3 dB = 0.708×), and rebuild the WEM as a RIFF/WAVE with a `fmt ` PCM16
chunk + the preserved original `hash` chunk + the `data` chunk. Structurally this
verifies (vgmstream reads it back as 16-bit PCM, HIRC unchanged), but whether the
game ACCEPTS PCM in a slot its HIRC/DIDX declared as Vorbis is untested in-game.
Treat a PCM bank as an experiment the operator must test in-game; keep the Vorbis
banks as the rollback.

Per-weapon event ids (verified 2026-10-05): the Dominator's firing bank `content/audio/wep_jar5_dominator` has 249 WEMs and 16 HIRC type-4 event ids; the shipped "Space Marine II" bolter bank has the SAME 16 event ids and 249 WEM ids (full-bank swap works because only the WEM audio differs). The broomhandle sidearm bank has 193 WEMs and 14 DIFFERENT event ids — zero overlap — so it cannot be swapped in for the Dominator. To give weapon A weapon B's report, splice B's "fire" WEM into A's bank and keep A's HIRC.

On 2026-10-01 that list was `content/audio/vehicle_frv`, `content/audio/wep_frv_heavy_flamer`, and `content/audio/wep_frv_supply_autoturret`. The M-102, M-103 Supply, and M-104 Incinerator share `vehicle_frv`, and that bank holds the horn. The other two are the weapon banks. Do not ship a second copy of the horn bank per vehicle while this is still true.

The 2026-08 Dixie patch was a full-bank replace. Against that day's vanilla `vehicle_frv.bnk` it was missing event id 3058490728 and 32 WEM ids. Horn WEM 761194215 was 29636 bytes vanilla and 407654 bytes in the Dixie RIFF. The rebuild keeps vanilla BKHD and HIRC, replaces that WEM, and pads each WEM to a 16-byte boundary.

Dixie container, measured on the pre-rebuild patch: magic `0xF0000011`. `BKHD` starts at 320. After HIRC the tail is `content/audio/vehicle_frv` plus padding. The three content-dependent length fields are at `+192`, `+232`, and `+308`; recompute all three from `DATA_size` and `file_size` (see "Rebuilding a `.patch_0` bank" above), not just offset 308 — `+308` is `DATA_size + C`, not the total file length. Do not use the Lua size fields at `0xA0` and `0xC0`. The zip root is `manifest.json`, `thumbnail.png`, and `9ba626afa44a3aa3.patch_0`, with no Options key and no `Addon/` folder. `Guid` is the installed uuid.


## Reusable constants (cross-confirmed 2026-10-02)

- `0xFB8D88A3` dlsum("WeaponMagazineComponentData") — magazines/ammo.
- `0x45171B68` dlsum("ProjectileWeaponComponentData") — projtype at +0, programmable-ammo function projectile at +576.
- `0x88E4DBB1` dlsum("WeaponDataComponentData") — recoil and `function_info` selector at +184/+188.
- `0x4F2CF417` dlsum("LoadoutEntryComponentData") — armory trait labels (five localization string IDs at +12; 386 index rows of 16-byte `{resource u64, record u32, reserved u32}` then 193 records × 32 bytes). Keyed by resource hash (== entity hash for the Dominator).
- `0xE0A72CF0` dlsum("DamageSettings") — the damage-type table (Dominator reads damage/durable/AP from it; LAS-98 and MS-11 patch it).
- `0xB3915DE3` dlsum("HealthComponentData") — exosuit health + armor.
- `0xC6A4A7935BD1E995` MurmurHash64A multiplier; the low 32 bits `0x5BD1E995`. The packer (murmur64a addon-id hash) and the EXO Stratagem Launcher both use it.
- `0x6AB3B43F` a game.dll layout anchor seen in Armored Overhaul, Field Repair, and the Mech Part HUD's game.dll identity pair (6AA96B14/6AB3B43F). Not a table type; a build/layout check.
- Config-file pattern: read `%LOCALAPPDATA%` key=value overrides at load so tunables change without repacking. Dominator `read_overrides` is the example. A value that can be a string sentinel (`speed=off`) must be matched against the literal BEFORE `tonumber` — `tonumber('off')` is nil, so a numeric branch checked first silently drops the sentinel and leaves the field on its default.
