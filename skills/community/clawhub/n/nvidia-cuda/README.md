# nvidia-cuda

`nvidia-cuda` is an open-source skill package for Codex, OpenClaw, and similar agent systems that need to write or review deep learning code for NVIDIA GPUs.

It is opinionated on purpose. The package encodes modern AI infra practice for H100, H200, and B200-class systems:

- BF16 and FP8-aware precision policy
- `torch.compile` as a benchmarked option, not a taboo
- attention backend selection that does not stop at default SDPA
- FSDP and ZeRO before using gradient checkpointing as a crutch
- `.item()` and host sync anti-pattern detection
- dataloader, pinning, prefetch, and persistent worker checks
- NCCL, TP/SP/CP/EP, TensorRT-LLM, speculative decoding, and TE guidance

## Why this exists

A lot of GPU training code still leaves major performance on the floor because it inherits conservative defaults:

- full FP32 everywhere
- no compile pass
- no attention backend evaluation on newer hardware
- per-step host synchronization for metrics
- checkpointing used before state sharding
- dataloaders that starve the GPU

Those mistakes compound. This skill gives an agent a clear optimization order and a concrete review checklist.

## What is inside

- [SKILL.md](SKILL.md): the main operational policy
- [references/official-notes.md](references/official-notes.md): official PyTorch and NVIDIA references
- [references/latest-gpu-recommendations-2026-04.md](references/latest-gpu-recommendations-2026-04.md): latest GPU shortlist as of 2026-04-19
- [references/runtime-support.md](references/runtime-support.md): tested and expected runtime surface
- [agents/openai.yaml](agents/openai.yaml): optional UI metadata for skill-aware clients
- [scripts/](scripts/): reusable probes, scanners, and benchmarks
- [examples/](examples/): sample environment and planning configs

## Bundled tooling

The repository now includes reusable scripts:

- `scripts/cuda_env_probe.py`
- `scripts/check_training_stack.py`
- `scripts/benchmark_attention.py`
- `scripts/training_step_benchmark.py`
- `scripts/dataloader_benchmark.py`
- `scripts/nccl_smoke.py`
- `scripts/ddp_fsdp_smoke.py`

Example commands:

```bash
python scripts/cuda_env_probe.py --json
python scripts/check_training_stack.py path/to/project
python scripts/benchmark_attention.py --list-flash-impls
python scripts/benchmark_attention.py --backend cudnn --dtype bf16 --seq 4096 --compile
python scripts/training_step_benchmark.py --dtype bf16 --compile --iters 10
python scripts/dataloader_benchmark.py --pin-memory --num-workers 8 --persistent-workers --prefetch-factor 4
torchrun --standalone --nproc_per_node=2 scripts/nccl_smoke.py --json
torchrun --standalone --nproc_per_node=2 scripts/ddp_fsdp_smoke.py --mode ddp --json
torchrun --standalone --nproc_per_node=2 scripts/ddp_fsdp_smoke.py --mode fsdp --json
```

## Install locally

### Codex

Copy this directory to your skills path as `~/.codex/skills/nvidia-cuda/`.

### OpenClaw / ClawHub-compatible agents

The repository root is already a skill package:

- `SKILL.md` at the root
- supporting files under `references/` and `agents/`

That means you can publish this repository directly as a skill package after review.

## Triggering

Use the skill by name:

```text
$nvidia-cuda optimize this H100 training loop
```

Example prompts:

- `$nvidia-cuda review this multi-GPU training stack for H200 underutilization`
- `$nvidia-cuda optimize this transformer inference path on B200`
- `$nvidia-cuda audit this dataloader, precision policy, and logging loop`

## Hardware and framework stance

The skill is most opinionated for:

- H100 / Hopper
- H200
- B200 / Blackwell-class GPUs

The primary software target is PyTorch on CUDA, with side coverage for:

- NCCL
- Triton
- Transformer Engine
- TensorRT-LLM
- Megatron Core style large-model sharding

## Latest GPU recommendations

As of **2026-04-19**, the practical shortlist in this repository is:

- **RTX 5090** for cost-sensitive local prototyping
- **RTX PRO 6000 Blackwell Workstation Edition** for serious single-workstation AI development
- **DGX Station** if you want a full deskside AI system rather than a loose card
- **RTX PRO 6000 Blackwell Server Edition** for universal enterprise server deployment
- **H200** for memory-first Hopper deployments
- **DGX B300** for the newest top-end single-node training system
- **DGX B200** as the current Blackwell step-down single-node training system
- **GB200 NVL72** for rack-scale frontier training and trillion-parameter inference
- **GB300 NVL72** as the newest rack-scale recommendation for AI reasoning and test-time scaling
- **L4** for efficient low-power inference

Detailed rationale and official links:

- [latest-gpu-recommendations-2026-04.md](references/latest-gpu-recommendations-2026-04.md)

## Sample configs

This repository now includes planning and environment examples:

- [workstation-rtx-pro6000-blackwell.env](examples/workstation-rtx-pro6000-blackwell.env)
- [b200-8gpu-torchrun.env](examples/b200-8gpu-torchrun.env)
- [dgx-b300-training.yaml](examples/dgx-b300-training.yaml)
- [h200-long-context-training.yaml](examples/h200-long-context-training.yaml)
- [gb300-serving.yaml](examples/gb300-serving.yaml)
- [l4-edge-serving.yaml](examples/l4-edge-serving.yaml)
- [runtime-support.md](references/runtime-support.md)

## Release policy

This repository uses semver. The current target release is `0.4.0`.

Version `0.4.0` establishes:

- the initial optimization doctrine
- the anti-pattern blocklist
- H100/H200/B200 attention and precision guidance
- training and inference optimization ladders
- ClawHub-ready repository packaging
- reusable probes and benchmark scripts for environment, attention, training-step, and dataloader analysis
- current NVIDIA GPU purchase guidance with official references and sample planning configs
- a basic CI smoke workflow and NCCL smoke-test helper
- explicit DDP/FSDP smoke coverage and broader scanner coverage for Triton, CUDA, and C++ review surfaces

## ClawHub publication note

ClawHub supports publishing skill packages from a local path via its CLI.

At the time this repository was prepared:

- the upstream ClawHub project documents `clawhub skill publish <path>`
- the ClawHub web UI also supports signed-in publication

CLI example:

```bash
npx clawhub@latest publish . \
  --slug nvidia-cuda \
  --name "NVIDIA CUDA" \
  --version 0.4.0 \
  --changelog "Add official FA/DDP/FSDP tooling and broader scanner coverage"
```

Because community skill marketplaces can carry supply-chain risk, publish only reviewed, minimal, instruction-focused packages and inspect any scanner output before making a listing public.

## License

[MIT-0](LICENSE)
