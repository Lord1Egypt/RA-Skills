# Model Selection Policy

Formal dynamic selection rules for the natural-language wrapper live in `catalog-aware-selection.md`.

## Preference Order

The current runtime in `scripts/ima_runtime/cli_flow.py` chooses models in this order:

1. explicit `--model-id`
2. saved per-user preference from `~/.openclaw/memory/ima_prefs.json`
3. interactive first-run selection when stdin is a TTY and `--output-json` is not enabled
4. no hidden fallback; non-interactive runs fail and require a model choice

For first-time operators, the intended helper paths are now:

1. `python3 scripts/ima_runtime_setup.py`
2. choose a task type and model interactively
3. let the helper save the local preference used by later CLI runs

Or:

1. run `python3 scripts/ima_runtime_cli.py --task-type ... --prompt "..."`
2. accept the suggested model or choose another in the terminal prompt
3. let the successful run persist the selected model as the local preference

After a successful run, `cli_flow.py` persists the resulting model as the preference for that `user_id` and `task_type`. The current CLI does not wait for an explicit "save this as default" confirmation.

Preferences are stored only in the current schema:

```json
{
  "users": {
    "u1": {
      "text_to_video": {
        "model_id": "wan2.6-t2v",
        "model_name": "Wan 2.6",
        "credit": 20,
        "last_used": "2026-04-03T12:34:56+00:00"
      }
    }
  }
}
```

Lookup reads only `users -> user_id -> task_type -> model_id`. Any other top-level or nested key shape is ignored and treated as having no saved preference.

`--version-id` is optional. When omitted, the runtime binds the last matching product-list leaf, which is treated as the newest available version in the current API ordering.

## Default Model Rules

The runtime does not auto-pick a hidden default model for video tasks. Documentation may recommend models for humans, and the interactive CLI can offer a recommended first-run choice, but non-interactive execution still requires either an explicit model or a saved preference.

This is deliberate. `ima_runtime_setup.py` and the interactive TTY prompt may suggest a catalog recommendation during onboarding when one is present; otherwise they fall back to an explicitly labeled first available model. Scripted or machine-readable execution still refuses to create a video task without either `--model-id` or a saved preference.

## Task-Type Recommendation Matrix

These recommendations are explicit operator guidance for onboarding and CLI help text. They are not hidden runtime defaults.

### `text_to_video`

- recommended: `ima-pro-fast` -> `Seedance 2.0 Fast`
- stable alternative: `wan2.6-t2v`
- premium: `ima-pro` -> `Seedance 2.0` (requires subscription)

### `image_to_video`

- recommended: `ima-pro-fast` -> `Seedance 2.0 Fast`
- stable alternative: `wan2.6-i2v`
- premium: `ima-pro` -> `Seedance 2.0` (requires subscription)

### `reference_image_to_video`

- recommended: `kling-video-o1`
- second choice: `ima-pro-fast` -> `Seedance 2.0 Fast`
- premium: `ima-pro` -> `Seedance 2.0` (requires subscription)

### `first_last_frame_to_video`

- recommended: `kling-video-o1`
- second choice: `ima-pro-fast` -> `Seedance 2.0 Fast`
- premium: `ima-pro` -> `Seedance 2.0` (requires subscription)

When no model is available, the safe fallback is operational rather than implicit:

1. run `python3 scripts/ima_runtime_setup.py`, or call `--list-models --task-type ...`
2. choose a supported `model_id`
3. bind that model against the live product list before create

## Alias And Canonicalization Rules

Known aliases are normalized before lookup:

- `Seedance 2.0` -> `ima-pro`
- `Seedance 2.0-Fast` and `Seedance 2.0 Fast` -> `ima-pro-fast`
- `Ima Sevio 1.0` -> `ima-pro`
- `Ima Sevio 1.0-Fast` and `Ima Sevio 1.0 Fast` -> `ima-pro-fast`

This repo uses `Seedance 2.0` / `Seedance 2.0 Fast` as the canonical operator-facing names.
The `Ima Sevio` forms remain supported as legacy aliases. All other model IDs are passed through as given.
Capability-specific model tables live under `capabilities/video/references/models.md`.
