---
name: minimax-image
description: 使用MiniMax图像生成API进行文生图。支持文字描述生成图片，适用于PPT配图、封面图、内容配图等场景。触发词：生成图片、文生图、创建图片、MiniMax图片。
version: 1.0.0
author: TJMtaotao
tags: [图片生成, AI绘画, 文生图, MiniMax]
---

# MiniMax 图像生成技能

## 功能概述

使用 MiniMax API 进行文本到图像生成（Text-to-Image）。

## API 信息

- **接口地址**: https://api.minimaxi.com/v1/image_generation
- **模型**: image-01
- **比例**: 支持 16:9, 1:1, 9:16 等

## 输入要求

| 参数 | 说明 | 必填 |
|------|------|------|
| prompt | 图片描述文本 | ✅ |
| aspect_ratio | 宽高比（默认16:9） | 否 |
| n | 生成数量（默认1，最大4） | 否 |

## 使用方法

### 命令行调用

```bash
python3 /path/to/scripts/generate.py "你的图片描述" --ratio 16:9 --num 1
```

### Python调用

```python
from minimax_image import MiniMaxImage

client = MiniMaxImage(api_key="your-api-key")
result = client.generate("蓝色科技风格PPT封面，标题：深度学习")
image_urls = result["image_urls"]
```

## 输出

- 返回生成的图片URL列表
- 图片自动保存至 `{output}/{date}/` 目录

## 依赖

```
pip install requests
```

## API Key 配置

API Key通过环境变量 `MINIMAX_API_KEY` 设置，或在初始化时传入。

获取地址：https://platform.minimaxi.com/