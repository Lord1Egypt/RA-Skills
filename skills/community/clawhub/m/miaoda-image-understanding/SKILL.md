---
name: miaoda-image-understanding
description: "Use when user needs to understand, analyze, or describe image content. Do NOT use Read tool to read images — use this skill instead. Supports local file path input. 触发词：图片理解, 图片分析, 图片描述, 识别图片, 看图, 图片识别, image understanding, describe image, analyze image, 图片内容, 看看这张图, 这张图是什么, 图中有什么"
---

# Image Understanding

通过 `miaoda-studio-cli image-understanding` 使用 AI 理解、分析和描述图片内容。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--image, -i` | 本地图片文件路径 | 是 | - |
| `--prompt, -p` | 关于图片的问题或指令 | 否 | 请描述这张图片的内容 |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 使用示例

```bash
# 基础用法：描述图片内容
miaoda-studio-cli image-understanding --image ./photo.png

# 针对图片提问
miaoda-studio-cli image-understanding --image ./photo.png --prompt "这张图片中有什么"

# 分析本地图片并输出 JSON
miaoda-studio-cli image-understanding --image ./screenshot.png --prompt "提取图片中的文字" --output json

# 简写参数
miaoda-studio-cli image-understanding -i ./photo.jpg -p "分析图片的色彩风格"
```

## 使用场景决策

```
需要理解图片内容
├─ 描述图片整体内容 → 不指定 --prompt，使用默认描述
├─ 针对图片提问 → 用 --prompt 指定具体问题
├─ 提取图片中的文字 → --prompt "提取图片中的文字"
├─ 分析图片风格/构图 → --prompt 描述分析需求
└─ 需要程序处理结果 → 加 --output json
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 本地文件路径包含空格未加引号 | 路径有空格时用引号包裹：`-i "my image.png"` |
| 用此命令处理文档（PDF/Word） | 文档解析用 `miaoda-studio-cli doc-parse`（见 miaoda-doc-parse skill） |
| prompt 过于模糊（如"分析"） | 明确指定需求，如"提取文字"、"描述场景"、"识别物体" |
