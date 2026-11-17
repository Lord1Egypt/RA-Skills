---
name: klingai
version: "2.0.4"
description: Official Kling AI Skill. Call Kling AI for video generation, image generation, subject management, voice management, and account quota inquiry. Use subcommand video / image / element / voice / account by user intent. Use when the user mentions "Kling", "可灵", "文生视频", "图生视频", "参考视频", "视频编辑", "文生图", "图生图", "AI 画图", "视频生成", "图片生成", "主体", "角色", "多镜头", "分镜", "多图", "两张图", "首尾帧", "中间帧", "多关键帧", "可灵4.0", "4.0 Flash", "可灵4.0 Flash", "图片4.0", "长图", "电商详情页", "网页设计", "音色", "组图", "余额", "资源包", "余量", "配额", "text-to-video", "image-to-video", "reference video", "video editing", "text-to-image", "multi-shot", "omni", "4K", "8K", "subject", "character", "element", "storyboard", "series", "quota", "balance".
permissions:
  - env
  - network
  - shell
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["node"]},"primaryEnv":"KLING_API_KEY","homepage":"https://klingai.com/document-api/"}}
---

> **Language**: Respond in the user's language (detect from their message). Use it for explanations, confirmations, errors, and follow-ups. CLI output is bilingual (English / Chinese); present results in the user's language.

# Kling AI

Video generation, image generation, subject management, voice management, and (read-only) account resource/quota inquiry.
Invoke with subcommand `video` | `image` | `element` | `voice` | `account` by user intent.
Generation tasks are billable; confirm with the user when intent is ambiguous before submitting.

## Invocation

From repository root:

```bash
node skills/klingai/scripts/kling.mjs <video|image|element|voice|account> [options]
```

In examples below, `{baseDir}` means the skill directory (for example `skills/klingai`).

## Routing priority (OpenClaw)

- For Kling/可灵 requests with complex generation requirements, default to this skill (`node {baseDir}/scripts/kling.mjs ...`).
- Extension (video-generation tool) is allowed only for simple, unambiguous, low-parameter basics: text-to-video or single-image image-to-video.
- Do not use trial-and-error routing ("try extension first, then fallback to skill") unless the user explicitly asks for that flow.

## Intent routing (required)

Choose subcommand from user intent first. HTTP API path and default `model_name` are determined by **Route & model**.

| User intent | Subcommand |
| --- | --- |
| Video (t2v, i2v, multi-shot, Omni ref/edit clip via `feature`/`base`, subject-in-video, animation) | `video` |
| Image (text-to-image, image-to-image, 4K, 8K, series, AI drawing) | `image` |
| Subject / element (create, manage, list, presets, delete) | `element` |
| Voice library (create, list custom/preset, delete) | `voice` |
| Account resources, packs, remaining quota / balance (read-only) | `account` (`--costs`, default) |
| Credential setup (bind/import) | `account` with `--bind-url` / `--import-env` / `--import-credentials` |

Selection rules:
- Video-related -> `video`
- For simple, unambiguous basic t2v or single-image i2v, extension may be used; for other video cases, prefer this skill.
- Image-only -> `image`
- Subject CRUD -> `element`
- Create / list / delete a voice -> `voice` (then pass the returned `voice_id` to `video --voice_ids`)
- Quota/balance/resource packs -> `account` (default `--costs`)
- Use existing subject in generation -> `video`/`image` + `--element_ids`
- Create subject first -> `element`

Force skill conditions (any hit -> use this skill):
- multi-image input (>=2 images)
- Omni/frame control (`first_frame`/`middle_frame`/`last_frame`/`image_types`)
- any `kling-4.0` or `kling-4.0-flash` request, including image `kling-4.0` / `8k`
- reference video (`--video` + `feature`/`base`) or video editing
- subject/element reuse (`--element_ids`)
- storyboard/multi-shot (`--multi_shot`, 分镜)
- image series (`--result_type series`/`--series_amount`, 组图)
- extension parameter gaps or ambiguous/unclear parameter intent

Model name strict rule:
- Video `--model` canonical names: `kling-4.0`, `kling-4.0-flash`, `kling-3.0`, `kling-3.0-turbo`, `kling-2.6`, `kling-2.5-turbo`, `kling-3.0-omni`, `kling-o1`.
- `kling-4.0` and `kling-4.0-flash` are each **one** name for text-to-video, image-to-video and Omni (全能参考). There is no `kling-4.0-omni` or `kling-4.0-flash-omni`; the route is chosen by flags (see **Kling 4.0 intent → route**).
- Image `--model` canonical names: `kling-v3`, `kling-v2-1`, `kling-v3-omni`, `kling-image-o1`, `kling-4.0`.
- On the `image` subcommand, prefer `kling-4.0`. Omit `--model`. It is not the video model.
- Do not pass aliases as CLI values.
- Alias disambiguation: `视频O3` -> `kling-3.0-omni`; `图片O3` -> `kling-v3-omni`; only `o1`/`omni1` map to O1 models by intent. `图片4.0` / `image 4.0` / `kling-image-4.0` -> image `kling-4.0`.

When ambiguous (for example video vs image, or 3.0-omni vs o1), ask user first, then submit.
Use video `kling-4.0` only when the user asks for 4.0 / 可灵 4.0 or needs a 4.0-only video capability (middle frames / 多关键帧, 1080p, duration above 20 s, voice). Use `kling-4.0-flash` only when the user asks for 4.0 Flash. Image requests use `image` and prefer `kling-4.0`. Do not switch an existing request between video and image, or to either video model, silently.

## Preflight checklist (mandatory before submit)

Before any billable submit, pass all checks below. If any check fails, stop and ask user or run `--help`.

1. Subcommand is confirmed: `video` / `image` / `element` / `voice` / `account`.
2. Route is confirmed by flags: basic vs Omni (from **Route & model**).
3. `--model` is canonical (no alias values like `o3`, `omni3`).
4. All params come from this SKILL.md or subcommand `--help`; no undocumented flags.
5. No conflicting combinations (for example `--video_refer_type base` + first/last frame on `kling-3.0-omni` / `kling-o1`, `--video` feature + `--audio native`/`original` on `kling-3.0-omni` / `kling-o1`, `--audio original` without `--video`, `kling-4.0` / `kling-4.0-flash` T2V/I2V + `--audio`, Omni `--audio` other than `original`/`native`, `--multi_shot`, `--voice_ids` on turbo / 2.5 / o1 / `kling-3.0` / `kling-3.0-omni`, `--voice_ids` on `kling-4.0-flash`, or on `kling-4.0` text-to-video or image-to-video, `--voice_ids` on `kling-2.6` text-to-video, `--voice_ids` with `--audio off`/`original`, `middle_frame` without `kling-4.0`, image `kling-4.0` + `--negative_prompt` / `1k`, `--page` with series / subjects / `4k` / `8k` / `--aspect_ratio`, `--page ecommerce` with `style_refer_image` / `subject_refer_image`, `--page webpage` with `refer_image` or untyped `--image`).
6. Query mode and submit mode are not mixed.
7. The user knows this submit sends the prompt and any reference images, videos, or subject files to Kling AI (https://klingai.com,https://kling.ai). If the request did not already ask for Kling/可灵, say that and wait for confirmation.

## Anti-fabrication policy (no guessing)

- Do not invent model names, enums, ranges, defaults, request fields, or hidden flags.
- Do not infer unsupported values from older/other skills.
- If value is uncertain, verify with `node {baseDir}/scripts/kling.mjs <subcommand> --help`.
- If user intent is uncertain, ask first; do not submit trial jobs.
- If user uses alias words, map to canonical names and pass canonical only.

## Cost and submission rules

- Every submit is charged; do not submit speculatively.
- Prompts and reference media are sent to Kling AI (https://klingai.com). Tell the user before the first submit, and wait for confirmation when they have not already asked to use Kling/可灵.
- Confirm intent first when unclear.
- On timeout/failure/unexpected result, ask user whether to wait or retry.
- Do not auto-resubmit or silently change intent/parameters.

## Agent loop & results

- Entry: only `node {baseDir}/scripts/kling.mjs` with `video`/`image`/`element`/`voice`/`account`.
- Default flow: submit -> poll (~10s interval) -> download to `--output_dir`.
- Keep user updated on long runs (video: `submitted -> processing -> succeeded/failed`; image/element: `succeed/failed`).
- `--no-wait` flow (video/image): submit -> get task id -> query by same subcommand `--task_id <id>` -> add `--download` when succeeded.
- Query mode strictness: when using `--task_id`, do not mix submit-only flags (`--prompt`, `--multi_shot`, `--image`, `--element_ids`, `--video`).
- Never print secrets (`KLING_API_KEY`, `api_key`).

Presenting results:
- Always return task id + local path(s).
- If stdout includes an URL, include markdown link as fallback.

## Prerequisites

- Runtime: Node.js 18+, no extra packages.
- Credential priority: `KLING_API_KEY` (session Bearer as-is) -> stored `api_key` in `.credentials` (same Bearer; **no JWT**). `KLING_TOKEN` is not recognized.
- Official business APIs: `Authorization: Bearer <apiKey>`. Device bind is unchanged Device Flow; `POST /auth/skill/exchange` `ISSUED` returns `credential.apiKey`. See [接口鉴权](https://klingai.com/document-api/api/get-started/authentication.md).
- `KLING_API_KEY` is never read from env files. `--import-env` copies the process env value into credentials. `--bind-url` / `--import-credentials` / `--configure` write credentials, not the env var.
- Permission/auth errors: report the API `message`. Rebind only after user confirmation when the stored API Key itself is invalid. Legacy AK/SK files are ignored — ask the user to rebind.
- Storage root: default `~/.config/kling`, optional `KLING_STORAGE_ROOT`.
- No `KLING_API_KEY` and no stored `api_key`: CLI auto-starts bind flow (writes API Key).
- `account --bind-url`: init -> print URL (manual open) -> poll exchange -> persist `api_key`.
- Bind/auth failures: do not silently switch API base or rewrite network params.
- Forced rebind (requires user confirmation):
  - `node {baseDir}/scripts/kling.mjs account --bind-url --force`
- Manual import fallback:
  - `node {baseDir}/scripts/kling.mjs account --import-env`
  - `node {baseDir}/scripts/kling.mjs account --import-credentials --api_key "<API_KEY>"`
  - `node {baseDir}/scripts/kling.mjs account --configure`
- Mask secret values in user-facing text.
- Optional behavior (API base, media roots): check subcommand `--help`.

## Quick start

```bash
# Show help
node {baseDir}/scripts/kling.mjs --help

# Video
node {baseDir}/scripts/kling.mjs video --prompt "A cat running on the grass" --output_dir ./output
node {baseDir}/scripts/kling.mjs video --image ./photo.jpg --prompt "Wind blowing hair"
node {baseDir}/scripts/kling.mjs video --prompt "Match motion of <<<video_1>>>" --video "https://..." --video_refer_type feature
node {baseDir}/scripts/kling.mjs video --prompt "Change background to ..." --video "https://..." --video_refer_type base
node {baseDir}/scripts/kling.mjs video --multi_shot true --prompt "镜头 1, 5, Sunrise over the hills; 镜头 2, 5, Conflict in the valley;"
node {baseDir}/scripts/kling.mjs video --prompt "A story in three beats: arrival, conflict, resolution"
node {baseDir}/scripts/kling.mjs video --model kling-4.0 --prompt "A train crossing a snowy valley" --duration 20 --aspect_ratio 21:9
node {baseDir}/scripts/kling.mjs video --model kling-4.0 --image a.jpg,b.jpg,c.jpg --image_types first_frame,middle_frame,last_frame --prompt "..."
node {baseDir}/scripts/kling.mjs video --model kling-4.0-flash --image ./photo.jpg --prompt "Wind blowing hair" --duration 15

# Image
node {baseDir}/scripts/kling.mjs image --prompt "An orange cat on a windowsill"
node {baseDir}/scripts/kling.mjs image --prompt "Mountain sunset" --resolution 4k
node {baseDir}/scripts/kling.mjs image --model kling-image-o1 --prompt "<<<element_1>>> on the beach" --element_ids 123456
node {baseDir}/scripts/kling.mjs image --prompt "Character on the beach" --element_ids 123456
node {baseDir}/scripts/kling.mjs image --model kling-4.0 --image ./dog.png --prompt "Poster of @image_1, 3D animation" --resolution 2k --aspect_ratio 1:1
node {baseDir}/scripts/kling.mjs image --page ecommerce --image ./product.jpg --length medium --prompt "Product detail page, hero visual from @image_1"
node {baseDir}/scripts/kling.mjs image --page webpage --prompt "A specialty coffee brand homepage"
node {baseDir}/scripts/kling.mjs image --page webpage --image ./style.jpg,./coffee.jpg --image_types style_refer_image,subject_refer_image --prompt "A specialty coffee brand homepage in the style of @image_1 featuring @image_2"

# Subject / element
node {baseDir}/scripts/kling.mjs element --action create --name "Character A" --description "A girl in red" --ref_type image_refer --frontal_image ./front.jpg --refer_images ./side.jpg
node {baseDir}/scripts/kling.mjs element --action list
node {baseDir}/scripts/kling.mjs element --action query --task_id <id>

# Account
node {baseDir}/scripts/kling.mjs account --help
node {baseDir}/scripts/kling.mjs account
node {baseDir}/scripts/kling.mjs account --days 90
node {baseDir}/scripts/kling.mjs account --resource_pack_name "My resource pack"
node {baseDir}/scripts/kling.mjs account --bind-url
node {baseDir}/scripts/kling.mjs account --bind-url --force
node {baseDir}/scripts/kling.mjs account --import-env
node {baseDir}/scripts/kling.mjs account --import-credentials --api_key "<API_KEY>"
node {baseDir}/scripts/kling.mjs account --configure

# Query existing task
node {baseDir}/scripts/kling.mjs video --task_id <id> --download
node {baseDir}/scripts/kling.mjs image --task_id <id> --download
```

## Core parameters by subcommand

Do not invent values/ranges/enums/defaults. If unsure, check:
`node {baseDir}/scripts/kling.mjs <subcommand> --help`

### video (video generation)

Official docs: [能力地图视频](https://klingai.com/document-api/guides/capability-map/video.md) [能力地图图片](https://klingai.com/document-api/guides/capability-map/image.md). [视频Kling 4.0](https://klingai.com/document-api/api/video/4-0/video-omni.md),[文生视频 3.0](https://klingai.com/document-api/api/video/3-0-omni/text-to-video.md), [图生视频 3.0](https://klingai.com/document-api/api/video/3-0-omni/image-to-video.md), [Omni 视频](https://klingai.com/document-api/api/video/3-0-omni/video-omni.md),[主体管理](https://klingai.com/document-api/api/video/4-0/elements.md),[音色管理](https://klingai.com/document-api/api/video/4-0/voice-customization.md)

| Parameter | Description | Default |
| --- | --- | --- |
| `--prompt` | T2V/Omni required. Multi-shot format: `镜头 n, m, words;` (half-width separators; n=index 1–6, m=shot seconds ≥1 summing to `--duration`, words ≤512). Omni refs: `@image_1` `@element_1` `@video_1` (`@video_2`, …). | — |
| `--image` | Basic i2v: single first-frame image (`kling-4.0`: up to 10 keyframes, see `--image_types`; `kling-4.0-flash`: one explicit `first_frame` stays image-to-video). Omni: comma-separated list. A first frame, or `kling-4.0` frame-only keyframes, stays on image-to-video unless `--aspect_ratio` is set (then Omni; see `--aspect_ratio`). | — |
| `--image_types` | Per-image type aligned with `--image`: `first_frame` / `middle_frame` / `last_frame` / `refer_image` / empty (`refer_image` when multiple images). `middle_frame` is `kling-4.0` only. `kling-4.0` frame-only types stay on I2V unless `--aspect_ratio` is set (then Omni). `kling-4.0-flash`: only `first_frame` stays image-to-video; `last_frame` or `--image_tail` routes to Omni (no `middle_frame`). Any `refer_image` goes Omni. Other models: Omni only. Do not combine `last_frame` with `--image_tail`. | — |
| `--duration` | Seconds. `kling-4.0`: 3–30. Omitted: not sent. The server reads a duration stated in the prompt; on Omni it then uses `base_video` when present; otherwise the official default is 10. `kling-4.0-flash`: 3–20. Omitted: not sent. Same fallback as `kling-4.0`. `kling-3.0` / `kling-3.0-turbo` / `kling-3.0-omni`: 3–15. `kling-o1`: 3–10. `kling-2.6` / `kling-2.5-turbo`: `5` or `10`. | `kling-4.0` / `kling-4.0-flash`: omitted; others: 5 |
| `--model` | Path model; see **Route & model**. | route default |
| `--resolution` | `720p` / `1080p` / `4k`. `4k` only on `kling-3.0` and `kling-3.0-omni`. `kling-4.0`: `720p` / `1080p`. `kling-4.0-flash`: `720p` only. | official `1080p` (`kling-4.0`) / `720p` (others, including `kling-4.0-flash`) if omitted |
| `--aspect_ratio` | `16:9` / `9:16` / `1:1`; `kling-4.0` and `kling-4.0-flash` add `4:3` / `3:4` / `21:9` (T2V / Omni) and `adaptive` (Omni). Image-to-video has no aspect_ratio, so `--image` plus this flag (a first frame or `kling-4.0` keyframes included) routes to Omni and submits the value as given. Omni also submits an explicit value with a first frame or base video. If omitted on Omni with no first frame and not a base edit, CLI sends `16:9` (`kling-4.0` / `kling-4.0-flash`: not sent, official default `adaptive`). | T2V `16:9`; Omni `16:9` (`kling-4.0` / `kling-4.0-flash`: omitted) |
| `--audio` | `native` / `off` / `original`. 3.0 T2V/I2V and 2.6: `native\|off`. Omni 3.0: `native\|original\|off`. O1: `original\|off`. Turbo/2.5: not sent (rejected). `kling-4.0` / `kling-4.0-flash` Omni: `original` (keep input video sound) or `native` (generate new audio); T2V/I2V: do not pass `--audio`. `original` requires `--video` (reference video, not a video subject) and rejects `--voice_ids`. `kling-3.0-omni` / `kling-o1` feature video: `off` only; their base video is not `native`. 2.6 native requires `1080p`. | official `off` if omitted (not `kling-4.0` / `kling-4.0-flash`) |
| `--voice_ids` | Voice IDs (comma-separated). `contents` `type=voice` with `voice_id` and `id` (`1`, `2`, …). Prompt uses `@1`. Does **not** change route. `kling-4.0`: Omni only, max 3; `--audio original` is rejected; T2V and I2V reject this flag. `kling-4.0-flash` rejects this flag. `kling-2.6`: image-to-video only, max 2; omitted `--audio` is sent as `native` and resolution `1080p`; `--audio off` is rejected. Not on `kling-3.0` / `kling-3.0-omni` / turbo / 2.5 / o1. Get IDs from `voice --action list-presets` / `list` / `create`. | — |
| `--image_tail` | Last-frame image (`contents[].type=last_frame`). Requires `--image`. Do not combine with `--image_types last_frame`. Turbo I2V does not support last_frame. On `kling-4.0-flash`, `--image_tail` routes to Omni. | — |
| `--element_ids` | Subject IDs (comma-separated). Single `--image` + `kling-3.0` I2V: `contents` `type=element` (max 3). Otherwise Omni (`kling-4.0` / `kling-4.0-flash` I2V has no element, so it goes Omni). | — |
| `--video` | Omni reference clip(s): public http(s) URL, comma-separated. `kling-4.0` / `kling-4.0-flash`: up to 5, prompt `@video_1` `@video_2` …. `kling-3.0-omni` / `kling-o1`: one URL. At most one `base_video`. | — |
| `--video_refer_type` | `feature` → `feature_video` / `base` → `base_video`. One value, or a list aligned with `--video`. One URL and omitted type → `base`. Several URLs: list each type, or a single `feature` for every URL. | base for one URL |
| `--multi_shot` | `true` / `false`. Request field only on `kling-3.0` and `kling-3.0-omni` (`settings.multi_shot`); rejected on `kling-4.0` / `kling-4.0-flash`. Turbo: write `镜头 n, m, words;` in `--prompt`; do not pass `--multi_shot`. `false` disables 镜头-format prompts. `kling-3.0` / `kling-3.0-omni` base video edit: if omitted, CLI sends `false` (server default `true` would fail). | official `true` if omitted (3.0 / 3.0-omni; base edit → `false`) |
| `--output_dir` | Output directory. | `./output` |
| `--task_id` | Query via `GET /tasks?task_ids=`; pair with `--download`. | — |

Do not pass: `--mode`, `--sound`, `--shot_type`, `--multi_prompt`, `--keep_original_sound`, `--negative_prompt`.

Model aliases (do not pass aliases to `--model`): see **Model catalog**.

Omni `contents` image rules:
- `url` cannot be empty (URL or Base64).
- Types: `first_frame` / `middle_frame` (`kling-4.0` only) / `last_frame` / `refer_image`. Last-frame requires first-frame, except `kling-4.0` and `kling-4.0-flash`, where `last_frame` alone is allowed. `kling-3.0-omni`, `kling-o1` and `kling-4.0` support last_frame (o1 has extra limits below). `kling-4.0-flash` has no `middle_frame`.
- `kling-3.0-omni` / `kling-o1`: with `--video` max 4 images; without `--video` max 7.
- `kling-4.0` / `kling-4.0-flash`: max 10 images (with or without `--video`).
- `kling-o1`: when image count > 2, no `last_frame`. First+last: no extra `refer_image`.
- `kling-3.0-omni` / `kling-o1`: frame generation cannot combine with `--video_refer_type base`.
- `kling-o1` + `feature_video`: first_frame only, no last_frame.
- `kling-o1` first_frame only (no `refer_image`, no `--video`): `--duration` only `5` or `10`.

Omni `contents` element rules:
- `element_id` cannot be empty; `id` is `element_1`…
- `kling-3.0-omni` / `kling-o1`: frame generation supports up to 3 subjects.
- First+last frame with `kling-o1`: subjects unsupported.
- `kling-3.0-omni` / `kling-o1`: with `--video`: `image_count + element_count <= 4`; otherwise `<= 7`.
- `kling-4.0`: max 7 subjects. Video-character subjects are at most 3, and those subjects plus reference videos total at most 5. An element id does not say which kind of subject it is, so the CLI does not apply that combined cap; the server does. `image_count + video_count + element_count + voice_count <= 15`.
- `kling-4.0-flash`: max 7 subjects. Video-character subjects are at most 3, and those subjects plus reference videos total at most 5. An element id does not say which kind of subject it is, so the CLI does not apply that combined cap; the server does. `image_count + video_count + element_count <= 15`. No `--voice_ids`.

Omni / 4.0 `contents` voice rules:
- Item: `type=voice`, `voice_id`, `id`=`1` (`2`, `3` …); prompt `@1`. Model limits, route, and audio side effects: see `--voice_ids`.

Omni `contents` video rules:
- Counts and type mapping: see `--video` / `--video_refer_type`. On `kling-4.0` / `kling-4.0-flash`, at most one `base_video`; any other clip is `feature_video`. Video-character subjects plus reference videos: see element rules above.
- `kling-3.0-omni` / `kling-o1` `feature_video`: `--audio` must be `off`; do not set `--multi_shot false`.
- `kling-3.0-omni` / `kling-o1` `base_video`: no first/last frame. No `--multi_shot true`; if `--multi_shot` omitted, CLI sends `false`; `--audio` cannot be `native`.

Compact examples:

```bash
# explicit frame marking by intent
node {baseDir}/scripts/kling.mjs video --model kling-3.0-omni --image a.jpg,b.jpg,c.jpg --image_types first_frame,refer_image,last_frame --prompt "..."

# with reference video: image count <= 4
node {baseDir}/scripts/kling.mjs video --model kling-3.0-omni --video "https://..." --video_refer_type feature --audio off --image a.jpg,b.jpg --prompt "..."

# kling-4.0 multi-keyframe I2V (frame-only types, max 10 images incl. --image_tail)
node {baseDir}/scripts/kling.mjs video --model kling-4.0 --image a.jpg,b.jpg,c.jpg --image_types first_frame,middle_frame,middle_frame --image_tail d.jpg --prompt "..."

# kling-4.0 Omni (refer image + subject); no --multi_shot
node {baseDir}/scripts/kling.mjs video --model kling-4.0 --image a.jpg --image_types refer_image --element_ids 123456 --prompt "@element_1 in the style of @image_1"

# kling-4.0 voice is Omni only (prompt uses @1)
node {baseDir}/scripts/kling.mjs video --model kling-4.0 --image a.jpg --image_types refer_image --prompt "A woman says hello in the voice of @1" --voice_ids 850087542757535834

# kling-4.0-flash: one first frame stays image-to-video, 3–20s, 720p; no --audio / --multi_shot
node {baseDir}/scripts/kling.mjs video --model kling-4.0-flash --image a.jpg --duration 15 --prompt "Her hair moves in the wind"

# kling-2.6 voice is image-to-video only (id is 1, prompt uses @1)
node {baseDir}/scripts/kling.mjs video --model kling-2.6 --image a.jpg --prompt "@1 whispers softly" --voice_ids 829826751244537879
```

If the user asks for a voice / 音色 without naming a model, ask which of `kling-4.0` Omni or `kling-2.6` image-to-video to use. Do not invent a `voice_id`. List official voices with `voice --action list-presets`, or create one with `voice --action create` (public `--voice_url` or `--video_id` only).

### image (image generation)

| Parameter | Description | Default |
| --- | --- | --- |
| `--model` | Prefer `kling-4.0`. See **Route & model**. | `kling-4.0` |
| `--prompt` | Image prompt (required). `kling-4.0`: `@image_1` / `@element_1`. `kling-v3-omni` / `kling-image-o1`: `<<<image_1>>>` / `<<<element_1>>>`. | — |
| `--image` | One image, or a comma-separated list on `kling-4.0` and image Omni. | — |
| `--resolution` | `kling-4.0`: `2k` / `4k` / `8k`. `1k`: `kling-v3` or `kling-v2-1`. `--page`: `1k` / `2k`. | `2k`; `--page`: `1k` |
| `--aspect_ratio` | `kling-4.0`: `16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `3:2` / `2:3` / `21:9` / `auto` (with or without `--image`). Image Omni `auto` needs `--image`. | `auto` |
| `--n` | Result count 1–9 when `result_type=single`. Not used for `kling-4.0` series. | 1 |
| `--negative_prompt` | `kling-v3` / `kling-v2-1` text-to-image only. Not with `--image`. Not on `kling-4.0`. | — |
| `--result_type` | `single` / `series`. `kling-4.0` series allows text or image input. Image Omni series needs `--image`. | single |
| `--series_amount` | `kling-4.0`: 2–10 or `auto`. Image Omni series: 2–9 or `auto`, and needs `--image`. | 4 |
| `--element_ids` | Subject IDs. `kling-4.0`: image subjects only; images + subjects ≤ 10. `kling-v2-1` unsupported. Not on `--page`. | — |
| `--page` | Long-page route. `ecommerce`: 电商详情页, 1–3 `refer_image`. `webpage`: 网页设计, text or `style_refer_image` (0–1) + `subject_refer_image` (0–1). | — |
| `--image_types` | Per-image type aligned with `--image` on `--page`: `refer_image` (`ecommerce` only, 1–3; default on `ecommerce`) / `style_refer_image` (`webpage` only, 0–1) / `subject_refer_image` (`webpage` only, 0–1). `webpage` with `--image` requires explicit `--image_types`; cross-use is rejected locally. | `ecommerce`: `refer_image` |
| `--length` | `ecommerce` only: `short` / `medium` / `long`. | `medium` |
| `--output_dir` | Output directory. | `./output` |
| `--task_id` | Query task id; pair with `--download`. | — |

Notes:
- `n` and `series_amount` apply to different modes. `--series_amount` without `--result_type` selects series. `--result_type single` cannot be combined with `--series_amount`.
- `kling-4.0` series does not require `--image`. Image Omni series does.
- `--negative_prompt` is `kling-v3` / `kling-v2-1` text-to-image only.
- `kling-4.0` omitted aspect is `auto`, with or without `--image`. Image Omni `auto` needs `--image`; text-to-image Omni uses `16:9`.
- `--page` is only for 电商详情页 (`ecommerce`) or 网页设计 (`webpage`). `ecommerce` uses `refer_image` only (1–3 images; `--image_types` defaults to `refer_image`). `webpage` reference images use `--image_types` `style_refer_image` (0–1, visual/layout style) and/or `subject_refer_image` (0–1, subject element) only — `refer_image` or untyped `--image` on `webpage`, and `style_refer_image` / `subject_refer_image` on `ecommerce`, are rejected locally. Resolution on that route is `1k` / `2k` (default `1k`). Prompt uses `@image_1` (`@image_2`, …) in `--image` order. No subjects, aspect, count, or series.

Omni refs rules (image):
- `image` cannot be empty (URL or Base64).
- `element_id` cannot be empty.
- `image_count + element_count <= 10`.
- `kling-4.0`: same cap. Prompt uses `@image_1` / `@element_1` in flag order. Subjects must be image subjects.

### element (subject management)

Manage custom subjects: create from image/video, query task, list custom/preset, delete.
Use `element_id` in `video`/`image` with `--element_ids` for reusable subject consistency.

| Parameter | Description |
| --- | --- |
| `--action create` | Create subject; requires `--name` (<=20), `--description` (<=100), `--ref_type` |
| `--ref_type` | `image_refer` (requires `--frontal_image` and `--refer_images`) / `video_refer` (requires `--video`) |
| `--frontal_image` | Front reference image (`image_refer`) |
| `--refer_images` | Other reference images (comma-separated, **required** 1–3). Official API: must differ from the frontal image. |
| `--video` | Reference video (`video_refer`) |
| `--voice_id` | Optional voice bind (image_refer: 人物/类人形象) |
| `--action query --task_id <id>` | Query creation task |
| `--action list` | List custom subjects |
| `--action list-presets` | List preset subjects |
| `--action delete --element_id <id>` | Delete subject |

If the user only provides a frontal image: **ask** whether to (1) add 1–3 other-angle images, or (2) explicitly reuse the frontal file as `--refer_images`. Do not submit without `--refer_images`. The CLI does not silently copy `--frontal_image` into `refer_images`.

### voice (voice management)

Model-independent library. Official paths are the same on the 2.6 and 3.0 Omni voice pages (`/v1/general/custom-voices`). Use the returned `voice_id` in `video --voice_ids` (`kling-4.0` Omni or `kling-2.6` image-to-video).

| Parameter | Description |
| --- | --- |
| `--action create` | Create a custom voice. Requires `--name` (≤20). Exactly one of `--voice_url` or `--video_id`. |
| `--voice_url` | Public http(s) URL (`.mp3` / `.wav` / `.mp4` / `.mov`, one speaker, 5–30 s). Local paths and base64 are rejected. |
| `--video_id` | Existing work ID. Official limit: 2.6 with sound on, avatar, or lip-sync. |
| `--action query --task_id <id>` | Query the creation task; read `task_result.voices[].voice_id`. |
| `--action list` | List custom voices |
| `--action list-presets` | List official preset voices |
| `--action delete --voice_id <id>` | Delete a custom voice |

### account (resource & quota inquiry, optional credential setup)

| Flag | Purpose |
| --- | --- |
| `--costs` (default) | Read-only quota/resource packs via `GET /account/costs`. |
| `--bind-url` | Device bind with polling; prints URL for manual open; optional `--force`. |
| `--import-env` | Read `KLING_API_KEY` and persist. |
| `--import-credentials` | Persist `--api_key`. |
| `--configure` | Interactive API Key input and save credentials. |

All bind/account files persist under storage root (`~/.config/kling` by default, or `KLING_STORAGE_ROOT`).

`--costs` query params:

| Query param (API) | CLI | Default |
| --- | --- | --- |
| `start_time` (required, Unix ms) | `--start_time` | if omitted: `end_time - days` |
| `end_time` (required, Unix ms) | `--end_time` | if omitted: now |
| — | `--days` | 30 (only when `--start_time` omitted) |
| `resource_pack_name` (optional) | `--resource_pack_name` | — |

Run `node {baseDir}/scripts/kling.mjs account --help` for details.
Run `node {baseDir}/scripts/kling.mjs video --help`, `image --help`, `element --help`, or `voice --help` for full params.

## Route & model (`scripts/kling.mjs` flags select the default model_name)

Agents call `node {baseDir}/scripts/kling.mjs <video|image|element|voice|account>` with flags.
`--model` selects the official path/model. Video encodes model in the URL (`/text-to-video/kling-4.0`); image still sends `model_name`. Must be exact canonical spelling.
If `--model` is omitted, route defaults apply.
CLI guardrails reject incompatible model/route and invalid `audio` / frame combinations before submit.

### Routing decision tree (must follow)

1. Choose subcommand from intent: `video` / `image` / `element` / `voice` / `account`.
2. Determine route triggers:
   - any Omni trigger -> Omni route
   - otherwise -> basic route
3. Validate model-route compatibility:
   - Omni route accepts only Omni-capable canonical models
   - basic route rejects Omni-only models
4. Validate strict parameter combos (`audio`, `multi_shot`, frame rules, ref limits).
5. If uncertain, run `--help` or ask user; never guess-submit.

### Video (`video` subcommand)

Omni routing triggers (any of these -> `/omni-video/{model}`):
- `--video`
- comma in `--image` (exception: `kling-4.0` frame-only `--image_types` stays I2V when `--aspect_ratio` is omitted)
- `--image` + `--aspect_ratio` (a first frame or `kling-4.0` frame-only keyframes included; see `--aspect_ratio`)
- `--element_ids` without a single I2V first-frame (or with turbo/2.6/2.5/`kling-4.0`/`kling-4.0-flash`)
- `kling-4.0` / `kling-4.0-flash` + `--image_types` containing `refer_image`
- `kling-4.0-flash` + last frame (`--image_tail`, or `--image_types` containing `last_frame`, including first and last). Only an explicit first frame stays image-to-video. Do not reject `last_frame`
- explicit `--model kling-3.0-omni` or `--model kling-o1` (Omni-only names; `kling-4.0` / `kling-4.0-flash` are **not** Omni triggers by themselves)

Otherwise:
- T2V: no `--image` → `POST /text-to-video/{model}`
- I2V: single `--image` (optional `--image_tail`, except `kling-4.0-flash` where `--image_tail` routes to Omni; optional `--element_ids` on `kling-3.0` max 3) → `POST /image-to-video/{model}`
- I2V (`kling-4.0` only): up to 10 keyframes, every `--image_types` entry is `first_frame` / `middle_frame` / `last_frame` (plus optional `--image_tail`) → `POST /image-to-video/kling-4.0`

#### Kling 4.0 intent → route

`kling-4.0` and `kling-4.0-flash` each have three endpoints under one name. Pass that `--model`; pick flags from intent, and the CLI routes. The table uses `kling-4.0`; `kling-4.0-flash` uses the same flags with `kling-4.0-flash` in the path, except where a row says otherwise.

| User intent (with 4.0) | Flags | Endpoint |
| --- | --- | --- |
| Text only, no media / subject | `--prompt` (`--aspect_ratio` optional) | `/text-to-video/kling-4.0` |
| Animate one image as first frame | `--image x.jpg` (`--image_tail` optional on `kling-4.0`) | `/image-to-video/kling-4.0`. With `--aspect_ratio`: `/omni-video/kling-4.0`. `kling-4.0-flash` only-first-frame: `/image-to-video/kling-4.0-flash`. Its `--image_tail` or `last_frame`: `/omni-video/kling-4.0-flash` |
| Keyframes: first / middle / last frames in order (多关键帧) | `--image a,b,c --image_types first_frame,middle_frame,last_frame` | `/image-to-video/kling-4.0` only. With `--aspect_ratio`: `/omni-video/kling-4.0`. Not on `kling-4.0-flash` |
| Style / scene / character reference images (not frames) | `--image a,b` (types empty or `refer_image`) | `/omni-video/kling-4.0` |
| Use subject(s) | `--element_ids ...` (with or without images) | `/omni-video/kling-4.0` |
| Reference video (motion / style) | `--video URL --video_refer_type feature`. Up to 5 URLs on 4.0 and 4.0 Flash: `--video u1,u2 --video_refer_type feature` | `/omni-video/kling-4.0` |
| Edit a video | `--video URL --video_refer_type base` | `/omni-video/kling-4.0` |
| Mixed: frames + refer images | `--image_types` mixing frames and `refer_image` | `/omni-video/kling-4.0` |
| Use voice / 音色 | `--voice_ids ...` together with Omni flags (reference image, subject, or video) | `/omni-video/kling-4.0`. Text-only and image-to-video reject `--voice_ids`. `kling-4.0-flash` rejects `--voice_ids`. Voice alone does not switch route. |

Rules for 4.0 / 4.0 Flash:
- If it is unclear whether images are **frames** (where the video starts / passes / ends) or **references** (style, scene, character), ask the user before submitting.
- Text-only always goes T2V (there is no "Omni without references") and rejects `--voice_ids`.
- Not accepted on either model: `--multi_shot`, `4k`, `--audio off`. T2V / I2V: do not pass `--audio`. Omni `--audio`: `original` (keep input-video sound; requires `--video`, not a video subject; no `--voice_ids`) or `native` (generate new audio). Voice: `--voice_ids` on `kling-4.0` Omni only.
- `kling-4.0`: duration 3–30 (omitted: see `--duration`). Resolution `720p` / `1080p` (official default `1080p`).
- `kling-4.0-flash`: duration 3–20 (omitted: see `--duration`). Resolution `720p` only. Only an explicit first frame stays image-to-video. An explicit last frame, or first and last frames, routes to Omni and is not rejected. No `middle_frame`. Up to 5 reference videos, at most one `base_video`. Omni aspect official default `adaptive` (omitted, not sent). No `--voice_ids`.

`--multi_shot` does not force Omni; it still follows the routing triggers above.

| Video routing (CLI) | Default if `--model` omitted | Allowed `--model` |
| --- | --- | --- |
| T2V / I2V | `kling-4.0` | `kling-3.0`, `kling-3.0-turbo`, `kling-2.6`, `kling-2.5-turbo`, `kling-4.0`, `kling-4.0-flash` |
| Omni | `kling-4.0` | `kling-4.0` (default), `kling-3.0-omni`, `kling-o1`, `kling-4.0-flash` |

### Image (`image` subcommand)

Prefer `kling-4.0` for image generation: text, reference images, subjects, `2k` / `4k` / `8k`, and series. Omit `--model`.

`--page` switches to the long-page route only for 电商详情页 (`ecommerce`) or 网页设计 (`webpage`). Other image tasks stay on the rows below.

Use another image model only for a capability `kling-4.0` does not have, or when the user names that model:
- `1k` or `--negative_prompt`: `kling-v3` (or named `kling-v2-1`)
- named `kling-image-o1`: `1k` / `2k`, no `4k`, no series

| Image routing (CLI) | Default if `--model` omitted | Allowed `--model` |
| --- | --- | --- |
| `kling-4.0` (text, images, subjects, 2k/4k/8k, series) | `kling-4.0` | `kling-4.0` |
| 电商详情页 `--page ecommerce`；网页设计 `--page webpage` | `kling-4.0` | `kling-4.0` |
| `1k` or `--negative_prompt` | `kling-v3` | `kling-v3`, `kling-v2-1` |
| named image Omni | the named model | `kling-v3-omni`, `kling-image-o1` |

### Model catalog (by name)

Common aliases (understanding only; do not pass aliases to `--model`):
- `omni3`, `omni v3`, `视频O3`, `video o3`, `O3`, `o3` -> `kling-3.0-omni` (video) / `kling-v3-omni` (image)
- `o1`, `omni1` -> `kling-o1` (video) or `kling-image-o1` (image)
- `kling-4.0-omni`, `4.0 全能参考`, `4.0 Omni`, `可灵 4.0` -> `kling-4.0` (video)
- `图片4.0`, `image 4.0`, `kling-image-4.0`, `image-4.0` -> `kling-4.0` (image)
- `kling-4.0-flash-omni`, `4.0 Flash`, `可灵 4.0 Flash` -> `kling-4.0-flash` (video)

`--model` input rule: pass only canonical names from this table.

| Model | Valid on | Notes |
| --- | --- | --- |
| `kling-4.0` | T2V / I2V / Omni video; `image` | Video: one name, three endpoints (see **Kling 4.0 intent → route**). Duration 3–30; 720p/1080p; no `--multi_shot` / 4k. Omni `--audio`: `original` or `native`; T2V / I2V do not pass `--audio`. I2V: up to 10 keyframes, no subjects. Omni: max 10 images, 7 subjects, 5 reference videos (one `base_video`); aspect adds `4:3`/`3:4`/`21:9` (T2V / Omni) and `adaptive` (Omni). Voice: Omni `--voice_ids` only (max 3). Image: preferred image model. Omit `--model` on `image`. Resolution `2k`/`4k`/`8k` (default `2k`). Aspect adds `4:3`/`3:4`/`3:2`/`2:3`/`21:9`/`auto` (default `auto`). `single` n 1–9; `series` 2–10 or `auto` (text or image). Up to 10 images and image subjects. Prompt `@image_1` / `@element_1`. No `1k`, no `--negative_prompt`. Long page, only for 电商详情页 or 网页设计: `--page ecommerce` (1–3 `refer_image`, `--length` `short`/`medium`/`long`) or `--page webpage` (text, or 0–1 `style_refer_image` + 0–1 `subject_refer_image` via `--image_types`). Resolution `1k`/`2k` (default `1k`). |
| `kling-4.0-flash` | T2V / I2V / Omni video | One name, three endpoints (same flag routing as `kling-4.0`). Duration 3–20 (omitted is not sent; official default 10); 720p only; no `--multi_shot` / 4k / `--voice_ids`. Omni `--audio`: `original` or `native`; T2V / I2V do not pass `--audio`. I2V: one explicit `first_frame`, no subjects, no `middle_frame`. `last_frame` / `--image_tail` routes to Omni. Omni: max 10 images, 7 subjects, 5 reference videos (one `base_video`); aspect adds `4:3`/`3:4`/`21:9` (T2V / Omni) and `adaptive` (Omni). |
| `kling-3.0` | T2V / I2V | Video basic. Resolution 720p/1080p/4k; audio native/off; multi_shot. I2V contents may include `element` (max 3). No `--voice_ids`. |
| `kling-3.0-turbo` | T2V / I2V | No audio / `settings.multi_shot`; I2V first_frame only (no last_frame). Multi-shot via prompt `镜头 n, m, words;` only. |
| `kling-2.6` | T2V / I2V | Duration 5 or 10; audio native/off (native needs 1080p). Last-frame: 1080p silent. Voice: I2V `--voice_ids` max 2 (sends `audio=native` and `1080p`). |
| `kling-2.5-turbo` | T2V / I2V | Duration 5 or 10; no audio field. Last-frame: 1080p only. |
| `kling-3.0-omni` | Omni video | Omni video. audio native/original/off (`original` needs `--video`); 4k; first+last frame; feature/base video. No `--voice_ids`. |
| `kling-o1` | Omni video | Duration 3–10; audio original/off; no 4k; no multi_shot field. First-frame-only: 5 or 10s. Feature video: no last_frame. First+last: no extra refs/subjects. |
| `kling-v3` | Basic image | `1k` / `2k` and `--negative_prompt`. Supports subjects. |
| `kling-v2-1` | Basic image | `1k` / `2k`. No subjects. |
| `kling-v3-omni` | Omni image | When the user names 图片O3. `1k`/`2k`/`4k`; series needs `--image`. Text-to-image: no `aspect_ratio=auto` (uses `16:9`). |
| `kling-image-o1` | Omni image | When the user names image O1. `1k`/`2k`. No `4k`, no series. Text-to-image uses `16:9`; `auto` only with `--image`. |

Principle:
- Set task flags first (`--image`, `--element_ids`, `--video`, `--multi_shot`, ...).
- Omit `--model` to use route defaults.
- If `--model` is explicit, it must match route implied by flags.

## When to use Omni; element vs image reference

Which route: follow **Route & model** triggers.
Prefer video Omni for reference-video edit or mixed video prompts (`@image_1` / `@element_1` / `@video_1`). Image generation prefers `kling-4.0` (`@image_1` / `@element_1`, including text series).
Single-image + subject on `kling-3.0` I2V stays on the video basic route. Image subjects use `image` and prefer `kling-4.0`.

Prefer plain image reference for simple tasks.
Create element first only when user explicitly wants reusable subject consistency across outputs.

## Prompt template syntax (video / image Omni)

In Omni video, pass media/subjects by flags; reference in `--prompt` with official `@` ids (`contents[].id`):
- `@image_1` -> first `--image` (`@image_2`, ...)
- `@element_1` -> first `--element_ids` (`@element_2`, ...)
- `@video_1` -> first `--video` (`@video_2`, …)
- `kling-4.0` I2V keyframes also get ids `image_1`, `image_2`, ... in `--image` order (`--image_tail` is the last one).
- `@1` -> first `--voice_ids` (`@2`, `@3` for the rest) on `kling-4.0` Omni and `kling-2.6` image-to-video

Image `kling-4.0` uses `@image_1` / `@element_1`. `kling-v3-omni` and `kling-image-o1` use `<<<image_1>>>` / `<<<element_1>>>`. `kling-v3` uses subjects without `<<<>>>`.

## Notes

- Timing: video ~1–5+ min; image ~20–60 s; subject creation ~30 s–2 min.
- Retention: platform may remove assets after ~30 days; save outputs locally.
- Server checks prompt length and media size; the CLI does not. Users are strongly advised to validate these locally.

| Model | Prompt | Image | Reference video |
| --- | --- | --- | --- |
| `kling-4.0` | English ≤26000, other languages ≤11000 (mixed: English/26000 + other/11000 ≤ 1) | ≤30MB, side ≥300px, aspect 2:5–5:2 | ≤300MB, side 700–4553px, area ≤8294400, aspect 2:5–5:2, 3–30s each and in total (includes video-character subjects), 24–60fps in (24fps out) |
| image `kling-4.0` | English ≤50000, other languages ≤21000 (mixed: English/50000 + other/21000 ≤ 1) | ≤30MB, side ≥300px, aspect 2:5–5:2, jpg/jpeg/png | — |
| image `--page` | English ≤166000, other languages ≤71000 (mixed: English/166000 + other/71000 ≤ 1) | ≤30MB, side ≥300px, aspect 2:5–5:2, jpg/jpeg/png (`ecommerce`: 1–3 `refer_image`; `webpage`: 0–1 `style_refer_image` + 0–1 `subject_refer_image`) | — |
| `kling-4.0-flash` | English ≤26000, other languages ≤11000 (mixed: English/26000 + other/11000 ≤ 1) | ≤30MB, side ≥300px, aspect 2:5–5:2 | ≤300MB, side 700–4553px, area ≤8294400, aspect 2:5–5:2, 3–20s each and in total (includes video-character subjects; those subjects 3–8s), 24–60fps in (24fps out) |
| `kling-3.0` | ≤3072, suggest ≤2500 | ≤50MB, side ≥300px, aspect 1:2.5–2.5:1 | — |
| `kling-3.0-omni` | ≤3072, suggest ≤2500 | ≤50MB, side ≥300px, aspect 1:2.5–2.5:1 | ≤200MB, side 700–4553px, area ≤8294400, aspect 0.4–2, 3–15.5s, 24–60fps in (24fps out) |
| `kling-2.6` | ≤2500 | ≤50MB, side ≥300px, aspect 1:2.5–2.5:1 | — |

## Reference

- Official docs index: https://klingai.com/document-api/llms.txt
- Official docs home: https://klingai.com/document-api/
- API endpoint quick map in this package: `reference.md`
