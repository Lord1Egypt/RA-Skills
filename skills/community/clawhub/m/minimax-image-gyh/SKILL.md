---
name: minimax-image-gyh
description: MiniMax 图像生成模型（image-01），根据文本描述生成高质量图片。使用 MINIMAX_API_KEY 环境变量。
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["python3"]}}}
---

# MiniMax 图像生成

使用 MiniMax image-01 模型根据文本描述生成图片。

## 支持的模型

| 模型 | 说明 |
|------|------|
| `image-01` | 最新图像生成模型，支持文生图 |
| `image-01-live` | 实时图像生成 |

## 前置要求

- Python 3
- `pip3 install requests`
- 设置环境变量 `MINIMAX_API_KEY`

## 使用方法

```bash
# 文生图
python3 {baseDir}/scripts/image_gen.py \
  --prompt "一个穿古装的东方美女，银杏树下，月光皎洁" \
  --output girl.png

# 指定尺寸
python3 {baseDir}/scripts/image_gen.py \
  --prompt "未来城市夜景，霓虹灯光，科幻风格" \
  --size 1024x1024 \
  --output city.png
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 图片描述文本（建议中英混杂效果更好） | - |
| `--model` | 模型名称 | `image-01` |
| `--size` | 图片尺寸 | `1024x1024` |
| `--output` | 输出文件路径 | `output.png` |
