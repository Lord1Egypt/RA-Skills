---
name: minimax-image-gen
displayName: AI Text-to-Image Tool · MiniMax image-01
description: "MiniMax image-01 文生图工具。支持中文指令（画一张、生成图片、帮我画）和英文指令（generate an image、draw）。双端支持（中国区/国际区）。Token Plan 每日免费额度：Plus 50张/天、Max 120张/天、Ultra 800张/天。模型：image-01，输出 PNG。"
allowList:
  - env: MINIMAX_API_KEY   # MiniMax API key for image generation
---
---

# MiniMax image-01 文生图工具

MiniMax image-01 文本生成图像工具。使用 MiniMax 的 image-01 模型从文字描述生成图片。

---

## 安装依赖

```bash
pip install requests
```

---

## 环境变量

```bash
# macOS / Linux
export MINIMAX_API_KEY=your_key

# Windows (PowerShell)
$env:MINIMAX_API_KEY="your_key"
```

**获取 API Key：**
- 中国区：https://platform.minimaxi.com/user-center/basic-information/interface-key
- 国际区：https://www.minimax.io/platform/user-center/basic-information/interface-key

---

## 区域选择

| 区域 | API 地址 | 适用用户 |
|------|---------|---------|
| **中国区** | `https://api.minimax.chat/v1/image_generation` | 中国用户 / MiniMax 中国站 |
| **国际区** | `https://api.minimax.io/v1/image_generation` | 海外用户 |

---

## 快速使用

```bash
# 中国用户
python scripts/image_gen.py "你的图片描述" --region cn

# 国际用户
python scripts/image_gen.py "your prompt" --region global
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述（必填） | — |
| `--region` | 区域：`cn` 或 `global`（必填） | — |
| `--aspect` | 比例：16:9、1:1、4:3、9:16、21:9 | 16:9 |
| `--n` | 生成数量（1-9） | 1 |
| `--no-enhance` | 关闭 Prompt 增强 | 开启 |
| `--output` | 输出目录 | 当前目录 |

---

## 比例参考

| 比例 | 最佳用途 |
|------|---------|
| 16:9 | 横版 / 视频封面 |
| 1:1 | 社交媒体 / 卡片 |
| 9:16 | 手机竖版 / Stories |
| 4:3 | 博客 / 文档 |

---

## Prompt 增强（默认开启）

对于短描述（<8词），自动补充专业摄影/艺术参数：

- 光影：soft natural lighting、cinematic lighting、volumetric light
- 画质：4K、sharp focus、highly detailed
- 风格：photorealistic、detailed linework、professional quality

示例：
- "一只猫" → 自动补充 soft lighting、sharp focus、4K
- "赛博朋克城市" → 自动补充 neon lighting、Blade Runner atmosphere、cinematic

关闭增强：`python image_gen.py "简单描述" --region cn --no-enhance`

---

## 输出

图片保存为 `minimax_gen_1.png`、`minimax_gen_2.png` 等。

---

## 每日额度（Token Plan）

| 套餐 | 每日图片额度 |
|------|-------------|
| Starter | 0（不包含图像生成） |
| **Plus** | **50 张/天** |
| Max | 120 张/天 |
| Ultra | 800 张/天 |

额度每日零点重置，直接消耗 Token Plan 套餐额度，无需额外付费。

---

**作者：** Mzusama
**模型：** MiniMax image-01
