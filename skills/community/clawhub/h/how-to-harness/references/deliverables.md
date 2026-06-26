# 产物模板与选择指南（Deliverables Templates & Guide）

> 用途：Capture 阶段帮用户选定产物形态 + Layer 4 阶段按 schema 组织已锁定的决策。
> 调用时机：Capture 阶段问
   │
   ├─ Q1: 这份材料最终给谁看？
   │    ├─ 管理层 / 上级 / 对外    → 走 PRD 或 One-Pager 路线
   │    ├─ 开发团队（实现用）      → 走 Design Doc 路线
   │    ├─ 跨团队（架构评审）      → 走 RFC 路线
   │    ├─ AI coding agent（直接开发）→ 走 Kickoff Checklist 路线
   │    └─ 自己（决策还在演化）    → 走 ADR 路线
   │
   ├─ Q2: 是否需要多方同步？
   │    └─ 是 → 多产物并行（推荐：One-Pager + 主产物 + Kickoff）
   │
   └─ Q3: 现有决策的锁定度？
        ├─ 还很模糊          → 先出 ADR，逐步演化
        ├─ 大方向定了         → 出 PRD 或 Design Doc
        └─ 完全锁定，准备落地  → 出 Kickoff Checklist + Milestone Plan
```

---

## 6 类产物模板

### 模板 1：PRD（Product Requirements Document）

**适用场景**：产品立项 / 评审 / 对管理层汇报 / 跨部门沟通

**核心价值**：把"用户价值 + 可度量成功标准 + 实现边界"三件事说清楚

**完整模板**：

```markdown
# <产品名> - Product Requirements Document

**Version**: 1.0
**Date**: YYYY-MM-DD
**Author**: xxx
**Status**: Draft / Review / Approved

---

## 1. Executive Summary

### Problem Statement
（1-2 句描述核心痛点，用数字支持）

### Proposed Solution
（1-2 句描述解决方案的核心思路）

### Success Criteria（MVP 完成后 N 周评估）
| KPI | 基线 | 目标 |
|-----|------|------|
| 指标 1 | ... | ... |
| 指标 2 | ... | ... |
| 指标 3 | ... | ... |

---

## 2. User Experience & Functionality

### 2.1 User Personas
**P1 · <角色名>**
- 身份：...
- 目标：...
- 痛点：...

（通常 2-4 类）

### 2.2 User Stories & Acceptance Criteria

#### US-1
**As a** <角色>
**I want to** <动作>
**so that** <收益>

**Acceptance Criteria**：
- 具体、可观测、二元判定的"Done"条件
- 尽可能量化

### 2.3 Non-Goals（显式排除）
- ❌ 不做 X
- ❌ 不做 Y
- ❌ 不做 Z

---

## 3. AI System Requirements（如适用）

### 3.1 Tool & Integration Requirements
| 调用方 | 被调用能力 | 来源 |

### 3.2 Evaluation Strategy
| 维度 | 权重 | 度量方法 |

**通过标准**：...

### 3.3 Safety & Guardrails
| 层级 | 机制 |

---

## 4. Technical Specifications

### 4.1 Architecture Overview
（附 Mermaid 架构图）

### 4.2 Component Breakdown
| 组件 | 归属 | 说明 |

### 4.3 Data Model
（核心实体 Schema，YAML 或伪代码示例）

### 4.4 Integration Points
| 交互 | 协议 | 认证 |

### 4.5 Security & Privacy
- 凭证管理
- 数据处理
- 审计
- 合规

---

## 5. Risks & Roadmap

### 5.1 Technical Risks
| 风险 | 概率 | 影响 | 缓解 |

### 5.2 Phased Rollout
| 阶段 | 目标 | 验收 | 时间 |

### 5.3 Dependencies & Assumptions
- 依赖：...
- 假设：...
```

**PRD 质量标准**：
- ❌ "The search should be fast" → ✅ "The search must return within 200ms for a 10k dataset"
- ❌ "UI must be modern" → ✅ "UI must follow the Vercel design system, Lighthouse Accessibility = 100"
- 每个 User Story 必须有 AC
- Non-Goals 必须显式列出

---

### 模板 2：Design Doc（设计文档）

**适用场景**：工程团队内部设计 / 新系统从 0 到 1

**核心价值**：把"怎么实现"说清楚，能直接指导编码

**完整模板**：

```markdown
# <系统名> Design Doc

**作者**：xxx · **日期**：YYYY-MM-DD · **状态**：Draft / Approved

---

## 1. Background & Goals

### 1.1 Current State
（现状 / 痛点，用数字支撑）

### 1.2 Goals
1. ...
2. ...

### 1.3 Non-Goals
- ❌ ...

---

## 2. Architecture

### 2.1 High-Level Architecture
（Mermaid 顶层图，分层结构）

### 2.2 Core Abstractions
- 关键抽象 1：职责 / 边界
- 关键抽象 2：职责 / 边界

### 2.3 Data Flow
（从输入到输出的完整路径）

---

## 3. Components

### 3.1 <Component-A>
- **职责**：...
- **接口**：（API / CLI / 消息）
- **内部结构**：...
- **依赖**：...

### 3.2 <Component-B>
...

---

## 4. Data Model

### 4.1 Core Entities
```yaml
entity_name:
  field_1: type (description)
  field_2: ...
```

### 4.2 Relationships
（ER 图或文字描述）

### 4.3 Storage Choice
- 选什么数据库 / 文件系统 / 消息队列
- 为什么

---

## 5. Workflow / State Machine

### 5.1 State Transitions
（Mermaid 状态图）

### 5.2 Idempotency / Retry / Resume
- 幂等性保证
- 重试策略
- 断点续传

---

## 6. Integration Points

| 方向 | 对端系统 | 协议 | 数据契约 |

---

## 7. Failure Modes & Recovery

| 故障类型 | 检测 | 应对 | 恢复 |

---

## 8. Milestones

| 阶段 | 目标 | 验收标志 | 估时 |

---

## 9. Risks

| 风险 | 概率 | 影响 | 缓解措施 |

---

## 附录

### A. Glossary（术语表）
### B. References（参考资料）
### C. Open Questions（待解决问题）
```

**Design Doc 与 PRD 的核心区别**：
- PRD 回答"做什么 / 为谁 / 成功标准是什么"
- Design Doc 回答"怎么做 / 怎么演进 / 怎么容错"

---

### 模板 3：RFC（Request For Comments）

**适用场景**：跨团队协作 / 架构评审 / 重大改造

**核心价值**：**显式列出 Alternatives Considered**，让评审者理解作者思考过程

**完整模板**：

```markdown
# RFC-XXX: <改造主题>

**作者**：xxx · **日期**：YYYY-MM-DD · **状态**：Draft / Review / Accepted / Rejected
**评审截止**：YYYY-MM-DD

---

## Context

### 当前状态
（系统 / 流程 / 痛点）

### 为什么现在改
（业务驱动 / 技术债 / 规模问题）

---

## Proposal

### 改动摘要
（一句话）

### 详细设计
（核心改动的具体形式）

### 前后对比（Before / After）
```diff
- 旧方案
+ 新方案
```

---

## Alternatives Considered

### 方案 A：...
- **做法**：...
- **优点**：...
- **缺点**：...
- **为什么不选**：...

### 方案 B：...
- ...

### 方案 C（最终选择）：...
- ...
- **为什么选**：...

---

## Impact

### 受影响的系统
| 系统 | 影响类型 | 需要配合 |

### 受影响的团队
| 团队 | 配合工作 | 时长估计 |

### 迁移策略
1. 阶段 1：...
2. 阶段 2：...

---

## Rollout Plan

| 阶段 | 内容 | 时间 | 回滚方案 |

---

## Open Questions
（留给 commenter 发表意见的问题）

1. Q1: ...
2. Q2: ...
```

**RFC 的独特价值**：Alternatives Considered 是必填项，体现作者思考过的深度。

---

### 模板 4：Kickoff Checklist / Milestone Plan（执行清单）

**适用场景**：方案已定 / 交给 AI coding agent 或执行团队落地

**核心价值**：**拆到"每个文件 / 每条命令"的粒度**，拿到即可开工

**完整模板**：

```markdown
# <项目名> · Week N Kickoff

> 目的：把 Week N 的工作拆到"每个文件 / 每条命令"的粒度，让 AI coding agent 能直接启动。

**验收标准**：<具体的、可观测的、二元判定的标准>

---

## 📍 当前状态

| 状态 | 说明 |
|------|------|
| ✅ 已完成 | ... |
| 🟡 待做 | ... |

---

## 🎯 任务全景（N 个 Task）

| # | Task | Executor | 时长 | 依赖 | 状态 |
|---|------|----------|------|------|------|
| T1 | 任务 A | dimayip | 30 min | - | 🟡 |
| T2 | 任务 B | AI agent | 1 h | T1 | 🟡 |

---

## 📁 T1: <任务名>

### Context
<背景、关键链接、设计文档路径>

### Repository Layout
<目录结构、关键文件位置>

### Steps
1. 具体步骤 1（含 bash 命令）
2. 具体步骤 2（含代码片段）
3. ...

### Constraints
⚠️ **不修改** ...
⚠️ **不删除** ...
⚠️ <其他硬约束>

### Deliverables
1. <产出 1>
2. <产出 2>

### Validation
（如何验证任务完成 + 具体命令 + 预期输出）

---

## 📁 T2: <任务名>
...

---

## 🎓 给<负责人>自己的清单（非代理部分）

| # | 事项 | 预计时长 | 状态 |
|---|------|---------|------|

---

## 🔗 相关文件
- 设计文档：...
- 上游 PRD：...
```

**Kickoff 清单的独特价值**：AI coding agent 拿到**每个 Task 的 prompt** 就能直接启动。

---

### 模板 5：ADR（Architecture Decision Record）

**适用场景**：决策还在演化中 / 想要可追溯的决策历史 / 避免"我们当时为什么这么决定"的疑问

**核心价值**：**粒度小、可增长**，每个关键决策一个文件

**完整模板**（单个 ADR）：

```markdown
# ADR-XXX: <决策主题>

**状态**：Proposed / Accepted / Deprecated / Superseded by ADR-YYY
**日期**：YYYY-MM-DD
**决策者**：xxx

---

## Context

### 决策背景
（为什么要做这个决策 / 触发事件）

### 约束
- 技术约束
- 业务约束
- 资源约束

### 驱动因素
（什么因素最重要？成本 / 时延 / 可靠性 / 可维护性？）

---

## Decision

我们决定：**<一句话说清决策>**

### 具体内容
（更详细的决策描述）

---

## Consequences

### 积极影响
- ...

### 消极影响
- ...

### 中性影响
- ...

---

## Alternatives Considered

### Alt A: ...
- **为什么不选**：...

### Alt B: ...
- **为什么不选**：...

---

## References
- 相关 ADR: ADR-YYY
- 相关讨论：...
```

**ADR 的目录组织**：

```
docs/adr/
├── 0001-use-postgres-over-mysql.md
├── 0002-adopt-event-sourcing.md
├── 0003-deprecate-redis-cache.md
└── ...
```

**ADR 的独特价值**：6 个月后新人问"我们为什么用 PostgreSQL？"，直接翻 ADR-0001 就有完整答案。

---

### 模板 6：One-Pager（单页摘要）

**适用场景**：对上汇报 / 横向同步 / 新人入职 / 30 秒介绍

**核心价值**：**一页 A4 说清楚所有事**

**完整模板**：

```markdown
# <系统名> · Executive One-Pager

**日期**：YYYY-MM-DD · **负责人**：xxx · **MVP**：X 周

---

## 一句话定位
> （一句话：是什么 / 为谁服务 / 核心方法论）

---

## 核心问题 → 本方案
| 核心问题 | 本方案 |
|---------|--------|
| 问题 1 | 解决方案 1 |
| 问题 2 | 解决方案 2 |
| 问题 3 | 解决方案 3 |

---

## 架构一图流
（Mermaid，一张图覆盖全景）

---

## 关键数据与时间
| 维度 | 数字 |
|------|------|
| 业务规模 | ... |
| 当前基线 | ... |
| MVP 时间 | ... |
| 人力投入 | ... |
| 预期提升 | ... |

---

## N 周交付节奏
```
Week 1  ...  ────●
Week 2  ...  ──────●
...
```

---

## 关键设计决策（Top 10）
1. ✅ ... 
2. ✅ ...
...

---

## 跟相关方沟通的要点
- **向上汇报**：...
- **横向团队**：...
- **执行团队**：...
- **终端用户**：...

---

**下一步**：...
```

**One-Pager 长度控制**：1500-2500 字（中文）或 800-1200 words（英文）。超过就是失败。

---

## 多产物并行（三件套 / 四件套）

触发条件：Capture 阶段确认有多类消费者（如 管理层 + 开发 + AI agent）。

推荐组合：

### 典型组合 A：产品立项场景
- **One-Pager**（对上）
- **PRD**（评审）
- **Kickoff Checklist**（开发）

### 典型组合 B：工程改造场景
- **RFC**（跨团队评审）
- **Design Doc**（实现团队）
- **Kickoff Checklist**（执行）

### 典型组合 C：从 0 到 1 设计
- **PRD**（定义做什么）
- **Design Doc**（定义怎么做）
- **Kickoff Checklist**（定义第一步怎么开工）
- **One-Pager**（对外同步）

**交付前一致性校验（必做）**：多份产物的核心决策必须完全一致。逐项检查：

- [ ] MVP 时间一致
- [ ] 成功标准一致
- [ ] 关键决策对齐（HP-1~HP-7 的具体答案在每份产物中保持同一答案）
- [ ] 角色分工一致

任一不一致 → 不交付，先补齐。

---

## 交付硬约束

- ❌ PRD/Design Doc 中残留"待确认"字样 → 回退到 Socratic 锁定决策，不带未锁项交付。
- ❌ One-Pager 超过 2 页 → 合并重复段落 / 删除非 Top 决策 / 用图代替文字。
- ❌ Kickoff 清单粒度只到"实现功能 X" → 必须细化到具体文件 / 命令 / 预期输出。
- ❌ RFC 缺少 Alternatives Considered → 必填项，未填不交。
- ❌ 把 Design Doc 当 PRD 写（堆实现细节）/ 把 PRD 当 Design Doc 写（堆架构图） → 视角对齐：PRD = 用户价值，Design Doc = 实现细节。
- ❌ 用户要多份产物只交一份 → 用 task_list 拆分，逐份交付。
