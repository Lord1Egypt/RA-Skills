---
name: ms-ai
version: 1.1.1
description: |
  ModelScope AI 技能：生图、改图、析图、生文。支持文生图、图生图、视觉理解、文本生成，遇到限速自动轮换模型。
author: 小老弟
category: ai-generation
tags:
  - ai
  - image-generation
  - vision
  - text-generation
  - modelscope
---

# MS-ai — ModelScope AI 技能

通过 ModelScope API 进行文生图、图生图、视觉理解和文本生成，遇到 429 限速自动轮换模型。

## 前置条件

### 1. 安装依赖

```bash
pip install requests Pillow
```

### 2. 配置 API Key

编辑 `~/.openclaw/openclaw.json`，在 `skills.entries` 下添加：

```json
{
  "skills": {
    "entries": {
      "ms-ai": {
        "enabled": true,
        "env": {
          "MODELSCOPE_API_KEY": "ms-key1,ms-key2,ms-key3"
        }
      }
    }
  }
}
```

> 多个 Key 用逗号 `,` 分隔。当一个 Key 的所有模型都失败时，自动切换到下一个 Key 重试全部模型。

> 💡 也可以使用环境变量 `export MODELSCOPE_API_KEY=key1,key2`，但推荐用 Skill 级别配置，更整洁且仅对该 Skill 生效。

> ⚠️ 本技能调用 ModelScope API 会消耗额度。如果用户没有明确说"使用ms-ai"，必须先告知并确认后再执行。

## 功能概览

| 功能 | 脚本 | 说明 |
|------|------|------|
| 文生图 | `generate.py` | 文字描述 → 图片 |
| 图生图 | `generate.py --image` | 上传图片 + 描述 → 修改后的图片 |
| 视觉理解 | `vision.py` | 分析图片内容、OCR、场景识别 |
| 文本生成 | `text.py` | 多模型对话/文本生成 |

## 图片生成 (generate.py)

```bash
# 文生图（默认 1920x1080 横屏）
python3 <skill_dir>/scripts/generate.py --prompt "一只金色的猫" --output cat.jpg

# ⭐ 推荐：用 --aspect 指定场景（agent 首选方式）
python3 <skill_dir>/scripts/generate.py --prompt "PPT封面" --aspect ppt --output slide.png
python3 <skill_dir>/scripts/generate.py --prompt "抖音短视频" --aspect douyin --output video.png
python3 <skill_dir>/scripts/generate.py --prompt "竖版海报" --aspect poster --output poster.png

# 也可以直接传宽高比
python3 <skill_dir>/scripts/generate.py --prompt "风景画" --aspect 16:9 --output landscape.jpg

# 图生图
python3 <skill_dir>/scripts/generate.py --prompt "给狗戴上生日帽" --image dog.png --output result.jpg

# 精确指定像素尺寸（最高优先级）
python3 <skill_dir>/scripts/generate.py --prompt "自定义" --width 2560 --height 1440 --output custom.jpg
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 描述文字（必填） | — |
| `--output` | 输出文件路径 | `output.jpg` |
| `--model` | 指定模型（别名或完整ID） | 自动轮换 |
| `--image` | 输入图片（图生图，可多次指定） | — |
| `--aspect` | **宽高比预设或场景名（推荐）** | — |
| `--width` | 图片宽度 | 1920 |
| `--height` | 图片高度 | 1080 |
| `--lora` | LoRA 模型 ID | — |

> 📐 **优先级**：`--aspect` > `--width/--height` > 默认 1920×1080

### 🎯 场景→尺寸速查表（Agent 必读！）

**生图前必须根据使用场景选择正确的 `--aspect` 参数：**

| 场景 | `--aspect` 值 | 尺寸 | 说明 |
|------|--------------|------|------|
| **PPT / 幻灯片** | `ppt` 或 `16:9` | 1920×1080 | 横屏演示 |
| **横屏视频** | `video-h` 或 `16:9` | 1920×1080 | YouTube、B站 |
| **竖屏短视频** | `video-v` / `douyin` / `9:16` | 1080×1920 | 抖音、快手、Reels |
| **文章/视频封面** | `cover` 或 `16:9` | 1920×1080 | 公众号、头条 |
| **微信公众号** | `weixin` 或 `16:9` | 1920×1080 | 图文封面 |
| **竖版海报** | `poster` 或 `2:3` | 1200×1800 | 活动海报、宣传 |
| **社交媒体** | `social` 或 `1:1` | 1024×1024 | 微博、朋友圈 |
| **头像** | `avatar` 或 `1:1` | 1024×1024 | 个人头像 |
| **电影画幅** | `cinema` 或 `21:9` | 2560×1080 | 超宽屏 |
| **摄影/印刷** | `photo` 或 `3:2` | 1800×1200 | 标准摄影 |
| **A4 文档** | `print-a4` 或 `3:4` | 1152×1536 | 竖版文档 |
| **iPad 横屏** | `4:3` | 1536×1152 | 传统比例 |

> ⚠️ **Agent 调用规则**：每次生图前，先判断使用场景，再传 `--aspect`。不确定时默认 16:9（横屏）。

## 视觉理解 (vision.py)

```bash
python3 <skill_dir>/scripts/vision.py --image photo.jpg --prompt "描述这张图片"
python3 <skill_dir>/scripts/vision.py --image screenshot.png --prompt "图片里有什么文字？"
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 分析提示词（必填） | — |
| `--image` | 输入图片路径 | — |
| `--model` | 指定模型 | 自动轮换 |
| `--stdin-b64` | 从 stdin 读取 base64 图片 | — |

> `--image` 和 `--stdin-b64` 二选一。涉及视觉理解任务时优先使用此脚本。

## 文本生成 (text.py)

```bash
python3 <skill_dir>/scripts/text.py --prompt "解释量子计算"
python3 <skill_dir>/scripts/text.py --prompt "写一首诗" --stream
python3 <skill_dir>/scripts/text.py --prompt "继续" --history history.json --output history.json
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 用户输入（必填） | — |
| `--model` | 指定模型 | 自动轮换 |
| `--max-tokens` | 最大输出 token 数 | 4096 |
| `--temperature` | 温度（0-2） | 0.7 |
| `--stream` | 流式输出 | 关闭 |
| `--history` | 历史消息 JSON 文件 | — |

## 模型配置

### 文生图模型

| 优先级 | 模型 ID | 别名 |
|--------|---------|------|
| 1 | `FireRedTeam/FireRed-Image-Edit-1.1` | `firered` |
| 2 | `Qwen/Qwen-Image-2512` | `qwen` |
| 3 | `Qwen/Qwen-Image-Edit-2511` | `edit` |
| 4 | `Tongyi-MAI/Z-Image-Turbo` | `turbo` |

### 视觉理解 / 文本生成模型

| 优先级 | 模型 ID | 别名 |
|--------|---------|------|
| 1 | `moonshotai/Kimi-K2.5` | `kimi` |
| 2 | `ZhipuAI/GLM-5` | `glm` |
| 3 | `MiniMax/MiniMax-M2.5` | `minimax` |
| 4 | `Qwen/Qwen3.5-397B-A17B` | `qwen` |
| 5 | `XiaomiMiMo/MiMo-V2-Flash`（仅text） | `mimo` |

### 轮换机制（Key × 模型双重轮换）

策略：**先换 Key，每个 Key 试完所有模型，再换下一个 Key**

1. 使用 Key1，按优先级依次尝试所有模型
2. Key1 的所有模型都失败 → 切换到 Key2，重新尝试所有模型
3. 所有 Key × 所有模型都失败 → 报错退出

总共最多尝试 `n_keys × n_models` 次。遇到 429 限速等待 10 秒后换下一个模型。

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `未设置 MODELSCOPE_API_KEY` | 未配置 API Key | 在 `skills.entries.ms-ai.env` 中配置 |
| `429 Too Many Requests` | 频率限制 | 脚本自动轮换，等待重试 |
| `所有模型都失败` | 额度用尽或全部限速 | 等待后重试 |
| `ImportError: requests` | 缺少依赖 | `pip install requests Pillow` |

## 更新日志

### v1.2.0 (2026-03-26)
- **`--aspect` 预设参数**：支持宽高比（16:9, 9:16 等）和场景名（ppt, douyin, poster 等）
- **默认尺寸**：从 1024×1024 改为 1920×1080（16:9 横屏，覆盖 PPT/视频/封面等主流场景）
- **场景速查表**：SKILL.md 新增 场景→尺寸 对照表，agent 一眼选对
- 支持 8 种宽高比 + 13 个场景别名

### v1.1.0 (2026-03-24)
- **Key 轮换**：支持多个 API Key（逗号分隔），所有模型失败后自动切换下一个 Key
- 新增 `common.py` 共享模块，统一 Key + 模型双重轮换逻辑
- 轮换策略：先换 Key → 每个 Key 试完所有模型 → 再换下一个 Key

### v1.0.2 (2026-03-24)
- 配置方式统一为 Skill 级别 env（openclaw.json skills.entries）
- 文档结构优化

### v1.0.1 (2026-03-24)
- 移除 openclaw.json tools 自定义键配置

### v1.0.0 (2026-03-24)
- 首次发布：文生图、图生图、视觉理解、文本生成
- 模型自动轮换（429 限速处理）
