# HappyHorse 1.0 视频生成技能

把 HappyHorse 1.0 文生视频接入你的 AI Agent。

**HappyHorse 1.0 • 安装 • API Key • [HiAPI](https://www.hiapi.ai/zh)**

[免费获取 API Key](https://www.hiapi.ai/zh/register) · [查看价格](https://www.hiapi.ai/zh/pricing) · [HiAPI 文档](https://docs.hiapi.ai) · [全部 HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/zh/for-ai/)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? 跳过 README，直接看 [llms-install.md](llms-install.md)，里面有专为 Agent 准备的安装步骤和错误处理规则。

---

## 这是什么？

一个适用于 OpenClaw / Claude Code / OpenCode / Codex 类 Agent 的 AI 视频生成技能。安装后，你的 AI Agent 可以通过 HiAPI 使用 HappyHorse 1.0，根据文字提示词生成视频。

HiAPI 是为开发者打造的 AI API 平台：一个 API，所有 AI 模型。图像、视频、音乐和文本，一个密钥全搞定。

| 技能 | 描述 | 模型 |
| --- | --- | --- |
| HiAPI HappyHorse 1.0 Video | 文生视频 | HappyHorse 1.0 |

---

## 这个 skill 适合什么

当用户需要快速、明确的单模型文生视频工作流时，用这个 skill。如果用户需要更强的图生视频控制，转到 [hiapi-seedance-2-0-video-skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill)。如果用户给的简报只有一两句话，需要先得到一份分镜级提示词再生成，先用 [hiapi-video-prompt-generator-skill](https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill) 跑一遍。如果希望 Agent 在聊天里发现更多 HiAPI 工具，查看 [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills)，或使用远程 MCP：`https://mcp.hiapi.ai/mcp`。

---

## 安装

### 一行命令（推荐）

```bash
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
```

安装脚本会自动检测 Codex（`~/.codex/skills`）和 Claude Code（`~/.claude/skills`）。如果两个都存在，`-y` 会同时装到两个目录。指定 Agent 或自定义目录：

```bash
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --codex          # 只装到 ~/.codex/skills
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --claude         # 只装到 ~/.claude/skills
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --target=/path   # 自定义目录
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
```

脚本会顺便检查 `HIAPI_API_KEY` 是否已设置，并给出获取地址。

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
```

### 手动安装（任意 Agent）

```bash
git clone https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-happyhorse-1-0-video-skill "$AGENT_SKILLS_DIR/hiapi-happyhorse-1-0-video"
```

将 `AGENT_SKILLS_DIR` 替换为你的 Agent 技能目录。

### Agent 自动安装（复制给你的 Agent）

```text
安装 HiAPI HappyHorse 1.0 视频生成技能：

1. 运行：npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
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

## HappyHorse 1.0 视频生成

通过自然语言让你的 AI Agent 生成视频。HappyHorse 1.0 可以把一句提示词变成高清视频，适合短视频、广告分镜、社媒内容和电影感概念片段。

### 功能

- 文生视频：描述场景、主体、镜头运动、风格和声音氛围，生成视频
- 视频时长：`3` 到 `15` 秒之间的整数
- 视频清晰度：`720p`、`1080p`
- 画面尺寸：`16:9`、`9:16`、`1:1`、`4:3`、`3:4`
- 可选 seed：`0` 到 `2147483647` 之间的整数，用于尽量复现同参数结果
- 本地输出：可下载的视频会保存到 `outputs/`
- URL 输出：如果视频无法下载，Agent 会返回远程视频 URL
- 错误提示：未配置 Key、Key 无效、余额不足、参数错误、任务超时、任务失败都有明确下一步

### 使用示例

直接和你的 AI Agent 对话：

> 使用 `$hiapi-happyhorse-1-0-video` 生成一段 5 秒 1080p 的武侠屋顶飞跃视频。

> 用 HiAPI HappyHorse 1.0 创建一段竖版产品宣传短片。

> 生成一段电影感广告分镜，动作真实，并带自然声音氛围。

### 命令行脚本

```bash
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "一位武侠女剑客在黄昏时分纵身跃过寺庙屋脊，丝绸长袍随风飘动" \
  --seconds 5 \
  --resolution 1080p \
  --size 16:9 \
  --seed 12345
```

---

## 文件结构

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── social-preview.jpg
│   └── social-preview.svg
├── references/
│   ├── api.md
│   └── output.md
├── scripts/
│   ├── check-config.mjs
│   ├── hiapi-happyhorse-1-video.mjs
│   └── lib/
│       └── happyhorse-1-video.mjs
├── tests/
│   └── happyhorse-1-video.test.mjs
└── llms-install.md
```

---

## 常见问题

| 问题 | 解决方案 |
| --- | --- |
| `HIAPI_API_KEY is required` | 去 [免费获取 API Key](https://www.hiapi.ai/zh/register) 创建 Key，然后设置 `HIAPI_API_KEY`。 |
| `401 Unauthorized` | 检查 API Key 是否正确，或重新生成 Key。 |
| `402 Payment Required` / `403` quota / 余额不足 | 进入 [HiAPI Dashboard](https://www.hiapi.ai/zh/dashboard) 检查账号状态。 |
| `400 Bad Request` | 检查视频时长、清晰度、画面尺寸和 seed。 |
| `429 Too Many Requests` | 稍后重试，或减少并发生成请求。 |
| 任务超时 | 视频可能还在生成中，稍后重试，或生成更短的视频。 |
| 任务失败 | 换一个更清晰的提示词。 |
| 没有视频输出 | 检查任务返回内容；该 skill 期望任务成功后返回视频 URL。 |
| 有可选更新 | CLI 启动时会检查 HiAPI skills 索引。如果只是建议升级，会打印升级命令并继续执行。 |
| 必须更新 | CLI 会停止并打印必须执行的升级命令。运行 `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y` 后重启 Agent。 |

只有在离线或内网环境无法访问 skills 索引时，才建议设置 `HIAPI_SKIP_UPDATE_CHECK=1` 跳过检查。

---

## 兼容性

| Agent | 安装方式 |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y` |
| Cursor / 其他 Agent | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --target=/your/skills/dir` |

---

## 展示图

仓库包含 [assets/social-preview.jpg](assets/social-preview.jpg)，源文件是 [assets/social-preview.svg](assets/social-preview.svg)。把 JPG 设置为 GitHub 仓库的 Social preview 图片后，在 X / Twitter 分享 GitHub 链接时会显示这张 HappyHorse 1.0 中文推广图。

---

## 许可证

MIT

---

[HiAPI](https://www.hiapi.ai/zh) — 一个 API，所有 AI 模型
