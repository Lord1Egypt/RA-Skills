---
name: pans-gpu-solution-builder
description: |
  GPU 算力方案构建器。根据客户的工作负载类型（训练/推理/微调/批量推理/开发测试）、
  部署规模（小型/中型/大型/企业级）和月度预算，自动推荐最优 GPU 配置
  （H100/A100/L40S/A10G/RTX 4090 等），生成含 GPU 型号、数量、算力、
  月度/小时成本的配置表、扩展路线图和技术建议，输出 Markdown 或 JSON 格式。
  触发词：GPU方案, 算力配置, 方案构建, GPU推荐, 配置推荐,
  solution builder, GPU选型, 算力方案
---

# Pans Gpu Solution Builder

## Overview

GPU 算力方案构建器。根据客户需求自动构建 GPU 算力方案。

## 工作负载类型

| 类型 | 说明 | 推荐 GPU |
|------|------|----------|
| `training` | 大语言模型训练、深度学习训练 | H100, A100 80GB |
| `inference` | 在线推理服务、API 部署 | L40S, A10G, A100 |
| `finetuning` | LoRA/QLoRA 微调、领域适配 | A100 40GB, L40S |
| `inference_batch` | 离线批量处理、数据标注 | RTX 4090, A10G |
| `development` | 模型开发、实验调试 | RTX 4090, A10G |

## 规模定义

| 规模 | 说明 | 最大预算 |
|------|------|----------|
| `small` | 起步/实验阶段 | $5,000/月 |
| `medium` | 生产环境/中等负载 | $20,000/月 |
| `large` | 大规模训练/推理 | $100,000/月 |
| `enterprise` | 超大规模/集群部署 | $500,000/月 |

## 使用方法

```bash
# 生成训练方案（中规模，$10,000预算）
python3 scripts/solution.py --workload training --budget 10000 --scale medium

# 生成推理方案（小型，$5,000预算）
python3 scripts/solution.py --workload inference --budget 5000 --scale small --format json

# 生成微调方案，输出到文件
python3 scripts/solution.py --workload finetuning --budget 8000 --scale medium --output solution.md
```

## 输出内容

- **GPU 配置推荐表**：型号、数量、总显存、算力、月成本、预算匹配评分
- **成本估算**：月度、小时、年度预估
- **扩展路线图**：从当前规模到更大规模的升级路径
- **技术建议**：网络配置、存储方案、分布式训练框架、推理优化建议
