# FFmpeg 参考指南

## 常用命令速查

### 视频压缩

```bash
# 基本压缩 (CRF 23)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4

# 压缩到 720p
ffmpeg -i input.mp4 -vf "scale=-2:720" -c:v libx264 -crf 23 output.mp4

# 压缩到目标比特率 (2 Mbps)
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 128k output.mp4

# 快速压缩 (lower quality, faster)
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 28 output.mp4

# 慢速压缩 (better quality, smaller size)
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 18 output.mp4
```

### 图像处理

```bash
# 压缩 JPEG (quality 1-31, lower is better)
ffmpeg -i input.png -q:v 5 output.jpg

# 压缩 WebP
ffmpeg -i input.png -c:v libwebp -q:v 80 output.webp

# 调整大小
ffmpeg -i input.jpg -vf "scale=800:-1" output.jpg

# 批量转换格式
for f in *.png; do ffmpeg -i "$f" "${f%.png}.webp"; done
```

### 格式转换

```bash
# MP4 to WebM
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# MOV to MP4
ffmpeg -i input.mov -c:v copy -c:a copy output.mp4

# GIF to MP4
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p output.mp4
```

## CRF 值参考

| CRF | 质量 | 用途 |
|-----|------|------|
| 17-18 | 视觉无损 | 存档 |
| 20-22 | 高质量 | 专业用途 |
| 23 | 默认 | 一般用途 |
| 28 | 中等 | 网络分享 |
| 35+ | 低质量 | 预览/草稿 |

## Preset 速度对比

| Preset | 速度 | 文件大小 |
|--------|------|----------|
| ultrafast | 最快 | 最大 |
| superfast | 很快 | 很大 |
| veryfast | 快 | 大 |
| faster | 较快 | 较大 |
| fast | 中等 | 中等 |
| medium | 默认 | 默认 |
| slow | 慢 | 较小 |
| slower | 很慢 | 很小 |
| veryslow | 最慢 | 最小 |

## 视频滤镜 (vf)

```bash
# 缩放
scale=1920:1080          # 固定尺寸
scale=-2:720             # 保持比例，高度720
scale=1280:-2            # 保持比例，宽度1280

# 裁剪
crop=800:600:100:100     # 宽:高:x:y

# 旋转
transpose=1              # 90度顺时针

# 帧率
fps=30                   # 限制30fps

# 组合滤镜
-vf "scale=-2:720,fps=30"
```

## 音频参数

```bash
# 音频编码器
-c:a aac                 # AAC (推荐)
-c:a libmp3lame          # MP3
-c:a libopus             # Opus (WebM)

# 音频比特率
-b:a 128k                # 128 kbps (默认)
-b:a 192k                # 192 kbps (高质量)
-b:a 64k                 # 64 kbps (语音)

# 音频采样率
-ar 44100                # CD 质量
-ar 48000                # 视频标准
```

## 元数据处理

```bash
# 去除所有元数据
-map_metadata -1

# 保留元数据
-map_metadata 0

# 添加元数据
-metadata title="My Video"
-metadata author="John Doe"
```

## 双通道音频处理

```bash
# 只保留单声道
-ac 1

# 保持原声道
-acodec copy
```

## 常用技巧

```bash
# 只处理前30秒
-t 30

# 从第60秒开始
-ss 00:01:00

# 提取片段 (60-90秒)
-ss 00:01:00 -t 30

# 静音视频 (去除音频)
-an

# 视频静音 (只保留音频)
-vn

# 快速预览 (低质量)
ffmpeg -i input.mp4 -vf "scale=480:-1" -crf 35 -preset ultrafast preview.mp4
```

## 故障排除

**"Unknown encoder"**: 安装完整版 ffmpeg

**"Permission denied"**: 检查文件权限

**"Invalid argument"**: 检查滤镜语法

**文件反而变大**: 降低 CRF 值或检查源文件是否已压缩
