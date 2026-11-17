# Advanced Diffusion Controls

Reference for the diffusion-engine knobs ACE-Step 1.5 exposes beyond
the prompt: `guidance_scale`, `infer_method`, `shift`, `timesteps`,
`use_adg`, `cfg_interval_*`. Load when a request asks to push prompt
adherence, change solver behavior, swap noise schedules, or debug
quality/stability regressions on BASE / SFT / XL checkpoints.

> **Status:** Tier 3 reference. Backed by `ACE-Step-1.5/docs/en/INFERENCE.md`
> § "Generation Parameters" + § "Advanced DiT Parameters". Read with
> [`acestep-shift-schedule.md`](acestep-shift-schedule.md) (for `shift`)
> and [`acestep-xl-models.md`](acestep-xl-models.md) (for XL footguns).

## TL;DR

ACE-Step 1.5's diffusion surface is **smaller than the SD / SDXL
vocabulary**. The user-facing levers are `guidance_scale`,
`infer_method`, `shift`, `timesteps`, `use_adg`, and `cfg_interval_*`
— detailed in § 1 below. There is **no `eta` slider** (binary via
`infer_method`) and **no `scheduler` selector** with named values like
`euler` / `dpm++` / `heun` — those live inside ACE-Step's fixed
internal solver and are tuned via `shift` (constant reshape) or
`timesteps` (full grid).

## 1. Parameter table

| Parameter | Type | Default | Range | Effect | Notes |
| --- | --- | --- | --- | --- | --- |
| `guidance_scale` | `float` | `7.0` | 1.0–15.0 | CFG strength — higher = stricter prompt adherence | **BASE / SFT only.** Typical 5.0–9.0. |
| `infer_method` | `str` | `"ode"` | `ode` / `sde` | Solver | `ode` = deterministic (eta=0); `sde` = stochastic (eta>0). |
| `shift` | `float` | `1.0` | 1.0–5.0 | Reshape schedule (`t' = shift·t / (1+(shift-1)·t)`) | `3.0` for BASE/SFT/XL. See [`acestep-shift-schedule.md`](acestep-shift-schedule.md). |
| `timesteps` | list of float | `None` | `[1.0 → 0.0]` | Custom timestep grid | Strictly decreasing. Overrides `inference_steps` + `shift`. |
| `use_adg` | `bool` | `False` | bool | Adaptive Dual Guidance | **BASE only.** Quality boost at cost of speed. |
| `cfg_interval_start` / `_end` | `float` | `0.0` / `1.0` | 0.0–1.0 | Apply CFG only on a band | `1.0` end = full-range CFG. |

## 2. Parameter impact

**`guidance_scale`** — low (1.0–3.0) dreamy / weak-adherence;
mid (5.0–7.0) balanced; high (8.0–12.0) strict but possibly harsh;
>12 risks over-saturation. **turbo ignores.**

**`infer_method`** — `"ode"` is the deterministic daily driver (same
seed = same output). Use `"sde"` when SFT outputs feel "stuck" or you
want batch diversity at locked seed. Wall-clock roughly equal.
**`sde` is not bit-exact reproducible** — lock `ode` for A/B tests.

**`shift`** — `1.0` even (turbo default); `3.0` front-loaded
(BASE/SFT/XL default — stronger semantics, drier arrangement);
`5.0` even more front-loaded. **Not** a vocal/instrument separator
(that's VAE-level).

**`timesteps`** — when supplied, overrides both `inference_steps` and
`shift`. Use for **continuous shift** on `turbo-continuous` or to
A/B a custom schedule. Strictly decreasing `[~1.0 → 0.0]`.

**`use_adg`** — BASE-only quality boost, 1.5–2× slower per step.

**`cfg_interval_*`** — apply CFG only on a band (e.g. `start=0.1`,
`end=0.7`) to skip cold-start noise and avoid end-of-diffusion
over-fitting when `guidance_scale ≥ 9.0`.

## 3. Recommended values per use case

| Scenario | `inference_steps` | `guidance_scale` | `shift` | `infer_method` | `use_adg` |
| --- | --- | --- | --- | --- | --- |
| `turbo` (standard, 8 steps) | 8 | 7.0 (ignored) | 1.0 | `ode` | false |
| `xl-turbo` (fast XL) | 8 | 7.0 (ignored) | 1.0 | `ode` | false |
| BASE 50 steps, prompt strict | 50 | 7.0 | 3.0 | `ode` | true |
| BASE 50 steps, dreamy | 50 | 4.0 | 1.0 | `ode` | false |
| SFT 50 steps, default | 50 | 5.0 | 3.0 | `ode` | false |
| SFT 50 steps, stable | 50 | 5.0 | 3.0 | `sde` | false |
| XL-SFT 50 steps, gentle vocals | 50 | 4.0 | 1.0 | `ode` | false |
| XL-BASE 50 steps, strict semantics | 50 | 7.0 | 3.0 | `ode` | true |

> **`xl-base` with default 8 steps = "soup" output.** Always pass
> `num_inference_steps=50` explicitly on XL Base — see
> [`acestep-xl-models.md`](acestep-xl-models.md) § 3.

## 4. Examples

### 4.1 BASE 50 steps — strict semantics, ADG on

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bassline",
    "audio_duration": 210, "thinking": true,
    "inference_steps": 50, "guidance_scale": 7.0,
    "shift": 3.0, "infer_method": "ode",
    "use_adg": true, "audio_format": "wav"
  }')
```

### 4.2 SDE for SFT stability / continuous shift

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "warm acoustic ballad with breathy female vocal",
    "audio_duration": 60, "thinking": true,
    "inference_steps": 50, "guidance_scale": 5.0,
    "shift": 3.0, "infer_method": "sde",
    "audio_format": "flac"
  }')
```

```python
# 4.3  Continuous shift via timesteps (overrides shift + inference_steps)
from acestep.inference import GenerationParams, GenerationConfig, generate_music
params = GenerationParams(
    caption="ambient cinematic buildup",
    timesteps=[0.97, 0.85, 0.70, 0.55, 0.40, 0.28, 0.18, 0.10, 0.05, 0.0],
    thinking=True,
)
config = GenerationConfig(batch_size=1, audio_format="flac")
generate_music(dit_handler, llm_handler, params, config, save_dir="/out")
```

## 5. Footguns

1. **`guidance_scale` does nothing on turbo** (ignored on `v15-turbo`
   and `xl-turbo`). 2. **`use_adg` silently no-ops on SFT / turbo.**
   3. **`shift` is NOT a vocal/instrument separator** (VAE-level).
   4. **`timesteps` overrides `shift` + `inference_steps`.**
   5. **`infer_method="sde"` is not reproducible** — lock `ode` for A/B
   tests. 6. **`xl-base` with default 8 steps = "soup" output** —
   always pass `num_inference_steps=50` explicitly on XL Base (see
   [`acestep-xl-models.md`](acestep-xl-models.md) § 3).
   7. **Custom `timesteps` must be strictly decreasing** from ~1.0 to 0.0.
   8. **`cfg_interval_*` band too narrow** (`end - start < 0.1`) leaves
   the prompt barely anchored.

## 6. Sources + See also

- `ACE-Step-1.5/docs/en/INFERENCE.md` § Generation Parameters +
  § Advanced DiT Parameters + § Best Practices #2 Parameter Tuning.
- [`acestep-generation.md`](acestep-generation.md) — base 3-step
  workflow, full parameter table, tier selection.
- [`acestep-shift-schedule.md`](acestep-shift-schedule.md) — the
  full `shift` taxonomy.
- [`acestep-xl-models.md`](acestep-xl-models.md) — XL DiT footguns.
- [`acestep-task-types.md`](acestep-task-types.md) — BASE-only tasks
  (`extract` / `lego` / `complete`).
