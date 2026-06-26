# Natural-Language Routing

This repo now exposes two operator layers:

- structured execution: `python3 scripts/ima_runtime_cli.py ...`
- natural-language wrapper: `python3 scripts/route_and_execute.py --request "..."`

The wrapper exists to parse free-form user requests, validate them against the live catalog, and then call the structured runtime. It is a thin orchestration layer, not a second execution engine.

## Responsibility Split

- `parse_user_request.py`
  - infer task intent from free-form text
  - classify media roles
  - extract structured constraints such as `duration`, `resolution`, `aspect_ratio`, and audio intent
  - return clarification when the request is still ambiguous
- `validate_params.py`
  - fetch live catalog data
  - filter models by media capability and explicit structured constraints
  - rank compatible candidates using semantic intent
  - fail clearly on conflict
- `route_and_execute.py`
  - connect parsing and validation to the existing runtime
  - support `--dry-run` for safe inspection
  - call `ima_runtime_cli.py` behavior only after the route and model are stable
- `ima_runtime_cli.py`
  - remains the underlying execution contract
  - should not be treated as the natural-language understanding layer

## Core Principle

Natural-language understanding must not bypass runtime validation.

The wrapper may infer intent and propose a route, but it must still:

1. validate the inferred request against the live catalog
2. validate media counts and media roles
3. fail or clarify before create-task if the route is unstable

## Clarification Gate

The wrapper must stop and clarify when:

- two or more images are present but their roles are unclear
- the request could plausibly map to both `first_last_frame_to_video` and `reference_image_to_video`
- the user mixes speed and quality signals with no stable ranking preference and more than one live model remains compatible
- the request asks for reference media types that exceed what the live catalog exposes for the selected model

Recommended clarification style:

- ask about image roles first
- ask about model tradeoff second
- do not silently guess

## Output Contract

### `parse_user_request.py`

Returns a structured parse containing:

- `task_type`
- `intent_hints`
- `constraints`
- `semantic_intent`
- `explicit_model_id`
- `media_assets`
- `clarification` when needed

### `validate_params.py`

Returns one of:

- `status=ok` with `selected_model` and `compatible_models`
- `status=clarification`
- `status=error`

### `route_and_execute.py`

- `--dry-run` prints both parse and validation result
- normal execution delegates into the existing runtime after route/model stabilization

## Non-Goals

This wrapper does not:

- perform multi-step workflow chaining
- merge multiple output media types into one automatic pipeline
- bypass live-catalog capability checks
- replace the low-level runtime contract
