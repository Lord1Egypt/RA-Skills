---
name: minimax-image
description: MiniMax 图片生成技能 - 支持文生图(Text-to-Image)、图生图(Image-to-Image)。支持多种宽高比(1:1/16:9/9:16/4:3/3:4)，返回 URL 或 Base64 格式，可下载保存到本地。
version: 1.0.0
author: laowang
tags:
  - minimax
  - image
  - generation
  - image-generation
  - edit
---

# MiniMax Image Skill

使用 MiniMax API 进行图片生成和图片编辑。支持文生图、图生图多种宽高比，返回 URL 或 Base64 格式，可下载保存到本地。

## 环境配置

```json
{
  "MINIMAX_API_KEY": "your-api-key",
  "MINIMAX_REGION": "cn" | "int"
}
```

- `MINIMAX_API_KEY`: MiniMax API 密钥
- `MINIMAX_REGION`: 区域设置，`cn` 为中国，`int` 为国际（默认 `cn`）

## 可用函数

### generate_image(prompt, aspect_ratio, response_format)
文生图 - 根据文本描述生成图片

**参数**:
- `prompt`: 图片描述文本
- `aspect_ratio`: 宽高比（默认: `1:1`）
  - `1:1` - 正方形
  - `16:9` - 宽屏
  - `9:16` - 竖屏
  - `4:3` - 标准
  - `3:4` - 竖版标准
- `response_format`: 返回格式（默认: `url`）
  - `url` - 返回图片URL
  - `base64` - 返回base64编码

**返回**: 图片URL或base64编码

**示例**: `generate_image("一只可爱的猫咪", "1:1", "url")`

### generate_image_from_image(prompt, image_file, image_url, aspect_ratio)
图生图 - 根据参考图和描述生成新图片

**参数**:
- `prompt`: 图片修改描述
- `image_file`: 参考图文件路径（本地文件）
- `image_url`: 参考图URL
- `aspect_ratio`: 宽高比

**返回**: 生成的图片URL或base64编码

**示例**: `generate_image_from_image("把这只猫变成老虎", image_file="cat.png")`

### download_image(image_url, output_path)
下载图片到本地

**参数**:
- `image_url`: 图片URL
- `output_path`: 保存路径

**返回**: 保存的文件路径

### save_base64_image(base64_data, output_path)
保存base64编码的图片

**参数**:
- `base64_data`: base64编码的图片数据
- `output_path`: 保存路径

**返回**: 保存的文件路径

## 使用示例

### 文生图

```
python scripts/image.py generate "日出时分的海边风景" -o sunset.png -r 16:9
```

### 图生图

```
python scripts/image.py edit "把这张照片变成油画风格" -i photo.jpg -o painting.png
```

### 使用参考图URL

```
python scripts/image.py edit "给这幅画加上蓝天白云" -i https://example.com/painting.jpg -o new_painting.png
```

## 返回格式说明

- `response_format=url`: 返回的图片URL有效期为1小时
- `response_format=base64`: 直接返回图片数据，可直接保存

## 注意事项

1. prompt 描述越详细，生成效果越好
2. 支持中文描述
3. 图生图时参考图越大越好（建议 > 512px）
4. 生成的图片版权由用户自行承担
