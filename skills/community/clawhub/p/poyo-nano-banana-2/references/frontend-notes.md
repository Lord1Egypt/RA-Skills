# Frontend implementation notes from desktop `poyoapi`

These notes come from the local desktop frontend at `/Users/ronny/Desktop/poyoapi`.

## Relevant files

- `components/tool/nano-banana-2/index.tsx`
- `services/nanobananaService.ts`
- `data/models.json`
- `app/[locale]/models/nano-banana-2-api/ClientPage.tsx`

## What the frontend actually does

### Request flow

1. Upload user images first and obtain public URLs.
2. Submit `POST /api/generate/submit` with a JSON body.
3. Read `response.data.task_id`.
4. Poll `GET /api/generate/status/{task_id}` every 3 seconds until `finished` or `failed`.

### Supported models in the shared component

The frontend component knows about these model ids:

- `nano-banana-2-new`
- `nano-banana-2-new-edit`
- `nano-banana-2`
- `nano-banana-2-edit`
- `nano-banana`
- `nano-banana-edit`

For this skill, prefer the newer documented pair:

- `nano-banana-2-new`
- `nano-banana-2-new-edit`

### Frontend capability map

For the newer pair, the UI enables:

- `resolution`: yes
- `google_search`: yes
- `mask`: no
- reference images on edit model: yes
- max reference images for `nano-banana-2-new-edit`: 14

### Frontend file validation

Reference image uploads are validated as:

- max file size: 10 MB
- allowed MIME types: `image/jpeg`, `image/png`, `image/webp`

The component also contains mask-upload code for other model families, but Nano Banana 2 New currently has no mask capability enabled.

### Default UX choices in the frontend

- default prompt: `Generate image：Nano Banana 2 API is now available on Poyo.ai`
- default resolution: `1K`
- default aspect ratio: `16:9`
- status polling interval: 3 seconds

## Product/marketing copy used by the frontend

`data/models.json` describes Nano Banana Pro as:

- provider: Google
- tasks: Text to Image, Image to Image
- positioning: advanced Gemini image model with 4K output, stronger reasoning, real-time data integration, and multi-image composition

That copy is marketing-facing; use API docs as the source of truth for technical behavior.

## Practical guidance for skill users

- If a user provides local images, upload them somewhere reachable first, then pass URL(s) in `input.image_urls`.
- If the request is edit-oriented, require at least one source image.
- Polling every ~3 seconds matches the current frontend implementation.
- Prefer `16:9` for general demos because the PoYo frontend uses that default.
