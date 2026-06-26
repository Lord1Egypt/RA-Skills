---
name: lrshuAI-first-tail-frame-to-video
version: 1.0.2
description: 首尾帧生视频技能。当你需要提供首帧图片和尾帧图片来控制视频的起止画面并生成视频时调用。
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# First & Tail Frame to Video (首尾帧生视频)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-first-tail-frame-to-video` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
- **Jimeng I2V First Tail v3.0** (`jimeng-i2v-first-tail-v30`): 即梦图生视频首尾帧模型。
- **Veo 3.1** (`veo_3_1`): 高质量视频生成模型 (支持首尾帧)。
- **Kling V3** (`kling-v3`): 可灵 V3 视频生成模型 (支持首尾帧)。
- **Kling V3 Omni** (`kling-v3-omni`): 可灵 Omni 视频模型 (支持首尾帧)。
- **Doubao Seedance 1.5 Pro** (`doubao-seedance-1_5-pro`): 豆包舞蹈视频生成模型 (支持首尾帧)。

## 调用示例
```bash
# 注意：当前脚本将 `--image` 作为首帧传递，`--image-tail` 作为尾帧传递，
# 并将 `--prompt` 作为视频描述传递。
# 请确保首帧和尾帧的尺寸相同，否则可能会导致视频生成问题。
python script/invoke_model.py --model 'jimeng-i2v-first-tail-v30' --prompt '从白天变成黑夜' --image 'path/to/first_frame.jpg' --image-tail 'path/to/tail_frame.jpg'
```