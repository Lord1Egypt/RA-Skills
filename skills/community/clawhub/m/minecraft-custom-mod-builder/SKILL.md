---
name: minecraft-custom-mod-builder
description: "Minecraft Custom Mod Builder: Deterministically generate and preview Minecraft Bedrock, Bedrock skin pack, Fabric, and NeoForge mod artifacts from structured specs. Use when an agent needs minecraft custom mod builder, create installable minecraft bedrock add ons (.mcaddon) from a simple description, build java mods for fabric and neoforge and download the .jar, design custom swords, pickaxes, create mod project, target platform, mod id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder"}}
---
# Minecraft Custom Mod Builder

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Create your own custom Minecraft mods and add-ons — no coding required. Just describe what you want to add to the game, from a flaming sword or a glowing ore to a rideable mob, a custom skin pack, or a whole new dimension, and get back a ready-to-install file in seconds. Build for Minecraft Bedrock (.mcaddon) and Java with Fabric and NeoForge (.jar). Create items, weapons, tools, armor, blocks, ores, food, mobs, bosses, biomes, structures, recipes, loot tables, enchantments, trades, and special in-game behavior — each with its own custom texture from a color, your own artwork, or generated pixel art. Preview every icon before you install, and download editable source so you can keep building. Perfect for creators, streamers, server owners, and players who want their own Minecraft content fast.

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
* `color_hex` — an explicit `#RRGGBB` color. Only `item_kind in {tool, weapon}` (with `tool_type`) and the dedicated `texture_kind in {block, entity}` paths produce a recognizable sprite (sword/pickaxe/axe/shovel/hoe; shaded block face; humanoid silhouette). For every other kind — `generic`, `food`, `fuel`, `projectile`, `block_placer`, `entity_placer`, `armor`, particles, machines, storage — `color_hex` renders only as a flat colored 16×16 square. That is appropriate for raw materials (ingots, dust, gems) but looks like a missing texture for armor/food/machines. **Use `source_base64` or `source_file_id` whenever the item's identity is visual** (armor, food, machines, storage, projectiles). Tool/weapon `color_hex` requires `tool_type`; otherwise rejected.

A spec that omits the texture binding is rejected at validation with `MINECRAFT_VISIBLE_ASSET_TEXTURE_REQUIRED`. There is no procedural blob fallback. If you want the user to see something, you supply the texture.

**Armor pieces must ship a real PNG.** `item_kind="armor"` rejects `color_hex`-only textures (`MINECRAFT_ARMOR_TEXTURE_REQUIRES_IMAGE`) — the procedural sprite for armor is a flat colored square, which looks broken on the wearer model and in inventory. Supply `source_base64` or `source_file_id` for every helmet/chestplate/leggings/boots.

##### Authoring textures with the Icon Generator + `pixelize_to`

The canonical way to author textures for items, blocks, entities, and particles is the **Icon Generator** (`/product-icon-generator`). Render at the exact target grid in `pixel_art_mode=true` — 16×16 for items and blocks, 64×64 for entities and skin packs — and pipe the returned `file_id` straight into this texture's `source_file_id`. Detailed recipes live in `agent_instructions/minecraft_texture_agent.md`.

When the texture originates outside the Icon Generator (AI image creator, user upload, third-party source), use the ingest-side safety net by setting `texture.pixelize_to` and optionally `texture.palette_colors`. Both fields are opt-in (`None` by default) so existing bindings remain byte-identical. Example: `{"texture": {"source_file_id": "abc...", "pixelize_to": 16, "palette_colors": 8}}` nearest-neighbor downscales the input to 16×16 and quantizes it to an 8-color palette with dithering disabled, producing crisp pixel-art output regardless of how the source was made. Failures surface as `MINECRAFT_TEXTURE_PIXELIZE_FAILED`.

Recommended defaults unless you have a specific reason to deviate: items/blocks → `pixelize_to: 16, palette_colors: 8`; entities/skins → `pixelize_to: 64, palette_colors: 16`; particles → `pixelize_to: 16, palette_colors: 4`. The `color_hex` binding path is unaffected — it already produces crisp procedural sprites.

#### Quick Recipes

##### Diamond sword
```json
{"items":[{"item_id":"flame_sword","display_name":"Flame Sword","item_kind":"weapon","tool_type":"sword","tool_tier":"diamond","damage":7,"texture":{"color_hex":"#ff5522"}}]}
```

##### Iron pickaxe
```json
{"items":[{"item_id":"iron_pickaxe","display_name":"Iron Pickaxe","item_kind":"tool","tool_type":"pickaxe","tool_tier":"iron","texture":{"color_hex":"#cccccc"}}]}
```

##### Custom-texture armor set
```json
{"items":[
  {"item_id":"set_helmet","display_name":"Set Helmet","item_kind":"armor","tool_tier":"diamond","armor":{"slot":"head","protection":3,"toughness":2},"texture":{"source_file_id":"<file_id>","pixelize_to":16,"palette_colors":8}},
  {"item_id":"set_chest","display_name":"Set Chest","item_kind":"armor","tool_tier":"diamond","armor":{"slot":"chest","protection":8,"toughness":2},"texture":{"source_file_id":"<file_id>","pixelize_to":16,"palette_colors":8}},
  {"item_id":"set_legs","display_name":"Set Legs","item_kind":"armor","tool_tier":"diamond","armor":{"slot":"legs","protection":6,"toughness":2},"texture":{"source_file_id":"<file_id>","pixelize_to":16,"palette_colors":8}},
  {"item_id":"set_boots","display_name":"Set Boots","item_kind":"armor","tool_tier":"diamond","armor":{"slot":"feet","protection":3,"toughness":2},"texture":{"source_file_id":"<file_id>","pixelize_to":16,"palette_colors":8}}
]}
```

##### Block + matching ore
```json
{"blocks":[{"block_id":"raw_obsidium","display_name":"Raw Obsidium","block_kind":"basic","hardness":3.0,"resistance":12,"texture":{"color_hex":"#2a0033"}}],"worldgen":[{"feature_id":"obsidium_ore","feature_kind":"ore_feature","block_id":"raw_obsidium","vein_size":4,"count_per_chunk":2,"min_y":0,"max_y":48,"biomes":["minecraft:overworld"]}]}
```

##### Passive entity (sheep-like)
```json
{"entities":[{"entity_id":"cloudling","display_name":"Cloudling","entity_kind":"passive_mob","health":12,"texture":{"source_file_id":"<file_id>","pixelize_to":64,"palette_colors":16}}]}
```

##### Sword with on-hit fire event
```json
{"items":[{"item_id":"flame_sword","display_name":"Flame Sword","item_kind":"weapon","tool_type":"sword","tool_tier":"diamond","damage":7,"texture":{"color_hex":"#ff5522"}}],"events":[{"event_id":"flame_sword_ignite","event_kind":"on_item_hit_entity","conditions":[{"condition_kind":"held_item","identifier":"modid:flame_sword"}],"actions":[{"action_kind":"set_on_fire","duration_ticks":120}]}]}
```

##### Skin pack (Bedrock)
```json
{"action":"create_mod_project","target_platform":"bedrock_skinpack","mod_id":"blue_pack","mod_name":"Blue Pack","skin_pack":{"pack_id":"blue_pack","display_name":"Blue Pack","skins":[{"skin_id":"blue_hero","display_name":"Blue Hero","texture":{"source_base64":"<base64-encoded 64x64 PNG>"}}]}}
```

Skin pack textures must be exactly 64×64 PNG.

#### Verify Every Generation

Always follow `create_mod_project` with a `render_preview_image` call against the just-generated `mod_id`. The preview confirms the icon renders correctly before you ask the user to install. If the preview looks like a flat colored square or the wrong tool sprite, you forgot `item_kind`, `tool_type`, or both.

#### Common Mistakes

| Mistake | What happens now |
|---|---|
| `item_kind="generic"` on a weapon with `damage` set | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="tool"` without `tool_type` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="weapon"` with `tool_type="pickaxe"` | Rejected: weapon requires `sword` or `custom` |
| `item_kind="armor"` without `armor` or `wearable` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `item_kind="food"` without `food` preset or `nutrition` | Rejected: `MINECRAFT_ITEM_KIND_REQUIRES_PRESET` |
| `texture` omitted on any visible asset | Rejected: `MINECRAFT_VISIBLE_ASSET_TEXTURE_REQUIRED` |
| `texture: {}` with no `color_hex`, `source_base64`, or `source_file_id` | Rejected: `MINECRAFT_TEXTURE_SOURCE_REQUIRED` |
| `item_kind="armor"` with `texture: {color_hex: ...}` only | Rejected: `MINECRAFT_ARMOR_TEXTURE_REQUIRES_IMAGE` |
| `pixelize_to` set to a value other than 16, 32, 64, or 128 | Rejected: schema validation |
| Source image fails to decode during pixelize | `MINECRAFT_TEXTURE_PIXELIZE_FAILED` |
| Pickaxe specced to "break any block" but only breaks a few | Add `tool.break_all_blocks: true` |
| Feature appears in the wrong platform build | Set `enabled_platforms: ["bedrock"]` (or fabric/neoforge) |
| Block `drops` references an item id that doesn't exist | Rejected with `MINECRAFT_SPEC_VALIDATION_FAILED` |
| Multiple `items[]` entries for one weapon | Two items in inventory; collapse to one ItemSpec |
| `on_item_hit_entity` without a `held_item` condition | Fires for every hit; add a `held_item` condition |
| `command_id` shadowing a Minecraft command (e.g. `give`, `tp`) | Reject or behavior conflict; pick a unique id |

#### Supported Platforms

- `bedrock`: Minecraft Bedrock add-on generation. Produces `.mcaddon` installables and Mojang Minecraft Creator Tools validation reports.
- `fabric`: Minecraft Java Fabric generation. Produces source zips and optional built jars.
- `neoforge`: Minecraft Java NeoForge generation. Produces source zips and optional built jars.
- `bedrock_skinpack`: Bedrock skin pack generation. Produces `.mcpack` files.
- `forge` is retired. Use `neoforge`.

#### Texture Binding Fields (BindingTextureSpec)

Every visible asset's `texture` field is a `BindingTextureSpec`. Required: exactly one of `color_hex`, `source_base64`, or `source_file_id`.

Optional ingest-side transforms:
- `pixelize_to`: integer in `{16, 32, 64, 128}`. Nearest-neighbor downscales the source image to that square dimension before baking.
- `palette_colors`: integer 2-256. Quantizes the (post-pixelize) image to the requested palette size via Fast Octree (no dither).

Both fields default to `None` (no transform). They only affect the `source_base64` and `source_file_id` paths; `color_hex` renders are unaffected.

#### Actions

- `list_capabilities`: Return the supported feature/event/action matrix for a target platform.
- `validate_mod_project`: Validate a spec without writing artifacts. Use to check coherence before paying for `create_mod_project`.
- `create_mod_project`: Validate + generate the mod artifact. Returns source zip and/or installable archive paths.
- `render_preview_image`: Render an enlarged preview of a generated texture/icon for verification.

#### Output Behavior

- Bedrock `installable` returns a `.mcaddon` and validation report. With `validate_output=true`, Mojang Minecraft Creator Tools validates the generated add-on.
- Fabric/NeoForge `installable` returns a jar when `build_jar=true`; otherwise use `source` for source zips only.
- `render_preview_image` returns a preview artifact with a PNG `file_id`, signed URL, and image metadata.
- Artifacts expire according to the File Manager storage policy.

## When To Use
- Use this skill for `Minecraft Custom Mod Builder` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: minecraft custom mod builder, create installable minecraft bedrock add ons (.mcaddon) from a simple description, build java mods for fabric and neoforge and download the .jar, design custom swords, pickaxes, create mod project, target platform, mod id.
- Supported action names: `create_mod_project`, `list_capabilities`, `render_preview_image`, `validate_mod_project`.

## Use Cases
- Create installable Minecraft Bedrock add-ons (.mcaddon) from a simple description
- Build Java mods for Fabric and NeoForge and download the .jar
- Design custom swords
- pickaxes
- tools
- and armor with their own textures
- Add new blocks
- ores
- and crops with world generation
- Create custom mobs from passive animals to hostile bosses and tameable pets
- Make Bedrock skin packs (.mcpack) for a fresh character look
- Give items special behavior like a sword that sets enemies on fire
- Add custom crafting recipes
- loot tables
- enchantments
- and villager trades

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `create_mod_project` (action slug: `create-mod-project`): Generate mod artifacts and upload them to File Manager. Returns artifact file_ids, signed URLs, generated file manifests, validation results, install instructions, warnings, and build reports. Always follow this call with render_preview_image to confirm the icon before asking the user to install. Price: `25` credits. Parameters: `advanced_resources`, `allow_experimental_bedrock_features`, `assets`, `build_jar`, `compatibility_mode`, `description`, `features`, `include_file_preview`, plus 8 more.
- `list_capabilities` (action slug: `list-capabilities`): Return supported platforms, pinned dependencies, feature kinds, event kinds, action kinds, output artifacts, unsupported categories, the v2 schema version, the major capability matrix, and the Bedrock component registry derived from the pinned Mojang Bedrock Samples archive. Price: `25` credits. Parameters: `target_platform`.
- `render_preview_image` (action slug: `render-preview-image`): Render an enlarged PNG preview for an item/block/entity texture and upload it to File Manager. Three modes: (1) spec preview — pass target_platform, mod_id, mod_name, features; (2) archive preview — pass source_archive_file_id; (3) direct image preview — pass preview_source_file_id. Returns a preview artifact with PNG file_id, signed URL, and image metadata. Price: `25` credits. Parameters: `advanced_resources`, `allow_experimental_bedrock_features`, `assets`, `compatibility_mode`, `description`, `features`, `minecraft_version`, `mod_id`, plus 10 more.
- `validate_mod_project` (action slug: `validate-mod-project`): Validate either a structured mod specification (spec mode) or a previously generated source archive (archive mode). Spec mode: provide target_platform, mod_id, mod_name, features (or skin_pack for skinpacks). Archive mode: provide source_archive_file_id. Returns a validation report with error codes and warnings; does NOT write artifacts. Price: `25` credits. Parameters: `advanced_resources`, `allow_experimental_bedrock_features`, `assets`, `compatibility_mode`, `description`, `features`, `minecraft_version`, `mod_id`, plus 5 more.

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
- x402 route: not enabled for this product.
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

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
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
      "build_jar": true,
      "compatibility_mode": "strict",
      "description": "example description",
      "features": {
        "animation_controllers": [
          {}
        ],
        "animations": [
          {}
        ],
        "biomes": [
          {}
        ],
        "blocks": [
          {
            "block_id": "example block id",
            "block_kind": "basic",
            "collision_box": {},
            "component_overrides": [
              {}
            ],
            "crafting_table": false,
            "crop": {},
            "custom_components": [
              "example custom component"
            ],
            "description": "example description"
          }
        ],
        "commands": [
          {
            "actions": [
              {}
            ],
            "command_id": "example command id",
            "command_kind": "simple_command",
            "description": "example description",
            "enabled_platforms": [
              "bedrock"
            ],
            "parameters": [
              {}
            ],
            "permission_level": "any"
          }
        ],
        "damage_types": [
          {}
        ],
        "dimensions": [
          {}
        ],
        "effects": [
          {}
        ]
      },
      "include_file_preview": true
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
    "build_jar": true,
    "compatibility_mode": "strict",
    "description": "example description",
    "features": {
      "animation_controllers": [
        {}
      ],
      "animations": [
        {}
      ],
      "biomes": [
        {}
      ],
      "blocks": [
        {
          "block_id": "example block id",
          "block_kind": "basic",
          "collision_box": {},
          "component_overrides": [
            {}
          ],
          "crafting_table": false,
          "crop": {},
          "custom_components": [
            "example custom component"
          ],
          "description": "example description"
        }
      ],
      "commands": [
        {
          "actions": [
            {}
          ],
          "command_id": "example command id",
          "command_kind": "simple_command",
          "description": "example description",
          "enabled_platforms": [
            "bedrock"
          ],
          "parameters": [
            {}
          ],
          "permission_level": "any"
        }
      ],
      "damage_types": [
        {}
      ],
      "dimensions": [
        {}
      ],
      "effects": [
        {}
      ]
    },
    "include_file_preview": true
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
- Marketplace product: https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
