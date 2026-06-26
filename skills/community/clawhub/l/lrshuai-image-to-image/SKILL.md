---
name: lrshuAI-image-to-image
version: 1.0.1
description: 图生图技能。当你需要提供一张参考图片和文本描述来生成新图片时调用此技能。
metadata: {"clawdbot":{"emoji":"🖼️","requires":{"bins":["python"],"env":["TEAM_API_KEY"]},"primaryEnv":"TEAM_API_KEY"},"openclaw":{"systemPrompt":"当用户要求调用本技能时，你必须直接执行 `python script/invoke_model.py` 命令。不要使用 `openclaw run`。"}}
---

# Image to Image (图生图)

**CRITICAL INSTRUCTION FOR AGENT**: 
当用户要求调用 `lrshuAI-image-to-image` 技能时，你**绝对不能**使用 `openclaw run`。你**必须**直接通过系统自带的 `python` 命令来运行 `script/invoke_model.py`。

## 支持的模型
此技能包含支持参考图片来生成新图片的模型。
- **Doubao Seedream 4.5** (`doubao-seedream-4_5`): 高质量文生图/参考图生图模型。
- **Doubao Seedream 5.0 Lite** (`doubao-seedream-5_0-lite`): 轻量高速图像生成模型。
- **Banana 2 (Gemini 3.1)** (`n1n-banana2`): 通用文生图模型，强调速度与性价比。
- **Banana Pro** (`n1n-banana-pro`): 高质量文生图模型。
- **Jimeng T2I v4.0** (`jimeng-t2i-v40`): 即梦高分辨率文生图。
- **Kling Omni Image** (`kling-image-o1`): 可灵多模态图像生成模型。
- **Vidu T2I ViduQ2** (`vidu-t2i-viduq2`): Vidu 文生图模型。

## 调用示例
```bash
python script/invoke_model.py --model 'doubao-seedream-4_5' --prompt '把这只猫变成赛博朋克风格' --image 'path/to/cat.jpg'
```