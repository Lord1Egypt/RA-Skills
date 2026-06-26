---
name: lrshuAI-sfx-generation
version: 1.0.0
description: 音效生成技能。当你需要根据文本描述生成环境音效或特殊声效时调用此技能。
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# SFX Generation (音效生成)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-sfx-generation` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
- **Keling SFX** (`keling-audio-sfx`): 音效生成模型。

## 调用示例
```bash
python script/invoke_model.py --model 'keling-audio-sfx' --prompt '星球大战中光剑挥舞的声音'
```