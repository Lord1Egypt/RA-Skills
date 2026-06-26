# mlx-stt - 基于 mlx-audio Whisper 的语音转文本技能

使用 mlx-audio Whisper 模型将音频转录为文本，完全在 Apple Silicon 上运行，无需 API 密钥。

## 触发条件

当用户请求以下操作时使用此技能：
- "转录这段音频"
- "把语音转成文字"
- "听写这个文件"
- "STT"
- "语音识别"
- "把录音转文字"

## 工具：mlx_stt

> **注意：** 本插件依赖 `mlx-audio` Python 库。使用前请确保已安装：
> ```bash
> uv tool install mlx-audio --prerelease=allow
> ```

### 转录音频

```json
{
  "action": "transcribe",
  "audioPath": "/path/to/audio.mp3",
  "language": "可选：语言代码 (zh/en 等)",
  "task": "可选：transcribe 或 translate"
}
```

**参数说明：**
- `action`: 必须是 "transcribe"
- `audioPath`: 音频文件路径（必需）
- `language`: 可选，语言代码（省略则自动检测）
- `task`: 可选，"transcribe"（转录）或 "translate"（翻译成英文）

**返回值：**
```json
{
  "success": true,
  "text": "转录的文本内容",
  "language": "检测到的语言",
  "duration": 5.2,
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "第一句话"
    }
  ]
}
```

### 检查状态

```json
{
  "action": "status"
}
```

返回 STT 服务器状态、加载的模型等信息。

### 重载配置

```json
{
  "action": "reload"
}
```

无需重启 OpenClaw 即可重载 STT 配置。

## 可用模型

### Whisper 系列

| 模型 | 语言 | 描述 | 内存需求 |
|------|------|------|----------|
| **whisper-large-v3-turbo** (推荐默认) | 99+ | 快速准确，日常使用 | ~2GB |
| **whisper-large-v3** | 99+ | 最高准确度 | ~6GB |
| **distil-large-v3** | EN | 蒸馏版，更快 | ~1.5GB |

### Qwen3 系列

| 模型 | 语言 | 描述 | 内存需求 |
|------|------|------|----------|
| **Qwen3-ASR-0.6B** | ZH, EN, JA, KO 等 | 轻量多语言 ASR | ~1GB |
| **Qwen3-ASR-1.7B** | ZH, EN, JA, KO 等 | 高精度多语言 ASR | ~4GB |
| **Qwen3-ForcedAligner-0.6B** | ZH, EN, JA, KO 等 | 词级时间戳对齐 | ~1GB |

### 其他模型

| 模型 | 语言 | 描述 | 内存需求 |
|------|------|------|----------|
| **Parakeet-TDT-0.6B-v3** | 25 EU 语言 | NVIDIA 高精度 | ~1.5GB |
| **VibeVoice-ASR-9B** | 多语言 | 说话人分离，长音频 (60min) | ~18GB |
| **Voxtral-Mini-3B** | 多语言 | Mistral 语音模型 | ~6GB |
| **Canary** | 25 EU + RU | NVIDIA 多语言 + 翻译 | ~2GB |
| **Moonshine** | EN | Useful Sensors 轻量 ASR | ~500MB |
| **MMS** | 1000+ | Meta 超大规模多语言 | 可变 |
| **Granite-Speech** | EN, FR, DE, ES, PT, JA | IBM ASR + 翻译 | ~4GB |

## CLI 命令

| 命令 | 描述 |
|------|------|
| `/mlx-stt status` | 查看 STT 服务器状态 |
| `/mlx-stt transcribe <音频路径>` | 转录音频文件 |
| `/mlx-stt reload` | 重载 STT 配置 |
| `/mlx-stt models` | 列出可用模型 |

## 使用示例

### 基础转录（自动检测语言）

```json
{
  "action": "transcribe",
  "audioPath": "/tmp/recording.m4a"
}
```

### 指定语言

```json
{
  "action": "transcribe",
  "audioPath": "/tmp/chinese_audio.mp3",
  "language": "zh"
}
```

### 翻译成英文

```json
{
  "action": "transcribe",
  "audioPath": "/tmp/foreign_audio.mp3",
  "task": "translate"
}
```

### 使用特定模型

在配置中指定，或使用时覆盖。

## 支持的音频格式

- MP3
- WAV
- M4A
- FLAC
- OGG
- WebM
- MP4（提取音频）

## 注意事项

- **完全本地**：所有处理在本地完成，数据不出机器
- **自动语言检测**：不指定 language 时自动检测
- **时间戳**：返回结果包含每个片段的时间戳
- **长音频**：支持长音频文件，自动分段处理
- **背景噪音**：Whisper 对背景噪音有一定鲁棒性

## 配置

在 `openclaw.json` 中配置：

```json
{
  "plugins": {
    "entries": {
      "openclaw-mlx-audio": {
        "config": {
          "stt": {
            "enabled": true,
            "model": "mlx-community/whisper-large-v3-turbo",
            "port": 19290,
            "language": "zh",
            "pythonEnvMode": "managed"
          }
        }
      }
    }
  }
}
```

## 故障排除

### STT 服务器未启动

检查状态：
```bash
/voice-stt status
```

如果显示未运行，检查配置中的 `enabled` 是否为 `true`。

### 转录失败

1. 检查音频文件是否存在
2. 检查音频格式是否支持
3. 查看服务器日志

### 识别准确度低

- 尝试使用更大的模型（如 whisper-large-v3）
- 指定正确的语言代码
- 确保音频质量良好（减少背景噪音）

### 处理速度慢

- 使用更小的模型（如 whisper-turbo 或 whisper-small）
- 缩短音频长度
- 确保没有其他高负载任务

## 高级用法

### 批量转录

可以循环调用 transcribe 处理多个文件。

### 实时转录

结合音频录制工具，实现近实时的语音转文字。

### 多语言混合

Whisper v3 支持多语言混合音频的自动检测和转录。
