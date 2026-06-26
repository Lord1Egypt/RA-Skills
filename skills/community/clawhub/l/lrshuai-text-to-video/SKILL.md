---
name: lrshuAI-text-to-video
version: 1.0.0
description: 文生视频技能。当你需要仅提供一段文本描述来生成视频时调用此技能。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Text to Video (文生视频)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-text-to-video` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
此技能包含仅需文本即可生成视频的模型。
- **Veo 3.1** (`veo_3_1`): 高质量视频生成模型。
- **Sora 2** (`sora-2`): 通用高质量视频生成模型。
- **Doubao Seedance 1.5 Pro** (`doubao-seedance-1_5-pro`): 豆包舞蹈视频生成。

## 调用示例
```bash
python script/invoke_model.py --model 'veo_3_1' --prompt '一个机器人在赛博朋克城市的街道上行走，下着雨'
```