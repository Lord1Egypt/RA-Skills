# Image with ComfyUI

Call a user-defined ComfyUI server (local or remote) for **text-to-image**, **image-to-image/edit**, **image-to-video**, and **image-to-3D-mesh** generation. **Qwen-Image 2.1 Turbo** is the **default** model for both T2I and image editing (including multi-image reference composition) as of v3.7.0; **Qwen-Image 2.1** (legacy, 25-step), Z-Image, SD3.5 Medium, Qwen Image Edit (2511), Wan2.2, and Hunyuan 3D v2.1 (3D mesh) are available as options.

> **New here?** Qwen-Image 2.1 needs a one-time ComfyUI setup — see [Qwen-Image 2.1 ComfyUI Setup](#qwen-image-21-comfyui-setup).

## Quick Start

1. **Ensure a ComfyUI server is running** (locally, or on a host you can reach).
2. **Set the URL** (via environment variable or `config.json`). The endpoint is user-defined — the bundled default is `http://localhost:8188`; point `COMFYUI_URL` at any ComfyUI server you control — a data-flow warning is printed on every run for non-local hosts. If no server is reachable, the script exits with configuration instructions:
   ```bash
   export COMFYUI_URL=http://comfyui.host:api-port
   ```
3. **Test a workflow** (see [Testing](#testing) below).

## Configuration

Read `config.json` at the skill root. All values can be overridden by environment variables:

| Env Variable | Overrides | Default |
|---|---|---|
| `COMFYUI_URL` | `comfyui_url` | `http://localhost:8188` |
| `COMFYUI_TIMEOUT` | `timeout_seconds` | `120` |
| `COMFYUI_POLL_INTERVAL` | `poll_interval_seconds` | `10` |
| `COMFYUI_KEEP_MODELS_RESIDENT` | `keep_models_resident` | `false` |
| `COMFYUI_PURGE` | `purge_remote` | `true` |
| `COMFYUI_OUTPUT_DIR` | `output_dir` | `media/comfyui` |
| `COMFYUI_APIKEY` | `comfyui_api_key` | _(none → no auth header)_ |

**Priority:** Environment variables > `config.json`.

> Note: The config.json key `comfyui_api_key` (string) is optional. When empty/absent, **no** `Authorization` header is added and behavior is unchanged. When set, every ComfyUI API request carries `Authorization: Bearer <key>` (env var wins over the config value).

### 🔒 ComfyUI API Key (Bearer Auth)

If your ComfyUI instance requires an API key, set it via either of these (env var takes precedence):

```bash
export COMFYUI_APIKEY=sk-your-key
```

or, in `config.json`:

```json
"comfyui_api_key": "sk-your-key"
```

When present, the skill adds `Authorization: Bearer <key>` to all ComfyUI API calls (`/prompt`, `/history`, `/object_info`, `/upload/image`, `/view`, `/upload/*`). Do not commit your key to version control — prefer the env var, and never paste it into the chat or logs.

> **⚠️ This skill only *sends* the key — it doesn't authenticate your ComfyUI itself.** For the Bearer key to be honored, the ComfyUI server must run an authentication custom node that recognizes that key. The reference implementation is [`sunshinejnjn/comfyui-auth`](https://github.com/sunshinejnjn/comfyui-auth) (a fork of the original [`ivellioscolin/comfyui-auth`](https://github.com/ivellioscolin/comfyui-auth)). To set it up:
> 1. Clone it into your ComfyUI: `git clone https://github.com/sunshinejnjn/comfyui-auth.git ComfyUI/custom_nodes/comfyui-auth`
> 2. Edit its `apikeys.conf` — add a `label = <your-key>` line (the key is read **as written**, plain or as configured), then restart ComfyUI (the plugin reloads its config per request, but a re-clone/restart makes the new code load).
> 3. Point this skill at that server via `COMFYUI_URL` and set `COMFYUI_APIKEY` to that same key.
>
> Without the plugin installed on the server, the key is silently ignored and the API responds as if no auth is required. The `test` command (`python3 image_with_comfyui.py test`) will tell you whether the endpoint answers before you try generating.

### Data & Privacy

- **Transmitted to the endpoint**: prompts and workflow JSON (all modes); **full source images** for I2I and I2V.
- **Endpoint** is user-defined (`COMFYUI_URL` env var > `comfyui_url` in `config.json`; bundled default `http://localhost:8188`). A non-local endpoint prints a warning on every run, and an unreachable server exits with configuration instructions (this section + [Qwen-Image 2.1 ComfyUI Setup](#qwen-image-21-comfyui-setup)). Use HTTPS for remote servers and never put credentials in the URL or logs.
- **Written to disk**: generated media is saved under `output_dir` (config) or `COMFYUI_OUTPUT_DIR` in your workspace; delivery staging copies live in `~/.openclaw/media/outbound/` and are removed after a successful send. If your content is sensitive, review the endpoint and output location before running.

## Models & Custom Nodes

This skill uses the **existing** ComfyUI installation — it does not ship models or nodes. Before using, ensure your ComfyUI has:

### Required Models

Every model below has a **verified download source** in [`MODEL_URL.txt`](MODEL_URL.txt) — open that file for the exact HuggingFace repo, folder, and filename. The bundled workflows are configured for the **SFW/official model set — that is the default and the recommended setup**. Some deployments additionally run community UC/NSFW-merged weights (e.g. uncensored Qwen-Image 2.1, NSFW creator merges for Wan2.2); those are an **explicit opt-in, non-default choice** — they are never part of this skill's standard configuration, and nothing in this skill enables them.

| Model | Expected Location | Source |
|---|---|---|
| Z-Image (SVD XT) | `ComfyUI/models/checkpoints/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| SD3.5 Medium | `ComfyUI/models/checkpoints/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| Qwen Image Edit Plus | `ComfyUI/models/checkpoints/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| **Qwen-Image 2.1 Turbo** (default T2I + edit, `qwen21t`) | see [Qwen-Image 2.1 ComfyUI Setup](#qwen-image-21-comfyui-setup) | [`MODEL_URL.txt`](MODEL_URL.txt) |
| Wan2.2 1.3B | `ComfyUI/models/checkpoints/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| Wan2.2 VAEMODEL | `ComfyUI/models/vae/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| Wan2.2 Audio Model | `ComfyUI/models/audio_encoders/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| T5XXL & FluxFill | `ComfyUI/models/clip/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| **Hunyuan 3D v2.1** (I2M) | `ComfyUI/models/checkpoints/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| **MiniMax H3 (video, default 2v)** — diffusion / video VAE / audio VAE / r2v LoRA / embeddings | `ComfyUI/models/diffusion_models/` + `models/vae/` + `models/loras/` + `models/embeddings/` | [`MODEL_URL.txt`](MODEL_URL.txt) |
| **MiniMax H3 text encoder** (GGUF Q4_K_M, nif0 Instruct repo — public, anonymous download OK; ⚠ repo id casing is `MiniMax`) + mmproj (i2t, same stem, same dir) | `ComfyUI/models/clip/` | [`MODEL_URL.txt`](MODEL_URL.txt) |

### Required Custom Nodes

Install **pinned at reviewed commits** (as of 2026-09-20). Check out the exact commit rather than a mutable default branch, and install dependencies in an isolated venv under a non-privileged user — never `pip install` as root:

| Node | Package (repo) | Pinned commit |
|---|---|---|
| Impact Pack | [ltdrdata/ComfyUI-Impact-Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack) | `429d0159a` |
| WAS Nodes | [WASasquatch/was-node-suite-comfyui](https://github.com/WASasquatch/was-node-suite-comfyui) *(repo renamed from `ComfyUI-WAS-Nodes`)* | `9934caa92` |
| ComfyUI-Manager | [Comfy-Org/ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager) *(migrated from `comfyanonymous/`)* | `946ef8fe6` |
| ComfyUI-GGUF (Nif00 fork — MiniMax H3 `CLIPLoaderGGUF` + mmproj support) | [Nif00/ComfyUI-GGUF](https://github.com/Nif00/ComfyUI-GGUF) | `b6a9358c4` |
| rgthree | [rgthree/rgthree-comfy](https://github.com/rgthree/rgthree-comfy) | — (required by the Qwen-Image 2.1 workflow's LoRA pass-through node) |

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
cd ComfyUI-Impact-Pack && git checkout --detach 429d0159ad429e64d2b3916e6e7be9c22d025c3c
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Repeat the same pin-and-checkout pattern for the other two repositories (use their pinned commits above). Review dependency lists before installing, and re-check upstream commits before upgrading a pin.

When a missing node or model is detected, the script reports the package name and a manual install hint — it never executes `git clone` itself (ComfyUI may run on another host).

### Optional: retrieve-then-purge plugin (v4.5.0+)

After the local save succeeds the script posts `POST /purge_after_retrieval` to delete the server-side copies of the run's output files **and** the input files it uploaded (ComfyUI's `output/` and `input/` would otherwise grow forever). This needs the [comfyui-purge-after-retrieval](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval) plugin on the server (ComfyUI ≥ 0.38) — **install it on the ComfyUI host**:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/sunshinejnjn/comfyui-purge-after-retrieval.git
# then restart ComfyUI
```

- It reuses the **same API key** as [comfyui-auth](https://github.com/sunshinejnjn/comfyui-auth) (no new credentials) and exposes no workflow nodes.
- **Without it**: generation still works; the script asks the server to delete the files on **every run**, showing an install hint for the plugin **once per host per run** (a persistent per-host dedup — not a 3-run cutoff). A successful purge resets per-host state. `--keep` / `purge_remote: false` / `COMFYUI_PURGE=0` disable the purge entirely — details in [SKILL.md](SKILL.md) *Error Handling* #5.

## Qwen-Image 2.1 ComfyUI Setup

**Qwen-Image 2.1 Turbo** (model id `qwen21t`) is the **default** model for both `t2i` and `i2i` as of v3.7.0. It is the fast (8-step) turbo quantization of the same Qwen-Image 2.1 architecture; one workflow covers text-to-image, single-image edit, and multi-image reference composition. It is a distilled model — **CFG must stay at 1.0** (the script enforces this; raising it burns the image).

The earlier default was **Qwen-Image 2.1** (model id `qwen21`, 25-step). It still exists and can be forced with `--model qwen21`; the turbo default (`qwen21t`) is much faster (8 steps) with the same quality band. Both load the same `fp8_e4m3fn_fast` int8-convrot quantization; see the model files section below.

### Prerequisites
- **ComfyUI ≥ 0.37.0** (frontend 1.53.6). The workflow uses core nodes that only exist in recent builds:
  - `TextEncodeQwenImage21` (`comfy_extras.nodes_qwen`)
  - `ResolutionSelector` (`comfy_extras.nodes_resolution`)
  - `ComfySwitchNode` / `If/Else Switch` (`comfy_extras.nodes_logic`)
  - `PrimitiveBoolean` (`comfy_extras.nodes_primitive`)
  
  If any show up as a red *missing node*, **update ComfyUI** — they are core, not a custom pack. (`If/Else Switch` is experimental and may be hidden from node search until you enable experimental nodes; loading the workflow works either way.)

### Model files (3)
Both `qwen21` (legacy) and `qwen21t` (turbo, default) load from the same folders. Place each under your ComfyUI install. These are the exact filenames the workflows expect:

| Model | File | Destination folder |
|---|---|---|
| **turbo** (default) | `QWEN_Image/qwen-image-2.1-turbo-int8_convrot.safetensors` | `ComfyUI/models/diffusion_models/` (keep the `QWEN_Image/` subfolder; older builds may use `models/unet/`) |
| **legacy** (`qwen21`) | `QWEN_Image/qwen-image-2.1-UC-int8_convrot.safetensors` | `ComfyUI/models/diffusion_models/` (keep the `QWEN_Image/` subfolder; older builds may use `models/unet/`) |
| text encoder | `qwen3vl_8b_int8_convrot.safetensors` | `ComfyUI/models/text_encoders/` (Qwen3-VL 8B int8; loaded with `type: qwen_image`) |
| VAE | `qwen_image_2.1_vae_bf16.safetensors` | `ComfyUI/models/vae/` |

> The **turbo** diffusion file is `qwen-image-2.1-**turbo**-int8_convrot` and the **legacy** one is `qwen-image-2.1-**UC**-int8_convrot` — different filenames, same quantization family. Each workflow's UNETLoader (turbo → `workflows/qwen_image_2.1_turbo_api.json` node 17; legacy → `workflows/qwen_image_2.1_api.json` node 17) selects its own file by name, with `weight_dtype: fp8_e4m3fn_fast`. If you use a different quantization/filename, update the relevant node's `unet_name` to match what's on disk.

> Download source (SFW, all quantizations) → [MODEL_URL.txt](MODEL_URL.txt) → `abenzerps/Qwen-Image-2.1-Turbo-Quantized` and the original `qwen21` sources listed there.

> Unlike the original foprc workflow (which used a GGUF Q8 model + ComfyUI-GGUF), this workflow loads the diffusion model via **`UNETLoader`** with `weight_dtype: fp8_e4m3fn_fast`. That **removes the ComfyUI-GGUF dependency** — the only custom node needed is **rgthree**.

If you use a different quantization/filename, update `unet_name` in `workflows/qwen_image_2.1_api.json` (node `17`) to match what's on disk.

### Custom nodes
- **rgthree-comfy** (for the `Power Lora Loader` node) — install via ComfyUI Manager or `git clone https://github.com/rgthree/rgthree-comfy` into `custom_nodes/`, then restart.
- All other nodes are core ComfyUI.
- *Optional:* the LoRA stack is off by default and passes the model/CLIP straight through. If you don't have rgthree, you can instead delete node `10` and rewire `17 → 6` (model) and `2 → 5` (clip).

### Verifying your setup
```bash
python3 image_with_comfyui.py test          # server reachable?
python3 image_with_comfyui.py t2i --prompt "A red fox in snow" --aspect 1:1
python3 image_with_comfyui.py i2i --prompt "Change the sky to sunset" --image /path/in.jpg
```
If a loader dropdown is blank in the web UI, the file isn't where ComfyUI is looking — check the folder above. If a node reports *missing*, update ComfyUI (see Prerequisites).

### How the dual-mode switch works
Node `12` (`PrimitiveBoolean`) is the master switch:
- **OFF** (`false`) → pure **T2I**: the sampler starts from an empty latent sized by `ResolutionSelector` (aspect ratio + megapixels).
- **ON** (`true`) → **edit / multi-image**: reference image(s) feed `TextEncodeQwenImage21`, whose output latent is sampled instead. The script wires 1 image to `image_1`, and extra images to `image_2 … image_N` (up to 16).

### Multi-image prompt format
With 2+ reference images, the model sees them in **slot order** (`image_1`, `image_2`, …). Reference each by index in the prompt so it knows which is which:
```
Put the garment from <image2> onto the person in <image1>, keep <image1>'s pose and lighting.
Combine both photos into one scene: subject of <image1> on the left, subject of <image2> on the right.
```
Keep the instruction concise and in the user's language; the skill passes it through verbatim. `--image` accepts multiple paths (order = slot order = `<image1>`, `<image2>` …).

## Testing

Use the built-in test script:

```bash
# Health check
python3 image_with_comfyui.py test

# Test each workflow individually
python3 image_with_comfyui.py t2i --prompt "A cat on a windowsill"

# Run the health check before each batch of jobs
python3 image_with_comfyui.py test
```

### Output filename scheme

Generated files use a short mode prefix + timestamp (`YYYYMMDD_HHMMSS`) + ComfyUI's counter:

| Mode | Prefix | Example (JPG) |
|---|---|---|
| Qwen-Image 2.1 **Turbo** T2I (`qwen21t`, **default now**) | `qtt2i` | `qtt2i_20260928_050328_00001.jpg` |
| Qwen-Image 2.1 **Turbo** I2I (`qwen21t`, **default now**) | `qti2i` | `qti2i_20260928_050328_00001.jpg` |
| Qwen-Image 2.1 (legacy, `qwen21`) | `qt2i` | `qt2i_20260928_050328_00001.jpg` |
| Qwen-Image 2.1 (legacy, `qwen21`) | `qi2i` | `qi2i_20260928_050328_00001.jpg` |
| Qwen Image Edit (2511) | `qei2i` | `qei2i_20260928_050328_00001.jpg` |
| Z-Image T2I | `zt2i` | `zt2i_20260928_050328_00001.jpg` |
| SD3.5 Medium T2I | `st2i` | `st2i_20260928_050328_00001.jpg` |
| Character cutout (`pi2m`/`hyi2m` step 1) | `mcut` | `mcut_20260928_050328_00001.png` |
| Trellis2/Pixal3D I2M (`pi2m`) | `pi2m` | `pi2m_00002.glb` |
| Trellis2/Pixal3D I2M delivery package | `pi2m` | `pi2m_00002.zip` (the GLB at natural units inside) |
| Hunyuan 3D v2.1 I2M (`hyi2m`) | `hyi2m` | `hyi2m_20260928_050328_00001.glb` |
| Hunyuan 3D v2.1 I2M delivery package | `hyi2m` | `hyi2m_20260928_050328_00001.zip` (the ×3000-scaled GLB inside) |

The trailing underscore ComfyUI appends is stripped, so names never end in `_`. The `pi2m` (Pixal3D / Trellis2) GLB **carries its own real-world units** (delivery scale ×1) and is packaged as `<same-stem>.zip` — the `.glb` stays on disk, but what gets sent to the user is the **zip** (delivery rules: SKILL.md → Output Delivery). The `hyi2m`/legacy Hunyuan 3D v2.1 GLB is **scaled ×3000 in place, then packaged as `<same-stem>.zip`** — the `.glb` stays on disk, but what gets sent to the user is the **zip** (delivery rules: SKILL.md → Output Delivery; the character image is also sent, as an image, and the mesh is never rendered).

### Manual Workflow Testing

You can also test workflows directly in the ComfyUI web UI. Copy any workflow file from `workflows/` into ComfyUI, load it, and run:

- **Qwen-Image 2.1 Turbo (T2I + edit + multi-image, default `qwen21t`)**: `workflows/qwen_image_2.1_turbo_api.json`
- **Qwen-Image 2.1 legacy (T2I + edit + multi-image, `qwen21`)**: `workflows/qwen_image_2.1_api.json`
- **Z-Image T2I**: `workflows/z-image_t2i_api.json`
- **SD3.5 Medium T2I**: `workflows/sd3.5-med_t2i_api.json`
- **Qwen Image Edit (2511)**: `workflows/qwen_image-edit_api.json`
- **MiniMax H3 I2V (default `h3_i2v`)**: `workflows/h3_fasth3_i2v_api.json`
- **MiniMax H3 T2V (`h3_t2v`)**: `workflows/h3_fasth3_t2v_api.json`
- **Wan2.2 I2V**: `workflows/wan2.2_i2v_api.json`
- **Hunyuan 3D v2.1 I2M (image → 3D mesh)**: `workflows/hunyuan3d-v2.1_i2m_api.json`

## Important Notes

### Local Skill — No Automatic Installation

This skill **does not install anything automatically**. It connects to your existing ComfyUI instance via API calls; the workflows, models, and custom nodes must already be configured in your ComfyUI setup. If a node is missing, the skill only *reports* the package and a pinned manual install hint (it never runs `git clone` itself, since ComfyUI may be on another host). The manual commands in [Required Custom Nodes](#required-custom-nodes) are optional setup steps for your own ComfyUI — review and pin them before running.

### VRAM Release vs. Speed Tradeoff

By default this skill uses the `UnloadAllModels` node (and `UnloadModel` in the Qwen edit branch) to free VRAM after each generation, preventing VRAM exhaustion during repeated tasks. The unload nodes are stripped only when `keep_models_resident` is explicitly set to `true` (config or `COMFYUI_KEEP_MODELS_RESIDENT`); otherwise they run and release VRAM on every run. The unload nodes are bypassed automatically if a given ComfyUI instance doesn't have them — the system detects and skips them transparently.

> **The slow part of a “5-minute” run is almost never inference.** It's model reload *or* agent-side overhead before the run, not the sampling. See the skill's **Execution Discipline — Fast Path** section for how the run is expected to be invoked.

### Workflow Modifications

All workflow files in the `workflows/` directory are **adapted versions** of original ComfyUI workflows. They are repackaged into self-contained HTTP-API graphs — the original source is **not** kept inside the JSON. The original source for each workflow plus exactly what was changed is documented in [references/attribution.md](references/attribution.md). Known modifications include:
- API-ready output node placement + timestamped output filenames
- Parameter exposure (aspect, steps, CFG, seed, neg, etc.) for external control
- Prompt auto-routing (e.g. Qwen Edit routes to the positive prompt node)
- A standard **safetensors** model load replacing the original GGUF load (Qwen-Image 2.1), dropping the ComfyUI-GGUF dependency
- VRAM-cleanup nodes (`UnloadAllModels`, `UnloadModel`) added, auto-bypassed when absent
- The SD3.5 double-`.safetensors` suffix bug fixed; Wan2.2 pointed at 4-step Lightspeed weights

### Error Handling

The system handles three categories of errors automatically:

1. **Missing nodes** — Reports which node is missing, provides package name, install command, and GitHub URL.
2. **Missing models** — Attempts to substitute a compatible model (e.g., SD3.5 medium variants → SD3.5 large).
3. **Non-critical utility nodes** — Automatically bypasses nodes like `UnloadAllModels` without interrupting generation.

## CLI Reference

```bash
# Generate image from text (default: Qwen-Image 2.1 Turbo, --model qwen21t)
python3 image_with_comfyui.py t2i --prompt "Your description" --aspect 1:1

# Generate with an explicit model
python3 image_with_comfyui.py t2i --model z-image --prompt "Your description"
python3 image_with_comfyui.py t2i --model sd35 --prompt "Your description" --negative "blurry"

# Edit an image (default: Qwen-Image 2.1 Turbo, --model qwen21t)
python3 image_with_comfyui.py i2i --prompt "Replace background" --image /path/to/image.png

# Multi-image reference (2+ images; order = <image1>, <image2>, ...)
python3 image_with_comfyui.py i2i \
  --prompt "Put the shirt from <image2> on the person in <image1>" \
  --image /path/person.jpg /path/shirt.jpg

# Generate video from image
python3 image_with_comfyui.py wan2.2 --prompt "Camera pans left" --image /path/to/image.png

# Turn the character in an image into a 3D mesh (GLB)
# Default: pi2m (Pixal3D / Trellis2) — source image fed straight in, scale x1
python3 image_with_comfyui.py pi2m --image /path/to/character.jpg
# Older path: hyi2m (Hunyuan 3D v2.1) — extract first (i2i transparent cutout), scale x3000
python3 image_with_comfyui.py hyi2m --image /path/to/character.jpg
# --extract rembg (u2net cutout, no redraw) | --extract none (image used as-is)
# Delivery: for pi2m, just the pi2m_*.zip; for hyi2m, character image + hyi2m_*.zip;
# the mesh is never rendered (no GLB -> image/video conversion; viewer links OK)

# Test ComfyUI connection
python3 image_with_comfyui.py test
```

## Timeout Reference

Video modes use a **length-based** floor (`length_seconds × 600`) to cover cold loads and long generations on shared GPUs (10 s ⇒ 6000 s, 15 s ⇒ 9000 s, 30 s ⇒ 18000 s). Other modes use a fixed cap.

| Mode | Timeout |
|---|---|
| T2I (all Qwen-Image models) | 500s |
| I2I (Qwen 2.1) | 600s |
| I2I (Qwen Image Edit 2511) | 600s |
| I2V (MiniMax H3 `h3_i2v`) | `length_seconds × 600` |
| T2V (MiniMax H3 `h3_t2v`) | `length_seconds × 600` |
| I2V (Wan2.2) | 1000s |
| I2M (Pixal3D / Trellis2, default `pi2m`) | 1000s |
| I2M (Hunyuan 3D v2.1 `hyi2m`) | 900s |

## Release Notes

- **4.7.4** — Added `websearch` and `webfetch` to the skill's `allowed-tools` preapproval so the agent invoking the skill is authorized to search the web and fetch reference pages as context. Note: these two are **agent** tools, not **script** tools — the ComfyUI script itself never searches or scrapes arbitrary hosts; it only connects to the single configured ComfyUI endpoint (see `env` / `network` and `declared-permissions`).
- **4.7.5** — Addressed the two findings from the A.I.G / scanner v0.2.2 audit: (1) **bearer-credential cross-origin redirect**: the script now routes every request through a single custom opener whose redirect handler strips the `Authorization` header before following any redirect that would leave the request's origin, so the ComfyUI API key is only ever sent to the configured endpoint and is never leaked to a third-party origin; same-origin redirects keep the header and behave exactly as before. (2) **residual server files**: the script now records every server-side output (final results + intermediate stage outputs + extra SaveImage outputs) produced by a run, and on success purges the whole run's server-side copies in one shot instead of only the final outputs and upload inputs — so no generated image is left behind on the ComfyUI server.
- **4.7.3** — Declared the `env` and `network` capabilities in the skill's `allowed-tools` preapproval, so the skill's MCP Least Privilege audit findings (which require reading `COMFYUI_*` environment variables and making HTTPS/HTTP requests to the single configured ComfyUI endpoint only) are covered by an explicit, documented declaration instead of an undeclared capability.
- **4.7.2** — Fixed an all-or-nothing safety bug in the Hunyuan 3D (`hyi2m`) / I2M (`i2m`) two-step path. When character extraction broke off early (in particular an output-retrieval failure), the run previously continued with the original image while recording nothing. If mesh generation then succeeded, cleanup could delete the uploaded source/reference copies from the server even though the run was not fully successful, violating the advertised run-wide all-or-nothing retention guarantee. The run now tracks extraction failure and retains all server-side files for retry; `--keep` / `COMFYUI_PURGE=0` still opt out entirely. The successful path (mesh succeeds → source, cutout, and GLB all purged) is unchanged.
- **4.7.1** — Added HTTPS / trusted-endpoint warnings for remote (non-localhost) ComfyUI hosts. Purge now happens only after the extraction stage's result is safely produced and before the mesh stage, so a failed mesh no longer loses the uploaded source image.
