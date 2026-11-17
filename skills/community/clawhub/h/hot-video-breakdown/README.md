# 热门视频拆解

一个全自动的热门视频内容拆解工具。支持自动解析、离线转写、AI 分析和交互式 HTML 报告生成。

## ⚠️ 安全声明

使用本工具前请知悉以下行为：

- **网络下载**：会从用户提供的视频链接下载视频文件到临时目录
- **模型下载**：首次运行会自动从 Hugging Face 下载 Whisper small 模型（约 500MB）
- **本地文件写入**：转写字幕、分析结果和 HTML 报告会写入当前工作目录的 `output/` 文件夹
- **推荐操作**：仅在信任的视频链接上使用；打开生成的 HTML 报告前确认分析 JSON 来源可信

## 核心能力

- 自动解析热门视频链接，提取标题、时长、创作者的元数据
- 基于 faster-whisper 的离线语音转文字（small 模型）
- 由调用方 AI 驱动的深度内容分析
- 生成交互式胶囊卡片 HTML 报告

## 快速开始

```bash
# 安装依赖
pip install yt-dlp faster-whisper

# 解析视频
python scripts/parse.py "视频链接"

# 生成 HTML 报告
python scripts/parse.py --generate-html output/_analysis.json
```

## 要求

- Python 3.10+
- 首次运行会自动下载 Whisper small 模型（约 500MB）
- CPU 可用，无需 GPU
