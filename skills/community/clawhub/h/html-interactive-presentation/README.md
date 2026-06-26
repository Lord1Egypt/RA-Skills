# HTML Interactive Presentation Skill

把 Markdown 文章变成可交互、可播放的 16:9 理解界面 HTML。

## 能力

- **多模态配图** — 调用 MiniMax CLI (`mmx image`) 生成技术蓝图风格配图
- **自动口播** — 提取章节文案，用 MiniMax TTS (`mmx speech synthesize`) 合成逐段 MP3
- **三种播放模式** — 手动翻页、带声翻页、自动播放
- **主题系统** — Blueprint / Paper Press / Monochrome 等多套视觉主题

## 工作流

1. 输入 Markdown 文章 → 产出 B 站风口播稿 + 开发计划
2. Checkpoint 确认：稿子 / outline / 主题 / 素材 / 模式
3. 脚手架 Vite + React + TS 项目 → 逐章实现
4. MiniMax CLI 生成配图 + 合成口播
5. `vite build` 产出可部署的静态页面

## 依赖

- Node.js 18+
- [web-video-presentation](https://github.com/ConardLi/garden-skills) skill（提供了脚手架和基础组件）

### 可选（多模态能力）

| 功能 | 推荐工具 | 可替代方案 |
|------|---------|-----------|
| 配图生成 | MiniMax CLI (`mmx image`) | OpenAI DALL-E / Stable Diffusion / 跳过用 placeholder |
| 口播合成 | MiniMax CLI (`mmx speech`) | OpenAI TTS / Edge TTS / Azure / ElevenLabs / 跳过 |
| 文本对话 | 由 AI 编程助手自身完成 | — |

没有 MiniMax API 时，配图可以用 placeholder 占位，口播可以改用 OpenAI TTS 或 Edge TTS（改一行脚本即可），不影响核心网页浏览体验。

## 兼容性

| Agent | 安装位置 | 状态 |
|-------|---------|------|
| **Claude Code** | `.claude/skills/` 或 ClawHub | ✅ |
| **OpenClaw** | `.opencode/skills/` 或 ClawHub | ✅ |
| **Hermes** | 支持 Skills 规范的目录 | ✅ |
| **Cursor** | `.agents/skills/` | ✅ |
| **Codex CLI** | `.codex/skills/` | ✅ |

> `SKILL.md` 格式是跨 Agent 可移植的 —— 任何支持 Skills 规范的 AI 编程助手都可以使用。

## 安装

```bash
# ClawHub（推荐）
clawhub install html-interactive-presentation

# 或手动克隆
git clone https://clawhub.ai/liangzhipengdamon-maker/html-interactive-presentation
```

## 用法

在你的 AI 编程助手中加载技能后，输入 Markdown 文章路径：

```
把 /path/to/article.md 做成交互式理解界面 HTML
```

AI 会按工作流推进：分析文章 → 产出稿子 → 确认计划 → 构建网页 → 合成配图口播 → 产出最终页面。
