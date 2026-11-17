---
name: makaron
description: Use Makaron CLI to generate AI images, videos, music, and motion designs. Trigger when user needs creative media production — photo editing, video generation, video editing, music composition, or design creation. Requires `npx makaron-cli` and MAKARON_API_KEY env var.
---

# Makaron CLI — Agent Integration Skill

> **makaron.app** is for humans. **makaron-cli** is for AI agents.

Makaron is a multimodal AI creative agent. You talk to it via `makaron chat`, and it produces images, videos, music, and animated designs — all saved to a persistent project.

## Setup

### Get your API key

**Option A: Human login**
1. Go to [makaron.app](https://makaron.app) and log in
2. Open the menu (top-right) → **Get API Key**
3. Copy your `mk_live_...` key

**Option B: Self-Registration (no human required)**
```bash
# Step 1: Get challenge
npx makaron-cli register --json
# → { "challenge_id": "...", "challenge": "...", "expected_format": "numeric, round to 2 decimal places" }

# Step 2: Solve and verify
npx makaron-cli register --verify --challenge-id <id> --answer 34.5
# → Key saved to ~/.makaron/auth.json
# → { "api_key": "mk_live_...", "credits": N, "claim_url": "..." }

# (Optional) Let a human claim this account
npx makaron-cli claim
# → { "claim_url": "..." } — share with human to link key to their account (valid 7 days)
```

Discovery endpoint: `GET https://www.makaron.app/api/agent/register` — returns full registration flow + CLI usage as JSON.

After self-registration the key is saved locally — no need to export `MAKARON_API_KEY`.

```bash
export MAKARON_API_KEY=mk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Verify: `npx makaron-cli list` should show projects.

## Core Workflow

```bash
# One-shot: create project + upload image + submit prompt — all in one command
RUN_ID=$(npx makaron-cli chat --project auto --image photo.jpg -b "make it cinematic and create a 5s video")

# Wait for the final customer-ready result
npx makaron-cli responses get $RUN_ID --wait --json
```

Or with an existing project:
```bash
RUN_ID=$(npx makaron-cli chat --project $PROJECT_ID -b "make a 5s video")
npx makaron-cli responses get $RUN_ID --wait --json
```

## Primary: `chat` (Agent-driven creative work)

Use `chat` for all creative tasks. Makaron Agent decides how to execute — it can edit images, generate videos, compose music, and create designs in a single conversation.

```bash
npx makaron-cli chat --help
```

### Submit a request

```bash
# With existing project
npx makaron-cli chat --project <id> --json -b "<prompt>"

# Auto-create project (with or without images)
npx makaron-cli chat --project auto --image photo.jpg --json -b "make it cinematic"
npx makaron-cli chat --project auto --image img1.jpg --image img2.jpg --json -b "combine these"
```

Returns immediately:
```json
{"runId": "xxx", "projectId": "...", "projectUrl": "https://www.makaron.app/projects/...", "status": "running"}
```

### Common workflows

| What you want | Example |
|--------------|---------|
| Edit an image | `npx makaron-cli chat --project <id> --image photo.jpg "remove the person in the background"` |
| Generate an image | `npx makaron-cli chat --project auto "generate a cinematic poster of a rainy Tokyo alley"` |
| Make a video from the current project | `npx makaron-cli chat --project <id> "make this into a 5 second cinematic video"` |
| Fix one moment in a video from a screenshot | `npx makaron-cli chat --project <id> --image screenshot.png "@4 this frame should be Paris; only fix this moment"` |
| Cut or assemble video | `npx makaron-cli chat --project <id> --video clip.mp4 "cut out the dead air and keep the best 20 seconds"` |
| Add music | `npx makaron-cli chat --project <id> "add calm piano background music"` |
| Beat-sync video from audio | `npx makaron-cli chat --project auto --audio beat.mp3 --video-model seedance-fast --video-resolution 480p "make a beat-synced video"` |
| Create motion design | `npx makaron-cli chat --project <id> "make an animated Instagram story with this image"` |

### Marketplace skills

Use marketplace skills when the user asks for a named Makaron effect, template, or skill such as "Football Captain", "足球队长", "World Cup MVP", or a marketplace UUID.

External users only need `MAKARON_API_KEY`; no admin permissions are required for listing, searching, showing, installing, or using marketplace skills.

```bash
# Browse public marketplace skills
npx makaron-cli skills list
npx makaron-cli skills search "football"
npx makaron-cli skills search "足球"
npx makaron-cli skills show <marketplace-id-or-label>

# Install a marketplace skill into the API key owner's workspace
npx makaron-cli skills install <marketplace-id-or-label>

# Use a marketplace skill. If the skill is not installed yet, chat auto-installs it,
# then injects the installed skill name into the agent run.
npx makaron-cli chat --project auto \
  --image selfie.jpg \
  --skill <marketplace-id-or-label> \
  -b "make this with the selected skill"
```

`--skill` accepts an installed skill name, a marketplace UUID, or a unique marketplace label. If a marketplace skill is matched, the CLI installs or reuses it and sends `[Active skill: <installed-skill-name>]` to Makaron Agent. Do not call admin skill commands for ordinary users. There is intentionally no user-facing CLI delete command for marketplace skills.

### With additional images (existing project)

```bash
npx makaron-cli chat --project <id> --image ref1.jpg --image ref2.jpg -b "use these as style reference"
```

### Inspect existing timeline media

Before starting a follow-up run on an existing project, list the current timeline media so you know what assets are available and which `<<<media_N>>>` references to use:

```bash
npx makaron-cli project media <projectId> --json
```

This is project-scoped. `responses get <runId> --pick output` only returns artifacts from one run; `project media` returns the whole project timeline: original uploads, references, generated images, video snapshots, and editable compositions.

### With video input (edit, compose, extend)

```bash
# Upload a video and transform it — Agent understands video content natively
npx makaron-cli chat --project auto --video selfie.mp4 -b "put Iron Man armor on me"

# Combine a person's photo with a video scene
npx makaron-cli chat --project <id> --video party.mp4 --image kid.jpg -b "make this kid join the party"

# Multiple videos — compose or splice
npx makaron-cli chat --project <id> --video clip1.mp4 --video clip2.mp4 -b "combine into one seamless video"

# Video URL (public, downloadable)
npx makaron-cli chat --project auto --video https://example.com/dance.mp4 -b "extend this to 15 seconds"
```

Supported formats: MP4, MOV, WebM. CLI local video uploads support max 50MB, max 120s with 1s metadata tolerance, and <=1080p / 2,086,876 frame pixels. The frontend can transcode larger videos before upload; the CLI uploads directly to Storage and rejects videos above those limits. Videos are uploaded to the project timeline. The Agent can analyze scenes, edit content, compose multiple clips, extend duration, and add effects — all via natural language. Seedance video-reference editing is still limited to ~15s provider references, so longer uploaded videos should be split/prepared by the agent before model submission; Kling remains the base/direct edit path.

Use `chat --project <id|auto> --video ...` for any project/timeline video work. Direct video commands are standalone raw-tool calls.

### With reference audio (MP3/WAV)

Attach a short song, beat, or voice recording when the video should follow audio pacing:

```bash
npx makaron-cli chat --project auto \
  --audio beat.mp3 \
  --video-model seedance-fast \
  --video-resolution 480p \
  -b "make a 15s beat-synced video"
```

`--audio` accepts repeatable local files or public URLs. Local MP3/WAV files must be 2-15s and <=15MB; reference audio currently works with Seedance video generation.

### Fix one video moment from a screenshot

When a video is mostly good but one moment needs a local fix, attach a screenshot of the problem frame and describe the correction in normal language:

```bash
npx makaron-cli chat --project <id> \
  --image screenshot.png \
  "@4 this frame should be Paris, keep the same style and only fix this moment"
```

Makaron can locate the screenshot in the video, regenerate only the nearby segment, and then print a `Next steps` command when the new clip should be stitched back into the full MP4.

### Check status (single query)

```bash
npx makaron-cli responses get <runId> --json
```

### Advanced: stream incremental events

```bash
npx makaron-cli responses watch <runId> --jsonl
```

Outputs one JSON per line as artifacts appear:
```
{"event":"output.added","item":{"id":"out_1","type":"image","status":"completed","url":"https://..."}}
{"event":"output.added","item":{"id":"out_2","type":"video","status":"rendering","task_id":"xxx"}}
{"event":"output.updated","item":{"id":"out_2","type":"video","status":"completed","url":"https://..."}}
{"event":"done","status":"completed"}
```

### Extract specific results

```bash
npx makaron-cli responses get <runId> --pick first_image_url
npx makaron-cli responses get <runId> --pick image_urls        # all images (JSON array)
npx makaron-cli responses get <runId> --pick first_video_url
npx makaron-cli responses get <runId> --pick video_urls        # all videos
npx makaron-cli responses get <runId> --pick project_url
npx makaron-cli responses get <runId> --pick text              # agent's text reply
npx makaron-cli responses get <runId> --pick output            # full output array
npx makaron-cli responses get <runId> --pick status
```

## Fallback: Direct tool calls (no project context)

Use these only when `chat` is unavailable or you need raw model access without project/conversation context.

### `edit` — One-shot image editing

```bash
# Edit an existing image
npx makaron-cli edit --image photo.jpg "add cinematic warm lighting"

# Text-to-image (no input)
npx makaron-cli edit "a cyberpunk cityscape at night"

# With model/reference
npx makaron-cli edit --image photo.jpg --ref style.jpg "match this style"

# Output to file
npx makaron-cli edit --image photo.jpg --out result.jpg "make it dramatic"
```

Options: `--image`, `--model gemini|gemini-lite|qwen|openai|pony|wai`, `--ref <file>` (up to 3), `--aspect <ratio>`, `--out <path>`

### `video` — Standalone video tools (no project timeline)

```bash
# 1. Write script from images
npx makaron-cli video script --image img1.jpg "cinematic story"

# 2. Analyze a video (standalone, no timeline write)
npx makaron-cli analyze --video input.mp4 "describe the key actions and pacing"

# 3a. Submit image-to-video rendering (images must be public URLs from step 1 or uploaded)
npx makaron-cli video create --script "Shot 1 (5s): <<<image_1>>> ..." --image https://...jpg --duration 5 --model kling
npx makaron-cli video create --script "Shot 1 (15s): <<<image_1>>> and <<<image_2>>> build a neon one-person studio" --image https://...jpg --image https://...webp --duration 15 --model seedance-mini --video-resolution 480p --aspect 9:16

# 3b. Edit a video from a local file or public URL
npx makaron-cli video create --script "make it funny" --video input.mp4 --duration 5 --model seedance-fast
npx makaron-cli video create --script "make it warmer and cinematic" --video https://example.com/input.mp4 --duration 5 --model seedance --video-resolution 1080p

# 4. Check status
npx makaron-cli video status <taskId>
```

`video create` returns a provider task id and does not create or update a Makaron project timeline. For project/timeline video editing, use:

```bash
npx makaron-cli chat --project <id|auto> --video input.mp4 -b "make it funny"
```

Options for `video create`: `--script "..."`, `--script-file <path>`, `--image <url>` (repeatable, up to 7), `--video <file|url>`, `--duration <seconds>`, `--aspect 9:16|16:9|1:1`, `--model seedance-fast|seedance-mini|seedance|kling|grok|google-omni`, `--video-resolution auto|480p|720p|1080p|4k`. Default model is `seedance-fast`. SeeDance accepts integer output duration 4-15s (default 5s); `seedance-mini` supports 480p/720p and is best for cheaper drafts/multi-size tests; Kling supports 5-15s; Grok 1.5 supports 1-15s single-image-to-video only; Gemini Omni supports 3-10s fast 720p image/video generation and editing with native generated audio, including up to 6 image references when no video reference is provided. For `--model grok`, forced `--aspect` is ignored to avoid xAI stretching the source image; pad/create the image at the target shape first or use another model.

Video edit model behavior: `--model kling --video` uses Kling base/direct edit internally; `--model seedance-fast --video`, `--model seedance-mini --video`, or `--model seedance --video` uses the SeeDance video-reference path and requires target <=15s, <=50MB, width/height 300-6000px, aspect ratio 0.4-2.5, and frame pixels 409,600-2,086,876. `--model google-omni --video` uses Gemini Omni direct video editing and accepts one reference video in Makaron. Output duration is clamped to 3-10s. Grok does not support video references.

### `music` — Music generation

```bash
npx makaron-cli music create "gentle piano, warm strings, cinematic"
npx makaron-cli music create --vocals --style "lo-fi" "rainy day vibes"
npx makaron-cli music status <taskId>
```

Options: `--vocals` (include vocals), `--style "genre"`

## Response Schema

```typescript
type MakaronRunResponse = {
  id: string
  status: "in_progress" | "completed" | "failed" | "aborted"
  incomplete: boolean                // true = keep polling
  project_id: string
  project_url: string
  next_poll_after_ms?: number        // suggested poll interval
  output: MakaronOutput[]
}

type MakaronOutput =
  | { id: string; type: "text"; status: "completed"; content: string }
  | { id: string; type: "image"; status: "completed"; url: string; snapshot_id: string }
  | { id: string; type: "design"; status: "completed"; url: string; width: number; height: number; animated: boolean; duration?: number }
  | { id: string; type: "video"; status: "queued"|"rendering"|"completed"|"failed"; task_id: string; snapshot_id?: string; url?: string; elapsed_seconds?: number; width?: number; height?: number; error?: string; completion_actions?: CompletionAction[] }
  | { id: string; type: "music"; status: "queued"|"rendering"|"completed"|"failed"; task_id: string; url?: string; elapsed_seconds?: number }

type CompletionAction = {
  label: string
  prompt: string
  description?: string
  policy?: "confirm" | "auto"
}
```

## Polling Rules

1. Poll while `incomplete: true` or `status` is `"in_progress"`
2. Use `next_poll_after_ms` as interval (default 5000ms)
3. Stop when `status` is `"completed"`, `"failed"`, or `"aborted"`
4. Top-level `status: "completed"` means ALL artifacts are ready (including rendered videos)
5. If an async video fails, top-level `status` is `"failed"` and the failed video may include `completion_actions` for a safe retry or diagnosis. Agents can surface these as the next user-confirmed step.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (completed) or valid in-progress response |
| 1 | Failed, aborted, or HTTP error |
| 2 | Timeout (partial response still printed to stdout) |

## What Makaron Agent Can Do

| Task | Example prompt |
|------|---------------|
| Edit photo | "make it cinematic with warm tones" |
| Style transfer | "convert to oil painting style" |
| Add/remove elements | "add a cat on the table" / "remove background person" |
| Text-to-image | "generate a cyberpunk cityscape" |
| Video from image | "create a 5 second video of her walking" |
| Video with model | "use seedance model, make a 5s video" |
| Real MP4 edits | `--video clip.mp4 "trim this to the best 20 seconds and preserve audio"` |
| Background music | "add calm piano music" |
| Motion design | "create an Instagram story with animated text" |
| Multi-step | "edit the photo then make a video from it" |

## Export editable Remotion compositions

Animated Remotion compositions are saved as editable timeline/code artifacts first. Use `materialize` as the preferred high-level Remotion-to-MP4 command:

```bash
npx makaron-cli materialize --project <projectId> --media <N> --pick url
npx makaron-cli materialize --project <projectId> --design-json composition.json --pick url
npx makaron-cli responses get <runId> --materialize --wait --pick first_video_url
```

`materialize` defaults to `--wait`, `--publish`, and `fast_720p`, so the completed MP4 is added back to the timeline like CUI. Use `--no-publish` only when you need a file URL without a new timeline video. The completed export reports `duration_seconds`, `render_seconds`, and `realtime_ratio`; use those metrics instead of provider-video ETA rules.

For JSON-to-MP4, pass a Makaron/Remotion composition JSON with `--design-json`. This is the correct CLI path when another agent already has the composition JSON and only needs the exported video:

```bash
npx makaron-cli materialize --project <projectId> --design-json composition.json --pick url
cat composition.json | npx makaron-cli materialize --project <projectId> --design-json - --pick url
```

Keep `--project` because exports are project-scoped and publish back to the timeline by default. Use `--no-publish` only when you want the MP4 URL without adding a timeline video.

## Recommended Pattern: Service Flow (Feishu/OpenClaw/Group Chat)

When serving end-users in a chat environment (Feishu, Slack, Discord), use this proactive message pattern:

```bash
# 1. Immediately acknowledge the user
send_message "Got it! Working on it now..."

# 2. Create project + submit (one command)
RUN_ID=$(npx makaron-cli chat --project auto --image photo.jpg -b "make it cinematic and create a 5s video")

# 3. Send project link proactively
PROJECT_URL=$(npx makaron-cli responses get $RUN_ID --pick project_url)
send_message "Project created: $PROJECT_URL"

# 4. Wait for the final customer-ready result
RESULT=$(npx makaron-cli responses get $RUN_ID --wait --json)
IMAGE_URLS=$(echo "$RESULT" | jq -r '[.result.images[]?.imageUrl, .output[]? | select(.type == "image") | .url] | map(select(. != null)) | unique | .[]')
VIDEO_URLS=$(echo "$RESULT" | jq -r '[.result.videos[]?.videoUrl, .output[]? | select(.type == "video") | .url] | map(select(. != null)) | unique | .[]')

for URL in $IMAGE_URLS; do
  send_image "$URL"
done
for URL in $VIDEO_URLS; do
  send_video "$URL"
done
send_message "All done!"
```

**Key principles for service agents:**
- **Proactive, not silent**: Acknowledge immediately, send the project link early, then send the final customer-ready media when the run completes.
- **Media over links**: When possible, send images/videos as native media in the chat (download URL and upload as attachment), not just paste the URL.
- **Immediate acknowledgment**: Reply within 1 second of receiving user request. Don't make users wait for project creation.
- **Project link early**: Send the project URL right after creation so users can check anytime.
- **Use `get --wait --json` as the default service path**: reserve `watch --jsonl` for advanced streaming or debugging integrations that explicitly need incremental events.

## Important Notes

- One project = one conversation thread. All history is preserved.
- One run at a time per project. New message interrupts previous run.
- Multi-image: `create --image a.jpg --image b.jpg` or `chat --image ref.jpg`.
- Provider-generated videos can take 3-5 minutes; Grok is usually around 30-40 seconds; Gemini Omni is usually around 30-70 seconds plus Storage handoff. Remotion compositions should be converted with `materialize` / `responses get --materialize`, and timing should be read from `duration_seconds`, `render_seconds`, and `realtime_ratio`.
- Music takes ~60 seconds. Appears in output when done.
- Images are typically ready in 15-30 seconds.
- stdout is always machine-readable JSON/text. Human-friendly logs go to stderr.
- Always use `chat` as the primary interface — even for single image edits.
- `edit`/`video`/`music` are fallback tools for when `chat` is unavailable or you need raw model access without project context.
