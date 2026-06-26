---
name: modelscope-image
description: 魔搭(ModelScope)AI 图片生成。支持多种模型、LoRA 微调。触发词：生成图片、AI绘画、文生图、image generation、generate image。当用户要求生成图片、画图、AI 作画，或提到魔搭、ModelScope、通义万象时使用。
---

# ModelScope 图片生成

调用魔搭(ModelScope) API 生成 AI 图片。

## 快速开始

```bash
# 设置 API Key（首次使用）
set MODELSCOPE_API_KEY=你的密钥

# 或保存到配置文件
py scripts/generate.py --save-key 你的密钥

# 生成图片
py scripts/generate.py -p "A golden cat"
py scripts/generate.py -p "一只在月光下奔跑的银狼" -o wolf.jpg
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 图片描述（必需） | - |
| `-m, --model` | 模型 ID | Tongyi-MAI/Z-Image-Turbo |
| `-o, --output` | 输出文件路径 | result_image.jpg |
| `-l, --lora` | 单个 LoRA repo-id | - |
| `--lora-weight` | 单个 LoRA 权重 | 1.0 |
| `--lora-json` | 多 LoRA JSON 配置 | - |
| `--api-key` | API Key | 从环境变量/配置文件读取 |

## LoRA 支持

**单个 LoRA:**
```bash
py scripts/generate.py -p "动漫少女" -l your-lora-id --lora-weight 0.8
```

**多个 LoRA（权重之和需为 1.0）:**
```bash
py scripts/generate.py -p "风景画" --lora-json "{\"lora-1\": 0.6, \"lora-2\": 0.4}"
```

## API Key 配置

三种方式（优先级从高到低）：

1. 命令行参数: `--api-key YOUR_KEY`
2. 环境变量: `set MODELSCOPE_API_KEY=YOUR_KEY`
3. 配置文件: `~/.modelscope/api_key`

获取 API Key: https://modelscope.cn/my/myaccesstoken

## 依赖

```bash
pip install requests pillow
```

## 常用模型

- `Tongyi-MAI/Z-Image-Turbo` - 快速生成（默认）
- 更多模型见 ModelScope 平台
