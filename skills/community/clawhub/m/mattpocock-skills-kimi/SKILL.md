---
name: mattpocock-skills-kimi
description: >
  Matt Pocock 工程方法论 Kimi 适配版 — 一键安装 6 个生产级开发 skills：
  grilling（需求对齐）、grill-with-docs（代码库对齐+文档维护）、handoff（跨会话交接）、
  tdd（测试驱动开发）、diagnosing-bugs（六阶段 Bug 诊断）、to-prd（合成 PRD）。
  当用户需要对齐需求、设计确认、写测试、修 Bug、写 PRD、会话交接时触发。
  安装后需将 skills/ 子目录复制到 .agents/skills/ 或 skills/ 目录下。
version: 1.0.0
license: MIT
---

# Matt Pocock Skills — Kimi 适配版 (Meta-Skill)

> 原始理念来自 [Matt Pocock](https://github.com/mattpocock/skills)，
> 本仓库为 **Kimi Work / Kimi Claw (OpenClaw)** 生态进行本地化适配。
> 核心理念：small, easy to adapt, composable。

## 包含的 Skills

本 meta-skill 捆绑以下 6 个独立 skills，安装后请按下方指引启用：

| Skill | 功能 | 触发场景 |
|-------|------|---------|
| `grilling` |  relentlessly interview，对齐需求 | "对齐一下需求"、"帮我理清"、"讨论设计" |
| `grill-with-docs` | 代码库对齐 + 实时维护 CONTEXT.md + ADR | 有代码库时的 grilling 场景 |
| `handoff` | 跨会话交接，压缩上下文 | "会话太长了"、"handoff"、"上下文满了" |
| `tdd` | 测试驱动开发，红绿重构，垂直切片 | "写测试"、"TDD"、"先写测试"、"开发" |
| `diagnosing-bugs` | 六阶段 Bug 诊断 | "修 Bug"、"报错"、"debug"、"排查" |
| `to-prd` | 对话转 PRD + 发布到 Issue Tracker | "写 PRD"、"出需求文档"、"写成 spec" |

## 安装方式

### 方式 1：自动安装（推荐）

安装本 meta-skill 后，系统已包含所有子 skills 的 SKILL.md。
将其复制到 OpenClaw 的 skills 目录即可生效：

```bash
# 找到 skill 安装目录（ClawHub 安装后通常在此）
META_DIR="$HOME/.openclaw/skills/mattpocock-skills-kimi"

# 复制所有子 skills
for skill in grilling grill-with-docs handoff tdd diagnosing-bugs to-prd; do
  cp -r "$META_DIR/skills/$skill" "$HOME/.openclaw/workspace/.agents/skills/"
done
```

### 方式 2：从 GitHub 手动安装

```bash
git clone https://github.com/CoolingRabbit/mattpocock-skills-kimi.git
cp -r mattpocock-skills-kimi/skills/* ~/.openclaw/workspace/.agents/skills/
```

### 方式 3：逐个安装

使用 `clawhub install` 逐个安装子 skills（如果它们独立发布）。

## 使用建议

**典型工作流：**

1. **需求阶段**：`grilling` 或 `grill-with-docs` → 对齐需求，确认设计
2. **设计阶段**：`grill-with-docs` → 维护 CONTEXT.md 和 ADR
3. **文档阶段**：`to-prd` → 合成 PRD，发布到 Issue Tracker
4. **开发阶段**：`tdd` → 垂直切片，红绿重构
5. **调试阶段**：`diagnosing-bugs` → 六阶段诊断
6. **交接阶段**：`handoff` → 压缩上下文，跨会话接力

## License

MIT License — 原始版权归属 Matt Pocock。
ClawHub 分发版遵循平台 MIT-0 要求。
