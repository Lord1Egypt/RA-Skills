---
name: pixel-art-processing
description: |
  Pixel art sprite sheet processing tool — video frame extraction, GIF/frames conversion,
  sprite sheet compose/split, image matting, pixelation, resize, crop, and watermark removal.
  Use when processing pixel art, game assets, RPG Maker sprites, or any sprite sheet workflow.
  Triggers on: sprite sheet, GIF拆帧, 序列帧, 像素图片, 抠图, 去水印, 视频转帧,
  pixel art, sprite, GIF to frames, frames to GIF, background removal, pixelate.
---

# Pixel Art Processing / 像素美术处理

> [!NOTE]
> This skill is based on **FrameRonin** (https://github.com/systemchester/FrameRonin).
> All core algorithms and workflows are derived from the FrameRonin project.

## Overview / 概述

This skill provides a complete pixel art / sprite sheet processing pipeline:

| 功能 / Feature | 描述 / Description |
|---|---|
| 🎬 视频转序列帧 | Extract frames from video → matting → sprite sheet合成 |
| 🔄 GIF ↔ 序列帧 | GIF拆帧 / 序列帧合成GIF |
| 🖼️ 多图合成单图 | Multiple images → single sprite sheet |
| ✂️ 单图拆分 | Split single image into grid frames |
| 🖌️ 简易拼接 | Simple vertical/horizontal/overlay stitching |
| 🗑️ 抠图 (AI) | rembg AI background removal |
| 📐 缩放/裁切 | Resize, crop, padding |
| 🔲 像素化 | Pixelation effect |
| 💧 色度键抠图 | Green/blue screen chroma keying |
| 🚫 Gemini水印去除 | Remove Gemini visible watermark |
| ⚔️ RPGMAKER处理 | One-click RPG Maker sprite workflow |
| 🎥 Seedance水印去除 | Remove Seedance/即梦 video watermark |

## Quick Start / 快速开始

### 1. Deploy Backend / 部署后端

```bash
# Docker部署（推荐 / Recommended）
cd <skill>/scripts
docker-compose up -d

# 或手动部署 / Or manual:
pip install -r requirements.txt
python run_api.py
```

后端地址 / Backend URL: `http://localhost:8000`
API文档 / API docs: `http://localhost:8000/docs`

### 2. Start Worker / 启动Worker

```bash
# 需要Redis / Redis required
rq worker pixelwork --url redis://localhost:6379/0
```

## Core Concepts / 核心概念

### Sprite Sheet Layout / Sprite Sheet布局

```
┌────┬────┬────┬────┐
│ 0  │ 1  │ 2  │ 3  │  row=0
├────┼────┼────┼────┤
│ 4  │ 5  │ 6  │ 7  │  row=1
├────┼────┼────┼────┤
│ 8  │ 9  │ ..│ .. │
└────┴────┴────┴────┘

Index JSON:  { i, x, y, w, h, t }
i = frame index
x, y = position on sheet
w, h = frame size
t = timestamp (seconds)
```

### Processing Modes / 处理模式

- **tight_bbox**: 紧贴alpha边界裁切 / Crop tightly to alpha boundary
- **safe_bbox**: alpha边界+padding / Alpha boundary + padding margin
- **none**: 不裁切 / No crop

## API Reference / API参考

详见 / See: [references/api.md](references/api.md)

## Client-side Processing / 客户端处理

对于 GIF/序列帧转换等纯前端功能，使用浏览器Canvas API直接处理：

For pure client-side features like GIF/frames conversion, use browser Canvas API directly:

```
scripts/
├── client_gif_processor.html   # GIF拆帧/合成 - 浏览器直接运行
├── sprite_split.html           # Sprite sheet拆分 - 浏览器直接运行
└── image_processor.html         # 图像基本处理 - 浏览器直接运行
```

直接在浏览器打开这些HTML文件即可使用。

Open these HTML files directly in browser to use.

## RPG Maker Workflow / RPG Maker 工作流

详见 / See: [references/rpgmaker.md](references/rpgmaker.md)

## Sprite Sheet Math / Sprite Sheet 数学

详见 / See: [references/sprite_math.md](references/sprite_math.md)

## Algorithm Details / 算法细节

### 透明行列检测 / Transparent Row/Column Detection

用于超级拆分：按透明行/列智能切割图像。

Used for super-split: intelligently cuts image by transparent rows/columns.

```javascript
// 找出完全透明的行索引
// Find fully transparent rows
function findTransparentRows(imageData) {
  const { data, width, height } = imageData
  const rows = []
  for (let y = 0; y < height; y++) {
    let allTransparent = true
    for (let x = 0; x < width; x++) {
      if (data[(y * width + x) * 4 + 3] !== 0) {
        allTransparent = false
        break
      }
    }
    if (allTransparent) rows.push(y)
  }
  return rows
}
```

### Alpha边界框 / Alpha Bounding Box

```javascript
function getAlphaBbox(img) {
  // 返回 {x1, y1, x2, y2} 或 null
  // Returns {x1, y1, x2, y2} or null
}
```

### 连通域检测 / Connected Component

用于超级橡皮等工具：按连通域+容差选区。

Used for super eraser: select by connected component + tolerance.

## FFmpeg Integration / FFmpeg集成

视频帧提取依赖 ffprobe/ffmpeg：

Video frame extraction requires ffprobe/ffmpeg:

```bash
# 提取帧 / Extract frames
ffmpeg -y -ss <timestamp> -i video.mp4 -vframes 1 output.png

# 获取视频信息 / Get video info
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

## Dependencies / 依赖

### Backend / 后端
- FastAPI >= 0.104.0
- PIL/Pillow >= 10.0.0
- rembg >= 2.0.50 (u2net model)
- ffmpeg-python >= 0.2.0
- opencv-python-headless >= 4.8.0
- Redis + RQ (for async jobs)

### Frontend / 前端
- gifuct-js (GIF拆帧)
- gifenc (GIF编码)
- jszip (批量下载)
- React + Ant Design

## Feature Flags / 特性开关

| 功能 | 路径 |
|---|---|
| NFT门槛 | frontend/src/config/features.ts → RONIN_PRO_REQUIRE_NFT |
| Ronin登录 | frontend/src/auth/context.tsx |
| Gemini链接 | frontend/src/config/gemini.ts |

## Deploy to Remote / 远程部署

```bash
# 1. 构建前端 / Build frontend
cd frontend && npm install && npm run build

# 2. 配置Nginx / Nginx config
# See nginx.conf in references/

# 3. 启动后端 / Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 4. Docker完整部署 / Full Docker deploy
docker-compose -f docker-compose.yml up -d
```

## Credits / 致谢

- **FrameRonin** by systemchester: https://github.com/systemchester/FrameRonin
- **rembg** for AI matting: https://github.com/danielgatis/rembg
- **gifuct-js** / **gifenc** for GIF processing
