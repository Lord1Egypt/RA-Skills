---
name: local-gmncode-vision
description: 当内置 image 工具不可用、但本机配置了 GMNCODE_API_KEY 时，使用本地脚本直连 GMNCODE Responses API 完成图片理解。适用于角色识别、图片描述、风格分析、截图理解等任务。
---

# local-gmncode-vision

当你发现：
- `image` 工具报错
- 错误包含 `No media-understanding provider registered`
- 当前环境已有 `GMNCODE_API_KEY`

就用这个技能。

## 用法

脚本路径：
`/home/ubuntu/.openclaw/workspace/scripts_gmncode_image.py`

基础调用：

```bash
/home/ubuntu/.openclaw/workspace/scripts_gmncode_image.py <image_path> "你的提示词"
```

示例：

```bash
/home/ubuntu/.openclaw/workspace/scripts_gmncode_image.py /path/to/image.jpg "识别这张图里的角色；如果无法确认具体角色，就描述人物外观、服饰和可能风格来源。"
```

## 适用场景

- 识别二次元/国漫/游戏角色
- 描述人物外观、服装、风格
- 分析截图界面内容
- 在官方 image 工具失效时提供稳定替代

## 注意事项

- 依赖环境变量：`GMNCODE_API_KEY`
- 当前默认模型：`gpt-5.4`
- 这是本地替代方案，不是 OpenClaw 官方 image provider 修复
- 如果后续官方 image 工具修好，优先用官方工具

## 输出原则

- 不确定时明确说“不确定”
- 可以给出“更像谁”的概率判断
- 不要把风格像误说成实锤出处
