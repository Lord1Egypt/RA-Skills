---
name: minimax-vision
description: MiniMax 图片理解 MCP - 自动识别用户发送的图片
metadata: {"clawdbot":{"emoji":"👁️","triggers":["分析图片","识别图片","看看这张图","这张是什么","帮我看看"]}}
---

# MiniMax Vision - 图片理解

使用 MiniMax MCP 进行图片识别。

## 使用方式

当用户发送图片或让你分析图片时，自动调用：

```bash
mcporter call minimax.understand_image --args '{"prompt": "你要求的描述", "image_source": "图片路径"}'
```

## 工作流程

1. 检测到用户发送图片（在 media/inbound/ 目录）
2. 使用 mcporter 调用 minimax.understand_image
3. 返回识别结果给用户

## 注意事项

- 图片路径: ~/.openclaw/media/inbound/*.jpg/*.png/*.gif/*.webp
- 依赖 mcporter 和 minimax MCP 已配置
