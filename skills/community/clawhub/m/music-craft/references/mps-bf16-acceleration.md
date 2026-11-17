# MPS Acceleration for ACE-Step on Apple Silicon

Honest reference for running ACE-Step's DiT on Apple Silicon GPUs via Metal
Performance Shaders (MPS). **As of 2026-07-30, ACE-Step forces `torch.float32`
on MPS — there is no documented bf16 path.** This doc reflects what is verifiable
in the ACE-Step source code.

Reference hardware: **M3 MacBook, 24 GB unified memory**.

## Current limitations (verified from source)

As of `acestep/core/generation/handler/init_service_orchestrator.py:101`,
ACE-Step selects the dtype as:

```python
self.dtype = torch.bfloat16 if resolved_device == "xpu" else torch.float32
```

**Translation**: bf16 is only enabled for Intel XPU. On MPS (Apple Silicon),
ACE-Step runs the DiT in `torch.float32`, full stop. There is **no environment
variable to override this** at runtime. `ACESTEP_USE_BF16` does not exist in
the code.

> ✅ Verified — `grep -rn "ACESTEP_USE_BF16" <ACE-Step-1.5 checkout>/`
> returns no matches.

What this means in practice on a 24 GB M3:

- **DiT (2B fp32)**: ~8 GB resident, comfortable on 24 GB unified memory.
- **DiT (4B / XL fp32)**: ~16 GB resident, leaves only ~6–8 GB for OS, IDE,
  browser, app memory pool. Tight. XL is **slow**, not impossible.
- **VAE**: hardcoded to fp16 in `memory_utils.py:212–213`, regardless of
  device — this is the only way fp16 sneaks into the pipeline on MPS.

Until upstream ACE-Step adds a real MPS bf16 path (or you build a custom
Diffusers client), these numbers are what you get on Apple Silicon.

## What DOES work: real env vars

These are the variables ACE-Step actually consumes:

| Variable | Value | Why it matters |
| --- | --- | --- |
| `PYTORCH_MPS_HIGH_WATERMARK_RATIO` | `0.0` | Removes MPS's default ~40 % pool cap so 4B DiT fits in unified memory. **Without this, MPS OOMs at load.** |
| `ACESTEP_LM_BACKEND` | `mlx` | LM (1.7B / 0.6B) runs natively via MLX on Apple Silicon. vLLM is CUDA-only. |
| `ACESTEP_GENERATION_TIMEOUT` | `3600` | XL 50-step runs take 50–100 s/step — default 600 s fires mid-gen. Mandatory for `xl-mixed`. |

> **Variable that does NOT exist**: `ACESTEP_USE_BF16`. Do not set it.
> If you find docs that reference it, those docs are wrong.

## Setup (real, working)

> **Memory warning:** `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` removes PyTorch's upper limit on MPS memory. A large model can then use most of the Mac's unified memory, slow other apps, and push the system into heavy swap. Explain this and get the user's OK before setting it; set it only for the ACE-Step server process (not globally in a shell profile), close other heavy apps first, and watch `sysctl vm.swapusage` during the first run. It is needed for XL DiTs, not for the standard tier.

```bash
# Apple Silicon ACE-Step — what actually matters today
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0   # XL only, after the user agrees (see warning above)
export ACESTEP_LM_BACKEND=mlx
export ACESTEP_GENERATION_TIMEOUT=3600   # remove if not running XL

# Sanity check: skip the rest on non-Apple-Silicon
if [ "$(uname -s)" != "Darwin" ] || [ "$(uname -m)" != "arm64" ]; then
  echo "WARN: not Apple Silicon — MPS env vars will be ignored" >&2
fi
```

Start the server:

```bash
source ./apple-silicon-ace.sh
cd "${ACE_STEP_PATH}"
uv run acestep-api --port 8001
```

Health check:

```bash
python3 scripts/acestep_request.py health   # → {"status": "ok"}
```

## Performance on M3 24 GB (real-feel estimates, fp32)

> ⚠️ **These numbers are estimates, not measurements.** Verify with
> `time` around a real request on your own hardware before trusting them.
> Source reasoning: DiT forward pass is memory-bandwidth-bound at fp32,
> not compute-bound, so ~2× speedup vs CPU is plausible but unverified here.

| Tier | Hardware | Duration | Wall time (est.) |
| --- | --- | --- | --- |
| `v15-turbo` (2B DiT + 1.7B LM) | MPS fp32 | 30 s | ~5 min |
| `v15-turbo` (2B DiT + 1.7B LM) | MPS fp32 | 60 s | ~8 min |
| `v15-turbo` (2B DiT + 1.7B LM) | MPS fp32 | 210 s | ~25 min |
| `xl-base` / `xl-mixed` (4B DiT) | MPS fp32 | 60 s | ~50 min |
| `xl-mixed` (4B DiT) | MPS fp32 | 210 s | ~3–4 h |

**First run adds ~90 s for model load.** Subsequent runs are faster because
the model stays in MPS memory between requests.

CPU fp32 fallback (no MPS at all) is roughly 3× slower than the MPS row above.
CUDA + bf16 on a 24 GB NVIDIA box is ~2× faster than MPS fp32 (CUDA bf16
**does** work — see ACE-Step source line 101).

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `MPS backend out of memory` at server start | `PYTORCH_MPS_HIGH_WATERMARK_RATIO` not set | With the user's OK (see the memory warning above), restart the server with `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` set for that process only; otherwise use the standard tier. |
| Generation hangs at minute 10 then errors | Default 600 s timeout fired mid-diffusion | `export ACESTEP_GENERATION_TIMEOUT=3600`. |
| XL (4B) on 16 GB Mac is unusable | fp32 4B does not fit, swap-thrashes | Stay on `v15-turbo`. 24 GB runs but slowly. |
| `RuntimeError: ... on CPU-only machine` | `uname -m` is `x86_64` (Intel Mac) | MPS is Apple-Silicon-only. Unset the MPS vars and use CPU or cloud. |
| Audio artifacts on MPS but fine on CPU | Possible MPS op edge case (rare) | File upstream; as a workaround, force CPU (`unset ACESTEP_LM_BACKEND`). |

If a generation aborts, check the server log first — `acestep-api` writes the
traceback to stderr with the OOM step index. Most MPS failures are at
**load time** (model load), not mid-generation.

## Quick Decision Tree (honest)

```
Are you on Apple Silicon?
├── No  → don't read this doc; use CUDA + bf16 (real speedup) or CPU
└── Yes → is your Mac ≥ 32 GB unified memory?
    ├── Yes → daily driver is CUDA via cloud, MPS fp32 as fallback
    └── No  (16 / 24 GB)
        ├── Quick drafts     → v15-turbo, MPS fp32, expect ~25 min / 3 min song
        ├── Production audio → cloud (CUDA bf16) or patience on MPS fp32
        └── Cloud-only       → remote ACE-Step API or another cloud backend
```

## Future: when bf16 lands on MPS

If upstream ACE-Step adds MPS bf16 (likely signal: a PR merged into
`init_service_orchestrator.py` changing the dtype rule), update this doc to:

1. Document the actual bf16 switch (env var or CLI flag — whichever they pick).
2. Re-measure the wall-clock on M3 24 GB / M3 Max.
3. Update the decision tree to recommend MPS bf16 for XL on 24 GB.

Until then, **MPS = fp32**. Don't promise bf16 speed.

## Related

- [`acestep-generation.md`](acestep-generation.md) — full request schema, tier
  table, MLX LM setup.
- [`acestep-xl-models.md`](acestep-xl-models.md) — XL-specific commands and
  the env-var block.
- [`setup-and-preflight.md`](setup-and-preflight.md) — hardware probe and
  per-OS install steps.
- [`error-handling.md`](error-handling.md) — OOM and timeout recovery.
