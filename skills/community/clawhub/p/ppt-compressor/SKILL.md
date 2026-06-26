---
name: ppt-compressor
description: 压缩 PPTX 演示文稿文件体积。通过压缩内嵌图片和视频、清理冗余数据、优化 ZIP 打包等手段显著减小 .pptx 文件大小。支持 low/medium/high/extreme 四档压缩级别。视频压缩依赖 ffmpeg。当用户需要压缩 PPT、减小演示文稿体积、优化 PPTX 文件大小时使用。
license: MIT
metadata:
    version: '1.1.0'
    author: OpenDesk
---

# PPT 压缩技能

将 `.pptx` 文件解包后对内嵌图片进行有损/无损压缩、用 ffmpeg 压缩内嵌视频、清理冗余元数据，再重新打包，从而减小文件体积。

## 依赖

- **Pillow**（图片压缩，必需）：`pip install Pillow`
- **ffmpeg**（视频压缩，可选）：未安装时视频保留原始数据，脚本会输出安装指引

## 使用方法

```bash
python scripts/compress.py <input.pptx> [options]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入 PPTX 文件路径 | 必填 |
| `-o, --output` | 输出文件路径 | `<input>_compressed.pptx` |
| `-l, --level` | 压缩档次：`low` / `medium` / `high` / `extreme` | `medium` |
| **图片参数** | | |
| `--image-quality` | 图片 JPEG 质量 (1-100) | 由 level 决定 |
| `--max-width` | 图片最大宽度像素 | 由 level 决定 |
| `--max-height` | 图片最大高度像素 | 由 level 决定 |
| `--strip-thumbnail` | 移除文档缩略图 | 由 level 决定 |
| `--strip-comments` | 移除幻灯片批注 | `false` |
| `--convert-png` | 不透明 PNG 转 JPEG | 由 level 决定 |
| `--no-convert-png` | 禁止 PNG 转 JPEG | - |
| **视频参数** | | |
| `--video-crf` | 视频 CRF 值 (0-51，越高压缩率越大) | 由 level 决定 |
| `--video-scale` | 视频最大短边像素 (如 720、1080) | 由 level 决定 |
| `--video-preset` | x264 编码预设 (ultrafast~veryslow) | 由 level 决定 |
| `--no-video` | 跳过视频压缩 | `false` |

### 压缩档次预设

| 档次 | JPEG 质量 | 图片尺寸 | 移除缩略图 | PNG→JPG | 视频 CRF | 视频尺寸 | 编码预设 |
|------|-----------|----------|------------|---------|----------|----------|----------|
| low | 85 | 2560px | 否 | 否 | 23 | 原始 | medium |
| medium | 70 | 1920px | 是 | 是 | 28 | 1080p | medium |
| high | 50 | 1440px | 是 | 是 | 32 | 720p | slow |
| extreme | 30 | 1024px | 是 | 是 | 38 | 480p | slow |

### 使用示例

基本压缩（medium 档）：
```bash
python scripts/compress.py "报告.pptx"
```

高压缩档：
```bash
python scripts/compress.py "报告.pptx" -l high -o "报告_小.pptx"
```

跳过视频只压图片：
```bash
python scripts/compress.py "报告.pptx" -l medium --no-video
```

自定义视频参数：
```bash
python scripts/compress.py "报告.pptx" --video-crf 30 --video-scale 720 --video-preset slow
```

### ffmpeg 安装指引

若系统未安装 ffmpeg，脚本运行时会跳过视频并输出安装方法：

- **Windows**: `winget install Gyan.FFmpeg` 或 `scoop install ffmpeg` 或 `choco install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu)
