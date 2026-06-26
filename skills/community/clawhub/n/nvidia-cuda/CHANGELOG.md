# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and the project follows Semantic Versioning.

## [0.4.0] - 2026-04-19

### Added

- `scripts/ddp_fsdp_smoke.py` for one-step DDP and FSDP smoke validation under `torchrun`

### Changed

- expanded `scripts/benchmark_attention.py` to expose official flash implementation listing and activation paths
- expanded `scripts/check_training_stack.py` to cover Triton, CUDA, C++, and launcher-adjacent text surfaces instead of only Python AST scanning
- documented official DDP/FSDP/torchrun and Triton review references

## [0.3.0] - 2026-04-19

### Added

- `references/latest-gpu-recommendations-2026-04.md` with scenario-based NVIDIA GPU recommendations as of 2026-04-19
- `examples/workstation-rtx-pro6000-blackwell.env`
- `examples/b200-8gpu-torchrun.env`
- `examples/dgx-b300-training.yaml`
- `examples/h200-long-context-training.yaml`
- `examples/gb300-serving.yaml`
- `examples/l4-edge-serving.yaml`
- `references/runtime-support.md`
- `scripts/nccl_smoke.py`
- `requirements.txt`
- `.github/workflows/smoke.yml`

### Changed

- documented the latest GPU shortlist directly in `README.md`
- added hardware-purchase guidance to `SKILL.md`

## [0.2.0] - 2026-04-19

### Added

- `scripts/cuda_env_probe.py` for deterministic CUDA and PyTorch environment probing
- `scripts/check_training_stack.py` for heuristic scanning of high-cost training anti-patterns
- `scripts/benchmark_attention.py` for SDPA, flash, and cuDNN attention backend benchmarking
- `scripts/training_step_benchmark.py` for synthetic transformer training-step benchmarking
- `scripts/dataloader_benchmark.py` for worker, pinning, and prefetch throughput checks

### Changed

- upgraded the repository from a documentation-only skill package into a skill package with reusable tooling
- documented bundled tooling in both `SKILL.md` and `README.md`

## [0.1.0] - 2026-04-19

### Added

- initial `nvidia-cuda` skill package for NVIDIA deep learning optimization and review
- BF16, FP8, TF32, and mixed precision policy guidance for H100, H200, and B200-class hardware
- `torch.compile` and CUDA Graphs decision rules
- attention backend policy covering SDPA, FA3/FA4 registration, cuDNN attention, Transformer Engine, and varlen attention
- large-model training guidance for FSDP2, ZeRO-style sharding, distributed optimizer, TP, SP, CP, PP, and EP
- LLM serving guidance for paged KV, chunked prefill, inflight batching, speculative decoding, and TensorRT-LLM
- hard anti-pattern rules for per-step `.item()`, untuned dataloaders, and premature checkpointing
- official reference notes with PyTorch and NVIDIA documentation links
- ClawHub-ready project layout with root `SKILL.md`
