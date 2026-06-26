# mlx-tts - 基于 mlx-audio 的文本转语音技能

使用 mlx-audio 将文本转换为语音，完全在 Apple Silicon 上运行，无需 API 密钥。

## 触发条件

当用户请求以下操作时使用此技能：
- "朗读这段文字"
- "把这段话转成语音"
- "用声音说..."
- "TTS"
- "语音合成"

## 工具：mlx_tts

> **注意：** 本插件依赖 `mlx-audio` Python 库。使用前请确保已安装：
> ```bash
> uv tool install mlx-audio --prerelease=allow
> ```

### 生成语音

```json
{
  "action": "generate",
  "text": "要合成的文本",
  "outputPath": "/tmp/output.mp3",
  "model": "可选：指定模型",
  "langCode": "可选：语言代码 (zh/en/ja 等)",
  "speed": "可选：语速倍数 (1.0 为正常)"
}
```

**参数说明：**
- `action`: 必须是 "generate"
- `text`: 要转换为语音的文本（必需）
- `outputPath`: 输出文件路径，限制在 `/tmp` 或 `~/.openclaw/voice/outputs/`
- `model`: 可选，覆盖默认模型
- `langCode`: 可选，语言代码（Kokoro 模型需要）
- `speed`: 可选，语速倍数（0.5-2.0）

**返回值：**
```json
{
  "success": true,
  "outputPath": "/tmp/output.mp3",
  "duration": 2.5,
  "model": "使用的模型名称"
}
```

### 检查状态

```json
{
  "action": "status"
}
```

返回 TTS 服务器状态、加载的模型、启动时间等信息。

### 重载配置

```json
{
  "action": "reload"
}
```

无需重启 OpenClaw 即可重载 TTS 配置。

## 可用模型

| 模型 | 语言 | 描述 | 内存需求 |
|------|------|------|----------|
| **Kokoro-82M** (推荐默认) | EN, JA, ZH, FR, ES, IT, PT, HI | 快速轻量，54 种预设声音 | ~500MB |
| **Qwen3-TTS-0.6B** | ZH, EN, JA, KO 等 | 中文质量优秀，支持声音克隆 | ~2.5GB |
| **Qwen3-TTS-1.7B** | ZH, EN, JA, KO 等 | 声音设计，根据描述生成 | ~16GB+ |
| **Chatterbox** | 16 种语言 | 最广泛的语言覆盖 | ~16GB+ |
| **CSM-1B** | EN | 对话式语音，支持声音克隆 | ~2GB |
| **Dia-1.6B** | EN | 对话-focused TTS | ~4GB |
| **Spark-TTS-0.5B** | EN, ZH | 高效 TTS | ~1GB |
| **Soprano-1.1-80M** | EN | 高质量轻量 TTS | ~200MB |
| **OuteTTS-0.6B** | EN | 高效 TTS | ~1.5GB |
| **Ming-omni-0.5B** (Dense) | EN, ZH | 轻量 MoE，声音克隆 | ~1GB |
| **Ming-omni-16.8B** (BailingMM) | EN, ZH | MoE 多模态，语音/音乐/事件 | ~32GB+ |

## CLI 命令

| 命令 | 描述 |
|------|------|
| `/mlx-tts status` | 查看 TTS 服务器状态 |
| `/mlx-tts test <文本>` | 测试生成语音 |
| `/mlx-tts reload` | 重载 TTS 配置 |
| `/mlx-tts models` | 列出可用模型 |

## 使用示例

### 基础用法

```json
{
  "action": "generate",
  "text": "你好，我是你的 AI 助手"
}
```

### 指定输出路径

```json
{
  "action": "generate",
  "text": "欢迎使用 OpenClaw",
  "outputPath": "~/.openclaw/voice/outputs/welcome.mp3"
}
```

### 使用特定模型和语言

```json
{
  "action": "generate",
  "text": "Hello, this is a test",
  "model": "mlx-community/Kokoro-82M",
  "langCode": "en"
}
```

### 调整语速

```json
{
  "action": "generate",
  "text": "慢慢朗读这段话",
  "speed": 0.8
}
```

## 注意事项

- **首次生成较慢**：模型需要预热，首次请求可能需要几秒
- **完全本地**：所有处理在本地完成，数据不出机器
- **路径限制**：输出路径必须在 `/tmp` 或 `~/.openclaw/voice/outputs/`
- **符号链接检查**：输出路径中的符号链接会被拒绝
- **文件大小限制**：超过 64MB 的音频会被拒绝

## 配置

在 `openclaw.json` 中配置：

```json
{
  "plugins": {
    "entries": {
      "openclaw-mlx-audio": {
        "config": {
          "tts": {
            "enabled": true,
            "model": "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16",
            "port": 19280,
            "langCode": "zh",
            "pythonEnvMode": "managed"
          }
        }
      }
    }
  }
}
```

## 故障排除

### TTS 服务器未启动

检查状态：
```bash
/voice-tts status
```

如果显示未运行，检查配置中的 `enabled` 是否为 `true`。

### 生成失败

1. 检查文本是否为空
2. 检查输出路径是否合法
3. 查看服务器日志

### 模型下载慢

模型首次使用会下载到 `~/.cache/huggingface/hub/`，可以使用镜像加速。
