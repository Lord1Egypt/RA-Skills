# 智能图形库（Smart Graphics / SmartArt / Diagrams）

咨询 / 汇报 / 提案类 PPT 常用关系图来表达丰富信息之间的层级、关系、逻辑。

> **核心思路**
> 不要让 LLM 直接"画关系图形"。流程应该是：
>
> ```text
> 内容 (Content)
>   ↓
> 语义图 (Semantic Graph: 节点 + 关系)
>   ↓
> 图形类型路由 (Diagram Router)
>   ↓
> 图形模板 (Diagram Template)
>   ↓
> 自动布局 (Auto Layout)
>   ↓
> PPTX 渲染 (pptxgenjs)
>   ↓
> 视觉质检 (Visual QA)
> ```
>
> **第一原则**：先识别"信息之间的关系是什么"（Hierarchy / Process / Cycle / Comparison / Matrix），再选图形类型，再决定视觉样式。
> **第二原则**：关系语义优先于视觉装饰——`causes` 用粗实线箭头，`depends_on` 用虚线箭头，`maps_to` 用细线；不要所有关系都用同一种箭头。
>
> 这个文件是**图形类型与关系语义的索引**，不是实现细节。实现见 SKILL.md 主体的「## 对于每张幻灯片」。

---

## 相关文件与依赖关系

> **本文件定位**：结构维度（topology）——信息是什么拓扑？

| 文件 | 关系 | 何时查阅 |
|---|---|---|
| [SKILL.md](../SKILL.md) | 上游入口 | 整个生成流程的入口、配色 / 字体 / QA 规则 |
| [slide-layouts.md](slide-layouts.md) | 正交维度 | 单页怎么分块（上下 / 左右 / 矩阵 / 时间…）——和本页正交，不冲突 |
| [visual-metaphors.md](visual-metaphors.md) | **主从张力**（见该文件 §32 与末尾"## 与 diagrams.md 的关系"） | 当这页是**隐喻主导**（转型 / 升级 / 突破 / 增长等情绪）时 |
| [优普丰品牌设计配色方案.md](优普丰品牌设计配色方案.md) | 下游（视觉层） | 选好结构后用什么颜色 |

### 三个 reference 文件的分工

```
slide-layouts.md     ← 单页布局（page-level, ortho dimension）
       │
       ▼
┌──────────────────┐
│  这页 PPT 内容    │
└────────┬─────────┘
         │
   ┌─────┴──────┐
   ↓            ↓
diagrams.md    visual-metaphors.md
(结构维度)     (隐喻维度)
   │            │
   └─────┬──────┘
         ↓
   pptxgenjs 渲染
         ↓
   视觉 QA
```

### 关键交叉点（在本文件中的位置）

- §10 路由示例 → 选图前先看 §10.1 的 4 元组（Entity / Relationship / Problem / Target）
- §12 路由规则 → 完整 if/then 路由逻辑
- §16 端到端 Pipeline → 含 visual_intent 的最小完整示例
- §32（跨文件）→ visual-metaphors.md 里的 `visual_intent` schema，包含 `relation_to_base_structure` 字段判断"兼容 vs 覆盖"

### 与 visual-metaphors.md 的引用约定

本文件讲**结构**（什么形状适合数据），visual-metaphors.md 讲**隐喻**（什么情绪适合叙事）。两者关系见视觉隐喻库末尾的"## 与 diagrams.md 的关系（主从张力模型）"。

> **本文件不教怎么讲故事，那是 `visual-metaphors.md` 的事。**

---


## 目录

**Part A — 图形类型库（选哪种图形？）**

- §1 [Hierarchy（层级 / 包含）](#1-hierarchy层级--包含)
- §2 [Process（流程 / 序列）](#2-process流程--序列)
- §3 [Cycle（循环 / 闭环）](#3-cycle循环--闭环)
- §4 [Comparison（对比）](#4-comparison对比)
- §5 [Matrix（矩阵）](#5-matrix矩阵)
- §6 [Framework（框架 / 模型）](#6-framework框架--模型)
- §7 [Strategy（战略）](#7-strategy战略)
- §8 [Architecture（架构）](#8-architecture架构)
- §17 [Mapping（映射 / 跨映射）](#17-mapping映射--跨映射)

**Part B — 语义与路由（怎么决定用哪种？）**

- §9 [关系语义库（Relationship Semantics Library）](#9-关系语义库relationship-semantics-library)
- §10 [路由示例（Router Examples）](#10-路由示例router-examples)
- §11 [咨询推理模式（Consulting Reasoning Patterns）](#11-咨询推理模式consulting-reasoning-patterns)
- §12 [路由规则（Router Rules）](#12-路由规则router-rules)

**Part C — 渲染与质检（怎么画漂亮？怎么检查？）**

- §13 [Auto Layout 原则](#13-auto-layout-原则)
- §14 [Connector Routing & Visual Hierarchy](#14-connector-routing--visual-hierarchy)
- §15 [Visual QA 三维度](#15-visual-qa-三维度)
- §16 [端到端 Pipeline 示例（AI 转型三层架构）](#16-端到端-pipeline-示例ai-转型三层架构)

**Part D — 模板与索引（拿来即用）**

- §18 [咨询模板库（Diagram Templates）](#18-咨询模板库diagram-templates)
- §19 [完整 Diagram Primitives 索引](#19-完整-diagram-primitives-索引)

**附：选择流程 + Diagram Generation Rules**

---

## 1. Hierarchy（层级 / 包含）

表达：A 包含 B、A 是 B 的上级、A 属于 B。

| 图形 | 适用场景 |
|---|---|
| **Pyramid** | 战略层 / 业务层 / 执行层；自上而下的层级 |
| **Organization Chart** | 组织架构、汇报关系 |
| **Tree Structure** | 问题树、决策树、分解结构 |
| **Hierarchy Diagram** | 通用层级关系 |
| **Nested Boxes** | 嵌套的范围 / 子模块 |
| **Nested Circles** | 层级 + 视觉柔和感 |
| **Tiered Structure** | 分层架构、责任分层 |

**典型表达：**

```text
战略层
   ↓
业务层
   ↓
执行层
```

**YAML 示例：**

```yaml
# Pyramid（金字塔）
type: pyramid
levels:
  - id: strategy
    label: 战略层
  - id: business
    label: 业务层
  - id: execution
    label: 执行层

# Layered Architecture（分层架构）
type: layered_architecture
layers:
  - Business
  - Process
  - Data
  - Technology

# Tree（树）
type: tree
root:
  id: problem
  label: 核心问题
children:
  - id: people
    label: 人
  - id: process
    label: 流程
  - id: technology
    label: 技术
```

---

## 2. Process（流程 / 序列）

表达：A 发生在 B 之后、A 导向 B。

| 图形 | 适用场景 |
|---|---|
| **Chevron Process** | 阶段性强、强调方向感 |
| **Arrow Process** | 通用线性流程 |
| **Step Process** | 编号步骤、可数阶段 |
| **Circular Process** | 流程回到起点（注意与 Cycle 区分） |
| **Continuous Cycle** | 强调连续不间断 |
| **Workflow** | 业务 / 工作流（节点 + 决策） |
| **Stage-Gate** | 阶段 + 准入门槛（POC → Pilot → Scale） |
| **Pipeline** | 漏斗前的多步流转 |
| **Funnel** | 漏斗：从大量到少量（销售、转化） |

**典型表达：**

```text
发现问题 → 分析问题 → 设计方案 → 实施 → 验证
```

**YAML 示例：**

```yaml
# Linear Process（线性流程）
type: linear_process
steps:
  - 识别问题
  - 分析原因
  - 设计方案
  - 实施
  - 验证

# Stage Gate（阶段门）
type: stage_gate
stages:
  - name: Discovery
  - name: POC
  - name: Pilot
  - name: Scale
gates:
  - after: POC
    decision: "Go / No-Go"

# Hub & Spoke（中心辐射）
type: hub_spoke
hub:
  id: ai_platform
  label: AI 平台
spokes:
  - id: organization
    label: 组织
  - id: process
    label: 流程
  - id: data
    label: 数据
  - id: agent
    label: Agent
```

**ASCII 示意：**

```text
           组织
            ↑
            │
流程 ←── AI平台 ──→ 数据
            │
            ↓
           Agent
```

适用场景：中心节点明确（这里是 AI 平台），周边有 3-8 个 spoke 节点，关系是**单向**或**中心向外辐射**。

**⚠️ 何时不要用 Hub & Spoke：**

如果周边节点之间也存在关系（如流程 ↔ 数据），或整体是**多对多网络**（如 Customer ↔ Platform ↔ Partner ↔ Agent ↔ Data），应该用 **Ecosystem**（§17.5）而不是 Hub & Spoke。

---

## 3. Cycle（循环 / 闭环）

表达：A 强化 A、持续改进、生命周期、反馈回路。

| 图形 | 适用场景 |
|---|---|
| **Circular Cycle** | PDCA、双因素闭环 |
| **Continuous Cycle** | 永续运转 |
| **PDCA Cycle** | 戴明环：Plan-Do-Check-Act |
| **Flywheel** | 飞轮：势能积累（亚马逊、增长模型） |
| **Lifecycle** | 产品 / 用户 / 客户生命周期 |
| **Feedback Loop** | 反馈回路 |
| **Closed Loop** | 业务闭环、运营闭环 |

**适合：** 持续改进、产品生命周期、运营闭环、AI Agent Loop。

---

## 4. Comparison（对比）

表达：A 与 B 对比、A vs B、Before vs After。

| 图形 | 适用场景 |
|---|---|
| **Before / After** | 转型前后、改造前后 |
| **Current / Future** | 现在 vs 未来 |
| **As-Is / To-Be** | 现状 vs 目标（咨询常用） |
| **Traditional / New** | 旧 vs 新 |
| **Internal / External** | 内外对比 |
| **Option A / Option B** | 方案对比、决策 |
| **Good / Better** | 改进路径 |
| **Gap Analysis** | 差距分析（与 Current × Target 矩阵可互换） |

---

## 5. Matrix（矩阵）

表达：两个维度交叉分类。

| 图形 | 适用场景 |
|---|---|
| **2×2 Matrix** | 通用双维度（优先级、定位） |
| **3×3 Matrix** | 三档等级（成熟度、机会） |
| **Priority Matrix** | 优先级排序 |
| **Impact / Effort Matrix** | 影响 × 投入 |
| **Value / Complexity Matrix** | 价值 × 复杂度 |
| **Risk Matrix** | 风险 × 概率 |
| **Maturity Matrix** | 能力成熟度 |
| **Capability Matrix** | 能力盘点 |

**YAML 示例（Impact × Effort）：**

```yaml
type: matrix
x_axis:
  label: Implementation Effort
  low: 0
  high: 10
y_axis:
  label: Business Impact
  low: 0
  high: 10
items:
  - name: AI FAQ
    x: 2
    y: 8
  - name: AI Forecast
    x: 7
    y: 9
  - name: AI Report
    x: 3
    y: 6
```

自动布局产出 2×2 象限：

```text
High Impact
    │
    │   Quick Wins       Strategic Bets
    │
    │
    │   Fill-ins         Avoid / Later
    │
    └──────────────────────────────
       Low Effort       High Effort
```

四个象限的语义：

- **Quick Wins**（左上：高影响 + 低投入）→ 优先做
- **Strategic Bets**（右上：高影响 + 高投入）→ 战略性投入
- **Fill-ins**（左下：低影响 + 低投入）→ 有空再做
- **Avoid / Later**（右下：低影响 + 高投入）→ 暂缓

---

## 6. Framework（框架 / 模型）

表达：3 层 / 4 支柱 / 5 维度等结构化思考模型。

| 图形 | 适用场景 |
|---|---|
| **3-Layer Framework** | 三层架构（业务/流程/技术） |
| **4-Pillar Framework** | 四大支柱 |
| **5-Dimension Framework** | 五力 / 五维分析 |
| **House Model** | 战略屋（愿景/使命/战略/举措） |
| **Pyramid Framework** | 金字塔模型（自上而下） |
| **Layered Architecture** | 分层架构 |
| **Capability Map** | 能力地图（多维度能力盘点） |
| **Operating Model** | 运营模型 |
| **Business Model Canvas** | 商业模式画布 |

---

## 7. Strategy（战略）

表达：愿景 → 战略 → 执行的承接关系。

| 图形 | 适用场景 |
|---|---|
| **Strategy House** | 战略屋 |
| **Strategic Pyramid** | 战略金字塔 |
| **Three Horizons** | 三视野模型（H1 现业务、H2 兴起业务、H3 未来业务） |
| **North Star** | 北极星指标 |
| **Strategic Choices** | 战略选择 |
| **Strategic Themes** | 战略主题 |
| **Vision → Strategy → Execution** | 愿景 → 战略 → 执行 |
| **Objectives → Initiatives → KPIs** | 目标 → 举措 → 关键结果 |

**Roadmap YAML 示例（Now / Next / Later）：**

```yaml
type: roadmap
horizons:
  - name: Now
    period: "0-3 months"
  - name: Next
    period: "3-12 months"
  - name: Later
    period: "12-24 months"
workstreams:
  - name: Organization
  - name: Process
  - name: Technology
  - name: AI
```

自动产出横向 swimlane 时间线：

```text
             NOW             NEXT             LATER

Organization ────────●────────────────────────────
Process      ───────────────●─────────────────────
Technology   ─────●───────────────●───────────────
AI           ─────────●──────────────────●────────
```

每个 workstream 一行，每个 horizon 占一段，节点位置由 start/end period 自动推算。

---

## 8. Architecture（架构）

表达：分层、堆叠、平台 + 模块、生态结构。

| 图形 | 适用场景 |
|---|---|
| **Layered Architecture** | 分层架构 |
| **Stack** | 技术栈 |
| **Platform Model** | 平台 + 应用 |
| **Operating Model** | 运营模型（组织 + 流程 + 技术） |
| **Capability Architecture** | 能力架构 |
| **Business Architecture** | 业务架构 |
| **Technology Architecture** | 技术架构 |
| **Hub-and-Spoke** | 中心辐射（与第 5 节 Hub & Spoke 同源） |
| **Modular Architecture** | 模块化架构 |

**典型表达：**

```text
        Business Strategy
              ↓
        Business Capabilities
              ↓
        Processes / Products
              ↓
        Technology / Data
              ↓
        Infrastructure
```

---

## 9. 关系语义库（Relationship Semantics Library）

> **目标**：关系图不是"节点 + 线"。每一条线都应该表达一种明确的语义。
> Agent 第一步判断「A 和 B 到底是什么关系？」，再决定「用什么线 / 箭头 / 方向 / 样式？」。

### 9.1 关系 Schema（每个关系的标准描述）

```yaml
relationship:
  id: "supports"            # 关系 ID
  semantic:
    name: "支撑"             # 中文名
    description: "A 为 B 提供能力、资源或基础"
  direction:
    directed: true           # 是否带方向
  visual:
    connector: "arrow"       # 箭头类型
    line_style: "solid"      # solid / dashed / dotted
    arrow: "end"             # end / start / both / none
    weight: "medium"         # thin / medium / bold
  layout:
    preferred_direction: "bottom_to_top"  # top_to_bottom / left_to_right / radial
  examples:
    - "数据平台 → AI 应用"
    - "组织能力 → 战略执行"
```

### 9.2 关系类型全集

#### A. Hierarchical（层级 / 包含）

```yaml
contains:        { meaning: "A 包含 B",         visual: container }
parent_of:       { meaning: "A 是 B 的上级",     visual: downward_arrow }
belongs_to:      { meaning: "A 属于 B",         visual: upward_arrow }
part_of:         { meaning: "A 是 B 的组成部分", visual: nested }
```

#### B. Causal（因果）

```yaml
causes:          { meaning: "A 导致 B",                  visual: { connector: strong_arrow } }
contributes_to:  { meaning: "A 对 B 有贡献",              visual: { connector: thin_arrow } }
drives:          { meaning: "A 是 B 的主要驱动力",         visual: { connector: bold_arrow } }
```

#### C. Dependency（依赖）

```yaml
depends_on:      { meaning: "A 依赖 B",                  visual: { connector: dashed_arrow } }
requires:        { meaning: "A 需要 B",                  visual: { connector: dashed_arrow } }
enables:         { meaning: "A 使 B 成为可能",            visual: { connector: solid_arrow } }
```

#### D. Sequence（时序）

```yaml
precedes:        { meaning: "A 发生在 B 之前" }
follows:         { meaning: "A 发生在 B 之后" }
leads_to:        { meaning: "A 导向 B" }
```

#### E. Mapping（映射）

```yaml
maps_to:         { meaning: "A 对应 B",                  visual: { connector: thin_line } }
implements:      { meaning: "A 实现 B",                  visual: { connector: arrow } }
addresses:       { meaning: "A 解决 B",                  visual: { connector: arrow } }
```

#### F. Feedback（反馈）

```yaml
feedback:        { meaning: "A 和 B 相互反馈",            visual: { connector: bidirectional } }
reinforces:      { meaning: "A 强化 B",                  visual: { connector: circular_arrow } }
```

#### G. Comparison（对比）

```yaml
compares_to:     { meaning: "A 与 B 对比",               visual: { connector: comparison_line } }
contrasts_with:  { meaning: "A 与 B 存在差异",            visual: { connector: contrast_line } }
```

### 9.3 关系渲染规则（Rendering Rules）

**Rule 1：不要所有关系都使用同一种箭头。**

如果这些线分别代表 `causes` / `depends_on` / `maps_to`，视觉上**必须**有区别——粗细、虚实、方向都得能区分。

**Rule 2：关系语义优先于视觉装饰。**

```text
Semantic relationship
        ↓
Connector type
        ↓
Direction
        ↓
Line style
        ↓
Color / emphasis
```

而不是：

```text
Looks nice
   ↓
Draw random arrows
```

**Rule 3：不要用颜色代替关系语义。**

颜色主要用于：

- 分类（categorization）
- 强调（emphasis）
- 状态（status）
- 风险（risk）
- 优先级（priority）

不要把"红色 = causes，蓝色 = supports"当成唯一的关系表达——色弱 / 单色印刷 / 灰度投影都会丢失信息。

### 9.4 关系渲染速查（Quick Reference）

下面这张表是 Agent 在做 connector 决策时的**直接查表清单**：

| 关系类型 | 视觉建议 | 备注 |
|---|---|---|
| `contains` | 实线 / 容器 | 层级包含 |
| `depends_on` | 虚线箭头 | 强依赖 |
| `causes` | 强箭头 | 因果 |
| `supports` | 普通箭头 | 支撑 |
| `feedback` | 双向箭头 | 反馈闭环 |
| `optional` | 虚线 | 可选路径 |
| `conflict` | 红色 / 叉号 | 冲突关系 |
| `equivalent` | 双向连接 | 等价 / 平行 |
| `sequence` | 单向箭头 | 时序 |
| `mapping` | 对齐连线 | 映射（非层级） |

**记住：** 任何一条线都应该能从视觉上**立刻**读出它的语义。读者不需要图例就能区分。

---

## 10. 路由示例（Router Examples）

> **目的**：拿到一段文字，Agent 应当按"抽 Entity / Relationship / Problem / Target → 决定 Diagram"四步走。
> 不是凭感觉选图，是按语义路由。

### 10.1 抽取模板

```yaml
Entity       = <核心实体 1..n>
Relationship = <主关系类型，取自 §9.2>
Problem      = <当前痛点 / 信息缺失>
Target       = <期望产出 / 想强调的洞察>
```

### 10.2 路由案例库

| 输入文本 | Entity | Relationship | Problem | Target | → 路由到 |
|---|---|---|---|---|---|
| "部门之间数据不互通" | Departments | Data Flow | Silo | Integrated Flow | **Sankey / Value Stream** |
| "战略如何落地到执行" | Strategy / Business / Execution | contains (hierarchical) | alignment gap | cascaded execution | **Layered Architecture (Pyramid)** |
| "问题的根因拆不清楚" | Issue Tree branches | hierarchical decomposition | root cause unclear | actionable branches | **Issue Tree** |
| "现状与目标的差距" | As-Is / To-Be | comparison | gap unclear | prioritized initiatives | **Gap Analysis / Before-After** |
| "市场有 4 个细分象限" | 2 dimensions × quadrants | matrix positioning | portfolio unclear | invest / divest | **2×2 Matrix** |
| "AI 如何驱动业务价值" | Objective → Scenario → Use Case → Capability → Agent → Value | mapping + sequence | value path unclear | AI roadmap | **AI Transformation Map** |
| "产品持续改进的闭环" | Plan / Do / Check / Act | cycle | improvement stagnant | closed loop | **PDCA Cycle** |
| "客户旅程从认知到复购" | Touchpoints | sequence | conversion drop | journey optimization | **Funnel + Process** |

### 10.3 路由决策流程

1. **抽取 4 元组**：从原文找出 Entity / Relationship / Problem / Target。
2. **查 §9.2 表**：把 Relationship 映射到 Hierarchical / Causal / Dependency / Sequence / Mapping / Feedback / Comparison 之一。
3. **查 §1-§8 章节**：根据 Relationship + Entity 数量 + Problem 类型，挑出最匹配的图形（参见 §10.2 路由表）。
4. **套模板**：匹配命中 → 用已知模板 → Auto Layout 出坐标。
5. **没有匹配**：降级到最接近的通用结构（Process / Hierarchy / Matrix），不要硬画。

### 10.4 完整 Router Examples（3 个真实场景）

> 这里是 §10.2 路由表的**完整版**——含输入文本、semantic graph、Router 完整 YAML 输出。
> 和"被选中" vs"被拒绝"的对比示例。

#### Router Example 1 — 优先级矩阵（Impact × Effort）

**输入：**

```text
我们有 20 个 AI 应用场景，
按照业务价值和实施难度进行分类，
并希望找出优先实施的场景。
```

**Semantic extraction：**

```yaml
entities:
  - AI Use Case

dimensions:
  - Business Value
  - Implementation Difficulty

objective:
  - Prioritization
```

**Router 决策：**

```yaml
selected_diagram:
  type: matrix
  subtype: impact_effort
```

**而不是：**

```yaml
selected_diagram:
  type: cards      # ❌ cards 不能体现 2D 分类
```

**理由：** 内容有 2 个维度（Business Value × Implementation Difficulty）+ 大量 items（20 个 AI 场景）→ 命中 §12 router_rules 中 `dimensions: 2, items: many → matrix` 规则。

---

#### Router Example 2 — 分层架构（Layered Hierarchy）

**输入：**

```text
AI 战略向下分解成业务目标、
业务目标进一步形成 AI 场景，
AI 场景再落到 Agent 和自动化能力。
```

**Semantic graph：**

```text
Strategy
   ↓
Business Objective
   ↓
AI Use Case
   ↓
Agent / Automation
```

**Router 决策：**

```yaml
diagram:
  type: layered_hierarchy
```

**理由：** 单向 contains 关系、4 层深度、纯层级 → 命中 `relationship: hierarchy, depth: 3+ → tree / layered_architecture`。完整 5 步示例见 §16。

---

#### Router Example 3 — 跨职能多对多（Cross-Functional Many-to-Many）

**输入：**

```text
研发、采购、SQE 和物流之间存在多个数据断点，
一个 AI 场景可能同时涉及多个部门。
```

**Router 决策：**

```yaml
relationship: many_to_many
problem: cross_functional_dependency

diagram:
  type: cross_mapping
```

**而不是：**

```yaml
diagram:
  type: hub_spoke    # ❌ hub_spoke 会丢失"多个 AI 场景 ↔ 多个部门"的交叉关联
```

**理由：** 4 个部门（研发/采购/SQE/物流）+ 多个 AI 场景 + 关系是**多对多** + 问题本质是**数据断点 / 跨职能依赖** → 命中 `many_to_many → mapping` 规则，应该用 cross_mapping 而不是 hub_spoke。

完整 Many-to-Many Mapping YAML 模板见 §17.3。

---

## 11. 咨询推理模式（Consulting Reasoning Patterns）

> **目的**：让 Agent 直接识别「咨询场景的常见叙事骨架」，而不是从零造结构。
> 每种模式都是一组固定的实体序列 + 一个对应的推荐图形。

### 11.1 Diagnosis（诊断）

```text
Symptom → Problem → Root Cause → Impact
```

→ **Issue Tree**（问题树 / 鱼骨图）

适用：客户说"业绩下滑"——把症状拆成根因。

### 11.2 Strategy（战略）

```text
Vision → Strategic Choices → Pillars → Initiatives → KPIs
```

→ **Strategy Pyramid / Strategy House**

适用：年度战略汇报、董事会汇报。

### 11.3 Transformation（转型）

```text
Current State → Gap → Target State → Initiatives → Roadmap
```

→ **Transformation Architecture**（As-Is / To-Be + Roadmap）

适用：数字化转型、组织变革、流程重塑。

### 11.4 AI Transformation（AI 转型）

```text
Business Objective → Business Scenario → AI Use Case → AI Capability → AI Agent → Business Value
```

→ **AI Transformation Map**（价值链展开图）

适用：AI 战略落地、Agent 应用场景设计。

### 11.5 使用方式

- **先看文本属于哪种咨询场景**（诊断 / 战略 / 转型 / AI 转型）→ 套对应骨架。
- **如果不属于任何一种**，回到 §1-§8 按图形类型自由组合。
- **不要把不同模式混着画**：一页讲一个 Pattern，清晰度优先。

---

## 12. 路由规则（Router Rules）

> **目标**：拿到一段文字，自动判断用哪种图形。Agent 不应凭感觉选——而应按下面的 if/then 规则路由。
> **判定流程**：先抽 §10.1 的 4 元组（Entity / Relationship / Problem / Target），再用下面规则匹配。

```yaml
router_rules:

  # 矩阵类
  - if:
      dimensions: 2
      items: many
    then:
      diagram: matrix

  # 层级类
  - if:
      relationship: hierarchy
      depth: 3+
    then:
      diagram: tree

  # 序列类
  - if:
      relationship: sequence
    then:
      diagram: linear_process

  - if:
      relationship: lifecycle
    then:
      diagram: circular_cycle

  # 映射类
  - if:
      relationship: many_to_many
    then:
      diagram: mapping                # ← 注意：many-to-many 用 mapping，不用 hub_spoke

  # 中心辐射 vs 生态网络（关键区分！）
  - if:
      central_node: true
      spokes: 3-8
      relationships: one_way
    then:
      diagram: hub_spoke              # 单向、中心明确 → Hub & Spoke

  - if:
      nodes: many
      relationships: bidirectional_many
      pattern: network
    then:
      diagram: ecosystem              # 多对多、双向、像 Customer/Platform/Partner/Agent → Ecosystem，不要硬塞 hub_spoke

  # 时间线
  - if:
      x_axis: time
    then:
      diagram: roadmap

  # 对比类
  - if:
      current_state: true
      target_state: true
    then:
      diagram: before_after

  # 战略类（从推理模式路由）
  - if:
      pattern: diagnosis
    then:
      diagram: issue_tree

  - if:
      pattern: strategy
    then:
      diagram: strategy_pyramid

  - if:
      pattern: transformation
    then:
      diagram: transformation_architecture

  - if:
      pattern: ai_transformation
    then:
      diagram: ai_transformation_map
```

**关键陷阱：** `many-to-many` ≠ Hub & Spoke。看到"研发/采购/SQE/物流之间数据断点"，应该想到 ecosystem 或 mapping，不是 hub_spoke。

---

## 13. Auto Layout 原则

### 13.1 铁律：LLM 不要手算坐标

```text
LLM
 ↓
Graph structure（节点 + 关系）
 ↓
Layout algorithm（计算坐标）
 ↓
Render
```

**完整的 Auto Layout Pipeline：**

```text
Semantic Graph
      ↓
Graph Constraints        # §13.3 的 canvas/nodes/spacing/text/connectors 约束
      ↓
Layout Algorithm         # §13.2 按 diagram type 选算法
      ↓
Bounding Boxes           # 节点尺寸 + 位置
      ↓
Connector Routing        # §14.1 连线路由（orthogonal / direct / curved）
      ↓
Collision Detection      # 检测碰撞并修复
      ↓
Render
```

**错误示范（LLM 随机生成坐标）：**

```text
x = random()
y = random()
```

**正确流程（结构化数据 → 算法 → 坐标）：**

```js
const graph = {
  nodes: [
    { id: "strategy", importance: 1.0 },
    { id: "business", importance: 0.7 },
    { id: "execution", importance: 0.4 }
  ],
  edges: [
    { from: "strategy", to: "business" },
    { from: "business", to: "execution" }
  ]
}

const layout = layoutEngine.calculate(graph, {
  algorithm: "dag_sugiyama",
  constraints: layoutConstraints
})

render(layout)
```

**严禁 LLM 输出：**

```text
x: 3.72
y: 5.18
width: 1.23
height: 0.72
```

**应该输出：**

```yaml
nodes:
  - id: strategy
  - id: business
  - id: execution
edges:
  - strategy -> business
  - business -> execution
```

让 Layout Engine 根据图形类型选算法算坐标。

### 13.2 图形类型 → 布局算法选择

| 图形类型 | 推荐算法 | 说明 |
|---|---|---|
| **Hierarchy（树 / 金字塔 / 分层架构）** | **DAG / Sugiyama** | 自顶向下分层，父节点居中于子节点 |
| **Network（生态 / 复杂网络）** | **Force-directed** | 力导向，自动避让，适合无明确层级 |
| **Timeline（时间线 / Roadmap）** | **Linear layout** | 横向或纵向线性排列，按时间 index |
| **Tree（问题树 / 决策树）** | **Tree layout** | 递归计算子树宽度，父节点居中 |
| **Matrix（矩阵 / 热力图）** | **Grid layout** | 按 x/y 归一化到网格 |
| **Hub & Spoke / Radial** | **Radial layout** | 极坐标：中心点 + 角度均匀分布 |

### 13.2.1 Hierarchy 算法（7 步）

```text
Algorithm:

1. Identify root nodes             # 识别根节点
2. Calculate node depth            # 计算每个节点深度
3. Group nodes by depth            # 按深度分层
4. Calculate width of each subtree # 计算每个子树宽度
5. Position parent at center of children  # 父节点居中于子节点中间
6. Resolve sibling collisions      # 解决兄弟节点碰撞
7. Normalize spacing               # 统一间距
```

### 13.2.2 Radial 算法

```text
angle = 360° / node_count

for each node:
    x = centerX + radius * cos(angle)
    y = centerY + radius * sin(angle)
```

### 13.2.3 Timeline 算法

```text
timeline_x = startX + index * interval
node.y     = lane_y[workstream]    # 每个 workstream 占一条 lane
```

### 13.2.4 Matrix 算法

```text
column = normalize(x_value)
row    = normalize(y_value)

x = matrix.left + column * matrix.width
y = matrix.bottom - row * matrix.height
```

### 13.3 Auto Layout Constraints（标准约束）

每个图形渲染前必须满足：

```yaml
constraints:

  canvas:
    margin: 0.4                    # 边距（英寸）

  nodes:
    min_width: 1.2
    max_width: 2.5
    min_height: 0.5

  spacing:
    horizontal: 0.3
    vertical: 0.25

  text:
    min_font_size: 12
    max_lines: 3

  connectors:
    avoid_nodes: true              # 连线避开节点
    avoid_crossing: true           # 连线尽量不交叉
```

---

## 14. Connector Routing & Visual Hierarchy

### 14.1 Connector Routing（连线策略）

```yaml
routing:
  strategy:
    - orthogonal                    # 直角布线（最常用）
    - direct                        # 直线（短距离）
    - curved                        # 曲线（避免锐角）

  avoid:
    - nodes                         # 绕开节点
    - labels                        # 绕开标签

  minimize:
    - crossings                     # 连线交叉数
    - bends                         # 转折数
    - length                        # 总长度
```

**反例（连线穿过节点）：**

```text
A ───────────────→ B
        C  ← 被线穿过
```

**正例（绕开 C）：**

```text
A ───────┐
         │
         └────────→ B

        C  ← 独立显示
```

**真实场景示例（PPT 渲染时常见）：**

```text
        Strategy
           │
           ↓
        Business
           │
           ↓
        Capability   ← ← ← 连线直接从 Strategy 穿透到这里，跨越了 Business
```

应该重构成：

```text
        Strategy
           │
           ↓
        Business ────────────┐
           │                │
           ↓                ↓
        Capability   ──→  Execution Layer
```

**或用 orthogonal routing：**

```text
Strategy ───┐
            │
            └──→ Execution
Business ───┘
```

### 14.2 Visual Hierarchy Engine（视觉层级引擎）

不是所有节点都应该一样大。咨询 PPT 的核心是"主次分明"——用 `importance` 字段驱动视觉：

```yaml
nodes:

  - id: strategy
    importance: 1.0                # 最高 → 大号、加粗、深色

  - id: capability
    importance: 0.7                # 中等

  - id: detail
    importance: 0.4                # 最低 → 小号、浅色
```

**importance → 视觉的映射规则：**

```text
importance (0..1)
   ↓
size          # 节点尺寸（width × height）
   ↓
font          # 字号
   ↓
weight        # 字重（regular / bold）
   ↓
visual emphasis  # 边框粗细、阴影、强调色
```

**典型咨询 PPT 的视觉层级：**

```text
核心结论（最大、最深、最粗）
   ↓
一级信息（中等、清晰可读）
   ↓
二级信息（较小、辅助说明）
   ↓
Supporting Detail（最小、最浅、说明性）
```

**反例：** 所有节点同样大小 = 没有重点 = 失去"咨询味"。

---

## 15. Visual QA 三维度

> 生成 PPT 之后，必须按下面三个维度做 QA。SKILL.md 主体已经描述了整体 QA 流程；这里专讲**图形 QA** 的具体检查项。

### 15.1 Geometry QA（几何）

- **overlap**：元素之间是否有重叠？
- **out-of-bounds**：是否超出幻灯片边界（x≥0, y≥0, x+w≤10, y+h≤5.625）？
- **collision**：节点是否互相挤压？
- **alignment**：相同层级的元素是否对齐？
- **spacing**：元素间距是否一致（0.3"-0.5"）？
- **connector crossing**：连线是否过度交叉？

### 15.2 Typography QA（排版）

- **text overflow**：文字是否溢出节点？
- **font size**：字号是否符合约束（min 12pt）？
- **line count**：每块文字是否 ≤ 3 行？
- **contrast**：文字与背景对比是否足够？

### 15.3 Diagram QA（语义）

- **orphan node**：有没有孤立的节点（没有任何边）？
- **missing connector**：声明了关系但没画线？
- **ambiguous relationship**：关系类型不清（是 causes 还是 supports？）？
- **excessive crossing**：连线交叉过多（> N 条）？
- **inconsistent hierarchy**：层级深度不一致？

**发现任何问题 → Repair → Re-render。**

```text
Generate
   ↓
Render
   ↓
Screenshot
   ↓
Vision Model（如果有）
   ↓
Detect Problems
   ↓
Repair（修几何 / 改层级 / 换模板）
   ↓
Render Again
```

---

## 16. 端到端 Pipeline 示例（AI 转型三层架构）

> 这个完整示例来自设计文档。展示从自然语言到 PPT 渲染的**全流程 5 步**。

### 16.1 输入

```text
公司 AI 转型分成三层：

战略层：AI 战略与治理

业务层：
业务场景、AI 产品、AI 能力

执行层：
Agent、自动化、数据、技术平台
```

### 16.2 Step 1 — 抽取 Semantic Graph

```yaml
nodes:
  - strategy
  - business
  - execution

edges:
  - from: strategy
    to: business
    type: enables

  - from: business
    to: execution
    type: decomposes_into
```

### 16.3 Step 2 — Router 决策

```yaml
analysis:
  hierarchy: true
  depth: 3
  relationship: hierarchical

decision:
  diagram_type: layered_architecture
```

### 16.4 Step 3 — 选 Template

```yaml
template:
  id: layered_architecture
  orientation: vertical
  alignment: center
```

### 16.5 Step 4 — Auto Layout

```yaml
layout:
  strategy:
    x: 4.0           # ← 这些坐标由 Layout Engine 计算，不是 LLM 编造
    y: 1.2
    importance: 1.0

  business:
    x: 3.0
    y: 2.7
    importance: 0.7

  execution:
    x: 2.0
    y: 4.2
    importance: 0.4
```

### 16.6 Step 5 — Render（PPT 输出预览）

```text
        ┌───────────────┐
        │    战略层      │
        │ AI 战略与治理  │
        └───────┬───────┘
                ↓
    ┌───────────────────────┐
    │       业务层           │
    │ 场景 │ AI 产品 │ 能力  │
    └───────────┬───────────┘
                ↓
┌─────────────────────────────────┐
│             执行层               │
│ Agent │ 自动化 │ 数据 │ 技术平台 │
└─────────────────────────────────┘
```

### 16.7 关键 takeaway

- **Step 1 决定一切**：节点和边错了，后面全错。
- **Step 4 不要让 LLM 编坐标**：永远交给 Layout Engine。
- **importance 决定视觉层级**：战略层最大、加粗、深色；执行层最小、浅色。
- **每个 step 都可以人工 override**：Agent 给的是默认方案，Designer 可以调整。

---

## 17. Mapping（映射 / 跨映射）

> **目的**：表达"两组实体之间的对应关系"——这是 AI 转型 / 咨询报告里**最高频**的一类图形，比传统 SmartArt 更重要。

### 17.1 适用场景

- 业务目标 → AI Use Case 的拆解
- AI 场景 → 业务流程（NPDS 流程）的覆盖
- 能力 → 部门 / 角色的归属
- 风险 → 控制措施的对应

### 17.2 One-to-Many（一对多）

```text
Business Objective
        │
        ├── Use Case A
        ├── Use Case B
        └── Use Case C
```

```yaml
type: mapping

source:
  - objective

targets:
  - use_case_a
  - use_case_b
  - use_case_c
```

### 17.3 Many-to-Many（多对多）

> **重要**：many-to-many 用 mapping，**不要**用 hub_spoke。
> 多对多关系画成 hub_spoke 会丢失"交叉关联"信息。

```text
AI Scenario
       ↕
NPDS Process
```

```yaml
type: many_to_many_mapping

left:
  - AI 场景 A
  - AI 场景 B
  - AI 场景 C

right:
  - 研发
  - 采购
  - SQE
  - 物流

relationships:
  - [A, 研发]
  - [A, SQE]
  - [B, 采购]
  - [B, 物流]
  - [C, 研发]
```

**渲染要求：** 连线由 Mapping Layout Engine 计算，**不要让 LLM 手工算 connector 坐标**——多对多的连线最乱。

### 17.4 Traceability（追溯矩阵）

横轴 = 来源，纵轴 = 目标，每个交叉点表达"是否覆盖"。常用样式：✓ / ✗ / 颜色深浅。

### 17.5 Ecosystem（生态网络）—— 与 Hub & Spoke 区分

> 如果关系不是简单的中心辐射，而是**多对多、双向**（Customer ↔ Platform ↔ Partner ↔ Agent），
> **不要用** Hub & Spoke。Hub & Spoke 会丢失"交叉关联"信息。

**ASCII 示意：**

```text
Customer
   ↕
Platform
 ↙   ↘
Partner  Agent
  ↘     ↙
    Data
```

```yaml
type: ecosystem

nodes:
  - Customer
  - Platform
  - Partner
  - Agent
  - Data

edges:
  - Customer ↔ Platform
  - Platform ↔ Partner
  - Platform ↔ Agent
  - Partner ↔ Data
  - Agent ↔ Data
```

**Router 自动选择：**

```text
many-to-many
+
network relationship

→ ecosystem / network diagram
```

**与 Hub & Spoke 的对比：**

| 维度 | Hub & Spoke | Ecosystem |
|---|---|---|
| 中心 | 明确（hub） | 无中心（任意节点可作中心） |
| 关系方向 | 单向 / 中心向外 | 多向 / 双向 |
| 节点数 | 中心 1 + spoke 3-8 | 任意（≥4） |
| spoke 间关系 | 无 | 任意两节点都可连 |
| 适合 | "以 X 为核心的能力图" | "X / Y / Z 之间的协作网络" |

---

## 18. 咨询模板库（Diagram Templates）

> **目的**：模板不是简单的"样式"，而是**结构 + 约束 + 渲染规则**的完整封装。
> 命中模板 → 直接出图；不命中 → 降级到通用结构。

### 18.1 Strategy House（战略屋）

```yaml
template:
  id: strategy_house

  semantic_purpose:
    - strategy alignment        # 战略对齐
    - strategic architecture    # 战略架构

  structure:
    roof: Vision               # 屋顶：愿景
    pillars: Strategic Pillars # 支柱：战略支柱（通常 3-5 根）
    foundation: Capabilities   # 地基：能力

  layout:
    type: symmetric            # 对称布局
    alignment: center

  constraints:
    max_pillars: 5             # 支柱上限（太多会糊）
```

### 18.2 Capability Map（能力地图）

```yaml
template:
  id: capability_map

  structure:
    level_1: strategic_capability   # 战略能力
    level_2: business_capability    # 业务能力
    level_3: enabling_capability    # 使能能力

  layout:
    type: layered_grid              # 分层网格

  constraints:
    max_columns: 5
    max_rows: 4
```

**Level 示例（来自 AI 转型）：**

```yaml
nodes:
  - name: AI 战略
    level: 1
    importance: 1.0

  - name: 数据能力
    level: 2
    importance: 0.7

  - name: AI 平台
    level: 2
    importance: 0.7

  - name: Agent 能力
    level: 2
    importance: 0.7

  - name: 智能营销
    level: 3
    importance: 0.4
```

Engine 自动布局：

```text
             AI 战略
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
     数据     AI 平台    Agent
       │        │        │
       └────────┼────────┘
                ↓
            AI 应用
```

### 18.3 Issue Tree（问题树）

```yaml
template:
  id: issue_tree

  structure:
    root: problem                     # 根节点：核心问题
    branches: mutually_exclusive_categories  # 分支：MECE 分类
    leaves: root_causes               # 叶子：根因

  layout:
    type: hierarchical_tree

  constraints:
    max_depth: 4                      # 深度上限
    branches_per_node: 3-5            # 每层分支数
```

### 18.4 Transformation Architecture（转型架构）

```yaml
template:
  id: transformation_architecture

  semantic_purpose:
    - as_is_to_be                     # 现状到目标
    - transformation_roadmap          # 转型路径

  structure:
    left: current_state               # 左：现状
    center: gap                       # 中：差距
    right: target_state               # 右：目标
    bottom: initiatives               # 下：举措
    timeline: roadmap                 # 时间线

  layout:
    type: hybrid                      # 混合布局

  constraints:
    max_initiatives: 8                # 举措上限
```

### 18.5 AI Transformation Map（AI 转型图）

```yaml
template:
  id: ai_transformation_map

  semantic_purpose:
    - ai_value_chain                  # AI 价值链

  structure:
    level_1: business_objective       # 业务目标
    level_2: business_scenario        # 业务场景
    level_3: ai_use_case              # AI 用例
    level_4: ai_capability            # AI 能力
    level_5: ai_agent                 # AI Agent
    level_6: business_value           # 业务价值

  layout:
    type: layered_flow                # 分层流向

  constraints:
    max_use_cases: 12                 # 用例上限（多了就拆页）
```

### 18.6 使用流程

```text
1. 看文本属于 §11 的哪种 Consulting Pattern
   ↓
2. 查本节找到对应 Template（如 Strategy → strategy_house）
   ↓
3. 把节点数据填进 template.data_schema
   ↓
4. Template 给出 structure + layout + constraints
   ↓
5. Auto Layout 出坐标
   ↓
6. Render 输出
```

**关键：** Template 是"半成品"——它把结构定死了，但数据由 Agent 从原文抽取填进去。

---

## 19. 完整 Diagram Primitives 索引

> 这是一张**全量索引表**，把 §1-§17 的所有图形按"图形分类 → 具体图形"梳理成一颗树。
> 方便 Agent 快速定位"我现在想画的那种东西叫什么"。

```text
Hierarchy          →  Pyramid, Org Chart, Tree, Layered Architecture, Nested Structure
Process            →  Linear, Chevron, Funnel, Pipeline, Stage Gate
Relationship       →  Hub & Spoke, Network, Dependency Map, Ecosystem, Many-to-Many
Cycle              →  Circular, Continuous, PDCA, Flywheel, Lifecycle, Feedback Loop, Closed Loop
Comparison         →  Before/After, Current/Future, As-Is/To-Be, Traditional/New, Option A/B, Good/Better, Gap
Matrix             →  2×2, 3×3, Priority, Impact/Effort, Value/Complexity, Risk, Maturity, Capability, Heatmap
Framework          →  3-Layer, 4-Pillar, 5-Dimension, House, Pyramid, Capability Map, Operating Model, Canvas
Strategy           →  Strategy House, Strategy Pyramid, 3 Horizons, North Star, Vision→Strategy→Execution
Architecture       →  Layered, Stack, Platform, Operating, Capability, Business, Technology, Hub-and-Spoke, Modular
Mapping            →  One-to-One, One-to-Many, Many-to-Many, Traceability
Roadmap            →  Timeline, Swimlane, Horizon (Now/Next/Later), Wave, Milestone
```

**使用方式：** 拿到一节内容，先在脑子里过一遍这棵树——它属于哪一类？然后到对应章节查细节。

---

## 选择流程（5 步决策）

1. **识别节点（Entities）**：哪些是核心概念？
2. **识别关系（Relationships）**：节点之间的关系是 Hierarchy / Process / Cycle / Comparison / Matrix 中的哪一种？
3. **查表选图形**：在上面对应章节挑出最匹配的类型。
4. **决定样式**：根据关系语义选 connector（粗/细/虚/双向）。
5. **落到代码**：参照 SKILL.md 主体的「## 对于每张幻灯片」用 pptxgenjs 实现。

## Diagram Generation Rules（写入 Agent 心智）

1. **永远先识别语义结构，再画图。** 没有"画一个漂亮的图"这种事——只有"画一个表达 X 语义的图"。
2. **优先使用模板**：Semantic structure 一旦匹配已知模板，就用模板，不要让 LLM 算坐标。
3. **节点太多 = 拆页 / 聚合 / 简化**：单图节点 ≤ 7 是黄金法则，超过就要重组。
4. **关系线要编码语义**：causes ≠ depends_on ≠ maps_to，视觉上必须可区分。
5. **避免过度装饰**：阴影、3D、渐变——能不加就不加。语义清晰 > 美观。
6. **永远不要让 LLM 手算坐标**：让 Auto Layout 算法处理位置/对齐/避让。
7. **生成后跑 Visual QA**：overlap / overflow / connector crossing / text overflow。
8. **优先级**：语义清晰 > 可读性 > 对齐 > 美观 > 装饰。
