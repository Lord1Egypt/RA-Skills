
---
name: image-compression
description: 自动检测图片大小，当图片超过 Telegram 发送限制时自动压缩。支持调整压缩后的宽度、质量和格式。
metadata: {"openclaw": {"os": ["darwin"], "author": "Honcy Ye", "email": "honcy.ye@gmail.com"}}
---

# 图片自动压缩技能

自动检测图片大小，当图片超过 Telegram 发送限制（10MB）时自动压缩，确保图片能够成功发送。

## 功能特性
- **自动检测**：自动检查图片大小是否超过限制
- **智能压缩**：
  - 调整图片宽度（默认 1024px）
  - 优化图片质量（默认 85%）
  - 支持多种格式（PNG、JPEG、GIF）
- **保留原文件**：压缩后生成新文件，不修改原文件
- **输出文件名**：自动添加 "_compressed" 后缀

## 使用场景
- 发送大图片到 Telegram
- 优化图片大小以减少网络传输时间
- 确保图片符合特定平台的尺寸限制

## 技术实现
- 使用 macOS `sips` 命令进行图片压缩
- 支持调整压缩参数
- 自动处理文件路径和文件名

## 依赖
- macOS `sips` 工具（系统自带）

## 使用方法
```bash
# 压缩图片（默认参数）
bash scripts/compress_image.sh "/path/to/image.png"

# 自定义宽度
bash scripts/compress_image.sh "/path/to/image.png" 800

# 自定义宽度和质量
bash scripts/compress_image.sh "/path/to/image.png" 800 80

# 发送压缩后的图片到微信文件传输助手
bash scripts/compress_and_send.sh "/path/to/image.png" "文件传输助手"
```

## 配置选项
- **max_width**：压缩后图片的最大宽度（默认 1024px）
- **quality**：压缩质量（0-100，默认 85）
- **max_size**：触发压缩的图片大小阈值（默认 10MB）

## 脚本说明
- `scripts/compress_image.sh`：基本压缩功能
- `scripts/compress_and_send.sh`：压缩后发送到微信
- `scripts/compress_and_send_telegram.sh`：压缩后发送到 Telegram

## 示例
```bash
# 压缩并发送到微信
bash scripts/compress_and_send.sh "/Users/honcy/Desktop/screenshot_20260221_231100.png" "文件传输助手"

# 压缩并发送到 Telegram
bash scripts/compress_and_send_telegram.sh "/Users/honcy/Desktop/screenshot_20260221_231100.png" 5578370460
```
