#!/usr/bin/env python3.11
"""
AI算力竞品对比分析器
对比 AWS / GCP / Azure / 火山引擎 / 阿里云 GPU 实例定价
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional

# ─────────────────────────────────────────────
# 数据定义
# ─────────────────────────────────────────────

GPU_DATA = [
    # AWS
    {
        "provider": "AWS",
        "instance": "p5en.48xlarge",
        "gpu": "H100 SXM 80GB",
        "vram": "80GB HBM3",
        "vcpus": 192,
        "memory_gb": 2048,
        "ondemand": 98.32,
        "1yr": 58.99,
        "3yr": 44.24,
        "network": "3200 Gbps",
        "storage": "EBS Only",
        "region": "us-east-1",
    },
    {
        "provider": "AWS",
        "instance": "p4d.24xlarge",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 96,
        "memory_gb": 1152,
        "ondemand": 40.50,
        "1yr": 24.30,
        "3yr": 18.23,
        "network": "400 Gbps",
        "storage": "8TB NVMe",
        "region": "us-east-1",
    },
    {
        "provider": "AWS",
        "instance": "p4de.24xlarge",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 96,
        "memory_gb": 1152,
        "ondemand": 55.86,
        "1yr": 33.52,
        "3yr": 25.14,
        "network": "400 Gbps",
        "storage": "8TB NVMe",
        "region": "us-east-1",
    },
    {
        "provider": "AWS",
        "instance": "g6.48xlarge",
        "gpu": "L40S",
        "vram": "48GB",
        "vcpus": 192,
        "memory_gb": 2048,
        "ondemand": 22.05,
        "1yr": 13.23,
        "3yr": 9.92,
        "network": "3200 Gbps",
        "storage": "EBS Only",
        "region": "us-east-1",
    },
    {
        "provider": "AWS",
        "instance": "g5.48xlarge",
        "gpu": "A10G",
        "vram": "24GB",
        "vcpus": 192,
        "memory_gb": 2048,
        "ondemand": 12.24,
        "1yr": 7.34,
        "3yr": 5.51,
        "network": "3200 Gbps",
        "storage": "7.6TB NVMe",
        "region": "us-east-1",
    },
    # GCP
    {
        "provider": "GCP",
        "instance": "a3-highgpu-8g",
        "gpu": "H100 SXM 80GB",
        "vram": "80GB HBM3",
        "vcpus": 208,
        "memory_gb": 2048,
        "ondemand": 105.46,
        "1yr": 63.28,
        "3yr": 47.46,
        "network": "200 Gbps",
        "storage": "Clustered",
        "region": "us-central1",
    },
    {
        "provider": "GCP",
        "instance": "a2-highgpu-1g",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 12,
        "memory_gb": 170,
        "ondemand": 11.36,
        "1yr": 6.82,
        "3yr": 5.11,
        "network": "32 Gbps",
        "storage": "375GB NVMe",
        "region": "us-central1",
    },
    {
        "provider": "GCP",
        "instance": "a2-highgpu-4g",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 48,
        "memory_gb": 680,
        "ondemand": 40.33,
        "1yr": 24.20,
        "3yr": 18.15,
        "network": "100 Gbps",
        "storage": "1500GB NVMe",
        "region": "us-central1",
    },
    {
        "provider": "GCP",
        "instance": "g2-standard-8",
        "gpu": "L4",
        "vram": "24GB",
        "vcpus": 32,
        "memory_gb": 128,
        "ondemand": 2.44,
        "1yr": 1.46,
        "3yr": 1.10,
        "network": "20 Gbps",
        "storage": "300GB NVMe",
        "region": "us-central1",
    },
    # Azure
    {
        "provider": "Azure",
        "instance": "ND H100 v5",
        "gpu": "H100 SXM 80GB",
        "vram": "80GB HBM3",
        "vcpus": 224,
        "memory_gb": 2048,
        "ondemand": 104.40,
        "1yr": 62.64,
        "3yr": 46.98,
        "network": "3200 Gbps",
        "storage": "6.4TB NVMe",
        "region": "eastus",
    },
    {
        "provider": "Azure",
        "instance": "NC A100 v4",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 96,
        "memory_gb": 900,
        "ondemand": 39.82,
        "1yr": 23.89,
        "3yr": 17.92,
        "network": "80 Gbps",
        "storage": "2.88TB NVMe",
        "region": "eastus",
    },
    {
        "provider": "Azure",
        "instance": "NV L40s",
        "gpu": "L40S",
        "vram": "48GB",
        "vcpus": 72,
        "memory_gb": 900,
        "ondemand": 14.40,
        "1yr": 8.64,
        "3yr": 6.48,
        "network": "80 Gbps",
        "storage": "1.8TB NVMe",
        "region": "eastus",
    },
    # 火山引擎
    {
        "provider": "火山引擎",
        "instance": "ecs.vgh.8xlarge",
        "gpu": "H100 SXM 80GB",
        "vram": "80GB HBM3",
        "vcpus": 64,
        "memory_gb": 512,
        "ondemand": 12.50,
        "1yr": 7.50,
        "3yr": 5.00,
        "network": "100 Gbps",
        "storage": "500GB SSD",
        "region": "cn-beijing",
    },
    {
        "provider": "火山引擎",
        "instance": "ecs.vga.4xlarge",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 32,
        "memory_gb": 256,
        "ondemand": 6.20,
        "1yr": 3.72,
        "3yr": 2.48,
        "network": "50 Gbps",
        "storage": "500GB SSD",
        "region": "cn-beijing",
    },
    {
        "provider": "火山引擎",
        "instance": "ecs.vgl.4xlarge",
        "gpu": "L40S",
        "vram": "48GB",
        "vcpus": 32,
        "memory_gb": 256,
        "ondemand": 3.80,
        "1yr": 2.28,
        "3yr": 1.52,
        "network": "50 Gbps",
        "storage": "500GB SSD",
        "region": "cn-beijing",
    },
    # 阿里云
    {
        "provider": "阿里云",
        "instance": "ecs.ebmgn7.26xlarge",
        "gpu": "H100 SXM 80GB",
        "vram": "80GB HBM3",
        "vcpus": 104,
        "memory_gb": 768,
        "ondemand": 15.80,
        "1yr": 9.48,
        "3yr": 6.32,
        "network": "100 Gbps",
        "storage": "1TB SSD",
        "region": "cn-hangzhou",
    },
    {
        "provider": "阿里云",
        "instance": "ecs.gn7.26xlarge",
        "gpu": "A100 80GB",
        "vram": "80GB HBM2e",
        "vcpus": 104,
        "memory_gb": 768,
        "ondemand": 9.50,
        "1yr": 5.70,
        "3yr": 3.80,
        "network": "100 Gbps",
        "storage": "1TB SSD",
        "region": "cn-hangzhou",
    },
    {
        "provider": "阿里云",
        "instance": "ecs.gn7r.26xlarge",
        "gpu": "A100 40GB",
        "vram": "40GB HBM2e",
        "vcpus": 104,
        "memory_gb": 768,
        "ondemand": 7.20,
        "1yr": 4.32,
        "3yr": 2.88,
        "network": "100 Gbps",
        "storage": "1TB SSD",
        "region": "cn-hangzhou",
    },
    {
        "provider": "阿里云",
        "instance": "ecs.gn6v.10xlarge",
        "gpu": "V100 32GB",
        "vram": "32GB HBM2",
        "vcpus": 40,
        "memory_gb": 480,
        "ondemand": 4.50,
        "1yr": 2.70,
        "3yr": 1.80,
        "network": "50 Gbps",
        "storage": "500GB SSD",
        "region": "cn-hangzhou",
    },
]

# GPU 型号过滤映射
GPU_FILTER_MAP = {
    "h100": ["H100"],
    "a100": ["A100"],
    "l40s": ["L40S"],
    "a10g": ["A10G"],
    "l4": ["L4"],
    "v100": ["V100"],
    "all": [],
}

# 云厂商过滤映射
PROVIDER_FILTER_MAP = {
    "aws": ["AWS"],
    "gcp": ["GCP"],
    "azure": ["Azure"],
    "volc": ["火山引擎"],
    "ali": ["阿里云"],
    "all": [],
}

# 区域映射
REGION_FILTER_MAP = {
    "us-east": ["us-east-1", "eastus", "us-central1"],
    "us-west": ["us-west-3", "westus3"],
    "cn": ["cn-beijing", "cn-hangzhou", "cn-shanghai"],
    "eu": ["europe-west4", "westeurope"],
    "all": [],
}

# 颜色定义
COLORS = {
    "header": "\033[95m",
    "h100": "\033[91m",     # 红
    "a100": "\033[93m",     # 黄
    "l40s": "\033[92m",     # 绿
    "a10g": "\033[96m",     # 青色
    "l4": "\033[94m",       # 蓝
    "v100": "\033[90m",     # 灰
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}

PROVIDER_COLORS = {
    "AWS": "\033[91m",
    "GCP": "\033[94m",
    "Azure": "\033[96m",
    "火山引擎": "\033[92m",
    "阿里云": "\033[93m",
}

def get_gpu_color(gpu_name: str) -> str:
    for key, color in COLORS.items():
        if key != "header" and key != "reset" and key != "bold" and key != "dim":
            if key.upper() in gpu_name.upper():
                return color
    return ""

def get_provider_color(provider: str) -> str:
    return PROVIDER_COLORS.get(provider, "")

def filter_data(gpu: str, provider: str, region: str) -> list:
    gpu_filters = GPU_FILTER_MAP.get(gpu.lower(), [])

    # 支持逗号分隔的云厂商，如 "aws,gcp"
    provider_parts = [p.strip().lower() for p in provider.split(",")]
    provider_filters = []
    for p in provider_parts:
        found = PROVIDER_FILTER_MAP.get(p, [])
        provider_filters.extend(found)
    provider_filters = list(dict.fromkeys(provider_filters))  # 去重

    region_filters = REGION_FILTER_MAP.get(region.lower(), [])

    filtered = []
    for item in GPU_DATA:
        # GPU 过滤
        if gpu_filters:
            gpu_match = any(f.upper() in item["gpu"].upper() for f in gpu_filters)
            if not gpu_match:
                continue

        # 云厂商过滤
        if provider_filters:
            if item["provider"] not in provider_filters:
                continue

        # 区域过滤
        if region_filters:
            if item["region"] not in region_filters:
                continue

        filtered.append(item)

    return filtered

def format_price(val: float) -> str:
    return f"${val:.2f}"

def format_table(data: list, mode: str) -> str:
    if not data:
        return "No data found matching the filter criteria."

    # 表头
    header = [
        "Provider",
        "Instance",
        "GPU",
        "VRAM",
        "vCPUs",
        "Memory",
    ]
    if mode in ("pricing", "all"):
        header += ["On-Demand", "1yr Reserved", "3yr Reserved"]
    header += ["Network", "Storage", "Region"]

    # 计算列宽
    col_widths = [len(h) for h in header]
    rows = []
    for item in data:
        row = [
            item["provider"],
            item["instance"],
            item["gpu"],
            item["vram"],
            str(item["vcpus"]),
            f"{item['memory_gb']}GB",
        ]
        if mode in ("pricing", "all"):
            row += [
                format_price(item["ondemand"]),
                format_price(item["1yr"]),
                format_price(item["3yr"]),
            ]
        row += [item["network"], item["storage"], item["region"]]
        rows.append(row)
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    # 构建表格
    sep = "─" * (sum(col_widths) + len(col_widths) * 3 + 1)
    sep_mid = "┼".join("─" * (w + 2) for w in col_widths)

    lines = []
    # 表头
    header_cells = [h.center(w) for h, w in zip(header, col_widths)]
    lines.append(f"{COLORS['header']}{COLORS['bold']}┌{sep}─┐\033[0m")
    lines.append(f"{COLORS['header']}{COLORS['bold']}│ {' │ '.join(header_cells)} │\033[0m")
    lines.append(f"{COLORS['header']}{COLORS['bold']}├{sep_mid}─┤\033[0m")

    # 数据行
    for i, row in enumerate(rows):
        gpu_color = get_gpu_color(row[2])
        provider_color = get_provider_color(row[0])

        colored_cells = []
        for j, (cell, width) in enumerate(zip(row, col_widths)):
            if j == 0 and provider_color:
                colored_cells.append(f"{provider_color}{cell.center(width)}{COLORS['reset']}")
            elif j == 2 and gpu_color:
                colored_cells.append(f"{gpu_color}{cell.center(width)}{COLORS['reset']}")
            elif j >= 6 and j <= 8 and gpu_color:
                colored_cells.append(f"{gpu_color}{cell.center(width)}{COLORS['reset']}")
            else:
                colored_cells.append(cell.center(width))

        row_sep = "┤" if i < len(rows) - 1 else "┴"
        lines.append(f"│ {f' │ '.join(colored_cells)} │")
        lines.append(f"├{sep_mid}{row_sep}")

    lines[-1] = lines[-1].replace("┴", "┘")
    lines[-1] = lines[-1].replace("┼", "┤")

    return "\n".join(lines)

def format_json(data: list, mode: str) -> str:
    output = []
    for item in data:
        out = {
            "provider": item["provider"],
            "instance": item["instance"],
            "gpu": item["gpu"],
            "vram": item["vram"],
            "vcpus": item["vcpus"],
            "memory_gb": item["memory_gb"],
            "region": item["region"],
            "network": item["network"],
            "storage": item["storage"],
        }
        if mode in ("pricing", "all"):
            out.update({
                "ondemand_price_usd_per_hr": item["ondemand"],
                "reserved_1yr_usd_per_hr": item["1yr"],
                "reserved_3yr_usd_per_hr": item["3yr"],
            })
        output.append(out)
    return json.dumps(output, ensure_ascii=False, indent=2)

def format_csv(data: list, mode: str, writer) -> None:
    header = [
        "Provider", "Instance", "GPU", "VRAM", "vCPUs", "Memory (GB)",
        "Network", "Storage", "Region",
    ]
    if mode in ("pricing", "all"):
        header += ["On-Demand ($/hr)", "1yr Reserved ($/hr)", "3yr Reserved ($/hr)"]

    writer.writerow(header)
    for item in data:
        row = [
            item["provider"], item["instance"], item["gpu"], item["vram"],
            item["vcpus"], item["memory_gb"],
            item["network"], item["storage"], item["region"],
        ]
        if mode in ("pricing", "all"):
            row += [item["ondemand"], item["1yr"], item["3yr"]]
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(
        description="AI算力竞品对比分析器 — 对比 AWS/GCP/Azure/火山引擎/阿里云 GPU 定价",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 compare.py --gpu h100                        # H100 所有云厂商对比
  python3 compare.py --gpu a100 --format json          # A100 JSON 输出
  python3 compare.py --provider aws,gcp --format csv   # 仅 AWS 和 GCP
  python3 compare.py --gpu l40s --region cn            # 中国区 L40S
        """,
    )
    parser.add_argument(
        "--gpu", default="all",
        choices=["h100", "a100", "l40s", "a10g", "l4", "v100", "all"],
        help="GPU 型号过滤 (默认: all)",
    )
    parser.add_argument(
        "--provider", default="all",
        help="云厂商过滤，逗号分隔: aws,gcp,azure,volc,ali,all (默认: all)",
    )
    parser.add_argument(
        "--region", default="all",
        choices=["us-east", "us-west", "cn", "eu", "all"],
        help="区域过滤 (默认: all)",
    )
    parser.add_argument(
        "--mode", default="all",
        choices=["pricing", "specs", "all"],
        help="输出模式: pricing=仅价格, specs=仅规格, all=完整 (默认: all)",
    )
    parser.add_argument(
        "--format", default="table",
        choices=["table", "json", "csv"],
        help="输出格式 (默认: table)",
    )
    parser.add_argument(
        "--output", default=None,
        help="输出文件路径 (默认: stdout)",
    )

    args = parser.parse_args()

    # 解析 provider 参数（支持逗号分隔）
    provider_str = ",".join(p.strip().lower() for p in args.provider.split(","))

    data = filter_data(args.gpu, provider_str, args.region)

    if not data:
        print("No data found matching the filter criteria.", file=sys.stderr)
        sys.exit(1)

    # 输出
    if args.format == "table":
        output = format_table(data, args.mode)
    elif args.format == "json":
        output = format_json(data, args.mode)
    else:
        output = None  # CSV 单独处理

    if output:
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="") as f:
                f.write(output)
            print(f"✅  已导出到 {args.output} ({len(data)} 条记录)", file=sys.stderr)
        else:
            print(output)
    else:
        # CSV
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                format_csv(data, args.mode, writer)
            print(f"✅  已导出到 {args.output} ({len(data)} 条记录)", file=sys.stderr)
        else:
            writer = csv.writer(sys.stdout)
            format_csv(data, args.mode, writer)

if __name__ == "__main__":
    main()
