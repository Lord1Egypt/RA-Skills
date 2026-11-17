# AI Headshots API

Use this reference for the staged professional-headshot workflow. Use
`scripts/headshots.sh` for normal operation instead of assembling requests manually.

## Authentication and ownership

Send an account API key with the `headshot:process` scope:

```http
X-API-Key: $MCE_API_KEY
```

`Authorization: Bearer $MCE_API_KEY` is also accepted. The account user becomes the
owner of every project and private asset. Another account receives a not-found response
instead of access to that data. Server environment keys are not sufficient without a
user identity.

These discovery endpoints are public:

- `GET /v1/headshots/catalog?locale=en`
- `GET /v1/headshots/showcases?locale=en`
- `GET /v1/headshots/showcases/{showcase_id}?locale=en`
- `GET /v1/headshots/scenes/{scene_id}?locale=en`

Supported published locales are `en`, `zh-CN`, `ja-JP`, `ko-KR`, `th-TH`, `vi-VN`,
`ms-MY`, `id-ID`, and `fil-PH`. Short content-language aliases are accepted where documented.

## Workflow

Keep the identifiers returned by each stage:

```text
project_id -> preview_id -> reference_id -> job_id -> candidate_id
                                                   -> render_id -> export_id
```

Do not submit generation before the user has reviewed and confirmed the reference
preview. Generation consumes credits; preparation and discovery do not.

## Prepare a reference

### Create or restore a project

`POST /v1/headshots/projects` is multipart form data:

- `image` — required JPG, PNG, or WebP, subject to the service upload limit.
- `scene_id` — optional live scene id.
- `entry_source` — normally `direct_upload`, or `scene_gallery` when a scene led to the upload.

Do not combine `entry_source=direct_upload` with `scene_id`. Use `scene_gallery` when sending
a scene id; `scene_gallery` requires one.

Use `POST /v1/headshots/projects/{project_id}/source` with an `image` part to replace
the source while preserving the project history. Use `GET /v1/headshots/projects/{id}`
to restore a project, `GET /v1/headshots/projects` to list projects, and `DELETE` on the
project resource to remove it and its private derivatives.

### Inspect the source

`POST /v1/headshots/projects/{project_id}/inspect` returns practical eligibility:

```json
{"eligible": true, "status": "ready", "reasons": [], "warnings": []}
```

Stop when `eligible` is false. Surface warnings before creating a preview.

Set the garment catalog preference with
`POST /v1/headshots/projects/{project_id}/garment-preference`:

```json
{"garment_preference": "female"}
```

The value is `male`, `female`, or `null` to clear it. This selects catalog variants; it
does not infer or alter gender identity.

### Grade, smooth, and crop the reference preview

`POST /v1/headshots/projects/{project_id}/previews` accepts JSON:

```json
{
  "skin_base_id": "motu_business_neutral",
  "smoothing_strength": 0.2,
  "crop_spec_id": "profile_4x5",
  "crop_anchor": "auto",
  "crop_rotation": 0
}
```

- `skin_base_id` — allowed portrait base style; corrects skin colour and white balance.
- `smoothing_strength` — `0`–`1`; `0` preserves texture and applies no smoothing.
- `crop_spec_id` — normally `avatar_1x1`, `profile_4x5`, or `headshot_3x4`.
- `crop_anchor` — `auto`, `center`, or `manual`.
- `crop_zoom` — `1`–`2`; used by non-manual crop modes.
- `crop_offset_x`, `crop_offset_y` — `-1`–`1`.
- `crop_x`, `crop_y`, `crop_width`, `crop_height` — normalized complete rectangle for a manual crop.
- `crop_rotation` — `-15`–`15` degrees.

The response contains `preview_id`, the applied `parameters`, and a private image URL.
Download it with `GET /v1/headshots/projects/{project_id}/previews/{preview_id}/image`.

After the user approves the downloaded preview, confirm an immutable reference with
`POST /v1/headshots/projects/{project_id}/references`:

```json
{"preview_id": "hprev_..."}
```

Download it with
`GET /v1/headshots/projects/{project_id}/references/{reference_id}/image`.

Confirmation also makes the person available in the owner's reusable person-reference library.
Library deduplication uses the confirmed image content, not crop or skin-preparation parameters.

### Reuse or remove a saved person

- `GET /v1/headshots/person-references?limit=20` lists active library entries.
- `GET /v1/headshots/person-references/{person_reference_id}/image` downloads a private preview.
- `POST /v1/headshots/projects/from-person-reference` with
  `{"person_reference_id":"hperson_...","scene_id":"professional_profile"}` starts a new project.
- `POST /v1/headshots/projects/{project_id}/person-reference` with
  `{"person_reference_id":"hperson_..."}` switches the active person inside the same project.
- `DELETE /v1/headshots/person-references/{person_reference_id}` soft-deletes only the library entry.

Applying a person to an existing project replaces its future preparation source and appends a new
immutable reference version. Historical jobs, candidates, favorites, and references remain intact.
Soft deletion does not remove library assets or any project data, and history import must not
recreate a deleted entry.

## Configure and generate

Use the public catalog or scene endpoint to discover ids. Never invent ids or generation
prompts. The public API exposes controlled ids and compatibility, not internal prompts.

`POST /v1/headshots/recommendation` validates a partial selection and returns a complete
compatible configuration:

```json
{
  "project_id": "hproj_...",
  "reference_id": "href_...",
  "scene_id": "professional_profile",
  "generation_style_id": null,
  "pose_id": null,
  "outfit_id": null,
  "background_id": null,
  "output_ratio": "4:5",
  "framing": "auto"
}
```

Optional booleans are `hair_grooming_enabled` and `face_refinement_enabled`. Set
`allow_incompatible=true` only when the user explicitly chooses catalog options outside
the scene recommendation.

Submit the complete returned selection to `POST /v1/headshots/jobs` with an
`Idempotency-Key` header. `batch_size` is `1`, `2`, or `4`; `output_ratio` is `1:1`,
`4:5`, or `3:4`. A successful request returns HTTP 202 and a `job_id`.

Generation is asynchronous. Query `GET /v1/headshots/jobs/{job_id}`. Terminal states include
`completed`, `partially_completed`, `failed`, and `cancelled`; do not repeatedly submit a
replacement job while one is queued or running. A partially completed job may still contain
billable ready candidates, so surface `failure_reason` and retain every successful result.
Candidate entries contain `candidate_id`, `ordinal`, `status`, and an
`image_url` when ready. Download each private URL with the same API key.

Select a candidate with `POST /v1/headshots/jobs/{job_id}/selection` and
`{"candidate_id":"hcand_..."}`. Favorites are available under
`/v1/headshots/projects/{project_id}/favorites`.

## Post-process

List styles with:

```http
GET /v1/headshots/postprocess/styles?reference_id={reference_id}&locale=en
```

Each style maps a public style id to `base_id` and an optional `flavour_id`. Create a
render with `POST /v1/headshots/candidates/{candidate_id}/renders`:

```json
{"base_id": "motu_business_neutral", "flavour_id": null}
```

Download `GET /v1/headshots/renders/{render_id}/image`.

Create an immutable portrait-lighting Render directly from the Candidate master:

```json
{
  "render_kind": "portrait_lighting",
  "lighting_style": "natural_dimension",
  "lighting_strength": 0.70
}
```

To apply lighting after an existing grade, include that grade's explicit
`"source_render_id": "hrender_..."`. The response identifies `render_kind`,
`source_render_id`, `lighting_style`, and the resolved `lighting_strength`. The Candidate
master and every earlier Render remain unchanged; repeated identical requests reuse the
same cached Render.

For the preferred single-pass Headshots workflow, send the approved grade selection
in the same request instead of `source_render_id`:

```json
{
  "render_kind": "portrait_lighting",
  "base_id": "motu_business_neutral",
  "flavour_id": null,
  "lighting_style": "natural_dimension",
  "lighting_strength": 0.70
}
```

This runs grading and portrait lighting in one pipeline decode/parse/render pass and
creates one immutable output Render from the Candidate master.

## Export

Create a controlled crop with `POST /v1/headshots/candidates/{candidate_id}/exports`:

```json
{
  "source_type": "master",
  "crop_spec_id": "profile_4x5",
  "format": "jpeg",
  "quality": 92
}
```

Use `source_type="render"` plus the explicit `render_id` to export a post-processed
version. Supported crop specs include `avatar_1x1`, `profile_4x5`, `headshot_3x4`,
`bust_3x4`, `half_body_2x3`, `three_quarter_2x3`, `full_body_9x16`, and `banner_16x9`.
Formats are `jpeg`, `png`, and `webp`; quality is `70`–`100`.

Optional automatic adjustments are `offset_x` and `offset_y` from `-0.15` to `0.15`.
A manual crop requires the complete normalized rectangle and may include
`crop_rotation` from `-15` to `15`.

Download the returned `download_url`. Exports are immutable and tied to their explicit
candidate or render source.

## Errors and credits

- `400` — invalid transition, ids, compatibility, or parameters.
- `401` — missing or invalid session/API key.
- `402` — insufficient credits; do not retry unchanged.
- `403` — missing `headshot:process` or a non-user-bound service key.
- `404` — missing resource or owner mismatch.
- `409` — conflicting or duplicate state transition when applicable.
- `413` / `415` — invalid upload size or type.
- `503` — Headshots storage, worker, catalog, or post-processing is unavailable.

Preserve `Idempotency-Key` for a generation retry after an uncertain network response.
Surface provider or moderation failure details from the job instead of returning an old
candidate as if it were new.
