---
name: lrshuAI-music-generation
version: 1.0.1
description: 音乐生成技能。当你需要根据文本描述或风格要求生成完整的音乐曲目时调用此技能。
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Music Generation (音乐生成)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-music-generation` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
- **Suno Music** (`suno_music`): 高质量全曲生成模型

## 调用示例
```bash
python script/invoke_model.py --model 'suno_music' --prompt '一首欢快的赛博朋克风格电子乐'
```