# Kling AI — API reference

Official source: [klingai.com/document-api/llms.txt](https://klingai.com/document-api/llms.txt)

| Subcommand | Endpoints |
| ---------- | --------- |
| `video`    | `POST /text-to-video/kling-3.0` (`kling-4.0` / `kling-4.0-flash` / `kling-3.0-turbo` / `kling-2.6` / `kling-2.5-turbo`); `POST /image-to-video/kling-3.0` (same model suffixes); `POST /omni-video/kling-3.0-omni`; `POST /omni-video/kling-o1`; `POST /omni-video/kling-4.0`; `POST /omni-video/kling-4.0-flash`; query `GET /tasks?task_ids=` |
| `image`    | `POST/GET /v1/images/generations`, `POST/GET /v1/images/omni-image`; `kling-4.0`: `POST /image-generation/kling-4.0`; long page (`--page ecommerce` / `webpage`): `POST /long-image-generation/kling-4.0`; query `GET /tasks?task_ids=` |
| `element`  | `POST/GET /v1/general/advanced-custom-elements`, `GET /v1/general/advanced-presets-elements`, `POST /v1/general/delete-advanced-elements` |
| `voice`    | `POST/GET /v1/general/custom-voices`, `GET /v1/general/presets-voices`, `POST /v1/general/delete-voices` |
| `account`  | `GET /account/costs` (quota/resource packs); bind flow (no Bearer, bind base): `POST /console/api/auth/skill/init-sessions`, `POST /console/api/auth/skill/exchange` |

Auth and polling notes:

- Official: path-encoded models (all `video` submit paths above) are **new API** and require `Authorization: Bearer <API Key>`. See [authentication](https://klingai.com/document-api/api/get-started/authentication.md).
- Official: `/v1/...` image and element paths are **old API** (`model_name` in body); API Key Bearer works.
- Current script: process env `KLING_API_KEY` is sent as Bearer as-is. Else `api_key` in `~/.config/kling/.credentials` is sent as Bearer (**no JWT**). `account --bind` writes that API Key from exchange `ISSUED`. `KLING_TOKEN` is not recognized.
- Bind APIs (`/console/api/auth/skill/...`) are device-bind endpoints and do not use Bearer.
- New video submit returns `data.id` + `data.status` (`submitted` / `processing` / `succeeded` / `failed`). Poll `GET /tasks?task_ids=` and read `outputs[].url`.
- Image/element/voice `/v1` submit still returns `task_id`; poll `GET {submit_path}/{task_id}` until `succeed`/`failed`, then read `task_result`.
- Image `kling-4.0` (`POST /image-generation/kling-4.0`) uses the new task shape: `data.id` / `data.status` (`succeeded`), poll `GET /tasks?task_ids=`, read `outputs[].url` where `type=image`. Resolution `2k`/`4k`/`8k`. No callback, watermark, or external task id in the CLI.
- Long page uses the same task shape on `POST /long-image-generation/kling-4.0`. `--page ecommerce` is 电商详情页 (1–3 `refer_image`, `length` `short`/`medium`/`long`). `--page webpage` is 网页设计 (0–1 `style_refer_image` + 0–1 `subject_refer_image` via `--image_types`; no `refer_image`, no `length`). Resolution `1k`/`2k`.

Account mode mapping:

- `account --costs`: remote call to `GET /account/costs`
- `account --bind` / `account --bind-url`: remote bind calls (`init-sessions` + `exchange`)
- `account --import-env` / `--import-credentials` / `--configure`: local credential operations only (no business API submit)

## Model docs

Official pages (primary source):

- [Docs index](https://klingai.com/document-api/llms.txt)
- [Video capability map](https://klingai.com/document-api/guides/capability-map/video.md)
- [Image capability map](https://klingai.com/document-api/guides/capability-map/image.md)
- Kling 4.0 T2V / I2V / Omni video: internal beta doc (2026.09.22), not yet on the public docs site
- Kling 4.0 Flash T2V / I2V / Omni video: internal beta doc, not yet on the public docs site. Duration 3–20 (omitted is not sent; do not fill 10; see SKILL.md Flash rules). 720p only; only an explicit first frame stays image-to-video; `last_frame` or `--image_tail` routes to Omni (no `middle_frame`); up to 5 reference videos; Omni aspect official default `adaptive`. No `contents` type `voice`
- Voice (`contents` type `voice`): `voice_id` plus `id`=`1`, prompt `@1`. kling-4.0 Omni only (max 3; T2V / I2V rejected; not on kling-4.0-flash) and kling-2.6 image-to-video only (max 2, `audio=native` + `1080p`). Not on kling-3.0 / kling-3.0-omni. Create/list: `voice` subcommand → `/v1/general/custom-voices` / `presets-voices` ([4.0 Omni](https://klingai.com/document-api/api/video/4-0/video-omni.md), [2.6 image-to-video](https://klingai.com/document-api/api/video/2-6/image-to-video.md)).
- [Kling 3.0 T2V](https://klingai.com/document-api/api/video/3-0-omni/text-to-video.md)
- [Kling 3.0 I2V](https://klingai.com/document-api/api/video/3-0-omni/image-to-video.md)
- [Kling 3.0 Omni video](https://klingai.com/document-api/api/video/3-0-omni/video-omni.md)
- [Kling 3.0 Turbo T2V](https://klingai.com/document-api/api/video/3-0-turbo/text-to-video.md)
- [Kling 3.0 Turbo I2V](https://klingai.com/document-api/api/video/3-0-turbo/image-to-video.md)
- [Kling O1 video](https://klingai.com/document-api/api/video/o1/video-omni.md)
- [Kling 2.6 T2V](https://klingai.com/document-api/api/video/2-6/text-to-video.md)
- [Kling 2.6 I2V](https://klingai.com/document-api/api/video/2-6/image-to-video.md)
- [Kling 2.5 Turbo T2V](https://klingai.com/document-api/api/video/2-5-turbo/text-to-video.md)
- [Kling 2.5 Turbo I2V](https://klingai.com/document-api/api/video/2-5-turbo/image-to-video.md)
- [Image 3.0 generations](https://klingai.com/document-api/api/image/3-0-omni/image-generation.md)
- [Omni image](https://klingai.com/document-api/api/image/3-0-omni/image-omni.md)
- [Elements](https://klingai.com/document-api/api/video/3-0-omni/elements.md)
- [Account costs](https://klingai.com/document-api/api/assets/account-usage.md)
