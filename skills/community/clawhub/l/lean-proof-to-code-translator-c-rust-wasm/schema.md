# Lean Proof To Code Translator - C Rust Wasm Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `lean-to-code-translator-w-proof-c-rust-wasm`

x402 availability: not enabled for this product.

## `generate`

Action slug: `generate`

Price: `5` credits

Compile a source-only Lean archive into verified C, Rust, or Wasm artifacts using the platform-pinned runtime and shared cache. This action starts an asynchronous task and returns a task_id immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entry_module` | `string` | no | Lean module to import from the uploaded source tree, for example UserProofs.Main. |
| `entry_symbol` | `string` | no | Lean definition to export from entry_module. Fully qualified names are accepted; unqualified names are tried as bare names and common namespace-qualified forms. |
| `source_archive_file_id` | `string` | no | Stored zip archive containing Lean source files under UserProofs/. Do not upload lakefile.lean, lean-toolchain, lake-manifest.json, or .lake. |
| `target_language` | `string` | no | Target language to generate. Supported values: c, rust, wasm. |
| `timeout_seconds` | `integer` | no | How long to wait for the isolated lean-service request before failing. |
| `use_vendored_runtime` | `boolean` | no | When true, generate from the vendored Lean runtime shipped in the isolated lean-service container. |

Sample parameters:

```json
{
  "entry_module": "example entry module",
  "entry_symbol": "example entry symbol",
  "source_archive_file_id": "example source archive file id",
  "target_language": "c",
  "timeout_seconds": 10,
  "use_vendored_runtime": true
}
```

Generated JSON parameter schema:

```json
{
  "entry_module": {
    "description": "Lean module to import from the uploaded source tree, for example UserProofs.Main.",
    "required": false,
    "type": "string"
  },
  "entry_symbol": {
    "description": "Lean definition to export from entry_module. Fully qualified names are accepted; unqualified names are tried as bare names and common namespace-qualified forms.",
    "required": false,
    "type": "string"
  },
  "source_archive_file_id": {
    "description": "Stored zip archive containing Lean source files under UserProofs/. Do not upload lakefile.lean, lean-toolchain, lake-manifest.json, or .lake.",
    "required": false,
    "type": "string"
  },
  "target_language": {
    "description": "Target language to generate. Supported values: c, rust, wasm.",
    "enum": [
      "c",
      "rust",
      "wasm"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "How long to wait for the isolated lean-service request before failing.",
    "maximum": 300,
    "minimum": 10,
    "required": false,
    "type": "integer"
  },
  "use_vendored_runtime": {
    "description": "When true, generate from the vendored Lean runtime shipped in the isolated lean-service container.",
    "required": false,
    "type": "boolean"
  }
}
```

## `get_targets`

Action slug: `get-targets`

Price: `5` credits

List the currently supported target languages and bundle requirements.

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

## `get_task`

Action slug: `get-task`

Price: `5` credits

Check the status of a generate or verify task and retrieve results when complete.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task ID returned from a previous generate or verify call. |

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
    "description": "Task ID returned from a previous generate or verify call.",
    "required": true,
    "type": "string"
  }
}
```

## `list_tasks`

Action slug: `list-tasks`

Price: `5` credits

List recent generate and verify tasks for the current budget.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum number of tasks to return. Default 20. |

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
    "description": "Maximum number of tasks to return. Default 20.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `verify`

Action slug: `verify`

Price: `5` credits

Verify a previously generated Lean proof export bundle against the same pinned runtime and shared cache. This action starts an asynchronous task and returns a task_id immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bundle_file_id` | `string` | yes | Stored bundle zip file_id produced by a previous generate call. |
| `target_language` | `string` | no | Target language encoded in the bundle. Supported values: c, rust, wasm. |
| `timeout_seconds` | `integer` | no | How long to wait for the isolated lean-service request before failing. |
| `verification_mode` | `string` | no | Use fast for hash checks or full to rebuild and re-export. |

Sample parameters:

```json
{
  "bundle_file_id": "example bundle file id",
  "target_language": "c",
  "timeout_seconds": 10,
  "verification_mode": "fast"
}
```

Generated JSON parameter schema:

```json
{
  "bundle_file_id": {
    "description": "Stored bundle zip file_id produced by a previous generate call.",
    "required": true,
    "type": "string"
  },
  "target_language": {
    "description": "Target language encoded in the bundle. Supported values: c, rust, wasm.",
    "enum": [
      "c",
      "rust",
      "wasm"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "How long to wait for the isolated lean-service request before failing.",
    "maximum": 300,
    "minimum": 10,
    "required": false,
    "type": "integer"
  },
  "verification_mode": {
    "description": "Use fast for hash checks or full to rebuild and re-export.",
    "enum": [
      "fast",
      "full"
    ],
    "required": false,
    "type": "string"
  }
}
```
