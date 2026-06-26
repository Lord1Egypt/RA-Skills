---
name: ollama-t2i
description: 本地 Ollama 文生图工具。使用 x/z-image-turbo 模型生成图片，分辨率 1024x1024，每张图约耗时 90 秒。当用户说"生成图片"、"文生图"、"画一张图"、或提交中文提示词生成图像时使用。
---

# Ollama 文生图 (Text-to-Image)

## 环境要求

- Ollama 服务运行于 `http://localhost:11434`
- 模型：`x/z-image-turbo`（需提前拉取 `ollama pull x/z-image-turbo`）
- 输出目录：`images/`（自动创建）

## 使用方法

### Python 脚本

运行以下命令生成图片：

```bash
python3 ~/.openclaw/openclaw/skills/ollama-t2i/scripts/t2i.py "你的中文提示词"
```

### 单次生成

```bash
python3 ~/.openclaw/openclaw/skills/ollama-t2i/scripts/t2i.py "五名青年男子并排站立，着装休闲，多背双肩包..."
```

### 批量生成

编辑脚本内的 `prompts` 列表，或传多个参数：

```bash
python3 ~/.openclaw/openclaw/skills/ollama-t2i/scripts/t2i.py "提示词1" "提示词2"
```

## 输出

- 文件名格式：`YYYY-MM-DD_HH-MM_image_<随机数>.png`
- 保存路径：`images/`
- 包含请求耗时统计

## 代码位置

`scripts/t2i.py`
