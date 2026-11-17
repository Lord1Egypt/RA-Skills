# Minecraft Custom Mod Builder Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `minecraft-custom-mod-builder`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `create_mod_project`

Action slug: `create-mod-project`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/create-mod-project/invoke`

Price: `15` credits

Synchronous unverified source/debug generation. Accepts only verification_level='off'; use start_build_job for install-ready final artifacts.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advanced_resources` | `array` | no | Non-executable data/resource files or Bedrock .mcfunction files. Java source and Bedrock JavaScript are rejected. |
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock experimental features when required. |
| `assets` | `object` | no | Optional textures, sounds, particles, models, and language entries. |
| `authoring_mode` | `string` | no | Typed declarative generation mode. Agent-edited code must use start_build_job with source_archive_file_id. |
| `build_jar` | `boolean` | no | Fabric/NeoForge only. Build jar when true. |
| `compatibility_mode` | `string` | no | Strict platform fidelity. Platform-mismatched features are rejected, never dropped. |
| `description` | `string` | no | Short mod description. |
| `features` | `object` | no | FeatureSet object. Use arrays such as items, blocks, entities, events, commands, client_modules, machines, recipes, particles, sounds, functions, storage, worldgen, scoreboards, biomes, dimensions, effects, and skins. See get_instructions for nested fields. |
| `fidelity_policy` | `string` | no | Preserve intent by default. acknowledged_approximation is valid only after explicit user approval of a fully implemented alternative; placeholders are never accepted. |
| `include_file_preview` | `boolean` | no | Include capped text previews in generated_files. |
| `minecraft_version` | `string` | no | Pinned version. Omit unless explicitly needed. |
| `mod_id` | `string` | yes | Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$. |
| `mod_metadata` | `object` | no | Optional metadata such as version, license, authors, logo_texture, brand_color_hex, java_side, and bedrock_experiments. |
| `mod_name` | `string` | yes | Human-readable mod name. |
| `output_mode` | `string` | no | installable, source, or both. |
| `skin_pack` | `object` | no | Skin pack definition for target_platform=bedrock_skinpack. |
| `target_platform` | `string` | yes | bedrock, bedrock_skinpack, fabric, or neoforge. |
| `user_intent_summary` | `string` | no | Optional concise intent statement for deterministic classification; not used for silent reinterpretation. |
| `validate_output` | `boolean` | no | Run output validation when supported. |
| `verification_level` | `string` | no | create_mod_project is unverified and accepts only off. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "advanced_resources": {
    "description": "Non-executable data/resource files or Bedrock .mcfunction files. Java source and Bedrock JavaScript are rejected.",
    "items": {
      "description": "",
      "required": false,
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock experimental features when required.",
    "required": false,
    "type": "boolean"
  },
  "assets": {
    "description": "Optional textures, sounds, particles, models, and language entries.",
    "required": false,
    "type": "object"
  },
  "authoring_mode": {
    "description": "Typed declarative generation mode. Agent-edited code must use start_build_job with source_archive_file_id.",
    "enum": [
      "auto",
      "declarative"
    ],
    "required": false,
    "type": "string"
  },
  "build_jar": {
    "description": "Fabric/NeoForge only. Build jar when true.",
    "required": false,
    "type": "boolean"
  },
  "compatibility_mode": {
    "description": "Strict platform fidelity. Platform-mismatched features are rejected, never dropped.",
    "enum": [
      "strict"
    ],
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Short mod description.",
    "required": false,
    "type": "string"
  },
  "features": {
    "description": "FeatureSet object. Use arrays such as items, blocks, entities, events, commands, client_modules, machines, recipes, particles, sounds, functions, storage, worldgen, scoreboards, biomes, dimensions, effects, and skins. See get_instructions for nested fields.",
    "required": false,
    "type": "object"
  },
  "fidelity_policy": {
    "description": "Preserve intent by default. acknowledged_approximation is valid only after explicit user approval of a fully implemented alternative; placeholders are never accepted.",
    "enum": [
      "preserve_intent",
      "acknowledged_approximation"
    ],
    "required": false,
    "type": "string"
  },
  "include_file_preview": {
    "description": "Include capped text previews in generated_files.",
    "required": false,
    "type": "boolean"
  },
  "minecraft_version": {
    "description": "Pinned version. Omit unless explicitly needed.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$.",
    "required": true,
    "type": "string"
  },
  "mod_metadata": {
    "description": "Optional metadata such as version, license, authors, logo_texture, brand_color_hex, java_side, and bedrock_experiments.",
    "required": false,
    "type": "object"
  },
  "mod_name": {
    "description": "Human-readable mod name.",
    "required": true,
    "type": "string"
  },
  "output_mode": {
    "description": "installable, source, or both.",
    "enum": [
      "installable",
      "source",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition for target_platform=bedrock_skinpack.",
    "required": false,
    "type": "object"
  },
  "target_platform": {
    "description": "bedrock, bedrock_skinpack, fabric, or neoforge.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": true,
    "type": "string"
  },
  "user_intent_summary": {
    "description": "Optional concise intent statement for deterministic classification; not used for silent reinterpretation.",
    "required": false,
    "type": "string"
  },
  "validate_output": {
    "description": "Run output validation when supported.",
    "required": false,
    "type": "boolean"
  },
  "verification_level": {
    "description": "create_mod_project is unverified and accepts only off.",
    "enum": [
      "off"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `get_build_job`

Action slug: `get-build-job`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/get-build-job/invoke`

Price: `2` credits

Fetch one tenant-scoped build job by task_id. Poll until status is completed or failed, then inspect result.runtime_verification, result.visual_proof (File Manager frame file_ids/signed_urls; also in artifacts with label=visual_proof_frame), result.quality_gate, result.ready_for_install, and artifacts. Open visual proof frames before customer delivery.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Build job id returned by start_build_job. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Build job id returned by start_build_job.",
    "required": true,
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/get-instructions/invoke`

Price: `15` credits

Get tool instructions and available actions.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_build_jobs`

Action slug: `list-build-jobs`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/list-build-jobs/invoke`

Price: `2` credits

List recent Minecraft build jobs for the active budget to recover task_id values or inspect recent queued/completed builds.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum jobs to return, from 1 to 100. |

Sample parameters:

```json
{
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "Maximum jobs to return, from 1 to 100.",
    "required": false,
    "type": "integer"
  }
}
```

## `list_capabilities`

Action slug: `list-capabilities`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/list-capabilities/invoke`

Price: `2` credits

Return supported platforms, pinned versions, feature/action matrices, implementation_status, quality-gate fields, and unsupported families.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `target_platform` | `string` | no | Optional platform filter. |

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
    "description": "Optional platform filter.",
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

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/render-preview-image/invoke`

Price: `5` credits

Render and upload an enlarged PNG preview for an item, block, or entity from a structured spec, source archive, or direct image file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `features` | `object` | no | FeatureSet object for spec preview. |
| `mod_id` | `string` | no | Lowercase namespace for spec/source preview. |
| `mod_name` | `string` | no | Human-readable mod name for spec preview. |
| `preview_background` | `string` | no | checkerboard, transparent, white, or black. |
| `preview_size` | `integer` | no | Square preview PNG size from 32 to 1024 pixels. |
| `preview_source_file_id` | `string` | no | File Manager image file_id for direct image preview. |
| `preview_target_id` | `string` | no | Feature id or namespaced id, such as flame_sword or flame_tools:flame_sword. |
| `preview_target_kind` | `string` | no | item, block, or entity. |
| `skin_pack` | `object` | no | Skin pack definition for target_platform=bedrock_skinpack. |
| `source_archive_file_id` | `string` | no | File Manager file_id for a generated source zip to preview from. |
| `target_platform` | `string` | no | Optional platform context. |

Sample parameters:

```json
{
  "features": {},
  "mod_id": "example mod id",
  "mod_name": "example mod name",
  "preview_background": "checkerboard",
  "preview_size": 1,
  "preview_source_file_id": "example preview source file id",
  "preview_target_id": "example preview target id",
  "preview_target_kind": "item"
}
```

Generated JSON parameter schema:

```json
{
  "features": {
    "description": "FeatureSet object for spec preview.",
    "required": false,
    "type": "object"
  },
  "mod_id": {
    "description": "Lowercase namespace for spec/source preview.",
    "required": false,
    "type": "string"
  },
  "mod_name": {
    "description": "Human-readable mod name for spec preview.",
    "required": false,
    "type": "string"
  },
  "preview_background": {
    "description": "checkerboard, transparent, white, or black.",
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
    "description": "Square preview PNG size from 32 to 1024 pixels.",
    "required": false,
    "type": "integer"
  },
  "preview_source_file_id": {
    "description": "File Manager image file_id for direct image preview.",
    "required": false,
    "type": "string"
  },
  "preview_target_id": {
    "description": "Feature id or namespaced id, such as flame_sword or flame_tools:flame_sword.",
    "required": false,
    "type": "string"
  },
  "preview_target_kind": {
    "description": "item, block, or entity.",
    "enum": [
      "item",
      "block",
      "entity"
    ],
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition for target_platform=bedrock_skinpack.",
    "required": false,
    "type": "object"
  },
  "source_archive_file_id": {
    "description": "File Manager file_id for a generated source zip to preview from.",
    "required": false,
    "type": "string"
  },
  "target_platform": {
    "description": "Optional platform context.",
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

## `start_build_job`

Action slug: `start-build-job`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/start-build-job/invoke`

Price: `15` credits

Queue generated or agent-edited source for compile, package, real Minecraft runtime checks, File Manager visual_proof gallery, and the install-readiness gate. Poll get_build_job and ship only when result.ready_for_install=true and quality_gate.status='passed', after reviewing visual_proof frames.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advanced_resources` | `array` | no | Non-executable data/resource files or Bedrock .mcfunction files for generated spec builds. Edit executable source through source_archive_file_id. |
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock experimental features when required. |
| `assets` | `object` | no | Optional textures, sounds, particles, models, and language entries. |
| `authoring_mode` | `string` | no | Use auto/declarative for structured specs. Use agent_code only with source_archive_file_id for edited source. |
| `build_jar` | `boolean` | no | Fabric/NeoForge only. Build jar when true. |
| `compatibility_mode` | `string` | no | Strict platform fidelity. Platform-mismatched features are rejected, never dropped. |
| `description` | `string` | no | Short mod description. |
| `features` | `object` | no | FeatureSet object for generated spec builds. Omit when testing uploaded source_archive_file_id. |
| `fidelity_policy` | `string` | no | Preserve intent by default. acknowledged_approximation is valid only after explicit user approval of a fully implemented alternative; placeholders are never accepted. |
| `include_file_preview` | `boolean` | no | Include capped text previews in generated_files. |
| `minecraft_version` | `string` | no | Pinned version. Omit unless explicitly needed. |
| `mod_id` | `string` | yes | Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$. Required for spec builds and source-archive jobs. |
| `mod_metadata` | `object` | no | Optional metadata such as version, license, authors, logo_texture, brand_color_hex, java_side, and bedrock_experiments. |
| `mod_name` | `string` | no | Human-readable mod name. Required for spec builds; not required when source_archive_file_id is provided. |
| `output_mode` | `string` | no | installable, source, or both. |
| `skin_pack` | `object` | no | Skin pack definition for target_platform=bedrock_skinpack. |
| `source_archive_file_id` | `string` | no | File Manager file_id for a generated or agent-edited source zip. The job tests the uploaded source without regenerating over edits. Java zips must contain editable source/resources only; build/cache trees and precompiled .class, .jar, or native binaries are rejected. |
| `source_test_mode` | `string` | no | For source_archive_file_id jobs: test_only for iteration, or test_and_package to return install artifacts only after the quality gate passes. |
| `target_platform` | `string` | yes | bedrock, bedrock_skinpack, fabric, or neoforge. |
| `user_intent_summary` | `string` | no | Optional concise intent statement for deterministic classification; not used for silent reinterpretation. |
| `validate_output` | `boolean` | no | Run output validation when supported. |
| `verification_contract` | `object` | no | For edited-source behavior verification, define machine-observable expected_checks bound to the same target_platform and mod_id, including at least one behavior, render, or client check. |
| `verification_level` | `string` | no | behavior is the default install-ready gate; boot_smoke proves loading only and remains non-install-ready; off is unverified. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "advanced_resources": {
    "description": "Non-executable data/resource files or Bedrock .mcfunction files for generated spec builds. Edit executable source through source_archive_file_id.",
    "items": {
      "description": "",
      "required": false,
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock experimental features when required.",
    "required": false,
    "type": "boolean"
  },
  "assets": {
    "description": "Optional textures, sounds, particles, models, and language entries.",
    "required": false,
    "type": "object"
  },
  "authoring_mode": {
    "description": "Use auto/declarative for structured specs. Use agent_code only with source_archive_file_id for edited source.",
    "enum": [
      "auto",
      "declarative",
      "agent_code"
    ],
    "required": false,
    "type": "string"
  },
  "build_jar": {
    "description": "Fabric/NeoForge only. Build jar when true.",
    "required": false,
    "type": "boolean"
  },
  "compatibility_mode": {
    "description": "Strict platform fidelity. Platform-mismatched features are rejected, never dropped.",
    "enum": [
      "strict"
    ],
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Short mod description.",
    "required": false,
    "type": "string"
  },
  "features": {
    "description": "FeatureSet object for generated spec builds. Omit when testing uploaded source_archive_file_id.",
    "required": false,
    "type": "object"
  },
  "fidelity_policy": {
    "description": "Preserve intent by default. acknowledged_approximation is valid only after explicit user approval of a fully implemented alternative; placeholders are never accepted.",
    "enum": [
      "preserve_intent",
      "acknowledged_approximation"
    ],
    "required": false,
    "type": "string"
  },
  "include_file_preview": {
    "description": "Include capped text previews in generated_files.",
    "required": false,
    "type": "boolean"
  },
  "minecraft_version": {
    "description": "Pinned version. Omit unless explicitly needed.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$. Required for spec builds and source-archive jobs.",
    "required": true,
    "type": "string"
  },
  "mod_metadata": {
    "description": "Optional metadata such as version, license, authors, logo_texture, brand_color_hex, java_side, and bedrock_experiments.",
    "required": false,
    "type": "object"
  },
  "mod_name": {
    "description": "Human-readable mod name. Required for spec builds; not required when source_archive_file_id is provided.",
    "required": false,
    "type": "string"
  },
  "output_mode": {
    "description": "installable, source, or both.",
    "enum": [
      "installable",
      "source",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition for target_platform=bedrock_skinpack.",
    "required": false,
    "type": "object"
  },
  "source_archive_file_id": {
    "description": "File Manager file_id for a generated or agent-edited source zip. The job tests the uploaded source without regenerating over edits. Java zips must contain editable source/resources only; build/cache trees and precompiled .class, .jar, or native binaries are rejected.",
    "required": false,
    "type": "string"
  },
  "source_test_mode": {
    "description": "For source_archive_file_id jobs: test_only for iteration, or test_and_package to return install artifacts only after the quality gate passes.",
    "enum": [
      "test_only",
      "test_and_package"
    ],
    "required": false,
    "type": "string"
  },
  "target_platform": {
    "description": "bedrock, bedrock_skinpack, fabric, or neoforge.",
    "enum": [
      "bedrock",
      "bedrock_skinpack",
      "fabric",
      "neoforge"
    ],
    "required": true,
    "type": "string"
  },
  "user_intent_summary": {
    "description": "Optional concise intent statement for deterministic classification; not used for silent reinterpretation.",
    "required": false,
    "type": "string"
  },
  "validate_output": {
    "description": "Run output validation when supported.",
    "required": false,
    "type": "boolean"
  },
  "verification_contract": {
    "description": "For edited-source behavior verification, define machine-observable expected_checks bound to the same target_platform and mod_id, including at least one behavior, render, or client check.",
    "required": false,
    "type": "object"
  },
  "verification_level": {
    "description": "behavior is the default install-ready gate; boot_smoke proves loading only and remains non-install-ready; off is unverified.",
    "enum": [
      "off",
      "boot_smoke",
      "behavior"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `validate_mod_project`

Action slug: `validate-mod-project`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/minecraft-custom-mod-builder/actions/validate-mod-project/invoke`

Price: `5` credits

Validate a structured Minecraft mod spec or a previously generated/uploaded source archive without writing install artifacts.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allow_experimental_bedrock_features` | `boolean` | no | Allow Bedrock experimental features when required. |
| `features` | `object` | no | FeatureSet object for spec mode. Use get_instructions for nested fields. |
| `minecraft_version` | `string` | no | Pinned version. Omit unless explicitly needed. |
| `mod_id` | `string` | no | Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$. |
| `mod_name` | `string` | no | Human-readable mod name for spec mode. |
| `skin_pack` | `object` | no | Skin pack definition for target_platform=bedrock_skinpack. |
| `source_archive_file_id` | `string` | no | File Manager file_id for a generated or agent-edited source zip to validate instead of a spec. Java zips must contain editable source/resources only; generated outputs and precompiled executables are rejected. |
| `target_platform` | `string` | no | bedrock, bedrock_skinpack, fabric, or neoforge. |

Sample parameters:

```json
{
  "allow_experimental_bedrock_features": true,
  "features": {},
  "minecraft_version": "example minecraft version",
  "mod_id": "example mod id",
  "mod_name": "example mod name",
  "skin_pack": {},
  "source_archive_file_id": "example source archive file id",
  "target_platform": "bedrock"
}
```

Generated JSON parameter schema:

```json
{
  "allow_experimental_bedrock_features": {
    "description": "Allow Bedrock experimental features when required.",
    "required": false,
    "type": "boolean"
  },
  "features": {
    "description": "FeatureSet object for spec mode. Use get_instructions for nested fields.",
    "required": false,
    "type": "object"
  },
  "minecraft_version": {
    "description": "Pinned version. Omit unless explicitly needed.",
    "required": false,
    "type": "string"
  },
  "mod_id": {
    "description": "Lowercase namespace matching ^[a-z][a-z0-9_]{1,63}$.",
    "required": false,
    "type": "string"
  },
  "mod_name": {
    "description": "Human-readable mod name for spec mode.",
    "required": false,
    "type": "string"
  },
  "skin_pack": {
    "description": "Skin pack definition for target_platform=bedrock_skinpack.",
    "required": false,
    "type": "object"
  },
  "source_archive_file_id": {
    "description": "File Manager file_id for a generated or agent-edited source zip to validate instead of a spec. Java zips must contain editable source/resources only; generated outputs and precompiled executables are rejected.",
    "required": false,
    "type": "string"
  },
  "target_platform": {
    "description": "bedrock, bedrock_skinpack, fabric, or neoforge.",
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
