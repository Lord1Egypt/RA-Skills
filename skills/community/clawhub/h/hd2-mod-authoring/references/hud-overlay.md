# HUD overlay and game-object state (verified 2026-10-02)

> The Dominator arming badge this file verifies was removed 2026-10-04 in favour
> of the programmable-ammo wheel (SKILL.md section 11). The wheel was briefly
> removed for the Bile Titan spit bug, then restored safely in v3.1 with the
> P/40-K's own round as the alternate. The draw-text and equipped-read techniques
> below remain valid for any future overlay; they are not retired, just no longer
> used by the Dominator.

A Bingus Lua mod can draw text on screen with the game's own font, and can read
live game-object state through the Stingray API. This is a different path from
the pre-rasterized glyph atlas (the Mech Part HUD primary renderer); `Gui.text`
renders ASCII with no bundled glyph data.

## Draw text (verified in game — the Dominator arming badge)

```lua
local sr = rawget(_G, "stingray")
local FONT = "core/performance_hud/debug"
local id = sr.Gui.text(gui, str, FONT, size, FONT, sr.Vector2(x, y), col)
-- col = sr.Color(alpha_byte, r, g, b)  -- alpha 0..255, r/g/b 0..255
-- remove with sr.Gui.destroy_text(gui, id)
```

Screen coordinates are Stingray screen space: origin bottom-left, y grows up.
`Vector2(x, y)` is the text position. Redraw only on state change; do not draw
every frame.

Do not run the heavy equipped-weapon read every second. The Dominator arming
badge first polled `hud_equipped()` every 60 frames (~1 s). That walk is
`objects_owned_by` + a type check per owned object + two hash-table walks of up
to 64 x 8-byte `ReadProcessMemory` each, plus `Application.worlds()` every ~0.5
s. The per-second main-thread hitch caused audio underruns ("sound kept cutting
out") and dropped hit registration ("center-mass shot, bot not hit"); reverting
removed it. Throttle the equipped check to ~5 s, cache the network/inventory
roots and the avatar entity, and only re-walk when the resolved resource hash
changes. A state-change redraw rule does not license a per-second state poll.

## Pitfalls that each cost a game test

- `sr.Vector2` and `sr.Vector3` are callable **tables**, not functions, so
  `type(sr.Vector2) == "table"`. A guard that requires
  `type(sr.Vector2) == "function"` silently disables the whole overlay. Check
  `sr.Vector2 ~= nil`, not the type.
- `App.worlds()` may not be dense and a second (UI) world may not exist. Iterate
  with `pairs`, try non-main worlds first, then fall back to `App.main_world`.
  DRIVER HUD states it outright: "Do not assume App.worlds is dense or that a
  second world always exists." `ipairs` + first-non-main-only can leave the gui
  never created.
- Create the gui with `sr.World.create_screen_gui(world, 'scale', 1, 1)` and
  re-create it when the world changes on map load (check world liveness each
  tick). `sr.Application.worlds` / `sr.Application.main_world` give the worlds.

## Reading game-object state: never probe unknown field names

`sr.GameSession.game_object_field(session, id, name)` with an **unknown** field
name — or an invalid object id — can hang the whole game (black screen), not
just error. Probing a list of candidate names is not safe. Only call it with a
name already known valid for this build (known names: `baegche` = avatar,
`un6y1d` = player-unit type, `state`, `motion_enabled`, `rotation_enabled`).
If a value is needed for an unknown field, read it from native memory instead.
`objects_owned_by(session, peer)` returns zero objects on the ship; the local
avatar only exists in a mission.

## Equipped-weapon read (offsets from DRIVER HUD 1.5.1; confirmed in game 2026-10-02)

The equipped weapon is not an owned object and is not a simple
`game_object_field`. DRIVER HUD reads it from the avatar inventory in native
memory. Offsets relative to the `game.dll` module base, all verbatim from
DRIVER HUD 1.5.1 (installed and working):

- `GetModuleHandleA("game.dll")` = module base.
- `0x346BF98` network root, `0x3326738` inventory root.
- Network tables: goid-indexed at `net+0xF22EC8`, entity-indexed at
  `net+0xF1AEB0`, descriptor array at `net+0xF32F18` (24-byte entries).
- Hash table header (20 bytes): entries ptr at 0, capacity u32 at 8, empty u32
  at 12, multiplier u32 at 16. Lookup: `first = mul32(key, multiplier) %
  capacity`, probe up to 64 slots of 8-byte `{key, dense-index}`.
- Descriptor (24 bytes): resource u64 at 0 (lo/hi u32), entity u32 at 8, unit
  u32 at 12, goid u32 at 16, flags u32 at 20.
- Inventory: hash table at `inv+0x28` keyed by avatar **entity** → row index;
  rows array at `inv+0x50`; rows are 48 bytes of slot entity u32s. DRIVER HUD
  reads the support weapon at row `+8` ("slot three"). The primary weapon at
  row `+0` is an inference from that layout and is not yet confirmed.

Confirmed: the primary weapon is at inventory row +0. The equipped weapon's
identity is the descriptor `resource` (u64) — for the Dominator that is
`0x80F1A156D9FA1E36` (hi 0x80F1A156, lo 0xD9FA1E36). That value is ALSO the
Dominator's WeaponData/ProjectileWeapon entity key (verified against SHODAN's
WEAPONS catalog). `0xB6AFF2195568767F` is the **R-36 Eruptor**, not the
Dominator — an earlier build keyed `DOMINATOR_ENTITY` to it and installed the
ammo wheel + recoil on the Eruptor by mistake. When a match keeps failing,
log the resolved resource on every held-weapon change and compare against it.

`ReadProcessMemory` does not hang; it returns nil on a bad read. Fail closed
(no overlay) on any nil, rather than guessing.
