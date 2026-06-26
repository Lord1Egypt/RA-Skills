---
name: lrshuAI-voice-clone
version: 1.0.0
description: 声音克隆技能。当你需要提供一段参考音频，并生成使用该声音说话的新音频时调用此技能。
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Voice Clone (声音克隆)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-voice-clone` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
- **Kling Audio Clone** (`kling-audio-clone`): 可灵音色克隆模型。
- **Vidu Audio Clone** (`vidu-audio-clone`): Vidu 音色克隆模型。

## 调用示例
```bash
python script/invoke_model.py --model 'kling-audio-clone' --prompt '这是克隆出来的声音，你好啊！' --audio 'path/to/reference_audio.wav'
```