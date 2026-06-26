#!/usr/bin/env python3
"""Benchmark a synthetic transformer training step on CUDA."""

from __future__ import annotations

import argparse
import json
import time
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F


DTYPES = {
    "fp32": torch.float32,
    "fp16": torch.float16,
    "bf16": torch.bfloat16,
}


class TinyTransformerLM(nn.Module):
    def __init__(self, vocab_size: int, hidden_size: int, num_heads: int, num_layers: int) -> None:
        super().__init__()
        self.embed = nn.Embedding(vocab_size, hidden_size)
        self.layers = nn.ModuleList(
            [
                nn.TransformerEncoderLayer(
                    d_model=hidden_size,
                    nhead=num_heads,
                    dim_feedforward=hidden_size * 4,
                    dropout=0.0,
                    activation="gelu",
                    batch_first=True,
                    norm_first=True,
                )
                for _ in range(num_layers)
            ]
        )
        self.norm = nn.LayerNorm(hidden_size)
        self.head = nn.Linear(hidden_size, vocab_size, bias=False)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        x = self.embed(tokens)
        causal_mask = torch.ones(tokens.size(1), tokens.size(1), device=tokens.device, dtype=torch.bool).triu(1)
        for layer in self.layers:
            x = layer(x, src_mask=causal_mask)
        x = self.norm(x)
        return self.head(x)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--seq", type=int, default=512)
    parser.add_argument("--hidden", type=int, default=1024)
    parser.add_argument("--heads", type=int, default=16)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--vocab", type=int, default=32000)
    parser.add_argument("--dtype", choices=sorted(DTYPES), default="bf16")
    parser.add_argument("--compile", dest="use_compile", action="store_true")
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--iters", type=int, default=10)
    parser.add_argument("--log-every", type=int, default=0, help="If > 0, force loss.item() every N steps.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is unavailable.")

    dtype = DTYPES[args.dtype]
    torch.set_float32_matmul_precision("high")
    device = "cuda"

    model = TinyTransformerLM(args.vocab, args.hidden, args.heads, args.layers).to(device)
    if args.use_compile:
        model = torch.compile(model, mode="max-autotune")
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    scaler = torch.amp.GradScaler("cuda") if dtype == torch.float16 else None

    tokens = torch.randint(0, args.vocab, (args.batch, args.seq), device=device)
    targets = torch.randint(0, args.vocab, (args.batch, args.seq), device=device)

    def step(step_idx: int) -> float | None:
        optimizer.zero_grad(set_to_none=True)
        with torch.amp.autocast("cuda", dtype=dtype, enabled=dtype != torch.float32):
            logits = model(tokens)
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        if scaler is not None:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        if args.log_every > 0 and step_idx % args.log_every == 0:
            return float(loss.item())
        return None

    for idx in range(args.warmup):
        step(idx)
    torch.cuda.synchronize()

    start_evt = torch.cuda.Event(enable_timing=True)
    end_evt = torch.cuda.Event(enable_timing=True)
    wall_start = time.perf_counter()
    start_evt.record()
    sampled_losses: list[float] = []
    for idx in range(args.iters):
        value = step(idx)
        if value is not None:
            sampled_losses.append(value)
    end_evt.record()
    torch.cuda.synchronize()
    wall_elapsed = time.perf_counter() - wall_start

    avg_ms = start_evt.elapsed_time(end_evt) / args.iters
    tokens_per_s = (args.batch * args.seq) / (wall_elapsed / args.iters)
    result: dict[str, Any] = {
        "dtype": args.dtype,
        "compile": args.use_compile,
        "batch": args.batch,
        "seq": args.seq,
        "hidden": args.hidden,
        "heads": args.heads,
        "layers": args.layers,
        "avg_ms": round(avg_ms, 4),
        "tokens_per_s": round(tokens_per_s, 2),
        "log_every": args.log_every,
        "sampled_losses": sampled_losses[:5],
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
