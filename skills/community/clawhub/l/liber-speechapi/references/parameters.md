# Liber SpeechAPI 参数说明文档

## 概述

Liber SpeechAPI skill 提供三类能力：

1. **Telegram/openclaw 语音工作流**：语音输入 → ASR → 回复压缩 → Telegram OGG/Opus TTS
2. **通用文字转语音**：显式把文本合成为音频，默认输出 `wav`
3. **通用语音转文字**：显式把音频转为结构化识别结果，默认输出 `json`

配置支持 `config.json` 中的 `default` 值，表示使用后端默认参数，不在请求中传递该字段。

---

## 配置文件结构

### config.json 格式

```json
{
    "asr": {
        "model": "openai/whisper-large-v3",
        "language": "zh",
        "task": "transcribe",
        "timestamps": "chunk"
    },
    "tts": {
        "model": "multilingual",
        "language": "zh",
        "format": "wav"
    },
    "global": {
        "voice_summary_limit": 100,
        "telegram_tts_format": "ogg_opus",
        "asr_output": "json"
    }
}
```

### 默认值处理规则

- 如果参数值为 `default` 或 `null`，请求时不传递该字段
- 使用后端服务器默认值
- `tts.format` 用于通用 TTS 默认输出格式
- `global.telegram_tts_format` 用于 Telegram 场景语音格式
- `global.asr_output` 用于通用 ASR 默认输出模式

---

## ASR 参数详解 (Insanely Fast Whisper)

### 核心参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `model` | string | `openai/whisper-large-v3` | 预训练模型名称 |
| `language` | string | `zh` | 输入音频语言 |
| `task` | string | `transcribe` | 任务类型：`transcribe` 或 `translate` |
| `timestamps` | string | `chunk` | 时间戳粒度：`chunk` 或 `word` |

### 性能参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `batch_size` | integer | 后端默认 | 并行计算批次大小 |
| `flash` | boolean | 后端默认 | 是否使用 Flash Attention 2 加速 |

### 高级功能参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `hf_token` | string | `null` | Hugging Face 访问令牌 |
| `diarization_model` | string | 后端默认 | 说话人分割模型 |
| `num_speakers` | integer | `null` | 确切说话人数量 |
| `min_speakers` | integer | `null` | 最小说话人数量 |
| `max_speakers` | integer | `null` | 最大说话人数量 |
| `transcript_path` | string | 后端默认 | 转录结果保存路径 |

### 输出模式

| 模式 | 默认值 | 描述 |
|------|--------|------|
| `json` | 是 | 返回完整 ASR JSON |
| `text` | 否 | 仅返回识别文本 |

---

## TTS 参数详解 (Chatterbox)

### 模型配置

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `model` | string | `multilingual` | 模型类型：`multilingual`、`turbo`、`standard` |
| `language` | string | `zh` | 输出语言 |
| `format` | string | `wav` | 通用 TTS 默认输出格式 |

### 生成参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `repetition_penalty` | float | 后端默认 | 重复惩罚系数 |
| `temperature` | float | 后端默认 | 采样温度 |
| `top_p` | float | 后端默认 | 核采样概率阈值 |
| `top_k` | integer | 后端默认 | Top-K 采样 |
| `norm_loudness` | boolean | 后端默认 | 是否标准化音频响度 |
| `exaggeration` | float | 后端默认 | 夸张度系数 |
| `cfg_weight` | float | 后端默认 | 无分类器引导权重 |

### 输出格式规则

| 场景 | 默认输出 |
|------|----------|
| 直接文字转语音 | `wav` |
| Telegram 语音回复 | `ogg_opus` |
| 显式指定格式 | 使用用户指定格式 |

---

## 全局参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `voice_summary_limit` | integer | 100 | 语音回复文本长度限制 |
| `default_clone_audio` | string | `tmp/clone.wav` | 默认声音克隆参考音频路径 |
| `telegram_tts_format` | string | `ogg_opus` | Telegram 语音输出格式 |
| `asr_output` | string | `json` | 通用 ASR 默认输出模式 |

---

## 常见配置场景

### 场景 1: 通用文字转语音

```json
{
    "tts": {
        "model": "multilingual",
        "language": "zh",
        "format": "wav"
    }
}
```

### 场景 2: Telegram/openclaw 语音回复

```json
{
    "tts": {
        "model": "multilingual",
        "language": "zh",
        "format": "wav"
    },
    "global": {
        "telegram_tts_format": "ogg_opus",
        "voice_summary_limit": 100
    }
}
```

### 场景 3: 通用语音转文字

```json
{
    "asr": {
        "language": "zh",
        "task": "transcribe",
        "timestamps": "word"
    },
    "global": {
        "asr_output": "json"
    }
}
```

### 场景 4: 语音克隆

```json
{
    "tts": {
        "model": "multilingual",
        "language": "zh",
        "cfg_weight": 0.5
    },
    "global": {
        "default_clone_audio": "tmp/clone.wav"
    }
}
```

---

## 参数优化建议

### 性能优化

- GPU 设备建议使用 `flash=true`
- 内存不足时减小 `batch_size`
- 快速转录可使用更轻模型

### 质量优化

- 使用 `openai/whisper-large-v3` 获得更好的识别质量
- TTS 使用 `standard` 模型获得更高音质
- 调整 `cfg_weight` 控制克隆相似度
