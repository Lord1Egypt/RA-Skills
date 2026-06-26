# Entry And Routing

## Runtime Handoff

The repo now exposes two public entry shapes:

- structured runtime entry: `scripts/ima_runtime_cli.py`
- natural-language wrapper entry: `scripts/route_and_execute.py`

The structured path flows into `ima_runtime.cli_parser`, then `ima_runtime.cli_flow`, and then the video capability route.
The natural-language path first runs `parse_user_request.py`, then `validate_params.py`, and delegates to the structured runtime only after route and model selection are stable.

In `cli_flow.py` the structured runtime:

1. resolves API key and CLI flags
2. fetches the live product list for the requested `task_type`
3. validates and prepares media inputs
4. builds a `GatewayRequest`
5. resolves the request into a video `TaskSpec`
6. binds a live model version and executes the video task

The repo is video-only, so both entry paths eventually call `capabilities/video/routes.py` after building a `GatewayRequest`. The separate gateway router in `scripts/ima_runtime/gateway/router.py` remains an internal seam for future multi-capability dispatch, but it is not part of the active direct execution path today.

## Natural-Language Wrapper Contract

`route_and_execute.py` is the only supported free-form wrapper in this repo.

It must:

1. parse free-form user intent into structured constraints
2. validate the request against the live catalog
3. clarify before execution when route or model choice is not stable
4. delegate to the structured runtime only after those checks pass

It must not:

- silently bypass media-role ambiguity
- silently bypass live-catalog incompatibility
- invent a model when multiple compatible candidates remain and semantic intent is insufficient

## Clarification Boundary

`build_video_task_spec()` is the authority for task-type routing:

- explicit `intent_hints.task_type` wins when it is one of the supported video task types
- `video_mode=first_last_frame` maps to `first_last_frame_to_video`
- `video_mode=reference` maps to `reference_image_to_video`
- one input image defaults to `image_to_video`
- zero input images defaults to `text_to_video`
- two or more images without an explicit role triggers a `ClarificationRequest`

That clarification boundary is deliberate. Neither the wrapper nor the runtime should guess whether two images mean first/last frame, reference images, or "animate only one of them".
