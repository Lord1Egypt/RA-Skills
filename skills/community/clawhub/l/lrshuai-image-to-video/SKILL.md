---
name: lrshuAI-image-to-video
version: 1.0.2
description: 参考生视频技能。当你需要提供一张图片和文本描述来生成视频时调用此技能。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Image to Video (参考生视频)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-image-to-video` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
此技能包含支持单张图片和文本生成视频的模型。
- **Veo 3.1** (`veo_3_1`): 高质量视频生成模型。
- **Sora 2** (`sora-2`): 通用高质量视频生成模型。
- **Kling V3** (`kling-v3`): 可灵 V3 视频生成模型。
- **Kling V3 Omni** (`kling-v3-omni`): 可灵 Omni 视频模型。
- **Vidu I2V ViduQ2** (`vidu-i2v-viduq2`): Vidu 图生视频模型。
- **Jimeng OmniHuman 1.5** (`jimeng-omnihuman-1_5`): 即梦数字人视频生成。
- **Bailian Wan2 6 R2V** (`bailian-wan2_6-r2v`): 阿里百炼 Wan2 视频生成。
- **Bailian Wan2 6 R2V Flash** (`bailian-wan2_6-r2v-flash`): 阿里百炼 Wan2 视频生成（极速版）。

## 调用示例
```bash
python script/invoke_model.py --model 'veo_3_1' --prompt '镜头平移，画面中的人物开始微笑' --image 'path/to/image.jpg'
```