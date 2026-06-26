---
name: pans-competitor-compare
description: |
  AI算力销售竞品对比分析器。实时对比AWS/GCP/Azure/火山引擎/阿里云GPU定价和规格。
  支持按GPU型号、云厂商、区域筛选，输出对比表格或CSV。
  触发词：竞品对比, GPU价格, 云厂商对比, 定价分析, competitor analysis, pricing comparison
---

# pans-competitor-compare

AI算力销售竞品对比分析器 — 对比 AWS / GCP / Azure / 火山引擎 / 阿里云的 GPU 实例定价。

## 快速开始

```bash
# 查看 H100 所有云厂商对比（表格）
python3 scripts/compare.py --gpu h100

# 查看 A100 按量价格（JSON）
python3 scripts/compare.py --gpu a100 --mode pricing --format json

# 仅看 AWS 和 GCP
python3 scripts/compare.py --gpu all --provider aws,gcp --format table

# 导出 CSV
python3 scripts/compare.py --gpu h100 --format csv --output ~/Desktop/h100_comparison.csv
```

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--gpu` | GPU型号过滤：`h100` / `a100` / `l40s` / `a10g` / `l4` / `all` | `all` |
| `--provider` | 云厂商过滤：`aws` / `gcp` / `azure` / `volc` / `ali` / `all`，逗号分隔 | `all` |
| `--region` | 区域过滤：`us-east` / `us-west` / `cn` / `eu` / `all` | `all` |
| `--mode` | 输出模式：`pricing`（仅价格） / `specs`（仅规格） / `all`（完整） | `all` |
| `--format` | 输出格式：`table`（彩色表格） / `json` / `csv` | `table` |
| `--output` | 输出文件路径（可选，默认打印到 stdout） | - |

## 数据来源

- **AWS**: p5en (H100), p4d/p4de (A100 80GB), g6 (L40S), g5 (A10G)
- **GCP**: a3-highgpu-8g (H100), a2-highgpu (A100), g2-standard (L4)
- **Azure**: ND H100 v5, NC A100 v4, NV L40s
- **火山引擎**: H100 / A100 / L40S
- **阿里云**: H100 / A100 80GB / A100 40GB / V100 / A10

## 输出字段

| 字段 | 说明 |
|------|------|
| `provider` | 云厂商 |
| `instance` | 实例名称 |
| `gpu` | GPU型号 |
| `vram` | 显存容量 |
| `vcpus` | vCPU数量 |
| `memory` | 内存（GB） |
| `ondemand` | 按量付费价格（$/hr） |
| `1yr` | 1年预留实例价格（$/hr） |
| `3yr` | 3年预留实例价格（$/hr） |
| `network` | 网络带宽 |
| `storage` | 本地存储 |
| `region` | 适用区域 |

## 价格参考

> ⚠️ 价格数据基于 2026-04 参考价，实际价格以各云厂商官网为准。
> AWS/GCP/Azure 为美区价格（us-east-1 / us-central1 / eastus）。
> 火山引擎/阿里云为中国区参考价。
