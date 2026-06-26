# OpenClaw 飞书语音聊天 - 完全离线版

[Python](https://www.python.org/)
[License](LICENSE)

一个为 OpenClaw + 飞书客户端设计的全语音对话技能，基于 Qwen3-TTS 和 Whisper 实现完全离线的语音识别和语音合成。无需任何云端 API，所有模型本地运行。

## ✨ 特性

- 🎤 **完全离线运行** - 所有模型本地运行，不需要云端 API，保护隐私
- 🚀 **高性能** - 使用常驻内存的 HTTP 服务，模型只加载一次，响应速度快
- 🎯 **自动触发** - 收到语音消息自动识别，回复自动合成语音，无需手动操作
- 🌍 **多语言支持** - 支持中文、英文、日语、韩语等 10 种语言的识别和合成
- 🎨 **音色克隆** - 支持自定义音色嵌入，可将任意人声克隆为参考音色文件
- 🔌 **OpenAI 兼容** - TTS 服务兼容 OpenAI TTS API，可直接集成到 OpenClaw
- 🔧 **易于部署** - 一键安装脚本，自动配置虚拟环境
- 🛠️ **音色克隆工具** - 提供独立工具用于音色克隆和测试
- 🧹 **智能文本清理** - 自动清理 LLM 回复中的括号描述和表情符号，只朗读实际内容

## 📋 目录

- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [安装](#安装)
- [配置](#配置)
- [使用方法](#使用方法)
- [工作原理](#工作原理)
- [依赖要求](#依赖要求)
- [常见问题](#常见问题)
- [贡献](#贡献)
- [许可证](#许可证)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/shuaishi1991/openclaw-feishu-voice-free.git
cd openclaw-feishu-voice-free
```

### 2. 安装和部署

按照 [安装](#📦-安装) 部分的详细步骤进行：

1. 复制文件到 OpenClaw skills 目录
2. 运行安装脚本（`bash setup.sh`）
3. 下载模型文件（Whisper 和 Qwen3-TTS）

### 3. 配置 OpenClaw

编辑 `/root/.openclaw/openclaw.json`，按照 [配置](#⚙️-配置) 部分的说明添加配置。

### 4. 启动服务

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

# 启动 Whisper ASR 服务（端口 8001）
nohup python scripts/server/whisper-server.py --port 8001 > /tmp/whisper-server.log 2>&1 &

# 启动 Qwen3-TTS 服务（端口 8000，使用 OpenAI 兼容 API）
nohup python scripts/server/tts-base-server-openai.py --port 8000 --clone voice_embedings/huopo_kexin.pt > /tmp/tts-server.log 2>&1 &

deactivate
```

**注意：** 如果还没有音色文件，可以先不指定 `--clone` 参数，使用默认音色。后续可以通过 [音色克隆工具](#音色克隆) 创建自定义音色。

### 5. 重启 OpenClaw

```bash
openclaw gateway restart
```

现在你可以在飞书发送语音消息，系统会自动识别并回复语音！

---

**详细说明：** 如需了解更多信息，请查看 [安装](#📦-安装)、[配置](#⚙️-配置) 和 [使用方法](#🎯-使用方法) 部分。

## 📁 项目结构

```
openclaw-feishu-voice-free/
├── README.md                          # 项目说明文档
├── setup.sh                           # 虚拟环境安装脚本
├── openclaw.json                      # 配置文件示例
├── voice_embedings/                   # 存放克隆好的音色文件（.pt 格式）
└── scripts/
    ├── server/
    │   ├── whisper-server.py          # Whisper ASR HTTP 服务（端口 8001）
    │   ├── tts-base-server.py         # Qwen3-TTS HTTP 服务（自定义 API）
    │   └── tts-base-server-openai.py   # Qwen3-TTS HTTP 服务（OpenAI 兼容 API，推荐）
    └── tools/
        └── tts-base.py                 # 音色克隆工具（独立测试和克隆音色）
```

## 📦 安装

### 系统要求

- Python 3.10 - 3.12
- OpenClaw 已安装并运行
- 足够的磁盘空间（模型文件约 5-10GB）
- GPU 推荐（CPU 也可运行，但速度较慢）
- 网络连接（用于下载模型，首次使用需要）

### 模型要求

需要下载以下模型到本地：


| 模型          | HuggingFace Repo                | 默认路径                                                        | 大小     |
| ----------- | ------------------------------- | ----------------------------------------------------------- | ------ |
| Whisper ASR | `openai/whisper-large-v3-turbo` | `/root/.openclaw/models/whisper/whisper-large-v3-turbo`     | ~3GB   |
| Qwen3-TTS   | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | `/root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base` | ~3.5GB |


### 安装步骤

1. **复制文件到 OpenClaw skills 目录**

```bash
mkdir -p /root/.openclaw/skills/openclaw-feishu-voice-free
cp -r * /root/.openclaw/skills/openclaw-feishu-voice-free/
chmod +x /root/.openclaw/skills/openclaw-feishu-voice-free/setup.sh
```

1. **运行安装脚本**

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
bash setup.sh
```

`setup.sh` 会自动：

- 检测 Python 版本
- 创建虚拟环境
- 安装所有必需的依赖包

1. **下载模型文件**

需要下载两个模型到本地：

#### 下载 Whisper 模型（ASR）

```bash
# 创建模型目录
mkdir -p /root/.openclaw/models/whisper

# 使用 huggingface-cli 下载（推荐）
pip install huggingface_hub
huggingface-cli download openai/whisper-large-v3-turbo \
  --local-dir /root/.openclaw/models/whisper/whisper-large-v3-turbo \
  --local-dir-use-symlinks False

# 或者使用 Python 脚本下载
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='openai/whisper-large-v3-turbo',
    local_dir='/root/.openclaw/models/whisper/whisper-large-v3-turbo',
    local_dir_use_symlinks=False
)
"
```

#### 下载 Qwen3-TTS 模型（TTS）

```bash
# 创建模型目录
mkdir -p /root/.openclaw/models/Qwen3-TTS

# 使用 huggingface-cli 下载（推荐）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base \
  --local-dir /root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base \
  --local-dir-use-symlinks False

# 或者使用 Python 脚本下载
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='Qwen/Qwen3-TTS-12Hz-1.7B-Base',
    local_dir='/root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base',
    local_dir_use_symlinks=False
)
"
```

**注意：**

- 模型文件较大（约 5-10GB），下载需要一些时间
- 确保有足够的磁盘空间
- 如果网络较慢，可以使用镜像站点或手动下载

1. **安装系统依赖（可选）**

```bash
# Ubuntu/Debian
apt install ffmpeg

# CentOS/RHEL
yum install ffmpeg
```

## ⚙️ 配置

### OpenClaw 配置

在 `/root/.openclaw/openclaw.json` 中配置：

#### 1. 配置 Whisper ASR（语音识别）

在 `tools.media.audio` 中配置 Whisper 服务：

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "bash",
            "args": [
              "-c",
              "curl -s -X POST http://localhost:8001/transcribe -H 'Content-Type: application/json' -d \"{\\\"audio_path\\\": \\\"{{MediaPath}}\\\", \\\"language\\\": \\\"Chinese\\\"}\" | jq -r '.text // empty'"
            ],
            "timeoutSeconds": 60
          }
        ]
      }
    }
  }
}
```

#### 2. 配置 Qwen3-TTS（语音合成）

在 `messages.tts` 中配置 TTS 服务（使用 OpenAI 兼容 API）：

```json
{
  "messages": {
    "tts": {
      "auto": "always",
      "provider": "openai",
      "timeoutMs": 120000,
      "openai": {
        "apiKey": "no need",
        "baseUrl": "http://localhost:8000/v1",
        "model": "Qwen3-TTS-12Hz-1.7B-Base",
        "voice": "huopo_kexin"
      }
    }
  }
}
```

**注意：** 

- `baseUrl` 指向本地 TTS 服务（使用 `tts-base-server-openai.py`）
- `voice` 参数会被忽略（实际使用启动服务时指定的 `--clone` 音色文件）
- `apiKey` 可以设置为任意值（本地服务不需要）

### 服务配置

#### Whisper ASR 服务

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

python scripts/server/whisper-server.py \
  --port 8001 \
  --model /root/.openclaw/models/whisper/whisper-large-v3-turbo \
  --language Chinese
```

**参数说明：**

- `--port`: 服务端口（默认 8001）
- `--model`: 模型路径或 HuggingFace repo ID（默认 `openai/whisper-large-v3-turbo`）
- `--language`: 默认识别语言（默认 Chinese）
- `--batch-size`: 批处理大小（默认 16）

**模型说明：**

- 默认使用 `openai/whisper-large-v3-turbo` 模型
- 也可以使用其他 Whisper 模型，如 `openai/whisper-large-v3`、`openai/whisper-medium` 等
- 如果模型已下载到本地，直接使用本地路径
- 如果使用 HuggingFace repo ID，首次运行时会自动下载

#### Qwen3-TTS 服务（推荐：OpenAI 兼容 API）

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

python scripts/server/tts-base-server-openai.py \
  --port 8000 \
  --model /root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base \
  --clone voice_embedings/huopo_kexin.pt
```

**参数说明：**

- `--port`: 服务端口（默认 8000）
- `--model`: 模型路径或 HuggingFace repo ID（默认 `Qwen/Qwen3-TTS-12Hz-1.7B-Base`）
- `--clone`: 音色克隆文件路径（可选，支持相对路径）

**音色文件路径：**

- 支持绝对路径：`/path/to/voice.pt`
- 支持相对路径：`voice_embedings/my_voice.pt`（会自动在 skill 目录和 voice_embedings 目录查找）
- 如果不指定，使用默认音色

**API 端点：**

- `POST /v1/audio/speech` - 生成语音（兼容 OpenAI TTS API）
- `GET /v1/models` - 获取模型列表
- `GET /` - 健康检查

#### Qwen3-TTS 服务（自定义 API，可选）

如果需要使用自定义 API 格式，可以使用 `tts-base-server.py`：

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

python scripts/server/tts-base-server.py \
  --port 8000 \
  --model /root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base \
  --clone voice_embedings/my_voice.pt
```

**API 端点：**

- `POST /generate` - 生成语音
- `GET /` - 健康检查

## 🎯 使用方法

### 音色克隆

使用 `scripts/tools/tts-base.py` 工具可以克隆任意人声并生成音色文件：

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

# 从参考音频克隆音色并保存为 .pt 文件
python scripts/tools/tts-base.py \
  --audio /path/to/reference_audio.wav \
  --text "这是参考音频的文字内容" \
  --save-clone voice_embedings/my_custom_voice.pt \
  --prompt "测试生成的语音"

# 使用已保存的音色文件生成语音
python scripts/tools/tts-base.py \
  --clone voice_embedings/my_custom_voice.pt \
  --prompt "使用克隆音色生成的文本" \
  --output output.wav

deactivate
```

**音色克隆说明：**

- `--audio`: 参考音频文件路径（支持 wav、mp3、m4a 格式）
- `--text`: 参考音频的文字内容（必须准确）
- `--save-clone`: 保存克隆音色到指定路径（.pt 格式）
- `--clone`: 使用已保存的音色文件生成语音
- 生成的音色文件保存在 `voice_embedings/` 目录下

### 基本使用

1. **启动服务**（在 venv 中）

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

# 启动 Whisper ASR 服务（端口 8001）
nohup python scripts/server/whisper-server.py --port 8001 > /tmp/whisper-server.log 2>&1 &

# 启动 Qwen3-TTS 服务（端口 8000，OpenAI 兼容 API）
nohup python scripts/server/tts-base-server-openai.py --port 8000 --clone voice_embedings/huopo_kexin.pt > /tmp/tts-server.log 2>&1 &

deactivate
```

1. **检查服务状态**

```bash
# 检查 Whisper 服务
curl http://localhost:8001/

# 检查 TTS 服务
curl http://localhost:8000/
```

1. **重启 OpenClaw**

```bash
openclaw gateway restart
```

1. **在飞书发送语音消息**

系统会自动：

- 识别语音为文字（通过 Whisper 服务）
- 调用 LLM 生成回复
- 合成语音回复（通过 Qwen3-TTS 服务）
- 发送语音消息给用户

### 手动测试

#### 测试 ASR（语音转文字）

```bash
# 使用 curl 测试 Whisper 服务
curl -X POST http://localhost:8001/transcribe \
  -H "Content-Type: application/json" \
  -d '{"audio_path": "/path/to/audio.mp3", "language": "Chinese"}'
```

#### 测试 TTS（文字转语音）

```bash
# 使用 curl 测试 TTS 服务（OpenAI 兼容 API）
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3-TTS-12Hz-1.7B-Base",
    "input": "你好，欢迎使用 Qwen3-TTS",
    "voice": "alloy"
  }' \
  --output output.mp3
```

### 使用 systemd 管理服务（推荐生产环境）

创建 systemd 服务文件可以确保服务在系统重启后自动启动：

#### 创建 Whisper ASR 服务

创建 `/etc/systemd/system/openclaw-feishu-voice-free-whisper.service`：

```ini
[Unit]
Description=OpenClaw Feishu Voice Free Whisper ASR Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/skills/openclaw-feishu-voice-free
Environment="PATH=/root/.openclaw/skills/openclaw-feishu-voice-free/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/root/.openclaw/skills/openclaw-feishu-voice-free/venv/bin/python scripts/server/whisper-server.py --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 创建 Qwen3-TTS 服务

创建 `/etc/systemd/system/openclaw-feishu-voice-free-tts.service`：

```ini
[Unit]
Description=OpenClaw Feishu Voice Free Qwen3-TTS Server (OpenAI Compatible)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/skills/openclaw-feishu-voice-free
Environment="PATH=/root/.openclaw/skills/openclaw-feishu-voice-free/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/root/.openclaw/skills/openclaw-feishu-voice-free/venv/bin/python scripts/server/tts-base-server-openai.py --port 8000 --clone voice_embedings/huopo_kexin.pt
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-feishu-voice-free-whisper openclaw-feishu-voice-free-tts
sudo systemctl start openclaw-feishu-voice-free-whisper openclaw-feishu-voice-free-tts
sudo systemctl status openclaw-feishu-voice-free-whisper openclaw-feishu-voice-free-tts
```

## 🔧 工作原理

### 工作流程

```
1. 用户在飞书发送语音消息
   ↓
2. OpenClaw 接收并下载音频文件到本地
   ↓
3. OpenClaw 通过 tools.media.audio 配置调用 Whisper 服务（HTTP API）
   POST http://localhost:8001/transcribe
   ↓
4. Whisper 服务识别语音为文字，返回给 OpenClaw
   ↓
5. OpenClaw 调用 LLM（如 GPT、Claude 等）生成文字回复
   ↓
6. OpenClaw 通过 messages.tts 配置调用 TTS 服务（OpenAI 兼容 API）
   POST http://localhost:8000/v1/audio/speech
   ↓
7. TTS 服务合成语音（自动清理括号内容和表情符号），返回 MP3 文件
   ↓
8. OpenClaw 发送语音消息给飞书用户
```

### 架构设计

- **OpenClaw**: 负责消息接收、LLM 调用、文件 IO、与飞书客户端通信
- **whisper-server**: 常驻内存的 Whisper 模型，提供 ASR 服务（HTTP API）
- **tts-base-server-openai**: 常驻内存的 Qwen3-TTS 模型，提供 TTS 服务（兼容 OpenAI API）
- **飞书客户端**: 用户发送语音消息，接收语音回复

### 文本清理

TTS 服务会自动清理 LLM 回复中的括号描述内容和表情符号，不会朗读：

```
输入: "(嘴角微笑) 今天天气真好😊 (看向窗外)"
输出: "今天天气真好"
```

清理规则：

- 移除所有圆括号内容：`(xxx)`
- 移除所有方括号内容：`[xxx]`
- 移除所有花括号内容：`{xxx}`
- 移除所有表情符号（Emoji）
- 清理多余空格和换行

## 📋 依赖要求

### Python 依赖

- `torch` - PyTorch 深度学习框架
- `transformers` - HuggingFace transformers（用于 Whisper）
- `accelerate` - 模型加速
- `soundfile` - 音频文件处理
- `requests` - HTTP 请求
- `qwen-tts` - Qwen3-TTS 模型
- `pydub` - 音频格式转换

所有依赖会在运行 `setup.sh` 时自动安装。

### 系统依赖

- `ffmpeg` - 音频处理（可选，推荐安装）

## ❓ 常见问题

### Q: setup.sh 失败，提示 Python 版本不兼容

**A:** 确保系统有 Python 3.10-3.12。检查版本：

```bash
python3 --version
```

如果不是 3.10-3.12，需要安装正确版本。

### Q: 服务启动失败

**A:** 检查以下几点：

1. **端口是否被占用**

```bash
netstat -tulpn | grep -E "(8000|8001)"
```

1. **依赖是否安装**

```bash
source venv/bin/activate
pip list | grep -E "(torch|transformers|qwen-tts)"
```

1. **查看服务日志**

```bash
tail -f /tmp/whisper-server.log
tail -f /tmp/tts-server.log
```

### Q: Skill 不触发

**A:** 检查配置和日志：

1. **检查配置**

```bash
cat /root/.openclaw/openclaw.json | grep -A 20 "openclaw-feishu-voice-free"
```

1. **检查 skill 是否加载**

```bash
openclaw skill list | grep openclaw-feishu-voice-free
```

1. **查看 OpenClaw 日志**

```bash
tail -f /root/.openclaw/logs/openclaw.log
```

### Q: TTS 不工作

**A:** 确保：

1. `messages.tts.auto: "always"` 已设置
2. `messages.tts.provider: "openai"` 已设置（使用 OpenAI 兼容 API）
3. `messages.tts.openai.baseUrl: "http://localhost:8000/v1"` 已设置
4. TTS 服务在运行（端口 8000）
5. 检查服务健康状态：`curl http://localhost:8000/`
6. 检查服务日志：`tail -f /tmp/tts-server.log`

### Q: 如何更换音色？

**A:** 有两种方式：

#### 方式1：使用音色克隆工具创建音色文件

```bash
cd /root/.openclaw/skills/openclaw-feishu-voice-free
source venv/bin/activate

# 从参考音频克隆音色并保存
python scripts/tools/tts-base.py \
  --audio /path/to/reference_audio.wav \
  --text "参考音频的文字内容" \
  --save-clone voice_embedings/my_voice.pt \
  --prompt "测试文本"

deactivate
```

#### 方式2：在启动服务时指定音色文件

```bash
# 使用绝对路径
python scripts/server/tts-base-server-openai.py --clone /path/to/your-voice.pt

# 或使用相对路径（从 skill 目录或 voice_embedings 目录）
python scripts/server/tts-base-server-openai.py --clone voice_embedings/my_voice.pt
```

**注意：** 

- 音色文件需要是 `.pt` 格式，使用 `scripts/tools/tts-base.py` 的 `--save-clone` 参数生成
- 修改音色后需要重启 TTS 服务才能生效
- 如果使用 systemd 管理服务，需要修改服务文件中的 `--clone` 参数

### Q: 服务无法连接

**A:** 检查以下几点：

1. **检查服务是否运行**

```bash
# 检查端口占用
netstat -tulpn | grep -E "(8000|8001)"

# 检查进程
ps aux | grep -E "(whisper-server|tts-base-server)"
```

1. **检查服务日志**

```bash
tail -f /tmp/whisper-server.log
tail -f /tmp/tts-server.log
```

1. **检查防火墙**

```bash
# 如果服务绑定在 0.0.0.0，确保防火墙允许端口
# Ubuntu/Debian
ufw allow 8000
ufw allow 8001
```

1. **检查模型文件**

```bash
# 检查 Whisper 模型
ls -lh /root/.openclaw/models/whisper/whisper-large-v3-turbo/

# 检查 Qwen3-TTS 模型
ls -lh /root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base/
```

### Q: 音色文件找不到

**A:** 检查以下几点：

1. **检查音色文件路径**

```bash
# 检查 voice_embedings 目录
ls -la /root/.openclaw/skills/openclaw-feishu-voice-free/voice_embedings/
```

1. **使用绝对路径**

如果相对路径不工作，使用绝对路径：

```bash
python scripts/server/tts-base-server-openai.py --clone /root/.openclaw/skills/openclaw-feishu-voice-free/voice_embedings/huopo_kexin.pt
```

1. **检查文件格式**

确保音色文件是 `.pt` 格式，并且是通过 `tts-base.py --save-clone` 生成的

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👤 作者

**Shuai Shi**

- 项目主页: [https://github.com/shuaishi1991/openclaw-feishu-voice-free](https://github.com/shuaishi1991/openclaw-feishu-voice-free)

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - 强大的 AI 助手框架
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) - 高质量的语音合成模型
- [Whisper](https://github.com/openai/whisper) - 优秀的语音识别模型

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐！

---

**注意**: 这是一个 OpenClaw Skill，需要先安装和配置 OpenClaw 才能使用。