# Endpoint Mapping

This reference is distilled from public PixelLab API docs, OpenAPI metadata, official tutorial coverage, and community workflow notes. PixelLab may change request fields over time, so run `scripts/pixellab_workflow.py refresh-api-metadata --output-dir <run-dir>` when route behavior looks stale.

## Core Route Families

| Goal | Preferred endpoints | Notes |
|---|---|---|
| Simple image or sprite from text | `/v2/create-image-pixflux`, `/v2/create-image-pixflux-background`, `/v2/create-image-pixen`, `/v2/create-image-bitforge` | Use these before Pro multi-output routes for ordinary 64/128/200px sprites. Pixflux exposes view/direction/outline/shading/detail/init/color controls; Pixen covers larger simple outputs; Bitforge is reference/palette friendly. |
| Pro/reference candidate generation | `/v2/generate-image-v2`, `/v2/generate-with-style-v2` | Treat these as async candidate generation, not one-call-one-asset. They can return multiple candidates; build a contact sheet and approve an index. |
| Convert or clean up an existing image | `/v2/image-to-pixelart`, `/v2/image-to-pixelart-pro`, `/v2/remove-background`, `/v2/resize`, `/v2/edit-image`, `/v2/edit-images-v2`, `/v2/inpaint`, `/v2/inpaint-v3` | Good for concept art, screenshots, rough mockups, cleanup passes, and transparent exports. |
| Rotation and directional views | `/v2/rotate`, `/v2/generate-8-rotations-v3` | Prefer v3 for ordinary 8-direction packs. Use `/v2/generate-8-rotations-v2` only for Pro rotation workflows. |
| Animation | `/v2/create-character-state`, `/v2/animate-with-text-v3`, `/v2/animate-with-text-v2`, `/v2/animate-with-text`, `/v2/animate-with-skeleton`, `/v2/edit-animation-v2`, `/v2/interpolation-v2`, `/v2/transfer-outfit-v2`, `/v2/objects/{object_id}/animations`, `/v2/characters/animations`, `/v2/animate-character` | Use states before motion when the source pose is stiff. Use v3 for modern text animation from frames. Use transfer outfit plus edit animation for modular clothing layers. Use interpolation for in-betweens after key poses exist. Use skeleton when motion control matters. |
| Tiles | `/v2/create-tileset`, `/v2/tilesets`, `/v2/create-tileset-sidescroller`, `/v2/tilesets-sidescroller`, `/v2/create-tiles-pro`, `/v2/create-isometric-tile` | Do not generate tiles through generic image endpoints by default. Match top-down, side-scroller, Pro tile, and isometric tile workflows to their own routes. |
| UI | `/v2/generate-ui-v2` | Use the UI route for HUDs, panels, buttons, inventory strips, and icons. |
| Map props and reusable objects | `/v2/map-objects`, `/v2/create-1-direction-object`, `/v2/create-8-direction-object`, `/v2/objects`, `/v2/objects/{object_id}/states`, `/v2/objects/{object_id}/animations` | Use map/object routes for pickups, hazards, props, doors, chests, interactables, and assets that may later need states or animation. |
| Characters and objects | `/v2/create-character-v3`, `/v2/create-character-with-4-directions`, `/v2/create-character-with-8-directions`, `/v2/create-character-pro`, `/v2/create-character-state`, `/v2/create-1-direction-object`, `/v2/create-8-direction-object`, `/v2/characters`, `/v2/objects`, `/v2/objects/{object_id}/states`, `/v2/objects/{object_id}/select-frames` | Use character/object creators when later state or animation reuse is likely. Use list/get/tag management only for account-owned assets. Account cleanup is outside this asset-generation workflow. |
| Prompt enhancement | `/v2/enhance-pixen-prompt`, `/v2/enhance-character-v3-prompt`, `/v2/enhance-animation-v3-prompt` | Use before expensive generation when the user's prompt is thin or vague. |

## Size And Workflow Notes

- Pixflux/Pixen/Bitforge image creation currently requires `description` and `image_size`; use `no_background`, not `remove_background`, when transparent output is needed.
- `/v2/create-character-v3` currently accepts `view` values `side`, `low top-down`, or `high top-down`. Do not send a `direction` field to this endpoint; put facing language in the prompt or use 4/8-direction character endpoints when direction packs matter.
- Current linted size limits: Pixflux up to 400x400, Pixen up to 512x512 with dimensions divisible by 4, Bitforge up to 200x200, Rotate up to 128x128, Resize up to 200x200, Isometric tile up to 64x64.
- `/v2/create-1-direction-object` can produce multiple objects from one request depending on size; when it does, the object can enter review and require frame/object selection.
- `/v2/map-objects` supports `view`, `outline`, `shading`, `detail`, init image, forced palette image, background/map image, and inpainting controls.
- Image-to-pixel-art: use when converting non-pixel source images; send a `Base64Image`, input `image_size`, and desired `output_size`.
- Resize: pixel-art-aware resize, described in the report as 16x16 to 200x200.
- Remove background: transparent PNG workflow; send `image`, `image_size`, and optional `background_removal_task`.
- Rotate: directional camera/view workflow; send `from_image`, `image_size`, and direction/view changes.
- Animate-with-text v3: requires `first_frame` and `action`; accepts optional `last_frame`, even `frame_count` from 4 to 16, `no_background`, `seed`, and `enhance_prompt`.
- Transfer outfit v2 and edit animation v2: both work on 2 to 16 frames and require matching frame `size` values plus output `image_size`; use these for modular outfit/equipment layers.
- Interpolation v2: requires `start_image`, `end_image`, `action`, and `image_size`; use it after key poses exist, not as the first motion design step.
- Create character state: requires `character_id` and `edit_description`; use it to pose the same character before animation.
- Isometric tile: described in the report as 16x16 to 64x64.
- Create tiles (Pro): use `/v2/create-tiles-pro` for square, hex, pointy-hex, isometric, and octagon tile variants with tile size, view angle, thickness/depth, and optional style tiles. Fetch finished tiles with `/v2/tiles-pro/{tile_id}` when the response provides a tile id.

## Errors To Surface

- `401`: invalid API key. Ask the user to fix local credential configuration; do not print the key.
- `402`: insufficient credits. Tell the user it is an account/billing limit, not a code bug.
- `422`: validation error. Inspect the payload against current endpoint docs.
- `429` or `529`: throttling or rate limiting. The helper retries idempotent `GET`/`HEAD` requests with bounded exponential backoff; `POST` generation calls are not retried automatically.
- `502`, `503`, `504`: service-side transient failures. The helper retries idempotent polling/get requests but does not resubmit paid generation POSTs automatically.

## Background Jobs

Some PixelLab flows return a background job id. Use `--poll` with the helper, or call:

```bash
python3 pixellab-ai/scripts/pixellab_client.py get /v2/background-jobs/JOB_ID --poll --quiet
```

For a timed-out result file, resume polling instead of submitting another paid POST:

```bash
python3 pixellab-ai/scripts/pixellab_client.py poll-result-file ./run/results/meta/asset/result.json \
  --result-file ./run/results/meta/asset/result.json \
  --download-dir ./run/candidates/asset
```

Timeout means the job may still be processing. It is not proof of generation failure.
