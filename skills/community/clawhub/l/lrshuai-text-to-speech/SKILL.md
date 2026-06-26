---
name: lrshuAI-text-to-speech
version: 1.0.0
description: 文字转语音技能。当你需要将文本转换为自然的人声朗读时调用此技能。
metadata: {"clawdbot":{"emoji":"🗣️","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Text to Speech (文字转语音)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-text-to-speech` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
- **Gemini 2.5 Pro TTS** (`n1n-gemini-2.5-pro-preview-tts`): 文本转语音模型。
- **Doubao TTS** (`doubao-tts`): 豆包文本转语音模型。
- **Keling TTS** (`keling-tts`): 可灵文本转语音模型。

## 调用示例
```bash
python script/invoke_model.py --model 'doubao-tts' --prompt '你好，欢迎使用文字转语音服务！'
```