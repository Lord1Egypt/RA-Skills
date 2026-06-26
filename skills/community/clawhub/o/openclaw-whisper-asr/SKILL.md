---
name: whisper-asr
description: |
  本地 Whisper 语音识别配置。自动将飞书/Telegram 等渠道的语音消息转成文字。
  适用于需要离线、低延迟语音转文字的场景。
---

# 本地 Whisper 语音识别配置 (whisper-asr)

## 概述

通过 whisper.cpp 在服务器上配置本地语音识别，用于：
- 识别用户发来的语音消息
- 离线运行，无需 API
- 支持中文等多种语言

## 前置要求

- Linux 服务器（已测试 Ubuntu/Debian）
- ffmpeg 已安装
- ~150MB 磁盘空间（base 模型）

---

## 安装步骤

### 1. 安装 ffmpeg

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 2. 克隆 whisper.cpp

```bash
cd /home/brew/.openclaw/workspace
git clone https://github.com/ggml-org/whisper.cpp.git
```

### 3. 下载中文模型

```bash
cd whisper.cpp
sh ./models/download-ggml-model.sh base
```

**模型选择建议：**

| 模型 | 大小 | 内存 | 推荐场景 |
|------|------|------|---------|
| tiny | 75 MB | ~273 MB | 快速测试 |
| **base** | 142 MB | ~388 MB | 平衡推荐 |
| small | 466 MB | ~852 MB | 更高精度 |

### 4. 编译

```bash
cd whisper.cpp
cmake -B build
cmake --build build -j --config Release
```

---

## 使用方式

### 1. 转换音频格式

飞书语音通常是 ogg 格式，需要转换为 whisper 需要的格式：

```bash
ffmpeg -i input.ogg -ar 16000 -ac 1 -c:a pcm_s16le output.wav
```

### 2. 语音转文字

```bash
./build/bin/whisper-cli \
  -m models/ggml-base.bin \
  -f output.wav \
  --language zh \
  --no-timestamps
```

**常用参数：**
- `-m`: 模型路径
- `-f`: 输入音频文件
- `--language zh`: 指定中文
- `--no-timestamps`: 不输出时间戳
- `-t 4`: 线程数（默认自动）

### 3. 完整示例（单命令）

```bash
ffmpeg -i input.ogg -ar 16000 -ac 1 -c:a pcm_s16le /tmp/audio.wav && \
./build/bin/whisper-cli -m models/ggml-base.bin -f /tmp/audio.wav --language zh --no-timestamps
```

---

## 路径速查

| 项目 | 路径 |
|------|------|
| whisper.cpp 目录 | `/home/brew/.openclaw/workspace/whisper.cpp` |
| 可执行文件 | `/home/brew/.openclaw/workspace/whisper.cpp/build/bin/whisper-cli` |
| 模型目录 | `/home/brew/.openclaw/workspace/whisper.cpp/models/` |
| base 模型 | `/home/brew/.openclaw/workspace/whisper.cpp/models/ggml-base.bin` |

---

## 常见问题

### Q: 识别结果不准确？
A: 尝试使用更大的模型（small/medium），或在安静环境下录音。

### Q: 识别速度慢？
A: 增加线程数：`./whisper-cli -t 8 ...`

### Q: 支持其他语言？
A: 不指定 `--language` 会自动检测。也可指定 `--language en` 等。

---

## 进阶：量化模型（节省资源）

```bash
# 量化（减少模型大小）
./build/bin/quantize models/ggml-base.bin models/ggml-base-q5.bin q5_0

# 使用量化模型
./build/bin/whisper-cli -m models/ggml-base-q5.bin -f audio.wav --language zh
```

---

_本技能参考 [whisper.cpp 官方文档](https://github.com/ggml-org/whisper.cpp)_
