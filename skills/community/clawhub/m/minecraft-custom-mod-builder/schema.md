# Minecraft Custom Mod Builder Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `minecraft-custom-mod-builder`

x402 availability: not enabled for this product.

## `create_mod_project`

Action slug: `create-mod-project`

Price: `25` credits

Generate mod artifacts and upload them to File Manager. Returns artifact file_ids, signed URLs, generated file manifests, validation results, install instructions, warnings, and build reports. Always follow this call with render_preview_image to confirm the icon before asking the user to install.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advanced_resources` | `array` | no | Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64\|content_text\|source_file_id, content_type}. |
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock features that require experimental world toggles. |
| `assets` | `object` | no | Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape. |
| `build_jar` | `boolean` | no | Fabric/NeoForge only; build the jar offline when true. |
| `compatibility_mode` | `string` | no | {"default": "strict", "enum": ["strict", "allow_platform_passthrough"]} |
| `description` | `string` | no | Short mod description shown in the pack metadata. |
| `features` | `object` | no | Structured feature set. Required when target_platform is bedrock/fabric/neoforge. Omit when target_platform='bedrock_skinpack' (use skin_pack instead). |
| `include_file_preview` | `boolean` | no | Include capped previews for small generated text files in the response. |
| `minecraft_version` | `string` | no | Pinned Minecraft version. Omit to use the platform default. |
| `mod_id` | `string` | yes | Required. Lowercase ^[a-z][a-z0-9_]{1,63}$. Becomes the mod namespace in generated identifiers (e.g. <mod_id>:flame_sword). |
| `mod_metadata` | `object` | no | Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape. |
| `mod_name` | `string` | yes | Human-readable mod name shown in the pack list. |
| `output_mode` | `string` | no | Artifact mode: 'installable' (.mcaddon/.mcpack/.jar only), 'source' (zip only), or 'both'. |
| `skin_pack` | `object` | no | Skin pack definition. Required when target_platform='bedrock_skinpack'. |
| `target_platform` | `string` | yes | Required. One of bedrock, bedrock_skinpack, fabric, neoforge. Legacy 'forge' is rejected with a migration error pointing to 'neoforge'. |
| `validate_output` | `boolean` | no | Run platform validation (Bedrock Creator Tools) where available. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "advanced_resources": {
    "description": "Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64|content_text|source_file_id, content_type}.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock features that require experimental world toggles.",
    "required": false,
    "type": "boolean"
  },
  "assets": {
    "description": "Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape.",
    "required": false,
    "type": "object"
  },
  "build_jar": {
    "default": true,
    "description": "Fabric/NeoForge only; build the jar offline when true.",
    "required": false,
    "type": "boolean"
  },
  "compatibility_mode": {
    "default": "strict",
    "enum": [
      "strict",
      "allow_platform_passthrough"
    ],
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Short mod description shown in the pack metadata.",
    "required": false,
    "type": "string"
  },
  "features": {
    "description": "Structured feature set. Required when target_platform is bedrock/fabric/neoforge. Omit when target_platform='bedrock_skinpack' (use skin_pack instead).",
    "properties": {
      "animation_controllers": {
        "items": {
          "description": "AnimationControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "animations": {
        "items": {
          "description": "AnimationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "biomes": {
        "items": {
          "description": "BiomeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "blocks": {
        "items": {
          "properties": {
            "block_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game block id.",
              "required": true,
              "type": "string"
            },
            "block_kind": {
              "default": "basic",
              "description": "Block class. 'basic' = stone-like solid block. 'ore' = drops items via the drops field when mined with the correct tool. 'light' = emits full light (use light_level to override). 'interactive' = supports right-click handlers via events. 'crop' / 'plant' = grows over time via the crop preset. 'redstone' = signal-aware (use redstone preset). 'machine' = container that runs a recipe (pair with the matching MachineSpec). 'container' = inventory storage (pair with the matching StorageSpec).",
              "enum": [
                "basic",
                "ore",
                "light",
                "interactive",
                "crop",
                "plant",
                "redstone",
                "machine",
                "container"
              ],
              "required": false,
              "type": "string"
            },
            "collision_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "crafting_table": {
              "default": false,
              "required": false,
              "type": "boolean"
            },
            "crop": {
              "description": "CropSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable block name shown to players.",
              "required": true,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "flammable": {
              "properties": {
                "catch_chance_modifier": {
                  "default": 5,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "destroy_chance_modifier": {
                  "default": 20,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "friction": {
              "maximum": 1,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "hardness": {
              "maximum": 100,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "light_level": {
              "maximum": 15,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "map_color": {
              "required": false,
              "type": "string"
            },
            "material_instances": {
              "additionalProperties": {
                "description": "MaterialInstanceSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "object"
            },
            "placement_filter": {
              "description": "PlacementFilterSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "redstone": {
              "description": "RedstoneSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "resistance": {
              "maximum": 10000,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "selection_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the block face. See BindingTextureSpec.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "tick": {
              "properties": {
                "interval_range": {
                  "items": {
                    "type": "integer"
                  },
                  "maxItems": 2,
                  "minItems": 2,
                  "required": false,
                  "type": "array"
                },
                "looping": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "commands": {
        "items": {
          "properties": {
            "actions": {
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "required": false,
              "type": "array"
            },
            "command_id": {
              "required": true,
              "type": "string"
            },
            "command_kind": {
              "enum": [
                "simple_command",
                "argument_command",
                "function_command",
                "admin_command"
              ],
              "required": true,
              "type": "string"
            },
            "description": {
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "parameters": {
              "items": {
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "permission_level": {
              "default": "any",
              "enum": [
                "any",
                "op",
                "admin"
              ],
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "damage_types": {
        "items": {
          "description": "DamageTypeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "dimensions": {
        "items": {
          "description": "DimensionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "effects": {
        "items": {
          "description": "EffectSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "enchantments": {
        "items": {
          "description": "EnchantmentSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "entities": {
        "items": {
          "properties": {
            "ai_goals": {
              "items": {
                "description": "EntityAIGoalSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "attack_damage": {
              "description": "Melee damage on attack. Default derived from entity_kind.",
              "maximum": 512,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "breedable": {
              "description": "EntityBreedableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable entity name shown in death messages and the spawn-egg tooltip.",
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "entity_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game entity id.",
              "required": true,
              "type": "string"
            },
            "entity_kind": {
              "description": "Mob class. Controls AI defaults, spawn category, and renderer registration. 'passive_mob' = cow/sheep-like, never attacks. 'hostile_mob' = zombie-like, attacks players on sight. 'neutral_mob' = wolf-like, attacks when hurt. 'tameable_pet' = wolf-like with taming behavior (requires tameable preset). 'rideable_mount' = horse-like (requires rideable preset). 'projectile' = arrow-like flying entity. 'npc_like' = villager-like with trades (use interactions preset). 'boss_like' = ender-dragon-like with boss bar.",
              "enum": [
                "passive_mob",
                "hostile_mob",
                "neutral_mob",
                "projectile",
                "npc_like",
                "tameable_pet",
                "rideable_mount",
                "boss_like"
              ],
              "required": true,
              "type": "string"
            },
            "equipment": {
              "description": "EntityEquipmentSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "families": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "health": {
              "default": 20,
              "description": "Maximum health points (each heart = 2 HP).",
              "maximum": 2048,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "interactions": {
              "items": {
                "description": "EntityInteractionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "loot_table": {
              "required": false,
              "type": "string"
            },
            "movement_speed": {
              "default": 0.25,
              "description": "Walking speed. Vanilla baseline is 0.25 for passive mobs.",
              "maximum": 5,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "render": {
              "description": "EntityRenderSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "rideable": {
              "description": "EntityRideableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "spawn_biomes": {
              "description": "Biome ids (minecraft:plains, etc.) where the mob can naturally spawn.",
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "spawn_weight": {
              "default": 10,
              "description": "Relative spawn weight in eligible biomes.",
              "maximum": 1000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "tameable": {
              "description": "EntityTameableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the entity model and its spawn-egg icon. Bedrock uses a 64x64 humanoid-style atlas by default; supply a 64x64 PNG via source_base64 or source_file_id to override.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "events": {
        "items": {
          "properties": {
            "actions": {
              "description": "Required non-empty list of actions to execute when the event fires.",
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "conditions": {
              "items": {
                "description": "ConditionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 20,
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "event_id": {
              "required": true,
              "type": "string"
            },
            "event_kind": {
              "description": "Event trigger. Filter to a specific item/block/entity with conditions; emit behavior with actions. Example: pair 'on_item_hit_entity' with a {condition_kind:'held_item', identifier:'modid:flame_sword'} condition and a {action_kind:'set_on_fire', duration_ticks:100} action to make a flame sword.",
              "enum": [
                "on_item_use",
                "on_item_hit_entity",
                "on_item_mine_block",
                "on_item_inventory_tick",
                "on_entity_spawn",
                "on_entity_death",
                "on_entity_hurt",
                "on_entity_tick",
                "on_player_tick",
                "on_player_join",
                "on_player_respawn",
                "on_block_break",
                "on_block_interact",
                "on_block_place",
                "on_block_tick",
                "on_projectile_hit",
                "on_enter_biome",
                "on_command",
                "on_inventory_change",
                "on_redstone_change",
                "on_machine_recipe_complete"
              ],
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "functions": {
        "items": {
          "description": "FunctionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "game_rules": {
        "items": {
          "description": "GameRuleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "items": {
        "items": {
          "properties": {
            "allow_off_hand": {
              "required": false,
              "type": "boolean"
            },
            "armor": {
              "description": "Armor preset (slot + protection). Required when item_kind='armor' unless wearable is set.",
              "properties": {
                "dyeable": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "knockback_resistance": {
                  "default": 0,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "protection": {
                  "default": 1,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "enum": [
                    "head",
                    "chest",
                    "legs",
                    "feet"
                  ],
                  "required": true,
                  "type": "string"
                },
                "toughness": {
                  "default": 0,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "trim_supported": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "block_placer": {
              "description": "Block id or preset; required when item_kind='block_placer'.",
              "required": false,
              "type": "string"
            },
            "bundle_interaction": {
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "compostable": {
              "properties": {
                "chance": {
                  "default": 0.3,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "cooldown": {
              "properties": {
                "category": {
                  "default": "generic",
                  "required": false,
                  "type": "string"
                },
                "cooldown_type": {
                  "default": "use",
                  "description": "Cooldown trigger. 'use' fires on right-click activation; 'attack' fires on swing. Accepts cooldown_type or type as input.",
                  "enum": [
                    "use",
                    "attack"
                  ],
                  "required": false,
                  "type": "string"
                },
                "duration_seconds": {
                  "default": 1,
                  "maximum": 3600,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "damage": {
              "description": "Attack damage when held. Used by item_kind in {'tool','weapon'}; default derives from tool_tier.",
              "maximum": 231,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "digger": {
              "properties": {
                "destroy_speeds": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "use_efficiency": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "display_name": {
              "description": "Human-readable item name shown to players in inventory tooltips.",
              "required": true,
              "type": "string"
            },
            "durability": {
              "description": "Use count before the item breaks. Used by tool/weapon/armor; default derives from tool_tier.",
              "maximum": 100000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "dyeable": {
              "description": "DyeableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enchantable": {
              "properties": {
                "slot": {
                  "default": "pickaxe",
                  "required": false,
                  "type": "string"
                },
                "value": {
                  "default": 10,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "entity_placer": {
              "description": "Entity id or preset (spawn-egg-like); required when item_kind='entity_placer'.",
              "required": false,
              "type": "string"
            },
            "fire_resistant": {
              "required": false,
              "type": "boolean"
            },
            "foil": {
              "required": false,
              "type": "boolean"
            },
            "food": {
              "description": "Food preset (nutrition, saturation, effects). Required when item_kind='food' unless nutrition is set.",
              "properties": {
                "can_always_eat": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "effects": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "nutrition": {
                  "default": 4,
                  "maximum": 20,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "remove_effects": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "saturation_modifier": {
                  "default": 0.6,
                  "required": false,
                  "type": "number"
                },
                "use_modifiers": {
                  "description": "UseModifierSpec object. See get_instructions for the full shape.",
                  "required": false,
                  "type": "object"
                },
                "using_converts_to": {
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "fuel": {
              "properties": {
                "duration_seconds": {
                  "default": 5,
                  "exclusiveMinimum": 0,
                  "maximum": 3600,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "glint": {
              "required": false,
              "type": "boolean"
            },
            "hover_text_color": {
              "required": false,
              "type": "string"
            },
            "interact_button": {
              "required": false,
              "type": "string"
            },
            "item_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game item id.",
              "required": true,
              "type": "string"
            },
            "item_kind": {
              "default": "generic",
              "description": "Behavior class. Drives icon sprite, creative-tab placement, stack size, and which preset fields are required. 'weapon' = sword-like, lands in Equipment tab, requires tool_type in {'sword','custom'}. 'tool' = pickaxe/axe/shovel/hoe, lands in Equipment tab, requires tool_type. 'armor' = head/chest/legs/feet, lands in Equipment tab, requires armor preset. 'food' = eatable, requires food preset or nutrition. 'projectile' = arrow-like, requires projectile/shooter/throwable. 'block_placer' / 'entity_placer' = spawn-egg-like, requires matching preset. 'fuel' = furnace fuel. 'generic' = raw material only (sticks, ingots, dust); rejects any combat/tool/armor/food preset.",
              "enum": [
                "generic",
                "tool",
                "weapon",
                "armor",
                "food",
                "fuel",
                "projectile",
                "block_placer",
                "entity_placer"
              ],
              "required": false,
              "type": "string"
            },
            "kinetic_weapon": {
              "required": false,
              "type": "object"
            },
            "liquid_clipped": {
              "required": false,
              "type": "boolean"
            },
            "max_stack_size": {
              "description": "Inventory stack size. Defaults to 1 for tool/weapon/armor/projectile and 64 for generic/food.",
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "nutrition": {
              "description": "Food hunger points restored on consumption. Required (with food preset) when item_kind='food'.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "piercing_weapon": {
              "required": false,
              "type": "object"
            },
            "projectile": {
              "description": "Projectile preset. One of projectile/shooter/throwable required when item_kind='projectile'.",
              "properties": {
                "minimum_critical_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "projectile_entity": {
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "rarity": {
              "description": "RaritySpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "record": {
              "required": false,
              "type": "object"
            },
            "repairable": {
              "properties": {
                "repair_items": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                }
              },
              "required": false,
              "type": "object"
            },
            "saturation": {
              "description": "Food saturation modifier paired with nutrition.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "shooter": {
              "description": "Bow-like shooter preset that consumes ammunition items.",
              "properties": {
                "ammunition": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "charge_on_draw": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "scale_power_by_draw_duration": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "search_inventory": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "use_in_creative": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "should_despawn": {
              "required": false,
              "type": "boolean"
            },
            "stacked_by_data": {
              "required": false,
              "type": "boolean"
            },
            "swing_sounds": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "texture": {
              "description": "Required visible-asset texture. Supply one of source_base64, source_file_id, or color_hex. color_hex paired with item_kind+tool_type renders a kind-shaped procedural sprite (sword, pickaxe, axe, shovel, or hoe).",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "throwable": {
              "description": "Throwable preset (snowball-like behavior).",
              "properties": {
                "do_swing_animation": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "launch_power_scale": {
                  "default": 1,
                  "exclusiveMinimum": 0,
                  "maximum": 10,
                  "required": false,
                  "type": "number"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "max_launch_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool": {
              "description": "Explicit tool preset overriding tool_type/tool_tier defaults.",
              "properties": {
                "attack_damage": {
                  "default": 4,
                  "maximum": 231,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "attack_speed": {
                  "default": 1.6,
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "break_all_blocks": {
                  "default": false,
                  "description": "When true, the tool can mine every block at full speed regardless of the vanilla pickaxe/axe/shovel/hoe destructible tag. Bedrock emits a Molang-true tag predicate on minecraft:digger; Java emits a tier that ignores TagBlockEntries restrictions. Combine with instabreak for a creative-mode super-tool.",
                  "required": false,
                  "type": "boolean"
                },
                "digger": {
                  "properties": {
                    "destroy_speeds": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "use_efficiency": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "enchantable": {
                  "properties": {
                    "slot": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "value": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "instabreak": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "mining_speed": {
                  "default": 4,
                  "exclusiveMinimum": 0,
                  "maximum": 2048,
                  "required": false,
                  "type": "number"
                },
                "repairable": {
                  "properties": {
                    "repair_items": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "tier": {
                  "default": "iron",
                  "enum": [
                    "wood",
                    "stone",
                    "iron",
                    "gold",
                    "diamond",
                    "netherite",
                    "custom"
                  ],
                  "required": false,
                  "type": "string"
                },
                "tool_type": {
                  "enum": [
                    "pickaxe",
                    "axe",
                    "shovel",
                    "hoe",
                    "sword",
                    "custom"
                  ],
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool_tier": {
              "description": "Tier preset. Determines default durability, attack damage, mining speed, enchantability, and repair material. Defaults to 'iron' when omitted on a tool/weapon. 'custom' opts out of all tier defaults.",
              "enum": [
                "wood",
                "stone",
                "iron",
                "gold",
                "diamond",
                "netherite",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "tool_type": {
              "description": "Tool kind. Controls the rendered icon sprite when color_hex is the texture source, the destructible-block tag, and the Equipment-tab sub-group. Required when item_kind='tool'. Use 'sword' for item_kind='weapon'. 'custom' opts out of the kind-specific defaults so the spec must declare its own damage/durability/digger.",
              "enum": [
                "pickaxe",
                "axe",
                "shovel",
                "hoe",
                "sword",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "use_modifiers": {
              "description": "UseModifierSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "wearable": {
              "properties": {
                "protection": {
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "default": "slot.armor.head",
                  "enum": [
                    "slot.armor.head",
                    "slot.armor.chest",
                    "slot.armor.legs",
                    "slot.armor.feet",
                    "slot.weapon.offhand"
                  ],
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "localizations": {
        "items": {
          "description": "LocalizationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "loot_tables": {
        "items": {
          "properties": {
            "conditions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "maxItems": 64,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "functions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "loot_id": {
              "required": true,
              "type": "string"
            },
            "target": {
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "machines": {
        "items": {
          "description": "MachineSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "particles": {
        "items": {
          "description": "ParticleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "recipes": {
        "items": {
          "properties": {
            "addition_item": {
              "required": false,
              "type": "string"
            },
            "base_item": {
              "required": false,
              "type": "string"
            },
            "cooking_time_seconds": {
              "maximum": 3600,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "count": {
              "default": 1,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "ingredients": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "input_item": {
              "required": false,
              "type": "string"
            },
            "key": {
              "additionalProperties": {
                "type": "string"
              },
              "required": false,
              "type": "object"
            },
            "pattern": {
              "items": {
                "type": "string"
              },
              "maxItems": 3,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "recipe_id": {
              "required": true,
              "type": "string"
            },
            "recipe_kind": {
              "default": "shapeless",
              "description": "Recipe class. 'shaped' requires pattern+key. 'shapeless' requires ingredients. 'furnace' requires input_item+cooking_time_seconds. 'smithing_transform' / 'smithing_trim' require template_item+base_item+addition_item. 'brewing_mix' / 'brewing_container' are Bedrock-only.",
              "enum": [
                "shaped",
                "shapeless",
                "furnace",
                "brewing_mix",
                "brewing_container",
                "smithing_transform",
                "smithing_trim"
              ],
              "required": false,
              "type": "string"
            },
            "result_item": {
              "required": true,
              "type": "string"
            },
            "template_item": {
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "render_controllers": {
        "items": {
          "description": "RenderControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "scoreboards": {
        "items": {
          "description": "ScoreboardSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "sounds": {
        "items": {
          "description": "SoundSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "storage": {
        "items": {
          "description": "StorageSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "structures": {
        "items": {
          "description": "StructureSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "trades": {
        "items": {
          "description": "TradeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "transportation": {
        "items": {
          "description": "TransportationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "ui": {
        "items": {
          "description": "UISpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "worldgen": {
        "items": {
          "properties": {
            "biomes": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "block_id": {
              "description": "Block id to place. Required for ore/single_block/vegetation features.",
              "required": false,
              "type": "string"
            },
            "count_per_chunk": {
              "default": 8,
              "maximum": 128,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "feature_id": {
              "required": true,
              "type": "string"
            },
            "feature_kind": {
              "description": "Worldgen feature class. 'ore_feature' places veins of block_id inside target_block. 'single_block_feature' places a single block. 'vegetation_patch' places a plant patch. 'structure_placement' places a stored structure. 'custom_biome' / 'custom_dimension' register a referenced biome/dimension.",
              "enum": [
                "ore_feature",
                "single_block_feature",
                "vegetation_patch",
                "structure_placement",
                "custom_biome",
                "custom_dimension"
              ],
              "required": true,
              "type": "string"
            },
            "max_y": {
              "default": 64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "min_y": {
              "default": -64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "radius": {
              "default": 4,
              "maximum": 32,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "source_file_id": {
              "required": false,
              "type": "string"
            },
            "target_block": {
              "default": "minecraft:stone",
              "required": false,
              "type": "string"
            },
            "vein_size": {
              "default": 6,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "vertical_range": {
              "default": 5,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "include_file_preview": {
    "description": "Include capped previews for small generated text files in the response.",
    "required": false,
    "type": "boolean"
  },
  "minecraft_version": {
    "description": "Pinned Minecraft version. Omit to use the platform default.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Required. Lowercase ^[a-z][a-z0-9_]{1,63}$. Becomes the mod namespace in generated identifiers (e.g. <mod_id>:flame_sword).",
    "required": true,
    "type": "string"
  },
  "mod_metadata": {
    "description": "Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape.",
    "required": false,
    "type": "object"
  },
  "mod_name": {
    "description": "Human-readable mod name shown in the pack list.",
    "required": true,
    "type": "string"
  },
  "output_mode": {
    "default": "both",
    "description": "Artifact mode: 'installable' (.mcaddon/.mcpack/.jar only), 'source' (zip only), or 'both'.",
    "enum": [
      "installable",
      "source",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition. Required when target_platform='bedrock_skinpack'.",
    "properties": {
      "display_name": {
        "required": false,
        "type": "string"
      },
      "pack_id": {
        "required": false,
        "type": "string"
      },
      "skins": {
        "items": {
          "properties": {
            "display_name": {
              "required": true,
              "type": "string"
            },
            "geometry": {
              "default": "geometry.humanoid.custom",
              "enum": [
                "geometry.humanoid.custom",
                "geometry.humanoid.customSlim"
              ],
              "required": false,
              "type": "string"
            },
            "localization_name": {
              "required": false,
              "type": "string"
            },
            "skin_id": {
              "required": true,
              "type": "string"
            },
            "skin_type": {
              "default": "free",
              "description": "Skin type. Accepts skin_type or type as input.",
              "enum": [
                "free",
                "paid"
              ],
              "required": false,
              "type": "string"
            },
            "texture": {
              "description": "Required 64x64 PNG skin texture. Supply source_base64 or source_file_id for a user-drawn skin; color_hex renders a flat humanoid silhouette.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "maxItems": 64,
        "minItems": 1,
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "target_platform": {
    "description": "Required. One of bedrock, bedrock_skinpack, fabric, neoforge. Legacy 'forge' is rejected with a migration error pointing to 'neoforge'.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": true,
    "type": "string"
  },
  "validate_output": {
    "default": true,
    "description": "Run platform validation (Bedrock Creator Tools) where available.",
    "required": false,
    "type": "boolean"
  }
}
```

## `list_capabilities`

Action slug: `list-capabilities`

Price: `25` credits

Return supported platforms, pinned dependencies, feature kinds, event kinds, action kinds, output artifacts, unsupported categories, the v2 schema version, the major capability matrix, and the Bedrock component registry derived from the pinned Mojang Bedrock Samples archive.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `target_platform` | `string` | no | Target platform. 'bedrock' generates a .mcaddon for Minecraft Bedrock Edition. 'bedrock_skinpack' generates a .mcpack skin pack. 'fabric' / 'neoforge' generate Java mod source zips and built jars. |

Sample parameters:

```json
{
  "target_platform": "bedrock"
}
```

Generated JSON parameter schema:

```json
{
  "target_platform": {
    "description": "Target platform. 'bedrock' generates a .mcaddon for Minecraft Bedrock Edition. 'bedrock_skinpack' generates a .mcpack skin pack. 'fabric' / 'neoforge' generate Java mod source zips and built jars.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `render_preview_image`

Action slug: `render-preview-image`

Price: `25` credits

Render an enlarged PNG preview for an item/block/entity texture and upload it to File Manager. Three modes: (1) spec preview — pass target_platform, mod_id, mod_name, features; (2) archive preview — pass source_archive_file_id; (3) direct image preview — pass preview_source_file_id. Returns a preview artifact with PNG file_id, signed URL, and image metadata.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advanced_resources` | `array` | no | Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64\|content_text\|source_file_id, content_type}. |
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock features that require experimental world toggles. |
| `assets` | `object` | no | Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape. |
| `compatibility_mode` | `string` | no | {"default": "strict", "enum": ["strict", "allow_platform_passthrough"]} |
| `description` | `string` | no | Short mod description shown in the pack metadata. |
| `features` | `object` | no | Structured feature set (items, blocks, entities, events, etc.). Required for create_mod_project on non-skinpack targets. |
| `minecraft_version` | `string` | no | Pinned Minecraft version. Omit to use the platform default. |
| `mod_id` | `string` | no | Required for spec-mode preview; optional for archive-mode (defaults to the archive's mod_id). |
| `mod_metadata` | `object` | no | Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape. |
| `mod_name` | `string` | no | Required for spec-mode preview. |
| `preview_background` | `string` | no | render_preview_image: background style for the preview canvas. |
| `preview_size` | `integer` | no | render_preview_image: square preview size in pixels (32-1024). Default 256. |
| `preview_source_file_id` | `string` | no | render_preview_image: File Manager file_id for a user-supplied image to preview directly. |
| `preview_target_id` | `string` | no | render_preview_image: feature id or namespaced id to preview. |
| `preview_target_kind` | `string` | no | render_preview_image: 'item', 'block', or 'entity'. Omit to auto-select. |
| `skin_pack` | `object` | no | Skin pack definition. Required for create_mod_project when target_platform='bedrock_skinpack'. |
| `source_archive_file_id` | `string` | no | File Manager file_id for a previously generated source zip. Use to preview an asset from a built mod without re-supplying the spec. |
| `target_platform` | `string` | no | Required for spec-mode preview. Optional when passing source_archive_file_id or preview_source_file_id. |

Sample parameters:

```json
{
  "advanced_resources": [
    {}
  ],
  "allow_experimental_bedrock_features": true,
  "assets": {},
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
  "minecraft_version": "example minecraft version",
  "mod_id": "example mod id"
}
```

Generated JSON parameter schema:

```json
{
  "advanced_resources": {
    "description": "Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64|content_text|source_file_id, content_type}.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock features that require experimental world toggles.",
    "required": false,
    "type": "boolean"
  },
  "assets": {
    "description": "Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape.",
    "required": false,
    "type": "object"
  },
  "compatibility_mode": {
    "default": "strict",
    "enum": [
      "strict",
      "allow_platform_passthrough"
    ],
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Short mod description shown in the pack metadata.",
    "required": false,
    "type": "string"
  },
  "features": {
    "description": "Structured feature set (items, blocks, entities, events, etc.). Required for create_mod_project on non-skinpack targets.",
    "properties": {
      "animation_controllers": {
        "items": {
          "description": "AnimationControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "animations": {
        "items": {
          "description": "AnimationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "biomes": {
        "items": {
          "description": "BiomeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "blocks": {
        "items": {
          "properties": {
            "block_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game block id.",
              "required": true,
              "type": "string"
            },
            "block_kind": {
              "default": "basic",
              "description": "Block class. 'basic' = stone-like solid block. 'ore' = drops items via the drops field when mined with the correct tool. 'light' = emits full light (use light_level to override). 'interactive' = supports right-click handlers via events. 'crop' / 'plant' = grows over time via the crop preset. 'redstone' = signal-aware (use redstone preset). 'machine' = container that runs a recipe (pair with the matching MachineSpec). 'container' = inventory storage (pair with the matching StorageSpec).",
              "enum": [
                "basic",
                "ore",
                "light",
                "interactive",
                "crop",
                "plant",
                "redstone",
                "machine",
                "container"
              ],
              "required": false,
              "type": "string"
            },
            "collision_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "crafting_table": {
              "default": false,
              "required": false,
              "type": "boolean"
            },
            "crop": {
              "description": "CropSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable block name shown to players.",
              "required": true,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "flammable": {
              "properties": {
                "catch_chance_modifier": {
                  "default": 5,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "destroy_chance_modifier": {
                  "default": 20,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "friction": {
              "maximum": 1,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "hardness": {
              "maximum": 100,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "light_level": {
              "maximum": 15,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "map_color": {
              "required": false,
              "type": "string"
            },
            "material_instances": {
              "additionalProperties": {
                "description": "MaterialInstanceSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "object"
            },
            "placement_filter": {
              "description": "PlacementFilterSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "redstone": {
              "description": "RedstoneSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "resistance": {
              "maximum": 10000,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "selection_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the block face. See BindingTextureSpec.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "tick": {
              "properties": {
                "interval_range": {
                  "items": {
                    "type": "integer"
                  },
                  "maxItems": 2,
                  "minItems": 2,
                  "required": false,
                  "type": "array"
                },
                "looping": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "commands": {
        "items": {
          "properties": {
            "actions": {
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "required": false,
              "type": "array"
            },
            "command_id": {
              "required": true,
              "type": "string"
            },
            "command_kind": {
              "enum": [
                "simple_command",
                "argument_command",
                "function_command",
                "admin_command"
              ],
              "required": true,
              "type": "string"
            },
            "description": {
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "parameters": {
              "items": {
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "permission_level": {
              "default": "any",
              "enum": [
                "any",
                "op",
                "admin"
              ],
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "damage_types": {
        "items": {
          "description": "DamageTypeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "dimensions": {
        "items": {
          "description": "DimensionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "effects": {
        "items": {
          "description": "EffectSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "enchantments": {
        "items": {
          "description": "EnchantmentSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "entities": {
        "items": {
          "properties": {
            "ai_goals": {
              "items": {
                "description": "EntityAIGoalSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "attack_damage": {
              "description": "Melee damage on attack. Default derived from entity_kind.",
              "maximum": 512,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "breedable": {
              "description": "EntityBreedableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable entity name shown in death messages and the spawn-egg tooltip.",
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "entity_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game entity id.",
              "required": true,
              "type": "string"
            },
            "entity_kind": {
              "description": "Mob class. Controls AI defaults, spawn category, and renderer registration. 'passive_mob' = cow/sheep-like, never attacks. 'hostile_mob' = zombie-like, attacks players on sight. 'neutral_mob' = wolf-like, attacks when hurt. 'tameable_pet' = wolf-like with taming behavior (requires tameable preset). 'rideable_mount' = horse-like (requires rideable preset). 'projectile' = arrow-like flying entity. 'npc_like' = villager-like with trades (use interactions preset). 'boss_like' = ender-dragon-like with boss bar.",
              "enum": [
                "passive_mob",
                "hostile_mob",
                "neutral_mob",
                "projectile",
                "npc_like",
                "tameable_pet",
                "rideable_mount",
                "boss_like"
              ],
              "required": true,
              "type": "string"
            },
            "equipment": {
              "description": "EntityEquipmentSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "families": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "health": {
              "default": 20,
              "description": "Maximum health points (each heart = 2 HP).",
              "maximum": 2048,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "interactions": {
              "items": {
                "description": "EntityInteractionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "loot_table": {
              "required": false,
              "type": "string"
            },
            "movement_speed": {
              "default": 0.25,
              "description": "Walking speed. Vanilla baseline is 0.25 for passive mobs.",
              "maximum": 5,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "render": {
              "description": "EntityRenderSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "rideable": {
              "description": "EntityRideableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "spawn_biomes": {
              "description": "Biome ids (minecraft:plains, etc.) where the mob can naturally spawn.",
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "spawn_weight": {
              "default": 10,
              "description": "Relative spawn weight in eligible biomes.",
              "maximum": 1000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "tameable": {
              "description": "EntityTameableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the entity model and its spawn-egg icon. Bedrock uses a 64x64 humanoid-style atlas by default; supply a 64x64 PNG via source_base64 or source_file_id to override.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "events": {
        "items": {
          "properties": {
            "actions": {
              "description": "Required non-empty list of actions to execute when the event fires.",
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "conditions": {
              "items": {
                "description": "ConditionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 20,
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "event_id": {
              "required": true,
              "type": "string"
            },
            "event_kind": {
              "description": "Event trigger. Filter to a specific item/block/entity with conditions; emit behavior with actions. Example: pair 'on_item_hit_entity' with a {condition_kind:'held_item', identifier:'modid:flame_sword'} condition and a {action_kind:'set_on_fire', duration_ticks:100} action to make a flame sword.",
              "enum": [
                "on_item_use",
                "on_item_hit_entity",
                "on_item_mine_block",
                "on_item_inventory_tick",
                "on_entity_spawn",
                "on_entity_death",
                "on_entity_hurt",
                "on_entity_tick",
                "on_player_tick",
                "on_player_join",
                "on_player_respawn",
                "on_block_break",
                "on_block_interact",
                "on_block_place",
                "on_block_tick",
                "on_projectile_hit",
                "on_enter_biome",
                "on_command",
                "on_inventory_change",
                "on_redstone_change",
                "on_machine_recipe_complete"
              ],
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "functions": {
        "items": {
          "description": "FunctionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "game_rules": {
        "items": {
          "description": "GameRuleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "items": {
        "items": {
          "properties": {
            "allow_off_hand": {
              "required": false,
              "type": "boolean"
            },
            "armor": {
              "description": "Armor preset (slot + protection). Required when item_kind='armor' unless wearable is set.",
              "properties": {
                "dyeable": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "knockback_resistance": {
                  "default": 0,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "protection": {
                  "default": 1,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "enum": [
                    "head",
                    "chest",
                    "legs",
                    "feet"
                  ],
                  "required": true,
                  "type": "string"
                },
                "toughness": {
                  "default": 0,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "trim_supported": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "block_placer": {
              "description": "Block id or preset; required when item_kind='block_placer'.",
              "required": false,
              "type": "string"
            },
            "bundle_interaction": {
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "compostable": {
              "properties": {
                "chance": {
                  "default": 0.3,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "cooldown": {
              "properties": {
                "category": {
                  "default": "generic",
                  "required": false,
                  "type": "string"
                },
                "cooldown_type": {
                  "default": "use",
                  "description": "Cooldown trigger. 'use' fires on right-click activation; 'attack' fires on swing. Accepts cooldown_type or type as input.",
                  "enum": [
                    "use",
                    "attack"
                  ],
                  "required": false,
                  "type": "string"
                },
                "duration_seconds": {
                  "default": 1,
                  "maximum": 3600,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "damage": {
              "description": "Attack damage when held. Used by item_kind in {'tool','weapon'}; default derives from tool_tier.",
              "maximum": 231,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "digger": {
              "properties": {
                "destroy_speeds": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "use_efficiency": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "display_name": {
              "description": "Human-readable item name shown to players in inventory tooltips.",
              "required": true,
              "type": "string"
            },
            "durability": {
              "description": "Use count before the item breaks. Used by tool/weapon/armor; default derives from tool_tier.",
              "maximum": 100000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "dyeable": {
              "description": "DyeableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enchantable": {
              "properties": {
                "slot": {
                  "default": "pickaxe",
                  "required": false,
                  "type": "string"
                },
                "value": {
                  "default": 10,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "entity_placer": {
              "description": "Entity id or preset (spawn-egg-like); required when item_kind='entity_placer'.",
              "required": false,
              "type": "string"
            },
            "fire_resistant": {
              "required": false,
              "type": "boolean"
            },
            "foil": {
              "required": false,
              "type": "boolean"
            },
            "food": {
              "description": "Food preset (nutrition, saturation, effects). Required when item_kind='food' unless nutrition is set.",
              "properties": {
                "can_always_eat": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "effects": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "nutrition": {
                  "default": 4,
                  "maximum": 20,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "remove_effects": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "saturation_modifier": {
                  "default": 0.6,
                  "required": false,
                  "type": "number"
                },
                "use_modifiers": {
                  "description": "UseModifierSpec object. See get_instructions for the full shape.",
                  "required": false,
                  "type": "object"
                },
                "using_converts_to": {
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "fuel": {
              "properties": {
                "duration_seconds": {
                  "default": 5,
                  "exclusiveMinimum": 0,
                  "maximum": 3600,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "glint": {
              "required": false,
              "type": "boolean"
            },
            "hover_text_color": {
              "required": false,
              "type": "string"
            },
            "interact_button": {
              "required": false,
              "type": "string"
            },
            "item_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game item id.",
              "required": true,
              "type": "string"
            },
            "item_kind": {
              "default": "generic",
              "description": "Behavior class. Drives icon sprite, creative-tab placement, stack size, and which preset fields are required. 'weapon' = sword-like, lands in Equipment tab, requires tool_type in {'sword','custom'}. 'tool' = pickaxe/axe/shovel/hoe, lands in Equipment tab, requires tool_type. 'armor' = head/chest/legs/feet, lands in Equipment tab, requires armor preset. 'food' = eatable, requires food preset or nutrition. 'projectile' = arrow-like, requires projectile/shooter/throwable. 'block_placer' / 'entity_placer' = spawn-egg-like, requires matching preset. 'fuel' = furnace fuel. 'generic' = raw material only (sticks, ingots, dust); rejects any combat/tool/armor/food preset.",
              "enum": [
                "generic",
                "tool",
                "weapon",
                "armor",
                "food",
                "fuel",
                "projectile",
                "block_placer",
                "entity_placer"
              ],
              "required": false,
              "type": "string"
            },
            "kinetic_weapon": {
              "required": false,
              "type": "object"
            },
            "liquid_clipped": {
              "required": false,
              "type": "boolean"
            },
            "max_stack_size": {
              "description": "Inventory stack size. Defaults to 1 for tool/weapon/armor/projectile and 64 for generic/food.",
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "nutrition": {
              "description": "Food hunger points restored on consumption. Required (with food preset) when item_kind='food'.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "piercing_weapon": {
              "required": false,
              "type": "object"
            },
            "projectile": {
              "description": "Projectile preset. One of projectile/shooter/throwable required when item_kind='projectile'.",
              "properties": {
                "minimum_critical_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "projectile_entity": {
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "rarity": {
              "description": "RaritySpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "record": {
              "required": false,
              "type": "object"
            },
            "repairable": {
              "properties": {
                "repair_items": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                }
              },
              "required": false,
              "type": "object"
            },
            "saturation": {
              "description": "Food saturation modifier paired with nutrition.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "shooter": {
              "description": "Bow-like shooter preset that consumes ammunition items.",
              "properties": {
                "ammunition": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "charge_on_draw": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "scale_power_by_draw_duration": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "search_inventory": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "use_in_creative": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "should_despawn": {
              "required": false,
              "type": "boolean"
            },
            "stacked_by_data": {
              "required": false,
              "type": "boolean"
            },
            "swing_sounds": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "texture": {
              "description": "Required visible-asset texture. Supply one of source_base64, source_file_id, or color_hex. color_hex paired with item_kind+tool_type renders a kind-shaped procedural sprite (sword, pickaxe, axe, shovel, or hoe).",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "throwable": {
              "description": "Throwable preset (snowball-like behavior).",
              "properties": {
                "do_swing_animation": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "launch_power_scale": {
                  "default": 1,
                  "exclusiveMinimum": 0,
                  "maximum": 10,
                  "required": false,
                  "type": "number"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "max_launch_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool": {
              "description": "Explicit tool preset overriding tool_type/tool_tier defaults.",
              "properties": {
                "attack_damage": {
                  "default": 4,
                  "maximum": 231,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "attack_speed": {
                  "default": 1.6,
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "break_all_blocks": {
                  "default": false,
                  "description": "When true, the tool can mine every block at full speed regardless of the vanilla pickaxe/axe/shovel/hoe destructible tag. Bedrock emits a Molang-true tag predicate on minecraft:digger; Java emits a tier that ignores TagBlockEntries restrictions. Combine with instabreak for a creative-mode super-tool.",
                  "required": false,
                  "type": "boolean"
                },
                "digger": {
                  "properties": {
                    "destroy_speeds": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "use_efficiency": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "enchantable": {
                  "properties": {
                    "slot": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "value": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "instabreak": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "mining_speed": {
                  "default": 4,
                  "exclusiveMinimum": 0,
                  "maximum": 2048,
                  "required": false,
                  "type": "number"
                },
                "repairable": {
                  "properties": {
                    "repair_items": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "tier": {
                  "default": "iron",
                  "enum": [
                    "wood",
                    "stone",
                    "iron",
                    "gold",
                    "diamond",
                    "netherite",
                    "custom"
                  ],
                  "required": false,
                  "type": "string"
                },
                "tool_type": {
                  "enum": [
                    "pickaxe",
                    "axe",
                    "shovel",
                    "hoe",
                    "sword",
                    "custom"
                  ],
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool_tier": {
              "description": "Tier preset. Determines default durability, attack damage, mining speed, enchantability, and repair material. Defaults to 'iron' when omitted on a tool/weapon. 'custom' opts out of all tier defaults.",
              "enum": [
                "wood",
                "stone",
                "iron",
                "gold",
                "diamond",
                "netherite",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "tool_type": {
              "description": "Tool kind. Controls the rendered icon sprite when color_hex is the texture source, the destructible-block tag, and the Equipment-tab sub-group. Required when item_kind='tool'. Use 'sword' for item_kind='weapon'. 'custom' opts out of the kind-specific defaults so the spec must declare its own damage/durability/digger.",
              "enum": [
                "pickaxe",
                "axe",
                "shovel",
                "hoe",
                "sword",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "use_modifiers": {
              "description": "UseModifierSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "wearable": {
              "properties": {
                "protection": {
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "default": "slot.armor.head",
                  "enum": [
                    "slot.armor.head",
                    "slot.armor.chest",
                    "slot.armor.legs",
                    "slot.armor.feet",
                    "slot.weapon.offhand"
                  ],
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "localizations": {
        "items": {
          "description": "LocalizationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "loot_tables": {
        "items": {
          "properties": {
            "conditions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "maxItems": 64,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "functions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "loot_id": {
              "required": true,
              "type": "string"
            },
            "target": {
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "machines": {
        "items": {
          "description": "MachineSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "particles": {
        "items": {
          "description": "ParticleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "recipes": {
        "items": {
          "properties": {
            "addition_item": {
              "required": false,
              "type": "string"
            },
            "base_item": {
              "required": false,
              "type": "string"
            },
            "cooking_time_seconds": {
              "maximum": 3600,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "count": {
              "default": 1,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "ingredients": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "input_item": {
              "required": false,
              "type": "string"
            },
            "key": {
              "additionalProperties": {
                "type": "string"
              },
              "required": false,
              "type": "object"
            },
            "pattern": {
              "items": {
                "type": "string"
              },
              "maxItems": 3,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "recipe_id": {
              "required": true,
              "type": "string"
            },
            "recipe_kind": {
              "default": "shapeless",
              "description": "Recipe class. 'shaped' requires pattern+key. 'shapeless' requires ingredients. 'furnace' requires input_item+cooking_time_seconds. 'smithing_transform' / 'smithing_trim' require template_item+base_item+addition_item. 'brewing_mix' / 'brewing_container' are Bedrock-only.",
              "enum": [
                "shaped",
                "shapeless",
                "furnace",
                "brewing_mix",
                "brewing_container",
                "smithing_transform",
                "smithing_trim"
              ],
              "required": false,
              "type": "string"
            },
            "result_item": {
              "required": true,
              "type": "string"
            },
            "template_item": {
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "render_controllers": {
        "items": {
          "description": "RenderControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "scoreboards": {
        "items": {
          "description": "ScoreboardSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "sounds": {
        "items": {
          "description": "SoundSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "storage": {
        "items": {
          "description": "StorageSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "structures": {
        "items": {
          "description": "StructureSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "trades": {
        "items": {
          "description": "TradeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "transportation": {
        "items": {
          "description": "TransportationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "ui": {
        "items": {
          "description": "UISpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "worldgen": {
        "items": {
          "properties": {
            "biomes": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "block_id": {
              "description": "Block id to place. Required for ore/single_block/vegetation features.",
              "required": false,
              "type": "string"
            },
            "count_per_chunk": {
              "default": 8,
              "maximum": 128,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "feature_id": {
              "required": true,
              "type": "string"
            },
            "feature_kind": {
              "description": "Worldgen feature class. 'ore_feature' places veins of block_id inside target_block. 'single_block_feature' places a single block. 'vegetation_patch' places a plant patch. 'structure_placement' places a stored structure. 'custom_biome' / 'custom_dimension' register a referenced biome/dimension.",
              "enum": [
                "ore_feature",
                "single_block_feature",
                "vegetation_patch",
                "structure_placement",
                "custom_biome",
                "custom_dimension"
              ],
              "required": true,
              "type": "string"
            },
            "max_y": {
              "default": 64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "min_y": {
              "default": -64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "radius": {
              "default": 4,
              "maximum": 32,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "source_file_id": {
              "required": false,
              "type": "string"
            },
            "target_block": {
              "default": "minecraft:stone",
              "required": false,
              "type": "string"
            },
            "vein_size": {
              "default": 6,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "vertical_range": {
              "default": 5,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "minecraft_version": {
    "description": "Pinned Minecraft version. Omit to use the platform default.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Required for spec-mode preview; optional for archive-mode (defaults to the archive's mod_id).",
    "required": false,
    "type": "string"
  },
  "mod_metadata": {
    "description": "Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape.",
    "required": false,
    "type": "object"
  },
  "mod_name": {
    "description": "Required for spec-mode preview.",
    "required": false,
    "type": "string"
  },
  "preview_background": {
    "default": "checkerboard",
    "description": "render_preview_image: background style for the preview canvas.",
    "enum": [
      "checkerboard",
      "transparent",
      "white",
      "black"
    ],
    "required": false,
    "type": "string"
  },
  "preview_size": {
    "default": 256,
    "description": "render_preview_image: square preview size in pixels (32-1024). Default 256.",
    "maximum": 1024,
    "minimum": 32,
    "required": false,
    "type": "integer"
  },
  "preview_source_file_id": {
    "description": "render_preview_image: File Manager file_id for a user-supplied image to preview directly.",
    "required": false,
    "type": "string"
  },
  "preview_target_id": {
    "description": "render_preview_image: feature id or namespaced id to preview.",
    "required": false,
    "type": "string"
  },
  "preview_target_kind": {
    "description": "render_preview_image: 'item', 'block', or 'entity'. Omit to auto-select.",
    "enum": [
      "item",
      "block",
      "entity"
    ],
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition. Required for create_mod_project when target_platform='bedrock_skinpack'.",
    "properties": {
      "display_name": {
        "required": false,
        "type": "string"
      },
      "pack_id": {
        "required": false,
        "type": "string"
      },
      "skins": {
        "items": {
          "properties": {
            "display_name": {
              "required": true,
              "type": "string"
            },
            "geometry": {
              "default": "geometry.humanoid.custom",
              "enum": [
                "geometry.humanoid.custom",
                "geometry.humanoid.customSlim"
              ],
              "required": false,
              "type": "string"
            },
            "localization_name": {
              "required": false,
              "type": "string"
            },
            "skin_id": {
              "required": true,
              "type": "string"
            },
            "skin_type": {
              "default": "free",
              "description": "Skin type. Accepts skin_type or type as input.",
              "enum": [
                "free",
                "paid"
              ],
              "required": false,
              "type": "string"
            },
            "texture": {
              "description": "Required 64x64 PNG skin texture. Supply source_base64 or source_file_id for a user-drawn skin; color_hex renders a flat humanoid silhouette.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "maxItems": 64,
        "minItems": 1,
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "source_archive_file_id": {
    "description": "File Manager file_id for a previously generated source zip. Use to preview an asset from a built mod without re-supplying the spec.",
    "required": false,
    "type": "string"
  },
  "target_platform": {
    "description": "Required for spec-mode preview. Optional when passing source_archive_file_id or preview_source_file_id.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `validate_mod_project`

Action slug: `validate-mod-project`

Price: `25` credits

Validate either a structured mod specification (spec mode) or a previously generated source archive (archive mode). Spec mode: provide target_platform, mod_id, mod_name, features (or skin_pack for skinpacks). Archive mode: provide source_archive_file_id. Returns a validation report with error codes and warnings; does NOT write artifacts.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advanced_resources` | `array` | no | Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64\|content_text\|source_file_id, content_type}. |
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock features that require experimental world toggles. |
| `assets` | `object` | no | Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape. |
| `compatibility_mode` | `string` | no | {"default": "strict", "enum": ["strict", "allow_platform_passthrough"]} |
| `description` | `string` | no | Short mod description shown in the pack metadata. |
| `features` | `object` | no | Structured feature set (items, blocks, entities, events, etc.). Required for spec-mode validation on non-skinpack targets. |
| `minecraft_version` | `string` | no | Pinned Minecraft version. Omit to use the platform default. |
| `mod_id` | `string` | no | Required for spec-mode validation (lowercase ^[a-z][a-z0-9_]{1,63}$). Optional in archive-mode. |
| `mod_metadata` | `object` | no | Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape. |
| `mod_name` | `string` | no | Required for spec-mode validation. Optional in archive-mode. |
| `skin_pack` | `object` | no | Skin pack definition. Required for spec-mode validation when target_platform='bedrock_skinpack'. |
| `source_archive_file_id` | `string` | no | File Manager file_id for a previously generated source zip. Supply this for archive-mode validation (skips spec validation; replays the zip's contents). |
| `target_platform` | `string` | no | Required for spec-mode validation. Optional in archive-mode (omit when passing source_archive_file_id). One of bedrock, bedrock_skinpack, fabric, neoforge. |

Sample parameters:

```json
{
  "advanced_resources": [
    {}
  ],
  "allow_experimental_bedrock_features": true,
  "assets": {},
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
  "minecraft_version": "example minecraft version",
  "mod_id": "example mod id"
}
```

Generated JSON parameter schema:

```json
{
  "advanced_resources": {
    "description": "Escape-hatch list of AdvancedResourceSpec entries for files the structured surface does not model (raw JSON blobs, custom sound definitions, etc.). Each entry has {path, content_base64|content_text|source_file_id, content_type}.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock features that require experimental world toggles.",
    "required": false,
    "type": "boolean"
  },
  "assets": {
    "description": "Optional AssetSetSpec containing pre-bound textures/sounds/particles/models/language entries: {textures: NamedAssetSpec[], sounds: NamedAssetSpec[], particles: NamedAssetSpec[], models: NamedAssetSpec[], language: {locale: {key: value}}}. See get_instructions for shape.",
    "required": false,
    "type": "object"
  },
  "compatibility_mode": {
    "default": "strict",
    "enum": [
      "strict",
      "allow_platform_passthrough"
    ],
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Short mod description shown in the pack metadata.",
    "required": false,
    "type": "string"
  },
  "features": {
    "description": "Structured feature set (items, blocks, entities, events, etc.). Required for spec-mode validation on non-skinpack targets.",
    "properties": {
      "animation_controllers": {
        "items": {
          "description": "AnimationControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "animations": {
        "items": {
          "description": "AnimationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "biomes": {
        "items": {
          "description": "BiomeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "blocks": {
        "items": {
          "properties": {
            "block_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game block id.",
              "required": true,
              "type": "string"
            },
            "block_kind": {
              "default": "basic",
              "description": "Block class. 'basic' = stone-like solid block. 'ore' = drops items via the drops field when mined with the correct tool. 'light' = emits full light (use light_level to override). 'interactive' = supports right-click handlers via events. 'crop' / 'plant' = grows over time via the crop preset. 'redstone' = signal-aware (use redstone preset). 'machine' = container that runs a recipe (pair with the matching MachineSpec). 'container' = inventory storage (pair with the matching StorageSpec).",
              "enum": [
                "basic",
                "ore",
                "light",
                "interactive",
                "crop",
                "plant",
                "redstone",
                "machine",
                "container"
              ],
              "required": false,
              "type": "string"
            },
            "collision_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "crafting_table": {
              "default": false,
              "required": false,
              "type": "boolean"
            },
            "crop": {
              "description": "CropSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable block name shown to players.",
              "required": true,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "flammable": {
              "properties": {
                "catch_chance_modifier": {
                  "default": 5,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "destroy_chance_modifier": {
                  "default": 20,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "friction": {
              "maximum": 1,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "hardness": {
              "maximum": 100,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "light_level": {
              "maximum": 15,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "map_color": {
              "required": false,
              "type": "string"
            },
            "material_instances": {
              "additionalProperties": {
                "description": "MaterialInstanceSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "object"
            },
            "placement_filter": {
              "description": "PlacementFilterSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "redstone": {
              "description": "RedstoneSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "resistance": {
              "maximum": 10000,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "selection_box": {
              "description": "BoxSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the block face. See BindingTextureSpec.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "tick": {
              "properties": {
                "interval_range": {
                  "items": {
                    "type": "integer"
                  },
                  "maxItems": 2,
                  "minItems": 2,
                  "required": false,
                  "type": "array"
                },
                "looping": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "commands": {
        "items": {
          "properties": {
            "actions": {
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "required": false,
              "type": "array"
            },
            "command_id": {
              "required": true,
              "type": "string"
            },
            "command_kind": {
              "enum": [
                "simple_command",
                "argument_command",
                "function_command",
                "admin_command"
              ],
              "required": true,
              "type": "string"
            },
            "description": {
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "parameters": {
              "items": {
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "permission_level": {
              "default": "any",
              "enum": [
                "any",
                "op",
                "admin"
              ],
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "damage_types": {
        "items": {
          "description": "DamageTypeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "dimensions": {
        "items": {
          "description": "DimensionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "effects": {
        "items": {
          "description": "EffectSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "enchantments": {
        "items": {
          "description": "EnchantmentSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "entities": {
        "items": {
          "properties": {
            "ai_goals": {
              "items": {
                "description": "EntityAIGoalSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "attack_damage": {
              "description": "Melee damage on attack. Default derived from entity_kind.",
              "maximum": 512,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "breedable": {
              "description": "EntityBreedableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "description": "Human-readable entity name shown in death messages and the spawn-egg tooltip.",
              "required": true,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "entity_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game entity id.",
              "required": true,
              "type": "string"
            },
            "entity_kind": {
              "description": "Mob class. Controls AI defaults, spawn category, and renderer registration. 'passive_mob' = cow/sheep-like, never attacks. 'hostile_mob' = zombie-like, attacks players on sight. 'neutral_mob' = wolf-like, attacks when hurt. 'tameable_pet' = wolf-like with taming behavior (requires tameable preset). 'rideable_mount' = horse-like (requires rideable preset). 'projectile' = arrow-like flying entity. 'npc_like' = villager-like with trades (use interactions preset). 'boss_like' = ender-dragon-like with boss bar.",
              "enum": [
                "passive_mob",
                "hostile_mob",
                "neutral_mob",
                "projectile",
                "npc_like",
                "tameable_pet",
                "rideable_mount",
                "boss_like"
              ],
              "required": true,
              "type": "string"
            },
            "equipment": {
              "description": "EntityEquipmentSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "families": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "health": {
              "default": 20,
              "description": "Maximum health points (each heart = 2 HP).",
              "maximum": 2048,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "interactions": {
              "items": {
                "description": "EntityInteractionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "loot_table": {
              "required": false,
              "type": "string"
            },
            "movement_speed": {
              "default": 0.25,
              "description": "Walking speed. Vanilla baseline is 0.25 for passive mobs.",
              "maximum": 5,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "render": {
              "description": "EntityRenderSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "rideable": {
              "description": "EntityRideableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "spawn_biomes": {
              "description": "Biome ids (minecraft:plains, etc.) where the mob can naturally spawn.",
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "spawn_weight": {
              "default": 10,
              "description": "Relative spawn weight in eligible biomes.",
              "maximum": 1000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "tameable": {
              "description": "EntityTameableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "texture": {
              "description": "Required visible-asset texture for the entity model and its spawn-egg icon. Bedrock uses a 64x64 humanoid-style atlas by default; supply a 64x64 PNG via source_base64 or source_file_id to override.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "events": {
        "items": {
          "properties": {
            "actions": {
              "description": "Required non-empty list of actions to execute when the event fires.",
              "items": {
                "description": "ActionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 50,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "conditions": {
              "items": {
                "description": "ConditionSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "maxItems": 20,
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "event_id": {
              "required": true,
              "type": "string"
            },
            "event_kind": {
              "description": "Event trigger. Filter to a specific item/block/entity with conditions; emit behavior with actions. Example: pair 'on_item_hit_entity' with a {condition_kind:'held_item', identifier:'modid:flame_sword'} condition and a {action_kind:'set_on_fire', duration_ticks:100} action to make a flame sword.",
              "enum": [
                "on_item_use",
                "on_item_hit_entity",
                "on_item_mine_block",
                "on_item_inventory_tick",
                "on_entity_spawn",
                "on_entity_death",
                "on_entity_hurt",
                "on_entity_tick",
                "on_player_tick",
                "on_player_join",
                "on_player_respawn",
                "on_block_break",
                "on_block_interact",
                "on_block_place",
                "on_block_tick",
                "on_projectile_hit",
                "on_enter_biome",
                "on_command",
                "on_inventory_change",
                "on_redstone_change",
                "on_machine_recipe_complete"
              ],
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "functions": {
        "items": {
          "description": "FunctionSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "game_rules": {
        "items": {
          "description": "GameRuleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "items": {
        "items": {
          "properties": {
            "allow_off_hand": {
              "required": false,
              "type": "boolean"
            },
            "armor": {
              "description": "Armor preset (slot + protection). Required when item_kind='armor' unless wearable is set.",
              "properties": {
                "dyeable": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "knockback_resistance": {
                  "default": 0,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "protection": {
                  "default": 1,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "enum": [
                    "head",
                    "chest",
                    "legs",
                    "feet"
                  ],
                  "required": true,
                  "type": "string"
                },
                "toughness": {
                  "default": 0,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "trim_supported": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "block_placer": {
              "description": "Block id or preset; required when item_kind='block_placer'.",
              "required": false,
              "type": "string"
            },
            "bundle_interaction": {
              "required": false,
              "type": "object"
            },
            "component_overrides": {
              "items": {
                "description": "ComponentOverrideSpec object. See get_instructions for the full shape.",
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "compostable": {
              "properties": {
                "chance": {
                  "default": 0.3,
                  "maximum": 1,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "cooldown": {
              "properties": {
                "category": {
                  "default": "generic",
                  "required": false,
                  "type": "string"
                },
                "cooldown_type": {
                  "default": "use",
                  "description": "Cooldown trigger. 'use' fires on right-click activation; 'attack' fires on swing. Accepts cooldown_type or type as input.",
                  "enum": [
                    "use",
                    "attack"
                  ],
                  "required": false,
                  "type": "string"
                },
                "duration_seconds": {
                  "default": 1,
                  "maximum": 3600,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "custom_components": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "damage": {
              "description": "Attack damage when held. Used by item_kind in {'tool','weapon'}; default derives from tool_tier.",
              "maximum": 231,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "digger": {
              "properties": {
                "destroy_speeds": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "use_efficiency": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "display_name": {
              "description": "Human-readable item name shown to players in inventory tooltips.",
              "required": true,
              "type": "string"
            },
            "durability": {
              "description": "Use count before the item breaks. Used by tool/weapon/armor; default derives from tool_tier.",
              "maximum": 100000,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "dyeable": {
              "description": "DyeableSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "enchantable": {
              "properties": {
                "slot": {
                  "default": "pickaxe",
                  "required": false,
                  "type": "string"
                },
                "value": {
                  "default": 10,
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                }
              },
              "required": false,
              "type": "object"
            },
            "entity_placer": {
              "description": "Entity id or preset (spawn-egg-like); required when item_kind='entity_placer'.",
              "required": false,
              "type": "string"
            },
            "fire_resistant": {
              "required": false,
              "type": "boolean"
            },
            "foil": {
              "required": false,
              "type": "boolean"
            },
            "food": {
              "description": "Food preset (nutrition, saturation, effects). Required when item_kind='food' unless nutrition is set.",
              "properties": {
                "can_always_eat": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "effects": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                },
                "nutrition": {
                  "default": 4,
                  "maximum": 20,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "remove_effects": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "saturation_modifier": {
                  "default": 0.6,
                  "required": false,
                  "type": "number"
                },
                "use_modifiers": {
                  "description": "UseModifierSpec object. See get_instructions for the full shape.",
                  "required": false,
                  "type": "object"
                },
                "using_converts_to": {
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "fuel": {
              "properties": {
                "duration_seconds": {
                  "default": 5,
                  "exclusiveMinimum": 0,
                  "maximum": 3600,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "glint": {
              "required": false,
              "type": "boolean"
            },
            "hover_text_color": {
              "required": false,
              "type": "string"
            },
            "interact_button": {
              "required": false,
              "type": "string"
            },
            "item_id": {
              "description": "Lowercase identifier (^[a-z][a-z0-9_]{1,63}$); becomes the in-game item id.",
              "required": true,
              "type": "string"
            },
            "item_kind": {
              "default": "generic",
              "description": "Behavior class. Drives icon sprite, creative-tab placement, stack size, and which preset fields are required. 'weapon' = sword-like, lands in Equipment tab, requires tool_type in {'sword','custom'}. 'tool' = pickaxe/axe/shovel/hoe, lands in Equipment tab, requires tool_type. 'armor' = head/chest/legs/feet, lands in Equipment tab, requires armor preset. 'food' = eatable, requires food preset or nutrition. 'projectile' = arrow-like, requires projectile/shooter/throwable. 'block_placer' / 'entity_placer' = spawn-egg-like, requires matching preset. 'fuel' = furnace fuel. 'generic' = raw material only (sticks, ingots, dust); rejects any combat/tool/armor/food preset.",
              "enum": [
                "generic",
                "tool",
                "weapon",
                "armor",
                "food",
                "fuel",
                "projectile",
                "block_placer",
                "entity_placer"
              ],
              "required": false,
              "type": "string"
            },
            "kinetic_weapon": {
              "required": false,
              "type": "object"
            },
            "liquid_clipped": {
              "required": false,
              "type": "boolean"
            },
            "max_stack_size": {
              "description": "Inventory stack size. Defaults to 1 for tool/weapon/armor/projectile and 64 for generic/food.",
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "nutrition": {
              "description": "Food hunger points restored on consumption. Required (with food preset) when item_kind='food'.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "integer"
            },
            "piercing_weapon": {
              "required": false,
              "type": "object"
            },
            "projectile": {
              "description": "Projectile preset. One of projectile/shooter/throwable required when item_kind='projectile'.",
              "properties": {
                "minimum_critical_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                },
                "projectile_entity": {
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "rarity": {
              "description": "RaritySpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "record": {
              "required": false,
              "type": "object"
            },
            "repairable": {
              "properties": {
                "repair_items": {
                  "items": {
                    "description": "Nested object; see get_instructions for full shape.",
                    "type": "object"
                  },
                  "required": false,
                  "type": "array"
                }
              },
              "required": false,
              "type": "object"
            },
            "saturation": {
              "description": "Food saturation modifier paired with nutrition.",
              "maximum": 20,
              "minimum": 0,
              "required": false,
              "type": "number"
            },
            "shooter": {
              "description": "Bow-like shooter preset that consumes ammunition items.",
              "properties": {
                "ammunition": {
                  "items": {
                    "type": "string"
                  },
                  "required": false,
                  "type": "array"
                },
                "charge_on_draw": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "scale_power_by_draw_duration": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "search_inventory": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "use_in_creative": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                }
              },
              "required": false,
              "type": "object"
            },
            "should_despawn": {
              "required": false,
              "type": "boolean"
            },
            "stacked_by_data": {
              "required": false,
              "type": "boolean"
            },
            "swing_sounds": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "texture": {
              "description": "Required visible-asset texture. Supply one of source_base64, source_file_id, or color_hex. color_hex paired with item_kind+tool_type renders a kind-shaped procedural sprite (sword, pickaxe, axe, shovel, or hoe).",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            },
            "throwable": {
              "description": "Throwable preset (snowball-like behavior).",
              "properties": {
                "do_swing_animation": {
                  "default": true,
                  "required": false,
                  "type": "boolean"
                },
                "launch_power_scale": {
                  "default": 1,
                  "exclusiveMinimum": 0,
                  "maximum": 10,
                  "required": false,
                  "type": "number"
                },
                "max_draw_duration": {
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "max_launch_power": {
                  "maximum": 10,
                  "minimum": 0,
                  "required": false,
                  "type": "number"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool": {
              "description": "Explicit tool preset overriding tool_type/tool_tier defaults.",
              "properties": {
                "attack_damage": {
                  "default": 4,
                  "maximum": 231,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "attack_speed": {
                  "default": 1.6,
                  "exclusiveMinimum": 0,
                  "maximum": 20,
                  "required": false,
                  "type": "number"
                },
                "break_all_blocks": {
                  "default": false,
                  "description": "When true, the tool can mine every block at full speed regardless of the vanilla pickaxe/axe/shovel/hoe destructible tag. Bedrock emits a Molang-true tag predicate on minecraft:digger; Java emits a tier that ignores TagBlockEntries restrictions. Combine with instabreak for a creative-mode super-tool.",
                  "required": false,
                  "type": "boolean"
                },
                "digger": {
                  "properties": {
                    "destroy_speeds": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "use_efficiency": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "enchantable": {
                  "properties": {
                    "slot": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    },
                    "value": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "instabreak": {
                  "default": false,
                  "required": false,
                  "type": "boolean"
                },
                "mining_speed": {
                  "default": 4,
                  "exclusiveMinimum": 0,
                  "maximum": 2048,
                  "required": false,
                  "type": "number"
                },
                "repairable": {
                  "properties": {
                    "repair_items": {
                      "description": "Nested object; see get_instructions for full shape.",
                      "required": false,
                      "type": "object"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "tier": {
                  "default": "iron",
                  "enum": [
                    "wood",
                    "stone",
                    "iron",
                    "gold",
                    "diamond",
                    "netherite",
                    "custom"
                  ],
                  "required": false,
                  "type": "string"
                },
                "tool_type": {
                  "enum": [
                    "pickaxe",
                    "axe",
                    "shovel",
                    "hoe",
                    "sword",
                    "custom"
                  ],
                  "required": true,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            },
            "tool_tier": {
              "description": "Tier preset. Determines default durability, attack damage, mining speed, enchantability, and repair material. Defaults to 'iron' when omitted on a tool/weapon. 'custom' opts out of all tier defaults.",
              "enum": [
                "wood",
                "stone",
                "iron",
                "gold",
                "diamond",
                "netherite",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "tool_type": {
              "description": "Tool kind. Controls the rendered icon sprite when color_hex is the texture source, the destructible-block tag, and the Equipment-tab sub-group. Required when item_kind='tool'. Use 'sword' for item_kind='weapon'. 'custom' opts out of the kind-specific defaults so the spec must declare its own damage/durability/digger.",
              "enum": [
                "pickaxe",
                "axe",
                "shovel",
                "hoe",
                "sword",
                "custom"
              ],
              "required": false,
              "type": "string"
            },
            "use_modifiers": {
              "description": "UseModifierSpec object. See get_instructions for the full shape.",
              "required": false,
              "type": "object"
            },
            "wearable": {
              "properties": {
                "protection": {
                  "maximum": 100,
                  "minimum": 0,
                  "required": false,
                  "type": "integer"
                },
                "slot": {
                  "default": "slot.armor.head",
                  "enum": [
                    "slot.armor.head",
                    "slot.armor.chest",
                    "slot.armor.legs",
                    "slot.armor.feet",
                    "slot.weapon.offhand"
                  ],
                  "required": false,
                  "type": "string"
                }
              },
              "required": false,
              "type": "object"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "localizations": {
        "items": {
          "description": "LocalizationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "loot_tables": {
        "items": {
          "properties": {
            "conditions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "drops": {
              "items": {
                "type": "string"
              },
              "maxItems": 64,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "functions": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "loot_id": {
              "required": true,
              "type": "string"
            },
            "target": {
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "machines": {
        "items": {
          "description": "MachineSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "particles": {
        "items": {
          "description": "ParticleSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "recipes": {
        "items": {
          "properties": {
            "addition_item": {
              "required": false,
              "type": "string"
            },
            "base_item": {
              "required": false,
              "type": "string"
            },
            "cooking_time_seconds": {
              "maximum": 3600,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "count": {
              "default": 1,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "ingredients": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "input_item": {
              "required": false,
              "type": "string"
            },
            "key": {
              "additionalProperties": {
                "type": "string"
              },
              "required": false,
              "type": "object"
            },
            "pattern": {
              "items": {
                "type": "string"
              },
              "maxItems": 3,
              "minItems": 1,
              "required": false,
              "type": "array"
            },
            "recipe_id": {
              "required": true,
              "type": "string"
            },
            "recipe_kind": {
              "default": "shapeless",
              "description": "Recipe class. 'shaped' requires pattern+key. 'shapeless' requires ingredients. 'furnace' requires input_item+cooking_time_seconds. 'smithing_transform' / 'smithing_trim' require template_item+base_item+addition_item. 'brewing_mix' / 'brewing_container' are Bedrock-only.",
              "enum": [
                "shaped",
                "shapeless",
                "furnace",
                "brewing_mix",
                "brewing_container",
                "smithing_transform",
                "smithing_trim"
              ],
              "required": false,
              "type": "string"
            },
            "result_item": {
              "required": true,
              "type": "string"
            },
            "template_item": {
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "render_controllers": {
        "items": {
          "description": "RenderControllerSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "scoreboards": {
        "items": {
          "description": "ScoreboardSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "sounds": {
        "items": {
          "description": "SoundSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "storage": {
        "items": {
          "description": "StorageSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "structures": {
        "items": {
          "description": "StructureSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "trades": {
        "items": {
          "description": "TradeSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "transportation": {
        "items": {
          "description": "TransportationSpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "ui": {
        "items": {
          "description": "UISpec object. See get_instructions for the full shape.",
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "worldgen": {
        "items": {
          "properties": {
            "biomes": {
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "block_id": {
              "description": "Block id to place. Required for ore/single_block/vegetation features.",
              "required": false,
              "type": "string"
            },
            "count_per_chunk": {
              "default": 8,
              "maximum": 128,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "description": {
              "required": false,
              "type": "string"
            },
            "display_name": {
              "required": false,
              "type": "string"
            },
            "enabled_platforms": {
              "items": {
                "enum": [
                  "bedrock",
                  "fabric",
                  "neoforge"
                ],
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "feature_id": {
              "required": true,
              "type": "string"
            },
            "feature_kind": {
              "description": "Worldgen feature class. 'ore_feature' places veins of block_id inside target_block. 'single_block_feature' places a single block. 'vegetation_patch' places a plant patch. 'structure_placement' places a stored structure. 'custom_biome' / 'custom_dimension' register a referenced biome/dimension.",
              "enum": [
                "ore_feature",
                "single_block_feature",
                "vegetation_patch",
                "structure_placement",
                "custom_biome",
                "custom_dimension"
              ],
              "required": true,
              "type": "string"
            },
            "max_y": {
              "default": 64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "min_y": {
              "default": -64,
              "maximum": 320,
              "minimum": -64,
              "required": false,
              "type": "integer"
            },
            "radius": {
              "default": 4,
              "maximum": 32,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "source_file_id": {
              "required": false,
              "type": "string"
            },
            "target_block": {
              "default": "minecraft:stone",
              "required": false,
              "type": "string"
            },
            "vein_size": {
              "default": 6,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            },
            "vertical_range": {
              "default": 5,
              "maximum": 64,
              "minimum": 1,
              "required": false,
              "type": "integer"
            }
          },
          "type": "object"
        },
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "minecraft_version": {
    "description": "Pinned Minecraft version. Omit to use the platform default.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Required for spec-mode validation (lowercase ^[a-z][a-z0-9_]{1,63}$). Optional in archive-mode.",
    "required": false,
    "type": "string"
  },
  "mod_metadata": {
    "description": "Optional ModMetadataSpec: version, license, authors, homepage_url, issue_tracker_url, credits, logo_texture, brand_color_hex (#RRGGBB), java_side, bedrock_experiments. See get_instructions for the full shape.",
    "required": false,
    "type": "object"
  },
  "mod_name": {
    "description": "Required for spec-mode validation. Optional in archive-mode.",
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition. Required for spec-mode validation when target_platform='bedrock_skinpack'.",
    "properties": {
      "display_name": {
        "required": false,
        "type": "string"
      },
      "pack_id": {
        "required": false,
        "type": "string"
      },
      "skins": {
        "items": {
          "properties": {
            "display_name": {
              "required": true,
              "type": "string"
            },
            "geometry": {
              "default": "geometry.humanoid.custom",
              "enum": [
                "geometry.humanoid.custom",
                "geometry.humanoid.customSlim"
              ],
              "required": false,
              "type": "string"
            },
            "localization_name": {
              "required": false,
              "type": "string"
            },
            "skin_id": {
              "required": true,
              "type": "string"
            },
            "skin_type": {
              "default": "free",
              "description": "Skin type. Accepts skin_type or type as input.",
              "enum": [
                "free",
                "paid"
              ],
              "required": false,
              "type": "string"
            },
            "texture": {
              "description": "Required 64x64 PNG skin texture. Supply source_base64 or source_file_id for a user-drawn skin; color_hex renders a flat humanoid silhouette.",
              "properties": {
                "color_hex": {
                  "description": "Explicit #RRGGBB color the renderer expands into a kind-shaped procedural sprite. One of source_base64, source_file_id, or color_hex is required on every visible asset.",
                  "required": false,
                  "type": "string"
                },
                "palette_colors": {
                  "description": "When set, the (post-pixelize) image is quantized to this number of palette colors via Pillow's Fast Octree quantizer with dither off (median-cut is not supported on RGBA inputs in stock Pillow; Fast Octree is deterministic and dither-free). Recommend 8 for crisp Minecraft-style sprites. Range: 2-256. None disables quantization. Has no effect on color_hex bindings.",
                  "maximum": 256,
                  "minimum": 2,
                  "required": false,
                  "type": "integer"
                },
                "pixelize_to": {
                  "description": "When set, the source image is nearest-neighbor downscaled to this square dimension on ingest before being baked into the mod. Allowed values: 16, 32, 64, 128. Use 16 for items and blocks, 64 for entities and skins. None (default) keeps the source image at its uploaded dimensions. Has no effect on color_hex bindings.",
                  "maximum": 128,
                  "minimum": 16,
                  "required": false,
                  "type": "integer"
                },
                "source_base64": {
                  "description": "Base64-encoded image bytes (PNG or JPEG). Mutually exclusive with source_file_id. Max image dimension 1024 px, max byte size 5 MB.",
                  "required": false,
                  "type": "string"
                },
                "source_file_id": {
                  "description": "File Manager file_id for a user-uploaded image. The file is fetched budget-scoped, validated, and converted to PNG. Use this when a user drew or uploaded their own texture.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "maxItems": 64,
        "minItems": 1,
        "required": false,
        "type": "array"
      }
    },
    "required": false,
    "type": "object"
  },
  "source_archive_file_id": {
    "description": "File Manager file_id for a previously generated source zip. Supply this for archive-mode validation (skips spec validation; replays the zip's contents).",
    "required": false,
    "type": "string"
  },
  "target_platform": {
    "description": "Required for spec-mode validation. Optional in archive-mode (omit when passing source_archive_file_id). One of bedrock, bedrock_skinpack, fabric, neoforge.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": false,
    "type": "string"
  }
}
```
