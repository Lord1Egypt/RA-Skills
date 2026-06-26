---
name: pose-transfer
description: AI-powered fashion model pose transfer tool. Generate pose variations of a model/product image using reference pose images while keeping clothing and background consistent.
dependency:
  python:
    - fal-client>=0.8.0
requires:
  - FAL_KEY environment variable
  - Python 3.8+
---

# Pose Transfer

AI 姿态迁移工具 —— 给模特换姿势，保持服装和背景不变。

## 使用方法

```bash
python3 scripts/generate.py \
  --original "/path/to/model.jpg" \
  --poses "/path/to/pose.jpg" \
  --output "./output" \
  --keep-background
```

## 参数

| 参数 | 说明 |
|------|------|
| `--original` | 原图路径 |
| `--poses` | pose 参考图（1-4张） |
| `--output` | 输出目录（默认./output）|
| `--keep-background` | 保留原图背景 |
| `--desc` | 详细描述（提高准确度）|
| `--expression` | 表情（默认smiling）|
| `--resolution` | 分辨率 1K/2K/4K |

## 前置要求

```bash
export FAL_KEY="your-fal-api-key"
pip install fal-client
```

获取 API Key: https://www.fal.ai/dashboard/keys

## 费用

- $0.15/张图
- 模型: fal-ai/nano-banana-pro/edit
