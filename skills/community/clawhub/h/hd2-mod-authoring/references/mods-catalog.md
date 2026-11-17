# Mod catalog (scanned the mods archive, 2026-10-02)

Classification of every archive, by addon id and kind. "Maintained" = kept in the source tree; "mined" = read for a technique; "cataloged" = classified, addon id recorded.

## Maintained (worked examples)

| Mod | Addon | Kind |
|---|---|---|
| JAR-5 Dominator: Rechambered | mods/dsh/dominator_bolt_pistol | lua |
| Mech Part HUD | mods/recon/mech_part_hud (was mods/arena_local/mech_part_hud) | lua |
| Exosuit Rebalance (ammo + armor + EAT rockets) | mods/recon/exosuit_ammo | lua |
| Exosuit Armor +1 (folded into Exosuit Rebalance; do not install separately) | mods/recon/exo45_armor | lua |
| M-1000 (AP4 + free movement) | mods/maxigun/ap4_public, mods/maxigun/free_movement_public | lua |
| Realistic Weapons v1.3 | mods/recon/realistic_weapons (flags: mods/recon/realistic_weapons_*) | lua. Entity hashes derived from a projectile fingerprint, not hardcoded. Seed hash is a drift log only. |
| Dixie Horn | (Wwise bank, no addon id) | wwise_bank |

The SHODAN tuners (mods/shodan/{arbitrator,onetwo,adjudicator,evictor,mg206}_tuning)
are the pre-merge Realistic Weapons; retired.

## Third-party, mined for a technique

| Mod | Addon | What it gave us |
|---|---|---|
| SHODAN Stat Editor (github SHODAN-HORAI) | mods/shodan/stat_editor | cross-confirms projectile velocity at +32, type 0xBD4042C2, stride 272 (== Dominator OFF_SPEED); writes only on edit/start/map-reload, no re-assert loop |
| JAR-5 Buff Pack v2.12 (joelc) | mods/joelc/jar5_buff_* | fire modes are a u32 enum array (primary +144, secondary +148, tertiary +152) in the weapon's OWN WeaponData record, NOT a separate ~144-byte record — its `[3,2,3]` fingerprint is the Buff Pack's POST-EDIT state (secondary already Burst=3), not stock `[3,2,0,0]`; reload is a passive stat (type 0x63CE0FEB, stat id 13, f32 1.36) repointing every armor passive block, not a weapon field. Damage/AP/speed patches cross-confirm DamageSettings 0xE0A72CF0 (damage +4, AP +12) and ProjectileSettings 0xBD4042C2 (speed f32 +32, name_upper +4 = 0x1E2FAF6F). NOTE: uses the OCLAW_UPDATE_BUS dispatcher — same attribution/JIT caveat as Realistic Weapons (SKILL section 7); heavy full-address-space scanner |
| EXO-45 Patriot Buff | mods/rexsybimatw/exo45_patriot_buff | HealthComponentData layout + byte-edit pattern |
| Exosuit Heavy Armor | mods/recon/exo45_armor | HealthComponentData value-scan + identity guard |
| DRIVER HUD 1.5.1 (installed) | — | network/inventory offsets for the equipped-weapon read |
| TacticalCombatOverhaul v2.6.13 (rojo) | mods/rojo/tco_core, tco_run_n_gun, tco_melee, tco_shellshock, tco_slippery_when_wet + Shared | Reread 2026-10-07, every source Lua. Live copies, not table writes, for stats the game copies at spawn: reload is WeaponReloadComponentData 0x991D454E stride 80 +56 (attachment component 113 in 0x683E604F). Ergonomics +356 on 0x88E4DBB1 was written on live copies and on the spawn row and still did not change handling in hand — derived at weapon build; they removed the feature. Do not treat +356 as a live handling field. Their working reload search is 1 ms/frame, 16-byte immutable needle, full-row signature with mutable words excluded, hot regions first (2.6.13 starts every new weapon hot-only). Settings pages are often PAGE_READONLY: write_protected VirtualProtects only the target range, writes, readback, restores the old protection. Optional SHODAN_EDITOR_HUB v1 register {searching,wants,handle,after_pass}; if the hub appears after a fallback scan that has not written, discard the fallback and rejoin. Status effects resolved by name (StatusEffectInfo stride 152, name ptr +8), not enum id — id 5 on this build is not Hallucination. Carrier must have zero damage/template refs and an empty presentation; clone only the Confusion visual block. Mod Options Menu silently drops a mod past 32 options (Core shipped defaults until they cut to 32). Input-record writes do not drive movement (Strafe Lock: 334 writes, angle stayed ~48°). Climb flag controller+0xf8c bit 0x200 also rises on melee lunges. Shared composes avatar fields by provider order instead of last-writer-wins. |
| WarbondDesk (warbond_desk) | mods/warbond_desk/main | NATIVE CODE patching: x64 byte-signature scans (hex + mask + anchor + reference_offset + kind="code") locate and patch game .text instructions, with image_base_offset/table_offset/table_count to resolve RIP-relative tables from code. A technique entirely different from value-table patching |
| Bolter-Jar Dominator (david_hogins) | mods/david_hogins/bolter_jar | the Dominator rechamber done via HD2Runtime typed API (`hd2.options` menu + `require('mods/skyeshade/hd2runtime')` + explosion-demolition choice) — confirms the typed route for our exact use case |
| Wrench-Repair 1.3.0 (ymir) | mods/ymir/entrenchment_repair | Reread 2026-10-07, full Lua + tests. HD2Runtime 0.28.1: require_runtime, local_player, equipped_weapon, events.on('entity_damaged'), in_mission, every(0.05). Contact is post-damage, not a hit hook: local_attacker + recent attack + descriptor recheck + health unchanged since the event, else refuse. Health is two copies — manager record +0x14 AND SyncedHealth rep (next hit is computed from the rep); if the second write fails, stop the session. Re-resolve the component index immediately before the write (arrays compact). Sentries heal through prologue-pinned AddHealthFraction (game+0x91E920) after raising max to 3x base, not a raw poke. FX-12 shield charge is a float + native sync (game+0xFD97E0, field 0x1AD6D70F), also prologue-pinned; layout byte pins idle the feature if the build moved. PE timestamp/size/checksum of game.dll+exe must match build 25480438 or the mod stays idle. Shovel damage row is patched only when the allocation is unique and the 76-byte row is still BASELINE or AP_ONLY (damage 2/2, AP 4). Dead zones (health 0) are not revived. Zone-only contacts (no entity_damaged) need a real zone drop plus last-creditor == local peer. Arm-to-exo link is proximity with a tie refusal. Shovels 7E1F76163C667E4B and E85E623F93F96FB3. Model options are separate Includes (Addon + Models/Red or Yellow, or Addon only). |
| Support Side Holster 2.6.1 (local) | mods/local/holster_* (67 addons) | multi-option architecture: dozens of tiny 200-byte addons each set one weapon hash in a shared `_G.SupportHolsterOptions` table, one big worker reads them |
| FirstPerson v2.9 (jim) | mods/jim/first_person | stingray camera repositioning (head node + offset, sr.Vector2/Vector3, ActionCam-style); no stat memory writes |
| SmoothBoot 3.0 (codex) | mods/codex/smoothboot | a rule engine that re-heads the Bingus mod chain, throttles per-mod (trip_ms circuit breaker), attributes errors by chunk name — meta-infra, not game data |
| Overdive v1.0 (hd2lab) | mods/hd2lab/spawn_director | spawn-director Lua is OBFUSCATED/encrypted (only the addon header line is readable) — some mods ship unreadable payloads; can't mine technique |
| Transmog Probe (cow) | mods/cow/transmog_probe | embeds a pre-rasterized glyph atlas (rects) + geometry probe — same glyph-atlas technique as Mech Part HUD |
| Mission Reroller (ipodalexei) | mods/ipodalexei/mission_reroller* | development core with SUPPORTED_BUILD + record layouts + inspect_snapshot; no native adapter yet |
| Enemy Balance & Behavior / Gameplay Systems 1.2 (enemyov) | mods/enemyov/** (64 addons) | ENEMY ATTACK REFERENCE MECHANISM — the missing piece behind the Bile Titan bug. Enemy attacks reference projectiles through a SEPARATE enemy-weapon component `0xd25fc7f7` = `WeaponDataComponent` (stride 1232 — same stride as player WeaponData 0x88E4DBB1, but a different type hash), NOT through the player `ProjectileWeapon` (0x45171B68). Attack schema: weapon_type 0xd25fc7f7 = WeaponDataComponent (1232), spread_type 0xf916ed4b = SpreadInfo (12), component_type 0xb4789330 = SensorEyeComponent (44), damage_type 0x260cbe2b = DamageInfo (76, root 0xe0a72cf0). Type names resolved 2026-10-05 by reverse dlsum (see install-and-format.md). NOTE (2026-10-06): these enemy component hashes are component TYPES inside enemy archetype keyed hash tables (in-mission only), not standalone LDLD tables — an in-mission 326-type census found none as top-level tables. Enemy actors are keyed by 32-bit hash (e.g. bile-spewer head 0x8c5570c9, resource 0xccae5264acd591b7) with named zones; HealthComponent zones carry armor at +216 (matches our exosuit armor offset). Uses a native-code-patching framework (RIP-relative memory resolution + code disassembly) — same class as WarbondDesk |
| GL-15 Evictor Ammo Selector (working) | — | hand-rolled programmable-ammo reference mod for the Evictor |
| Super-Earth Armory Forge (community) | mods/community/passive_picker_v4 | passive-picker UI |
| Weakpoint LockOn All-in-One | (19 binary) | enemy weakpoint targeting — binary patches, not Lua (type 0xe0a48d0be9a7453f + 0x18dead01056b72e9) |
| GL-15 Evictor Ammo Selector (codex) | mods/codex/gl15_evictor_ammo_selector | hand-rolled programmable-ammo selector; keeps GL-15 40mm model with Pineapple explosion. SOURCE of the dlsum algorithm (djb2-add minus 5381) — copied into install-and-format.md |
| Codex Module Bridge v1 (codex) | — | COMPILED bytecode (not source); bridges mods/codex/p11_self_heal + constitution_bolt_amr via require |
| P11 Self-Heal (codex) | — | COMPILED bytecode; stim-pistol self-heal via RPM/WPM |
| homing stim (stim_homing) | mods/stim_homing/acquisition_test | read-only Sony HID input reader (DS4/DS5 report decode, no hooks/emulation) |
| HD2 Transmog Helmet Passives | mods/hd2transmog/foundation | pure domain module — no memory/FFI/hooks; ownership from the authoritative owned-kit list only |
| Objective Tracker | — | payload unreadable — not source (`-- HD2-Addon:` absent) and no readable string constants seen; not verified as compiled bytecode vs binary |
| GL-15 Evictor Airburst v5.4.4 (dsh) | mods/dsh/evictor_gas_airburst | the GOLD STANDARD worked example of programmable-ammo + the clone problem done RIGHT. Evictor entity hash 0x7BB953FE/0x006E4432. Reveals two new tables: ExplosionSettings 0x2AEA2592 (stride 152; named fields in the constants list below; that mod did not name the extra f32s at +24 and +32) and WeaponRoundsComponentData 0x66081072 (component, record 136; primary projectile at +64, magazine +72 f32, ammo +80). KEY GOTCHA: the weapon re-arms option 0 from WeaponRounds +64, NOT ProjectileWeapon +0. Clones projectiles/explosions into types "referenced by NOTHING" (verified by: no entity delta, not in any weapon's +0/+576 — lesson 40) — the clone is SAFE when you verify against weapon slots AND entity deltas AND enemy tables, not when you guess "dormant" from name==0 |
| Patriot Exosuit Buffs v8 (morningspire) | mods/morningspire/patriot_ap4 | AP4 on the Patriot via known tables (0xBD4042C2, 0xE0A72CF0, 0xFB8D88A3, 0x45171B68) |
| Field Repair AmmoOnly 1.2 (combat) | mods/combat/field_repair_ammo | WeaponMagazine 0xFB8D88A3 + WeaponRounds 0x66081072 + magazine-anchor 0x6AB382E4 + game.dll 0x6AB3B43F |
| Dominator-Bolt-Pistol-Round (dsh) | mods/dsh/dominator_bolt_pistol | the ANCESTOR of our own rechamber: same addon id, REVISION dbp-v1, same NAME_15X100 (0x1E2FAF6F) identity matcher + 15x100mm ballistics fingerprint. Copy-warhead-onto-Dominator with source=201/fallback=-1 + explosion override. This is our mod's lineage — the identical-id install is an either/or, not a stack |
| SHODAN tuners (arbitrator/onetwo/adjudicator/evictor/mg206) | mods/shodan/*_tuning | damage-only tweaks (70→80, 23→28, 35→50) on DamageSettings 0xE0A72CF0 stride 76 — the pre-merge Realistic Weapons; each a one-field writer |
| LAS-98 AP Ramp 1.5 (ymir) | mods/ymir/laser_cannon_ramp | config-file stage ramp (stage1-4 seconds/ap/damage_bonus/demolition) on DamageSettings; signature scan by LDLD + count 649 |
| MS-11 Solo Silo (codex) | mods/codex/solo_silo_demo50 | demolition 40→50 on the Solo Silo blast/impact — a 12-byte write on one DamageSettings row; self-detects the sibling writer's conflict |
| Smarter Guard Dogs 4.6.3 (chef) | mods/chef/smarter_guard_dogs + 12 flag addons | AI behavior — NOT a stat table edit; scans game CODE after a patch to find its addresses, then re-targets dog/sentry fire (safety, target priority, skip-impenetrable-armor). Flags are tiny addons setting a per-frame-read flag |
| HD2-EXO-Stratagem-Launcher | mods/codex/exo_launcher | MurmurHash64A (0xC6A4A7935BD1E995) — the exosuit stratagem launcher |
| Armored Overhaul 3.2.0 (chef) | mods/chef/armored_overhaul_* (40+ addons) | vehicle handling/steering/turret via entity-hash-keyed records (Bastion 0x16474112/0x801385B6, Maelstrom 0xB0C9FAF4/0xAF8903F9) + config-file + Mod Options Menu API (register_option/on_change/api=1) + game.dll 0x6AB3B43F anchor |

## Third-party, cataloged (techniques observed)

| Mod | Addon(s) | Notes |
|---|---|---|
| SHODAN Stat Editor 简体中文补丁 | mods/shodan/stat_editor_zh_cn | translation layer, NOT a stat writer: hooks Gui.text/text_extents only, zero memory writes; manifest Description is "需要在原版之后加载" (load after the original editor) |
| Armored Overhaul 2.0.1 | mods/chef/armored_overhaul_* (12 addons) | vehicle handling; config-file + loader-api; uses 0x6AB3B43F game.dll anchor |
| Field Repair (ammo only) | mods/combat/field_repair, mods/combat/field_repair_ammo | patches WeaponMagazineComponentData (0xFB8D88A3); config-file |
| Smarter Guard Dogs & Sentries | mods/chef/smarter_guard_dogs_* (11 addons) | AI behavior; config-file |
| Vanilla Plus Megapack v14/v16 | mods/cowboybingus/* (8 addons) | CowboyBingus's own; loader-api + config-file |
| GL-15 Evictor Airburst | mods/dsh/evictor_gas_airburst | function_info.left = ProgrammableAmmo (known) |
| LAS-98 AP Ramp | mods/ymir/laser_cannon_ramp | DamageSettings (0xE0A72CF0) |
| MS-11 Solo Silo | mods/codex/solo_silo_demo50 | DamageSettings (0xE0A72CF0), dlsum(DamageSettings) |
| EXO Stratagem Launcher | mods/codex/exo_launcher | MurmurHash64A (0xC6A4A7935BD1E995) |
| Casemate Turrets | (binary) | type 0xe0a48d0be9a7453f |
| FRV Anti-Flip | (binary) | type 0x5f7203c8f280dab8 |
| Bingus Shared Loader v15 | (loader) | the framework itself |
| WWSC All-in-One | (rar) | sound banks; the Dominator SM2 firing sound came from here |

## Reusable constants surfaced by this scan

- `0xFB8D88A3` dlsum("WeaponMagazineComponentData") — magazines/ammo.
- `0xE0A72CF0` dlsum("DamageSettings") — damage type table (damage/durable/AP per type).
- `0xB3915DE3` dlsum("HealthComponentData") — exosuit health + armor.
- `0x2AEA2592` dlsum("ExplosionSettings") — ExplosionInfo, stride 152. The in-memory dump's array header is 16 bytes (count u32 at +8; 422 records on the 2026-10-07 dump) and the records follow. SHODAN v2.5 sets `tail = true` and uses `parse_rows`. The Dominator `validate_block` pointer check rejects that shape; the accept rule is SKILL.md section 4. Type id is the u32 at record +0. Named fields: damage_type +4, inner_radius +16, outer_radius +20, particle_effect_path +56/+60 (u64), audio_event +64, num_shrapnel_projectiles +80, shrapnel_projectile_type +84, persistent_status_volume +100, status_volume_effect_time +104, status_volume_audio_play/stop +108/+112. HD2 Runtime's ExplosionAuthoringCapabilities names +24 `shockwave_radius` (5.0 on the bolt pistol). +32 is not in that layout. Both are meter-like across the table (medians about 8 and 30). Do not trust a wiki inner/outer pair, or a type id copied out of an old comment, until you read the live record. On this dump: type 388 (the P/40-K warhead) is +16=1.0, +20=3.5, +24=5.0, +32=6.0. The Dominator log line `explosion on impact 0 -> 388` prints this pistol row, not the id written onto SAFE (SKILL.md section 7). Type 379 is 0.2/0.5/4.0, not the 1/3.5 pair. Type 155 is 1/2/2/2.5, not 4–7 m. The Eruptor projectile (type 40) points at explosion 158, which is 4/7/8. A player who takes damage at 6 m and not at 7 m is standing in 388's +32, not in +20. If the felt edge disagrees with +20, read +24 and +32 before retuning +16/+20. Those two floats are not proven damage fields; no write has shown which one the damage check uses. Writing 388 in place also changes the bolt pistol. Cloning the settings row onto a spare slot does not bring the effect. v3.4.8's slot 216 matched 388 except +0 and +20/+24/+32, the particle hash at +56 included, and the impact drew black squares. The effect is the per-row tail u64 (SKILL.md section 9): row 216 stayed on the dead hash while +40 still pointed at the pistol's tail slot. Copy that hash onto the spare row before using the spare id. v3.4.10 did, left expiry at 0, and that play is the confirmed graphic (SKILL.md section 9). Leaving the projectile on 388 avoids the squares only when the tail hash was never copied.
- `0x66081072` dlsum("WeaponRoundsComponentData") — component record 136; primary projectile +64, magazine capacity +72 (f32), ammo capacity +80. The weapon re-arms option 0 from +64, NOT from ProjectileWeapon +0.
- `0x6AB382E4` magazine-anchor (Field Repair AmmoOnly).
- `0xC6A4A7935BD1E995` MurmurHash64A multiplier (the packer's hash); low half 0x5BD1E995.
- `0x6AB3B43F` a game.dll layout anchor (appears in multiple mods and the Mech Part HUD game.dll pair).
- The config-file pattern: `%LOCALAPPDATA%` key=value overrides read at load, so tunables change without repacking. The Dominator `read_overrides` and many third-party mods use it.
