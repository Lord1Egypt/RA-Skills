#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ModelDeck VRAM budget calculator (standard library only).

Estimates the resident VRAM of a quantized transformer by splitting it into
weights, KV cache, compute buffer, and system reserve.

    weights_GiB = params_B * effective_bits * 1e9 / 8 / 2**30
    kv_GiB      = 2 * layers * kv_dim * bytes_per_element * ctx / 2**30

`kv_dim` is kv_heads * head_dim (grouped-query attention keeps this small).
Every number is an estimate derived from parameter count, quantization tier,
layer count, KV shape, and context length. Measure the real figure on the
target machine before committing to a deployment.

Examples
--------
    python vram_budget.py --params 8 --layers 32 --kv-heads 8 --head-dim 128 \
        --ctx 8192 --vram 16 --kv-dtype q8_0
    python vram_budget.py --params 32 --layers 64 --ctx 16384 --vram 24 --json
    python vram_budget.py --list-quants

Exit codes: 0 = at least one tier fits, 2 = nothing fits, 3 = bad arguments.
"""

from __future__ import annotations

import argparse
import json
import sys

GIB = float(1 << 30)
PARAM_TO_GIB = 1e9 / 8.0 / GIB  # params_B * bits -> GiB, about 0.1164

# Effective bits per weight, reconstructed from real GGUF file sizes.
# These include per-block scale overhead and vary by roughly +/-5% per model.
QUANTS = [
    ("F16", 16.00),
    ("Q8_0", 8.50),
    ("Q6_K", 6.56),
    ("Q5_K_M", 5.65),
    ("Q4_K_M", 4.85),
    ("Q4_K_S", 4.60),
    ("IQ4_XS", 4.25),
    ("Q3_K_M", 3.90),
    ("Q2_K", 3.35),
]

# Bytes per cached element. Quantized caches carry a scale factor per block
# (32 elements), so the nominal bit width is scaled by 34/32 for q8_0.
KV_BYTES = {
    "f16": 2.0,
    "bf16": 2.0,
    "q8_0": 1.0 * 34.0 / 32.0,
    "q4_0": 0.5 * 36.0 / 32.0,
}


def weights_gib(params_b: float, bits: float) -> float:
    return params_b * bits * PARAM_TO_GIB


def kv_gib(layers: int, kv_dim: int, ctx: int, kv_dtype: str, slots: int) -> float:
    per_element = KV_BYTES[kv_dtype]
    return 2.0 * layers * kv_dim * per_element * ctx * slots / GIB


def build_rows(args) -> list:
    kv_dim = args.kv_heads * args.head_dim
    rows = []
    for name, bits in QUANTS:
        w = weights_gib(args.params, bits)
        kv = kv_gib(args.layers, kv_dim, args.ctx, args.kv_dtype, args.parallel)
        total = w + kv + args.overhead
        rows.append(
            {
                "quant": name,
                "bits": bits,
                "weights_gib": round(w, 2),
                "kv_gib": round(kv, 2),
                "overhead_gib": round(args.overhead, 2),
                "total_gib": round(total, 2),
                "fits": total <= args.vram,
                "headroom_gib": round(args.vram - total, 2),
            }
        )
    return rows


def ctx_sweep(args, bits: float, ctxs: list) -> list:
    kv_dim = args.kv_heads * args.head_dim
    w = weights_gib(args.params, bits)
    out = []
    for ctx in ctxs:
        kv = kv_gib(args.layers, kv_dim, ctx, args.kv_dtype, args.parallel)
        total = w + kv + args.overhead
        out.append(
            {
                "ctx": ctx,
                "weights_gib": round(w, 2),
                "kv_gib": round(kv, 2),
                "total_gib": round(total, 2),
                "fits": total <= args.vram,
                "headroom_gib": round(args.vram - total, 2),
            }
        )
    return out


def band(percent: float) -> str:
    if percent >= 90:
        return "TIGHT"
    if percent >= 60:
        return "OK"
    return "ROOMY"


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Estimate resident VRAM for a quantized local model.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--params", type=float, default=8.0, help="parameter count in billions (default 8)")
    p.add_argument("--layers", type=int, default=32, help="transformer layers (default 32)")
    p.add_argument("--kv-heads", type=int, default=8, help="KV heads after GQA (default 8)")
    p.add_argument("--head-dim", type=int, default=128, help="dimension per head (default 128)")
    p.add_argument("--ctx", type=int, default=8192, help="context tokens per slot (default 8192)")
    p.add_argument("--parallel", type=int, default=1, help="parallel slots, each holding its own KV (default 1)")
    p.add_argument("--vram", type=float, default=16.0, help="usable VRAM in GiB (default 16)")
    p.add_argument("--kv-dtype", default="f16", choices=sorted(KV_BYTES), help="KV cache precision (default f16)")
    p.add_argument("--overhead", type=float, default=1.6,
                   help="compute buffer + driver/OS reserve in GiB (default 1.6)")
    p.add_argument("--ctx-list", default="4096,8192,16384,32768",
                   help="context values for the sweep table (default 4096,8192,16384,32768)")
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of tables")
    p.add_argument("--list-quants", action="store_true", help="print the quantization table and exit")

    args = p.parse_args(argv)

    for name, value in (("--params", args.params), ("--vram", args.vram),
                        ("--overhead", args.overhead)):
        if value <= 0:
            sys.stderr.write("error: %s must be > 0\n" % name)
            sys.exit(3)
    for name, value in (("--layers", args.layers), ("--kv-heads", args.kv_heads),
                        ("--head-dim", args.head_dim), ("--ctx", args.ctx),
                        ("--parallel", args.parallel)):
        if value <= 0:
            sys.stderr.write("error: %s must be a positive integer\n" % name)
            sys.exit(3)
    try:
        args.ctx_list = [int(x) for x in str(args.ctx_list).split(",") if x.strip()]
    except ValueError:
        sys.stderr.write("error: --ctx-list must be comma-separated integers\n")
        sys.exit(3)
    return args


def main(argv) -> int:
    if "--list-quants" in argv:
        print("quant      effective bits   weights per 1B params (GiB)")
        for name, bits in QUANTS:
            print("%-10s %14.2f   %10.3f" % (name, bits, bits * PARAM_TO_GIB))
        print("\nKV bytes per cached element: " + ", ".join(
            "%s=%.3f" % (k, v) for k, v in sorted(KV_BYTES.items())))
        return 0

    args = parse_args(argv)
    kv_dim = args.kv_heads * args.head_dim
    rows = build_rows(args)

    best = next((r for r in rows if r["fits"]), None)
    sweep_bits = best["bits"] if best else QUANTS[-1][1]
    sweep = ctx_sweep(args, sweep_bits, args.ctx_list)

    if args.json:
        print(json.dumps(
            {
                "inputs": {
                    "params_b": args.params, "layers": args.layers,
                    "kv_heads": args.kv_heads, "head_dim": args.head_dim,
                    "kv_dim": kv_dim, "ctx": args.ctx, "parallel": args.parallel,
                    "vram_gib": args.vram, "kv_dtype": args.kv_dtype,
                    "overhead_gib": args.overhead,
                },
                "tiers": rows,
                "context_sweep": {"quant": best["quant"] if best else QUANTS[-1][0], "rows": sweep},
                "verdict": "fits" if best else "no-tier-fits",
            },
            indent=2,
        ))
        return 0 if best else 2

    print("ModelDeck VRAM budget (estimate, verify on the target machine)")
    print("  model      : %.1fB params, %d layers, kv_dim=%d (%d heads x %d)"
          % (args.params, args.layers, kv_dim, args.kv_heads, args.head_dim))
    print("  workload   : ctx=%d, slots=%d, kv=%s, overhead=%.2f GiB"
          % (args.ctx, args.parallel, args.kv_dtype, args.overhead))
    print("  budget     : %.2f GiB usable VRAM" % args.vram)
    print()
    print("%-8s %6s %9s %9s %9s %8s  %s"
          % ("quant", "bits", "weights", "kv", "total", "free", "verdict"))
    for r in rows:
        pct = 100.0 * r["total_gib"] / args.vram
        mark = ("fits(" + band(pct) + ")") if r["fits"] else "no-fit"
        print("%-8s %6.2f %9.2f %9.2f %9.2f %8.2f  %s"
              % (r["quant"], r["bits"], r["weights_gib"], r["kv_gib"],
                 r["total_gib"], r["headroom_gib"], mark))
    print()
    if best:
        print("Largest fitting tier: %s (%.2f GiB total, %.1f%% of budget)"
              % (best["quant"], best["total_gib"], 100.0 * best["total_gib"] / args.vram))
    else:
        print("No tier fits. Reduce context, use q8_0 KV, or lower the parameter count.")
    print()
    print("Context sweep at %s (weights %.2f GiB, kv=%s, slots=%d):"
          % (best["quant"] if best else QUANTS[-1][0],
             weights_gib(args.params, sweep_bits), args.kv_dtype, args.parallel))
    print("%-9s %9s %9s %8s  %s" % ("ctx", "kv", "total", "free", "verdict"))
    for s in sweep:
        mark = "fits" if s["fits"] else "no-fit"
        print("%-9d %9.2f %9.2f %8.2f  %s"
              % (s["ctx"], s["kv_gib"], s["total_gib"], s["headroom_gib"], mark))
    print()
    print("Rule of thumb: keep 1-2 GiB free for the desktop/compositor and for KV growth.")
    print("KV grows linearly with context and with parallel slots; recompute when either changes.")
    return 0 if best else 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.stderr.write("interrupted\n")
        sys.exit(130)
