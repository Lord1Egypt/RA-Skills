---
name: li-feishu-audio
description: 飞书语音交互技能。支持语音消息自动识别、AI 处理、语音回复全流程。需要配置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量。使用 faster-whisper 进行语音识别，Edge TTS 进行语音合成，自动转换 OPUS 格式并通过飞书发送。适用于飞书平台的语音对话场景。
---

# Li Feishu Audio - 飞书语音交互技能

## 快速开始

本技能提供完整的飞书语音交互能力：

```
用户语音 → faster-whisper 识别 → AI 处理 → Edge TTS 合成 → OPUS 转换 → 飞书发送
```

## 核心组件

### 1. 语音识别 (fast-whisper)

**脚本**: `scripts/fast-whisper-fast.sh`

**用法**:
```bash
./scripts/fast-whisper-fast.sh <音频文件.ogg>
```

**配置**:
- 模型：faster-whisper tiny
- 语言：中文 (zh)
- 模型目录：可配置（环境变量 `FAST_WHISPER_MODEL_DIR`）
- 虚拟环境：技能目录下的 `.venv`（自动创建）

### 2. 语音合成 (Edge TTS)

**脚本**: `scripts/tts-voice.sh`

**用法**:
```bash
./scripts/tts-voice.sh "文本内容" [输出文件.mp3]
```

**配置**:
- 音色：zh-CN-XiaoxiaoNeural (中文女声)
- 输出格式：MP3 (自动转换为 OPUS)
- 虚拟环境：技能目录下的 `.venv`（自动创建）

### 3. 飞书语音发送

**脚本**: `scripts/feishu-tts.sh`

**用法**:
```bash
./scripts/feishu-tts.sh <音频文件.mp3> [用户 ID]
```

**配置**:
- 飞书 AppID: 从环境变量或 openclaw.json 读取
- 音频格式：OPUS (48kHz, 自动转换)
- 消息类型：audio

### 4. 自动清理

**脚本**: `scripts/cleanup-tts.sh`

**用法**:
```bash
./scripts/cleanup-tts.sh [保留数量]
```

**定时任务**: 每天凌晨 2 点自动执行

## 完整工作流

### 接收用户语音消息

1. 飞书收到语音消息（OGG/OPUS 格式）
2. 保存到 OpenClaw 媒体目录（自动处理）
3. 调用 `fast-whisper-fast.sh` 识别

### 生成回复

1. 识别结果发送给大模型
2. 大模型生成文字回复
3. 调用 `tts-voice.sh` 生成语音

### 发送语音回复

1. TTS 生成 MP3 文件
2. `sendMediaFeishu` 自动转换为 OPUS
3. 通过飞书 API 发送语音消息

## 环境要求

### 系统依赖

```bash
# Python
Python 3.11+
uv 包管理器

# 音频处理
ffmpeg (支持 OPUS 编码)
jq (JSON 处理)

# 飞书 API
飞书开放平台应用凭证
```

### Python 环境

```bash
# 虚拟环境
技能目录/.venv （自动创建）

# 已安装包
faster-whisper==1.2.1
edge-tts==7.2.7
```

### 模型文件

```bash
# 语音识别模型
$FAST_WHISPER_MODEL_DIR/models--Systran--faster-whisper-tiny/
```

## 配置说明

### 飞书凭证

**方法 1: 环境变量**（推荐）

创建 `.env` 文件：
```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**方法 2: openclaw.json**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

**⚠️ 安全提示**：不要将凭证提交到版本控制系统！

### 自定义目录（可选）

在 `.env` 文件中配置：

```bash
# 模型目录（默认：$HOME/.fast-whisper-models）
export FAST_WHISPER_MODEL_DIR="/opt/fast-whisper-models"

# 虚拟环境目录（默认：技能目录/.venv）
export VENV_DIR="/path/to/venv"

# 临时文件目录（默认：/tmp）
export TEMP_DIR="/tmp"

# 日志目录（默认：技能目录/logs）
export LOG_DIR="/path/to/logs"

# OpenClaw 配置路径（默认：$HOME/.openclaw/openclaw.json）
export OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
```

### TTS 配置

```json
{
  "messages": {
    "tts": {
      "auto": "always",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoxiaoNeural",
        "lang": "zh-CN"
      }
    }
  }
}
```

## 脚本说明

### fast-whisper-fast.sh

```bash
#!/bin/bash
# 语音识别脚本
export HF_ENDPOINT=https://hf-mirror.com  # 国内镜像
VENV_PYTHON="技能目录/.venv/bin/python"  # 由 install.sh 自动配置

# 用法
./fast-whisper-fast.sh <音频文件>
```

**输出格式**:
```
[0.00s -> 2.32s] 识别的文本内容
```

### tts-voice.sh

```bash
#!/bin/bash
# TTS 语音生成脚本
export HF_ENDPOINT=https://hf-mirror.com
VENV_PYTHON="技能目录/.venv/bin/python"

# 用法
./tts-voice.sh "文本内容" [输出文件.mp3]
```

### feishu-tts.sh

```bash
#!/bin/bash
# 飞书语音发送脚本
# 自动转换 MP3 → OPUS

# 用法
./feishu-tts.sh <音频文件.mp3> [用户 ID]
```

**转换参数**:
```bash
ffmpeg -y -i input.mp3 -acodec libopus -ar 48000 -ac 1 output.opus
```

### cleanup-tts.sh

```bash
#!/bin/bash
# TTS 临时文件清理脚本

# 用法
./cleanup-tts.sh [保留数量]  # 默认保留 10 个

# 定时任务（crontab）
0 2 * * * ./cleanup-tts.sh 10
```

## 故障排查

### 语音识别失败

**问题**: 无法识别语音内容

**检查**:
1. 模型是否下载：`ls $FAST_WHISPER_MODEL_DIR/`
2. 虚拟环境：`技能目录/.venv/bin/python --version`
3. 网络：`export HF_ENDPOINT=https://hf-mirror.com`

### TTS 生成失败

**问题**: 无法生成语音文件

**检查**:
1. edge-tts 安装：`uv pip list -p 技能目录/.venv | grep edge`
2. 网络连接：Edge TTS 需要访问微软服务
3. 输出目录权限

### 飞书发送失败

**问题**: 语音消息发送失败

**检查**:
1. 凭证配置：`echo $FEISHU_APP_ID`
2. 音频格式：必须是 OPUS
3. 用户 ID 类型：使用 open_id

## 性能指标

| 操作 | 耗时 |
|------|------|
| 语音识别 (tiny) | ~8-10 秒 |
| TTS 生成 | ~3-5 秒 |
| OPUS 转换 | <1 秒 |
| 飞书上传 | ~2-3 秒 |
| **总计** | **~15 秒** |

## 最佳实践

### 语音质量

1. **录音环境**: 安静环境，减少背景噪音
2. **说话速度**: 正常语速，避免过快
3. **音频格式**: 飞书自动发送 OPUS 格式

### 文件管理

1. **定期清理**: 每天凌晨自动清理
2. **保留策略**: 保留最近 10 个 TTS 目录
3. **空间上限**: 100MB 自动清理

### 错误处理

1. **识别误差**: 允许用户文字补充
2. **发送失败**: 降级为文字回复
3. **超时处理**: 设置合理超时时间

## 扩展功能

### 添加新音色

编辑 `tts-voice.sh`:

```python
# 中文男声
communicate = edge_tts.Communicate(TEXT, "zh-CN-YunxiNeural")

# 英文女声
communicate = edge_tts.Communicate(TEXT, "en-US-MichelleNeural")
```

### 调整语速音调

```python
# 在 edge_tts 中调整
communicate = edge_tts.Communicate(
    TEXT, 
    "zh-CN-XiaoxiaoNeural",
    rate="+10%",   # 语速
    pitch="-5%"    # 音调
)
```

### 支持更多语言

修改 `fast-whisper-fast.sh`:

```bash
# 多语言识别
model.transcribe("$AUDIO_FILE", language="auto")
```

## 相关文件

- **配置**: `.env` 文件或 openclaw.json
- **脚本**: 技能目录下的 `scripts/`
- **模型**: 可配置（`FAST_WHISPER_MODEL_DIR`，默认 `$HOME/.fast-whisper-models`）
- **临时文件**: 可配置（`TEMP_DIR`，默认 `/tmp`）
- **虚拟环境**: 可配置（`VENV_DIR`，默认 技能目录/.venv）
- **日志**: 可配置（`LOG_DIR`，默认 技能目录/logs）

## 版本信息

- **技能版本**: 0.1.3.1
- **作者**: 北京老李 (BeijingLL)
- **faster-whisper**: 1.2.1
- **edge-tts**: 7.2.7
- **Python**: 3.11

## 安全与供应链

### 必需的凭证

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `FEISHU_APP_ID` | ✅ | 飞书应用 ID (cli_xxx) |
| `FEISHU_APP_SECRET` | ✅ | 飞书应用密钥 |
| `FAST_WHISPER_MODEL_DIR` | ❌ | 模型目录，默认 `~/.fast-whisper-models` |
| `VENV_DIR` | ❌ | 虚拟环境目录，默认技能目录下 `.venv` |
| `TEMP_DIR` | ❌ | 临时文件目录，默认 `/tmp` |
| `OPENCLAW_CONFIG` | ❌ | OpenClaw 配置路径 |
| `LOG_DIR` | ❌ | 日志目录，默认技能目录下 `logs` |

### 外部依赖说明

**HuggingFace 镜像**: 默认使用 `https://hf-mirror.com` 加速国内下载，可通过环境变量 `HF_ENDPOINT` 修改。

**uv 安装**: `install.sh` 会在未安装 `uv` 时提示安装命令。建议从官方源验证后再执行。

**Microsoft Edge TTS**: TTS 服务调用微软 Azure 语音服务，需要网络访问。

## 安全说明

### 凭证管理

- ✅ 使用环境变量存储敏感凭证
- ✅ 不要将 `.env` 提交到版本控制
- ✅ 将 `.env` 加入 `.gitignore`

### 路径配置

- ✅ 使用可配置的路径（环境变量）
- ✅ 避免硬编码个人路径
- ✅ 使用相对路径或系统级目录

### 临时文件

- ✅ 定期清理临时文件
- ✅ 使用系统临时目录 `/tmp/`
- ✅ 设置合理的保留策略
