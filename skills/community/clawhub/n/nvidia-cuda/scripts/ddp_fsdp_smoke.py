#!/usr/bin/env python3
"""Minimal torchrun smoke test for DDP and FSDP."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.nn.parallel import DistributedDataParallel as DDP


class TinyMLP(nn.Module):
    def __init__(self, dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, dim * 2),
            nn.GELU(),
            nn.Linear(dim * 2, dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value is not None else default


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["ddp", "fsdp"], default="ddp")
    parser.add_argument("--dim", type=int, default=256)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--dtype", choices=["fp32", "bf16"], default="bf16")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is unavailable.")

    local_rank = env_int("LOCAL_RANK", 0)
    rank = env_int("RANK", 0)
    world_size = env_int("WORLD_SIZE", 1)
    device = torch.device("cuda", local_rank)
    torch.cuda.set_device(device)
    dist.init_process_group(backend="nccl", device_id=device)

    model = TinyMLP(args.dim).to(device)
    if args.mode == "ddp":
        wrapped = DDP(model, device_ids=[local_rank], output_device=local_rank)
    else:
        wrapped = FSDP(model, device_id=device)

    optimizer = torch.optim.AdamW(wrapped.parameters(), lr=1e-3)
    dtype = torch.bfloat16 if args.dtype == "bf16" else torch.float32
    scaler = None
    if dtype == torch.float16:
        scaler = torch.amp.GradScaler("cuda")

    inputs = torch.randn(args.batch, args.dim, device=device)
    targets = torch.randn(args.batch, args.dim, device=device)

    optimizer.zero_grad(set_to_none=True)
    with torch.amp.autocast("cuda", dtype=dtype, enabled=dtype != torch.float32):
        output = wrapped(inputs)
        loss = F.mse_loss(output, targets)
    loss.backward()
    optimizer.step()

    checksum = torch.tensor([float(loss.detach().float().item())], device=device)
    dist.all_reduce(checksum, op=dist.ReduceOp.SUM)
    checksum_value = float(checksum.item())

    result: dict[str, Any] = {
        "mode": args.mode,
        "rank": rank,
        "local_rank": local_rank,
        "world_size": world_size,
        "dtype": args.dtype,
        "loss_sum": checksum_value,
        "ok": torch.isfinite(torch.tensor(checksum_value)).item(),
        "device": torch.cuda.get_device_name(device),
    }

    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))

    dist.destroy_process_group()
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
