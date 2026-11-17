# 视频提示词生成器技能

把简短的视频创意、链接或调研主题，转成结构化、有来源支撑、可直接喂给 HiAPI Seedance 2.0 或 HappyHorse 1.0 的视频提示词。

**视频提示词生成器 • HiAPI 交付 • [HiAPI](https://www.hiapi.ai/zh)**

> 这个 skill 自身不需要 API Key。只有最终出片所用的渲染 skill（[Seedance 2.0](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill) 或 [HappyHorse 1.0](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill)）才需要 `HIAPI_API_KEY`。

[HiAPI 文档](https://docs.hiapi.ai) · [全部 HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/zh/for-ai/) · [查看价格](https://www.hiapi.ai/zh/pricing) · [免费获取 API Key](https://www.hiapi.ai/zh/register)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [图片提示词库](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [视频提示词库](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills（当前）** · 🤖 [Remote MCP](https://docs.hiapi.ai/zh/for-ai/) · 📖 [API 文档](https://docs.hiapi.ai)

---

> AI Agent？直接看 [llms-install.md](llms-install.md)，里面有专为 Agent 准备的安装步骤和契约。

---

## 这是什么？

一个适用于 OpenClaw / Claude Code / OpenCode / Codex 类 Agent 的"提示词生成器"技能。安装后，你只要把一句话的视频想法、一个产品链接，或者一个调研主题丢给 Agent，生成器就会反馈一份**有镜头调度的视频提示词**，可以直接粘贴到 HiAPI 的视频 skill。

这个 skill 本身不生成视频，它产出提示词。最终用以下哪个 skill 真正出片：

| 目标 skill | 适合什么 |
| --- | --- |
| [hiapi-seedance-2-0-video-skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill) | 文生视频、图生视频，电影感，4–15 秒 |
| [hiapi-happyhorse-1-0-video-skill](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill) | 快速文生视频草稿 |

"有调度的提示词"会把每一条关键事实、每一行屏幕文字、每一个动作和镜头运动写清楚，并显式列出**模型不应该生成的内容**。

---

## 适合什么场景

适合简报太短、用户没读源资料、提示词太笼统的情况。如果用户已经有按分镜写好的最终提示词，直接调用视频 skill 即可，无需走这一步。

如果想参考一批已经验证过的 Seedance 2.0 提示词，请看 [awesome-seedance-2-0-prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts)。

---

## 安装

### 一行命令（推荐）

```bash
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
```

安装脚本会自动检测 Codex（`~/.codex/skills`）和 Claude Code（`~/.claude/skills`）。指定 Agent 或自定义目录：

```bash
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --codex          # 只装到 ~/.codex/skills
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --claude         # 只装到 ~/.claude/skills
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --target=/path   # 自定义目录
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
```

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill
```

### 手动安装（任意 Agent）

```bash
git clone https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-video-prompt-generator "$AGENT_SKILLS_DIR/hiapi-video-prompt-generator"
```

### Agent 自动安装提示

```text
安装 HiAPI 视频提示词生成器技能：

1. 运行：npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
   （会自动检测 Codex / Claude Code 的 skills 目录）
2. 读取 SKILL.md 了解输出契约。
3. 拿到提示词后，传给以下任一 skill 出片：
   - https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
   - https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
```

---

## 使用示例

直接和你的 Agent 对话：

> 使用 `$hiapi-video-prompt-generator`，把 https://github.com/HiAPIAI/hiapi-skills 做成一段 5 秒的产品介绍。

> 用 HiAPI 视频提示词生成器，规划一段 9:16 的社交短视频，主题是"Agent skill 为什么比一次性 prompt 强"。

> `$hiapi-video-prompt-generator`：基于 `outputs/product.png`，规划 8 秒图生视频，柔和镜头、棚拍灯光。

生成器会返回一份分镜级提示词，并附上目标 HiAPI skill 的可直接复制命令。

---

## 输出契约

每次生成器都按这个结构返回：

1. **视频类型** — 产品演示、知识短片、社交短片、解说、Pitch、历史/市场、视觉概念。
2. **目标模型** — `hiapi-seedance-2-0-video` 或 `hiapi-happyhorse-1-0-video`，附一句原因。
3. **时长与画幅** — 根据所选目标的合法集合：Seedance 是 `4` 到 `15` 秒之间的任意整数 + `--ratio` ∈ `16:9|9:16|1:1|4:3|3:4|21:9|adaptive`；HappyHorse 是 `3` 到 `15` 秒之间的任意整数 + `--size` ∈ `16:9|9:16|1:1|4:3|3:4`。在这一段里写清楚用哪个 flag。
4. **核心目标** — 一句话：观众看完应该记得什么。
5. **资料提取摘要** — 5–10 条要点：来自来源的事实点标 `[source]`，仅"创意化的镜头/布光/转场"等舞台化选择可标 `[creative assumption]`；不要把猜测当作来源。
6. **叙事主线** — 一句话故事弧。
7. **分镜提示词** — 每个分镜含时间、画面、屏幕文字、动作/镜头、旁白、转场。
8. **关键屏幕文字** — 所有需要在画面里出现的精确文字（带引号）。
9. **动效与镜头控制** — 主导动作 + 辅助环境动作。
10. **风格要求** — 颜色、光线、字体、氛围。
11. **禁止项** — 模型不应该生成的内容。
12. **最终可复制提示词** — 一段可直接粘到 `--prompt` 的内容，**必须**保留分镜顺序、时间标记（如 `[0–1.2s]`）、所有屏幕文字原文、主导镜头动作以及至少一条禁止项。若被压成纯描述就算不合格。
13. **交付命令** — 一行 `cd` 进入目标 skill 的安装目录，再跟一行 `node scripts/...`：Seedance 用 `--ratio`，HappyHorse 用 `--size`，所有参数都填好。

详细契约见 [`SKILL.md`](SKILL.md)，分镜模式与资料提取见 [`references/`](references/)。

---

## 生成器会强制的默认值

- **时长**：默认 `5` 秒；不会出现 `30` 秒方案，HiAPI 的视频模型不支持那个长度。
- **画幅**：横向演示 `16:9`，社交短视频 `9:16`。
- **图生视频**：只走 Seedance 2.0，起始图通过 `--first-frame-url` 传入（URL、data URI 或素材 ID）；HappyHorse 1.0 不接受图片输入。
- **模型参数严格分开**：

| 模型 | 时长 (`--seconds`) | 清晰度 | 画幅 flag |
| --- | --- | --- | --- |
| Seedance 2.0 | `4` 到 `15` 秒之间的任意整数 | `480p`, `720p`, `1080p` | `--ratio` ∈ `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `adaptive` |
| HappyHorse 1.0 | `3` 到 `15` 秒之间的任意整数 | `720p`, `1080p` | `--size` ∈ `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |

如果用户提了不支持的时长或画幅，生成器会给出最接近的合法值，并在输出里注明改动。

### 为什么默认 5 秒（而不是上游的 30 秒）

参考项目 `video-prompt-director` 默认 30 秒，是为了配合 HyperFrames 那种多镜头脚本。HiAPI 的视频模型最长单段到 15 秒，默认 5 秒可以让生成器的产出**直接喂进** Seedance 2.0 或 HappyHorse 1.0 的 `--seconds`，省去用户压缩脚本的步骤。需要更长时，在目标模型允许范围内最高可到 `15` 秒。

---

## 文件结构

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── LICENSE
├── package.json
├── agents/
│   └── openai.yaml
├── references/
│   ├── prompt-patterns.md
│   ├── source-extraction.md
│   └── hiapi-handoff.md
├── scripts/
│   └── install.mjs
└── llms-install.md
```

---

## 常见问题

| 问题 | 解答 |
| --- | --- |
| 这个 skill 会直接调 HiAPI 视频接口吗？ | 不会。它产出提示词，配合 HiAPI 的视频 skill 出片。 |
| 用这个 skill 需要 `HIAPI_API_KEY` 吗？ | 不需要。Key 只在最后那一步、调用渲染 skill 时才用得到。 |
| 为什么默认 5 秒而不是 30 秒？ | HiAPI 的视频模型不出 30 秒。Seedance 支持 4 到 15 秒之间的整数；HappyHorse 是 3/5/8/10/15。 |
| 它会自动选目标模型吗？ | 会。没指定时，图生视频和电影感画面默认走 Seedance 2.0；纯文生视频快草稿走 HappyHorse 1.0。 |
| 简报里事实不够怎么办？ | 生成器只会把"镜头/布光/转场"这类**舞台化选择**标成 `[creative assumption]`。缺失的产品事实是直接抛回来问你，而不是编一个。 |
| 我给了 URL 会怎么处理？ | 先按 `references/source-extraction.md` 提取事实，再写提示词。 |

---

## 兼容性

| Agent | 安装方式 |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y` |
| Cursor / 其他 Agent | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --target=/your/skills/dir` |

---

## 许可证

MIT

---

[HiAPI](https://www.hiapi.ai/zh) — 一个 API，所有 AI 模型
