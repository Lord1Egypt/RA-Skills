---
name: minimax-image
description: Generate images using MiniMax API (image-01 model). Automatically optimizes prompts for better results. Use when user asks to generate images, create pictures, or draw.
version: 1.1.0
---

# MiniMax Image Generator v1.1.0

Generate images using MiniMax API with automatic prompt optimization.

## Version 1.1.0 Updates
- **Auto-prompt optimization**: Automatically converts user input into concise, clear English prompts
- Better image generation results through optimized prompts

## Usage

```
/minimax 一只可爱的橘猫
/画图 赛博朋克城市夜景
/minimax 帮我画一幅未来科技感的城市
```

## Environment

Requires `MINIMAX_API_KEY` or `AIMLAPI_API_KEY` environment variable.

## Auto-Prompt Optimization

The skill automatically:
1. Receives user's Chinese/English input
2. Converts to concise English prompt optimized for image generation
3. Adds relevant keywords for style, lighting, quality
4. Generates image with optimized prompt

## API

- Endpoint: `https://api.minimaxi.com/v1/image_generation`
- Model: `image-01`
- Aspect Ratio: 16:9 (default)