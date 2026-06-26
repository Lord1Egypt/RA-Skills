#!/usr/bin/env python3
"""
GPU 算力方案构建器
根据客户需求自动构建 GPU 算力方案
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class GPUConfig:
    """GPU 配置"""
    model: str
    vram_gb: int
    cuda_cores: int
    tflops_fp16: float
    tflops_fp32: float
    monthly_cost: float  # 美元/月
    hourly_cost: float   # 美元/小时


@dataclass
class Solution:
    """算力方案"""
    workload: str
    scale: str
    budget: float
    recommended_gpus: List[Dict]
    total_cost_monthly: float
    total_cost_hourly: float
    scaling_roadmap: List[Dict]
    recommendations: List[str]


# GPU 数据库
GPU_DATABASE = {
    "H100": GPUConfig(
        model="NVIDIA H100",
        vram_gb=80,
        cuda_cores=16896,
        tflops_fp16=989.4,
        tflops_fp32=494.7,
        monthly_cost=1999.0,
        hourly_cost=2.99
    ),
    "H100_NVLINK": GPUConfig(
        model="NVIDIA H100 NVLink",
        vram_gb=80,
        cuda_cores=16896,
        tflops_fp16=1978.8,
        tflops_fp32=989.4,
        monthly_cost=3999.0,
        hourly_cost=5.99
    ),
    "A100_40GB": GPUConfig(
        model="NVIDIA A100 40GB",
        vram_gb=40,
        cuda_cores=6912,
        tflops_fp16=312.0,
        tflops_fp32=156.0,
        monthly_cost=999.0,
        hourly_cost=1.49
    ),
    "A100_80GB": GPUConfig(
        model="NVIDIA A100 80GB",
        vram_gb=80,
        cuda_cores=6912,
        tflops_fp16=312.0,
        tflops_fp32=156.0,
        monthly_cost=1299.0,
        hourly_cost=1.99
    ),
    "L40S": GPUConfig(
        model="NVIDIA L40S",
        vram_gb=48,
        cuda_cores=18176,
        tflops_fp16=362.0,
        tflops_fp32=181.0,
        monthly_cost=699.0,
        hourly_cost=1.05
    ),
    "A10G": GPUConfig(
        model="NVIDIA A10G",
        vram_gb=24,
        cuda_cores=9216,
        tflops_fp16=125.0,
        tflops_fp32=62.5,
        monthly_cost=299.0,
        hourly_cost=0.45
    ),
    "RTX_4090": GPUConfig(
        model="NVIDIA RTX 4090",
        vram_gb=24,
        cuda_cores=16384,
        tflops_fp16=165.0,
        tflops_fp32=82.5,
        monthly_cost=199.0,
        hourly_cost=0.30
    ),
    "RTX_A6000": GPUConfig(
        model="NVIDIA RTX A6000",
        vram_gb=48,
        cuda_cores=10752,
        tflops_fp16=154.8,
        tflops_fp32=77.4,
        monthly_cost=349.0,
        hourly_cost=0.52
    ),
}


# 工作负载推荐配置
WORKLOAD_RECOMMENDATIONS = {
    "training": {
        "name": "模型训练",
        "description": "大语言模型训练、深度学习训练",
        "priority_gpus": ["H100", "H100_NVLINK", "A100_80GB", "A100_40GB"],
        "min_gpu_count": 4,
        "recommended_count": 8,
        "networking": "InfiniBand 或 NVLink 互联",
        "storage": "高性能并行文件系统",
    },
    "inference": {
        "name": "模型推理",
        "description": "在线推理服务、API 部署",
        "priority_gpus": ["L40S", "A10G", "A100_40GB", "H100"],
        "min_gpu_count": 1,
        "recommended_count": 2,
        "networking": "标准以太网",
        "storage": "高速本地 SSD",
    },
    "finetuning": {
        "name": "模型微调",
        "description": "LoRA/QLoRA 微调、领域适配",
        "priority_gpus": ["A100_40GB", "A100_80GB", "L40S", "RTX_A6000"],
        "min_gpu_count": 1,
        "recommended_count": 2,
        "networking": "标准以太网",
        "storage": "高速 SSD 存储",
    },
    "inference_batch": {
        "name": "批量推理",
        "description": "离线批量处理、数据标注",
        "priority_gpus": ["RTX_4090", "A10G", "L40S"],
        "min_gpu_count": 2,
        "recommended_count": 4,
        "networking": "标准以太网",
        "storage": "大容量存储",
    },
    "development": {
        "name": "开发测试",
        "description": "模型开发、实验调试",
        "priority_gpus": ["RTX_4090", "A10G", "RTX_A6000"],
        "min_gpu_count": 1,
        "recommended_count": 1,
        "networking": "标准以太网",
        "storage": "标准 SSD",
    },
}


# 规模定义
SCALE_DEFINITIONS = {
    "small": {
        "name": "小型",
        "gpu_multiplier": 1,
        "description": "起步/实验阶段",
        "max_budget": 5000,
    },
    "medium": {
        "name": "中型",
        "gpu_multiplier": 2,
        "description": "生产环境/中等负载",
        "max_budget": 20000,
    },
    "large": {
        "name": "大型",
        "gpu_multiplier": 4,
        "description": "大规模训练/推理",
        "max_budget": 100000,
    },
    "enterprise": {
        "name": "企业级",
        "gpu_multiplier": 8,
        "description": "超大规模/集群部署",
        "max_budget": 500000,
    },
}


def get_gpu_recommendations(workload: str, scale: str, budget: float) -> List[Dict]:
    """根据工作负载和规模获取 GPU 推荐"""
    workload_config = WORKLOAD_RECOMMENDATIONS.get(workload, WORKLOAD_RECOMMENDATIONS["training"])
    scale_config = SCALE_DEFINITIONS.get(scale, SCALE_DEFINITIONS["medium"])
    
    recommendations = []
    base_count = workload_config["recommended_count"]
    gpu_count = base_count * scale_config["gpu_multiplier"]
    
    for gpu_key in workload_config["priority_gpus"]:
        if gpu_key not in GPU_DATABASE:
            continue
            
        gpu = GPU_DATABASE[gpu_key]
        monthly_total = gpu.monthly_cost * gpu_count
        hourly_total = gpu.hourly_cost * gpu_count
        
        # 检查预算
        if monthly_total > budget * 1.5:  # 允许 50% 超预算
            continue
            
        fit_score = 100
        if monthly_total > budget:
            fit_score = max(0, 100 - int((monthly_total - budget) / budget * 50))
        
        recommendations.append({
            "gpu_model": gpu.model,
            "gpu_key": gpu_key,
            "quantity": gpu_count,
            "vram_total_gb": gpu.vram_gb * gpu_count,
            "tflops_fp16_total": gpu.tflops_fp16 * gpu_count,
            "monthly_cost": monthly_total,
            "hourly_cost": hourly_total,
            "fit_score": fit_score,
            "within_budget": monthly_total <= budget,
        })
    
    # 按性价比排序
    recommendations.sort(key=lambda x: (-x["fit_score"], x["monthly_cost"]))
    return recommendations[:3]  # 返回前3个推荐


def generate_scaling_roadmap(workload: str, current_scale: str) -> List[Dict]:
    """生成扩展路线图"""
    scales = ["small", "medium", "large", "enterprise"]
    current_index = scales.index(current_scale) if current_scale in scales else 1
    
    roadmap = []
    for i in range(current_index, len(scales)):
        scale = scales[i]
        scale_config = SCALE_DEFINITIONS[scale]
        workload_config = WORKLOAD_RECOMMENDATIONS[workload]
        gpu_count = workload_config["recommended_count"] * scale_config["gpu_multiplier"]
        
        roadmap.append({
            "phase": f"阶段 {i - current_index + 1}",
            "scale": scale,
            "scale_name": scale_config["name"],
            "gpu_count": gpu_count,
            "description": scale_config["description"],
            "estimated_monthly_cost": f"${scale_config['max_budget']:,}",
        })
    
    return roadmap


def generate_recommendations(workload: str, scale: str, budget: float, recommendations: List[Dict]) -> List[str]:
    """生成建议列表"""
    tips = []
    workload_config = WORKLOAD_RECOMMENDATIONS.get(workload, WORKLOAD_RECOMMENDATIONS["training"])
    
    if not recommendations:
        tips.append("⚠️ 当前预算可能不足以支持该工作负载，建议增加预算或选择更小规模")
        return tips
    
    best_fit = recommendations[0]
    
    tips.append(f"✅ 推荐配置: {best_fit['quantity']} x {best_fit['gpu_model']}")
    tips.append(f"💰 预估月成本: ${best_fit['monthly_cost']:,.2f}")
    
    if not best_fit["within_budget"]:
        tips.append(f"⚠️ 推荐配置超出预算 ${best_fit['monthly_cost'] - budget:,.2f}，建议调整规模或预算")
    
    tips.append(f"🔧 网络配置: {workload_config['networking']}")
    tips.append(f"💾 存储建议: {workload_config['storage']}")
    
    if workload in ["training", "finetuning"]:
        tips.append("💡 建议使用分布式训练框架 (DeepSpeed/FSDP/Megatron-LM)")
    
    if workload == "inference":
        tips.append("💡 建议使用 TensorRT-LLM 或 vLLM 优化推理性能")
    
    if scale in ["large", "enterprise"]:
        tips.append("💡 考虑使用 Kubernetes + GPU Operator 进行集群管理")
    
    return tips


def build_solution(workload: str, budget: float, scale: str) -> Solution:
    """构建完整的算力方案"""
    recommendations = get_gpu_recommendations(workload, scale, budget)
    roadmap = generate_scaling_roadmap(workload, scale)
    tips = generate_recommendations(workload, scale, budget, recommendations)
    
    total_monthly = recommendations[0]["monthly_cost"] if recommendations else 0
    total_hourly = recommendations[0]["hourly_cost"] if recommendations else 0
    
    return Solution(
        workload=workload,
        scale=scale,
        budget=budget,
        recommended_gpus=recommendations,
        total_cost_monthly=total_monthly,
        total_cost_hourly=total_hourly,
        scaling_roadmap=roadmap,
        recommendations=tips
    )


def format_markdown(solution: Solution) -> str:
    """格式化为 Markdown 输出"""
    workload_config = WORKLOAD_RECOMMENDATIONS.get(solution.workload, {})
    scale_config = SCALE_DEFINITIONS.get(solution.scale, {})
    
    lines = [
        "# GPU 算力方案建议书",
        "",
        "## 📋 需求概览",
        "",
        f"| 项目 | 内容 |",
        f"|------|------|",
        f"| 工作负载 | {workload_config.get('name', solution.workload)} |",
        f"| 规模 | {scale_config.get('name', solution.scale)} |",
        f"| 预算 | ${solution.budget:,.2f}/月 |",
        f"| 描述 | {workload_config.get('description', 'N/A')} |",
        "",
        "## 🎯 GPU 配置推荐",
        "",
    ]
    
    if solution.recommended_gpus:
        lines.extend([
            "| GPU 型号 | 数量 | 总显存 | FP16算力 | 月成本 | 预算内 |",
            "|----------|------|--------|----------|--------|--------|",
        ])
        for gpu in solution.recommended_gpus:
            within = "✅" if gpu["within_budget"] else "⚠️"
            lines.append(
                f"| {gpu['gpu_model']} | {gpu['quantity']} | {gpu['vram_total_gb']}GB | "
                f"{gpu['tflops_fp16_total']:.1f} TFLOPS | ${gpu['monthly_cost']:,.2f} | {within} |"
            )
    else:
        lines.append("_暂无符合条件的配置_")
    
    lines.extend([
        "",
        "## 💰 成本估算",
        "",
        f"- **月度成本**: ${solution.total_cost_monthly:,.2f}",
        f"- **小时成本**: ${solution.total_cost_hourly:.2f}",
        f"- **年度预估**: ${solution.total_cost_monthly * 12:,.2f}",
        "",
        "## 📈 扩展路线图",
        "",
        "| 阶段 | 规模 | GPU数量 | 描述 | 预估月成本 |",
        "|------|------|---------|------|------------|",
    ])
    
    for item in solution.scaling_roadmap:
        lines.append(
            f"| {item['phase']} | {item['scale_name']} | {item['gpu_count']} | "
            f"{item['description']} | {item['estimated_monthly_cost']} |"
        )
    
    lines.extend([
        "",
        "## 💡 建议与注意事项",
        "",
    ])
    for tip in solution.recommendations:
        lines.append(f"- {tip}")
    
    lines.extend([
        "",
        "---",
        "*由 pans-gpu-solution-builder 自动生成*",
    ])
    
    return "\n".join(lines)


def format_json(solution: Solution) -> str:
    """格式化为 JSON 输出"""
    data = {
        "workload": solution.workload,
        "scale": solution.scale,
        "budget": solution.budget,
        "total_cost": {
            "monthly": solution.total_cost_monthly,
            "hourly": solution.total_cost_hourly,
            "yearly": solution.total_cost_monthly * 12,
        },
        "recommended_gpus": solution.recommended_gpus,
        "scaling_roadmap": solution.scaling_roadmap,
        "recommendations": solution.recommendations,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="GPU 算力方案构建器 - 根据客户需求自动构建 GPU 算力方案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python solution.py --workload training --budget 10000 --scale medium
  python solution.py --workload inference --budget 5000 --scale small --format json
  python solution.py --workload finetuning --budget 8000 --scale medium --output solution.md
        """
    )
    
    parser.add_argument(
        "--workload",
        type=str,
        required=True,
        choices=list(WORKLOAD_RECOMMENDATIONS.keys()),
        help="工作负载类型"
    )
    
    parser.add_argument(
        "--budget",
        type=float,
        required=True,
        help="月度预算 (USD)"
    )
    
    parser.add_argument(
        "--scale",
        type=str,
        required=True,
        choices=list(SCALE_DEFINITIONS.keys()),
        help="部署规模"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        default="markdown",
        choices=["json", "markdown"],
        help="输出格式 (默认: markdown)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径 (默认输出到 stdout)"
    )
    
    args = parser.parse_args()
    
    # 构建方案
    solution = build_solution(args.workload, args.budget, args.scale)
    
    # 格式化输出
    if args.format == "json":
        output = format_json(solution)
    else:
        output = format_markdown(solution)
    
    # 输出到文件或 stdout
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"方案已保存至: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
