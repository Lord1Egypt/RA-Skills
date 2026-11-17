# ACE-Step Shift Schedule Taxonomy

Reference for the ACE-Step 1.5 **shift** parameter: what it controls in the
flow-matching diffusion process, how the three documented schedules
(`shift=1.0`, `shift=3.0`, and **continuous shift**) map to each model tier
(turbo, base, sft, xl-base, xl-mixed), and how to pick the right shift for
the request at hand. Load this when a request mentions `shift`,
timestep-shifting, or any of the four turbo variants (`turbo`,
`turbo-shift1`, `turbo-shift3`, `turbo-continuous`).

> **Status:** docs-only. Backed by `music-craft_ROADMAP.md` item **13i** and
> verified upstream against `ACE-Step-1.5/docs/en/INFERENCE.md` +
> `Tutorial.md`. No runtime changes; if the upstream semantics shift
> (e.g. a new default), update § 1 first.

## TL;DR

- **`shift` is a timestep-reshaping factor in flow-matching diffusion.**
  When `shift != 1.0`, the scheduler applies
  `t' = shift * t / (1 + (shift - 1) * t)` to every timestep `t` before
  the step. Higher `shift` = the early (high-noise, structure-defining)
  timesteps get **more compute**, low-noise detail timesteps get **less**.
- **Three documented schedules:**
  - `shift=1.0` — **default in the upstream `GenerationParams`**. Flat
    schedule; the original cosine/linear timesteps are untouched. Pairs
    with turbo's few-step (8) inference.
  - `shift=3.0` — **documented default for base / sft / xl-base / xl-sft
    checkpoints** (per upstream Tutorial + INFERENCE.md). Steep schedule;
    more effort on structure, less on micro-detail. The "best quality"
    default in upstream docs.
  - **continuous shift** — a time-varying schedule where the shift
    factor changes across timesteps instead of staying constant.
    Available in the `turbo-continuous` checkpoint (experimental) and
    as a research lever on custom flow-matching pipelines.
- **Tier-to-shift mapping:**

  | Tier | Default shift | Notes |
  | --- | --- | --- |
  | `turbo` (2B, 8 steps) | `1.0` (joint-distilled 1/2/3) | Most flexible; works at any shift in 1.0–5.0 |
  | `turbo-shift1` | `1.0` | Distilled only at shift=1; richer details, weaker semantics |
  | `turbo-shift3` | `3.0` | Distilled only at shift=3; clearer, drier, less orchestration |
  | `turbo-continuous` | continuous (1–5) | Experimental; not thoroughly tested upstream |
  | `base` / `xl-base` | `3.0` | Recommended; try `1.0` or `5.0` if defaults feel off |
  | `sft` / `xl-sft` | `3.0` (experiment 1.0–5.0) | SFT is not strictly turbo; shift is **applicable** |
  | `xl-mixed` (4B DiT + LM) | `3.0` | Inherits XL DiT default; same `1.0–5.0` envelope |

## 1. What `shift` controls

### 1.1 The formula

When `shift != 1.0`, the scheduler runs the standard timestep list
through:

```
t' = shift * t / (1 + (shift - 1) * t)
```

with `t` in `[0.0, 1.0]`. The transformation is monotonic; it just
**stretches or compresses** the noise schedule. The shape of the
denoising trajectory changes — early (high-noise) steps get a bigger
share of the step budget, or a smaller share, depending on `shift`.

### 1.2 Plain-language effect

Upstream `Tutorial.md` describes it as "attention allocation" during
denoising. The mental model:

| Shift value | Step allocation | Sound character |
| --- | --- | --- |
| **Lower** (`shift ≈ 1.0`) | Evenly distributed. Roughly equal compute per timestep. | "Draw and fix simultaneously." More micro-detail; risk of noisy detail. |
| **Higher** (`shift ≈ 3.0`) | Front-loaded. Early (high-noise, structure-defining) timesteps get more compute; late (low-noise, fine-detail) timesteps get less. | "Draw outline first, then fill." Stronger semantics, cleaner overall framework, potentially drier arrangement. |

**What `shift` is NOT:**

- **Not a vocal/instrument separation knob.** Stem separation lives in
  the VAE; tuning `shift` will not change how cleanly the model pulls
  vocals out of the mix.
- **Not a prompt-adherence knob.** That's `guidance_scale` (CFG).
- **Not a speed knob.** `shift` reshapes the schedule but does not add
  or remove steps. Wall-clock per step is the same; total wall-clock
  changes only because the model may converge differently.

### 1.3 The upstream documentation nuance

Upstream `INFERENCE.md` says the parameter is "**only effective for
base models, not turbo models**" — the SDK doc was written before the
shift-distilled turbo variants (`turbo-shift1`, `turbo-shift3`,
`turbo-continuous`) shipped. Read that line as "the **shift-aware
behavior** is best understood on base models; turbo models are
sensitive in different ways". In practice:

- `turbo` (default, joint-distilled 1/2/3) **accepts any `shift` in
  `1.0–5.0` without complaint**; the effect is muted because the model
  was distilled on three different schedules and learned to handle all
  of them.
- `turbo-shift1` is **biased toward `shift=1.0`**; values far from 1.0
  hurt quality.
- `turbo-shift3` is **biased toward `shift=3.0`**; values far from 3.0
  hurt quality.
- `turbo-continuous` **expects a continuous schedule** (1.0 → 5.0
  across the run), not a constant.
- `base` / `sft` / `xl-base` / `xl-sft` — `shift` is **fully effective**
  and is the standard knob to tune.

## 2. Shift variants

### 2.1 `shift=1.0` — flat schedule (turbo default)

```python
GenerationParams(
    caption="upbeat electronic dance music",
    inference_steps=8,
    shift=1.0,
    infer_method="ode",
)
```

- **What it does:** the noise schedule is **unchanged**. The denoising
  trajectory is the unmodified upstream default (typically a linear or
  cosine schedule from `t=1.0` to `t=0.0`).
- **When to use:** default for any `*turbo` checkpoint at 8 steps.
  Pairs naturally with `turbo-shift1`'s distillation; works on the
  joint-distilled `turbo` and `xl-turbo` without complaint.
- **Pros:** safest, most predictable, no surprise side effects from
  schedule reshaping.
- **Cons:** on long-form or detail-heavy prompts the structure may feel
  under-anchored (the model spreads effort evenly, so the chorus
  doesn't stand out from the verse).

### 2.2 `shift=3.0` — steep schedule (base/sft default)

```python
GenerationParams(
    caption="intricate jazz fusion with complex harmonies",
    inference_steps=50,
    guidance_scale=7.0,
    use_adg=True,
    shift=3.0,
    seed=42,
)
```

- **What it does:** reshapes the timestep grid so the early, high-noise
  steps (where structure, melody, and section shape are decided) get
  more compute. Late, low-noise steps (where micro-detail is rendered)
  get less.
- **When to use:** the documented default for `base`, `sft`, `xl-base`,
  `xl-sft`, and `xl-mixed`. **Must be passed explicitly** in Diffusers
  and `/release_task` JSON bodies for these checkpoints — see
  [`acestep-xl-models.md`](acestep-xl-models.md) § "Required parameters
  (FOOTGUNS — read first)".
- **Pros:** strong semantic coherence, cleaner chorus-vs-verse contrast,
  better BPM / key adherence on long-form outputs.
- **Cons:** can sound "dry" or under-arranged if the model didn't have
  enough steps to spend on detail — try `shift=1.0` if 3.0 feels
  sterile.

### 2.3 Continuous shift (1.0 → 5.0 across the run)

```python
# Upstream exposes continuous shift via the turbo-continuous checkpoint
# and through the custom `timesteps` parameter on GenerationParams.
# The default API surfaces it as a list of timesteps you provide.

GenerationParams(
    caption="ambient cinematic buildup with slow crescendo",
    # Custom schedule: front-load shift=1.0 (broad strokes), then
    # ramp up to shift=5.0 (tightening detail). The list is the actual
    # timestep grid the model denoises on.
    timesteps=[0.97, 0.85, 0.70, 0.55, 0.40, 0.28, 0.18, 0.10, 0.05, 0.0],
)
```

- **What it does:** instead of a single constant `shift`, the model
  uses a **time-varying shift** so different timesteps get different
  compute treatment. Two common patterns:
  - **Front-load (broad-then-narrow):** low shift early for global
    structure, high shift late for crisp detail. Useful for ambient /
    cinematic where macro arc matters.
  - **Back-load (narrow-then-broad):** high shift early for a strong
    skeleton, low shift late for richer micro-detail. Useful for
    detail-rich genres (jazz fusion, orchestral).
- **When to use:** only on the `turbo-continuous` checkpoint, or when
  you supply a custom `timesteps` list on `GenerationParams`. Upstream
  flag: experimental; "not thoroughly tested".
- **Pros:** can outperform both `shift=1.0` and `shift=3.0` on prompts
  that need both a strong macro arc AND rich micro-detail (the
  schedule paradox that a constant shift cannot resolve).
- **Cons:** no documented "best" envelope; requires A/B testing per
  prompt; can produce inconsistent results if the schedule is
  mis-shaped.

### 2.4 Quick comparison table

| Aspect | `shift=1.0` | `shift=3.0` | continuous shift |
| --- | --- | --- | --- |
| Schedule shape | Linear / unmodified upstream | Steep; front-loaded | Variable per timestep |
| Compute on structure | Even | High | Configurable |
| Compute on detail | Even | Lower | Configurable |
| Default tier | turbo (8 steps) | base / sft / xl-* (50 steps) | turbo-continuous only |
| Sensitivity to choice | Low on joint-distilled turbo | Medium on SFT | High (per-step schedule) |
| Quality ceiling | "Good, balanced" | "Best quality" upstream default | "Highest potential, lowest reproducibility" |
| Reproducibility | High | High | Low (depends on schedule shape) |

## 3. Tier-to-shift mapping table

Comprehensive map of ACE-Step 1.5 model checkpoints to their recommended
shift schedule. Sources:
[`ACE-Step-1.5/README.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/README.md) § Model Zoo
(DiT Models / XL DiT Models), [`docs/en/Tutorial.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md) § DiT
Models, [`docs/en/INFERENCE.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md) § GenerationParams.

| Tier | HF checkpoint | Distillation config | Recommended `shift` | Acceptable range | Notes |
| --- | --- | --- | --- | --- | --- |
| **turbo (default)** | `acestep-v15-turbo` | Joint distillation on shift 1, 2, 3 | `1.0` (or omit) | `1.0`–`5.0` | Most flexible. Default for daily-driver and 8-step inference. The skill's `standard` tier uses this with `shift=1.0` (effectively omitted). |
| **turbo-shift1** | `acestep-v15-turbo-shift1` | Distilled only on shift=1 | `1.0` (strict) | `0.9`–`1.2` | Richer micro-detail, weaker semantic anchor. Best for dense arrangements where detail matters more than structure. |
| **turbo-shift3** | `acestep-v15-turbo-shift3` | Distilled only on shift=3 | `3.0` (strict) | `2.5`–`3.5` | Clearer, drier, more minimal orchestration. Best for sparse, structurally-driven music (ballads, ambient, classical). |
| **turbo-continuous** | `acestep-v15-turbo-continuous` | Experimental; supports continuous shift 1–5 | custom schedule | continuous (1.0–5.0) | Most flexible; least tested. Best for prompts that need both macro arc and micro-detail. Not recommended for production without smoke tests. |
| **xl-turbo** | `acestep-v15-xl-turbo` | Joint distillation (XL variant of default turbo) | `1.0` | `1.0`–`5.0` | Same behavior as `turbo` but on the 4B DiT. The skill's `xl-turbo` reference tier. |
| **sft** | `acestep-v15-sft` | SFT (50 steps, CFG-able) | `3.0` (try 1.0–5.0) | `1.0`–`5.0` | SFT is not turbo. The upstream "only effective for base models" line in `INFERENCE.md` predates this finding; SFT responds to shift tuning. |
| **xl-sft** | `acestep-v15-xl-sft` | SFT on 4B DiT | `3.0` (try 1.0–5.0) | `1.0`–`5.0` | The skill's `xl-mixed` reference tier. Same caveat as `sft`: shift is effective. |
| **base** | `acestep-v15-base` | BASE (50 steps, full CFG, ADG-capable) | `3.0` | `1.0`–`5.0` | BASE is the original target for `shift=3.0` upstream. Required for `extract`/`lego`/`complete`. |
| **xl-base** | `acestep-v15-xl-base` | BASE on 4B DiT | `3.0` ⚠️ MUST pass explicitly | `1.0`–`5.0` | Documented default per `INFERENCE.md` § "Advanced DiT Parameters". Pinned in [`acestep-xl-models.md`](acestep-xl-models.md) § 3. |
| **xl-mixed** | `acestep-v15-xl-base` + 4B LM | BASE + 4B LM | `3.0` | `1.0`–`5.0` | Inherits `xl-base`'s shift default. Only viable on ≥32 GB hardware (M3 Max/Ultra or 24 GB VRAM GPU + 16 GB system). |

## 4. Decision tree — which shift for this request?

```text
What's the loaded DiT checkpoint?
│
├── turbo (any variant) at 8 steps
│   │
│   ├── Default behavior needed (no specific quality axis to push)?
│   │   └── shift=1.0   # safest; what the joint-distilled checkpoint
│   │                   # was trained to handle equally well
│   │
│   ├── Need richer micro-detail (dense arrangement, electronic, dense vocal stacks)?
│   │   └── switch to turbo-shift1 checkpoint + shift=1.0
│   │       # stronger at "draw and fix simultaneously"
│   │
│   ├── Need clearer structure / drier arrangement (ballad, ambient, classical)?
│   │   └── switch to turbo-shift3 checkpoint + shift=3.0
│   │       # stronger at "outline first, fill later"
│   │
│   ├── Need both strong macro arc AND rich detail (cinematic, jazz fusion)?
│   │   └── switch to turbo-continuous + custom timesteps schedule
│   │       # experimental; smoke-test before production
│   │
│   └── Just trying things / on a budget?
│       └── shift=1.0  # don't pay the schedule-shaping tax
│
├── base / xl-base (50 steps, full CFG, BASE-only tasks)
│   ├── First attempt / unknown prompt shape?
│   │   └── shift=3.0   # the documented default; matches upstream training
│   │
│   ├── Output feels "dry" / under-arranged?
│   │   └── try shift=1.5  # ease the schedule toward even
│   │       # or shift=1.0 if 1.5 still feels under-structured
│   │
│   ├── Output feels "mushy" / detail too noisy?
│   │   └── try shift=4.5 or shift=5.0  # sharpen structure at the
│   │                                    # cost of detail
│   │
│   ├── Doing extract / lego / complete (BASE-only tasks)?
│   │   └── shift=3.0  # matches the per-task defaults in
│   │                  # acestep-task-types.md § 3-5
│   │
│   └── Fine-tuning / LoRA training?
│       └── shift=3.0  # match the upstream training distribution
│
├── sft / xl-sft (50 steps, CFG-able)
│   ├── First attempt / unknown prompt shape?
│   │   └── shift=3.0  # documented default; best starting point
│   │
│   ├── Vocals render harsh at shift=3.0?
│   │   └── try shift=1.0  # smoother detail phase = softer sibilants
│   │
│   ├── Output structure feels flat (verse ≈ chorus)?
│   │   └── try shift=4.0  # push the macro arc harder
│   │
│   └── Switching from xl-sft to xl-base (BASE-only task)?
│       └── keep shift=3.0  # both checkpoints use the same default
│
└── xl-mixed (xl-base + 4B LM)
    ├── First attempt / unknown prompt shape?
    │   └── shift=3.0  # inherits xl-base default
    │
    ├── LM-driven planning is producing good captions but DiT still feels off?
    │   └── try shift=1.0 or shift=5.0  # isolate whether the schedule
    │                                   # is the issue or the LM is
    │
    └── On 24 GB M3 and the generation is too slow?
        └── fall back to xl-sft + 1.7B LM at shift=3.0  # the skill's
                                                       # documented
                                                       # compromise tier
```

## 5. Impact on quality

### 5.1 Qualitative differences

| Aspect | `shift=1.0` | `shift=3.0` | Continuous |
| --- | --- | --- | --- |
| **Arrangement richness** | Higher (more steps on detail) | Lower (more steps on structure) | Configurable per phase |
| **Macro arc (verse → chorus lift)** | Flatter contrast | Sharper contrast | Configurable |
| **Vocal intelligibility** | Higher at low step counts | Comparable at 50 steps | Comparable |
| **Orchestration density** | Higher | Lower (can sound "thin") | Configurable |
| **Prompt adherence (long prompts)** | Lower (less structure compute) | Higher | Depends on schedule |
| **Reproducibility across seeds** | High | High | Lower (more variables) |
| **Vocal harshness / sibilance** | Slightly softer | Slightly harsher at the same `guidance_scale` | Depends |

### 5.2 When `shift=3.0` clearly wins

- Long-form outputs (≥ 120 s) where the macro arc is the point.
- Genres with strong verse/chorus contrast (pop, rock, EDM build/drop).
- BASE-only tasks (`extract`, `lego`, `complete`) where upstream docs
  pin 3.0.
- When `guidance_scale ≥ 7.0` — the steeper schedule prevents CFG
  from over-fitting to late-step noise.

### 5.3 When `shift=1.0` clearly wins

- Short outputs (≤ 60 s) where structure compute doesn't matter much.
- Genres where micro-detail is the point (jazz fusion, complex
  electronic, orchestral).
- When you need **softer vocals** at high CFG (xl-sft at
  `guidance_scale=7.0` is often harsh — `shift=1.0` + `guidance_scale=5.0`
  is the gentler combo).

### 5.4 When continuous shift is worth the complexity

- Cinematic / trailer cues that need a strong opening arc AND dense
  detail in the climax.
- Jazz fusion / progressive where you want section-by-section schedule
  variation.
- Custom fine-tunes that target a specific schedule shape.

## 6. Impact on speed

`shift` **does not change the number of steps** and **does not change
the wall-clock per step**. It changes:

| Aspect | Effect of `shift` |
| --- | --- |
| **Wall-clock per step** | None — same compute per step regardless of shift |
| **Total wall-clock** | Roughly constant — same step count, same per-step time |
| **Convergence quality per step** | Higher `shift` = early steps contribute more to the final output. With a well-shaped schedule, you may converge in fewer steps; with a mis-shaped schedule, you may waste steps. |
| **Effective step count** | Higher `shift` effectively concentrates "useful" compute into fewer steps. Lower `shift` spreads it out. Net effect on a fixed `inference_steps` budget: `shift=3.0` at 8 steps may look like `shift=1.0` at 12 steps in quality. |

**Practical implication for the skill:**

- The standard-tier (`turbo`, 8 steps) wall-clock is **the same**
  regardless of `shift` setting. Choose `shift` based on desired
  character, not speed.
- The xl-mixed tier (4B DiT, 50 steps) is **dominated by per-step
  time**; `shift` does not materially change wall-clock. The 52-min /
  60 s figure from [`acestep-generation.md`](acestep-generation.md) §
  "M3 performance by tier" is `shift`-agnostic.

## 7. Examples

### 7.1 — `turbo` (standard tier, 8 steps, `shift=1.0`)

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "groovy funk track with slap bass, tight horn stabs, rhythmic guitar scratching",
    "audio_duration": 60,
    "thinking": true,
    "inference_steps": 8,
    "shift": 1.0,
    "infer_method": "ode"
  }')
```

### 7.2 — `xl-base` (BASE, 50 steps, `shift=3.0` — the documented default)

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bass",
    "lyrics": "[Verse]\nneon lights on a vacant street\n\n[Chorus]\nwe are the night",
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
```

### 7.3 — `xl-sft` with `shift=1.0` (softer vocals experiment)

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "warm acoustic ballad with breathy female vocal",
    "lyrics": "[Verse]\nwalking through the morning light",
    "audio_duration": 60,
    "thinking": true,
    "inference_steps": 50,
    "guidance_scale": 5.0,
    "shift": 1.0,
    "infer_method": "ode"
  }')
```

### 7.4 — `xl-sft` with `shift=5.0` (push the macro arc)

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "anthemic pop with explosive chorus, verse quiet and intimate, chorus huge and cathartic",
    "lyrics": "[Verse]\nquietly holding on\n\n[Chorus]\nwe rise together",
    "audio_duration": 60,
    "thinking": true,
    "inference_steps": 50,
    "guidance_scale": 7.0,
    "shift": 5.0,
    "infer_method": "ode"
  }')
```

### 7.5 — Continuous shift via custom `timesteps`

```python
from acestep.inference import GenerationParams, GenerationConfig, generate_music

# Continuous schedule: front-load shift=1.0 (broad strokes),
# then ramp up to shift=5.0 (tightening detail) by providing
# the actual timestep grid the model will denoise on.
params = GenerationParams(
    caption="ambient cinematic buildup with slow crescendo",
    timesteps=[0.97, 0.85, 0.70, 0.55, 0.40, 0.28, 0.18, 0.10, 0.05, 0.0],
    # When `timesteps` is provided, it overrides `inference_steps` and `shift`.
    thinking=True,
)

config = GenerationConfig(batch_size=1, audio_format="flac")
result = generate_music(dit_handler, llm_handler, params, config, save_dir="/output")
```

### 7.6 — Switching to a shift-distilled turbo variant

```bash
# 1. Stop the server
# 2. Set ACESTEP_CONFIG_PATH to the shift-distilled checkpoint
ACESTEP_CONFIG_PATH=acestep-v15-turbo-shift3 \
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B \
ACESTEP_LM_BACKEND=mlx \
uv run acestep-api --port 8001

# 3. Pass shift=3.0 (matches the distillation)
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "minimalist piano ballad, sparse arrangement, intimate",
    "inference_steps": 8,
    "shift": 3.0
  }')
```

### 7.7 — A/B test recipe (locked seed, only `shift` changes)

```bash
# Pick one prompt and one seed; sweep shift in 1.0, 2.0, 3.0, 4.0, 5.0.
# Compare the five outputs by listening + ebur128 LRA.

# One job at a time: submit, wait for it, then submit the next shift value.
for SHIFT in 1.0 2.0 3.0 4.0 5.0; do
  TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json \
    "{\"prompt\":\"warm indie folk, fingerstyle guitar, soft brushed drums\",\"audio_duration\":60,\"thinking\":true,\"inference_steps\":8,\"seed\":42,\"use_random_seed\":false,\"shift\":$SHIFT,\"audio_format\":\"wav\"}")
  python3 scripts/wait_for_acestep.py "$TASK_ID" --expected-seconds 60
done

# Listen to all five back-to-back.
```

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Output feels "mushy" / flat structure (verse ≈ chorus) | `shift` is too low for the prompt's macro arc | Bump `shift` toward 3.0; on SFT/XL, try 4.0 or 5.0 |
| Output feels "thin" / under-arranged | `shift` is too high for the prompt's detail needs | Drop `shift` toward 1.0; if already at 1.0, try `inference_steps=64` |
| Vocals render harsh / sibilant | `shift=3.0` + `guidance_scale ≥ 7.0` over-fits to late-step noise | Drop to `shift=1.0` AND `guidance_scale=5.0` (the softer combo for SFT — see [`acestep-xl-models.md`](acestep-xl-models.md) § 3) |
| BASE-only task (`extract`/`lego`/`complete`) silently fails | Wrong shift for the loaded BASE checkpoint | Confirm `shift=3.0` is passed; BASE tasks default to shift=3.0 in the API but won't reject wrong values — they'll just produce subpar output |
| 8-step XL produces "soup" output | `shift` is not the cause — `num_inference_steps` is | This is the `num_inference_steps=50` footgun from [`acestep-xl-models.md`](acestep-xl-models.md) § 3, not a shift issue. Pass `inference_steps=50` explicitly. |
| `shift=1.0` on `turbo-shift3` produces noisy detail | Wrong shift for the loaded checkpoint | Switch to `turbo-shift1` for `shift=1.0` workloads, or accept the `shift=3.0` default for `turbo-shift3` |
| Continuous shift (`timesteps=[…]`) ignores `shift` parameter | By design — custom `timesteps` overrides `shift` | If you want a continuous schedule, supply `timesteps` and don't pass `shift`. The two are mutually exclusive. |
| Same `shift`, different `inference_methods` produce different outputs | `infer_method="sde"` injects stochastic noise per step | Switch to `infer_method="ode"` for deterministic comparison; or accept the variability if using `sde` |
| Output is identical across seeds | Probably `num_inference_steps=8` on XL (wrong footgun) — not a shift issue | See 8-step XL footgun above |
| Output sounds great on `turbo` but "off" on `xl-turbo` | The XL variant is more sensitive to schedule mismatches | Match the `shift` to the prompt shape more carefully on XL; the 4B DiT is less forgiving of mis-shaped schedules |
| Custom `timesteps` schedule produces artifacts | Schedule is mis-shaped (e.g. monotonicity violation, too few points) | Verify the schedule is strictly decreasing from `~1.0` to `0.0`; aim for 8–16 points; cross-check by running the same schedule with `infer_method="ode"` (deterministic) to isolate the schedule from sampling noise |
| BMAD shift-sweep shows no audible difference | Either the prompt is shift-insensitive (e.g. simple percussive loop) or the step count is too low to reveal schedule effects | Accept the result; or raise `inference_steps` to 32+ on SFT/XL to expose schedule effects |

## 9. Footguns (must read)

These three footguns are specific to `shift` and silently degrade
quality if missed. They sit alongside the `num_inference_steps=50` and
`shift=3.0` footguns already documented in
[`acestep-xl-models.md`](acestep-xl-models.md) § 3.

1. **`shift` does NOT control vocal/instrument separation.** That is a
   VAE-level operation. Don't tune `shift` to chase cleaner stems —
   tune `audio_cover_strength` (for cover) or use Demucs for full
   stem separation.

2. **`shift` is fully effective on `sft` / `xl-sft` even though the
   upstream `INFERENCE.md` says "only effective for base models".** That
   doc line was written before the SFT-shift interactions were
   characterized. On SFT, `shift` is a real knob — try 1.0–5.0.

3. **Custom `timesteps` overrides `shift`.** Passing both is
   unnecessary; only one will be honored (the `timesteps` list, per
   upstream `GenerationParams` doc). For continuous shift, supply
   `timesteps` and omit `shift`.

## 10. Sources

- [`ACE-Step-1.5/docs/en/INFERENCE.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md)
  — `GenerationParams.shift` formula
  (`t = shift * t / (1 + (shift - 1) * t)`),
  default `1.0`, range `1.0–5.0`, "Recommended 3.0 for turbo models".
- [`ACE-Step-1.5/docs/en/Tutorial.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md)
  § DiT Models — turbo variant distillation configs (joint / shift1 /
  shift3 / continuous), semantic-vs-detail description of the shift
  parameter, "draw outline first then fill details" mental model.
- [`ACE-Step-1.5/README.md`](https://github.com/ace-step/ACE-Step-1.5/blob/main/README.md) § Model
  Zoo (DiT Models / XL DiT Models) — checkpoint names and properties.
- [`references/acestep-xl-models.md`](acestep-xl-models.md) — `shift=3.0`
  pinned as XL Base default; `shift` does NOT control vocal/instrument
  separation.
- [`references/acestep-task-types.md`](acestep-task-types.md) —
  `extract`/`lego`/`complete` all use `shift: 3.0` as the BASE-only
  default.
- [`references/acestep-generation.md`](acestep-generation.md) —
  `shift: 3.0` documented default for base models; the
  "only effective for base models, not turbo models" upstream note and
  the xl-sft-is-not-turbo caveat.
- `music-craft_ROADMAP.md` item **13i** — the original taxonomy
  request, tier-to-shift mapping table, and verification criterion.
- `music-craft-ENHANCEMENT-PLAN.md` — sequenced under item 12
  (Turbo shift-schedule taxonomy).

## 11. See also

- [`acestep-generation.md`](acestep-generation.md) — base 3-step
  workflow, full parameter table, quality tiers with ML-budget probe.
- [`acestep-xl-models.md`](acestep-xl-models.md) — XL (4B) DiT
  reference, including the `num_inference_steps=50` and `shift=3.0`
  footguns.
- [`acestep-task-types.md`](acestep-task-types.md) — the six
  audio-conditioned task types; `extract`/`lego`/`complete` (BASE-only).
- [`setup-and-preflight.md`](setup-and-preflight.md) — ML-budget probe,
  env-var reference, model download consent flow.
- [`quality-and-revision.md`](quality-and-revision.md) — listenability
  rubric for "is this output good enough to ship?" decisions when
  shift-sweeping.
- [`prompt-formula.md`](prompt-formula.md) — production-sheet prompt
  construction that pairs naturally with the right shift choice.
