# ACE-Step XL (4B) DiT Models

Reference for the ACE-Step 1.5 XL (4B-parameter) DiT family: how the two
deployment shapes — **`xl-base`** and **`xl-mixed`** — differ, what
hardware they need, the **must-pass parameters** that silently degrade
quality if forgotten, and a decision tree for picking XL vs. the standard
2B tier. Load this when a request mentions the XL DiT, the 4B DiT,
`acestep-v15-xl-*` checkpoints, or best-quality ACE-Step music generation.

> **Terminology note.** Elsewhere in this skill (`acestep-generation.md`),
> **`xl-mixed`** refers to the *4B DiT + 1.7B LM* combo (the
> `acestep-v15-xl-sft` + `acestep-5Hz-lm-1.7B` stack). This document uses
> the stricter XL definition: **`xl-mixed` = 4B DiT + 4B LM**
> (`acestep-v15-xl-base` + `acestep-5Hz-lm-4B`, ≈22 GB peak) — i.e. the
> "best" tier from the existing tier table. The two meanings are two
> different points on the same DiT + LM curve and the footguns below
> apply to both.

## TL;DR

- **XL DiT = ~4B parameters, ~9 GB bf16 / ~11 GB on disk for the DiT
  alone** (vs. ~4.7 GB for the 2B DiT). All HF checkpoints:
  [`acestep-v15-xl-base`](https://huggingface.co/ACE-Step/acestep-v15-xl-base),
  [`acestep-v15-xl-sft`](https://huggingface.co/ACE-Step/acestep-v15-xl-sft),
  [`acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo).
- **Two deployment shapes**:
  - **`xl-base`** — XL DiT only, BASE-only training. Required for
    `extract` / `lego` / `complete` task types (the BASE-only family).
  - **`xl-mixed`** — XL DiT + 4B LM. Heavy memory and slow on consumer
    hardware, but the highest-quality path on a 32 GB+ machine.
- **Hardware floor**: ≥12 GB VRAM (with CPU offload + quantization),
  ≥20 GB VRAM recommended; **24 GB M3 is the practical reference**
  (Luis's machine).
- **Two critical footguns**, both silently degrade output if missed:
  1. **`num_inference_steps=50` MUST be passed explicitly for XL Base.**
     The Diffusers `__call__` default is 8 (turbo-equivalent), so
     leaving it unset on XL silently produces "soup" output — all
     elements at the same level, no dynamics.
  2. **`shift=3.0` is the documented default for XL Base.** Pinned
     upstream and governs structure vs. detail (NOT vocal/instrument
     separation — separation is VAE-level).

## 1. Model variants

| Variant | What it is | HF checkpoint | LM | Peak RAM (bf16) | When to reach for it |
| --- | --- | --- | --- | --- | --- |
| **`xl-base`** | 4B DiT, BASE training only | `acestep-v15-xl-base` | optional (any LM works) | ~11 GB DiT + LM | `extract` / `lego` / `complete` tasks, large-scale fine-tuning, highest-quality text-to-music when 4B LM is overkill |
| **`xl-mixed`** | 4B DiT (xl-base) **+** 4B LM (`acestep-5Hz-lm-4B`) | both | 4B LM required | ~22 GB peak | Best quality on a 32 GB+ machine. Not yet viable on 24 GB M3 |
| `xl-sft` (intermediate) | 4B DiT, SFT training | `acestep-v15-xl-sft` | optional | ~11 GB DiT + LM | The default "best quality on 24 GB M3" choice — see `acestep-generation.md` Quality Tiers |
| `xl-turbo` | 4B DiT, distilled for 8 steps | `acestep-v15-xl-turbo` | optional | ~11 GB DiT + LM | When you want XL quality at turbo speed (8 steps) on 20 GB+ GPU |

> The skill already covers `xl-sft` and `xl-turbo` as separate quality
> tiers in `acestep-generation.md`. This document focuses on the two
> end-of-spectrum deployment shapes (`xl-base`, `xl-mixed`) and the
> parameters they share.

### What "BASE-only" means for `xl-base`

`xl-base` (like `acestep-v15-base`) is the **only** ACE-Step DiT
checkpoint that supports the audio-conditioned task types `extract`,
`lego`, and `complete`. TURBO and SFT checkpoints silently fail or
refuse these tasks. See `acestep-task-types.md` for the full task matrix.

Tradeoffs of BASE-only training:

- ✅ Full CFG works (set `guidance_scale=7.0` or experiment in 4–9).
- ✅ All five audio-conditioned task types available.
- ✅ The strongest baseline for LoRA / fine-tuning runs.
- ⚠️ BASE outputs can sound "technically correct but not performed" —
  see § 5.

## 2. Hardware requirements

> The table below describes **practical** requirements based on the
> upstream README's [Model Zoo tier matrix](https://github.com/ace-step/ACE-Step-1.5/blob/main/README.md#-model-zoo).
> On Apple Silicon (unified memory), the **ML budget** (free RAM − 2 GB
> safety margin) is the bottleneck, NOT total system RAM — see
> `setup-and-preflight.md` § Memory safety check.

| Class | RAM / VRAM | `xl-base` (4B DiT only) | `xl-mixed` (4B DiT + 4B LM) |
| --- | --- | --- | --- |
| Minimum (CPU offload + quantization) | 12 GB | ✅ Loads, slow | ❌ Not enough headroom |
| Reference (24 GB M3, unified) | 24 GB | ✅ Runs but ~50–130 s/step on MPS — too slow for daily iteration | ⚠️ Viable with env vars, ~3–4 h / 210 s, poor quality on M3 as of 2026-07 (see § 7) |
| Recommended (dedicated NVIDIA RTX-class) | 20–24 GB VRAM | ✅ ~10–15 min / 210 s | ❌ Requires CPU offload |
| Comfortable (32 GB+ unified, M3 Max/Ultra / M4 Max) | 32 GB+ | ✅ Fast, ample headroom | ✅ ~15 min / 210 s as documented |
| Production GPU (A100 / H100) | 40 GB+ VRAM | ✅ Fastest | ✅ Best wall-clock |

Notes:

- **Weights size**: ~9 GB bf16 for the DiT alone (the ~11 GB disk figure
  includes optimizer / metadata). Pair with any LM (`0.6B`, `1.7B`, or
  `4B`) — LM weights are additive.
- **Apple Silicon (MPS)**: requires `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` (removes the MPS memory cap; get the user's OK first, see [`mps-bf16-acceleration.md`](mps-bf16-acceleration.md))
  on the server; otherwise MPS OOMs at DiT load. Set this in
  `start_api_server_macos.sh` or via the server env block.
- **vLLM** is the recommended LM backend on Linux+CUDA. On macOS, set
  `ACESTEP_LM_BACKEND=mlx` for native acceleration.

## 3. Required parameters (FOOTGUNS — read first)

> **Naming note**: ACE-Step exposes the same parameter under two names
> depending on the call path:
>
> - **HTTP REST API** (`/release_task`): `inference_steps`
> - **Python Diffusers class** (`pipe.__call__`): `num_inference_steps`
> Both default to **8** (turbo-equivalent), which silently regresses XL
> quality. The Diffusers path is the one used in this skill's Python
> integration. The REST path is what `acestep-api` exposes.
> All examples below use the Python/Diffusers name. Translate to
> `inference_steps` if you are talking to the HTTP API directly.

These four parameters are the difference between a clean XL render and a
silent-quality regression. Always pin them explicitly when targeting an
XL checkpoint:

| Parameter | XL Base (`xl-base`) | XL Mixed (`xl-mixed`) | Why it matters |
| --- | --- | --- | --- |
| `num_inference_steps` (Diffusers) / `inference_steps` (REST) | **`50` ⚠️ MUST pass explicitly** | **50** (32–64 acceptable) | The default is **8** (turbo-equivalent). On XL, 8 steps produces "soup" — all elements at the same level, no dynamics. Verified on 24 GB M3: 8 steps = LRA 1.8–4.8 LU (very compressed); 50 steps = 4.0+ LU (more dynamic). |
| `shift` | **`3.0`** (documented default) | **3.0** (try 1.0–5.0) | Pinned upstream for XL Base. Governs structure vs. detail — high shift = "outline first, then fill"; low shift = "draw and fix simultaneously". **Not** vocal/instrument separation (that's VAE-level). |
| `infer_method` | **`"ode"` (Euler)** is fine for XL Base | Try `"ode"` first, then `"sde"` if SFT feels unstable | `"ode"` is deterministic + faster; `"sde"` adds stochastic noise per step and can stabilize SFT-family checkpoints. |
| `guidance_scale` | **`7.0`** (Diffusers/card default) — 4.0–9.0 range | **4.0–7.0** (xl-sft is sensitive; 7.0 may be harsh) | Higher = stricter prompt adherence, but **only effective on base/sft models** (turbo ignores CFG). On XL Base, 5.0 is the softer alternative if vocals render harsh. |

### Quick parameter table — copy/paste

| Param | Value | Footgun? |
| --- | --- | --- |
| `num_inference_steps` | **`50`** | ⚠️ MUST be explicit on XL Base |
| `shift` | **`3.0`** | ⚠️ Documented default for XL Base |
| `infer_method` | `"ode"` (or `"sde"` for SFT) | — |
| `guidance_scale` | `5.0` (softer) or `7.0` (strict) | — |
| `use_adg` | `true` recommended for BASE | BASE model only |
| `cfg_interval_start` / `cfg_interval_end` | `0.0` / `1.0` (full range) | — |
| `seed` | `-1` (random) for exploration; pin for A/B | — |
| `audio_format` | `"wav"` or `"flac"` for quality work | — |

### Other parameters that "look" important but aren't

- `shift` **does NOT** control vocal/instrument separation (that's
  VAE-level). Don't tune `shift` to chase cleaner stems.
- `guidance_scale` **does NOT** apply to `xl-turbo` (turbo is trained
  without CFG). For `xl-base` and `xl-sft` it does.
- `use_adg` (Adaptive Dual Guidance) is **BASE only**. Setting it on SFT
  or turbo silently no-ops.

## 4. Quality characteristics

Field observations and the upstream maintainers' verdict, condensed:

| Axis | `xl-base` | `xl-mixed` |
| --- | --- | --- |
| Vocal alignment to lyrics | Strong (XL diagonal) | Strong + LM planning |
| Vocal performance | **"Technically correct but not performed"** — strong lyric alignment, weak verse/chorus dynamic contrast. Plan post-processing for sibilance. | Plausibly better with 4B LM planning, but no public verification yet |
| Instrument separation | VAE-level (not XL-controlled) | Same |
| Tonal/instrumental detail | Higher than 2B at equal step count | Highest available |
| Long-form coherence (210 s, 50 steps) | Acceptable; repetition risk past ~3 min | Same |
| Music theory adherence | BPM/key/time-sig respected within reason (60–180 BPM, common keys) | Same + LM-driven corrections |

> **Vocal quality caveat.** The XL Base DiT produces technically correct
> vocals — phonemes land, words are intelligible — but the *performance*
> (prosody, verse → chorus dynamic lift, emotional arc) is weaker than a
> human reference. Two mitigations: (1) write the prompt to call out the
> performance ("breathy lead vocal with rising intensity into the chorus"),
> and (2) plan a post-processing pass for sibilance (`/ess/` and `/ʃ/`
> frequencies) if the output is harsh.

## 5. Decision tree — XL vs. standard

```text
Need `extract` / `lego` / `complete` task?
├── YES → xl-base (or base, if 2B is enough)
└── NO
    ├── Need LM-driven planning (rich captions, complex briefs)?
    │   ├── On 32 GB+ hardware → xl-mixed (best quality available)
    │   └── On 24 GB M3 → xl-sft + 1.7B LM (viable, slow)
    ├── Need the fastest XL quality?
    │   └── xl-turbo (8 steps; needs ≥20 GB VRAM)
    └── Need daily-driver turnaround?
        └── standard tier (2B turbo + 1.7B LM, 5–10 min / 210 s) ✅
```

Rule of thumb: **start with `standard`, switch to XL only when**: (a) you
need BASE-only tasks, or (b) you've got ≥32 GB and can wait 15+ min per
track. XL on 24 GB M3 is verified-viable but not production-ready as of
the 2026-07 web verification.

## 6. Limitations

- **24 GB M3 is too slow for daily XL use.** 60 s audio at 50 steps =
  ~52 min wall-clock (verified June 2026); 210 s audio = 3–4 h. Use
  `standard` for iteration, XL only for the final pass.
- **`xl-mixed` requires ≥32 GB unified memory (or a ~24 GB VRAM
  GPU + ~16 GB system)**. On 24 GB M3 the 4B LM will OOM during DiT
  diffusion; on MPS the model loads but generation is dominated by
  swap pressure.
- **macOS env vars are mandatory for XL.** Without both:

  ```bash
  PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0     # 4B DiT fits in MPS pool; removes the memory cap, ask first
  ACESTEP_GENERATION_TIMEOUT=3600          # 1 h cap; default 600 s fires mid-gen
  ```

  the server either OOMs at load or times out at minute 10. See
  `setup-and-preflight.md` for the full server-start command.
- **No documented cancel endpoint.** XL generations can run for an hour
  per track — lint prompts, lyrics, and metas before submission.
- **LM is skipped for `cover` / `repaint` / `extract`.** `thinking: true`
  has no effect on those task types regardless of the DiT checkpoint.
- **Model downloads are large.** Don't auto-download — use the consent
  flow in `acestep-generation.md` § Model download consent flow.

## 7. Example commands

### 7.1 — `xl-base` text2music (Linux+CUDA, 24 GB GPU)

```bash
ACESTEP_CONFIG_PATH=acestep-v15-xl-base \
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B \
ACESTEP_LM_BACKEND=vllm \
uv run acestep-api --port 8001
```

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bassline, shimmering pads, nostalgic neon night-drive mood",
    "lyrics": "[Verse 1]\nneon lights on a vacant street\n\n[Chorus]\nwe are the night",
    "audio_duration": 210,
    "bpm": 96,
    "key_scale": "D major",
    "time_signature": "4/4",
    "vocal_language": "en",
    "thinking": true,
    "inference_steps": 50,
    "guidance_scale": 7.0,
    "shift": 3.0,
    "infer_method": "ode",
    "use_adg": true,
    "audio_format": "wav"
  }')

python3 scripts/wait_for_acestep.py "$TASK_ID" --expected-seconds <audio_duration>
# Files save to ${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/
```

### 7.2 — `xl-base` extract (BASE-only task)

```bash
# Pre-flight: switch the loaded DiT to xl-base
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-xl-base", "lm_model": "acestep-5Hz-lm-1.7B"}'

python3 scripts/acestep_request.py release_task \
  --form task_type=extract \
  --form-file src_audio=/path/to/source.wav \
  --form audio_format=wav
```

See `acestep-task-types.md` § Extract for the full parameter table and
output contract.

### 7.3 — `xl-mixed` text2music (32 GB+ M-series)

```bash
ACESTEP_CONFIG_PATH=acestep-v15-xl-base \
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-4B \
ACESTEP_LM_BACKEND=mlx \
ACESTEP_GENERATION_TIMEOUT=3600 \
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 \
uv run acestep-api --port 8001
```

Same request body as § 7.1, but expect ~15 min / 210 s on M3 Max /
Ultra or M4 Max. On 24 GB M3 the same stack will load but is **not
production-ready** — see § 6 and the web verification footnote in
`acestep-generation.md`.

### 7.4 — Switching tiers mid-session

```bash
# Switch to xl-mixed (requires XL + 4B LM downloaded)
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-xl-base", "lm_model": "acestep-5Hz-lm-4B"}'

# Switch back to standard
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-turbo", "lm_model": "acestep-5Hz-lm-1.7B"}'
```

> Switching reloads the DiT weights (~10–90 s cold start). Don't batch
> BASE-only and turbo/SFT tasks in the same minute.

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| XL generation completes but audio sounds "soupy" / no dynamics | `num_inference_steps` (Diffusers) / `inference_steps` (REST) left at default (8) | Pass `num_inference_steps=50` (Diffusers) or `"inference_steps": 50` (REST) explicitly |
| MPS OOM at DiT load on macOS | `PYTORCH_MPS_HIGH_WATERMARK_RATIO` not zeroed | Restart the server with `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`. Explain that this removes the MPS memory cap (system-wide memory pressure, heavy swap) and get the user's OK first; or switch to the standard tier. |
| Generation aborts at ~10 minutes | `ACESTEP_GENERATION_TIMEOUT` left at default 600 s | Restart server with `ACESTEP_GENERATION_TIMEOUT=3600` (1 hour) |
| `extract` / `lego` / `complete` silently fails or refuses | Loaded DiT is SFT or Turbo, not BASE | Switch via `/v1/init` to `acestep-v15-xl-base` (or `acestep-v15-base` for 2B) |
| 4B LM doesn't load on 24 GB M3 | Insufficient unified memory for 4B DiT + 4B LM stack | Drop to `xl-sft + 1.7B LM` (the skill's `xl-mixed` tier in `acestep-generation.md`); or move to 32 GB+ hardware |
| Vocals render harsh / sibilant | `guidance_scale=7.0` too aggressive on SFT, or no post-processing planned | Try `guidance_scale=5.0`; plan a de-essing post-pass on the output |
| `use_adg=True` has no effect | Loaded DiT is not BASE | Drop `use_adg` for SFT/Turbo, or switch to a BASE checkpoint |
| Long XL generation (3–4 h on 24 GB M3) hits swap | Free RAM < ~18 GB ML budget | Close other apps; or accept the wall-clock for a one-off final pass |
| XL + vLLM runs but is slow on Apple Silicon | vLLM is CUDA-only; MPS path uses MLX | Set `ACESTEP_LM_BACKEND=mlx` on macOS |
| Server boots but `/v1/init` 500s on `xl-base` | Model not downloaded or wrong HF repo | Confirm `acestep-v15-xl-base` is present in `${ACE_STEP_PATH}`; verify with `huggingface-cli scan-cache` |
| 8-step XL produces nearly identical outputs across seeds | Likely missing the 50-step footgun or seed not pinned | Pass `num_inference_steps=50` (Diffusers) / `inference_steps=50` (REST) AND pin `seed=<int>` for A/B comparison |
| `xl-mixed` loads but DiT diffusion is dominated by swap pressure | 24 GB M3 ML budget < ~25 GB | Downgrade to `xl-sft + 1.7B LM`; revisit on 32 GB+ hardware |

## 9. Sources

- `ACE-Step-1.5/README.md` § News (XL release, 2026-04-02) and § Model
  Zoo — XL DiT table and LM table.
- `ACE-Step-1.5/docs/en/INFERENCE.md` § GenerationParams and § Parameter
  tuning — shift=3.0 for "best quality", `infer_method`, `use_adg` base-only,
  `shift` only effective on base models.
- `ACE-Step-1.5/docs/en/Tutorial.md` § DiT Models — `xl-base`/`xl-sft`/
  `xl-turbo` selection table, LM (0.6B/1.7B/4B) compatibility statement,
  ≥12 GB / ≥20 GB hardware notes.
- `music-craft-ENHANCEMENT-PLAN.md` § Capability table — XL (4B) DiT
  documentation scope, ~11 GB DiT weight figure.
- `music-craft_ROADMAP.md` item 13d — `num_inference_steps=50` footgun,
  `shift=3.0` pinning, "vocal quality: technically correct but not
  performed" verdict.
- `music-craft_ROADMAP.md` item 13i — shift-schedule taxonomy across tiers.
- `references/acestep-generation.md` § Quality Tiers — real-world 24 GB
  M3 timings, ML-budget tier table, env-var reference.
- `references/acestep-task-types.md` — BASE-only task support matrix and
  `/v1/init` switching pattern.
- `references/setup-and-preflight.md` § User & Hardware Setup — ML
  budget probe, unified-vs-dedicated memory detection, macOS env-var
  reminder.
