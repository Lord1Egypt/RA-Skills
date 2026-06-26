---
name: video2txt
description: 将本地视频或音频文件转写为 SRT 字幕文件和 TXT 纯文本文件
metadata: { "openclaw": { "emoji": "video", "requires": { "bins": ["python3"] } } }
---

# video2txt 技能

## 描述

将本地视频或音频文件转写为 SRT 字幕文件和 TXT 纯文本文件。

## 功能

- 提取视频/音频中的语音内容
- 生成带时间戳的 SRT 字幕文件
- 生成纯文本 TXT 文件
- 支持多种视频和音频格式
- 默认使用中文识别，自动转换为简体中文

​	使用场景：

1. 需要读取视频内容或理解视频时

## 使用方法

### 基本命令

```bash
python video_to_text.py --input <视频/音频文件路径>
```

### 注意事项

- **后台执行**：调用此脚本时，务必使用 `background: true` 参数，避免弹出控制台窗口
- 脚本运行过程中会输出详细的进度日志（每 10% 报告一次），方便追踪执行状态

### 示例

```bash
# 基本用法
python video_to_text.py --input "D:\videos\meeting.mp4"

# 指定输出目录
python video_to_text.py --input "D:\videos\meeting.mp4" --output-dir "D:\captions"

# 指定输出路径
python video_to_text.py --input "D:\videos\meeting.mp4" --output-path "D:\captions\meeting_result"

# 指定语言和模型
python video_to_text.py --input "D:\videos\meeting.mp4" --language zh --model-size small
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 输入文件路径（必需） | - |
| `--output-dir` | 输出目录 | 输入文件目录 |
| `--output-path` | 输出文件基础路径 | - |
| `--model-dir` | 模型下载目录 | 当前目录/models |
| `--model-size` | Whisper 模型大小 | base |
| `--language` | 识别语言 (auto/zh/en) | zh |
| `--device` | 推理设备 (cpu/cuda) | cpu |
| `--compute-type` | 计算类型 | int8 |
| `--beam-size` | 解码束大小 (1-5) | 2 |
| `--no-vad-filter` | 禁用 VAD 过滤 | false |

## 依赖

- faster-whisper >= 1.1.0
- av >= 12.0.0
- opencc-python-reimplemented >= 0.1.7
-  ffprobe/ffmpeg
- Whisper 模型文件（首次运行自动下载，需要发起网络请求，占用磁盘空间）

## 安装

1. 确保 Python 3.11 或 3.12 环境
2. 安装依赖：`python -m pip install -r requirements.txt`
3. 首次运行会自动下载 Whisper 模型到 models 目录

## 输出文件

- `<输入文件名>.srt` - 带时间戳的字幕文件
- `<输入文件名>.txt` - 纯文本文件

## 注意事项

- 首次运行需要下载 Whisper 模型，可能需要几分钟时间
- 建议使用 Python 3.11 或 3.12，避免与 faster-whisper 的兼容性问题
- 中文识别会自动将繁体字转换为简体字
- 为了减少用户等待焦虑，每间隔10秒左右报告一次处理进度
- beam-size 默认为 2，如需调整可手动指定 --beam-size 参数
