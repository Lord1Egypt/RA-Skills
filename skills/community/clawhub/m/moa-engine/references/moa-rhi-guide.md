# RHI 递归式 Harness 自我改进指南 (v2.1 适配版)

## 目录

- [RHI 概述](#rhi-概述)
- [核心组件：Harness 的四个维度](#核心组件harness-的四个维度)
- [进化循环](#进化循环)
- [三层安全权限架构](#三层安全权限架构)
- [多目标适应度函数](#多目标适应度函数)
- [三个补强机制](#三个补强机制)
- [Patch 格式规范](#patch-格式规范)
- [门控回滚与熔断机制](#门控回滚与熔断机制)
- [实施路线图](#实施路线图)

## RHI 概述

### 什么是 RHI

RHI（Recursive Harness Self-Improvement，递归式 Harness 自我改进）是一种**不更新模型权重、只修改智能体协作方式**的自我进化机制。

**核心思想**：将 MoA 系统的 Harness（包含角色定义、通信契约、工作流步骤）表示成一段可以反复修改的文本规范，由一个高阶的"改进智能体"像改代码一样修改这段文本。通过"执行→评估→修改→合并"的递归循环，让系统自主优化其协作方式。

### 为什么需要 RHI

传统 MoA 系统面临三个根本问题：

| 问题 | 传统做法 | RHI 做法 |
|------|---------|---------|
| Harness 是静态的，不能随任务自适应 | 人工反复修改 Prompt | 系统自主修改 Harness 文本 |
| 优化需要搜索大量候选方案，成本高 | 多次完整执行+评估 | 单元测试级别验证即可判断 |
| 一个教训只用于一次任务 | 经验沉没在上下文中 | 教训固化为标签定义 |

### RHI 与 MoA 的关系

```
MoA 定义了系统的骨架和肌肉（角色分工、对抗机制） →  确保智能涌现
RHI 定义了系统的神经系统（标签化信息流）和进化机制    →  确保系统能自我优化
```

**类比**：MoA 是一个团队的组织架构，RHI 是这个团队持续改进工作流程的方法论。

## 核心组件：Harness 的四个维度

RHI 将 Harness 拆解为四个可独立进化的维度（v2.1 标签化架构）：

### 1. Layer 2: 角色声明标签 (was [ROLES])

定义系统中有哪些智能体及其核心职责。v2.1 中角色通过标签声明，而非散落在 Prompt 文本中。

角色标签：`<planner>`、`<expert>`、`<critic>`、`<molder>`。

| 进化维度 | 示例 |
|---------|------|
| **角色头衔调整** | 系统发现总是漏过安全漏洞 → RHI 为 expert 增加 "security_auditor" role 属性 |
| **expert 领域属性优化** | 发现某个专家总输出低质量方案 → RHI 收窄其 domain 属性范围 |
| **critic 来源类型规则** | 批判者太啰嗦 → RHI 调整 source_type（planned/dynamic）规则 |
| **molder 协议属性** | 熔铸策略不稳定 → RHI 修改 molder 的 protocol 属性 |

### 2. Layer 3: 内容标签 (was [CONTRACTS])

定义智能体之间传递什么信息，以及信息的格式。v2.1 中通信契约被内容标签取代，标签自带字段约束，天然防止串供并保证信息保真。

内容标签：`<proposal>`、`<attack>`、`<revision>`、`<final_answer>`、`<boundary>`、`<creative_option>` 等。

| 进化维度 | 示例 |
|---------|------|
| **标签字段增删** | 发现 expert 总遗漏安全风险评估 → RHI 新增 `<risk_assessment>` 标签 |
| **标签属性值域变更** | attack 的 severity 取值过粗 → RHI 扩展值域（如 high/critical 分级） |
| **标签内容约束调整** | 批判者总是输出空泛批评 → RHI 修改 `<attack>` 约束：`<200字符` 且 `line_no` 不可为空（在 [IMMUTABLE] 限制内） |

### 3. 路由属性与执行状态 (was [HOPS])

定义协调器与子智能体之间的交互顺序和逻辑。v2.1 中工作流步骤被路由属性和执行状态对象取代。

路由属性：`visible_to`、`priority`、`route_on`、`domain`。执行状态对象：子任务状态流、attacks_queue、conflict_queue。

| 进化维度 | 示例 |
|---------|------|
| **visible_to 默认值调整** | critic 看不到 expert 的边界条件 → RHI 调整 visible_to 默认包含 `<boundary>` |
| **domain 匹配规则升级** | 字符串匹配漏掉近义领域 → RHI 将 domain 匹配从字符串升级为语义匹配 |
| **priority 路由规则** | 高优先级子任务被串行阻塞 → RHI 修改 priority 路由规则允许抢占 |
| **依赖状态流修改** | 修复次数过多 → RHI 在状态流中增加 `if retry > 3, escalate to human` |

### 4. Layer 4: 信号标签 (was [COORDINATOR])

v2.1 中协调器维度被信号标签取代。协调不再依赖一个独立的总管智能体，而是通过执行状态对象驱动流转，信号标签提供进化所需的反馈闭环。

信号标签：`<signal metric="..." score="..."/>` 自然嵌入在每个阶段中。

| 进化维度 | 示例 |
|---------|------|
| **新增信号指标** | 缺乏对"批判独立性"的度量 → RHI 新增 `<signal metric="critic_independence">` |
| **score 计算方法调整** | critique_specificity 评分过于宽松 → RHI 收紧计分函数 |
| **metric 权重调优** | 发现 token_efficiency 权重过高导致跳过关键步骤 → RHI 降低其权重 |

→ See moa-tag-system.md for complete tag definitions

## 进化循环

### 四步闭环

```
                    ┌─────────────┐
                    │  当前 Harness │
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │  步骤1: 执行 (Execute)    │
              │  按当前 Harness 执行任务    │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  步骤2: 评估 (Evaluate)   │
              │  收集执行指标和失败信息      │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  步骤3: 修改 (Modify)     │
              │  改进智能体生成 Patch      │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  步骤4: 合并 (Merge)      │
              │  通过门控后合并到主分支      │
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │  新版 Harness │ → 回到步骤1
                    └─────────────┘
```

### 进化三要素

| 生物进化 | RHI 对应机制 |
|---------|-------------|
| **变异** | 改进智能体对 Harness 文本的修改（Patch） |
| **选择** | 多目标适应度函数在沙盒中评分 |
| **遗传** | 高分 Patch 合并进 Harness 主分支，作为下一轮基线 |

### 关键洞察

进化不需要执行完整任务链。因为 Harness 是文本规范，Coding Agent 天生擅长阅读和修改代码。往往只需要跑通几个单元测试用例即可判断新 Harness 是否有效，极大压缩了进化成本。

## 三层安全权限架构

为防止 RHI 的"效率导向"破坏 MoA 的核心价值（认知摩擦），将 Harness 划分为三个安全层级：

### 第一层：不可变核心 (Immutable Core)

这些内容写死在 Harness 的前言信条中，RHI 的 Patch 解析器拒绝任何触碰它们的修改请求。

| 不可变项 | 保护原因 | 标记 |
|---------|---------|------|
| I1: `<phase id="3">` 对抗阶段不可移除、跳过、重排序 | RHI 天生想跳过最"耗时"的环节 | `[IMMUTABLE]` |
| I2: `<critic>` 角色标签不可移除或降权 | 没有批判者 = 没有认知摩擦 = MoA 灵魂死亡 | `[IMMUTABLE]` |
| I3: `<attack>` 批判标签不可移除，severity 值域不可收窄为空 | 防止空泛批判导致对抗形同虚设 | `[IMMUTABLE]` |
| I4: `<termination_signal>` 必须显式产出，不可自动生成 | 防止系统自欺欺人地提前终止 | `[IMMUTABLE]` |
| I5: `<final_answer>` "必须再创造"约束不可弱化为"可罗列" | 防止退化为"观点拼盘"，守住熔铸非拼接原则 | `[IMMUTABLE]` |
| I6: `<response>` + `<revision>` 专家必须回应批判，不可省略 | 防止专家回避批判，保证对抗闭环 | `[IMMUTABLE]` |

### 第二层：受保护摩擦区 (Protected Friction Zone / PFZ)

这些可以修改，但不能随便改。每次修改必须：

1. 在沙盒中对 ≥3 个历史任务重跑
2. FQ（摩擦质量）不下降、OQ（产出质量）不下降超过 5%
3. 两指标同时满足才放行

| PFZ 项 | 可调范围 | 评估重点 |
|--------|---------|---------|
| P1: expert version 必须与修正轮次对应 | 不可自动递增 | version 与轮次失配后 OQ 是否下降？ |
| P2: attack severity 值域 | 可扩展，不可收窄为空 | 收窄后 FQ（批判质量）是否下降？ |
| P3: 对抗轮次下限 | 不可降低（共识=1轮 / 辩论=2轮+ / 执行=1轮） | 降低下限后 FQ 是否下降？多轮是否有边际收益？ |

### 第三层：自由进化层 (Free Zone)

RHI 可以自由 Patch，只需通过多目标适应度函数的整体评分（不要求单项不降）：

- 标签定义增删改（非 [IMMUTABLE] 标签）
- visible_to 默认值调整
- domain 属性匹配规则升级（字符串→语义匹配）
- route_on 条件增加
- signal 标签新增（增加评估维度）
- creative_option 等非核心标签增删改
- 角色头衔（expert/critic role 属性）调整

→ See moa-tag-system.md [IMMUTABLE] section for the canonical I1-I6/P1-P3 list

### 权限分级决策

```
RHI 提出 Patch → 分类器判断修改目标层级:
  自由进化层 → 自动执行（整体 Score 提升即采纳）
  PFZ 层级   → 沙盒重跑 + 人工确认（默认 24h 未否决即自动采纳）
  Immutable   → 拒绝执行 + 记录日志 + 通知人类
```

## 多目标适应度函数

### 评估公式

```
Score = 0.35 × FQ + 0.35 × OQ + 0.20 × EF + 0.10 × IS
```

### 四项指标

| 指标 | 全称 | 含义 | 测量方式 |
|------|------|------|---------|
| **FQ** | Friction Quality | 批判是否具体、有深度 | 通过 `<signal metric="critique_specificity">` 和 `<signal metric="critic_independence">` 采集 |
| **OQ** | Output Quality | 最终答案质量 | 通过 `<signal metric="proposal_depth">` 和 `<signal metric="synthesis_novelty">` 采集，外部验证占40% |
| **EF** | Efficiency | 运行效率 | 通过 `<signal metric="token_efficiency">` 采集 |
| **IS** | Innovation Score | 最终答案是否超越任何单一专家 | 通过 `<signal metric="synthesis_novelty">` 和 `<signal metric="immutability_intact">` 采集 |

### 权重设计理由

- FQ + OQ 合计 70%：明确告诉 RHI，质量优先于速度
- EF 仅 20%：防止 RHI 为了效率杀死摩擦
- IS 占 10%：鼓励真正的突破性改进，而不只是小修小补

## 三个补强机制

RHI 的自我改进循环有三个结构性缺陷，需要以下三个补强机制来闭环：

### 补强 1：外部验证钩子

**解决的问题**：模型无法自己验证事实准确性和外部有效性。

**机制**：在评估阶段，根据任务类型自动接入外部验证。

| 任务类型 | 验证方式 |
|---------|---------|
| 代码生成 | 自动运行单元测试、lint 检查 |
| 数据分析 | 统计一致性检验、交叉验证 |
| 事实回答 | 知识库查证、来源交叉比对 |
| 设计方案 | 可行性检查表、边界条件枚举 |

**实现**：在适应度函数的 OQ 计算中，外部验证结果占 40% 权重，模型自评估占 60%（由 `<signal metric="proposal_depth">` 与外部验证信号加权合成）。这确保改进方向不会偏离真实世界的正确性。

### 补强 2：失败模式库

**解决的问题**：系统无法从历史错误中学习，每次都得从零开始找问题。

**机制**：建立结构化的失败模式知识库。

```
失败模式库结构:
{
  "pattern_id": "FP-001",
  "category": "并发安全",
  "description": "共享变量无同步保护导致竞态条件",
  "detection_signal": "检测到多线程/异步访问同一变量但无锁/原子操作",
  "criticality": "high",
  "first_observed": "2026-07-15",
  "occurrence_count": 12,
  "related_attacks": ["竞态条件攻击", "并发一致性问题"]
}
```

**使用方式**：
1. 每次 MoA 执行后，批判者的有效攻击点自动归档入库
2. 新任务启动时，根据任务特征向量检索匹配的失败模式
3. 批判者优先从库中调取已知攻击向量，结合任务特异性进行攻击
4. RHI 可以挖掘失败模式的共现关系，自动生成新的预防性标签定义或路由规则

### 补强 3：人机混合评估

**解决的问题**：纯自动循环缺乏人类价值观锚点，长期运行会漂移。

**机制**：根据 Patch 的风险等级和置信度，分级决策是否需要人工介入。

| Patch 风险等级 | 自评估置信度 | 处理方式 |
|---------------|-------------|---------|
| 低（Free Zone 微调） | 任意 | 自动采纳 |
| 中（PFZ 边界调整） | 高（>0.8） | 异步验证通道，自动积累证据后静默采纳 |
| 中（PFZ 边界调整） | 低（<0.8） | 提交人工审核，24h 超时自动拒绝 |
| 高（涉及核心约束） | 任意 | 直接拒绝（属于 Immutable）/ 强人工确认 |

**异步验证通道**：高置信度 PFZ Patch 不立即合并，而是在一个隔离的沙盒分支上并行运行。当积累了足够的成功证据后（比如连续 10 次任务 FQ + OQ 综合不低于基线），自动合并到主分支。这减少了不必要的人工介入，同时保证了安全性。

## Patch 格式规范

改进智能体生成的 Patch 必须遵循以下 JSON Schema：

```json
{
  "patch_id": "PATCH-2026-0730-001",
  "created_at": "2026-07-30T10:00:00Z",
  "target": "Harness v2.1",
  "type": "tag_definition | routing_rule | role_tag | signal_metric",
  "security_level": "free_zone | pfz | immutable",
  "description": "一句话描述本次修改的目标",
  "diff": [
    {
      "module": "Layer 3: 内容标签",
      "section": "批判契约",
      "action": "add_tag | modify_tag | remove_tag | add_attribute | modify_attribute | add_routing_rule | modify_routing_rule",
      "old_text": "修改前的文本片段",
      "new_text": "修改后的文本片段",
      "rationale": "为什么做这个修改，基于什么证据"
    }
  ],
  "expected_impact": {
    "FQ": "unchanged | +0.05 | -0.02",
    "OQ": "unchanged | +0.03 | -0.01",
    "EF": "unchanged | +0.10 | -0.05",
    "IS": "unchanged | +0.02 | 0"
  },
  "evidence": {
    "failure_tasks": ["task-id-1", "task-id-2"],
    "failure_pattern_id": "FP-001",
    "sandbox_results": {
      "FQ_change": "+0.05",
      "OQ_change": "+0.03",
      "tasks_tested": 3
    }
  }
}
```

### Patch 示例

以下是一个 v2.1 标签化 Patch 的工作示例——为 expert 输出增加风险评估标签：

```json
{
  "patch_id": "PATCH-2026-0804-001",
  "target": "Harness v2.1",
  "type": "tag_definition",
  "security_level": "free_zone",
  "description": "为 expert 输出增加风险评估标签",
  "diff": [
    {
      "module": "Layer 3: 内容标签",
      "action": "add_tag",
      "tag_name": "risk_assessment",
      "parent_tag": "<expert>",
      "default_visible_to": "critic,molder",
      "rationale": "发现专家方案经常遗漏安全风险评估，增加标签强制产出"
    }
  ],
  "expected_impact": {
    "FQ": "+0.05",
    "OQ": "+0.03",
    "EF": "-0.02",
    "IS": "unchanged"
  }
}
```

### Patch 生成约束

1. 每个 Patch 只能修改一个标签层级（避免跨层级耦合变更）
2. `evidence` 字段不可为空：每个 Patch 必须附带实证依据
3. `expected_impact` 必须先预估再提交，用于后续对比验证
4. PFZ 级别的 Patch 必须附带 `sandbox_results`

→ See moa-tag-system.md for tag layer structure and moa-routing-design.md for routing rules

## 门控回滚与熔断机制

### 三道防线

#### 防线 1：修改分类门控

每个 Patch 在提交时先被分类，按安全层级走不同的审批路径（见上文三层架构）。

#### 防线 2：单次回滚规则

```
FQ 下降 > 10%   → 立即回滚，不加判断
OQ 下降 > 5%    → 立即回滚，不加判断
FQ 下降 5-10%   → 标记为待审核，人工决定
OQ 下降 2-5%    → 标记为待审核，人工决定
EF 提升 > 30%   → 自动审查：是否因跳过关键步骤导致的效率提升

FQ 和 OQ 同时下降任一 > 0% → 立即回滚（交叉保护）
```

#### 防线 3：连续回滚熔断

```
连续 3 次回滚 → 冻结当前 Harness 版本
              → RHI 暂停运行
              → 通知人工介入分析根因
              → 只有人工手动解除冻结后才能恢复
```

### 回滚操作

回滚不仅仅是撤销 Patch，而是回到上一个稳定版本的完整快照，包括：
- Harness 文本的完整内容
- 该版本的评估基线数据
- 已验证的沙盒测试结果

## 实施路线图

### 阶段2 启动条件（来自阶段1）

RHI 只有在以下三个条件全部满足后才能启动：

1. **涌现已验证**：MoA 系统确实通过"对抗"产生了高质量结果，批判者不是橡皮图章
2. **结构已解耦**：标签层级（Layer 1-4）清晰分离，[IMMUTABLE] 标记精确到标签级
3. **评估已量化**：建立了 FQ/OQ/EF/IS 的基线值和测量方式

### 渐进式启用

```
Week 1-2: 仅启用 Free Zone 自动进化，积累评估数据
Week 3-4: 引入异步验证通道，处理高置信度 PFZ Patch
Week 5+:  完整启用三层架构，建立持续进化节奏
```

### 进化节奏建议

- 每完成 10 个 MoA 任务 → 触发一次 RHI 评估与 Patch 生成
- 每次最多生成 3 个 Patch（防止一次改太多无法归因）
- 每个 Patch 在沙盒中至少验证 3 个历史任务
- 每周进行一次人工审查，评估进化趋势
