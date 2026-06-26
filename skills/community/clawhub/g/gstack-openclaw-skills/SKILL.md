---
name: gstack-openclaw-skills
description: gstack 的 WorkBuddy/OpenClaw 适配版本。源自 gstack (Y Combinator Garry Tan)，专为 WorkBuddy/OpenClaw 等 AI 助手平台优化。包含 15 个专业工具，涵盖从产品构思到代码发布的完整开发流程。
version: 1.0.0
author: gstack-openclaw-skills Team
tags: [development, workflow, AI, productivity, gstack]
---

# gstack-openclaw-skills - gstack 的 WorkBuddy 适配版

> 源自 gstack (Y Combinator CEO Garry Tan)，适配 WorkBuddy/OpenClaw

## 简介

gstack-openclaw-skills 是 gstack 的开源 WorkBuddy/OpenClaw 适配版本。gstack 是 Y Combinator 总裁兼 CEO Garry Tan 开源的 Claude Code 设置，包含 15 个专业工具。

Garry Tan 声称在 60 天内使用 gstack 编写了**超过 60 万行生产代码**（35% 是测试），每天可完成 **1-2 万行可用代码**。

## 核心哲学

### 完整性原则 (Boil the Lake)

> "不要做半桶水，要做就做一整桶"

AI 辅助编程应该追求完整实现，而非走捷径。识别问题后必须实际修复，完成一项任务意味着真正完成。

### 智能借鉴

在借鉴其他产品的功能时，始终思考：
1. 该功能在原始产品中为何有效？
2. 该功能在自己的产品中可能成功还是失败？
3. 需要哪些适配才能使其在自己的产品中成功？

## 技能目录

### 产品构思阶段

| 技能 | 描述 |
|------|------|
| [office-hours](./office-hours/SKILL.md) | YC 办公时间，验证产品创意 |
| [plan-ceo-review](./plan-ceo-review/SKILL.md) | CEO 视角评审计划 |
| [plan-eng-review](./plan-eng-review/SKILL.md) | 工程经理视角评审架构 |
| [plan-design-review](./plan-design-review/SKILL.md) | 设计师视角评审设计 |

### 开发阶段

| 技能 | 描述 |
|------|------|
| [review](./review/SKILL.md) | 高级工程师代码审查 |
| [investigate](./investigate/SKILL.md) | 调试调查专家 |
| [design-consultation](./design-consultation/SKILL.md) | 设计咨询 |

### 测试发布阶段

| 技能 | 描述 |
|------|------|
| [qa](./qa/SKILL.md) | QA 负责人测试并修复 bug |
| [qa-only](./qa-only/SKILL.md) | QA 报告员（纯报告） |
| [ship](./ship/SKILL.md) | 发布工程师自动化发布 |

### 文档与回顾

| 技能 | 描述 |
|------|------|
| [document-release](./document-release/SKILL.md) | 技术作家更新文档 |
| [retro](./retro/SKILL.md) | 工程经理团队回顾 |

### 强力工具

| 技能 | 描述 |
|------|------|
| [codex](./codex/SKILL.md) | OpenAI Codex 独立审查 |
| [careful](./careful/SKILL.md) | 危险操作警告 |
| [freeze](./freeze/SKILL.md) | 文件编辑锁定 |
| [guard](./guard/SKILL.md) | 完全安全模式 |

## 推荐工作流

```
1. /office-hours       → 向 AI 描述你想构建的产品
2. /plan-ceo-review  → CEO 视角评审功能想法
3. /plan-eng-review  → 工程经理锁定技术架构
4. /plan-design-review → 设计师评审设计
5. /review           → 高级工程师审查代码
6. /qa               → QA 测试暂环境
7. /ship             → 发布代码
```

## 使用方法

在 WorkBuddy 中，你可以通过以下方式使用这些技能：

1. **直接调用**：告诉 WorkBuddy 你想使用的技能，如"使用 office-hours 技能"
2. **场景触发**：描述你的需求，WorkBuddy 会自动推荐合适的技能
3. **组合使用**：多个技能配合使用，形成完整工作流

## 与 gstack 的区别

| 特性 | gstack (原版) | gstack-openclaw-skills |
|------|--------------|----------------------|
| 平台 | Claude Code | 通用 AI 助手 |
| 命令格式 | Slash 命令 | 技能调用 |
| 依赖 | Bun、Git、浏览器 | 无特殊依赖 |
| 本地脚本 | 包含 | 已转换为纯 prompt |

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 感谢 [Garry Tan](https://github.com/garrytan) 创建 gstack
- 本项目仅供学习交流使用

---

**版本**: 1.0.0  
**更新日期**: 2025-03-19
