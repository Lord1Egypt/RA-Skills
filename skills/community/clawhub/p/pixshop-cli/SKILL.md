---
name: pixshop-cli
description: Pixshop CLI 命令行工具 — AI 图片/视频生成、编辑工具、应用市场、提示词库 / Pixshop CLI — command-line AI image/video generation, editing tools, apps, prompts. Use when user wants to generate images, create videos, edit photos, browse AI apps, or search prompts from terminal.
allowed-tools: Bash, Read
---

# Pixshop CLI — 命令行 AI 创意工具 / Command-Line AI Creative Tools

> **[Pixshop (pixshop.app)](https://pixshop.app)** — AI 图片编辑 & 视频创意平台

通过命令行使用 Pixshop 的全部 AI 创意能力。支持图片生成（15+ 模型）、视频制作、图片编辑工具（7 种）、48+ AI 应用、提示词库搜索。适合自动化工作流和批量处理。

## Setup / 配置

```bash
# 安装
npm install -g pixshop

# 登录（浏览器 OAuth）
pixshop login

# 验证
pixshop whoami
pixshop credits
```

## 命令列表 (10 Commands)

### 1. `pixshop generate` — AI 图片生成

从文本提示词生成高质量图片，支持 15+ 模型。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--prompt, -p` | string | ✅ | 图片描述 |
| `--model, -m` | string | | 模型：nano-banana (默认), flux-2, seedream, higgsfield-soul, gpt-image-15, z-image, kling-o1-image, wan-22-image, reve, topaz, qwen-image, gemini-3.1-flash-image, seedream-4.5 等 |
| `--aspect-ratio` | string | | 比例：1:1, 16:9, 9:16, 4:3, 3:4 |
| `--ref-image` | path | | 参考图片文件路径 |
| `--count` | number | | 生成数量 1-4，默认 1 |
| `--app-id` | string | | 使用特定 Nano Banana App |
| `--output, -o` | path | | 保存路径 |

**示例**:
```bash
pixshop generate -p "sunset over mountains" -o sunset.png
pixshop generate -p "portrait in anime style" --model nano-banana --aspect-ratio 9:16
pixshop generate -p "enhance this" --ref-image photo.jpg -o enhanced.png
pixshop generate -p "cute cat" --count 4 -o cats/
```

### 2. `pixshop video` — AI 视频生成

从文本或图片生成视频。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--prompt, -p` | string | | 视频描述 |
| `--image, -i` | path | | 源图片（图生视频） |
| `--model, -m` | string | | 模型：seedance-1.5-pro, grok-imagine-video |
| `--resolution` | string | | 分辨率：720p, 1080p, 2k, 4k |
| `--aspect-ratio` | string | | 比例：16:9, 9:16 |
| `--output, -o` | path | | 保存路径 |

**示例**:
```bash
pixshop video -p "a cat walking gracefully" -o cat.mp4
pixshop video -i photo.jpg -p "add gentle motion" -o animated.mp4
```

### 3. `pixshop tools` — AI 图片/视频编辑工具

7 种专业 AI 编辑工具。

**子命令**:

| 工具 | 说明 | 示例 |
|------|------|------|
| `face-swap` | 人脸替换 | `pixshop tools face-swap -i face.jpg --image2 target.jpg` |
| `upscale` | 超分辨率放大 | `pixshop tools upscale -i photo.jpg -o photo-hd.jpg` |
| `try-on` | 虚拟试穿 | `pixshop tools try-on -i person.jpg -p "red dress"` |
| `aice-ps` | AI 修图 | `pixshop tools aice-ps -i photo.jpg -p "make brighter"` |
| `fashion` | 时尚大片 | `pixshop tools fashion -i model.jpg -p "editorial shoot"` |
| `makeup` | 化妆模拟 | `pixshop tools makeup -i face.jpg -p "smoky eyes"` |
| `motion` | 运动控制 | `pixshop tools motion -i photo.jpg -p "zoom in slowly"` |

**通用参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--image, -i` | path | ✅ | 输入图片 |
| `--image2` | path | | 第二张图片（face-swap 用） |
| `--prompt, -p` | string | | 编辑指令 |
| `--output, -o` | path | | 输出路径 |

### 4. `pixshop apps` — Nano Banana AI 应用市场

浏览和使用 48+ 预设 AI 应用。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--category` | string | | 分类筛选 |
| `--search` | string | | 搜索关键词 |
| `--list` | boolean | | 列出所有应用 |

**示例**:
```bash
pixshop apps --list
pixshop apps --category generation
pixshop apps --search "avatar"
```

### 5. `pixshop prompts` — 提示词库

浏览和搜索高质量提示词。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--search, -s` | string | | 搜索关键词 |
| `--tags` | string | | 标签筛选 |
| `--category` | string | | 分类筛选 |
| `--list` | boolean | | 列出提示词 |

**示例**:
```bash
pixshop prompts -s "sunset" --tags landscape
pixshop prompts --category portrait --list
```

### 6. `pixshop credits` — 积分查询

查看当前积分余额和使用记录。

```bash
pixshop credits
```

### 7. `pixshop discover` — AI 工具目录

查看所有可用 AI 工具的完整目录。

```bash
pixshop discover
```

### 8. `pixshop projects` — Agent 项目管理

管理 Design Agent 画布项目。

```bash
pixshop projects
```

### 9. `pixshop config` — CLI 配置

管理 CLI 配置（API URL、认证信息等）。

```bash
pixshop config
```

### 10. `pixshop login/logout/whoami` — 认证管理

```bash
pixshop login     # 浏览器 OAuth 登录
pixshop logout    # 清除凭据
pixshop whoami    # 显示当前用户
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `--help, -h` | 显示帮助 |
| `--version, -v` | 显示版本 |
| `--json` | JSON 格式输出（方便脚本解析） |
| `--api-url <url>` | 自定义 API 地址 |
| `--no-color` | 禁用彩色输出 |

## 典型工作流

### 批量图片生成
```bash
for style in "anime" "watercolor" "cyberpunk"; do
  pixshop generate -p "portrait of a girl, $style style" -o "girl-$style.png"
done
```

### 图片编辑流水线
`pixshop generate` → 生成图片 → `pixshop tools upscale` → 超分放大 → `pixshop tools aice-ps` → 精修

### 视频创作
`pixshop generate -p "epic landscape"` → `pixshop video -i landscape.png -p "cinematic zoom"` → 完成

### 提示词驱动创作
`pixshop prompts -s "cyberpunk"` → 找到提示词 → `pixshop generate -p "<prompt>" --model flux-2`

## 注意事项

- **需要登录**：所有 AI 操作需先 `pixshop login`
- **积分消耗**：图片生成 2-3 credits，视频 6-12 credits，工具 1-3 credits
- **输出格式**：使用 `--json` 获取结构化 JSON 输出，方便脚本解析
- **配置文件**：存储在 `~/.pixshop-config.json`
- **支持格式**：PNG, JPEG, WebP 输入，最大 20MB

## 在线体验

- [Pixshop 首页](https://pixshop.app) — AI 创意平台全景
- [Nano Banana Apps](https://pixshop.app/apps) — 48+ AI 应用市场
- [提示词库](https://pixshop.app/prompt-library) — 海量高质量提示词
- [特效展示](https://pixshop.app/effects) — 人像风格化 & 创意特效
- [Design Agent](https://pixshop.app/agent) — AI 设计工作台
- [CLI 文档](https://pixshop.app/docs/cli) — 完整命令行文档

---
Powered by [Pixshop](https://pixshop.app) — AI 图片编辑 & 视频创意平台
