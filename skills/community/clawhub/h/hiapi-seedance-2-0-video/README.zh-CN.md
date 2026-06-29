# Seedance 2.0 视频生成技能

把 Seedance 2.0 视频生成接入你的 AI Agent。

**Seedance 2.0 • 安装 • API Key • [HiAPI](https://www.hiapi.ai/zh)**

[免费获取 API Key](https://www.hiapi.ai/zh/register) · [查看价格](https://www.hiapi.ai/zh/pricing) · [HiAPI 文档](https://docs.hiapi.ai) · [全部 HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/zh/for-ai/)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? 跳过 README，直接看 [llms-install.md](llms-install.md)，里面有专为 Agent 准备的安装步骤和错误处理规则。

---

## 这是什么？

一个适用于 OpenClaw / Claude Code / OpenCode / Codex 类 Agent 的 AI 视频生成技能。安装后，你的 AI Agent 可以通过 HiAPI 使用 Seedance 2.0，根据文字生成视频，也可以让图片动起来。

HiAPI 是为开发者打造的 AI API 平台：一个 API，所有 AI 模型。图像、视频、音乐和文本，一个密钥全搞定。

| 技能 | 描述 | 模型 |
| --- | --- | --- |
| HiAPI Seedance 2.0 Video | 文生视频、图生视频 | Seedance 2.0 |

---

## 这个 skill 适合什么

当用户需要更完整的视频工作流时，尤其是文生视频和图生视频，用这个 skill。如果用户只需要快速轻量的文生视频草稿，转到 [hiapi-happyhorse-1-0-video-skill](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill)。如果用户给的简报只有一两句话，需要先得到一份分镜级提示词再生成，先用 [hiapi-video-prompt-generator-skill](https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill) 跑一遍。如果要先找一张静态图的创意起点，再做动画，查看 [awesome-gpt-image-2-prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts)。如果希望 Agent 发现更多 HiAPI 工具，查看 [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills)，或使用远程 MCP：`https://mcp.hiapi.ai/mcp`。

---

## 安装

### 一行命令（推荐）

```bash
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
```

安装脚本会自动检测 Codex（`~/.codex/skills`）和 Claude Code（`~/.claude/skills`）。如果两个都存在，`-y` 会同时装到两个目录。指定 Agent 或自定义目录：

```bash
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --codex          # 只装到 ~/.codex/skills
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --claude         # 只装到 ~/.claude/skills
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --target=/path   # 自定义目录
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
```

脚本会顺便检查 `HIAPI_API_KEY` 是否已设置，并给出获取地址。

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
```

### 手动安装（任意 Agent）

```bash
git clone https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-seedance-2-0-video-skill "$AGENT_SKILLS_DIR/hiapi-seedance-2-0-video"
```

将 `AGENT_SKILLS_DIR` 替换为你的 Agent 技能目录。

### Agent 自动安装（复制给你的 Agent）

```text
安装 HiAPI Seedance 2.0 视频生成技能：

1. 运行：npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
   （会自动检测 Codex / Claude Code 的 skills 目录）
2. 从 https://www.hiapi.ai/zh/dashboard/api-keys 获取并设置环境变量 HIAPI_API_KEY
3. 读取 SKILL.md 了解使用方法
```

---

## 获取 API Key

1. 打开 [免费获取 API Key](https://www.hiapi.ai/zh/register)
2. 登录或注册 HiAPI 账号
3. 创建新的 API Key
4. 在运行 Agent 的终端设置环境变量：

```bash
export HIAPI_API_KEY="your_hiapi_api_key_here"
export HIAPI_BASE_URL="https://api.hiapi.ai"
```

检查配置：

```bash
node scripts/check-config.mjs
```

联网检查：

```bash
node scripts/check-config.mjs --live
```

---

## Seedance 2.0 视频生成

通过自然语言让你的 AI Agent 生成视频。如果你提供图片，Seedance 2.0 可以把它作为首帧，让画面动起来。

### 功能

- 文生视频：描述场景、镜头运动、氛围和声音感，生成视频
- 图生视频：提供图片 URL 或 data URI，描述你希望图片如何动起来
- 视频时长：`4` 到 `15` 秒之间的整数
- 视频清晰度：`480p`、`720p`、`1080p`
- 画面比例：`16:9`、`9:16`、`1:1`、`4:3`、`3:4`、`21:9`、`adaptive`
- 媒体模式：文生视频、首帧图生视频、首尾帧图生视频、多模态参考生视频
- 默认带生成音频（API 默认开启）；不需要音频时传 `--no-audio`，强制开启传 `--generate-audio`
- 可复现输出：传 `--seed <0-2147483647>`
- 本地输出：可下载的视频会保存到 `outputs/`
- URL 输出：如果视频无法下载，Agent 会返回远程视频 URL
- 错误提示：未配置 Key、Key 无效、余额不足、图片不可访问、任务超时、任务失败都有明确下一步

### 使用示例

直接和你的 AI Agent 对话：

> 使用 `$hiapi-seedance-2-0-video` 生成一段 5 秒的电影感海边悬崖视频。

> 用 HiAPI Seedance 2.0 创建一段竖版产品宣传短片。

> 让这张产品图动起来，加入柔和镜头运动和棚拍灯光。

### 命令行脚本

文生视频：

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "A cinematic shot of ocean waves crashing against cliffs at golden hour" \
  --seconds 5 \
  --resolution 720p \
  --ratio 16:9
```

图生视频：

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "The product photo comes alive with soft camera movement and studio lighting" \
  --first-frame-url "https://example.com/product.jpg" \
  --seconds 5
```

首尾帧图生视频：

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "从首帧自然过渡到尾帧的产品英雄画面" \
  --first-frame-url "asset://first-frame" \
  --last-frame-url "asset://last-frame" \
  --seconds 5
```

生成音频：

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "咖啡馆里的温暖场景，带自然环境声" \
  --seconds 5 \
  --generate-audio
```

多模态参考生视频：

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "参考图片的主体、参考视频的运动方式和参考音频的氛围，生成一段产品广告" \
  --reference-image-url "asset://image-1" \
  --reference-video-url "asset://video-1" \
  --reference-video-duration 6 \
  --reference-audio-url "asset://audio-1" \
  --reference-audio-duration 5 \
  --seconds 5
```

媒体模式互斥：首帧图生视频、首尾帧图生视频、多模态参考生视频不可混用。需要严格保证首尾帧时，优先使用首尾帧模式；如果想在多模态参考里暗示首尾帧，可以在提示词中说明哪张参考图作为首帧或尾帧。

参考素材限制：

- `reference_image_urls` 与首帧、尾帧图片合计不超过 9 张。
- `reference_video_urls` 最多 3 个；单个 2-15 秒；总时长不超过 15 秒。
- `reference_audio_urls` 最多 3 段；单个 2-15 秒；总时长不超过 15 秒。

---

## 文件结构

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── api.md
│   └── output.md
├── scripts/
│   ├── check-config.mjs
│   ├── hiapi-seedance-2-video.mjs
│   └── lib/
│       └── seedance-2-video.mjs
├── tests/
│   └── seedance-2-video.test.mjs
└── llms-install.md
```

---

## 常见问题

| 问题 | 解决方案 |
| --- | --- |
| `HIAPI_API_KEY is required` | 去 [免费获取 API Key](https://www.hiapi.ai/zh/register) 创建 Key，然后设置 `HIAPI_API_KEY`。 |
| `401 Unauthorized` | 检查 API Key 是否正确，或重新生成 Key。 |
| `402 Payment Required` / `403` quota / 余额不足 | 进入 [HiAPI Dashboard](https://www.hiapi.ai/zh/dashboard) 检查账号状态。 |
| `400 Bad Request` | 检查时长、清晰度、画面比例、媒体模式、参考素材数量和参考音视频时长。 |
| `429 Too Many Requests` | 稍后重试，或减少并发生成请求。 |
| 任务超时 | 视频可能还在生成中，稍后重试，或生成更短的视频。 |
| 任务失败 | 换一个更清晰的提示词，或换一张图片。 |
| 没有视频输出 | 检查任务返回内容；该 skill 期望任务成功后返回视频 URL。 |
| 有可选更新 | CLI 启动时会检查 HiAPI skills 索引。如果只是建议升级，会打印升级命令并继续执行。 |
| 必须更新 | CLI 会停止并打印必须执行的升级命令。运行 `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y` 后重启 Agent。 |

只有在离线或内网环境无法访问 skills 索引时，才建议设置 `HIAPI_SKIP_UPDATE_CHECK=1` 跳过检查。

---

## 兼容性

| Agent | 安装方式 |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y` |
| Cursor / 其他 Agent | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --target=/your/skills/dir` |

---

## 许可证

MIT

---

[HiAPI](https://www.hiapi.ai/zh) — 一个 API，所有 AI 模型
