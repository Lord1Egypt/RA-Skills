---
name: MiniMax TTS
description: 调用 MiniMax 语音合成 API 生成语音。支持系统音色、克隆音色、流式/非流式输出。使用场景：用户需要生成高质量中文语音、语音合成、文本转语音。
homepage: https://platform.minimax.io/docs/api-reference/speech-t2a-http
metadata:
  openclaw:
    emoji: 🎙️
    requires:
      bins: [python3]
      env: [MINIMAX_API_KEY]
      pip: [requests]
    primaryEnv: MINIMAX_API_KEY
    envHelp:
      MINIMAX_API_KEY:
        required: true
        description: MiniMax API Key
        howToGet: 1. 打开 https://platform.minimax.io
2. 注册账号并登录
3. 获取 API Key（账户管理 → API Keys）
        url: https://platform.minimax.io
---

# MiniMax TTS Skill

调用 MiniMax TTS API 生成语音。

## 配置

设置环境变量：
```bash
export MINIMAX_API_KEY="your-api-key"
```

## 使用方式

### 命令行

```bash
python3 ~/.openclaw/workspace/skills/minimax-tts/scripts/tts.py "要转语音的文本"
```

### 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` | 要转语音的文本 | 必填 |
| `--model` | 模型 | speech-2.8-turbo |
| `--voice` | 音色ID | Chinese_Male_Adult |
| `--speed` | 语速 | 1.0 |
| `--format` | 音频格式 | mp3 |
| `--output` | 输出文件 | output.mp3 |

### 示例

```bash
# 基本用法
python3 ~/.openclaw/workspace/skills/minimax-tts/scripts/tts.py "你好世界"

# 指定音色和模型
python3 ~/.openclaw/workspace/skills/minimax-tts/scripts/tts.py "你好世界" --voice Chinese_Female_Adult --model speech-2.8-hd

# 保存到指定文件
python3 ~/.openclaw/workspace/skills/minimax-tts/scripts/tts.py "测试语音" --output test.mp3
```

## 可用音色

调用 `get_voice` API 获取当前账号下所有音色：

```bash
python3 ~/.openclaw/workspace/skills/minimax-tts/scripts/tts.py --list-voices
```

常见系统音色：
- `Chinese_Male_Adult` - 中文男声
- `Chinese_Female_Adult` - 中文女声
- `English_Male_Adult` - 英文男声
- `English_Female_Adult` - 英文女声

## 支持的模型

| 模型 | 特点 |
|------|------|
| speech-2.8-hd | 最高质量，40+语言 |
| speech-2.8-turbo | 低延迟 |
| speech-2.6-hd | 高相似度 |
| speech-2.6-turbo | 性价比高 |
