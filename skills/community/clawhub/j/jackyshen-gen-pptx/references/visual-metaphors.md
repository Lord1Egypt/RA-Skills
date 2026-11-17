# 咨询视觉隐喻库（Consulting Visual Metaphor Library / 叙事型智能图形）

> **核心洞察**：咨询 PPT 的"高级感"不是来自更复杂的图形，而是来自**图形本身与叙事意图一致**。
> 同样的 `A → B → C → D`：
> - 画成 Linear Process → 强调**流程**
> - 画成 Staircase → 强调**升级**
> - 画成 Wave → 强调**曲折前进**
> - 画成 Mountain → 强调**挑战与突破**
> - 画成 Growth Curve → 强调**增长**
>
> Agent 不应"图漂亮就选"。应先识别**叙事意图 + 情绪方向**，再选图形。

---

## 相关文件与依赖关系

> **本文件定位**：隐喻维度（emotion）——读者应该感受到什么？

| 文件 | 关系 | 何时查阅 |
|---|---|---|
| [SKILL.md](../SKILL.md) | 上游入口 | 整个生成流程的入口、配色 / 字体 / QA 规则 |
| [slide-layouts.md](slide-layouts.md) | 正交维度 | 单页怎么分块（与本页正交，不冲突） |
| [diagrams.md](diagrams.md) | **主从张力**（结构维度）——本文件多数章节的"地基" | 当这页是**结构主导**（清晰的层级 / 流程 / 矩阵）时 |
| [优普丰品牌设计配色方案.md](优普丰品牌设计配色方案.md) | 下游（视觉层） | 选好隐喻后用什么颜色 / 字体传达情绪 |

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
diagrams.md    visual-metaphors.md    ← 本文件
(结构维度)     (隐喻维度)
   │            │
   └─────┬──────┘
         ↓
   pptxgenjs 渲染
         ↓
   视觉 QA
```

### 关键交叉点（在本文件中的位置）

- §32 Visual Emotional Direction → visual_intent schema 包含 `relation_to_base_structure` 字段（兼容 vs 覆盖）
- §33 Selection Rules → 把语义映射到推荐隐喻（与 diagrams.md §12 Router Rules 互补）
- 文件末尾"## 与 diagrams.md 的关系（主从张力模型）" → 与结构维度文件的完整关系说明

### 与 diagrams.md 的引用约定

本文件讲**隐喻**（叙事 + 情绪），diagrams.md 讲**结构**（拓扑 + 关系）。两者关系详见本文件末尾的"## 与 diagrams.md 的关系（主从张力模型）"。

> **本文件不教怎么画 Pyramid / Matrix，那些是 `diagrams.md` 的事。**

---


## 目录

| § | 隐喻 | § | 隐喻 |
|---|---|---|---|
| §1 | [Staircase（阶梯图）](#1-staircase阶梯图) | §17 | [Tree（树）](#17-tree树) |
| §2 | [Wave Timeline（波浪线）](#2-wave-timeline波浪线) | §18 | [Root System（根系）](#18-root-system根系) |
| §3 | [Growth Curve（上升曲线）](#3-growth-curve上升曲线) | §19 | [Foundation Blocks（基础块）](#19-foundation-blocks基础块) |
| §4 | [S-Curve（技术成熟曲线）](#4-s-curve技术成熟曲线) | §20 | [Waterfall Journey（瀑布叙事）](#20-waterfall-journey瀑布叙事) |
| §5 | [Mountain Journey（山峰图）](#5-mountain-journey山峰图) | §21 | [Wave + Staircase Hybrid（波浪阶梯混合）](#21-wave--staircase-hybrid) |
| §6 | [Bridge（桥梁图）](#6-bridge桥梁图) | §22 | [Breaking Wall（突破墙）](#22-breaking-wall突破墙) |
| §7 | [Gap Jump（跨越鸿沟）](#7-gap-jump跨越鸿沟) | §23 | [Gateway（门）](#23-gateway门) |
| §8 | [Rocket（火箭）](#8-rocket火箭) | §24 | [Zoom-in（放大镜）](#24-zoom-in放大镜) |
| §9 | [Flywheel（飞轮）](#9-flywheel飞轮) | §25 | [Spotlight（聚光灯）](#25-spotlight聚光灯) |
| §10 | [Funnel（漏斗）](#10-funnel漏斗) | §26 | [Focus Funnel（聚焦漏斗）](#26-focus-funnel聚焦漏斗) |
| §11 | [Pyramid（金字塔）](#11-pyramid金字塔) | §27 | [Bridge + Roadmap Hybrid（桥梁+路线图）](#27-bridge--roadmap-hybrid) |
| §12 | [Iceberg（冰山图）](#12-iceberg冰山图) | §28 | [Railway（轨道）](#28-railway轨道) |
| §13 | [Onion（洋葱图）](#13-onion洋葱图) | §29 | [Convergence（合流）](#29-convergence合流) |
| §14 | [Hexagon Network（蜂巢）](#14-hexagon-network蜂巢) | §30 | [Divergence（分叉）](#30-divergence分叉) |
| §15 | [Gear（齿轮图）](#15-gear齿轮图) | §31 | [Convergence + Divergence Combined（汇聚+分叉）](#31-convergence--divergence-combined) |
| §16 | [Puzzle（拼图）](#16-puzzle拼图) | §32 | [Visual Emotional Direction（视觉情绪方向）](#32-visual-emotional-direction视觉情绪方向) |
| | | §33 | [Visual Metaphor Selection Rules](#33-visual-metaphor-selection-rules) |

---

## 1. Staircase（阶梯图）

### 核心语义

```text
Level 1
   ↗
Level 2
      ↗
Level 3
         ↗
Level 4
```

同时表达：**层次 + 能力提升 + 成熟度 + 进阶 + 升级 + 突破**。

### 常见变体

- 3-Step Staircase
- 5-Step Staircase
- Capability Maturity Staircase
- Transformation Staircase

### 典型表达

```text
基础能力
    ↓
标准化
    ↓
数字化
    ↓
智能化
    ↓
AI-Native
```

### Agent Rule

```yaml
if:
  semantic:
    - progression
    - maturity
    - capability_upgrade
    - level
then:
  graphic: staircase
```

---

## 2. Wave Timeline（波浪线）

### 核心语义

```text
             ●
            / \
     ●     /   \        ●
    / \___/     \______/
___/
```

峰谷上放置事件：

```text
       Milestone B
            ●
           / \
          /   \
  A ●____/     \____● C
```

同时表达：**时间推进 + 项目历程 + 波动 + 挑战 + 阶段性成果 + 曲折前进 + 最终突破**。

### 特别适合

- 项目大事记 / 企业发展历程
- Transformation Journey
- 产品演进 / 技术发展 / 战略演进

### Agent Rule

```yaml
if:
  semantic:
    - timeline
    - journey
    - milestone
  emotional_context:
    - challenge
    - ups_and_downs
    - transformation
then:
  graphic: wave_timeline
```

---

## 3. Growth Curve（上升曲线）

**和 Wave Timeline 不同：**
- 波浪线强调**经历波折**
- Growth Curve 强调**总体持续增长**

```text
Value
  │
  │                  ●
  │             ●
  │         ●
  │      ●
  │   ●
  │ ●
  └──────────────────── Time
```

适用于：收益增长 / 能力成熟 / Adoption / AI 渗透率 / Productivity / Business Value。

### 常见变体

- Linear Growth
- Exponential Growth
- S-Curve
- J-Curve
- Learning Curve
- Adoption Curve

---

## 4. S-Curve（技术成熟曲线）

特别适合咨询报告。

```text
Value
 │
 │                     ______
 │                  __/
 │               __/
 │            __/
 │        ___/
 │____ ___/
 └──────────────────────── Time
```

### 表达

```text
探索
 ↓
快速增长
 ↓
成熟
 ↓
平台期
```

### 特别适合

- Technology Adoption
- Digital Transformation
- AI Adoption
- Capability Maturity
- Product Lifecycle

---

## 5. Mountain Journey（山峰图）

咨询 PPT 非常喜欢的一类。

```text
                         ★ Target
                        /\
                       /  \
             /\       /    \
            /  \_____/      \
___________/                \____
     Challenge      Breakthrough
```

### 表达

> 从当前位置出发 → 经历挑战 → 攀登 → 达到目标。

适合：Transformation Journey / 战略目标 / 企业转型 / Capability Building / Change Journey。

特别适合标题：**"From Current State to Future State"**。

---

## 6. Bridge（桥梁图）

视觉隐喻非常强。

```text
Current State                  Future State
     │                              │
     │                              │
─────┴──────────────┬───────────────┴─────
                    │
                 Bridge
             Transformation
```

### 表达

```text
AS-IS
  ↓
Gap
  ↓
Initiatives
  ↓
TO-BE
```

非常适合：Transformation / Gap Analysis / Capability Building / Digital Transformation / AI Transformation。

可以把桥上的每一段写成：

```text
Governance
Data
Technology
Process
People
```

---

## 7. Gap Jump（跨越鸿沟）

和 Bridge 类似，但语义更强调：**需要跨越一个巨大差距**。

```text
Current                    Future
   ●                         ●
  / \                       / \
 /   \                     /   \
───────\                 /───────
        \               /
         \_____GAP_____/
```

适合：Capability Gap / Performance Gap / Digital Gap / Current vs Target / Benchmark Gap。

### 与 Bridge 的区别

| 图形 | 语义 |
|---|---|
| **Bridge** | 有路径、有方法 |
| **Gap Jump** | 差距很大，需要突破 |

---

## 8. Rocket（火箭）

视觉隐喻：**加速、突破、起飞**。

```text
             🚀
             ↑
             │
          AI Scale
             │
        Digital
             │
       Foundation
```

咨询报告中不一定真的画火箭，而可以做成：

```text
        ▲
       / \
      /   \
     / AI  \
    / Scale \
   /─────────\
  / Foundation\
```

适合：Growth / Acceleration / AI Transformation / Digital Transformation / Scaling。

---

## 9. Flywheel（飞轮）

表达：**能力之间相互促进，形成自增强循环**。

```text
       Data
        ↓
    AI Capability
        ↓
    Better Product
        ↓
    More Users
        ↓
       Data
        ↺
```

或者：

```text
        ┌───────────┐
        ↓           │
      Data → AI → Value
        ↑           ↓
        └── Adoption
```

特别适合：AI Flywheel / Data Flywheel / Platform Strategy / Growth Loop / Continuous Improvement。

### 与普通 Cycle 的区别

- **Cycle** = 循环
- **Flywheel** = 循环**产生加速度**

---

## 10. Funnel（漏斗）

```text
████████████████████
       Opportunities
     ██████████████
        Use Cases
       ██████████
          POC
        ██████
         Pilot
        ████
         Scale
```

表达：**大量输入 → 筛选 → 聚焦 → 少量重点**。

适合：Opportunity → Priority / Innovation Pipeline / AI Use Case Selection / Sales Funnel / Talent Pipeline。

---

## 11. Pyramid（金字塔）

**和阶梯不同：**
- 阶梯强调**逐步上升**
- 金字塔强调**层级 / 权重 / 基础**

```text
           Strategy
        ─────────────
          Business
      ────────────────
         Capability
    ───────────────────
      Foundation
```

特别适合：Strategy / Operating Model / Capability Model / Management System。

---

## 12. Iceberg（冰山图）

非常适合咨询里的：**表象问题 vs 深层原因**。

```text
             Visible
──────────────────────── Water
             Symptoms

             ↓

        Processes
        Structure
        Incentives
        Culture
        Technology

             ↓

         Root Causes
```

### 典型表达

```text
Visible Problems
        ↓
Hidden Causes
        ↓
Systemic Issues
```

适合：Root Cause / Organizational Issues / Culture / Customer Experience / Management Problems。

---

## 13. Onion（洋葱图）

```text
┌────────────────────────┐
│       Ecosystem        │
│  ┌──────────────────┐  │
│  │    Enterprise    │  │
│  │  ┌────────────┐  │  │
│  │  │ Business   │  │  │
│  │  │ ┌────────┐ │  │  │
│  │  │ │ Core   │ │  │  │
│  │  │ └────────┘ │  │  │
│  │  └────────────┘  │  │
│  └──────────────────┘  │
└────────────────────────┘
```

### 表达

核心 → 外围 / 内部 → 外部 / 战略层级 / 影响范围 / Scope。

适合：Operating Model / Ecosystem / Stakeholder / Product Architecture / AI Architecture。

---

## 14. Hexagon Network（蜂巢）

```text
   ⬡──⬡──⬡
  / \ / \ /
 ⬡──⬡──⬡
  \ / \ /
   ⬡──⬡
```

表达：**多个能力模块相互连接，共同形成系统**。

特别适合：Capability Model / AI Capability / Operating Model / Digital Architecture / Organizational Capability。

**优点：** 比普通 Card Grid 更有"系统性"。

---

## 15. Gear（齿轮图）

```text
      ⚙ Strategy
          ↘
       ⚙ Process
          ↘
       ⚙ People
          ↘
       ⚙ Technology
```

### 核心隐喻

> 各部分相互咬合，任何一个环节都会影响整体。

适合：Operating Model / Transformation / Organizational System / Management System。

### ⚠️ 警告

**不要为了"看起来专业"而滥用齿轮**。如果元素之间没有真实的相互依赖，就不应该用。

---

## 16. Puzzle（拼图）

```text
┌────┬────┐
│    │    ├──┐
│ A  │ B  │  │
├────┤    │ C│
│ D  │    ├──┘
└────┴────┘
```

### 隐喻

> 多个部分共同构成完整解决方案。

适合：Transformation Components / Capability Building / Strategy Components / Solution Architecture。

### 关键区分

它表达的是**组合**，**而不是因果关系**。

---

## 17. Tree（树）

```text
                Objective
                   │
          ┌────────┼────────┐
          ↓        ↓        ↓
        Pillar   Pillar   Pillar
          │
      ┌───┼───┐
      ↓   ↓   ↓
     A    B    C
```

### 核心特点

> 从一个整体逐渐分解成多个部分。

特别适合：Issue Tree / Objective Tree / Strategy Decomposition / Capability Decomposition / Work Breakdown。

---

## 18. Root System（根系）

Tree 的反向变体。

```text
             Business Value
                  │
──────────────────┼──────────────────
        Process / Capability
                  │
          ┌───────┼───────┐
          │       │       │
        Data    People  Technology
          │       │       │
       ───┴───────┴───────┴───
              Foundation
```

或者画成"树根"：

```text
             Results
                │
                │
               / \
              /   \
             /     \
          ──/───────\──
           / \     / \
          /   \   /   \
        Data People Tech
```

### 隐喻

> 表面的成果来自深层能力基础。

适合：Business Results → Capabilities / AI Value → Data / Technology / People / Organizational Performance / Transformation Foundation。

---

## 19. Foundation Blocks（基础块）

```text
       Business Value
    ───────────────────
      AI Applications
    ───────────────────
 Data │ People │ Process │ Tech
```

比 Pyramid 更强调**底层支撑关系**。

适合：AI Foundation / Digital Foundation / Operating Model / Enterprise Architecture。

---

## 20. Waterfall Journey（瀑布叙事）

不是财务 Waterfall Chart，而是叙事型瀑布。

```text
Start
████████
       ██████
             █████
                  ███
                     █
                    Target
```

表达：**一步一步向下 / 向前传递**。

也可以反过来：

```text
Challenge
   ↓
Action
   ↓
Result
   ↓
Impact
```

适合：Initiative → Outcome / Problem → Action → Result / Transformation Impact / Project Evolution。

---

## 21. Wave + Staircase Hybrid

既表达**过程有波折**，又表达**总体持续升级**。

```text
Level 5                         ───────●
                              /
Level 4              ────────●
                         /
Level 3          ─────●
                   /
Level 2      ────●
             /
Level 1 ───●
```

或者：

```text
        ●───────
       /        \
──────●          ●───────
                         \
                          ●────── Target
```

适合：Transformation Journey / Agile Maturity / AI Adoption / Organizational Evolution。

---

## 22. Breaking Wall（突破墙）

表达：**当前存在障碍 → 通过关键举措实现突破**。

```text
Current
   │
   │       ███████████
   │       █  Barrier █
   │       ███████████
   │              ✕
   │             /
   │            /
   └───────────●────────→ Future
             Breakthrough
```

适合：Transformation Barrier / Bottleneck / Change Management / Critical Initiative。

---

## 23. Gateway（门）

表达：**通过某个关键条件，才能进入下一阶段**。

```text
Stage 1
   │
   ↓
┌───────────┐
│   Gate    │
│ Governance│
└─────┬─────┘
      ↓
Stage 2
```

适合：Stage Gate / Governance / Compliance / Approval / Maturity Transition。

---

## 24. Zoom-in（放大镜）

特别适合咨询报告的**从宏观 → 局部深入**。

```text
Enterprise
    │
    └──────────────┐
                   ↓
              Business
                   │
                   ↓
                Process
                   │
                   ↓
                Detail
```

或者：

```text
Overview
   ↓
Domain
   ↓
Process
   ↓
Use Case
```

适合：Executive → Detail / Strategy → Execution / Business → Process / Process → AI Use Case。

---

## 25. Spotlight（聚光灯）

表达：**在大量信息中识别重点**。

```text
○ ○ ○ ○ ○ ○ ○ ○
○ ○ ★ ○ ○ ○ ○ ○
○ ○ ○ ○ ○ ○ ○ ○
```

适合：Key Finding / Priority / Focus Area / Quick Win / Critical Issue。

---

## 26. Focus Funnel（聚焦漏斗）

比普通 Funnel 更适合咨询。

```text
100+ Opportunities
        ↓
  30 AI Scenarios
        ↓
   10 Priorities
        ↓
    5 POCs
        ↓
   2 Scale-ups
```

它同时表达：**规模缩小 + 注意力集中**。

---

## 27. Bridge + Roadmap Hybrid

用于非常典型的 Transformation Slide：

```text
CURRENT                              TARGET
  ●                                    ●
   \                                  /
    \________ Transformation ________/
       │       │       │       │
      Data   Process  People  AI
```

这里：
- **Bridge** = Gap
- **Bridge Segments** = Initiatives
- **Start** = Current
- **End** = Target

---

## 28. Railway（轨道）

```text
══════════════════════════════════════
     ●          ●          ●
    Gate       Gate       Gate
══════════════════════════════════════
```

两条平行线表达：**多个工作流沿着同一个方向共同推进**。

适合：Transformation Roadmap / Parallel Workstreams / Program Management / Product Development。

例如：

```text
Business ───●──────●────────●──────
Data     ─────●────●──────────●────
Technology ──●────────●───────●────
             P1     P2       P3
```

---

## 29. Convergence（合流）

多个输入最终汇聚成一个结果：

```text
Strategy ──────┐
Data ──────────┤
People ────────┼────→ AI Transformation
Technology ────┤
Process ───────┘
```

表达：**多种能力 / 条件共同形成一个结果**。

适合：Capability → Outcome / Multiple Inputs → One Strategy / Cross-functional Collaboration / AI Value Creation。

---

## 30. Divergence（分叉）

反过来：

```text
                 ┌→ Product
                 │
Strategy ────────┼→ Process
                 │
                 └→ Capability
```

表达：**一个战略 / 决策向多个方向展开**。

适合：Strategy Decomposition / Product Portfolio / Strategic Initiatives / Business Model。

---

## 31. Convergence + Divergence Combined（汇聚+分叉）

咨询报告里非常常见：

```text
                ┌→ Business
                │
Data ───────────┼→ Product
                │
                └→ AI

                     ↓

                  Value
```

更复杂的时候：

```text
Inputs
  ↓
Convergence
  ↓
Core Capability
  ↓
Divergence
 ↙ ↓ ↘
A  B  C
```

表达：**多种能力汇聚形成核心能力，再向多个业务方向释放价值**。

---

## 32. Visual Emotional Direction（视觉情绪方向）

> **这一节是整个隐喻库的核心洞察**。
>
> 同样的 `A → B → C → D`，画法不同，叙事意图也不同——但**不是所有画法都和原结构兼容**。

### 5 种不同的情绪方向（按"是否覆盖原结构"分组）

#### A. 结构兼容型（保留线性格局）

```text
Linear Process
A → B → C → D
```
**强调：** 流程 / 顺序
**结构：** 线性 A→B→C→D 保留

```text
Staircase
A
 └─ B
     └─ C
         └─ D
```
**强调：** 升级
**结构：** 线性 A→B→C→D 保留，加"↗"方向感

#### B. 结构替换型（隐喻覆盖原线性格局）

```text
Wave
      B        D
     / \      / \
A───/   \────/   \───
```
**强调：** 曲折前进
**结构：** 线性 A→B→C→D 被**替换成折线 / 波浪**

```text
Mountain
        D
       /\
      /  \
  B  /    \
 /\/       \
A           C
```
**强调：** 挑战与突破
**结构：** 线性 A→B→C→D 被**替换成山峰 / 攀登路径**

```text
Growth Curve
             D
          /
       C
     /
   B
 /
A
```
**强调：** 增长
**结构：** 线性 A→B→C→D 被**替换成曲线**

### 关键区分：兼容 vs 覆盖

| 隐喻 | 与原结构关系 | 何时选用 |
|---|---|---|
| **Linear Process** | ✅ 兼容 | 默认；强调流程本身 |
| **Staircase** | ✅ 兼容 | 强调"升级"，但仍要保留层级感 |
| **Wave Timeline** | ❌ 覆盖 | 强调"曲折前进"，愿意放弃线性格局 |
| **Mountain** | ❌ 覆盖 | 强调"挑战与突破"，愿意放弃线性格局 |
| **Growth Curve** | ❌ 覆盖 | 强调"长期增长"，愿意放弃线性格局 |

**这就是"主从张力"的体现：**

- 想保留原结构 → 选**兼容隐喻**
- 情绪优先于结构 → 选**覆盖隐喻**（隐喻主导，结构被重新定义）

### visual_intent 字段（加入 Router Schema）

```yaml
visual_intent:
  structural: "progression"          # progression / comparison / causation / cycle / mapping
  directional: "upward"              # upward / downward / horizontal / radial / zigzag
  emotional: "positive"              # positive / neutral / challenging
  narrative: "overcoming_challenges" # overcoming_challenges / breakthrough / growth / journey
  relation_to_base_structure: "compatible"  # compatible | overriding  ← 关键字段
```

### 完整 Router 输出示例

不是这种浅层判断：

```text
"这是一个 timeline"
```

而是这种结构化判断：

```yaml
semantic:
  primary: timeline
  secondary: progression
  narrative: journey

visual_intent:
  direction: upward
  emotion: positive
  volatility: medium
  ending: achievement
  relation_to_base_structure: overriding  # 隐喻会覆盖线性格局

selected_graphic:
  type: wave_timeline
  variant: upward_wave
```

**这一步非常关键。** 咨询公司 PPT 的"高级感"很多时候并不是来自更复杂的图形，而是来自**图形本身和叙事意图一致**。Agent 如果能理解这一层，就不会把所有内容都机械地画成矩形 + 箭头了。

### ⚠️ 反模式警告

**不要因为"想突出情绪"就滥用覆盖型隐喻。** 如果客户实际想要的是清晰的层级结构（结构主导），强行画 Mountain 会让信息丢失。

判断标准：

- **结构主导**（客户要的是"看清层级 / 流程 / 关系"）→ 用 Staircase / Funnel 等**兼容隐喻**
- **隐喻主导**（客户要的是"感受转型 / 突破 / 增长"）→ 才用 Mountain / Wave / Growth Curve 等**覆盖隐喻**

## 33. Visual Metaphor Selection Rules

> Agent 不应因为"这个图漂亮"就选择它。应该按照语义选择。

| Semantic | Recommended Graphic |
|---|---|
| 层次 | Pyramid / Staircase |
| 能力成熟 | Staircase / Maturity Ladder |
| 时间推进 | Timeline |
| 曲折历程 | Wave Timeline |
| 持续增长 | Growth Curve |
| 快速增长 | J-Curve / Exponential |
| 技术成熟 | S-Curve |
| 挑战 → 目标 | Mountain |
| Gap | Bridge / Gap Jump |
| 突破 | Breaking Wall |
| 多能力支撑 | Foundation / Root |
| 多模块协同 | Gear / Hexagon |
| 组成整体 | Puzzle |
| 核心 → 周边 | Hub & Spoke |
| 多方互联 | Ecosystem / Network |
| 循环 | Cycle |
| 自增强循环 | Flywheel |
| 大量 → 少量 | Funnel |
| 聚焦重点 | Spotlight |
| 多个输入 → 一个结果 | Convergence |
| 一个战略 → 多个方向 | Divergence |
| 从宏观 → 微观 | Zoom-in |
| 当前 → 未来 | Bridge / Roadmap |
| 多工作流并行 | Railway / Swimlane |
| 逐步升级 | Staircase |
| 阶段演进 | Wave + Staircase |
| 深层原因 | Iceberg / Root |
| Scope 层级 | Onion / Concentric Circles |
| 关键节点 | Milestone / Gate |

### Agent System Prompt（可直接复制）

```md
## Visual Metaphor Selection

Do not select a diagram based on aesthetics alone.

First identify the semantic intent.

If the information expresses:

- hierarchy → use Pyramid, Tree, or Layered Architecture
- progression → use Staircase or Maturity Ladder
- journey with fluctuations → use Wave Timeline
- continuous growth → use Growth Curve
- maturity over time → use S-Curve
- challenge and aspiration → use Mountain Journey
- current-to-target transformation → use Bridge
- significant capability gap → use Gap Jump
- breakthrough → use Breaking Wall
- reinforcing loop → use Flywheel
- simple repetition → use Cycle
- many possibilities narrowed to a few → use Funnel
- multiple inputs producing one outcome → use Convergence
- one strategy producing multiple initiatives → use Divergence
- multiple interdependent actors → use Ecosystem / Network
- hidden root causes → use Iceberg / Root System
- multiple layers of scope → use Onion / Concentric Circles
- multiple capabilities working together → use Hexagon / Gear
- multiple components forming a whole → use Puzzle
- parallel workstreams → use Railway / Swimlane
- macro-to-micro decomposition → use Zoom-in
- focus among many items → use Spotlight
```

---

## 与 diagrams.md 的关系（主从张力模型）

**核心结论：** 两个文件**不**是 layer 关系（上下层），**也不**是完全正交（独立）。它们是**主从张力**——看"这页是结构主导还是隐喻主导"。

### 两个维度

| 文件 | 关心 | 关键词 |
|---|---|---|
| `diagrams.md`（结构维度 / topology） | 信息是什么拓扑？（层级 / 流程 / 矩阵 / 网络 / 多对多） | 节点 / 边 / 关系类型 / 布局算法 |
| `visual-metaphors.md`（隐喻维度 / emotion） | 读者应该感受到什么？（升级 / 曲折 / 突破 / 增长 / 聚焦） | 叙事意图 / 情绪方向 / 视觉隐喻 |

### 何时走哪条路径？

| 这页要传达的是… | 主从 | 路径 |
|---|---|---|
| 清晰的层级 / 流程 / 关系 / 矩阵 | **结构主导** | 查 `diagrams.md` 选对应几何图形（如 Pyramid / Matrix / Hub-Spoke） |
| 转型 / 升级 / 突破 / 增长等情绪 | **隐喻主导** | 查 `visual-metaphors.md` 选对应隐喻（隐喻会**覆盖**结构） |
| 两者都重要 | **两者都用** | `diagrams.md` 选结构 → `visual-metaphors.md` 选**兼容隐喻**（如 Staircase ≈ Pyramid）或**覆盖隐喻**（如 Wave 替代 Pyramid） |

### 隐喻 vs 结构的两种交互方式

**兼容（compatible）**：隐喻在原结构基础上加情绪方向，结构不破坏。

- Staircase ≈ Pyramid（保留层级，加"↗ 升级"方向感）
- Funnel ≈ Funnel（保留漏斗形态，加"筛选"叙事）
- Cycle ≈ Cycle（保留环形，加"持续"含义）
- Tree ≈ Tree（保留分解结构）
- Focus Funnel ≈ Funnel（加数量标签）

**覆盖（overriding）**：隐喻重新定义结构，几何形态完全改变。

- Wave Timeline → 折线（替代线性 / 层级结构）
- Mountain → 山峰 + 攀登路径（替代线性 / 层级结构）
- Bridge → 横向跨度（替代金字塔 / 树）
- Growth Curve → 曲线（替代线性 / 层级结构）
- Rocket → 垂直向上 + 火焰（替代层级结构）
- Iceberg → 水面上下分层（保留分层但语意反转）

### 决策流程（实操版）

1. **抽语义**：从原文找 Entity / Relationship / Problem / Target（见 `diagrams.md` §10）
2. **判断主从**：
   - 客户问"组织架构是什么？" → **结构主导** → 走 `diagrams.md`
   - 客户问"我们如何完成这次转型？" → **隐喻主导** → 走 `visual-metaphors.md`
3. **选图形**：
   - 结构主导 → 在 `diagrams.md` §1-§8 找匹配的几何图形
   - 隐喻主导 → 在 `visual-metaphors.md` §1-§31 找对应的隐喻（接受结构被覆盖）
4. **Router 输出**：填 `visual_intent` 字段（见 §32），必须含 `relation_to_base_structure: compatible | overriding`

### 完整例子（AI 转型 3 层）

> 内容："AI 转型分 3 层：战略 → 业务 → 执行"

**3 条路径产出完全不同的视觉：**

| 路径 | 主导 | 视觉 | 适合场景 |
|---|---|---|---|
| Plain Pyramid | 结构 | 3 层金字塔（中性、清晰） | 架构汇报、组织介绍 |
| Staircase | 结构 + 兼容隐喻 | 阶梯上升（保留层级、加升级感） | 能力成熟度、阶段路径 |
| Mountain / Wave / Growth Curve | 隐喻覆盖 | 山峰 / 折线 / 曲线（情绪强烈，结构被重新定义） | 转型故事、长期价值 |

**问的不是"哪个好看"——是"这页要让读者带走的是结构清晰度，还是情绪方向？"**
