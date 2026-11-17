---
name: minecraft-custom-mod-builder
description: "Minecraft Custom Mod Builder: Generate and verify structured Minecraft Bedrock, Bedrock skin pack, Fabric, and NeoForge projects. Use when an agent needs minecraft custom mod builder, create runtime verified bedrock add ons and skin packs; build and verify fabric and neoforge jars; generate typed items, blocks, entities, commands, create mod project, target platform, mod id through AgentPMT-hosted remote tool calls. Discovery terms: minecraft custom mod builder."
version: 1.0.8
homepage: https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder"}}
---
# Minecraft Custom Mod Builder

## Freshness
Last updated: `2026-07-14`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Build structured Minecraft Bedrock add-ons, Bedrock skin packs, and Fabric/NeoForge projects with strict schemas, real runtime behavior checks, File Manager visual proof galleries, async install-readiness gates, and a full test loop for agent-edited source.

## Product Instructions
### Minecraft Mod Builder

Generate deterministic Minecraft Bedrock, Fabric, and NeoForge mod artifacts from structured specifications. This tool does not call an LLM, does not accept prompts, and does not require user credentials.

#### Two Rules That Will Save You Many Retries

##### Rule 1 — One ItemSpec equals one in-game item

A single `ItemSpec` produces one in-game item. The fields `damage`, `durability`, `max_stack_size`, `nutrition`, `tool`, `armor`, `food`, `block_placer`, `entity_placer`, `enchantable`, `repairable`, `digger`, `cooldown`, `glint`, `rarity`, `dyeable`, and `component_overrides` all attach to the *same item*. A weapon does **not** need a separate entity or a separate "damage item." A sword does **not** need a partner "enchantment item." You ship one item; this tool wires up every relevant Minecraft component on that item from the fields above.

Do not split one weapon idea across many `items[]` entries. Do not duplicate a weapon and call one copy "damage" and another "durability." That is the most common source of bloated, broken submissions.

##### Rule 2 — Every visible asset requires a texture

Items, blocks, entities, particles, named texture assets, machines, storage, and skin-pack skins must each carry a `texture` with one of these three sources:

* `source_base64` — base64-encoded PNG or JPEG bytes (max 1024×1024, max 5 MB).
* `source_file_id` — a File Manager file_id for a user-uploaded image.
* `color_hex` — an explicit `#RRGGBB` color. Only `item_kind in {tool, weapon}` (with `tool_type`) and the dedicated `texture_kind in {block, entity}` paths produce a recognizable sprite (sword/pickaxe/axe/shovel/hoe; shaded block face; model-compatible cuboid atlas). For every other kind — `generic`, `food`, `fuel`, `projectile`, `block_placer`, `entity_placer`, `armor`, particles, machines, storage — `color_hex` renders only as a flat colored 16×16 square. That is appropriate for raw materials (ingots, dust, gems) but looks like a missing texture for armor/food/machines. **Use `source_base64` or `source_file_id` whenever the item's identity is visual** (armor, food, machines, storage, projectiles). Tool/weapon `color_hex` requires `tool_type`; otherwise rejected.

A spec that omits the texture binding is rejected at validation with `MINECRAFT_VISIBLE_ASSET_TEXTURE_REQUIRED`. There is no procedural blob fallback. If you want the user to see something, you supply the texture.

**Java armor inventory icons must ship a real PNG.** `item_kind="armor"` rejects `color_hex`-only textures (`MINECRAFT_ARMOR_TEXTURE_REQUIRES_IMAGE`) because that produces only a flat inventory square. Supply `source_base64` or `source_file_id` for every helmet/chestplate/leggings/boots. Declarative Java armor uses the selected vanilla iron/gold/diamond/netherite equipment asset while worn; the supplied image is the inventory icon, not a wearable UV atlas. A custom material or custom worn texture must use the agent-edited source workflow and pass client/runtime verification. Declarative Bedrock armor is rejected because a wearable item without a verified attachable would be invisible on the wearer.

##### Authoring textures with the Icon Generator + `pixelize_to`

The canonical way to author textures for items, blocks, entities, and particles is the Icon Generator (`/product-icon-generator`). Render at the exact target grid in `pixel_art_mode=true` — 16×16 for items and blocks, 64×64 for entities and skin packs — and pipe the returned `file_id` straight into this texture's `source_file_id`. Detailed recipes live in `agent_instructions/minecraft_texture_agent.md`.

When the texture originates outside the Icon Generator (AI image creator, user upload, third-party source), use the ingest-side safety net by setting `texture.pixelize_to` and optionally `texture.palette_colors`. Both fields are opt-in (`None` by default) so existing bindings remain byte-identical. Example: `{"texture": {"source_file_id": "abc...", "pixelize_to": 16, "palette_colors": 8}}` nearest-neighbor downscales the input to 16×16 and quantizes it to an 8-color palette with dithering disabled, producing crisp pixel-art output regardless of how the source was made. Failures surface as `MINECRAFT_TEXTURE_PIXELIZE_FAILED`.

Recommended defaults unless you have a specific reason to deviate: items/blocks → `pixelize_to: 16, palette_colors: 8`; entities/skins → `pixelize_to: 64, palette_colors: 16`; particles → `pixelize_to: 16, palette_colors: 4`. The `color_hex` binding path is unaffected — it already produces crisp procedural sprites.

#### Request Shape Rules

Prefer the canonical field names below. The backend accepts the listed aliases when they are exact equivalents, but canonical names make the generated schema and validation errors easier to follow.

##### Verified async builds and install readiness

Use `start_build_job` for anything the user should install. It validates the request, queues the build, and returns immediately with `task_id` and `status="queued"`. Poll with `get_build_job` using the same `task_id` until `status` is `completed` or `failed`.

`start_build_job` defaults to `verification_level="behavior"`. The completed job result includes:

* `runtime_verification` — boot/behavior/render/client checks or the exact reason verification could not run.
* `visual_proof` — File Manager–hosted PNG frames (texture enlargements, entity composites, particle sheets, and Java in-game client screenshots when the client lane runs). Each frame has `signed_url`, `file_id`, `caption`, and machine checks. Video clips are not part of this surface yet.
* `quality_gate` — `passed`, `failed`, `blocked`, or `unverified`. Visual fidelity/frame failures use `MINECRAFT_VISUAL_FIDELITY_INSUFFICIENT` or `MINECRAFT_VISUAL_PROOF_FAILED`.
* `ready_for_install` — `true` only when the quality gate passed (behavior **and** required visual proof).
* `verification_not_run` — `true` when the requested runtime checks did not execute.
* `request_classification` — `supported_declarative`, `needs_agent_code`, or `platform_constrained`.

**Agent visual review is mandatory.** Before telling a user a mod is finished, open every `visual_proof.frames[].signed_url` (or use the File Manager tool with each frame `file_id` under the same budget) and confirm the art matches the request. The same frames are also listed in `artifacts[]` with `label=visual_proof_frame`. Do not claim success from behavior checks alone. If frames show flat colored squares, missing identity art, wrong subjects, or unusable scale, fix textures (`source_base64` / `source_file_id`, not only `color_hex` for armor, food, entities, particles, machines, or skins) or edit source and re-run `start_build_job`.

Treat `ready_for_install=false`, `quality_gate.status!="passed"`, `verification_not_run=true`, or `visual_proof.status` in `{failed,partial}` on a behavior job as "fix the spec/art/source and rerun." Do not present those artifacts as working mods even if the task status is `completed`; completed only means the job produced inspectable output.

A generated `behavior` job must declare at least one concrete feature, advanced resource, or skin. Use `create_mod_project` or `verification_level="off"` for an intentionally empty scaffold; an empty project cannot be certified as a functional mod.

Use `list_build_jobs` with `limit` (`1` to `100`) to inspect recent build jobs for the current budget.

`create_mod_project` remains synchronous and unverified. It accepts only `verification_level="off"` and returns `ready_for_install=false`. Use it for fast source/debug output, not final user delivery.

Use `verification_level="boot_smoke"` only when the user explicitly wants a faster runtime-load check instead of behavior checks. Use `verification_level="off"` only for debug/source iteration and tell the user the result is unverified.

##### Agent-edited source testing

For behavior the declarative schema cannot faithfully express, generate source first, edit the code, upload a zip, then call `start_build_job` with:

```json
{
  "action": "start_build_job",
  "target_platform": "fabric",
  "mod_id": "edited_mod",
  "authoring_mode": "agent_code",
  "source_archive_file_id": "file_...",
  "source_test_mode": "test_only",
  "verification_contract": {
    "schema_version": "1",
    "target_platform": "fabric",
    "mod_id": "edited_mod",
    "user_intent_summary": "Using the edited mod marks the player as verified.",
    "expected_checks": [
      {
        "check_id": "boot",
        "description": "The edited mod boots without registration errors.",
        "check_kind": "boot"
      },
      {
        "check_id": "player_marked",
        "description": "The edited behavior adds the edited_mod_verified player tag.",
        "check_kind": "behavior",
        "assertion_kind": "tag_present",
        "target": "edited_mod_verified"
      }
    ]
  }
}
```

`source_test_mode` defaults to `test_only`; use that mode while iterating. Set `source_test_mode="test_and_package"` only when the runtime report passes; install artifacts are returned only when `ready_for_install=true`. Do not put verifier files under `.agentpmt/verification/**` into shipped artifacts.

For `verification_level="behavior"`, the contract must include at least one `behavior`, `render`, or `client` check. A contract containing only `boot` and/or `static` checks is rejected because loading and file presence do not prove requested behavior. Use `verification_level="boot_smoke"` when load-only verification is the actual goal; boot-smoke output is never install-ready.

`authoring_mode` is deterministic: `auto` and `declarative` validate the typed feature schema; `agent_code` requires `source_archive_file_id` on `start_build_job`. The service never guesses this route from keywords in a prompt.

Every edited-source check must be machine-observable. Contract assertion kinds are grouped by surface:

| `check_kind` | Allowed `assertion_kind` values |
|---|---|
| `boot` | `boot_loaded` |
| `behavior` | `command_succeeds`, `scoreboard_value`, `scoreboard_delta`, `tag_present`, `tag_absent`, `effect_present`, `block_state`, `entity_present`, `entity_spawned`, `item_present`, `item_granted`, `item_dropped`, `teleport_delta`, `time_window`, `weather_state`, `machine_output` |
| `static` | `file_exists` |
| `render` | `render_coverage` |
| `client` | `client_option_state`, `message_observed`, `title_observed`, `screenshot_marker` |

Use `setup_commands` for bounded Minecraft-world setup and `trigger_command` for the command that causes the behavior. `scoreboard_value` and `scoreboard_delta` targets are `objective` or `objective:holder`; item, entity, effect, and block assertions use namespaced identifiers; `teleport_delta.expected_value` is an `x,y,z` offset; `time_window.target` uses the documented time keywords; `weather_state.target` is `clear`, `rain`, or `thunder`; `screenshot_marker.target` is `#RRGGBB` and its optional `expected_value` is a minimum pixel count. `message_observed` and `title_observed` compare exact text from the actual Java client GUI. `screenshot_marker` inspects the framebuffer. Self-reported log/client markers are not accepted as proof. The nonce-bound `AGENTPMT_RUNTIME` marker family is harness-private and rejected in uploaded source.

When typed postconditions cannot trigger the edited code directly, include the applicable verifier overlay in the source zip. Java server checks use `.agentpmt/verification/java/AgentpmtCustomVerifier.java` with `public static void verify(String checkId, ServerLevel serverLevel, ServerPlayer player)`. Java client checks may add `.agentpmt/verification/java/AgentpmtCustomClientVerifier.java` with `public static void verify(String checkId, Minecraft client)`. Bedrock uses `.agentpmt/verification/bedrock/custom_verifier.js` with `export function verifyCustomCheck(checkId, context)`. A Java archive may include both server and client verifier files when its contract has both surfaces. The harness always evaluates its built-in postcondition first, then runs a supplied custom verifier before recording success; agent-supplied verifier code is never the sole proof. The verifier must throw on failure and cannot replace a generic postcondition. Verifier overlays and `.agentpmt/runtime/**` are reserved, throwaway paths and never ship in artifacts.

For `client_option_state`, set `target` to `render_distance`, `simulation_distance`, `entity_distance_scaling`, `gamma`, `graphics_mode`, `cloud_status`, or `particles`, and set `expected_value` to the exact requested value. Use `message_observed`/`title_observed` for text and `screenshot_marker` with a `#RRGGBB` target for arbitrary visual overlays or particles; do not ask verifier code to certify its own output.

Uploaded Java build scripts, wrappers, `buildSrc`, alternate Gradle hooks, generated output/cache directories (`build`, `.gradle`, `out`, `target`), and precompiled Java/native binaries are not trusted. The service rejects generated outputs and precompiled `.class`/`.jar`/native-library files, replaces executable Gradle configuration with the pinned loader template, passes an explicit allowlisted child environment, and gives each job a disposable Gradle home backed by read-only shared caches. Submit editable source and ordinary resource assets only. Agent-edited source executes only in a private disposable Cloud Run worker with a dedicated no-role service account and one verification request per process. If that worker is unavailable, verification fails closed and the artifact is not install-ready.

`advanced_resources` is for non-executable data/resource files and Bedrock `.mcfunction` files. It rejects Java source and `behavior_pack/scripts/*.js`. To change executable Fabric, NeoForge, or Bedrock Script API code, edit the generated project and submit the complete zip with `authoring_mode="agent_code"`; do not try to inject executable code through a declarative request.

##### Bedrock custom namespace

For Bedrock add-ons, generated custom in-game identifiers use the Creator Tools namespace `creator_project:<id>`. Keep using `mod_id` for the request, artifact naming, file paths, and Java platforms. In Bedrock specs, short ids (`"ruby"`) and legacy `<mod_id>:<id>` refs still resolve to the generated custom feature; the emitted pack rewrites them to `creator_project:<id>`. Use `minecraft:<id>` for vanilla content and other explicit namespaces for external content.

##### Creative world mechanics and fidelity

Prank, cursed, chaotic, fake-glitch, admin, debug, and rule-bending ideas are valid requests when you express them as deterministic in-world mechanics. Use `features.events`, `features.commands`, conditions, scoreboards, tags, particles, sounds, titles, messages, gamerules, time/weather actions, block changes, explosions, lightning, and relative teleports when those primitives faithfully match the user's requested behavior.

Do not silently reinterpret intent. If the declarative schema can faithfully express the request, use it. If it cannot, classify the request as `needs_agent_code`, generate the typed base project, implement the requested code, and submit it back through the agent-edited source testing loop. If a substitution is user-approved, set `fidelity_policy="acknowledged_approximation"` and still require the quality gate.

This deterministic builder does not generate arbitrary client mixins, shader loaders, native code, optimization core patches, or custom packet frameworks through the declarative schema. Those requests belong in the agent-edited source workflow, not in a closest-supported substitution presented as success.

##### Implementation truth

Comments, debug chat, README guidance, and metadata do not count as mechanics. Every accepted declarative action has a concrete platform implementation and a runtime assertion. A mechanic without that implementation rejects with `MINECRAFT_CAPABILITY_NOT_IMPLEMENTED`, including its exact field path and `required_next_action="edit_source_and_start_build_job"`. There is no policy that converts incomplete behavior into a successful mod.

Features whose `enabled_platforms` exclude the selected `target_platform` are rejected with `MINECRAFT_PLATFORM_FEATURE_MISMATCH`; they are not dropped from the generated mod.

The request contract is pinned to `schema_version="2026-05-05-v2"` and `compatibility_mode="strict"`. The former platform-passthrough mode was retired because it could report success after dropping features that excluded the selected platform.

Action-specific top-level fields are fail-closed. `task_id` belongs only to `get_build_job`; `limit` only to `list_build_jobs`; preview fields only to `render_preview_image`; and `source_test_mode` plus `verification_contract` require `start_build_job` with `source_archive_file_id`. Build/output/verification options are accepted only by create/build actions. Remove accidental cross-action fields instead of expecting them to be ignored.

Bedrock declarative `features.dimensions` is rejected even when experiments are enabled because the pinned Creator Tools cooperative-add-on gate rejects dimension definitions (`CADDONIREQ191`/`CADDONREQ131`). Use an edited standalone behavior-pack project and retain the full verification gate for dimension work; the builder does not return a known-invalid cooperative add-on.

##### Java client modules

Use `features.client_modules` for Java-only client utility behavior on `target_platform="fabric"` or `target_platform="neoforge"`. Bedrock and skin packs reject client modules because they cannot install Java client code.

Supported `module_kind` values:

* `utility_client_preset` — general anarchy/utility preset for requests phrased as "2b2t client", "anarchy client", or "hacked client"; implements an FPS HUD, bounded typed performance-option updates, maximum-valid brightness, and TNT-cart placement scanning.
* `fps_hud` — HUD-only FPS display.
* `performance_profile` — FPS-oriented HUD plus typed client option updates for render distance, simulation distance, entity distance scale, fast graphics, clouds off, and minimal particles.
* `tnt_cart_placement_esp` — client-side scanner for nearby rail blocks where TNT minecarts can be placed; renders a HUD count and nearest candidate coordinates.
* `block_esp` — bounded client scanner for listed block identifiers.
* `entity_esp` — bounded client scanner for listed entity identifiers.
* `fullbright` — sets the client gamma option to Minecraft's maximum valid brightness.

Common aliases are accepted for `module_kind`: `hacked_client`, `anarchy_client`, `2b2t_client`, and `utility_client` normalize to `utility_client_preset`; `shizik`, `fps_boost`, and `optimization_client` normalize to `performance_profile`; `tnt_esp`, `tnt_cart_esp`, and `minecart_tnt_esp` normalize to `tnt_cart_placement_esp`. Renderer-hybrid aliases are recognized only so validation can return the edited-source next action; they do not generate metadata in place of renderer code.

Client-module options:

| field | Applies to | Notes |
|---|---|---|
| `scan_radius` | ESP modules | Horizontal scan radius, `4` to `64`; default `24`. |
| `update_interval_ticks` | all modules | Refresh interval, `1` to `200`; default `10`. |
| `max_rendered_markers` | ESP modules | Maximum retained HUD markers, `1` to `128`; default `32`. |
| `render_style` | ESP modules | Only `hud` is supported in this release; outline modes are rejected instead of ignored. |
| `color_hex` | all modules | HUD/overlay accent color; accepts the same color forms as textures. |
| `identifiers` | `block_esp`, `entity_esp` | Required list of block/entity ids to scan for. |
| `performance_mode` | `performance_profile`, `utility_client_preset` | `balanced`, `fps`, or `quality`; default `balanced`. |
| `max_render_distance` | performance modules | Applied render-distance option, `2` to `32`; default `8`. |
| `max_simulation_distance` | performance modules | Applied simulation-distance option, `5` to `32`; default `5`. |
| `entity_distance_scale` | performance modules | Applied entity render-distance scale, `0.1` to `1.0`; default `0.5`. |

Renderer rewrites require real loader-specific code and dependencies. Submit that edited Java source with a client verification contract; the declarative path rejects it instead of returning a misleading metadata-only artifact.

Examples:

```json
{
  "client_modules": [
    {
      "module_id": "anarchy_utility",
      "display_name": "Anarchy Utility",
      "module_kind": "2b2t_client",
      "color_hex": "lime",
      "scan_radius": 32,
      "max_rendered_markers": 48
    }
  ]
}
```

```json
{
  "client_modules": [
    {
      "module_id": "shizik_profile",
      "display_name": "Shizik FPS Profile",
      "module_kind": "shizik",
      "performance_mode": "fps",
      "max_render_distance": 6,
      "max_simulation_distance": 5,
      "entity_distance_scale": 0.35
    }
  ]
}
```

```json
{
  "client_modules": [
    {
      "module_id": "tnt_cart_spots",
      "display_name": "TNT Cart Placement ESP",
      "module_kind": "tnt_cart_placement_esp",
      "scan_radius": 48,
      "update_interval_ticks": 5,
      "max_rendered_markers": 64,
      "color_hex": "#ff3355"
    }
  ]
}
```

##### Versions, colors, and locales

Omit `minecraft_version` unless the user explicitly requires the pinned supported version. Each platform has one supported version in `list_capabilities`; unsupported older/newer versions are rejected instead of guessed. Whitespace is ignored, and `v` is accepted only when the remaining value exactly matches the pinned version.

Color fields (`color_hex`, `brand_color_hex`, `hover_text_color`, `map_color`, `default_color`) accept `#RRGGBB`, six-digit hex without `#`, three-digit short hex, or these color names: `black`, `white`, `red`, `green`, `blue`, `yellow`, `orange`, `purple`, `pink`, `brown`, `gray`, `grey`, `cyan`, `magenta`, `lime`, `gold`, `silver`. Values are normalized to lowercase `#rrggbb`.

Locales use `ll_RR`, such as `en_US`. Lowercase or hyphenated equivalents like `en_us`, `en-us`, and `en-US` are normalized.

##### Scoreboards, commands, functions, rarity

Use `objective_id` for scoreboards. Accepted aliases: `scoreboard_id`, `objective`. Use `criterion`; `criteria` is accepted.

Use `description` for commands. `display_name` is accepted as an alias when `description` is absent.

Functions may include optional `description` metadata. Use `lines`; `commands` is accepted as an alias when `lines` is absent.

Structured Bedrock functions are emitted under `behavior_pack/functions/agentpmt/<mod_id>/`. Advanced `.mcfunction` resources sent at older locations under `behavior_pack/functions/` are moved into that same cooperative namespace, and exact references between uploaded functions are rewritten automatically so Creator Tools does not reject loose files.

`features.functions[]` requires at least one single-line Minecraft command in `lines` (or its `commands` alias); empty functions, multiline input, and shell commands reject before generation. Java `features.tags[]` likewise requires at least one valid resource id in `values`; short ids and short `#tag` references are namespaced to the current mod. Every `features.localizations[]` entry requires a non-empty translation mapping so the builder never emits an inert language file.

Use `rarity.value` for item rarity. `rarity.rarity` and `rarity.name` are accepted aliases.

Historical exact aliases also normalize when the intent is deterministic:

| Location | Canonical field/value | Accepted alias |
|---|---|---|
| `ItemSpec` food field | `saturation` | top-level `saturation_modifier` |
| `ItemSpec` bow-like item | `item_kind="projectile"` + `shooter` | `tool_type="bow"` |
| `BlockSpec.block_kind` | `basic` | `generic` |
| `UISpec.ui_kind` | `hud_overlay` | `hud`, `overlay`, `screen_overlay` |
| `UISpec.ui_kind` | `key_mapping` | `keybind`, `key_binding` |
| `RecipeSpec.result_item` | `result_item` | `result`, `output`, `output_item`, `item_result`, `block_result`, `result_block`, `output_block`, `block_output` |

##### ActionSpec aliases

Every action uses `action_kind`. `particle_effect` and `spawn_particles` are accepted as `action_kind` aliases for `spawn_particle`.

Broadcast aliases are accepted for message/title actions: `broadcast_message`, `broadcast_chat`, `announce_message`, and `global_message` normalize to `send_message` with `audience="all_players"`; `broadcast_title`, `announce_title`, and `global_title` normalize to `show_title` with `audience="all_players"`.

When an action needs a target resource, prefer `identifier`. Accepted exact aliases:

| action_kind | Canonical field | Accepted aliases |
|---|---|---|
| `apply_effect`, `remove_effect` | `identifier` | `effect`, `effect_id` |
| `spawn_entity` | `identifier` | `entity`, `entity_id` |
| `play_sound` | `identifier` | `sound`, `sound_id` |
| `spawn_particle` | `identifier` | `particle`, `particle_id` |
| `add_tag`, `remove_tag` | `identifier` | `tag`, `tag_id` |
| `give_item`, `drop_item` | `identifier` | `item`, `item_id` |
| `give_item`, `drop_item` | `value` | `count`, `amount` |
| `replace_held_item` | `identifier` | `item`, `item_id` |
| `apply_damage`, `heal` | `value` | `amount` |
| `set_block`, `place_block` | `identifier` | `block`, `block_id` |
| `set_scoreboard` | `identifier` | `objective`, `objective_id`, `scoreboard_id` |
| `set_scoreboard` | `value` | `score`, `amount`, `delta` |
| `award_advancement` | `identifier` | `advancement`, `advancement_id` |
| `modify_attribute` | `identifier` | `attribute`, `attribute_id` |
| `modify_attribute` | `value` | `amount`, `level` |
| `set_cooldown` | `identifier` | `cooldown`, `cooldown_id`, `cooldown_category` |
| `play_animation` | `identifier` | `animation`, `animation_id` |
| `change_dimension` | `identifier` | `dimension`, `dimension_id` |
| `run_command` | `command` | `command_line`, `minecraft_command` |
| `send_message`, `show_title` | `message` | `text`, `title` |
| `show_title` | `title_display` | `display` |
| `set_time` | `value` | `time`, `time_of_day` |
| `set_weather` | `identifier` | `weather`, `weather_id` |

##### Action options

Use these optional action fields only on the listed `action_kind`; unsupported combinations are rejected instead of ignored.

| action_kind | Supported options |
|---|---|
| `play_sound` | `volume` (`0` to `16`), `pitch` (`>0` to `4`), `position` |
| `spawn_particle` | `count` (`1` to `256`), `spread_x`, `spread_y`, `spread_z` (`0` to `16`), `position` |
| `spawn_entity`, `teleport`, `set_block`, `place_block`, `break_block_with_drops`, `create_explosion`, `summon_lightning` | `position` |
| `apply_effect` | `amplifier` (`0` to `255`) |
| `run_command` | required `command` |
| `send_message`, `show_title` | required `message` or scalar `value` text |
| `give_item`, `drop_item`, `apply_damage`, `heal`, `damage_item`, `repair_item` | optional positive integer `value` |
| `modify_attribute` | optional finite numeric `value` (defaults to `1`) |
| `create_explosion` | optional finite numeric `value > 0` for power (defaults to `2`) |
| `set_scoreboard` | `operation`: `set`, `add`, or `remove` |
| `send_message`, `show_title` | `audience`: `source` or `all_players` |
| `show_title` | `title_display`: `title`, `subtitle`, or `actionbar`; optional `fade_in_ticks`, `stay_ticks`, and `fade_out_ticks` together |
| `set_time` | `value`: `day`, `night`, `noon`, `midnight`, or an integer from `0` to `24000` |
| `set_weather` | `identifier`: `clear`, `rain`, or `thunder` |
| `apply_effect`, `set_on_fire`, `set_weather`, `wait` | `duration_ticks` (`1` to `72000` game ticks) |
| `apply_effect`, `apply_damage`, `heal`, `set_on_fire`, `add_tag`, `remove_tag` | `radius` (`>0` to `64`) and optional `radius_filter`: `all_entities`, `players`, `hostile_mobs`, or `non_player_entities` |
| any executable action except `wait` | `chance_percent` (`>0` to `100`) |

`position` is always a relative offset from the event target or event block, never an absolute world coordinate. Send it as `{"x": x, "y": y, "z": z}` or `[x, y, z]` with integer coordinates from `-32` to `32`.

`set_entity_target`, `mount_entity`, and `tame_entity` operate on the event target. Add a `target_entity` condition identifying a compatible mob. For backward compatibility, `identifier`, `entity`, or `entity_id` supplied on one of these actions inside an event is moved to that condition when it does not conflict with an explicit condition. Bedrock rejects `set_entity_target` because the stable Script API exposes the AI target as read-only. `mount_entity` and `tame_entity` reject targets that do not expose the required platform component/API.

For `send_message` and `show_title`, `target` is accepted only as an audience alias when it is one of `source`, `self`, `player`, `@s`, `all`, `everyone`, `all_players`, `@a`, or `broadcast`. Use canonical `audience` in new requests.

For `give_item`, `drop_item`, `apply_damage`, and `heal`, any provided `value` or accepted value alias must be an integer `>= 1`.

Generic action fields are fail-closed: `identifier`, `value`, `command`, `message`, and `amplifier` reject on action kinds that do not consume them. Remove an accidental field or use the canonical field for the intended action; the builder never silently drops it.

For `set_scoreboard`, `operation` defaults to `set`. Use `add` to increment and `remove` to decrement; both require a positive integer `value` or accepted value alias. Use the opposite operation instead of negative deltas.

Use `wait` inside event or Script API command action lists to delay all following actions. A wait must be followed by an executable action, consecutive waits must be combined, and `chance_percent` belongs on the following action or owning event rather than the wait. Bedrock `.mcfunction` commands cannot express `wait` or `chance_percent`; use `simple_command` or `argument_command` for those.

##### Custom command parameters

Use `command_kind="argument_command"` with `parameters` for runtime command input. Parameter names are referenced in action `message` or `command` strings as `{param:name}`.

Supported `param_type` values are `string`, `integer`, `float`, and `player_name`. A `string` parameter is greedy text and must be last. Optional parameters must come after all required parameters. Example:

```json
{
  "commands": [
    {
      "command_id": "announce",
      "description": "Broadcast a title.",
      "command_kind": "argument_command",
      "permission_level": "op",
      "parameters": [{"name": "message", "param_type": "string"}],
      "actions": [
        {
          "action_kind": "show_title",
          "audience": "all_players",
          "title_display": "actionbar",
          "message": "{param:message}",
          "fade_in_ticks": 5,
          "stay_ticks": 60,
          "fade_out_ticks": 10
        }
      ]
    }
  ]
}
```

For `spawn_particle`, omitting `count` and spread fields preserves each platform generator's default particle behavior. Send explicit values when the count or spread matters.

##### ConditionSpec aliases

Every condition uses `condition_kind`. Prefer `identifier`; accepted exact aliases are `item`/`item_id` for `held_item`, `entity`/`entity_id` for `target_entity`, `block` for `block_id`, `biome` for `biome_id`, `tag`/`tag_id` for `has_tag`, and `objective`/`objective_id`/`scoreboard_id` for `score_at_least`. For `score_at_least`, `score` and `amount` are accepted aliases for `value`.

##### Condition value reference

- `entity_within_radius`: `value` is an integer radius from `1` to `64`; optional `identifier` filters the nearby entity type, for example `{"condition_kind":"entity_within_radius","identifier":"minecraft:player","value":12}`.
- `time_of_day`: `value` is one of `day`, `night`, `dawn`, `sunrise`, `morning`, `noon`, `dusk`, `sunset`, or `midnight`.
- `weather_is`: Java only; `identifier` is one of `clear`, `rain`, or `thunder`.
- `y_below`: `value` is an attainable Overworld threshold from `-63` to `320`; `y_above` accepts `-64` to `319`.
- `light_level_below`: Java only; `value` is an integer from `1` to `15` (`0` is impossible because light levels are never negative).

#### Recipes

Each recipe is a minimal copy-pasteable spec. Drop the recipe inside the `features` block of a `start_build_job` request along with `target_platform`, `mod_id`, and `mod_name`.

##### Recipe 1 — A diamond sword

```json
{
  "items": [
    {
      "item_id": "flame_sword",
      "display_name": "Flame Sword",
      "item_kind": "weapon",
      "tool_type": "sword",
      "tool_tier": "diamond",
      "damage": 7,
      "texture": {"color_hex": "#ff5522"}
    }
  ]
}
```

The validator confirms `item_kind="weapon"` with `tool_type="sword"`. The renderer expands `#ff5522` into a sword sprite. The item lands in the Equipment creative tab. Durability, repair material, enchantability, hand-equipped rendering, and the sword-tag default come from `tool_tier="diamond"`.

##### Recipe 2 — An iron pickaxe

```json
{
  "items": [
    {
      "item_id": "iron_pickaxe",
      "display_name": "Iron Pickaxe",
      "item_kind": "tool",
      "tool_type": "pickaxe",
      "tool_tier": "iron",
      "texture": {"color_hex": "#cccccc"}
    }
  ]
}
```

`tool_type="pickaxe"` is required: tools without `tool_type` are rejected because the icon and dig speed would be non-deterministic. Default damage/durability come from `tool_tier="iron"`. Substitute `axe`, `shovel`, or `hoe` for other vanilla tool kinds.

##### Recipe 3 — A custom-tier weapon

```json
{
  "items": [
    {
      "item_id": "void_blade",
      "display_name": "Void Blade",
      "item_kind": "weapon",
      "tool_type": "custom",
      "tool_tier": "custom",
      "damage": 12,
      "durability": 3000,
      "tool": {
        "tool_type": "custom",
        "tier": "custom",
        "attack_damage": 12,
        "attack_speed": 1.4
      },
      "repairable": {"repair_items": [{"item": "minecraft:netherite_ingot", "repair_amount": 50}]},
      "enchantable": {"slot": "sword", "value": 18},
      "texture": {"color_hex": "#2a0033"}
    }
  ]
}
```

Use `custom` to opt out of tier defaults. Declare `damage`, `durability`, `tool.attack_speed`, `repairable`, and `enchantable` explicitly.

##### Recipe 3b — A pickaxe that mines every block

```json
{
  "items": [
    {
      "item_id": "godpick",
      "display_name": "Godpick",
      "item_kind": "tool",
      "tool_type": "pickaxe",
      "tool_tier": "netherite",
      "tool": {
        "tool_type": "pickaxe",
        "tier": "netherite",
        "break_all_blocks": true,
        "instabreak": true
      },
      "texture": {"color_hex": "#ffd700"}
    }
  ]
}
```

`tool.break_all_blocks=true` tells the generator: this tool ignores the vanilla pickaxe/axe/shovel/hoe destructible tags and mines *every* block. Bedrock emits a Molang-true tag predicate on `minecraft:digger.destroy_speeds`; Java upgrades the tier to netherite so the tool's `INCORRECT_FOR` block tag is effectively empty. Pair with `instabreak: true` for one-shot mining.

##### Recipe 4 — A full Java diamond armor set

```json
{
  "items": [
    {"item_id": "set_helmet", "display_name": "Set Helmet", "item_kind": "armor", "tool_tier": "diamond", "armor": {"slot": "head",  "protection": 3, "toughness": 2}, "texture": {"source_base64": "<base64 PNG of the helmet icon>"}},
    {"item_id": "set_chest",  "display_name": "Set Chest",  "item_kind": "armor", "tool_tier": "diamond", "armor": {"slot": "chest", "protection": 8, "toughness": 2}, "texture": {"source_base64": "<base64 PNG of the chestplate icon>"}},
    {"item_id": "set_legs",   "display_name": "Set Legs",   "item_kind": "armor", "tool_tier": "diamond", "armor": {"slot": "legs",  "protection": 6, "toughness": 2}, "texture": {"source_base64": "<base64 PNG of the leggings icon>"}},
    {"item_id": "set_boots",  "display_name": "Set Boots",  "item_kind": "armor", "tool_tier": "diamond", "armor": {"slot": "feet",  "protection": 3, "toughness": 2}, "texture": {"source_base64": "<base64 PNG of the boots icon>"}}
  ]
}
```

One `ItemSpec` per armor slot. `armor.slot` is required: head/chest/legs/feet. `tool_tier` must be `iron`, `gold`, `diamond`, or `netherite` and selects the vanilla armor material (sound, repair item, durability, and worn equipment asset). Supply a real PNG for the inventory icon; `color_hex` is rejected with `MINECRAFT_ARMOR_TEXTURE_REQUIRES_IMAGE`. Use edited source for wood/stone/custom armor materials or a custom worn atlas.

##### Recipe 5 — A food item

```json
{
  "items": [
    {
      "item_id": "spicy_jerky",
      "display_name": "Spicy Jerky",
      "item_kind": "food",
      "food": {
        "nutrition": 7,
        "saturation_modifier": 0.6,
        "effects": [{"effect": "minecraft:fire_resistance", "chance": 1.0, "duration_seconds": 30, "amplifier": 0}]
      },
      "texture": {"color_hex": "#7a3a1a"}
    }
  ]
}
```

Pair `item_kind="food"` with the `food` preset. The food preset emits the eat animation, hunger restore, and any post-consumption effects.

##### Recipe 6 — A bow that fires arrows

```json
{
  "items": [
    {
      "item_id": "magic_arrow",
      "display_name": "Magic Arrow",
      "item_kind": "projectile",
      "projectile": {"projectile_entity": "minecraft:arrow"},
      "texture": {"color_hex": "#88aaff"}
    },
    {
      "item_id": "magic_bow",
      "display_name": "Magic Bow",
      "item_kind": "projectile",
      "shooter": {"charge_on_draw": true, "scale_power_by_draw_duration": true, "ammunition": ["modid:magic_arrow"], "max_draw_duration": 1.0},
      "texture": {"color_hex": "#552200"}
    }
  ]
}
```

Two items: one for the projectile, one for the launcher. Both carry `item_kind="projectile"`; the launcher has the `shooter` preset.

##### Recipe 7 — An ore plus its worldgen and drop

```json
{
  "blocks": [
    {
      "block_id": "ruby_ore",
      "display_name": "Ruby Ore",
      "block_kind": "ore",
      "hardness": 3.0,
      "resistance": 8.0,
      "drops": ["modid:ruby"],
      "texture": {"color_hex": "#c91140"}
    }
  ],
  "items": [
    {
      "item_id": "ruby",
      "display_name": "Ruby",
      "item_kind": "generic",
      "texture": {"color_hex": "#c91140"}
    }
  ],
  "worldgen": [
    {
      "feature_id": "ruby_ore_feature",
      "feature_kind": "ore_feature",
      "block_id": "ruby_ore",
      "target_block": "minecraft:stone",
      "vein_size": 6,
      "count_per_chunk": 4,
      "min_y": -32,
      "max_y": 48
    }
  ]
}
```

`drops` references an item id by namespace. The mined `ruby` is `item_kind="generic"` — it is a raw material that another recipe consumes; it does not need a tool/armor/food preset.

##### Recipe 8 — A hostile mob

```json
{
  "entities": [
    {
      "entity_id": "shadow_stalker",
      "display_name": "Shadow Stalker",
      "entity_kind": "hostile_mob",
      "health": 30,
      "attack_damage": 5,
      "movement_speed": 0.32,
      "spawn_biomes": ["minecraft:dark_forest", "minecraft:taiga"],
      "spawn_weight": 12,
      "texture": {"color_hex": "#1a1a2e"}
    }
  ]
}
```

The entity texture seeds both the mob model and the spawn-egg color. Bedrock additionally accepts `source_base64` or `source_file_id` to use a 64×64 PNG atlas.

##### Recipe 9 — A tameable pet

```json
{
  "entities": [
    {
      "entity_id": "stone_lynx",
      "display_name": "Stone Lynx",
      "entity_kind": "tameable_pet",
      "health": 20,
      "attack_damage": 4,
      "tameable": {"tame_items": ["minecraft:cooked_beef"], "probability": 0.5},
      "texture": {"color_hex": "#9d8866"}
    }
  ]
}
```

`entity_kind="tameable_pet"` plus the `tameable` preset enables the right-click-with-item taming flow.

##### Recipe 10 — A weapon that sets enemies on fire

```json
{
  "items": [
    {
      "item_id": "flame_sword",
      "display_name": "Flame Sword",
      "item_kind": "weapon",
      "tool_type": "sword",
      "tool_tier": "diamond",
      "damage": 8,
      "texture": {"color_hex": "#ff5522"}
    }
  ],
  "events": [
    {
      "event_id": "flame_sword_ignite",
      "event_kind": "on_item_hit_entity",
      "conditions": [{"condition_kind": "held_item", "identifier": "modid:flame_sword"}],
      "actions": [{"action_kind": "set_on_fire", "duration_ticks": 120}]
    }
  ]
}
```

One item, one event. The event filters by `held_item` (your sword's id) and emits `set_on_fire` against the hit entity. The event does *not* create a second item.

##### Recipe 11 — A skin pack with one skin

```json
{
  "action": "start_build_job",
  "target_platform": "bedrock_skinpack",
  "mod_id": "blue_pack",
  "mod_name": "Blue Pack",
  "skin_pack": {
    "pack_id": "blue_pack",
    "display_name": "Blue Pack",
    "skins": [
      {
        "skin_id": "blue_hero",
        "display_name": "Blue Hero",
        "texture": {"source_base64": "<base64-encoded 64x64 PNG>"}
      }
    ]
  }
}
```

Skin pack textures must be exactly 64×64 PNG.

##### Recipe 12 — A cursed prank item

```json
{
  "items": [
    {
      "item_id": "cursed_stick",
      "display_name": "Cursed Stick",
      "item_kind": "generic",
      "texture": {"color_hex": "#7a35ff"}
    }
  ],
  "events": [
    {
      "event_id": "cursed_stick_use",
      "event_kind": "on_item_use",
      "conditions": [{"condition_kind": "held_item", "identifier": "cursed_stick"}],
      "actions": [
        {"action_kind": "spawn_particle", "identifier": "minecraft:basic_flame_particle", "count": 24, "spread_x": 2, "spread_y": 1, "spread_z": 2},
        {"action_kind": "play_sound", "identifier": "minecraft:block.note_block.pling", "volume": 1.5, "pitch": 0.5},
        {"action_kind": "show_title", "message": "Something moved.", "audience": "source"},
        {"action_kind": "teleport", "position": [0, 3, 0]}
      ]
    }
  ]
}
```

Use relative `position` for harmless movement effects. The item stays one `ItemSpec`; the event supplies the prank behavior.

##### Recipe 13 — A fake-glitch block event

```json
{
  "blocks": [
    {
      "block_id": "glitch_panel",
      "display_name": "Glitch Panel",
      "block_kind": "interactive",
      "texture": {"color_hex": "#00ffff"}
    }
  ],
  "events": [
    {
      "event_id": "glitch_panel_interact",
      "event_kind": "on_block_interact",
      "conditions": [{"condition_kind": "block_id", "identifier": "glitch_panel"}],
      "actions": [
        {"action_kind": "set_time", "time_of_day": "midnight"},
        {"action_kind": "set_weather", "weather": "thunder", "duration_ticks": 200},
        {"action_kind": "spawn_particle", "identifier": "minecraft:large_smoke", "count": 48, "spread_x": 3, "spread_y": 2, "spread_z": 3},
        {"action_kind": "broadcast_message", "text": "World state desynchronized."}
      ]
    }
  ]
}
```

Fake-glitch behavior should be built from world-side events, particles, titles/messages, time, weather, sounds, and block changes.

##### Recipe 14 — An admin debug command

```json
{
  "commands": [
    {
      "command_id": "debug_storm",
      "description": "Toggle a dramatic debug storm.",
      "command_kind": "admin_command",
      "permission_level": "admin",
      "actions": [
        {"action_kind": "set_gamerule", "identifier": "doDaylightCycle", "value": false},
        {"action_kind": "set_time", "value": "night"},
        {"action_kind": "set_weather", "identifier": "thunder", "duration_ticks": 600},
        {"action_kind": "send_message", "message": "Debug storm enabled.", "audience": "all_players"}
      ]
    }
  ]
}
```

Use `admin_command` plus `permission_level="admin"` for operator tools. Prefer `set_gamerule`, `set_time`, and `set_weather` over raw command strings when those first-class actions cover the behavior.

##### Recipe 15 — A chaos trap

```json
{
  "blocks": [
    {
      "block_id": "chaos_plate",
      "display_name": "Chaos Plate",
      "block_kind": "interactive",
      "texture": {"color_hex": "#ff00ff"}
    }
  ],
  "scoreboards": [{"objective_id": "chaos_triggers", "display_name": "Chaos Triggers", "criterion": "dummy"}],
  "events": [
    {
      "event_id": "chaos_plate_trigger",
      "event_kind": "on_block_interact",
      "conditions": [{"condition_kind": "block_id", "identifier": "chaos_plate"}],
      "actions": [
        {"action_kind": "set_block", "identifier": "minecraft:gold_block", "position": [0, -1, 0]},
        {"action_kind": "summon_lightning", "position": [2, 0, 0]},
        {"action_kind": "create_explosion", "value": 2, "position": [-2, 0, 0]},
        {"action_kind": "set_scoreboard", "identifier": "chaos_triggers", "operation": "add", "value": 1}
      ]
    }
  ]
}
```

Keep high-impact effects bounded with explicit values and relative positions so the generated behavior remains predictable.

##### Recipe 16 — Timed/random progression with milestones

```json
{
  "scoreboards": [{"objective_id": "weeks", "display_name": "Weeks", "criterion": "dummy"}],
  "events": [
    {
      "event_id": "weekly_progress",
      "event_kind": "on_player_tick",
      "interval_ticks": 1200,
      "cooldown_ticks": 1200,
      "chance_percent": 35,
      "actions": [
        {"action_kind": "set_scoreboard", "identifier": "weeks", "operation": "add", "value": 1},
        {"action_kind": "show_title", "audience": "source", "title_display": "actionbar", "message": "A week passes..."}
      ]
    }
  ]
}
```

Use declared scoreboards for staged Java progress; the objective is created on server startup and behavior verification asserts that it exists. `set_scoreboard` can also create an undeclared writable objective at action time on both Java and Bedrock. A declared objective mutated by `set_scoreboard` must use `criterion="dummy"` or `"trigger"`; read-only vanilla criteria reject before generation. Use `interval_ticks` for cadence, `cooldown_ticks` to prevent repeated firing, and `chance_percent` for random outcomes.

##### Recipe 17 — A stalker entity with proximity behavior

```json
{
  "entities": [
    {
      "entity_id": "stalker",
      "display_name": "Stalker",
      "entity_kind": "hostile_mob",
      "health": 60,
      "movement_speed": 0.35,
      "scale": 2.5,
      "ai_goals": [
        {"goal_kind": "nearest_attackable_target", "priority": 1, "search_radius": 30},
        {"goal_kind": "melee_attack", "priority": 2, "speed_multiplier": 1.25, "attack_reach_multiplier": 2.0}
      ],
      "texture": {"color_hex": "#111111"}
    }
  ],
  "events": [
    {
      "event_id": "stalker_charge",
      "event_kind": "on_entity_tick",
      "interval_ticks": 20,
      "conditions": [{"condition_kind": "entity_within_radius", "identifier": "minecraft:player", "value": 12}],
      "actions": [
        {"action_kind": "wait", "duration_ticks": 20},
        {"action_kind": "apply_effect", "identifier": "minecraft:slowness", "duration_ticks": 80, "radius": 12, "radius_filter": "players"},
        {"action_kind": "spawn_particle", "identifier": "minecraft:basic_flame_particle", "count": 16, "spread_x": 1, "spread_y": 2, "spread_z": 1}
      ]
    }
  ]
}
```

`attack_reach_multiplier` is Bedrock-only. Fabric and NeoForge reject it with an actionable platform error; use `search_radius` and radius actions for cross-platform sensing.

##### Recipe 18 — A two-input machine

```json
{
  "items": [
    {"item_id": "amalgam", "display_name": "Amalgam", "texture": {"color_hex": "#b8f2ff"}}
  ],
  "machines": [
    {
      "machine_id": "amalgamator",
      "display_name": "Amalgamator",
      "texture": {"color_hex": "#606060"},
      "processing_time_ticks": 100,
      "machine_recipes": [
        {
          "recipe_id": "make_amalgam",
          "inputs": ["minecraft:iron_ingot", "minecraft:gold_ingot"],
          "output": "modid:amalgam",
          "output_count": 1
        }
      ]
    }
  ],
  "events": [
    {
      "event_id": "amalgamator_complete",
      "event_kind": "on_machine_recipe_complete",
      "actions": [{"action_kind": "broadcast_message", "text": "The amalgamator finished."}]
    }
  ]
}
```

Right-click the generated machine with each input item. Inputs are tracked per block position; when the full set is present, the output drops after `processing_time_ticks`.

#### Verify Every Generation

Use `render_preview_image` to inspect important textures, then submit the same spec through `start_build_job`. A visual preview checks the selected texture only; the async quality gate proves packaging, runtime loading, declared behavior, and client/render checks before installation.

```json
{
  "action": "render_preview_image",
  "target_platform": "bedrock",
  "mod_id": "flame_tools",
  "mod_name": "Flame Tools",
  "preview_target_kind": "item",
  "preview_target_id": "flame_sword",
  "features": { /* same features block from start_build_job */ }
}
```

If the preview looks like a flat colored square or the wrong tool sprite, you forgot `item_kind`, `tool_type`, or both.

#### Common Mistakes

Each entry pairs the failure mode with the structured error code the validator now returns. If you see the code, fix the spec.

| Mistake | What happens now |
|---|---|
| `item_kind="generic"` on a weapon with `damage` set | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="tool"` without `tool_type` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="weapon"` with `tool_type="pickaxe"` | Rejected: weapon requires `sword` or `custom` |
| `item_kind="armor"` without `armor` or `wearable` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="food"` without `food` preset or `nutrition` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="block_placer"` without `block_placer` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `food` preset on an `item_kind="tool"` | Rejected: preset/kind mismatch |
| `texture` omitted on any visible asset | Rejected: `MINECRAFT_VISIBLE_ASSET_TEXTURE_REQUIRED` |
| `texture: {}` with no `color_hex`, `source_base64`, or `source_file_id` | Rejected: `MINECRAFT_TEXTURE_SOURCE_REQUIRED` |
| `item_kind="armor"` with `texture: {color_hex: ...}` only | Rejected: `MINECRAFT_ARMOR_TEXTURE_REQUIRES_IMAGE` |
| Pickaxe specced to "break any block" but only breaks a few | Bedrock: add `tool.break_all_blocks: true`. Fabric/NeoForge: use the agent-edited source workflow; declarative requests reject because changing to a vanilla netherite tier does not make every block mineable. |
| Feature appears in the wrong platform build | Set `enabled_platforms: ["bedrock"]` (or fabric/neoforge) to scope it; an empty list applies to all platforms |
| Diamond/netherite armor looks/sounds/repairs like iron | Set `tool_tier: "diamond"` (or netherite); durability, enchant value, repair tag, and equip sound are derived from it |
| `recipe_kind="brewing_mix"` or `"brewing_container"` on Fabric/NeoForge | Rejected: brewing recipes are Bedrock-only. Use Bedrock or model the effect as a `crafting_shaped` recipe |
| Tool attack_speed left at the default 1.6 but the tool is a pickaxe | The Java side now derives the attack-speed delta per tool_type (sword -2.4, pickaxe -2.8, axe -3.1, shovel -3.0, hoe -1.0) so the swing animation matches vanilla; supply `tool.attack_speed` only if you want a non-vanilla swing rate |
| Block `drops` references an item id that doesn't exist | Rejected with `MINECRAFT_SPEC_VALIDATION_FAILED`. Define the dropped item under `features.items` or use a `minecraft:*` identifier |
| `recipe.result_item` / `block_placer` / `entity_placer` references a non-existent id | Rejected with `MINECRAFT_SPEC_VALIDATION_FAILED`. Same fix: define the target feature or use a `minecraft:*` identifier |
| Multiple `items[]` entries for one weapon (one for damage, one for enchant) | Two items in inventory; collapse to one ItemSpec |
| `on_item_hit_entity` without a `held_item` condition | Fires for every hit; add `{"condition_kind":"held_item","identifier":"modid:itemid"}` |
| `command_id` shadowing a Minecraft command (e.g. `give`, `tp`) | Reject or behavior conflict; pick a unique id |

#### Supported Platforms

- `bedrock`: Minecraft Bedrock add-on generation for pinned Mojang Bedrock Samples baseline `v1.26.20.4`. Produces source zips, `.mcaddon` installables, and Mojang Minecraft Creator Tools validation reports.
- `fabric`: Minecraft Java Fabric generation for pinned version `1.21.11`. Produces source zips and optional built jars using the pinned offline Gradle/Fabric toolchain.
- `neoforge`: Minecraft Java NeoForge generation for pinned Minecraft `1.21.11` and NeoForge `21.11.42`. Produces source zips and optional built jars using the pinned offline Gradle/NeoForge toolchain.
- `bedrock_skinpack`: Bedrock skin pack generation. Produces installable `.mcpack` files from skin texture images and localization/manifest metadata.
- `forge` is retired. Requests using `target_platform="forge"` are rejected with a structured migration error directing callers to `neoforge`.

#### Actions

##### `list_capabilities`

Return supported platforms, pinned dependencies, feature kinds, output artifacts, and platform notes.

Optional:
- `target_platform`: `bedrock`, `bedrock_skinpack`, `fabric`, or `neoforge`.

##### `validate_mod_project`

Validate either a structured mod specification or a source archive previously produced by this tool.

Modes:
- Spec validation: provide `target_platform`, `mod_id`, `mod_name`, and `features` (or `skin_pack` for skinpacks).
- Archive validation: provide `source_archive_file_id`.

##### `create_mod_project`

Generate synchronous source/debug artifacts without runtime verification. This action accepts only `verification_level="off"`, always returns `ready_for_install=false`, and must not be used for final delivery.

Required:
- `target_platform`: `bedrock`, `bedrock_skinpack`, `fabric`, or `neoforge`.
- `mod_id`: lowercase identifier matching `^[a-z][a-z0-9_]{1,63}$`.
- `mod_name`: human-readable mod name.
- `features`: structured feature object for normal Bedrock/Fabric/NeoForge mods.
- `skin_pack`: structured skin pack object for `target_platform=bedrock_skinpack`.

Optional:
- `minecraft_version`: omit to use the pinned platform version.
- `description`: short mod description.
- `output_mode`: `installable`, `source`, or `both`. Default is `both`.
- `build_jar`: for Fabric/NeoForge only. Default is `true`.
- `validate_output`: run external platform validation where available. Default is `true`.
- `include_file_preview`: include capped text previews in `generated_files`.
- `allow_experimental_bedrock_features`: allow script-based Bedrock features that may require experiments.
- `authoring_mode`: `auto` or `declarative` for typed features. `agent_code` is accepted only by `start_build_job` with `source_archive_file_id`.

##### `start_build_job`, `get_build_job`, and `list_build_jobs`

Use `start_build_job` for final artifacts. It queues compile/package/runtime work and immediately returns a `task_id`. Poll `get_build_job` with that id until `status` is `completed` or `failed`; inspect `result.ready_for_install`, `result.quality_gate`, and `result.runtime_verification`. `list_build_jobs` returns recent jobs for the current budget.

For generated specs, provide the same required fields as `create_mod_project`. For agent-edited source, provide `authoring_mode="agent_code"`, `source_archive_file_id`, `target_platform`, `mod_id`, and `source_test_mode`. `verification_level="behavior"` also requires a machine-checkable `verification_contract` bound to the same platform and mod id with at least one `behavior`, `render`, or `client` check; `boot_smoke` may omit it because that level proves loading only, never behavior.

##### `render_preview_image`

Render an enlarged PNG preview for an item, block, or entity texture and upload it to File Manager. Use it before the final verified build to confirm important icons look right.

Modes:
- Spec preview: provide `target_platform`, `mod_id`, `mod_name`, and `features`; the tool generates files in memory and previews the selected texture.
- Source archive preview: provide `source_archive_file_id` from a generated source zip; optionally include `mod_id`.
- Direct image preview: provide `preview_source_file_id` for a File Manager image uploaded by the user.

Optional:
- `preview_target_kind`: `item`, `block`, or `entity`.
- `preview_target_id`: feature id or namespaced id, such as `flame_sword` or `flame_tools:flame_sword`.
- `preview_size`: square preview PNG size from 32 to 1024 pixels. Default is 256.
- `preview_background`: `checkerboard`, `transparent`, `white`, or `black`. Default is `checkerboard`.

#### Field Reference

All feature arrays are optional. Use empty arrays or omit unused sections.

##### Texture binding (BindingTextureSpec)

Every visible asset's `texture` field is a `BindingTextureSpec`. Supply exactly one of:
- `source_base64`: base64-encoded image bytes (PNG or JPEG, max 1024 px, max 5 MB).
- `source_file_id`: File Manager file_id for a user-uploaded image.
- `color_hex`: explicit `#RRGGBB` color rendered as a kind-shaped procedural sprite.

`source_base64` and `source_file_id` are mutually exclusive. A spec with none of the three is rejected with `MINECRAFT_TEXTURE_SOURCE_REQUIRED`.

##### Items

- `item_id`: required lowercase identifier.
- `display_name`: required.
- `item_kind`: required behavior class (see Recipes). One of `generic`, `tool`, `weapon`, `armor`, `food`, `fuel`, `projectile`, `block_placer`, or `entity_placer`. Drives icon sprite, creative-tab placement, stack size, and required presets.
- `tool_type`: `pickaxe`, `axe`, `shovel`, `hoe`, `sword`, or `custom`. Required for `item_kind="tool"`; `weapon` requires `sword` or `custom`.
- `tool_tier`: `wood`, `stone`, `iron`, `gold`, `diamond`, `netherite`, or `custom` for tools/weapons. Armor permits only `iron`, `gold`, `diamond`, or `netherite` and defaults to iron; unsupported armor tiers reject instead of silently becoming iron.
- `texture`: required BindingTextureSpec.
- `damage`, `durability`, `max_stack_size`, `nutrition`, `saturation`: per-field semantics; defaults derive from `item_kind`/`tool_tier`.
- `tool`, `armor`, `food`, `block_placer`, `entity_placer`, `projectile`, `shooter`, `throwable`: presets used by the matching `item_kind`. The validator rejects preset/kind mismatches with `MINECRAFT_ITEM_KIND_REQUIRES_PRESET`. Bedrock honors `tool.mining_speed`, `instabreak`, and `break_all_blocks`; Java custom mining rules, nested digger/repair/enchant presets, and Bedrock custom attack speed require edited source and reject declarative generation.
- Optional Bedrock item component knobs implemented by the declarative renderer are `enchantable`, `repairable`, `digger`, `cooldown`, `use_modifiers`, `rarity`, `dyeable`, `glint` (also accepts the exact alias `foil`), `allow_off_hand`, `hover_text_color`, and `component_overrides`. Java supports its typed item properties, including `fire_resistant`, but rejects Bedrock-only component knobs. Unsupported platform/field combinations fail validation instead of being ignored; use edited source for custom components, swing sounds, or kinetic/piercing mechanics.

##### Blocks

- `block_id`: required lowercase identifier.
- `display_name`: required.
- `block_kind`: `basic`, `ore`, `light`, `interactive`, `crop`, `plant`, `redstone`, `machine`, or `container`. Consult `list_capabilities.implementation_status` for the target: Java rejects `redstone` because the declarative Java block does not implement signal behavior, while Bedrock implements conductor behavior but rejects signal emission.
- `texture`: required BindingTextureSpec.
- Implemented fields depend on the selected block kind and platform. Shared declarative fields include `hardness`, `resistance`, `light_level`, `drops`, and `texture`; Bedrock supports the typed component fields accepted by its pinned registry, including `collision_box`, `selection_box`, `placement_filter`, `flammable`, `friction`, `map_color`, `crop`, `redstone`, `tick`, `crafting_table`, and `component_overrides`. Explicit `material_instances` and `custom_components` require edited source because the declarative renderer derives the material instance from `texture` and does not register custom component code.

##### Entities

- `entity_id`: required lowercase identifier.
- `display_name`: required.
- `entity_kind`: `passive_mob`, `hostile_mob`, `neutral_mob`, `projectile`, `npc_like`, `tameable_pet`, `rideable_mount`, or `boss_like`. Java declarative generation accepts the first four; Java requests for the latter four reject and route to edited source. Bedrock also rejects `npc_like`: the old path emitted a fixed apple trade rather than the requested trade contract. Use edited source for NPC trades; other Bedrock kinds are accepted only when every populated behavior field has a real pack implementation. `ai_goals[].goal_kind=trade_with_player` and every `interactions[]` preset likewise reject until an explicit trade/interaction implementation is supplied through edited source.
- `texture`: required BindingTextureSpec. Seeds both the mob model and the spawn-egg color.
- `health`, `attack_damage`, `movement_speed`, `spawn_biomes`, `spawn_weight`, `families`, `ai_goals`, `interactions`, `rideable`, `tameable`, `breedable`, `equipment`, `render`, `loot_table`, `component_overrides`.

##### Particles

- `particle_id`: required lowercase identifier.
- `texture`: required BindingTextureSpec.

Bedrock custom particles generate a resource-pack particle definition and a `textures/agentpmt/<mod_id>/particle/{particle_id}.png` sprite. Spawn a custom particle with `{"action_kind": "spawn_particle", "identifier": "<particle_id>"}` or the legacy `<mod_id>:<particle_id>` form; the emitted Bedrock pack uses `creator_project:<particle_id>`. Use vanilla identifiers such as `minecraft:basic_flame_particle` when a custom texture is not needed.

##### Bedrock animations and controllers

Animation resources are Bedrock-only and must contain executable content. `AnimationSpec.animation_json` requires a non-empty `animations` object with at least one bones, sound, particle, or timeline behavior. `AnimationControllerSpec.controller_json` requires a state with an animation, transition, or event. `RenderControllerSpec.controller_json` requires a controller with non-empty `geometry`, `materials`, and `textures`. Empty resources are rejected instead of being emitted as inert placeholders.

##### Effects

Declarative custom effect definitions are rejected on every platform because the former generated registrations did not implement their advertised mechanics. To apply or remove a real vanilla effect, use the event/command actions `apply_effect` and `remove_effect` with a `minecraft:<effect>` identifier. Implement a genuinely custom status effect in agent-edited source and submit it through `start_build_job` with behavior checks.

##### Commands

- `command_id`: required lowercase identifier.
- `description`: required.
- `command_kind`: `simple_command`, `argument_command`, `function_command`, or `admin_command`.
- `permission_level`: `any`, `op`, or `admin`.
- `actions`: required non-empty array of action specs.

##### Worldgen

- `feature_id`: required lowercase identifier.
- `feature_kind`: `ore_feature`, `single_block_feature`, `vegetation_patch`, `structure_placement`, `custom_biome`, or `custom_dimension`.
- `block_id`, `target_block` (default `minecraft:stone`), `vein_size`, `count_per_chunk`, `min_y`, `max_y`, `biomes`.

`min_y` must be less than or equal to `max_y`.

##### Recipes

- `recipe_id`: required lowercase identifier.
- `result_item`: required item or block item identifier. Accepted aliases: `result`, `output`, `output_item`, `item_result`, `block_result`, `result_block`, `output_block`, `block_output`.
- `recipe_kind`: `shaped`, `shapeless`, `furnace`, `brewing_mix`, `brewing_container`, `smithing_transform`, or `smithing_trim`.
- `pattern`, `key`, `ingredients`, `count`, `cooking_time_seconds`, `input_item`, `template_item`, `base_item`, `addition_item`.

Java targets reject `brewing_mix` and `brewing_container` with `MINECRAFT_COMPONENT_UNSUPPORTED_ON_PLATFORM`; those recipe kinds are Bedrock-only.

##### Loot Tables

Bedrock `features.loot_tables` entries must set `target` to one generated entity id. The generator writes the table under `behavior_pack/loot_tables/agentpmt/<mod_id>/` and binds that exact path to the entity's `minecraft:loot` component. `EntitySpec.loot_table` may name the declared `loot_id`; legacy `loot_tables/.../<loot_id>.json` values resolve by the final filename. Conflicting, duplicate, undeclared, or missing entity targets are rejected. Java declarative loot tables remain rejected because generated Java entities do not yet bind per-entity death loot; use edited source there. For block drops on every platform, use `BlockSpec.drops`.

##### Events

- `event_id`: required lowercase identifier.
- `event_kind`: one of the supported kinds per platform (see Recipe 10).
- `conditions`: optional array of condition specs (`held_item`, `target_entity`, `source_entity`, `block_id`, `biome_id`, `has_tag`, `score_at_least`, `entity_within_radius`, `time_of_day`, `weather_is`, `y_below`, `y_above`; Java also supports `light_level_below`).
- `held_item`, `target_entity`, and `source_entity` require the matching resource `identifier`; `source_entity` accepts `entity` and `entity_id` as aliases. `score_at_least` requires an objective `identifier` and finite integer `value`, and checks the source player's score on every platform. `has_tag.subject` is `source` or `target` and defaults to `target`.
- Condition values: `entity_within_radius.value` is `1` to `64` and its optional `identifier` filters entity type; `time_of_day.value` is `day`, `night`, `dawn`, `sunrise`, `morning`, `noon`, `dusk`, `sunset`, or `midnight`; `weather_is.identifier` is Java-only `clear`, `rain`, or `thunder`; `y_below.value` is `-63` to `320`; `y_above.value` is `-64` to `319`; `light_level_below.value` is Java-only `1` to `15`. Java `source_entity` accepts only `minecraft:player` because Java event dispatch exposes the triggering player as source. Condition fields reject on kinds that do not consume them.
- `actions`: required non-empty array of action specs.
- `interval_ticks`: optional cadence for tick-style events (`on_player_tick`, `on_entity_tick`, `on_block_tick`, `on_enter_biome`, `on_item_inventory_tick`).
- `cooldown_ticks`: optional per-subject cooldown.
- `chance_percent`: optional whole-event random gate.
- `action_selection`: `all` or `random_one`.

`on_enter_biome` fires on the player's first observed biome and only when that biome id changes afterward; add a `biome_id` condition to select a specific destination biome. `on_item_inventory_tick` scans every occupied inventory slot and requires a `held_item` condition identifying the stack. `on_inventory_change` evaluates `held_item` against the changed stack. Slot-mutating `consume_item`, `damage_item`, and `repair_item` actions are rejected on both inventory event kinds because declarative actions mutate the main hand rather than an arbitrary inventory slot; implement explicit slot mutation through the agent-edited source workflow.

Target-mutating actions reject on `on_entity_death`, where the target is no longer live. On `on_projectile_hit`, target-mutating actions require a non-player `target_entity` condition so the entity-hit branch cannot accidentally apply the action to the projectile or shooter after a block impact. Event cooldowns are per source player for player/source events and per target entity for entity events.

`run_command` accepts a single Minecraft command line only. Shell-like syntax such as `&&`, `||`, backticks, `$()`, redirection, and shell/program names such as `bash`, `npm`, `gradle`, `java`, or `python` are rejected.

##### Machines and Storage

- `MachineSpec` requires `texture` (visible block face). The declarative runtime implements `machine_kind="processor"`; `generator`, `storage`, `tank`, and `transfer_endpoint` reject and route to edited source.
- `processing_time_ticks`: ticks between completing the input set and producing output. `processing_time` is accepted as an alias; `processing_time_seconds` is accepted when it converts to whole ticks.
- `machine_recipes`: inline machine recipes. Each recipe has `recipe_id`, `inputs` (1-9 item ids), `output`, and `output_count`.
- Machine recipes are interact-driven: right-click the machine with each required input item. The generated machine records pending inputs per block position, consumes matching inputs, waits `processing_time_ticks`, then drops the output item.
- Bedrock machine textures are merged into the normal `resource_pack/textures/terrain_texture.json` atlas. Do not remove the structured machine helper to avoid loose texture files.
- `StorageSpec` declaratively supports a Bedrock `backpack` with item slots. Java storage and Bedrock `item_container`, `fluid_tank`, and `energy_storage` requests reject and route to edited source instead of emitting inert capacity metadata.

##### Skins

- `SkinPackSpec.skins[]` requires `skin_id`, `display_name`, and a 64×64 `texture`.

#### Output Behavior

- Bedrock `installable` or `both` returns a `.mcaddon` and validation report. With `validate_output=true`, Mojang Minecraft Creator Tools validates the generated add-on.
- Bedrock skin packs return a `.mcpack`; with `validate_output=true`, the service first validates the archive structure, references, PNG integrity, and exact 64x64 skin dimensions. Minecraft Creator Tools then runs its supported skin checks, and only the add-on suite's expected missing-BP/RP-manifest findings (`CADDONREQ163` and `CADDONREQ164`) are ignored; every other Creator Tools error remains fatal.
- Fabric/NeoForge `installable` or `both` returns a jar when `build_jar=true`; otherwise use `source` for source zips only.
- `start_build_job` returns a `task_id` immediately. `get_build_job` returns queued/processing/failed/completed state; completed jobs expose artifacts, validation/build output, runtime checks, the quality gate, and install readiness.
- `render_preview_image` returns a `preview` artifact with a PNG `file_id`, signed URL, and image metadata. It previews texture/icon assets only; `start_build_job` performs gameplay verification.
- Supported Fabric/NeoForge entity kinds emit registered `EntityType` definitions, concrete generated entity subclasses, default attributes, spawn eggs, client renderer registrations, and loader-specific attribute hooks. Unsupported kinds or populated fields reject before generation.
- Supported Fabric/NeoForge `ore_feature` and `single_block_feature` worldgen specs emit configured/placed features plus loader-specific biome hooks. Other worldgen kinds reject before generation.
- `on_item_hit_entity` event specs emit loader-specific attack-event handlers and execute supported Java action templates such as fire, damage, healing, effects, particles, sounds, tags, item grants/drops, entity spawns, and Minecraft commands.
- Java builds use a per-job Gradle home and immutable pinned offline dependency/loader caches. No dependency versions are chosen at runtime and uploaded code cannot mutate the shared cache.
- Artifacts expire according to the File Manager storage policy. Store returned `file_id` values if another tool needs to retrieve or validate them later.

#### Maintenance

- Regenerate `minecraft_mods_service/bedrock_component_registry.json` after updating the pinned Mojang samples archive with `tools/regenerate_bedrock_component_registry.py`.
- Regenerate the public JSON schema after editing `minecraft_mods_service/models.py` with `tools/regenerate_public_tool_schema.py`. The regenerated artifact is written to two locations and checked for byte-equality by `test_schema_single_source.py`.

## When To Use
- Use this skill for `Minecraft Custom Mod Builder` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: minecraft custom mod builder, create runtime verified bedrock add ons and skin packs; build and verify fabric and neoforge jars; generate typed items, blocks, entities, commands, create mod project, target platform, mod id.
- Supported action names: `create_mod_project`, `get_build_job`, `get_instructions`, `list_build_jobs`, `list_capabilities`, `render_preview_image`, `start_build_job`, `validate_mod_project`.

## Use Cases
- Create runtime-verified Bedrock add-ons and skin packs; build and verify Fabric and NeoForge jars; generate typed items
- blocks
- entities
- commands
- events
- recipes
- particles
- sounds
- worldgen
- scoreboards
- processor machines
- storage
- and supported client modules; review File Manager visual_proof galleries before delivery; preview visible assets; download editable source; upload agent-edited source for isolated compile/package/server/client testing; detect broken
- unverified
- or visually inadequate artifacts before installation

## Related Product Skills
- Icon Generator: ../product-icon-generator (ClawHub: `product-icon-generator`, page: https://clawhub.ai/agentpmt/product-icon-generator; skills.sh: `npx skills add AgentPMT/agent-skills --skill product-icon-generator`)
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `8`.
x402 action routes are enabled and listed in `./schema.md`.

- `create_mod_project` (action slug: `create-mod-project`): Synchronous unverified source/debug generation. Accepts only verification_level='off'; use start_build_job for install-ready final artifacts. Price: `15` credits. Parameters: `advanced_resources`, `allow_experimental_bedrock_features`, `assets`, `authoring_mode`, `build_jar`, `compatibility_mode`, `description`, `features`, plus 12 more.
- `get_build_job` (action slug: `get-build-job`): Fetch one tenant-scoped build job by task_id. Poll until status is completed or failed, then inspect result.runtime_verification, result.visual_proof (File Manager frame file_ids/signed_urls; also in artifacts with label=visual_proof_frame), result.quality_gate, result.ready_for_install, and artifacts. Open visual proof frames before customer delivery. Price: `2` credits. Parameters: `task_id`.
- `get_instructions` (action slug: `get-instructions`): Get tool instructions and available actions. Price: `15` credits. Parameters: none.
- `list_build_jobs` (action slug: `list-build-jobs`): List recent Minecraft build jobs for the active budget to recover task_id values or inspect recent queued/completed builds. Price: `2` credits. Parameters: `limit`.
- `list_capabilities` (action slug: `list-capabilities`): Return supported platforms, pinned versions, feature/action matrices, implementation_status, quality-gate fields, and unsupported families. Price: `2` credits. Parameters: `target_platform`.
- `render_preview_image` (action slug: `render-preview-image`): Render and upload an enlarged PNG preview for an item, block, or entity from a structured spec, source archive, or direct image file. Price: `5` credits. Parameters: `features`, `mod_id`, `mod_name`, `preview_background`, `preview_size`, `preview_source_file_id`, `preview_target_id`, `preview_target_kind`, plus 3 more.
- `start_build_job` (action slug: `start-build-job`): Queue generated or agent-edited source for compile, package, real Minecraft runtime checks, File Manager visual_proof gallery, and the install-readiness gate. Poll get_build_job and ship only when result.ready_for_install=true and quality_gate.status='passed', after reviewing visual_proof frames. Price: `15` credits. Parameters: `advanced_resources`, `allow_experimental_bedrock_features`, `assets`, `authoring_mode`, `build_jar`, `compatibility_mode`, `description`, `features`, plus 15 more.
- `validate_mod_project` (action slug: `validate-mod-project`): Validate a structured Minecraft mod spec or a previously generated/uploaded source archive without writing install artifacts. Price: `5` credits. Parameters: `allow_experimental_bedrock_features`, `features`, `minecraft_version`, `mod_id`, `mod_name`, `skin_pack`, `source_archive_file_id`, `target_platform`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "minecraft-custom-mod-builder"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "minecraft-custom-mod-builder"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "minecraft-custom-mod-builder"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "minecraft-custom-mod-builder"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "minecraft-custom-mod-builder"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "minecraft-custom-mod-builder"
  }
}
```

## Call This Tool
Product slug: `minecraft-custom-mod-builder`

Marketplace page: https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account AgentAddress/x402 route: first use `../agentpmt-no-account-agentaddress-x402` for the canonical payment and wallet setup instructions.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
  - OpenClaw install: `openclaw skills install agentpmt-no-account-agentaddress-x402`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Minecraft-Custom-Mod-Builder",
    "arguments": {
      "action": "create_mod_project",
      "advanced_resources": [
        {}
      ],
      "allow_experimental_bedrock_features": true,
      "assets": {},
      "authoring_mode": "auto",
      "build_jar": true,
      "compatibility_mode": "strict",
      "description": "example description",
      "features": {}
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "minecraft-custom-mod-builder",
  "parameters": {
    "action": "create_mod_project",
    "advanced_resources": [
      {}
    ],
    "allow_experimental_bedrock_features": true,
    "assets": {},
    "authoring_mode": "auto",
    "build_jar": true,
    "compatibility_mode": "strict",
    "description": "example description",
    "features": {}
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_mod_project` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
