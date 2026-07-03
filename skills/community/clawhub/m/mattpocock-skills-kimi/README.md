# Matt Pocock Skills — Kimi 适配版

> 基于 [Matt Pocock](https://github.com/mattpocock/skills) 的 `skills` 仓库，为 **Kimi Work** 和 **Kimi Claw (OpenClaw)** 环境进行本地化适配。
>
> 核心理念不变：small, easy to adapt, composable — 用经过验证的软件工程实践，让 AI 辅助编码更可靠、更可维护。

---

## 与原版的关系

| | 原版 (mattpocock/skills) | 本仓库 (mattpocock-skills-kimi) |
|---|---|---|
| 目标平台 | Claude Code / Claude Desktop | Kimi Work, Kimi Claw (OpenClaw) |
| 触发方式 | `/command` 手动命令 | Model-invoked 自动触发 |
| 工具调用 | `run` / `gh` CLI 等 | `Bash` / `PythonRun` / GitHub MCP / 通用指令 |
| Issue Tracker | `gh issue create` | 抽象层：GitHub MCP / Token / CLI / 本地 Markdown |
| 配置文件 | `CLAUDE.md` / `AGENTS.md` | `IDENTITY.md` + Vault Memory + 项目内 `CONTEXT.md` |

本仓库保留 Matt Pocock 的所有核心方法论和思维框架，仅对工具调用、路径、触发机制进行 Kimi 生态的本地化适配。

---

## 已适配 Skill 列表

按实施顺序排列，逐步上线：

| # | Skill | 状态 | 说明 |
|---|-------|------|------|
| 1 | `grilling` | ✅ 已完成 |  relentlessly interview，对齐需求的底层循环 |
| 2 | `handoff` | ✅ 已完成 | 跨会话交接，压缩上下文 |
| 3 | `domain-modeling` | ✅ 已完成 | 维护项目术语表 `CONTEXT.md` + ADR |
| 4 | `codebase-design` | ✅ 已完成 | 深模块设计词汇与原则 |
| 5 | `tdd` | ✅ 已完成 | 红绿重构，垂直切片 |
| 6 | `diagnosing-bugs` | ✅ 已完成 | 六阶段 Bug 诊断 |
| 7 | `grill-with-docs` | ✅ 已完成 | 有代码库时的对齐 + 文档维护 |
| 8 | `to-prd` | ✅ 已完成 | 合成 PRD + Issue Tracker 发布 |

---

## 快速开始（Kimi Work & Kimi Claw）

最简方式：通过自然语言告诉你的AI安装本仓库的Skill。https://github.com/CoolingRabbit/mattpocock-skills-kimi

**Kimi Work / Kimi Claw / OpenClaw**：
1. 在对话中告诉 Kimi Claw：
   > "帮我安装 https://github.com/CoolingRabbit/mattpocock-skills-kimi 的 skill"

AI 会自动读取仓库、安装 skill 到对应目录。安装完成后，skill 会在合适场景自动触发。

---

### 手动安装方式（备选）

如果 AI 安装失败，可使用以下手动方式：

**Kimi Work**
```bash
# 通过 SkillManage 工具逐个安装
# 或运行 Kimi 的 skill 安装命令
```

**OpenClaw（通用安装器）**
```bash
npx skills add CoolingRabbit/mattpocock-skills-kimi
```

**OpenClaw（手动克隆）**
```bash
git clone https://github.com/CoolingRabbit/mattpocock-skills-kimi.git ~/.openclaw/skills/mattpocock-skills-kimi
```

---

## 本地化修改说明

详见 [`docs/ADAPTATION-NOTES.md`](./docs/ADAPTATION-NOTES.md)。

---

## 致谢与许可

- 原作者：**Matt Pocock** — [github.com/mattpocock/skills](https://github.com/mattpocock/skills)
- 核心方法论、词汇、设计原则全部来自 Matt Pocock 的原创工作
- 本仓库仅做 Kimi 生态的本地化适配

Licensed under the **MIT License** — 保留 Matt Pocock 版权声明。
