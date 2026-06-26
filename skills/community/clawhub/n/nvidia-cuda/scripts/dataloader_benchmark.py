#!/usr/bin/env python3
"""Benchmark dataloader and host-to-device throughput for CUDA training loops."""

from __future__ import annotations

import argparse
import json
import time
from typing import Any

import torch
from torch.utils.data import DataLoader, Dataset


class SyntheticDataset(Dataset):
    def __init__(self, sample_shape: tuple[int, ...], length: int, cpu_work_ms: float) -> None:
        self.sample_shape = sample_shape
        self.length = length
        self.cpu_work_ms = cpu_work_ms

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int):
        if self.cpu_work_ms > 0:
            time.sleep(self.cpu_work_ms / 1000.0)
        sample = torch.randn(self.sample_shape, dtype=torch.float32)
        target = torch.tensor(index % 2, dtype=torch.int64)
        return sample, target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--height", type=int, default=224)
    parser.add_argument("--width", type=int, default=224)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--pin-memory", action="store_true")
    parser.add_argument("--persistent-workers", action="store_true")
    parser.add_argument("--prefetch-factor", type=int, default=2)
    parser.add_argument("--cpu-work-ms", type=float, default=0.0)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--iters", type=int, default=50)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA is unavailable.")

    dataset = SyntheticDataset(
        sample_shape=(args.channels, args.height, args.width),
        length=(args.warmup + args.iters + 8) * args.batch_size,
        cpu_work_ms=args.cpu_work_ms,
    )
    loader_kwargs: dict[str, Any] = {
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "pin_memory": args.pin_memory,
        "persistent_workers": args.persistent_workers if args.num_workers > 0 else False,
    }
    if args.num_workers > 0:
        loader_kwargs["prefetch_factor"] = args.prefetch_factor

    loader = DataLoader(dataset, **loader_kwargs)
    iterator = iter(loader)

    for _ in range(args.warmup):
        batch, target = next(iterator)
        if device == "cuda":
            batch = batch.to(device, non_blocking=args.pin_memory)
            target = target.to(device, non_blocking=args.pin_memory)
            _ = (batch.mean() + target.float().mean()).item()
    if device == "cuda":
        torch.cuda.synchronize()

    start = time.perf_counter()
    processed = 0
    for _ in range(args.iters):
        batch, target = next(iterator)
        if device == "cuda":
            batch = batch.to(device, non_blocking=args.pin_memory)
            target = target.to(device, non_blocking=args.pin_memory)
            _ = (batch.mean() + target.float().mean()).item()
        processed += batch.size(0)
    if device == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    result = {
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "pin_memory": args.pin_memory,
        "persistent_workers": args.persistent_workers if args.num_workers > 0 else False,
        "prefetch_factor": args.prefetch_factor if args.num_workers > 0 else None,
        "cpu_work_ms": args.cpu_work_ms,
        "device": args.device,
        "batches_per_s": round(args.iters / elapsed, 2),
        "samples_per_s": round(processed / elapsed, 2),
        "avg_batch_ms": round((elapsed / args.iters) * 1000.0, 4),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
