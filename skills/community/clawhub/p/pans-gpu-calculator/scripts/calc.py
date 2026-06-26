#!/usr/bin/env python3
"""AI算力销售GPU配置计算器

输入模型参数量和需求，自动推荐最优GPU配置并估算成本。
支持训练和推理场景，覆盖H100/A100/L40S/A10G等主流GPU。
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class GPU:
    """GPU型号数据"""
    name: str
    memory_gb: int
    tflops_fp16: float
    price_per_hour: float
    memory_type: str


# 支持的GPU型号
GPUS = [
    GPU("H100", 80, 989, 2.5, "HBM3"),
    GPU("A100-80G", 80, 624, 1.8, "HBM2e"),
    GPU("A100-40G", 40, 624, 1.2, "HBM2e"),
    GPU("L40S", 48, 362, 0.8, "HBM3"),
    GPU("A10G", 24, 200, 0.5, "HBM2"),
]


def parse_params(params_str: str) -> int:
    """解析参数量字符串，如 7B, 70B, 405B"""
    params_str = params_str.upper().strip()
    if params_str.endswith("B"):
        return int(float(params_str[:-1]) * 1e9)
    elif params_str.endswith("M"):
        return int(float(params_str[:-1]) * 1e6)
    else:
        return int(float(params_str))


def estimate_memory(params: int, batch_size: int = 1, mode: str = "inference") -> float:
    """估算模型内存需求(GB)
    
    模型内存 = 参数量 × 2 bytes (FP16) + KV cache + 激活值
    - KV cache ≈ 2 × 层数 × hidden_dim × batch × seq_len
    - 激活值 ≈ 模型参数 × batch × 0.1 (推理) 或 × 1 (训练)
    
    简化估算:
    - 推理: 参数量 × 2 + 参数量 × 0.2 × batch (GB)
    - 训练: 参数量 × 2 × 4 (优化器状态) + 激活值
    """
    params_gb = params * 2 / 1e9  # FP16权重
    
    if mode == "inference":
        # KV cache和激活值估算
        overhead = params_gb * 0.2 * batch_size
        return params_gb + overhead
    else:
        # 训练: 权重 + 梯度 + 优化器状态 + 激活值
        # Adam: 2倍权重(梯度) + 2倍权重(m,v) = 4倍
        optimizer_state = params_gb * 2  # m和v
        gradients = params_gb
        activations = params_gb * batch_size * 0.5
        return params_gb + gradients + optimizer_state + activations


def calc_min_gpus(memory_gb: float, gpu: GPU) -> int:
    """计算最小GPU数量"""
    return math.ceil(memory_gb / gpu.memory_gb)


def estimate_inference_throughput(
    gpu: GPU, 
    params: int, 
    num_gpus: int,
    batch_size: int = 1,
    utilization: float = 0.4
) -> float:
    """估算推理吞吐(tokens/sec)
    
    吞吐 = GPU TFLOPS × 利用率 × GPU数 / 模型FLOPs_per_token
    模型FLOPs_per_token ≈ 2 × 参数量 (前向传播)
    """
    flops_per_token = 2 * params
    total_tflops = gpu.tflops_fp16 * num_gpus * utilization
    throughput = total_tflops * 1e12 / flops_per_token
    return throughput


def estimate_training_time(
    gpu: GPU,
    params: int,
    num_gpus: int,
    tokens: int,
    utilization: float = 0.3
) -> float:
    """估算训练时间(小时)
    
    训练时间 = 8 × 参数量 × token数 / (GPU数 × TFLOPS × 利用率)
    系数8 = 6 (前向+反向+优化) × 1.33 (通信开销)
    """
    total_flops = 8 * params * tokens
    total_tflops = gpu.tflops_fp16 * num_gpus * utilization
    seconds = total_flops / (total_tflops * 1e12)
    return seconds / 3600


def estimate_latency(throughput: float, batch_size: int = 1) -> float:
    """估算延迟(ms)"""
    if throughput <= 0:
        return float("inf")
    return 1000 * batch_size / throughput


def recommend_gpu(
    params: int,
    mode: str,
    batch_size: int = 1,
    latency_ms: Optional[float] = None,
    preferred_gpu: Optional[str] = None
) -> list[dict]:
    """推荐GPU配置
    
    返回所有GPU的评估结果，按成本效益排序
    """
    memory_needed = estimate_memory(params, batch_size, mode)
    results = []
    
    for gpu in GPUS:
        if preferred_gpu and gpu.name != preferred_gpu:
            continue
            
        num_gpus = calc_min_gpus(memory_needed, gpu)
        hourly_cost = num_gpus * gpu.price_per_hour
        monthly_cost = hourly_cost * 730
        
        if mode == "inference":
            throughput = estimate_inference_throughput(gpu, params, num_gpus, batch_size)
            latency = estimate_latency(throughput, batch_size)
            meets_latency = latency_ms is None or latency <= latency_ms
            
            results.append({
                "gpu": gpu.name,
                "memory": f"{gpu.memory_gb}GB {gpu.memory_type}",
                "num_gpus": num_gpus,
                "hourly_cost": hourly_cost,
                "monthly_cost": monthly_cost,
                "throughput_tokens_per_sec": round(throughput, 1),
                "latency_ms": round(latency, 1),
                "meets_latency": meets_latency,
                "memory_needed_gb": round(memory_needed, 1),
            })
        else:
            results.append({
                "gpu": gpu.name,
                "memory": f"{gpu.memory_gb}GB {gpu.memory_type}",
                "num_gpus": num_gpus,
                "hourly_cost": hourly_cost,
                "monthly_cost": monthly_cost,
                "memory_needed_gb": round(memory_needed, 1),
            })
    
    # 排序: 按月成本升序
    results.sort(key=lambda x: x["monthly_cost"])
    return results


def format_table(results: list[dict], mode: str) -> str:
    """格式化表格输出"""
    lines = []
    
    if mode == "inference":
        header = f"{'GPU':<12} {'Memory':<15} {'Count':>6} {'$/hr':>8} {'$/mo':>10} {'tok/s':>8} {'Latency':>10}"
        lines.append(header)
        lines.append("-" * len(header))
        
        for r in results:
            flag = "" if r.get("meets_latency", True) else " ⚠️"
            lines.append(
                f"{r['gpu']:<12} {r['memory']:<15} {r['num_gpus']:>6} "
                f"${r['hourly_cost']:>6.2f} ${r['monthly_cost']:>8.0f} "
                f"{r['throughput_tokens_per_sec']:>8} {r['latency_ms']:>6.1f}ms{flag}"
            )
    else:
        header = f"{'GPU':<12} {'Memory':<15} {'Count':>6} {'$/hr':>8} {'$/mo':>10}"
        lines.append(header)
        lines.append("-" * len(header))
        
        for r in results:
            lines.append(
                f"{r['gpu']:<12} {r['memory']:<15} {r['num_gpus']:>6} "
                f"${r['hourly_cost']:>6.2f} ${r['monthly_cost']:>8.0f}"
            )
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="AI算力销售GPU配置计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 推理70B模型，对比所有GPU
  calc.py --params 70B --mode inference --compare
  
  # 训练7B模型，1T tokens
  calc.py --params 7B --mode train --tokens 1T --compare
  
  # 指定GPU型号
  calc.py --params 70B --mode inference --gpu H100 --batch 8
  
  # JSON输出
  calc.py --params 405B --mode inference --json
"""
    )
    
    parser.add_argument("--params", required=True, help="模型参数量 (如 7B, 70B, 405B)")
    parser.add_argument("--mode", choices=["train", "inference"], default="inference",
                        help="模式: train(训练) 或 inference(推理)")
    parser.add_argument("--gpu", help="指定GPU型号 (H100, A100-80G, A100-40G, L40S, A10G)")
    parser.add_argument("--batch", type=int, default=1, help="Batch size")
    parser.add_argument("--latency", type=float, help="目标延迟(ms)")
    parser.add_argument("--tokens", help="训练token数 (如 1T, 100B)")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--compare", action="store_true", help="对比所有GPU型号")
    
    args = parser.parse_args()
    
    params = parse_params(args.params)
    preferred_gpu = args.gpu if not args.compare else None
    
    results = recommend_gpu(
        params=params,
        mode=args.mode,
        batch_size=args.batch,
        latency_ms=args.latency,
        preferred_gpu=preferred_gpu
    )
    
    if args.mode == "train" and args.tokens:
        # 解析token数
        tokens_str = args.tokens.upper()
        if tokens_str.endswith("T"):
            tokens = int(float(tokens_str[:-1]) * 1e12)
        elif tokens_str.endswith("B"):
            tokens = int(float(tokens_str[:-1]) * 1e9)
        else:
            tokens = int(float(tokens_str))
        
        # 计算训练时间
        for r in results:
            gpu = next(g for g in GPUS if g.name == r["gpu"])
            hours = estimate_training_time(gpu, params, r["num_gpus"], tokens)
            r["training_hours"] = round(hours, 1)
            r["training_days"] = round(hours / 24, 1)
            r["total_cost"] = round(hours * r["hourly_cost"], 2)
    
    if args.json:
        output = {
            "params": args.params,
            "params_count": params,
            "mode": args.mode,
            "batch_size": args.batch,
            "memory_needed_gb": results[0]["memory_needed_gb"] if results else 0,
            "recommendations": results
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"模型: {args.params} ({params/1e9:.1f}B参数)")
        print(f"模式: {args.mode}")
        print(f"内存需求: {results[0]['memory_needed_gb']} GB")
        print(f"{'='*60}\n")
        
        print(format_table(results, args.mode))
        
        if args.mode == "train" and args.tokens:
            print(f"\n训练配置 ({args.tokens} tokens):")
            print(f"{'GPU':<12} {'时间':>12} {'总成本':>12}")
            print("-" * 36)
            for r in results:
                print(f"{r['gpu']:<12} {r['training_days']:>6.1f} 天 ${r['total_cost']:>10.0f}")
        
        print(f"\n推荐: {results[0]['gpu']} × {results[0]['num_gpus']}")
        print(f"月成本: ${results[0]['monthly_cost']:,.0f}")


if __name__ == "__main__":
    main()
