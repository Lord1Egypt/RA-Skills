---
name: likeadmin-market-skills
description: "Plan and run intelligent workflows through a user-configured 算力超市 tenant. Use only when the user explicitly requests 算力超市, provides its configured tenant context, or invokes this skill for model, app, media, digital-human, music, smart-clip, asset, or social-media operations."
---

# 算力超市skills

Operate 算力超市 as a capability graph, not as a collection of endpoints. Turn a user outcome into the smallest compatible workflow, obtain missing decisions only where they materially affect cost or output, then run and trace each node.

## Credentials Guard

Before every network call, read persistent credentials from:

```text
~/.likeadmin-market-skills/credentials.json
```

The user copies a JSON file to that exact location. Its only required fields are:

```json
{
  "base_url": "https://your-tenant-api-origin",
  "api_key": "your-api-key"
}
```

For installation surfaces that support copyable environment variables, provide this setup block. These variables are only used by the user's shell to populate the local credential file; the skill does not read them at runtime.

```bash
export LIKEADMIN_MARKET_BASE_URL="https://your-tenant-api-origin"
export LIKEADMIN_MARKET_API_KEY="your-api-key"
printf '%s\n%s\n' "$LIKEADMIN_MARKET_BASE_URL" "$LIKEADMIN_MARKET_API_KEY" | node scripts/api-client.mjs config import-lines
unset LIKEADMIN_MARKET_BASE_URL LIKEADMIN_MARKET_API_KEY
node scripts/api-client.mjs config status
```

- `base_url` is a tenant API origin. Remove a trailing `/`; never append or hardcode a tenant domain.
- Send `api_key` only as `Authorization: Bearer <api_key>`. Never print it, place it in URLs, or write it into workflow state.
- `node scripts/api-client.mjs config path` prints the target location. `config status` reports presence only. The helper creates the directory with `0700` permissions and the credential file with `0600` permissions.
- `manifest.yaml` is the machine-readable declaration of this boundary and labels the two copyable variables as setup-only. Do not call any API when either field is absent.

## Plan Before Calling

1. Classify the request as a direct capability, a multi-step outcome, an inspection/query, or a destructive asset operation.
2. Discover the tenant's actual availability before selection: `GET /models?detail=1`, `GET /apps`, and `GET /apps/{app_code}`. Use `GET /pricing` or `/pricing/batch` before a cost-sensitive task.
3. Read [capability-catalog.json](references/capability-catalog.json) for type contracts, then use `node scripts/read-contract.mjs <contract-id|model-code|app-code/api-code>` for the matching full contract. The bundled snapshot covers all 136 published documents, including 29 model and 72 application contracts, but is not proof that a resource is enabled for this tenant.
4. Build a DAG only where an upstream output satisfies a downstream input type. Preserve an explicit model/app choice. If several eligible alternatives differ materially in price, quality, duration, audio, or resolution, ask the user to choose. Never silently choose a premium option.
5. Validate every required field and constraint before spending points. Confirm destructive asset deletion. Do not retry voice cloning automatically because a retry can create another voice.

## Media URL Boundary

Every local path, attachment, `file://`, `blob:`, or private/unreachable URL used in a business URL field must first go through:

```text
POST ${base_url}/api/v1/upload
multipart field: file
```

Require `code=1` and use only `data.url` in the dependent request. Do not upload already-public `http(s)` URLs. These input URLs are temporary, normally at most 24 hours, so submit dependent nodes immediately. `storage` is output transfer, never an input uploader.

Before uploading any local path, explicitly tell the user the configured tenant API destination and obtain confirmation for that specific transfer. The workflow runner enforces `confirm_local_upload: true` for local files.

Use the catalog's `media_url_fields` as the baseline, then inspect the selected contract for nested fields such as `content[].image_url.url`, `media[].url`, `materials[].fileUrl`, and `garment.data[].url`.

## Execute Nodes Correctly

- Text models: use `POST /chat/completions`; `stream=true` is SSE, not a pollable task.
- Async model generation: use `POST /tasks` with `model` and business fields at the JSON root. Do not mix root business fields with a non-empty legacy `params` object.
- Application APIs: use the exact method and `${base_url}/api/v1/apps/{app_code}/{api_code}`. Preserve case-sensitive fields such as Seedance `URL`, `Name`, `GroupId`, and `ProjectName`.
- Do not force an application `mode=async` or `mode=task`. Some applications use `mode` as their own quality or generation setting.
- Treat `{code:0}` as failure even when HTTP status is 200.
- For a platform `task_id`, poll `GET /tasks/{task_id}` until `completed`, `failed`, or `cancelled`. Use an app-specific query only when its contract requires an upstream/elastic ID or the user specifically requests it.

Use an explicit `callback_url` only when the user supplies a reachable endpoint. Callbacks lack a signature header, so retain polling as recovery.

## Deterministic Workflow Runner

Use [workflow-runner.mjs](scripts/workflow-runner.mjs) for fragile, repeatable chains after the agent has made the required capability and template choices. It uploads local media, verifies each platform task before continuing, and can persist non-secret node state with `--state <file>`.

Supported recipes include `clone-voice`, `tts`, `lipsync`, `clone-voice-lipsync`, `image-avatar`, `realman-smart-clip`, `avatar-smart-clip`, `material-smart-clip`, and `news-smart-clip`. Read [workflow-inputs.md](references/workflow-inputs.md) before running one.

The runner intentionally does not select a Smart Clip `style_id`, force a quality/cost option, delete an asset, or cross application-specific IDs. Those remain user-confirmed orchestration decisions.

## Sensitive Operations

Use social-media lookup, search, listing, and watermark-removal APIs only for content the user owns or is authorized to process. Do not bulk enumerate profiles or combine search, listing, detail retrieval, and watermark removal into a collection workflow. For a destructive asset delete or sensitive media operation, obtain explicit confirmation immediately before the request and communicate in the user's language.

## Composition Rules

Read [orchestration.md](references/orchestration.md) for supported recipes and non-combinable IDs. The important boundaries are:

- A `voice_tts` clone ID is valid for `voice_tts` TTS, not automatically for music-generation persona/voice fields.
- `lipsync` requires both an audio URL and a source video URL; a still image is not a valid substitute.
- Smart Clip always starts with a scene-compatible template. `realMan`, `oralMixCutting`, and `newsMixCutting` are not interchangeable.
- Only pass a generated result forward after confirming it is a reachable URL of the target media type. IDs such as `audio_id`, `persona_id`, `asset_id`, and template IDs stay within the applications that define them.
- If no enabled capability matches, explain the missing prerequisite or unavailable resource rather than fabricating a workflow.

## Reference Routing

- [capability-catalog.json](references/capability-catalog.json): complete online snapshot index, live-at-snapshot flag, schemas, URL fields, billing and operation semantics.
- [orchestration.md](references/orchestration.md): intent routing, DAG recipes, branching decisions, and safety constraints.
- [contracts.bundle.json](references/contracts.bundle.json): full local contract bundle; use `read-contract.mjs` to retrieve a single document without loading all of it.
- [api-client.mjs](scripts/api-client.mjs): persistent-credential guard, discovery, upload, request, and polling helper.
