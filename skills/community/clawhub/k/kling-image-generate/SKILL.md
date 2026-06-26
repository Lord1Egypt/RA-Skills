---
name: kling-image-generate
description: 可灵AI图像生成API工具。支持文生图、图生图、多图参考生成、图像Omni、扩图等功能。使用环境变量KLING_ACCESS_KEY和KLING_SECRET_KEY进行鉴权。当用户需要生成AI图像、图片编辑、图像扩展等任务时使用此技能。
---

# 可灵图像生成

> **🇨🇳 中文** | [🇬🇧 English](SKILL.en.md)

可灵AI图像生成服务，提供文生图、图生图、扩图等多种图像生成和编辑能力。

> 🔒 **安全说明**: 本技能需要调用可灵AI官方 API (`api-beijing.klingai.com`)，并使用用户提供的 API Key 进行 JWT 鉴权。所有凭证仅存储在本地环境变量中，不会上传或共享。

## 快速开始

### 1. 配置环境变量

```bash
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

### 2. 运行脚本

```bash
# 文生图（推荐带进度版本）
python3 scripts/generate_image_with_progress.py \
  --prompt "一只可爱的猫咪，皮克斯风格" \
  --model kling-v3 \
  --n 2 \
  --aspect_ratio 1:1 \
  --wait

# 图生图
python3 scripts/generate_image_with_progress.py \
  --prompt "保持原图风格，添加花朵装饰" \
  --image "https://example.com/image.png" \
  --image_reference subject \
  --wait
```

## 脚本清单

| 脚本 | 用途 | 推荐度 |
|------|------|--------|
| `generate_image_with_progress.py` | 图像生成（带进度显示） | ⭐ 推荐 |
| `generate_image.py` | 图像生成（基础版） | 可选 |
| `generate_omni_image.py` | Omni多图生成 | 按需 |
| `expand_image.py` | 图像扩图 | 按需 |
| `query_task.py` | 查询任务状态 | 工具 |
| `list_tasks.py` | 获取任务列表 | 工具 |

## 核心功能使用

### 文生图

```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "描述你想要的图像内容" \
  --model kling-v3 \
  --n 1 \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait
```

**常用参数：**
- `--model`: 模型（kling-v3, kling-v2-1, kling-v1-5 等）
- `--n`: 生成数量 1-9
- `--aspect_ratio`: 1:1, 16:9, 9:16, 4:3 等
- `--resolution`: 1k, 2k
- `--wait`: 等待任务完成并显示进度

### 图生图

```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "基于参考图的描述" \
  --image "https://example.com/ref.jpg" \
  --image_reference subject \
  --image_fidelity 0.7 \
  --wait
```

**参考类型：**
- `subject`: 主体参考（保持人物/物体主体）
- `face`: 面部参考（保持面部特征）

### Omni多图生成

支持多图参考、风格迁移等高级功能：

```bash
python3 scripts/generate_omni_image.py \
  --prompt "将<<<image_1>>>的风格应用到<<<image_2>>>上" \
  --images "url1,url2" \
  --model kling-v3-omni \
  --resolution 2k \
  --wait
```

### 扩图

智能扩展图像边界：

```bash
# 手动指定扩展比例
python3 scripts/expand_image.py \
  --image "https://example.com/img.jpg" \
  --up 0.5 --down 0.5 --left 0.5 --right 0.5 \
  --prompt "扩展区域的描述" \
  --wait

# 自动计算比例
python3 scripts/expand_image.py \
  --image "https://example.com/img.jpg" \
  --auto_ratio \
  --width 1024 --height 1024 \
  --aspect_ratio 16:9 \
  --wait
```

## 任务管理

### 查询任务状态

```bash
python3 scripts/query_task.py --task_id "xxx"
```

### 获取任务列表

```bash
python3 scripts/list_tasks.py --api_type generation --page 1
```

## 详细参考

- **完整 API 参数**: 参见 [references/api-reference.md](references/api-reference.md)
- **English Version**: [SKILL.en.md](SKILL.en.md)
