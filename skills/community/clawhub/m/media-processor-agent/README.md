# Media_Processor (OpenClaw 媒体处理专家)

`Media_Processor` 是 OpenClaw 框架下的核心媒体处理工具，旨在为 Agent 提供自动化的图片和视频加工能力。它支持本地文件及远程 URL（包括 m3u8 流媒体）的处理。

## 核心功能

- **图片处理**：
  - **压缩**：自动降低图片质量并转换为 JPEG 格式以减小文件体积。
  - **水印**：在图片右下角添加自定义文字水印。
- **视频处理**：
  - **压缩**：使用 H.264 (AVC) 编码进行视频压缩。
  - **转码**：强制将 H.265 (HEVC) 或其他格式转换为兼容性更好的 H.264。
  - **水印**：为视频添加静态文字水印。
- **在线支持**：
  - **自动下载**：直接传入 HTTP/HTTPS 链接（图片或 MP4）。
  - **流媒体**：支持 m3u8 协议的视频流处理。

## 环境部署

该技能依赖 `Python 3` 和 `FFmpeg` 系统组件。

### 1. 系统依赖安装 (以 Ubuntu/Debian 为例)

```bash
# 安装 FFmpeg (视频处理核心)
apt update && apt install -y ffmpeg

# 验证安装
ffmpeg -version
```

### 2. Python 依赖安装

建议在 OpenClaw 的 Python 环境中安装依赖：

#### 方式 A：直接安装 (推荐)
```bash
pip install -r requirements.txt

# 如果提示外部环境受限 (PEP 668)，请使用：
pip install -r requirements.txt --break-system-packages
```

#### 方式 B：虚拟环境 (venv) 安装 (环境隔离)
如果你希望保持系统环境纯净，可以为该技能创建独立的虚拟环境：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活环境 (Linux/macOS)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 使用虚拟环境运行
./venv/bin/python3 run.py --type image ...
```


## 使用指南

你可以直接调用 `run.py` 或通过 OpenClaw Agent 调度。

### 命令行参数

| 参数 | 说明 | 可选值 |
| :--- | :--- | :--- |
| `--type` | 素材类型 (必填) | `image`, `video` |
| `--action` | 动作类型 (必填) | `compress`, `watermark`, `convert` |
| `--input` | 输入路径 (必填) | 本地路径 或 远程 URL |
| `--output` | 输出路径 | 默认保存在同级或 `/docker/openclaw/data` |
| `--text` | 水印内容 | 默认为 `OpenClaw` |

### 示例命令

#### 1. 处理在线图片 (下载 + 水印)
```bash
python3 run.py --type image --action watermark --input "https://example.com/pic.jpg" --text "MyWatermark"
```

#### 2. 压缩本地视频
```bash
python3 run.py --type video --action compress --input "/path/to/video.mp4"
```

#### 3. 将 H.265 视频转码为 H.264
```bash
python3 run.py --type video --action convert --input "https://example.com/h265_video.mp4"
```

## 开发者说明

- **字体文件**：水印功能默认尝试加载 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`（文泉驿微米黑）。如果系统中没有该字体，将退回到默认字体（不支持中文）。
- **临时文件**：处理 URL 时产生的下载文件存放在 `/tmp`，处理完成后会自动清理。
- **编码器**：视频处理默认使用 `libx264`，音频流默认直接复制 (`-acodec copy`) 以保证质量。



<!-- clawhub publish . \
  --slug media-processor-agent \
  --name "media-processor" \
  --version 1.0.0 \
  --tags "media,tool,processing,video,transcode,stream,watermark" -->
