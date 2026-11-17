# Music with ComfyUI

Call a user-defined ComfyUI server (local or remote) to generate **music /
audio** with **AceStep Audio 1.5** (text + optional lyrics → MP3). The user may
specify any of **theme, length, style, and lyrics** (one or more). If no style
or lyrics are given explicitly, the skill derives them from the request — and
from any image the user provides (see [Image → Music](#image--music-deriving-style-and-lyrics)).

## Quick Start

1. **Ensure a ComfyUI server is running** (locally, or on a host you can reach)
   with the AceStep 1.5 nodes and models installed (see below).
2. **Set the URL** (via environment variable or `config.json`). The endpoint is
   user-defined — the bundled default is `http://localhost:8188`; point
   `COMFYUI_URL` at any ComfyUI server you control. A non-local host prints a
   data-flow warning on every run. If no server is reachable, the script exits
   with configuration instructions.
   ```bash
   export COMFYUI_URL=http://comfyui.host:api-port
   ```
3. **Test the connection** (see [Testing](#testing) below).

## Configuration

Read `config.json` at the skill root. All values can be overridden by
environment variables:

| Env Variable | Overrides | Default |
|---|---|---|
| `COMFYUI_URL` | `comfyui_url` | `http://localhost:8188` |
| `COMFYUI_TIMEOUT` | `timeout_seconds` | 600 |
| `COMFYUI_POLL_INTERVAL` | `poll_interval_seconds` | `10` |
| `COMFYUI_KEEP_MODELS_RESIDENT` | `keep_models_resident` | `false` |
| `COMFYUI_OUTPUT_DIR` | `output_dir` | `media/comfyui` |
| `COMFYUI_APIKEY` | `comfyui_api_key` | _(none → no auth header)_ |

**Priority:** Environment variables > `config.json`.

> Note: The config.json key `comfyui_api_key` is optional. When empty/absent,
> **no** `Authorization` header is added. When set, every ComfyUI API request
> carries `Authorization: Bearer <key>` (env var wins over the config value).
> **This skill only *sends* the key — it does not authenticate the server.**
> For the key to be honored, the ComfyUI server must run an authentication
> custom node: the reference implementation is
> [`sunshinejnjn/comfyui-auth`](https://github.com/sunshinejnjn/comfyui-auth) —
> `git clone https://github.com/sunshinejnjn/comfyui-auth.git
> ComfyUI/custom_nodes/comfyui-auth`, add a `label = <your-key>` line to its
> `apikeys.conf`, restart ComfyUI, and point `COMFYUI_APIKEY` at the same key
> (full steps in the image-with-comfyui README's *ComfyUI API Key* section).
> Without the plugin installed, the key is silently ignored.

### Data & Privacy

- **Transmitted to the endpoint:** the music tags/lyrics and the workflow JSON
  (all runs). **No image is ever uploaded.** The reference image is used for
  **vibe extraction only** — it is never uploaded to, or sent to, any
  destination. If the user provides one, the agent visual-reads it locally and
  turns it into tags/lyrics before calling the script.
- **Endpoint** is user-defined (`COMFYUI_URL` env var > `comfyui_url` in
  `config.json`; bundled default `http://localhost:8188`). A non-local endpoint
  prints a warning on every run, and an unreachable server exits with
  configuration instructions. Use HTTPS for remote servers and never put
  credentials in the URL or logs.
- **Written to disk:** generated audio is saved under `output_dir` (config) or
  `COMFYUI_OUTPUT_DIR` in your workspace.

## Models & Custom Nodes

This skill uses the **existing** ComfyUI installation — it does not ship models
or nodes. Before using, ensure your ComfyUI has:

### Required Models (all SFW — see `MODEL_URL.txt` for the exact HF locations)

| File | Destination folder |
|---|---|
| `acestep_v1.5_xl_turbo_bf16.safetensors` | `ComfyUI/models/diffusion_models/` |
| `qwen_0.6b_ace15.safetensors` | `ComfyUI/models/clip/` |
| `qwen_4b_ace15.safetensors` | `ComfyUI/models/clip/` |
| `ace_1.5_vae.safetensors` | `ComfyUI/models/vae/` |

> ⚠️ The SFW weights usually have **different filenames** than what the bundled
> workflow's loader nodes expect. The script does NOT rename model files for
> you. Either rename the downloaded files to match the workflow node names, OR
> edit the node's `unet_name` / `clip_name*` to the actual filenames.

### Required Custom Nodes

| Node | Package | Source |
|---|---|---|
| `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio` | [AceStep-ComfyUI](https://github.com/AceStep/AceStep-ComfyUI) | `git clone` into `custom_nodes/` |
| `VAEDecodeAudio` | [ComfyUI-Audio](https://github.com/ligersearch/ComfyUI-Audio) | `git clone` into `custom_nodes/` |
| `SaveAudioAdvanced` | [ComfyUI-VideoHelperSuite](https://github.com/Fannovel16/ComfyUI-VideoHelperSuite) | `git clone` into `custom_nodes/` |
| `ModelSamplingAuraFlow` | ComfyUI core node | **update ComfyUI** (no custom package) |

When a missing node or model is detected, the script reports the package name
and a manual install hint — it never executes `git clone` itself (ComfyUI may
run on another host).

### Optional: retrieve-then-purge plugin (v0.4.0+)

After the local save succeeds the script posts `POST /purge_after_retrieval` to delete the server-side copy of the generated audio (AceStep 1.5 has no image input, so there are no uploaded inputs to clean up). This needs the [comfyui-purge-after-retrieval](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval) plugin on the server (ComfyUI ≥ 0.38) — **install it on the ComfyUI host**:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/sunshinejnjn/comfyui-purge-after-retrieval.git
# then restart ComfyUI
```

- It reuses the **same API key** as [comfyui-auth](https://github.com/sunshinejnjn/comfyui-auth) (no new credentials) and exposes no workflow nodes.
- **Without it**: generation still works; the script prints an install hint up to 3 times (count in `config.json` → `purge_fail_hints`), then defaults to keeping the server-side file. A successful purge resets the counter. `--keep` / `purge_remote: false` / `COMFYUI_PURGE=0` disable the purge entirely — details in [SKILL.md](SKILL.md) *Error Handling* #5

## Image → Music — Deriving Style and Lyrics

The **agent** reads the image; the workflow reads **only text**. When the user
sends an image and does **not** specify a full style prompt and/or lyrics, let
the **agent** derive them:

- Use the image to infer a suitable **style / mood / genre** for `--tags`.
- Derive **lyrics** only when it fits (and keep them short, on-theme, in the
  requested `--language`).
- **No image is uploaded.** AceStep 1.5 has no image input; the reference image
  is used for **vibe extraction only** and never leaves the agent's local
  context.
  image into tags/lyrics and hands only that text to the script.

Detailed rules → [references/image-first.md](references/image-first.md).

## Testing

```bash
# Health check
python3 music_with_comfyui.py test

# Generate a short instrumental as a smoke test
python3 music_with_comfyui.py music --tags "short ambient test tone" --duration 8

# Verify before each batch of jobs
python3 music_with_comfyui.py test
```

## CLI Reference

```bash
# Instrumental from a style description (default 120s, config params)
python3 music_with_comfyui.py music --tags "Lo-fi hip hop, 80 BPM, warm, chill"

# With explicit length
python3 music_with_comfyui.py music --tags "Epic cinematic orchestral" --duration 90

# With lyrics
python3 music_with_comfyui.py music \
  --tags "Indie pop, 104 BPM, bright" \
  --lyrics "[Verse 1]\n..." --language en

# Style / tuning overrides
python3 music_with_comfyui.py music \
  --tags "80s synthwave, neon, driving" --bpm 118 --keyscale "A minor" --language en

# Fixed seed (reproducible)
python3 music_with_comfyui.py music --tags "Ambient pad, slow" --seed 42

# Image-first mode: send the image, let the agent derive tags/lyrics
# (there is no --tags-image flag; the agent visual-reads the image for you).
# python3 music_with_comfyui.py music --tags "..."  # agent fills the tags

# Health check
python3 music_with_comfyui.py test
```

## Important Notes

### Local Skill — No Automatic Installation

This skill **does not install anything automatically**. It connects to your
existing ComfyUI instance via API calls. If a node is missing, the skill only
*reports* the package and a pinned manual install hint (it never runs
`git clone`).

### VRAM Release vs. Speed Tradeoff

By default the skill uses the `UnloadAllModels` node to free VRAM after each
generation, preventing VRAM exhaustion during repeated tasks. It's stripped only
when `keep_models_resident` is explicitly `true`; otherwise it runs and releases
VRAM on every run. The unload nodes are bypassed automatically if absent.

### Workflow Modifications

The workflow in `workflows/` is an **adapted** version of a real AceStep 1.5
graph. The original source + what changed is documented in
[references/attribution.md](references/attribution.md).

### Error Handling

The system handles the same categories as the image skill:

1. **Missing nodes** — reports node, package, install command, GitHub URL.
2. **Missing models** — aborts with the install hint (no blind substitution;
   there is only one model here).
3. **Non-critical utility nodes** (`UnloadAllModels`) — bypassed automatically.

See the *Error Handling* section in [SKILL.md](SKILL.md) and the Models/Nodes tables above.

### Testing / Debugging

- Run `test` to confirm the endpoint answers before generating.
- If a loader dropdown is blank in the web UI, the file isn't where ComfyUI is
  looking — check the folder in the Models table above.
- If a node reports *missing*, install the custom node / update ComfyUI (see
  the Nodes table).
- AceStep 1.5 is a **GPU** model — on an unaccelerated host it will run very
  slowly or fail; confirm the server has a usable GPU.

## Release Notes

- **0.4.14** — Security hardening: every request now routes through a custom
  `urllib` opener whose redirect handler strips the `Authorization` (`Bearer`)
  header before following any redirect that would leave the request's origin,
  so the ComfyUI API key can never leak to a third-party host via a 3xx
  redirect. Same-origin redirects keep the header and behave exactly as
  before. This is defense-in-depth; the skill still only talks to the single
  configured ComfyUI endpoint.
- **0.4.0** — Added the optional `purge_after_retrieval` cleanup workflow.
- **0.3.x and earlier** — Initial AceStep Audio 1.5 generation support.

