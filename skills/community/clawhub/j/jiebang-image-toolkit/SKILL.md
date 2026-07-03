---
name: jiebang-image-toolkit
description: 图片格式转换与二维码生成工具 - 支持图片格式互转（PNG/JPEG/WebP/SVG/BMP）和自定义二维码生成。当用户提到图片格式转换、图片转格式、二维码生成、QR码制作、PNG转JPEG、WebP转换等需求时使用此技能。
---

# 捷帮图片工具

图片格式转换与二维码生成的专业工具。

## 核心能力

### 1. 图片格式转换 (image-convert)
支持以下格式互转：
- PNG ↔ JPEG
- PNG ↔ WebP
- JPEG ↔ WebP
- PNG ↔ BMP
- SVG 转换

### 2. 二维码生成 (qrcode)
生成自定义二维码：
- 支持自定义尺寸
- 支持纠错级别设置
- 支持Logo嵌入（可选）
- 支持颜色定制

## 输入参数

### 图片格式转换
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | string | 是 | 图片URL或Base64编码 |
| from_format | string | 是 | 源格式 (png/jpeg/webp/bmp/svg) |
| to_format | string | 是 | 目标格式 (png/jpeg/webp/bmp/svg) |
| quality | int | 否 | 输出质量 (1-100)，默认85 |

### 二维码生成
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 二维码内容（URL、文本等） |
| size | int | 否 | 二维码尺寸，默认300px |
| error_level | string | 否 | 纠错级别 L/M/Q/H，默认M |

## 输出格式

### 图片转换结果
```json
{
  "success": true,
  "data": {
    "format": "png",
    "size": "1024x768",
    "image_url": "转换后的图片URL或Base64"
  }
}
```

### 二维码生成结果
```json
{
  "success": true,
  "data": {
    "qrcode": "base64编码的二维码图片",
    "size": "300x300"
  }
}
```

## 使用示例

**示例1：图片格式转换**
```
输入：将 https://example.com/image.png 转换为JPEG
输出：{
  "format": "jpeg",
  "image_url": "data:image/jpeg;base64,..."
}
```

**示例2：生成二维码**
```
输入：生成一个包含 https://example.com 的二维码
输出：{
  "qrcode": "data:image/png;base64,...",
  "size": "300x300"
}
```

## 注意事项

- 图片URL需要可公开访问
- Base64编码时需包含完整前缀（如 data:image/png;base64,）
- 二维码内容长度有限制，建议不超过500字符
- 纠错级别越高，二维码图案越复杂
