# MoA 标签体系

## 目录

- [概述](#概述)
- [标签层级](#标签层级)
- [Layer 0: 执行容器](#layer-0-执行容器)
- [Layer 1: 阶段结构](#layer-1-阶段结构)
- [Layer 2: 角色声明](#layer-2-角色声明)
- [Layer 3: 内容标签](#layer-3-内容标签)
- [Layer 4: 信号标签](#layer-4-信号标签)
- [路由属性](#路由属性)
- [默认可见性矩阵](#默认可见性矩阵)
- [[IMMUTABLE] 完整清单](#immutable-完整清单)

## 概述

MoA v2.1 使用 XML 标签体系统一管理信息结构、路由和进化接口。标签替代了 v2.0 的 Contracts（输出模板）、Hops（条件分支）和记忆路由三套机制。

标签服务于两个层面：
- **执行层**：引导模型的输出结构，控制信息可见性
- **进化层**：为 RHI 提供可解析的修改单位

## 标签层级

```
Layer 0: <execution> 执行容器
Layer 1: <phase> 阶段结构
Layer 2: <planner>/<expert>/<critic>/<molder> 角色声明
Layer 3: <proposal>/<attack>/<synthesis> 内容标签
Layer 4: <signal> 信号标签（供 RHI 评估）
```

## Layer 0: 执行容器

`<execution task="{用户任务}" version="2.1" protocol="[协议]" risk="[是/否]">`

包裹整个 MoA 运行，标识一次完整执行的元数据。

## Layer 1: 阶段结构

| 标签 | 阶段 | IMMUTABLE |
|------|------|-----------|
| `<phase id="0" name="task_judgment">` | 任务类型判断 | 否 |
| `<phase id="1" name="strategic_planning">` | 战略规划 | 否 |
| `<phase id="2" name="expert_deliberation">` | 并行专家推演 | 否 |
| `<phase id="3" name="adversarial_review">` | 结构化对抗 | **是** |
| `<phase id="4" name="logical_molding">` | 逻辑熔铸 | 否 |

## Layer 2: 角色声明

### 战略规划师

```xml
<planner>任务分解树和角色指派</planner>
```

### 领域专家

```xml
<expert role="具体头衔" version="N" status="待审视|已修正|已采纳|已否决" subtask="子任务ID" domain="领域1,领域2">
  ...内容标签...
</expert>
```

| 属性 | 说明 | RHI 可修改 |
|------|------|-----------|
| role | 专家头衔 | 是 |
| version | 方案版本号 | 否 |
| status | 当前状态 | 否 |
| subtask | 绑定子任务 ID | 是 |
| domain | 领域标记（智能路由用） | 是 |

status 值域：待审视 | 已修正 | 已采纳 | 已否决 | 争议中（反驳通道触发时使用）

### 批判者

```xml
<critic role="具体头衔" target="expert_role" scope="子任务ID|全局" source="planned|dynamic" [IMMUTABLE]>
  ...内容标签...
</critic>
```

| 属性 | 说明 | RHI 可修改 |
|------|------|-----------|
| role | 批判者头衔 | 是 |
| target | 被批判的专家 | 是 |
| scope | 批判范围 | 是 |
| source | planned=Phase1指派 / dynamic=跨域感知追加 | 是 |
| [IMMUTABLE] | 标签本身不可被移除或降权 | — |

### 熔铸决策者

```xml
<molder protocol="[协议]">...内容标签...</molder>
```

## Layer 3: 内容标签

### Phase 0 内容

| 标签 | 语义 |
|------|------|
| `<task_type>` | 知识密集型 / 推理决策型 / 工具执行型 |
| `<decision_protocol>` | 共识优先 / 辩论投票 / 调度执行 |
| `<risk_flag>` | 是 / 否 |
| `<judgment_basis>` | 一句话判断依据 |

### Phase 1 内容

```xml
<decomposition>
  <subtask id="A" description="任务描述">
    <assignment>
      <expert_role>具体专家头衔</expert_role>
      <core_output>核心产出目标</core_output>
      <critic_role>具体批判者头衔</critic_role>
    </assignment>
    <dependency>none | subtask:X</dependency>
  </subtask>
</decomposition>

<!-- 循环依赖检测（Phase 1 后执行） -->
<dependency_check>
  若发现循环依赖，标记 <circular_detected> 并重新分解
</dependency_check>

<!-- 跨域批判者缺口检测（Phase 2 后执行） -->
<critic_gap_detection>
  若发现某 domain 未被任何 planned critic 覆盖，
  动态追加 <critic role="新头衔" source="dynamic">
</critic_gap_detection>
```

### Phase 2 内容（在 `<expert>` 内）

| 标签 | 语义 | 默认 visible_to |
|------|------|----------------|
| `<proposal>` | 核心方案 | critic,molder |
| `<technical_detail>` | 实现路径/技术细节 | critic(按需),molder |
| `<boundary>` | 能力边界声明 | critic,molder |
| `<referenced_dependency>` | 引用前置结论 | all |
| `<creative_option>` | 创意性可选项 | molder |

### Phase 3 内容（在 `<critic>` 内）

```xml
<attack id="1" target="expert_role" version="1" severity="致命|重要|次要">
  <issue>具体问题</issue>
  <impact>影响范围</impact>
  <trigger>触发/边界条件</trigger>
</attack>
```

| 标签 | 语义 | IMMUTABLE |
|------|------|-----------|
| `<attack>` | 批判攻击单元 | **是**（不可移除/降权） |
| `<issue>` | 具体问题 | — |
| `<impact>` | 影响范围 | — |
| `<trigger>` | 触发条件 | — |

信息请求：
```xml
<request_info target="expert_role" tag="technical_detail" section="需要展开的部分"/>
```

专家回应——通道1：确认并修正
```xml
<response target="attack_id" type="确认">
  <acknowledgment>确认问题存在</acknowledgment>
  <revision version="N">修正方案</revision>
</response>
```

专家回应——通道2：反驳
```xml
<response target="attack_id" type="反驳">
  <acknowledgment>反驳理由</acknowledgment>
  <evidence>支持反驳的证据或逻辑</evidence>
</response>
```

终止信号：
```xml
<termination_signal status="clear|needs_more_rounds">理由</termination_signal>
```
[IMMUTABLE: 必须显式产出，不可自动生成或跳过]

### Phase 4 内容（在 `<molder>` 内）

| 标签 | 语义 | IMMUTABLE |
|------|------|-----------|
| `<highlights>` | 各方案核心亮点 | — |
| `<highlight>` | 单个亮点 | — | 属性：source, version, status |
| `<conflict_resolution>` | 冲突裁决容器 | — |
| `<conflict>` | 争议点 | — |
| `<decision>` | 裁决结论 | — |
| `<rationale>` | 裁决依据 | — |
| `<refuted_attack>` | 被驳回的批判 | — |
| `<sustained_rebuttal>` | 被支持的反驳 | — |
| `<decision_chain>` | 完整决策链路 | — |
| `<audit_log>` | 审计日志（高风险） | — |
| `<final_answer>` | 最终方案 | **是**（必须再创造） |

冲突标记（跨子任务）：
```xml
<conflict_ref source="subtask:A" point="冲突点描述"/>
```

## Layer 4: 信号标签

信号标签自然嵌入在各阶段输出中，为 RHI 适应度函数提供结构化评估数据。

| 标签 | 采集位置 | 度量维度 | 说明 |
|------|---------|---------|------|
| `<signal metric="task_clarity" score="0-1"/>` | Phase 0 | — | 任务理解清晰度 |
| `<signal metric="proposal_depth" score="0-1"/>` | Phase 2 每个 expert | FQ | 方案具体程度和技术深度 |
| `<signal metric="critique_specificity" score="0-1"/>` | Phase 3 每个 critic | OQ | 批判的具体性和可操作性 |
| `<signal metric="critic_independence" count="N"/>` | Phase 3 整体 | OQ | 批判者独立发现的新问题数 |
| `<signal metric="revision_quality" score="0-1"/>` | Phase 3 每个 revision | OQ | 修正方案的实质性程度 |
| `<signal metric="synthesis_novelty" score="0-1"/>` | Phase 4 molder | FQ | 熔铸相对各方案的增量价值 |
| `<signal metric="token_efficiency" ratio="0-1"/>` | 各阶段 | EF | 实际 token / 预算 token |
| `<signal metric="immutability_intact" violations="0"/>` | 全程 | IS | IMMUTABLE 标记被触碰次数 |

## 路由属性

所有内容标签可携带以下路由属性：

| 属性 | 语义 | 默认值 | 示例 |
|------|------|--------|------|
| `visible_to` | 可见角色列表 | 按阶段默认 | `visible_to="critic,molder"` |
| `priority` | 处理优先级 | normal | `priority="critical"` |
| `route_on` | 条件路由 | 无 | `route_on="dependency_resolved"` |
| `domain` | 领域标记 | 无 | `domain="concurrency,security"` |

## 默认可见性矩阵

| 标签 | planner | expert(自身) | expert(他人) | critic | molder |
|------|---------|-------------|-------------|--------|--------|
| task_type / protocol / risk_flag | 全局 | 全局 | 全局 | 全局 | 全局 |
| decomposition / subtask | 全部 | 自身+依赖 | 依赖方 | 全部 | 全部 |
| proposal | 摘要 | 完整 | 不可见 | 完整 | 完整 |
| technical_detail | 不可见 | 完整 | 不可见 | 按需 | 完整 |
| boundary | 可见 | 完整 | 不可见 | 完整 | 完整 |
| referenced_dependency | 可见 | 完整 | 被引用方 | 完整 | 完整 |
| creative_option | 不可见 | 不可见 | 不可见 | 不可见 | 完整 |
| attack | 不可见 | 被攻击方 | 不可见 | 自身产出 | 完整 |
| response / revision | 不可见 | 自身 | 不可见 | 完整 | 完整 |
| termination_signal | 不可见 | 可见 | 不可见 | 可见 | 完整 |
| highlights / conflict_resolution | 不可见 | 不可见 | 不可见 | 不可见 | 完整 |
| final_answer | 不可见 | 不可见 | 不可见 | 不可见 | 自身产出 |
| signal | 不可见 | 不可见 | 不可见 | 不可见 | 完整 |

## [IMMUTABLE] 完整清单

### 核心不可变（MoA 灵魂）

| # | 保护对象 | 位置 | 约束 |
|---|---------|------|------|
| I1 | `<phase id="3">` 对抗阶段 | 阶段结构 | 不可移除、跳过、重排序 |
| I2 | `<critic>` 角色标签 | 角色声明 | 不可移除或降权 |
| I3 | `<attack>` 批判标签 | Phase 3 | 不可移除，severity 值域不可收窄为空 |
| I4 | `<termination_signal>` 终止信号 | Phase 3 | 必须显式产出，不可自动生成 |
| I5 | `<final_answer>` 最终方案 | Phase 4 | "必须再创造"约束不可弱化为"可罗列" |
| I6 | `<response>` + `<revision>` | Phase 3 | 专家必须回应批判，不可省略 |

### 保护摩擦区（可微调不可质变）

| # | 保护对象 | 约束 |
|---|---------|------|
| P1 | expert version 属性 | 必须与修正轮次对应，不可自动递增 |
| P2 | attack severity 属性 | 值域可扩展，不可收窄为空 |
| P3 | 对抗轮次下限 | 共识=1轮/辩论=2轮+/执行=1轮，下限不可降 |

### 自由区（RHI 可自主修改）

subtask 增删改、expert/critic 头衔调整、visible_to 默认值、route_on 条件、signal 标签新增、domain 属性使用、creative_option 等非核心标签增删改。
