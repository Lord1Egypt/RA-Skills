# Runtime Support

This repository is not a Python library package. It is a skill package plus runnable helper scripts.

## Intended runtime

Tested locally during repository development on:

- Python `3.13.11`
- PyTorch `2.11.0+cu130`
- CUDA runtime `13.0`
- NVIDIA H100 80GB HBM3

## Minimum practical expectations

- Python `3.10+`
- PyTorch `2.11+`
- CUDA-capable PyTorch build for any GPU benchmark or NCCL smoke test

## Script expectations

- `scripts/check_training_stack.py`:
  - Python standard library only
  - no CUDA required

- `scripts/cuda_env_probe.py`:
  - requires `torch`
  - does not require a working GPU just to report environment facts, but is most useful when CUDA is visible

- `scripts/benchmark_attention.py`
- `scripts/training_step_benchmark.py`
- `scripts/dataloader_benchmark.py`
- `scripts/nccl_smoke.py`
- `scripts/ddp_fsdp_smoke.py`
  - require `torch`
  - require CUDA visibility
  - `scripts/nccl_smoke.py` and `scripts/ddp_fsdp_smoke.py` also require `torchrun`-style distributed environment variables

## Compatibility note

Some recommendations in the skill target H200, B200, GB200, and GB300-era hardware. Those parts are based on official NVIDIA positioning and documentation, but not every path is runnable on the local H100 development host.
