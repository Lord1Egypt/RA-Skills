---
name: gstack
description: 世界顶级思维合集 —— 融合Google Staff Engineer、Martin Fowler/Kent Beck/Jeff Dean工程思维、Paul Graham/Sam Altman创业思维、Elon Musk创新思维、Stripe/Airbnb设计思维。v2.5.10：移除install.sh以完全消除ClawHub Suspicious警告。
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "category": "productivity"
      }
  }
---

> **⚠️ 安全声明 | Security Notice**
> 
> **本技能为纯文档型技能（Documentation-only Skill）**。
> 
> - ✅ 不包含任何可执行代码或外部 API 调用
> - ✅ 不需要任何 API Key、凭证或 secrets
> - ✅ 不访问网络、不读写用户文件（除标准 OpenClaw 工具调用外）
> - ✅ 所有功能通过 AI 角色提示词（prompts）实现
> - ✅ 无安装脚本，无外部依赖
> 
> **提到的外部服务**（GitHub、CI/CD、monitoring）仅用于：
> - 在对话中提供最佳实践建议
> - 指导用户如何配置这些服务
> - 不直接调用这些服务的 API

# gstack

**gstack for OpenClaw** —— 把 Garry Tan 的虚拟工程团队带到 OpenClaw 生态

> 将 AI Agent 从一个通用助手转变为结构化工程团队的 8 个核心角色

---

## 🎯 设计理念

Garry Tan (YC CEO) 用 Claude Code + gstack 在 60 天内产出 60 万行代码。我们把它移植到 OpenClaw，让每个人都能拥有虚拟工程团队。

**核心思想**：不是把 AI 当工具用，而是**当团队管** —— 每个阶段切换不同专家角色。

---

## 📦 包含技能

| 技能 | 角色 | 用途 |
|-----|------|-----|
| `gstack:ceo` | CEO / 产品经理 | 产品规划、需求分析、痛点挖掘 |
| `gstack:eng` | 工程经理 | 架构设计、技术选型、数据流规划 |
| `gstack:design` | 设计评审师 | 设计评审、AI Slop检测、设计系统生成 |
| `gstack:investigate` | 系统调试专家 | 根因分析、3次失败停止、Bug调查 |
| `gstack:security` | 首席安全官 | OWASP Top 10、STRIDE威胁建模 |
| `gstack:land` | 部署验证工程师 | PR合并、生产部署、健康验证 |
| `gstack:canary` | 金丝雀监控工程师 ⭐ NEW | 金丝雀分析、自动回滚决策 |
| `gstack:benchmark` | 性能基准工程师 ⭐ NEW | Core Web Vitals、性能回归检测 |
| `gstack:review` | 代码审查员 | 代码审查、Bug 发现、性能优化建议 |
| `gstack:qa` | QA 负责人 | 测试策略、验收标准、质量把关 |
| `gstack:ship` | 发布工程师 | 发版 checklist、部署流程、上线检查 |
| `gstack:browse` | 浏览器测试 | 网页抓取、功能验证、UI 检查 |
| `gstack:retro` | 复盘师 | 项目复盘、经验总结、改进建议 |
| `gstack:office` | 办公室时间 | 需求澄清、方向校准、头脑风暴 |

---

## 🚀 快速开始

### 1. 安装

```bash
clawhub install openclaw/gstack
```

或手动安装：

```bash
git clone https://github.com/openclaw/gstack-openclaw ~/.openclaw/skills/gstack
cd ~/.openclaw/skills/gstack && ./install.sh
```

### 2. 使用

在项目根目录创建 `GSTACK.md` 文件，记录项目上下文。

然后随时调用：

**示例命令：**
- `@gstack:ceo 帮我分析一下这个功能的产品价值`
- `@gstack:review 审查一下这个模块的代码`
- `@gstack:ship 准备发布 v1.0.0`

---

## 🎭 工作流示例

### 新功能开发流程

1. `@gstack:office` — 澄清需求，确定方向
2. `@gstack:ceo` — 产品规划，写 PRD
3. `@gstack:design` — 设计评审，生成设计系统
4. `@gstack:eng` — 技术架构设计
5. 【开发中...】
6. `@gstack:review` — 代码审查
7. `@gstack:qa` — 测试验收
8. `@gstack:ship` — 发布上线
9. `@gstack:retro` — 一周后复盘

---

## 📁 项目结构

**文件组织：**

- `SKILL.md` — 本文件（主技能描述）
- `README.md` — 详细使用文档
- `GSTACK.md.template` — 项目上下文模板
- `_skills/` — 子技能目录
  - `plan-ceo/` — CEO 技能
  - `plan-eng/` — 工程经理技能
  - `design/` — 设计评审技能 (v2.5.0)
  - `investigate/` — 系统调试技能 (v2.5.1)
  - `security/` — 安全审计技能 (v2.5.2)
  - `land/` — 部署验证技能 (v2.5.3)
  - `canary/` — 金丝雀监控技能 (v2.5.4) ⭐ NEW
  - `benchmark/` — 性能基准技能 (v2.5.5) ⭐ NEW
  - `review/` — 代码审查技能
  - `qa/` — QA 技能
  - `ship/` — 发布技能
  - `browse/` — 浏览器测试技能
  - `retro/` — 复盘技能
  - `office/` — 办公室时间技能
  - `docs/` — 文档技能
  - `test/` — 测试技能
  - `deploy/` — 部署技能
  - `init/` — 初始化技能
  - `status/` — 状态追踪技能
  - `github/` — GitHub 集成技能
  - `notify/` — 通知技能
- `docs/` — 文档目录
  - `workflow.md` — 完整工作流指南
  - `philosophy.md` — 设计理念

---

## 🙏 致谢

- [Garry Tan](https://github.com/garrytan) —— 原创 gstack 作者
- [Y Combinator](https://www.ycombinator.com/) —— 持续推动创业生态
- OpenClaw 社区 —— 让 AI Agent 触手可及

---

## 📄 License

MIT License —— 完全免费，随意使用、修改、分发

**我们的目标**：让每个开发者都能拥有 YC 级别的工程团队

---

*Made with 🦞 by OpenClaw Community*
