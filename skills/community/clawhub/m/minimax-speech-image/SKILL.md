---
name: minimax
description: >
  MiniMax 多模态技能 — 接入 MiniMax Token Plan 接口，语音合成（TTS/音色克隆/音色设计）
  和图片生成（文生图/图生图）。使用 speech-2.8-hd（语音）和 image-01（图像）模型，
  消费 Token Plan 额度。当用户提到语音合成、音色克隆、图片生成、文生图、图生图、
  MiniMax Token Plan 时触发。
version: 1.0.0
author: lumina
tags:
  - minimax
  - speech
  - tts
  - voice-clone
  - voice-design
  - image
  - generation
  - image-generation
  - token-plan
  - audio
  - edit
---

# MiniMax 多模态 Skill（Token Plan 版）

使用 MiniMax Token Plan 额度进行语音合成和图片生成。

## 环境配置

- `MINIMAX_API_KEY`: MiniMax API 密钥（必填，从 Token Plan 页面获取）
- `MINIMAX_REGION`: `cn` 国内 / `int` 国际（默认 `cn`）

## 语音模块

### 同步 TTS

```bash
python3 scripts/speech.py tts "欢迎使用" -v female-tianmei -o hello.mp3
```

**参数：**
- `text`: 要转换的文本
- `voice_id`: 音色 ID（见下方内置音色表）
- `output_file`: 输出路径
- `model`: 模型，默认 `speech-2.8-hd`
- `format`: 音频格式，默认 `mp3`
- `sample_rate`: 采样率，默认 `32000`
- `bitrate`: 比特率，默认 `128000`

### 异步 TTS

```bash
python3 scripts/speech.py tts-async "长文本内容" -v female-tianmei
# 返回 task_id，再用 query 命令查询
python3 scripts/speech.py query <task_id>
```

### 音色克隆

```bash
python3 scripts/speech.py clone <音频文件路径> -t "我的音色"
```

内部自动完成两步：1) 上传音频到 `/v1/files`；2) 调用 `/v1/voice_clone` 复刻音色。
模型：`speech-2.0-turbo`（默认）。克隆后返回 `voice_id`，可用于 TTS。

### 音色设计

```bash
python3 scripts/speech.py design "年轻女性，活泼开朗" -s custom
```

### 音色管理

```bash
python3 scripts/speech.py list                    # 列出可用音色
python3 scripts/speech.py delete <voice_id>     # 删除音色
```

### 内置音色

| voice_id | 描述 |
|---|---|
| female-tianmei | 女声甜美 |
| male-yunyang | 男声播音 |
| female-badu | 女声巴度 |

---

## 图片模块

### 文生图

```bash
python3 scripts/image.py generate "日出海边风景" -o sunset.png -r 16:9
```

**参数：**
- `prompt`: 图片描述
- `output_file`: 输出路径（必填）
- `aspect_ratio`: 宽高比，`1:1` / `16:9` / `9:16` / `4:3` / `3:4`（默认 `1:1`）
- `response_format`: 返回格式，`url`（默认）或 `base64`

### 图生图（编辑）

```bash
python3 scripts/image.py edit "把猫变成老虎" -i cat.png -o tiger.png -r 1:1
```

支持本地文件路径或 URL。

---

## Python 函数调用

### 语音

```python
from scripts.speech import text_to_speech, clone_voice, design_voice, list_voices

# TTS
text_to_speech("你好世界", voice_id="female-tianmei", output_file="hello.mp3")

# 音色克隆
voice_id = clone_voice("my_voice.mp3", title="我的音色")

# 音色设计
voice_id = design_voice("年轻男性，沉稳专业", style="custom")

# 音色列表
voices = list_voices()
```

### 图片

```python
from scripts.image import generate_image, generate_image_from_image, download_image

# 文生图
generate_image("日出海边", output_path="sunset.png", aspect_ratio="16:9")

# 图生图
generate_image_from_image("添加中国风元素", image_file="photo.png", output_path="result.png")

# 下载图片
download_image("https://example.com/image.png", "local.png")
```
