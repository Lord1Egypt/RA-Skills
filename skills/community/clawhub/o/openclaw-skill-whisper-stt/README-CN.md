# 🎙️ OpenClaw 技能：Whisper 语音转文字

使用 OpenAI 的 Whisper 模型将音频转换为文字的 OpenClaw 技能。

## 功能特性

- 🎙️ **语音识别** - 将音频转换为文字
- 🌍 **多语言支持** - 支持100+种语言
- 🇨🇳 **中文优化** - 中文识别效果极佳
- ⚡ **多模型选择** - 从tiny到large可选

## 环境要求

- Python 3.8+
- PyTorch
- openai-whisper
- ffmpeg

## 安装步骤

### 1. 安装依赖

```bash
# 安装Whisper
pip3 install openai-whisper

# 安装FFmpeg
# macOS
brew install ffmpeg
# Ubuntu
sudo apt install ffmpeg
# Windows
winget install ffmpeg
```

### 2. 安装技能

将技能文件放入你的 OpenClaw 工作区：
```
~/openclaw-workspace/skills/whisper-stt/
├── SKILL.md
├── transcribe.py
└── README-CN.md
```

## 使用方法

### 命令行

```bash
# 基本识别
python3 transcribe.py -i audio.mp3

# 指定模型
python3 transcribe.py -i audio.mp3 -m small

# 保存结果
python3 transcribe.py -i audio.mp3 -o result.txt
```

### Python API

```python
import whisper

# 加载模型（首次使用会下载）
model = whisper.load_model("base")

# 识别
result = model.transcribe("audio.mp3", language="zh")

# 获取文字
text = result["text"]
print(text)
```

## 模型对比

| 模型 | 大小 | 速度 | 精度 |
|------|------|------|------|
| tiny | ~1GB | 最快 | 基础 |
| base | ~1GB | 快 | 良好 |
| small | ~2GB | 中等 | 较好 |
| medium | ~5GB | 较慢 | 很好 |
| large | ~10GB | 最慢 | 最佳 |
| turbo | ~6GB | 快 | 接近large |

**推荐**：base 速度快，small 均衡，large 最准

## 支持格式

- MP3, WAV, M4A, OGG, FLAC, WebM
- 任何音频格式（FFmpeg支持即可）

## 使用示例

### 示例 1: 语音转文字

```bash
python3 transcribe.py -i voice_message.m4a -o transcript.txt
```

### 示例 2: 批量处理

```python
import whisper
import os

model = whisper.load_model("base")

for file in os.listdir("./audio"):
    if file.endswith(".mp3"):
        result = model.transcribe(f"./audio/{file}")
        print(f"{file}: {result['text']}")
```

## 故障排除

### "Module not found"

```bash
pip3 install openai-whisper
```

### "FFmpeg not found"

安装 FFmpeg：
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`

### "模型下载太慢"

使用镜像或先下载小模型：
```python
model = whisper.load_model("tiny")  # 更小更快
```

## 许可证

MIT 许可证

## 作者

- **Isaac** - [GitHub](https://github.com/QiaoTuCodes)
- **焱焱 (Yanyan)** - yanyan@3c3d77679723a2fe95d3faf9d2c2e5a65559acbc97fef1ef37783514a80ae453

## 鸣谢

- OpenAI Whisper 团队
- OpenClaw 团队

---

*此技能来自 OpenClaw 技能集合。*
