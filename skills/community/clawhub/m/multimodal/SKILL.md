---
name: Multimodal Analyzer
slug: multimodal
version: 1.0.0
description: 使用GLM-4.6V模型进行多模态内容理解（图片、视频、文档）
---

# Multimodal Understanding Skill

使用智谱GLM-4.6V模型理解图片、视频、文档内容。

## 功能

- 图片理解：OCR、场景分析、物体检测、属性识别
- 视频理解：内容摘要、关键帧分析
- 文档理解：PDF、复杂表格解析
- 深度思考模式：开启后进行深层推理分析

## 使用方式

```
理解这张图片：[图片URL或本地路径]
分析这个视频：[视频URL]
这个PDF讲什么：[PDF URL]
```

## 技术细节

- 模型：GLM-4.6V (106B, 128K上下文)
- API端点：https://open.bigmodel.cn/api/paas/v4/chat/completions
- 需要ZHIPU_API_KEY环境变量

## 限制

- 不支持同时处理图片+视频+文件（只能选一种模态）
- 视频URL需要公网可访问

## 调用脚本

调用 `scripts/analyze.py` 进行分析：

```bash
python scripts/analyze.py --type image|video|file --input <url_or_path> --prompt "你的问题"
```

参数：
- `--type`: 输入类型 (image/video/file)
- `--input`: URL或本地文件路径
- `--prompt`: 分析提示词
- `--thinking`: 启用深度思考模式
- `--stream`: 流式输出
