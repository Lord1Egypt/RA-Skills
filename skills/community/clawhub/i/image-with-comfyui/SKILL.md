---
name: image-with-comfyui
description: 'Use to generate, edit, or animate images and videos through a configured ComfyUI server — trigger with requests like "make a picture of", "replace the background", "cut out / extract the subject of", "turn this into a video", "edit my photo", or "make a 3D mesh of this character". Not for simple non-generation image tweaks. **Qwen-Image 2.1 Turbo** (model id `qwen21t`, the fast 8-step default) is the default model for both text-to-image (T2I) and image editing/multi-image (I2I); it can also **cut out / extract the main subject or any image element into a transparent-background image**. The earlier default **Qwen-Image 2.1** (id `qwen21`, 25-step) is still available via `--model qwen21`. Z-Image / SD3.5 (T2I), Qwen Image Edit (2511, single-image), **MiniMax H3 (FastH3 v2)** (I2V `h3_i2v` default / T2V `h3_t2v` — FastH3 v2 now generates video with an audio track, adding audio-enabled video generation to this skill), Wan2.2 (I2V), and **Pixal3D / Trellis2 (I2M, default image → 3D GLB mesh)** are available. The older **Hunyuan 3D v2.1 (I2M)** is still available under the `hyi2m` entry point. **Destructive cleanup disclosure:** after a run completes and results are saved locally, the script **deletes the server-side copies on the ComfyUI server of the generated outputs of this run AND of any input materials uploaded for generation** (source images / reference images) via `POST /purge_after_retrieval`, unless the user opts out via `--keep` or `COMFYUI_PURGE=0`. This removes only the generated outputs of the current run and the input materials uploaded for that run — nothing else on the server. The agent should tell the user before running when it will delete server-side copies, including any source/reference materials still needed, and honor `--keep` if the user wants to retain them. **All-or-nothing:** the script deletes server copies only when *every* required output of this run has been safely downloaded and saved locally; if **any** output fails to retrieve, nothing is deleted on the server — the run leaves the results available on the server for retry. Purge attempts are retried on every run (a persistent disable after repeated failures was intentionally removed)'
version: "4.7.5"
license: BSD-3-Clause
compatibility: 'ComfyUI ≥ 0.37.0 (≥ 0.38 needed on the server for the optional retrieve-then-purge plugin); requires python3; the endpoint and API key are loaded automatically from the environment — the agent just runs a subcommand, it does not manage the endpoint or key.'
allowed-tools: Read, Write, Edit, Exec, env, network, websearch, webfetch
  # env / network are used by the script itself (reads COMFYUI_* env, connects
  # to the one configured ComfyUI endpoint). websearch / webfetch are NOT called
  # by this skill's script; they are listed only so the agent invoking the skill
  # is pre-approved to search / fetch as context. The script never searches or
  # scrapes arbitrary hosts — see declared-permissions.
declared-permissions: |
  This skill is a self-contained ComfyUI HTTP client. The script declares the host
  capabilities it actually uses, and the agent never needs anything beyond the
  declared allowed-tools (Read, Write, Edit, Exec) to run it:
  - env   — reads COMFYUI_URL / COMFYUI_APIKEY / COMFYUI_OUTPUT_DIR / COMFYUI_TIMEOUT /
            COMFYUI_POLL_INTERVAL / COMFYUI_PURGE / COMFYUI_KEEP_MODELS_RESIDENT from the
            environment. These are the skill's own user-facing config overrides (documented
            in the module header and SKILL.md), not a privilege escalation. The API key is
            read into an Authorization header for the configured endpoint only; it is never
            printed, logged, or sent anywhere but that endpoint.
  - network — makes HTTPS/HTTP requests to the ONE configured ComfyUI endpoint only
            (GET /queue, /history, /object_info, /view, POST /prompt, /history, /purge_after_
            retrieval, and a multipart upload of the source image). No outbound fetch of
            arbitrary hosts, no code execution from remote payloads. Remote hosts print a
            data-flow warning on every run.
  - filesystem — writes generated media under the configured output_dir only (default
            media/comfyui); reads config.json and the bundled workflow JSON. It never writes
            outside output_dir and never reads credential/secret files.
  - No persistence: the skill does not install cron jobs, startup scripts, or state hooks.
    The purge_remote step deletes the current run's own server-side copies after a local save
    succeeds; it is scoped to this run and cannot touch unrelated files.
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      anyBins: ["python3"]
    config:
      path: "config.json"
    primaryEnv: COMFYUI_APIKEY
    envVars:
      - name: COMFYUI_APIKEY
        required: false
        description: >-
          ComfyUI API key. Sent only as an Authorization header to the configured
          endpoint (COMFYUI_URL / config.json comfyui_url). Empty/absent = no
          Authorization header is added; the key is never printed, logged, or
          sent anywhere but that endpoint.
      - name: COMFYUI_URL
        required: false
        description: ComfyUI server URL. Falls back to config.json comfyui_url when unset.
      - name: COMFYUI_TIMEOUT
        required: false
        description: Global generation timeout in seconds. Overrides config.json timeout_seconds.
      - name: COMFYUI_POLL_INTERVAL
        required: false
        description: Seconds between polling the server for generation status. Overrides config.json poll_interval_seconds.
      - name: COMFYUI_OUTPUT_DIR
        required: false
        description: Client-side output directory override. Overrides config.json output_dir.
      - name: COMFYUI_KEEP_MODELS_RESIDENT
        required: false
        description: >-
          "1/true/yes/on" keeps models resident between runs instead of releasing VRAM. Overrides config.json keep_models_resident (default: false).
      - name: COMFYUI_PURGE
        required: false
        description: >-
          "0" disables purge-after-retrieval globally. config.json purge_remote governs by default.
---

# Image with ComfyUI

Call a user-defined ComfyUI server to generate or edit images and videos, or turn an image into a 3D mesh. **Qwen-Image 2.1 Turbo** (id `qwen21t`) is the default model for both T2I and I2I; the earlier **Qwen-Image 2.1** (id `qwen21`, 25-step), Z-Image / SD3.5 (T2I), Qwen Image Edit 2511 (single-image edit), **MiniMax H3** (I2V `h3_i2v`, default / T2V `h3_t2v`), Wan2.2 (I2V), and **Pixal3D / Trellis2 (I2M, default image → 3D GLB)** are available. The older **Hunyuan 3D v2.1 (I2M)** is still available under the `hyi2m` entry point. If no ComfyUI server is reachable, the script exits with setup instructions — that is an environment/ops issue, not something to solve with your own requests (see [README.md](README.md)).

**Destructive cleanup disclosure:** after a run completes and results are saved locally, the script **deletes the server-side copies on the ComfyUI server of the generated outputs of this run AND of any input materials uploaded for generation** (source images / reference images) via `POST /purge_after_retrieval`, unless the user opts out via `--keep` or `COMFYUI_PURGE=0`. This removes only the generated outputs of the current run and the input materials uploaded for that run — nothing else on the server. The agent should tell the user before running when it will delete server-side copies, including any source/reference materials still needed, and honor `--keep` if the user wants to retain them. **All-or-nothing:** the script deletes server copies only when *every* required output of this run has been safely downloaded and saved locally; if **any** output fails to retrieve, nothing is deleted on the server — the run leaves the results available on the server for retry. Purge attempts are retried on every run (a persistent disable after repeated failures was intentionally removed).

- **T2I** (Text → Image) → **Qwen-Image 2.1 Turbo** (`qwen21t`, default) or Qwen-Image 2.1 legacy (`qwen21`) / Z-Image / SD3.5 Medium
- **I2I** (Image → Image / Edit / Multi-image, up to 16 refs) → **Qwen-Image 2.1 Turbo** (`qwen21t`, default) or Qwen-Image 2.1 legacy (`qwen21`) / Qwen Image Edit (2511, single image)
- **I2V** (Image → Video) → **MiniMax H3** (`h3_i2v`, default); Wan2.2 is still available under `wan2.2`
- **T2V** (Text → Video) → **MiniMax H3** (`h3_t2v`)
- **Cutout** (extract the main subject or any image element) → **Qwen-Image 2.1** — redraws the target on a transparent background, producing a clean, alpha-only image; see [Cutout below](#cutout-extract-the-subject).
- **I2M** (Image → 3D Mesh) → **Pixal3D / Trellis2** (default) — the source image feeds straight in (the graph removes its own background internally), generates a GLB, and zips it for delivery. The older **Hunyuan 3D v2.1** is available via `hyi2m` — it extracts the main character first (transparent PNG), generates a GLB, scales it ×3000, and zips it.

`config.json` at the skill root holds every default. The agent **never** reads, manages, or overrides the ComfyUI endpoint, API key, or poll settings by hand — the script loads those automatically at call time (env `COMFYUI_URL` / `COMFYUI_APIKEY` and `config.json`, as configured). The agent's entire job is: call one subcommand, then read the local output paths the script prints.

## Cutout — Extract the Subject

> **Note:** cutout is a genuine image-generation task, not a simple non-generation tweak — use it when the user wants to isolate the subject or any image element from its surroundings.

**Qwen-Image 2.1** can **cut out / extract** the main subject (or a specified element) from an image and return it on a transparent background. The output is a clean PNG with alpha only — it re-draws the target rather than doing a hard pixel mask, so it works well for organic shapes (people, animals, products, characters) and can target a specific described element (e.g. "extract just the red car", "isolate the vase") via the prompt.

- Use the **`i2i`** subcommand with `--image <path>` and a prompt that names the subject to extract. Keep the prompt focused on *what to keep*, not what to remove.
- The result is transparent (alpha-only). Deliver it as-is — never convert to JPG (which has no alpha channel, so it would flatten transparency onto white).
- This is the same redraw-to-transparent step that I2M runs first (see the i2m rules), but here it is used on its own to produce a standalone cutout image.

## When to Use

- Generate images from text → **t2i**
- Edit one image, or compose 2–16 reference images → **i2i** (`--image` order = slot order = `<image1>`, `<image2>` …)
- Turn an image into a short video → **MiniMax H3** (`h3_i2v`, default) or **wan2.2**
- Turn a text prompt into a short video → **MiniMax H3** (`h3_t2v`)
- Turn the character in an image into a **3D mesh (GLB)** → **`pi2m`** (Pixal3D / Trellis2, default) — the source image feeds straight in (the graph removes its own background internally). **`i2m` is an alias for `pi2m`** — the two names are interchangeable and both route to Pixal3D. For the older **Hunyuan 3D v2.1** extraction path (character extraction + ×3000 delivery), use `hyi2m`. See the **I2M Model Selection** table below.
- **Hybrid input (text prompt *plus* a source image as the conditioning frame / seed) → `h3_i2v`**, not `h3_t2v`. The source image drives the video; the prompt describes its motion. A `--seed` flag alone is *not* a way to feed an image in (it wants an integer).
- **Text only → `h3_t2v`.**
- The user sends an image, then within 2 minutes asks to edit or animate it → **image-first mode**:
  - **Detection:** the previous turn carries an image but no edit/video text; the current turn adds a short edit/animation request matched in the user's own language (CN or EN), e.g. 修一下/fix, 换背景/change background, 加特效/add an effect, 变动画/turn into a video, 改颜色/change color.
  - **Action:** route the remembered image + the new text to `i2i`/`wan2.2` (`--image <latest image>` = slot 1; `--prompt` = the new text). If unsure between I2I and I2V, **default to I2I** unless the text clearly says video/animation.
  - **Scope:** only the immediately preceding image from the *same user, same session*, inside the 2-minute window. Never reuse images from other users/sessions or older than 2 minutes. Don't ask for the image again — the script already has the latest path. Clear the remembered path once used, or after 2 minutes of silence.

### I2M Model Selection (which entry point matches your need)

Three I2M paths exist; pick by the extraction + delivery need, **not** by default:

| Want | Use | Why | Notes |
|---|---|---|---|
| Just mesh it (image feeds straight in, auto background removal) | **`pi2m`** | Pixal3D/Trellis2, `--image` is the only input, no redraw step | Delivery scale **×1** (real units baked in — no upscale). `__MAX resolution 512__` (config `mesh.pi2m.default_resolution`). |
| Clean cutout first, **not redraw**, then mesh | **`hyi2m --extract rembg`** | Non-generative `u2net` human cutout, done as a discrete step before the mesh | Best for *humans*; `u2net` is poor on non-humans. |
| Image is *already* a clean cutout, skip extraction | **`hyi2m --extract none`** | Feed the image straight in — only if it is already a clean cutout | No extraction run at all. |
| Highest detail + normalized-unit **×3000** delivery | **`hyi2m`** (Hunyuan 3D v2.1) | Default resolution **4096**, `--resolution` up to **8192**, delivery scale **×3000** | Only Hunyuan scales ×3000. |
| **User asked for ×3000 scale** | **`hyi2m`** | ×3000 is the Hunyuan normalized-unit convention — **the rule is `×3000 ⇒ hyi2m`** | Never pass `--scale 3000` to `pi2m` (see trap below). |
| **Redrawing first is fine / preferred for extraction** | **`hyi2m`** (default `--extract auto`) | Default extraction is **i2i** (Qwen-Image 2.1 redraws the character centered, transparent) | New users: `hyi2m` **redraws** the source before meshing unless `--extract rembg`/`none`. |

⚠️ **Never pass `--scale 3000` (or any large `--scale`) to `pi2m`.** `pi2m`'s default scale is **×1** because the Trellis2 mesh carries its own real-world units — `--scale 3000` would blow it up ~3000× (kilometres). `--scale N` is a real lever only on `hyi2m`, where the raw Hunyuan mesh is at a normalized unit scale (character ≈ 2 units) and needs the ×3000 in-place upscale before zipping (`--scale 1` keeps it unscaled).

⚠️ **`i2m` = `pi2m`.** The `i2m` subcommand is **an alias for the Pixal3D / Trellis2 `pi2m` path** (default I2M). It is *not* the Hunyuan path — if you want Hunyuan 3D v2.1 (character extraction + ×3000 delivery), use `hyi2m`.

- pi2m default `--resolution` 512 (Pixal3D/Trellis2 mesh at real units, delivery scale ×1 by default) — override with `--resolution N` if the node allows a larger latent grid; there is no documented maximum in this skill, so read the actual node cap from the workflow if a higher value is needed.
- hyi2m (Hunyuan 3D v2.1) default `--resolution` 4096; `--resolution` can go up to **8192** (the highest value shown in the cli-reference; treat it as the working cap).

## How the agent runs this (read first — this is the only thing that matters)

> **One command per job. That is the whole interaction.**

The script is **self-contained**: it reads `config.json` + the env-supplied
`COMFYUI_URL` / `COMFYUI_APIKEY` (auth header) automatically, submits the
workflow, **polls ComfyUI for progress on the agent's behalf**, **downloads and
saves the results** to `output_dir`, then prints those local paths. The agent
**never** touches the API key, never curls ComfyUI, and never polls `/queue` or
`/history` by hand — that is 150 lines the script already does internally.

- **Never** write your own `curl http://host:port/history/<id>` / `/queue` /
  `/object_info` / upload requests. The equivalent is the subcommand you run
  directly.
- **Never** `cat` the API key or put it in a header. It lives in the env that
  the script was started with; the script carries it into every request.
- If the script exits with configuration/setup instructions, the ComfyUI
  **endpoint or key is misconfigured at the environment level** — that is an
  ops fix (the `COMFYUI_URL` / `COMFYUI_APIKEY` env the script is launched
  under), **not** something to solve by building your own requests.
- For every model/flag, timeout, and delivery detail, see the reference files
  linked below instead of guessing.

## Data & Privacy (what actually goes over the wire)

- **What is transmitted:** prompts and the workflow JSON go to the configured
  endpoint for **every** mode; **I2I, I2V and I2M additionally upload the full
  source image**. The agent cannot control what the script transmits — it can
  only decide **whether** to run.
- **Endpoint / key:** loaded automatically from the environment (`COMFYUI_URL` /  
  `COMFYUI_APIKEY` and `config.json`). A non-local host prints a data-flow
  warning on every run. If no server answers, the script exits with setup
  instructions instead of a raw timeout. The Bearer key is only honored when the
  server runs an auth custom node that recognizes it — the reference
  implementation is [`sunshinejnjn/comfyui-auth`](https://github.com/sunshinejnjn/comfyui-auth) (setup: clone into
  `ComfyUI/custom_nodes/` + add your key to its `apikeys.conf`; full steps in the
  README's *ComfyUI API Key* section).
- **Written to disk:** generated media is saved under `output_dir`
  (`config.json` or `COMFYUI_OUTPUT_DIR`). Don't submit sensitive content if the
  endpoint or disk is a concern.
- **Secrets:** the API key is handled entirely inside the script (it is never
  printed, never logged, never part of the agent's output). The agent must not
  echo it into any message, URL, or log.

## Workflow Files

| Mode | Workflow | File |
|---|---|---|
| T2I (**Qwen-Image 2.1 Turbo, default `qwen21t`**) | Qwen-Image 2.1 Turbo | `workflows/qwen_image_2.1_turbo_api.json` |
| I2I (**Qwen-Image 2.1 Turbo, default `qwen21t`**, incl. multi-image) | same file, switch ON | `workflows/qwen_image_2.1_turbo_api.json` |
| T2I (Qwen-Image 2.1, legacy `qwen21`) | Qwen-Image 2.1 dual-mode | `workflows/qwen_image_2.1_api.json` |
| I2I (Qwen-Image 2.1, legacy) | same file, switch ON | `workflows/qwen_image_2.1_api.json` |
| T2I (Z-Image) | Z-Image | `workflows/z-image_t2i_api.json` |
| T2I (SD3.5) | SD3.5 Medium | `workflows/sd3.5-med_t2i_api.json` |
| I2I (legacy) | Qwen Image Edit (2511) | `workflows/qwen_image-edit_api.json` |
| **I2V (default `h3_i2v`)** | **MiniMax H3** Image-to-Video (8-step FastH3, int8_convrot — 4090-safe) | `workflows/h3_fasth3_i2v_api.json` |
| **T2V (`h3_t2v`)** | **MiniMax H3** Text-to-Video | `workflows/h3_fasth3_t2v_api.json` |
| I2V (legacy) | Wan2.2 Image-to-Video | `workflows/wan2.2_i2v_api.json` |
| I2M (Image → 3D Mesh) — default | Pixal3D / Trellis2 | `workflows/trellis2-pixal3d_i2m_api.json` |
| I2M (Image → 3D Mesh) — Hunyuan 3D v2.1 (`hyi2m`) | Hunyuan 3D v2.1 | `workflows/hunyuan3d-v2.1_i2m_api.json` |

Each workflow is an **adapted** version of a real ComfyUI graph. Original source + exactly what was changed → [references/attribution.md](references/attribution.md).

## CLI Usage

> **⚠️ The prompt is MANDATORY and must be passed via `--prompt` — never as a positional word.**
>
> Every subcommand (`t2i`, `i2i`, `h3_t2v`, `h3_i2v`, `wan2.2`) reads the prompt from `--prompt "..."`. Passing the prompt as a bare positional word fails immediately with exit code 2:
> `python3 image_with_comfyui.py t2i "some description"` → `t2i: error: the following arguments are required: --prompt`
>
> This is a **100%-avoidable failure loop** — the command never reaches ComfyUI, so the model can't help. Always write the prompt through `--prompt` on the **first** attempt.
>
> The default **I2M** entry point is `pi2m` (Pixal3D / Trellis2, no prompt — the character image is the condition; `--image` is its only required flag). `i2m` is an alias for `pi2m` — use either name, they are identical. `hyi2m` is the separate Hunyuan 3D v2.1 path (`--extract` + ×3000). `pi2m`/`hyi2m`/`i2m` take no prompt.

Full commands, output-format rules, and the timeout table live in the **CLI Reference / Output Format / Remote Purge / Timeout Reference** sections of README.md. The command flags below stay the same across every subcommand listed there.

**`--keep` (all generation subcommands):** retain the server-side copies of this run's outputs (and uploaded input images). Without it, the script auto-deletes them on the server after a **successful, all-or-nothing** retrieval (see Error Handling item 5).

## Prompt Formatting

- **Per-model prompt rules (formulas, key parameters, example prompts) are listed by model below.** Example prompts keep their bilingual keyword pairs where the original was bilingual (e.g. `blurry 模糊`).

  - **Z-Image (T2I):** structured natural-language (subject + scene + composition + lighting + style + constraints); **no negative prompts, no weighted tags**. `--aspect` optional — omitted ⇒ 1:1 1024×1024; in I2I match the source image's aspect.
  - **SD3.5 Medium:** natural-language sentences; **optional `--negative`**; default 1:1 1024×1024, 20 steps, **CFG 4.01** (control 4–7). Useful mixed CN/EN negatives: `blurry 模糊, low quality 低质量, pixelated 像素化, grainy 颗粒感, overexposed 过曝, underexposed 欠曝, flat lighting 平光, text 文字, watermark 水印, logo 商标`.
  - **Qwen-Image 2.1 Turbo / legacy:** 6-part natural-language formula; **CFG locked to 1.0** — never pass `--cfg`; optional short `--negative`. Turbo = 8-step default; 25-step legacy via `--model qwen21`.
  - **Qwen Image Edit (2511):** concise, positive-only, the user's exact words.
  - **MiniMax H3 (`h3_t2v`/`h3_i2v`):** motion/action prompts; default 10 s (i2v) / 15 s (t2v); `--length` overrides; `--aspect` optional for t2v.
  - **Wan2.2 (i2v):** motion/action prompts; default 81 frames, 4 steps, CFG 4.5; resolution depends on aspect (see README.md **CLI Reference** → Wan2.2 resolution table).
  - **`pi2m` / `hyi2m`:** no prompt — the source image is the only condition.

## Error Handling

The script auto-detects three categories of server-side problems and reports them with install/source guidance, and `t2i`/`i2i` run through a **runtime fallback chain** when the default model fails:

1. **Missing nodes** — reports which node, its package, and a pinned GitHub install hint (the script never runs `git clone` itself).
2. **Missing models** — substitutes a compatible model (SD3.5 medium variants → SD3.5 large; WAN high/low variants swap between each other).
3. **Non-critical utility nodes** (e.g. `UnloadAllModels`) — bypassed automatically without interrupting generation.
4. **Runtime fallback chain** — `t2i` auto-descends `qwen21 → z-image → sd35 → (any available server checkpoint)`; `i2i` auto-descends `qwen21 → qwen_imageedit` (never to a text-only model, since a T2I model can't honor the source image). A tier fails on send error / server timeout / `status_str == error` / no output images; **config problems** (missing model file or node) abort instead of degrading. A note prints when a lower tier succeeds. Disable with `--no-fallback`. A server unreachable *before* the run exits with setup instructions (endpoint/key config) rather than a raw mid-run timeout.
4. **Runtime fallback chain** — `t2i`/`i2i` auto-descend through alternate models (and, for t2i, any available checkpoint) on runtime failures; config problems (missing files/nodes) abort instead of degrading. Disable with `--no-fallback`.
5. **Post-retrieval purge failure (取回后删除失败)** — after a **successful all-or-nothing retrieval** the script asks the server to delete its copies of this run's outputs **and** uploaded input images (`POST /purge_after_retrieval`). If that fails (the server usually just lacks the plugin), generation is unaffected — the files are already local. The script then shows an install hint for the [comfyui-purge-after-retrieval](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval) plugin (server-side `git clone` into `custom_nodes/` + restart), **once per host per run**. Unlike older versions, a persistent failure counter is **not** stored in `config.json` and the auto-delete is **not** permanently disabled — every run retries the server-side deletion once the plugin is installed. **All-or-nothing guarantee:** if **any** output fails to download, the script does **not** delete anything on the server (outputs **and** uploaded inputs are retained) so the run's results stay available for retry. Disable entirely: `--keep` per run, or `purge_remote: false` / `COMFYUI_PURGE=0`.

## Output Delivery

**Send the generated file — do not just describe it.** Deliver in the **user's original session** using that channel's directive — never a bare URL line, and **never invent a directive variant** (`/MIL` is not a real directive; it will show up as literal text to the user). Per-channel prefixes and the staging/cleanup routine → [references/delivery.md](references/delivery.md)

**Output format:** generated images default to **JPG** (`config.json` → `image.output_format`). **Routing rule: if the user asks for a PNG image/file, or an RGBA image with transparency/alpha, always pass `--format png` and deliver the PNG file as-is — never convert to JPG** (JPEG has no alpha channel; the conversion would flatten transparency onto white). PNG output passes the server's PNG bytes through unchanged, so transparency is preserved byte-for-byte. Otherwise `--format jpg --jpg-quality N` is available per run; JPG conversion happens client-side (ComfyUI always saves PNG server-side). **i2m delivery rules (3D output):** the mesh is always **packaged as a zip** (`i2m_<timestamp>.zip`) and delivered as the **zip**, never the raw `.glb`. (a) For the default **`pi2m`** (Pixal3D / Trellis2) there is *no* extraction step — the character image is the model's own condition, not a separate file, so just deliver the zip. (b) For **`hyi2m`** (Hunyuan 3D v2.1) the raw mesh is at a normalized unit scale (character ≈ 2 units, no declared units), so the script **scales the GLB in place by the delivery factor** (default **×3000**; `--scale 1` keeps it unscaled) before zipping; optionally also attach the extracted character image if the user needs it. (c) **never render the mesh** — no GLB → image/video conversion and no 3D-viewer screenshots (a third-party online GLB viewer link may be shared **only if the user explicitly asks** — sharing such a link uploads the user's mesh to an external service, so never do it unprompted). Format conversion never applies to 3D files.

## Execution Discipline — Fast Path

The **measured GPU sampling time is ~12–20s**. When a task takes minutes, the delay is **not** inference — it's either a model cold-reload or agent-side overhead. Kill the waste:
0. **Never poll or check status by hand.** The script **submits, polls ComfyUI for progress, and fetches+saves the results itself** — then prints the local output paths. There is no agent-side step like `curl .../queue`, `.../history/<id>`, or `.../object_info`; that is the whole command you already ran. If a task is long, let the one command run (background it for i2m/video) and read the printed paths — do not spin around the ComfyUI API.

**i2m exception:** 3D generation is legitimately long (cold checkpoint load + 30 sampling steps + voxel decode ≈ minutes on a 4090). Run it once in the background (`exec` with a generous `timeoutSeconds`), report the queue state, and when it completes deliver the character image + the GLB zip per the i2m delivery rules above — don't spin tool calls around it.

1. **Never re-read on repeat.** Don't re-read `SKILL.md`, `config.json`, or the script for a known config / repeat / same-model job. Defaults are baked in; `--aspect` / `--steps` / `--cfg` are in the links above.
### Long-running jobs — use exec background mode (read this; this is where the skill trips up)

Two of these jobs are **legitimately long**, not overhead — do **not** treat them as stuck:
- **i2m / I2M** (3D GLB): cold checkpoint load + 30 sampling steps + voxel decode ≈ **minutes** on a 4090.
- **video** (wan2.2 / `h3_t2v` / `h3_i2v`): 5–15 s clips usually take **2–200 minutes** on a 4090.

For these, **run the one command in exec background mode and let it finish**, then deliver per the i2m / delivery rules above. Do not sit on the foreground command and do not spin tool calls around ComfyUI.

> **❌ The #1 mistake here: starting the job yourself with `nohup python3 image_with_comfyui.py … &` inside a normal foreground exec command, then letting that command return.**
>
> That is exactly how every turn on this skill gets wasted, and it is not a ComfyUI problem — it is a process-group problem:
>
> 1. You background the generation inside a **foreground** exec command; the `&` attaches the generation process to **that exec session's process group**.
> 2. The foreground command returns a few lines later, and the session sees the command as done.
> 3. The session end **recycles the whole process group** — including the `nohup`'d generation, because it is still a child of that session. `nohup` only blocks the normal "shell exit" signal; it does **not** survive a process-group recycle.
> 4. Result: your 120-minute generation dies at second ~10, the log stays empty, the process vanishes, and you have nothing. Nothing was ComfyUI's fault.
>
> **✅ Use exec's built-in background mode instead.** That mode launches the command as a session that *stays alive past the command* and returns the output when it completes — it is the correct tool for "run something long and get the result later." One command, the generation runs to completion on its own, results come back on finish. `t2v` / video / i2m succeed this way every time; the `nohup…&` approach fails every time.

3. **At most one pre-check merge.** Gather any needed info in a single batched command, or skip it entirely for trivial repeat jobs.
3. **Run immediately after one check.** Don't inspect, second-guess, or add tool calls between knowing the prompt and running.
4. **Verify only the minimum.** After the run, check only what the user asked (size / seed / file exists).
5. **Golden rule:** sampling is ~12–20s. Anything longer = reload or overhead — never pile on tool calls before the image exists.
6. **Prompt-flag trap:** pass `--prompt "..."` on the first attempt; a positional word wastes a whole turn.

## References (index)

- [references/attribution.md](references/attribution.md) — original source + modifications per workflow
- [references/delivery.md](references/delivery.md) — per-channel delivery + staging
