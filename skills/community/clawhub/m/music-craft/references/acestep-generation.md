# ACE-Step Generation

Complete ACE-Step 1.5 operating guide: API workflow (submit, poll, copy),
full-song generation, quality tiers with memory-safe selection, and
audio-conditioned generation (cover, repaint, reference audio). Load this
when the selected backend is ACE-Step.

## ACE-Step 1.5 (local — free, vocals + lyrics, best local quality)

**Best for:** local generation with real vocals, separate lyrics, song structure, up to 10 minutes (600s). No API key, no quota. Runs natively on Apple Silicon via MLX.

**Verified routing note (2026-06-12):** ACE-Step is the exact-duration route.
In a 9-song field run, local M1+M2 generations returned the requested
`audio_duration` exactly for 18/18 jobs. MiniMax cloud was faster but returned
57-135% of requested duration for the paired cloud jobs.

**Prerequisites:** REST API must be running on `http://127.0.0.1:8001`. Install with:
```bash
git clone https://github.com/ace-step/ACE-Step-1.5.git "${ACE_STEP_PATH}"
cd "${ACE_STEP_PATH}" && uv sync
uv run acestep-api --port 8001   # or: ./start_api_server_macos.sh
```

(See [`setup-and-preflight.md`](setup-and-preflight.md) for how `ACE_STEP_PATH` is determined.)

**Generation (3-step async):**

```bash
# 1. Submit task
TASK_ID=$(curl -s -X POST http://127.0.0.1:8001/release_task \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<detailed caption, e.g.: dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bass, neon night-drive mood>",
    "lyrics": "[Verse]\n<lyrics here>\n\n[Chorus]\n<lyrics here>",
    "audio_duration": 210,
    "bpm": 96,
    "key_scale": "D major",
    "time_signature": "4/4",
    "vocal_language": "en",
    "thinking": true,
    "inference_steps": 8,
    "guidance_scale": 7.0
  }' | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('task_id',''))")

# 2. Poll for completion. Treat empty `data` as pending, not failed.
# Wait, then check:
curl -s -X POST http://127.0.0.1:8001/query_result \
  -H "Content-Type: application/json" \
  -d "{\"task_ids\": [\"$TASK_ID\"]}"

# 3. Copy audio from cache dir when done
# Files saved to: ${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/
```

**Polling caveat:** The `/query_result` endpoint may return `{"data": [], "code": 200}` even while the task is actively running. This is a known server-side quirk. Don't treat empty data as "task failed" — instead, check for new MP3 files in the cache directory, or look at the server log (`/tmp/acestep-api.log`) for actual progress markers (e.g. `MLX DiT diffusion: 24/50`). If available, use `scripts/wait_for_acestep.py` because it reconciles `/query_result` with cache-file detection.

**Stats caveat:** `GET /v1/stats` exposes top-level state such as queued,
running, succeeded, failed, `queue_size`, and `avg_job_seconds`. It does not
show current sub-stage progress. For long jobs, use `/tmp/acestep-api.log` as
the source of truth for LM, DiT, CFG, and VAE progress.

**Cache caveat:** generated audio accumulates under
`${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/`. Review old files before
deleting them:

```bash
find "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  -type f -name '*.mp3' -mtime +7 -print
```

Replace `-print` with `-delete` only after confirming the files are no longer
needed.

**Cancel caveat:** there is no documented cancel endpoint for a queued or
running local job. Lint prompt, lyrics, duration, and metas before submitting.

For a JSON-safe direct submission template, see
[`local-ace-step-curl-template.md`](local-ace-step-curl-template.md). For the
M1 -> wait -> collect -> M2 pattern, see
[`wait-and-collect.md`](wait-and-collect.md).

**Prompt format:** Prefer a **detailed, multi-dimensional caption** — ACE-Step's own docs call the caption "the most important factor affecting generated music", and the project's example prompts are rich 1–3 sentence descriptions, not bare tags. Cover, in order: **genre, key instruments, vocal character, mood, and production/texture** words. A short 2–6 word tag still works (and the LM expands it when `thinking=true`), but specificity measurably improves results. The earlier "keep it to short tags" advice was wrong for ACE-Step 1.5.

Two rules that matter:
- **Resolve style conflicts temporally, don't stack them.** The model handles "starts soft strings, builds to driving synth-rock, ends ambient" far better than "classical + hardcore metal" jammed into one static caption.
- **Keep the caption consistent with the lyrics' section tags** (a "solo violin, classical" caption fighting a `[Guitar Solo - distorted]` tag degrades output).

## Full-song generation workflow (3:30 default)

The default `audio_duration` is **210s (3:30)** — the typical user expectation for a "song". Use 210s as the reference default only when the user has not specified a target length and no source-duration expectation needs to be matched. If source audio exists, confirm the target output length before submission rather than assuming the 210s default.

**Inputs to prepare (set up once, reuse for every song):**
1. **Lyrics** — write or obtain the full song lyrics with `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Verse 2]`, `[Bridge]`, `[Outro]` tags. ~150-200 words fits a 3:30 song comfortably.
2. **Detailed caption** — see "Prompt format" above. ~500-1000 chars covering genre, instruments, vocal character, mood, production, emotional arc, and avoid list.
3. **The 6 metas** — fill in `bpm`, `key_scale`, `time_signature`, `vocal_language`, `audio_duration: 210`, plus the prompt and lyrics.

**Request body template for a full song (copy/paste and fill in):**

```bash
TASK_ID=$(curl -s -X POST http://127.0.0.1:8001/release_task \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<your detailed multi-dimensional caption here>",
    "lyrics": "[Verse 1]\n<line>\n<line>\n\n[Pre-Chorus]\n<line>\n<line>\n\n[Chorus]\n<line>\n<line>\n\n[Verse 2]\n<line>\n<line>\n\n[Bridge]\n<line>\n<line>\n\n[Outro]\n<line>\n<line>\n",
    "audio_duration": 210,
    "bpm": 96,
    "key_scale": "D major",
    "time_signature": "4/4",
    "vocal_language": "en",
    "thinking": true,
    "inference_steps": 8,
    "guidance_scale": 7.0
  }' | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('task_id',''))")
```

**Expected wall-clock on M3 24GB (standard tier, 2B turbo, 8 steps):**
- LM thinking: ~6s (1.7B model, ~50 tok/s)
- DiT diffusion: ~4-6 min (scales linearly with audio length)
- VAE decode: ~40s
- **Total: ~5-7 min per 3:30 song**

Save each reference output in a per-song folder such as `~/Music mix/<project>/<song-slug>/M1_<style>_ACE_210s.mp3`. A good reference run uses `audio_duration: 210`, the detailed prompt format, and the standard tier. If your output sounds comparable (or better), the workflow is working.

**If you only have a 60-second subset of lyrics** (e.g. a hook for a jingle, or a single chorus to test the prompt), set `audio_duration: 60` — that's perfectly fine, just not a full song. Use the full-lyrics version for the final generation.

```
# Good (detailed, multi-dimensional — matches ACE-Step's own examples)
"A groovy funk track with slap bass, tight horn stabs, rhythmic guitar scratching, a charismatic male lead with call-and-response backing vocals, and an irresistible pocket groove"
"Dreamy 80s synthwave: warm analog synths, gated-reverb drums, arpeggiated bassline, shimmering pads, nostalgic neon night-drive mood"

# Also fine (short tag; LM expands it with thinking=true)
"dreamy synthwave, 80s retro, atmospheric pads"

# Avoid: contradictory styles stacked in one static caption (express as evolution instead)
"classical chamber strings AND crushing hardcore metal AND lo-fi hip-hop, all at once"
```

**Parameters:**

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `prompt` | string | required | **Detailed caption preferred** (genre + instruments + vocal character + mood + production), per ACE-Step's docs and example prompts. A short tag also works and is expanded by the LM when `thinking=true`. Resolve style conflicts temporally rather than stacking them. |
| `lyrics` | string | optional | `[Verse]`/`[Chorus]` tagged lyrics |
| `audio_duration` | int | **210** | **10–600s.** **Default: 210s (3:30)** for full songs — this is the typical user expectation and matches the reference workflow using `~/Music mix/<project>/<song-slug>/M1_<style>_ACE_210s.mp3`. Set to fit ALL lyrics (see Duration Guide below). Use shorter values (30–60s) only for jingles, hooks, or test drafts. |
| `thinking` | bool | false | LM rewrites tags → richer caption. **Always use `true`** for best results. Field note: one request may save two cache files (primary + variant), so collect and label both when present. |
| `use_format` | bool | false | When true, the LM also enhances your caption/lyrics (similar to `thinking` but for prompt enrichment). Try `true` if the LM seems to be missing context from your prompt. |
| `inference_steps` | int | 8 | Diffusion steps. For **`acestep-v15-turbo` (standard)**: 8 is the documented setting, do not exceed 20. For **`acestep-v15-xl-sft` (xl-mixed)**: 32-64 recommended, default 50. Using 8 with xl-sft produces "soup" output (all elements at same level, no dynamics). |
| `guidance_scale` | float | 7.0 | Higher = stricter prompt adherence. **Only effective for base/sft models**, not turbo. For `xl-sft`, try 4.0-7.0 range. |
| `shift` | float | 3.0 | Timestep shift factor (1.0-5.0). **Officially documented as "only effective for base models, not turbo models"** — but xl-sft is an SFT model, not turbo. Experiment with 1.0 or 5.0 if the default sounds off. |
| `infer_method` | string | "ode" | Diffusion inference method. `"ode"` (Euler, faster) or `"sde"` (stochastic, sometimes more stable for SFT models). |
| `seed` | int | -1 | -1 = random. Set for reproducibility |
| `vocal_language` | string | "en" | BCP-47 language code for vocals. Important for non-English songs — the model picks the right phoneme set. |
| `bpm` | int | none | Optional. When `thinking=true` and missing, the LM infers it. Set explicitly for tighter control. |
| `key_scale` | string | "" | Optional. E.g. "D major", "A minor". Same as `bpm`. |
| `time_signature` | string | "" | Optional. E.g. "4/4", "3/4". Same as `bpm`. |
| `cfg_interval_start` | float | 0.0 | CFG application start ratio (0.0-1.0). Default applies CFG throughout the diffusion. |
| `cfg_interval_end` | float | 1.0 | CFG application end ratio (0.0-1.0). |
| `use_adg` | bool | false | Adaptive Dual Guidance. **Base model only.** Not applicable to `xl-sft`. |

**Environment variables** (set when starting the server, not in the request body):

| Env var | Default | Notes |
|---|---|---|
| `ACESTEP_CONFIG_PATH` | `acestep-v15-turbo` | DiT model path. Set to `acestep-v15-xl-sft` for xl-mixed. |
| `ACESTEP_LM_MODEL_PATH` | `acestep-5Hz-lm-0.6B` | LM model path. Use `acestep-5Hz-lm-1.7B` for higher quality. |
| `ACESTEP_LM_BACKEND` | `vllm` | Backend for the LM. **On Apple Silicon (macOS), set to `mlx`** for native acceleration. vLLM is meant for Linux+CUDA. |
| `ACESTEP_GENERATION_TIMEOUT` | 600 | Per-generation timeout in seconds. **Set to `3600` (1 hour) when using xl-mixed on 24GB M3** — default 600s fires mid-generation. |
| `ACESTEP_OFFLOAD_TO_CPU` | false | Set to `true` for low-VRAM environments to support longer audio generation. |
| `PYTORCH_MPS_HIGH_WATERMARK_RATIO` | ~0.4 | **On macOS, set to `0.0`** to allow XL model to load (MPS otherwise enforces a tight memory cap that fails to load the 4B DiT). |
| `ACESTEP_CONFIG_PATH2`, `ACESTEP_CONFIG_PATH3` | empty | Optional secondary DiT models selectable via the `model` parameter in requests. |

**Duration Guide (audio_duration):**

The `audio_duration` parameter controls how much audio ACE-Step generates. If it's too short, lyrics get cut off. Estimate based on lyrics word count:

| Lyrics length | Words | Recommended `audio_duration` | Real-world length |
|---|---|---|---|
| Short (jingle, hook) | <50 | 30–60 | 0:30–1:00 |
| Single verse + chorus | 50–100 | 60–120 | 1:00–2:00 |
| Full song (2 verses, chorus, bridge) | 100–200 | 180–240 | 3:00–4:00 |
| Extended (3+ verses, long outro) | 200–350 | 240–360 | 4:00–6:00 |
| Epic (ballad, progressive) | 350+ | 360–600 | 6:00–10:00 |

**Rule of thumb:** Count lyrics words × 0.8–1.2 seconds per word, then add 20% for instrumental breaks between sections. Always round UP — ACE-Step will fade out naturally if lyrics end before duration.

**Lyrics format:** Use `[Verse 1]`, `[Chorus]`, `[Bridge]`, `[Outro]` tags. ACE-Step follows these to create song structure. Add `[Intro]` and `[Instrumental Break]` tags for non-vocal sections.

**M3 performance (tested, real-world verified June 2026):**

For 60s audio (standard tier, 2B turbo, 1.7B LM, 8 steps):
- LM thinking: ~12s (1.7B MLX model, ~50 tok/s)
- DiT diffusion: ~50s (8 steps × ~6s)
- VAE decode: ~28s
- **Total: ~3.5 min per track**

For 210s audio (3:30 song, same tier):
- DiT diffusion: ~4-5 min (scales linearly with audio length, ~3x more diffusion work)
- VAE decode: ~40s
- **Total: ~5-7 min per track**

Additional field timings from the 2026-06-12 9-song run on M3 24 GB,
standard tier, 8 steps:

| Requested duration | Typical wall time |
|---|---|
| 159-200 s | about 9-10 min |
| 239 s | about 12 min |
| 302 s | about 14-15 min |

First run adds ~90s for model loading. Subsequent runs are faster because the model stays in MPS memory.

**Key advantages over MusicGen:**
- Real vocals with accurate lyrics
- Song structure follows `[Verse]`/`[Chorus]` tags
- Up to 10 minutes (600s) — long enough for full songs
- MLX native on Apple Silicon (no conda needed)
- 48kHz stereo output

## ACE-Step Quality Tiers (memory-safe selection)

**TL;DR:** `fast` = quick drafts; `standard` = daily driver (default, ~10 min/210s); `xl-mixed` = best quality but slow on 24GB M3 (~3–4 h/210s, requires extended timeout). Never auto-download; check ML budget first.

ACE-Step supports multiple model sizes with different quality/speed/RAM trade-offs. The skill must check available RAM before offering any tier and NEVER auto-download models.

**Tier table:**

| Tier | DiT Model | LM Model | Peak RAM | Disk cost | Speed (210s) | Quality | When to use |
|---|---|---|---|---|---|---|---|
| **fast** | `v15-turbo` (2B) | `5Hz-lm-0.6B` (0.6B) | ~8 GB | Included in base ~10 GB | ~5 min | Good | Quick drafts, low-RAM machines |
| **standard** (default) | `v15-turbo` (2B) | `5Hz-lm-1.7B` (1.7B) | ~11 GB | Included in base ~10 GB | ~10 min | Very Good | Daily driver, most users |
| **xl-mixed** (24GB M3: viable with extended timeout) | `v15-xl-sft` (4B) | `5Hz-lm-1.7B` (1.7B) | ~25-30 GB | +~20 GB XL DiT download | **~52 min for 60s audio (verified); ~3-4 hours for 210s** | Very High+ | Final production on any RAM tier — just slow on 24GB |

> **Real-world hardware limits (verified June 2026 on M3 24GB unified memory):**
> - The `best` tier (4B XL + 4B LM, ~22 GB peak) requires ≥32 GB RAM. NOT offered on 24 GB systems.
> - The `xl-mixed` tier (4B DiT + 1.7B LM) **IS viable on 24 GB M3** if you extend the server timeout:
>   - Model loads successfully (~10 GB DiT, but MPS pool pressure ~20 GB with cached state)
>   - 50-step diffusion runs at ~50-100s/step (varies with audio length and memory pressure)
>   - **The default 600s server timeout fires mid-generation.** Set `ACESTEP_GENERATION_TIMEOUT=3600` to allow up to 1 hour per generation.
>   - Free RAM goes to 0 GB during generation, but it works
>   - **Verified June 2026: 60s audio at 50 steps = ~52 min wall-clock on 24GB M3**
> - **Recommendation for 24 GB M3 (unified memory):**
>   - For fast iterations: use `standard` tier (10 min for 210s, fast feedback)
>   - For final production: use `xl-mixed` tier with extended timeout (52 min for 60s, or ~3-4 hours for 210s)
> - **Recommendation for 32 GB+ M3/M4 (unified memory, more headroom):** `xl-mixed` runs in ~15 min as documented. `best` tier becomes viable.
> - **For dedicated GPU (NVIDIA/AMD, system RAM separate from VRAM):** A 12 GB GPU + 16 GB system can run xl-mixed in ~15 min. The probe script auto-detects this and uses the smaller pool.

**Memory safety check (run BEFORE any generation):**

The memory probe must distinguish **unified memory** (Apple Silicon, integrated graphics) from **dedicated memory** (discrete NVIDIA/AMD GPU). On unified memory, the OS, your apps, and the ML model all share the same pool — so 24 GB total might mean only ~18 GB is actually available for ML after macOS and your open apps. On dedicated GPUs, the VRAM is separate from system RAM, so a 12 GB GPU can run a 10 GB model even on a 16 GB system.

```bash
# 1. Total system RAM and current free
case "$(uname -s)" in
  Darwin)
    TOTAL_RAM_GB=$(sysctl -n hw.memsize | awk '{printf "%.0f", $1/1024/1024/1024}')
    FREE_RAM_KB=$(vm_stat | awk '/free page count/{print $3 * 4}')
    FREE_RAM_GB=$(awk "BEGIN {printf \"%.1f\", $FREE_RAM_KB/1024/1024}")
    ;;
  Linux)
    TOTAL_RAM_GB=$(awk '/MemTotal/{printf "%.0f", $2/1024/1024}' /proc/meminfo)
    FREE_RAM_GB=$(awk '/MemAvailable/{printf "%.1f", $2/1024/1024}' /proc/meminfo)
    ;;
  *) echo "unknown" ;;
esac
echo "Total RAM: ${TOTAL_RAM_GB} GB"
echo "Free RAM now: ${FREE_RAM_GB} GB"

# 2. Memory architecture detection
if [ "$(uname -m)" = "arm64" ] && [ "$(uname -s)" = "Darwin" ]; then
  MEM_ARCH="unified"
  echo "Architecture: unified (Apple Silicon — GPU shares with system)"
elif command -v nvidia-smi >/dev/null 2>&1; then
  GPU_VRAM_GB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1 | awk '{printf "%.0f", $1/1024}')
  GPU_FREE_GB=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1 | awk '{printf "%.0f", $1/1024}')
  echo "GPU: NVIDIA (${GPU_VRAM_GB} GB total VRAM, ${GPU_FREE_GB} GB free)"
  echo "Architecture: dedicated (system RAM and VRAM are separate pools)"
  MEM_ARCH="dedicated"
elif command -v rocm-smi >/dev/null 2>&1; then
  echo "Architecture: dedicated (AMD ROCm)"
  MEM_ARCH="dedicated"
else
  echo "Architecture: integrated/CPU-only (system RAM used for everything)"
  MEM_ARCH="unified"
fi

# 3. ML budget calculation
# Unified: free RAM minus safety margin (OS can reclaim 1-2 GB more on demand)
# Dedicated: use the SMALLER of free RAM or free VRAM (the bottleneck)
# Reserve 2 GB safety margin for OS/other apps
if [ "$MEM_ARCH" = "unified" ]; then
  ML_BUDGET_GB=$(awk "BEGIN {printf \"%.0f\", $FREE_RAM_GB - 2}")
  echo "ML budget: ~${ML_BUDGET_GB} GB (free RAM minus OS safety margin)"
else
  # Dedicated GPU: bottleneck is the smaller pool
  BOTTLENECK_GB=$FREE_RAM_GB
  if [ -n "$GPU_FREE_GB" ] && [ "$GPU_FREE_GB" -lt "$BOTTLENECK_GB" ]; then
    BOTTLENECK_GB=$GPU_FREE_GB
  fi
  ML_BUDGET_GB=$(awk "BEGIN {printf \"%.0f\", $BOTTLENECK_GB - 2}")
  echo "ML budget: ~${ML_BUDGET_GB} GB (smaller of free system RAM or free VRAM, minus safety margin)"
fi
```

Based on ML budget (NOT total RAM):

| ML budget | Available tiers | Use case |
|---|---|---|
| < 8 GB | fast only (warn user about tight fit, expect OOM) | Quick drafts |
| 8–11 GB | fast + standard | Daily driver |
| 12–20 GB | fast + standard + xl-mixed (with extended timeout) | Final production |
| ≥ 25 GB | ALL tiers including best (4B LM) | No constraints |

**Why this differs from "total RAM" tables:**

A 24 GB Apple Silicon Mac with macOS and 4 GB of open apps has only ~18 GB ML budget. The probe should report 18 GB, and the table should classify it as "fast + standard" — NOT "xl-mixed eligible" (which the old table would say based on 24 GB total).

Conversely, a Windows desktop with 16 GB system RAM and a 24 GB NVIDIA RTX 4090 has 22 GB ML budget (the VRAM is the bottleneck, not the system RAM). That system CAN run xl-mixed in ~15 min as documented.

The probe and the table together handle both cases correctly. The previous version of this skill used total RAM as the gating value, which was wrong for unified memory — leading to the "24GB Mac but xl-mixed sounds bad" surprise we hit in June 2026. The fix is to use ML budget (free memory minus OS safety margin, with unified-vs-dedicated awareness).

**Model download consent flow (NEVER auto-download):**

When ACE-Step is running but no models are loaded (fresh install), OR when the user requests a higher tier whose models aren't downloaded yet:

```
You: "ACE-Step is ready but needs audio models before generating. This will
       download ~10 GB to your disk — I will NOT do this without your explicit
       approval.
       
       Your options:
       
       ① Download standard (~10 GB) → good quality, ~10 min/track, fits your {N}GB RAM ✓
       ② Download xl-mixed (+20 GB extra = ~30 GB total) → best quality your machine can run,
          ~15 min/track, needs you to close heavy apps during generation
       ③ Skip local → use a cloud backend instead
          - MiniMax (if API key set) — fast, paid
          - Stable Audio (if STABILITY_API_KEY set) — paid
          - MusicGen (local fallback) — free, instrumental only
       
       You currently have {X} GB free disk space.
       
       Which option?"
```

**Wait for the user to choose before doing anything.** Do not download. Do not auto-load. Do not start generating.

Rules:
- Always show: model size, free disk space, free RAM, expected speed, what the user gets
- If disk space < model size: offer to free space first, or skip to cloud
- If RAM < tier requirement: warn clearly, suggest lower tier or cloud
- User can change tier later without re-downloading (just switch via `/v1/init`)
- Once models are downloaded, they persist — no need to ask again unless user wants to upgrade tier

**Switching tiers mid-session:**

```bash
# Switch to xl-mixed (requires XL model already downloaded)
curl -s -X POST http://127.0.0.1:8001/v1/init \
  -H "Content-Type: application/json" \
  -d '{"dit_model": "acestep-v15-xl-sft", "lm_model": "acestep-5Hz-lm-1.7B"}'

# Switch back to standard
curl -s -X POST http://127.0.0.1:8001/v1/init \
  -H "Content-Type: application/json" \
  -d '{"dit_model": "acestep-v15-turbo", "lm_model": "acestep-5Hz-lm-1.7B"}'
```

**M3 performance by tier (real-world verified, June 2026):**

| Tier | LM time | DiT time (8 steps) | DiT time (50 steps) | VAE decode | First run | Subsequent | Status on 24GB M3 |
|---|---|---|---|---|---|---|---|
| fast (2B+0.6B) | ~6s | ~45s | n/a (model is turbo) | ~28s | ~3 min | ~5 min | ✅ Works great |
| standard (2B+1.7B) | ~12s | ~50s | n/a (model is turbo) | ~28s | ~3 min | ~10 min | ✅ Works great (default) |
| xl-mixed (4B+1.7B) | ~12s | ~720s (90s/step × 8) | **~1500s for 60s audio (~50s/step × 30+ steps in 30 min) — verified ~52 min wall-clock** | ~65s | ~5 min | **~52 min for 60s; estimated 3-4 hours for 210s** | ✅ Works with `ACESTEP_GENERATION_TIMEOUT=3600` (1 hour). 8-step version produces "soup" output — use 50 steps. |
| best (4B+4B) | n/a | n/a | n/a | n/a | n/a | n/a | ❌ Excluded — needs 32GB+ |

**Critical findings from real-world testing (June 2026):**

1. **xl-mixed CAN RUN on 24 GB M3** (verified 60s audio at 50 steps completes in ~52 min) with the right env vars:
   ```bash
   ACESTEP_CONFIG_PATH=acestep-v15-xl-sft \
   ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B \
   ACESTEP_GENERATION_TIMEOUT=3600 \
   PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 \
   uv run acestep-api --port 8001
   ```
   - Without `ACESTEP_GENERATION_TIMEOUT=3600`, the default 600s (10 min) timeout fires mid-generation
   - Without `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`, the model fails to load (MPS OOM)
   - **⚠️ Generation completes but audio quality is poor** — high-frequency noise, unclear vocals, "no sense samples". Use standard tier for now; xl-mixed needs further tuning (see the "XL 50-step fixes to try" section below).

2. **XL + 8 steps produces "soup" output** — all elements at the same level, no dynamics. Always use 50 steps for XL.
   - Verified: LRA of XL+8 steps = 1.8-4.8 LU (very compressed)
   - Verified: LRA of XL+50 steps = 4.0+ LU (more dynamic)
   - 60s XL+50 step audio on 24GB M3 = ~52 min wall-clock

3. **Audio length affects time per step:**
   - 60s audio: ~50-100s/step
   - 210s audio: ~90-130s/step (more diffusion work per step)
   - For 210s at 50 steps: 90s × 50 = 75 min minimum, up to 3-4 hours with swap pressure

4. **Memory pressure is the bottleneck, not model loading.** Models load fine; generation just runs slow due to swap-thrashing.

**XL 50-step fixes to try** (in order of likelihood, each test takes ~52 min for 60s audio):

If you want to experiment with xl-mixed anyway, the most likely fixes are:

1. **Detailed prompt with all 6 metas** (BPM, key, time signature, vocal language, duration, genre filled explicitly in the request body) — the LM benefits from explicit anchors rather than just genre tags
2. **Add `use_format: true`** — lets the LM enhance your prompt
3. **Try `shift: 1.0` or `shift: 5.0`** (default is 3.0, officially documented for "base models, not turbo" — xl-sft is SFT, not turbo, so worth experimenting)
4. **Try `guidance_scale: 4.0`** (default 7.0 may be too aggressive for sft CFG)
5. **Try `infer_method: "sde"`** (stochastic, sometimes more stable than Euler for SFT models)
6. **Try `thinking: false`** (DiT-only mode, skips LM) — if this works, the LM is the problem; if it still sounds bad, the DiT is the problem
7. **Try `xl-turbo` instead of `xl-sft`** (counterintuitive but turbo is designed for fewer steps)

Start with #1 (free, just data change) and work down. If none of these produce acceptable audio, fall back to the standard tier.

**Conclusion:** `standard` is the practical best quality tier for 24 GB M3. Reserve `xl-mixed` for 32GB+ hardware (M3 Max/Ultra, M4 Max).

## ACE-Step Audio-Conditioned Generation (Cover, Repaint, Reference Audio)

Beyond text2music, ACE-Step 1.5 conditions on an input audio file. This is how you do a
**melody-aware local cover** — no cloud needed. Select the mode with `task_type` in the
`/release_task` body:

| `task_type` | What it does | Audio field |
|---|---|---|
| `text2music` (default) | Generate from caption + lyrics | none |
| `cover` | Re-style a song while following its melody/structure | `src_audio` |
| `repaint` | Regenerate only a time window, keep the rest | `src_audio` + `repainting_start/end` |
| `extract` | Stem separation | `src_audio` |

**Uploading the source audio (important):** the API **rejects absolute file paths**
(`{"detail":"absolute audio file paths are not allowed"}`). Upload the file as multipart
form-data, not JSON. Fields: `src_audio` (source for cover/repaint) or
`reference_audio`/`ref_audio` (style-transfer reference). Send other params as form fields:

```bash
curl -s -X POST http://127.0.0.1:8001/release_task \
  -F "task_type=cover" \
  -F "src_audio=@/path/to/song.wav" \
  -F "audio_cover_strength=0.35" \
  -F "prompt=dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bass, neon night-drive mood" \
  -F "bpm=129" -F "key_scale=D major" -F "audio_format=wav"
```

**Cover behavior (verified):**
- `audio_cover_strength` (0.0–1.0): **lower = bigger restyle** (~0.2–0.4 for a strong genre jump
  like rock to synthwave; 0.7–0.9 for a subtle restyle; 1.0 = closest to source).
- The **LM is skipped** for cover/repaint/extract — `thinking` has no effect; the caption and
  lyrics you send are used directly, so write a good caption.
- **Duration auto-locks to the source length** — `audio_duration` is ignored for cover.
- `reference_audio` (style transfer) conditions global timbre/feel, NOT melody; `src_audio`
  (cover) follows melody/structure. Melody capture is best on sparse, mid/slow-tempo songs —
  expect *melodic variation*, not an exact copy.

**VRAM / time caveat (verified on a 12 GB laptop GPU):** a full ~5-minute cover is impractical
on this class of hardware — encoding the source alone took ~13 minutes and the job hit the
server's **default 600 s generation timeout** and failed. Mitigations:
- **Cover a shorter segment** — trim the source first: `ffmpeg -ss <start> -t 60 -i in.wav out.wav`.
- **Raise the timeout** when starting the server: `ACESTEP_GENERATION_TIMEOUT=3600`.
- Full-length covers are realistic on ≥20 GB VRAM.

**Routing gate:** use ACE-Step cover only when the user explicitly accepts a local,
slower, experimental workflow and the source length/hardware budget make sense.
Use `music-craft-minimax` for fast cloud cover, long-source turnaround, mashups,
or when the user needs MiniMax-native controls and analysis scripts.

**Repaint** (fix one bad section instead of regenerating the whole track): `task_type=repaint`,
upload `src_audio`, set `repainting_start`/`repainting_end` (seconds) and `repaint_mode`
(`conservative`/`balanced`/`aggressive`) with `repaint_strength` (0–1). Use your structural
analysis to choose the window.

**Stem/remix helper path:** ACE-Step `extract` is experimental. For local arranger
experiments, prefer `scripts/extract_stems.py` when Demucs is installed; it writes
`stems.json` with normalized `vocals`, `drums`, `bass`, and `other` paths. Then
use `scripts/remix_stems.py --stems-json <stems.json> --output <mix.mp3> --dry-run`
to inspect the preview-quality `ffmpeg amix` command before rendering. This is
not DAW-quality mixing.

**Local audio understanding (no cloud):** ACE-Step can extract BPM, key, time-signature, and a
caption directly from an input file (the `analysis_only` / `full_analysis_only` request flags;
the "Audio Understanding" feature). This is a fully-local way to derive metas/caption from a
source song — an alternative to the librosa pipeline when ACE-Step is already running.

**Operational note (single-worker API):** the REST server processes one job at a time and may
not answer `/query_result` within a short timeout while mid-generation (60 s poll timeouts are
normal under load). Use a generous client timeout, tolerate poll timeouts, and detect
completion by watching `.cache/acestep/tmp/api_audio/` for new files.

**Quality loop:** generate a small batch (`batch_size` 2–4) and keep the best; request
`audio_format: "wav"` to avoid a lossy MP3 round-trip; set `seed` with `use_random_seed=false`
for reproducibility.
