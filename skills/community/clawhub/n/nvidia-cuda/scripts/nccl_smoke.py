#!/usr/bin/env python3
"""Minimal NCCL smoke test for torchrun-based multi-GPU validation."""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any

import torch
import torch.distributed as dist


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value is not None else default


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", default="nccl")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is unavailable.")

    local_rank = env_int("LOCAL_RANK", 0)
    rank = env_int("RANK", 0)
    world_size = env_int("WORLD_SIZE", 1)

    torch.cuda.set_device(local_rank)
    dist.init_process_group(backend=args.backend, device_id=torch.device("cuda", local_rank))

    tensor = torch.tensor([rank + 1.0], device="cuda")
    torch.cuda.synchronize()
    start = time.perf_counter()
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
    dist.barrier()
    torch.cuda.synchronize()
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    expected = sum(float(i + 1) for i in range(world_size))
    result: dict[str, Any] = {
        "backend": args.backend,
        "rank": rank,
        "local_rank": local_rank,
        "world_size": world_size,
        "device": torch.cuda.get_device_name(local_rank),
        "all_reduce_result": float(tensor.item()),
        "expected": expected,
        "elapsed_ms": round(elapsed_ms, 4),
        "ok": abs(float(tensor.item()) - expected) < 1e-6,
    }

    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))

    dist.destroy_process_group()
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
