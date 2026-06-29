---
name: image-convert
description: Image format conversion, compression, and video-to-GIF conversion. Use when user asks to convert, compress, or transform image/video files. Covers PNG, JPG, WebP, GIF, BMP, TIFF, HEIC, AVIF, and video-to-GIF. Trigger phrases: "convert image", "compress image", "转成gif", "视频转gif", "格式转换", "压缩图片".
---

# Image Convert & Compress

## Quick Commands

### Format Conversion (ffmpeg)

```bash
ffmpeg -i input.png output.jpg # PNG → JPG
ffmpeg -i input.jpg output.png # JPG → PNG
ffmpeg -i input.png output.webp        # PNG → WebP
ffmpeg -i input.jpg output.webp        # JPG → WebP (lossy)
ffmpeg -i input.jpg output.webp -quality 90  # JPG → WebP 高质量
```

### macOS Built-in (sips)

```bash
sips -s format jpeg input.png --out output.jpg    # PNG → JPG
sips -s format png input.jpg --out output.png # JPG → PNG
sips -s format jpeg -s formatOptions 80 input.png --out output.jpg  # 压缩 JPG
```

### HEIC/HEIF 支持

```bash
ffmpeg -i input.heic output.jpg # HEIC → JPG
ffmpeg -i input.jpg output.heic        # JPG → HEIC (需要 x265)
```

### ImageMagick (convert)

```bash
convert input.png -quality 80 output.jpg           # 压缩 JPG
convert input.png -resize 50% output.png # 缩小 50%
convert input.png -resize 800x output.jpg # 宽度 800px 等比
convert input.jpg -colors 256 output.png           # 减少颜色
convert input.png -strip output.png               # 去除元数据
```

### GIF 制作

**从视频（推荐高压缩）：**
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=full:max_colors=64[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 output.gif
```

**从视频（高质量）：**
```bash
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```

**参数说明：**
- `fps=N`：帧率，越高质量越大
- `scale=W:-1`：宽度，高度等比自动计算
- `max_colors=N`：调色板颜色数（8-256），越小文件越小
- `loop0`：无限循环；`loop -1`：不循环；`loop N`：循环 N 次

###图像压缩

**JPG 压缩：**
```bash
ffmpeg -i input.jpg -q:v 2 output.jpg    # q:v 1-31，越小质量越高
sips -s format jpeg -s formatOptions 70 input.jpg --out output.jpg
```

**PNG 压缩（pngquant）：**
```bash
pngquant --quality=65-80 --force --output output.png input.png
```

**PNG 优化（optipng）：**
```bash
optipng -o5 input.png                    # -o1 到 -o7压缩级别
```

**WebP 压缩：**
```bash
ffmpeg -i input.jpg -c:v libwebp -quality 75 output.webp
```

### GIF 压缩工具

**gifsicle（需安装）：**
```bash
gifsicle -O3 --colors128 --lossy 30 -o output.gif input.gif
```

**ffmpeg 重新压缩：**
```bash
ffmpeg -i input.gif -vf "split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse" -y output.gif
```

## 常用参数参考

| 格式 | 质量参数 | 特点 |
|------|---------|------|
| JPG  | -q:v 2-31 或 -s formatOptions 60-100 | 有损，文件小 |
| PNG  | 无损 | 透明背景支持 |
| WebP | -quality 0-100 | 优于 JPG/PNG |
| GIF | fps/colors | 动图，支持透明 |
| HEIC | 有损 | iPhone 默认格式 |
| AVIF | -quality | 极小文件，极高压缩 |

## 常见问题

**GIF 文件太大？**
1. 降低帧率：`-fps=8`
2. 缩小尺寸：`-scale=320:-1`
3. 减少颜色：`-max_colors=64`
4. 使用 gifsicle 压缩

**颜色失真？**
使用调色板生成器 `palettegen`+`paletteuse`，比默认256 色更好

**透明背景丢失？**
确保输出格式支持透明（PNG、GIF、WebP），JPG 不支持透明

**ffmpeg 报错 "Not found"？**
macOS 用 `ffmpeg`（Homebrew 安装的版本），非 Apple 预装版本

## 工具检查

```bash
which ffmpeg    # 检查 ffmpeg
which convert # 检查 ImageMagick
which optipng   # 检查 optipng
which pngquant # 检查 pngquant
```