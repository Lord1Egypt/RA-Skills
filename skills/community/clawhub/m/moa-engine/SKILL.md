---
name: moa-engine
version: 2.1.0
description: 编排多角色专家团队通过结构化对抗和逻辑熔铸协同解决复杂问题，支持XML标签化信息流、智能路由和递归式自我改进；当用户需要多角度分析、高风险决策审视、跨领域方案设计或深度架构评审时使用
---

# MoA 混合智能体编排引擎 v2.1

将单模型变为多角色协同的"虚拟专家团队"，通过结构化分工与对抗产出超越单模型极限的高阶方案。

> 设计原理见 [moa-system-guide.md](references/moa-system-guide.md)
> 标签体系见 [moa-tag-system.md](references/moa-tag-system.md)
> 智能路由见 [moa-routing-design.md](references/moa-routing-design.md)
> 可用元 Prompt 模板见 [moa-meta-prompt.md](references/moa-meta-prompt.md)
> 能力注册表见 [scripts/registry_cli.py](scripts/registry_cli.py) | 前置红队见 [scripts/red_team_cli.py](scripts/red_team_cli.py)

## When to Use

**触发条件**（满足任一即启动 MoA）：

- 任务涉及多个专业领域交叉，单一视角无法覆盖
- 高风险决策需要结构化对抗来抵御认知偏误和确认偏误
- 技术架构、产品设计或方案需要多角度充分审视
- 开放性问题存在显著不确定性，需要多路径推演权衡
- 用户明确要求多角度分析、专家团队讨论、深度审查或方案对比

**触发关键词**：多角度分析、专家团队、方案对比、深度审查、架构评审、多维推演、对抗论证

**不触发场景**：简单事实查询、单一领域常规任务、有明确单一答案的问题、闲聊对话

## 核心信条

1. **分工打破全栈盲区** -- 角色隔离，垂直极致审视
2. **对抗制造认知摩擦** -- 结构化攻击与防御，消灭逻辑死角
3. **熔铸实现逻辑跃迁** -- 最终产物是提纯再创造的"合金"
4. **协议优于参数** -- 智慧存在于连接与交互之中

## Phase 0: 任务类型自动判断

MoA 执行前自动分析任务特征，判断类型、评估复杂度与风险等级，推荐执行策略和专家领域。

**使用方式**：
```
# 分析任务，输出类型判断和推荐策略
python scripts/phase0_cli.py classify --task "<任务描述>"

# 详细输出（含得分明细）
python scripts/phase0_cli.py classify --task "<任务描述>" --verbose

# 联动注册表，推荐专家
python scripts/phase0_cli.py classify --task "<任务描述>" --profiles references/capability-profiles.json

# 列出所有任务类型
python scripts/phase0_cli.py list-types
```

### 任务类型与决策协议

| 任务类型 | 特征 | 决策协议 | 对抗轮次 |
|---------|------|---------|---------|
| 知识密集型 | 事实判断、合规审查、概念解释 | 共识优先 + 总管复核 | 1轮事实核查 |
| 推理决策型 | 方案选择、架构设计、策略规划 | 辩论 + 加权投票 | 2轮+深度对抗 |
| 工具执行型 | 代码生成、配置编写、自动化 | 总管调度执行 | 1轮质量批判 |

**风险标记**：高风险任务（涉及隐私/金融/医疗/安全/合规）自动启用审计日志，增加对抗轮次。

**复杂度影响**：高复杂度任务自动增加对抗轮次深度，推荐更多领域专家参与。

### 与注册表的联动

Phase 0 自动将任务分析结果中的推荐领域传递给注册表，匹配最合适的专家画像。匹配结果直接注入 Phase 1 的 `<assignment>` 中，规划师只需确认或微调，无需从零创建。

> 完整协议选择规则见 [moa-system-guide.md](references/moa-system-guide.md) 进阶设计一

## 四种核心角色

| 角色 | 职责 |
|------|------|
| **战略规划师** | 拆解任务树、判断任务类型、选择决策协议、动态指派专家与批判者 |
| **领域专家** | 在各自子任务内提供极致专业方案，明确能力边界，携带 domain 标签 |
| **无情批判者** | 基于事实、边界条件发起结构化攻击，可主动请求更多信息 |
| **熔铸决策者** | 审视全链路交锋，在最优解基础上高维重新组织与再创造 |

> 角色详细定义见 [moa-system-guide.md](references/moa-system-guide.md) 分工机制

## 标准执行流程

```
阶段0:  任务类型判断 → 选择决策协议 + 风险标记
阶段1:  战略规划     → 任务分解树 + 注册表匹配 + 角色指派 + 循环依赖检测
阶段1.5:前置红队     → 架构/安全/合规/成本扫描 → 注入 <pre_risk>
阶段2:  并行深度推演 → 各专家产出方案 [v1] + 跨域感知 → 动态追加批判者
阶段3:  结构化对抗   → 批判者攻击(复核 pre_risk) → 专家修正[v2]或反驳 → 直至无重大风险
阶段4:  逻辑熔铸     → 融合冲突 + 读取 pre_risk → 裁决（含反驳裁决）→ 最终方案
```

> 注册表匹配: `python scripts/registry_cli.py match --task "<子任务描述>" --profiles references/capability-profiles.json --top-k 3`
> 红队扫描: `python scripts/red_team_cli.py run --task "<任务描述>" --decomposition "<阶段1产出>" --teams arch,sec,comp,cost`

## [IMMUTABLE] 不可变标记

核心不可变（标签级，RHI Patch 解释器拒绝触碰）：

- I1: `<phase id="3">` 对抗阶段不可移除、跳过或重排序
- I2: `<critic>` 角色标签不可移除或降权
- I3: `<attack>` 批判标签不可移除，severity 值域不可收窄为空
- I4: `<termination_signal>` 必须显式产出，不可自动生成
- I5: `<final_answer>` "必须再创造"约束不可弱化为"可罗列"
- I6: `<response>` + `<revision>` 专家必须回应批判，不可省略

保护摩擦区（可微调不可质变）：P1 version 不可自动递增、P2 severity 值域可扩展不可收窄、P3 对抗轮次下限不可降低。

> 完整清单见 [moa-tag-system.md](references/moa-tag-system.md) [IMMUTABLE] 部分

## 能力注册表（专家画像库）

16 个预置专家画像，覆盖架构/安全/数据库/前端/产品/UX/数据/合规/性能/API/测试/DevOps/算法/商业/隐私/AI 领域。

**使用方式**：
```
# 语义匹配专家（BM25 算法，零外部依赖）
python scripts/registry_cli.py match --task "<子任务描述>" --profiles references/capability-profiles.json --top-k 3

# 列出所有专家
python scripts/registry_cli.py list --profiles references/capability-profiles.json

# 按领域过滤
python scripts/registry_cli.py list --profiles references/capability-profiles.json --domain security

# 注册新专家（手动录入）
python scripts/registry_cli.py register --id "expert-xxx" --title "..." --domains "a,b" --skills "x,y" --output references/capability-profiles.json

# 从信号标签更新 performance_vector（MoA 执行后自动调用）
python scripts/registry_cli.py update --signals signals.json --profiles references/capability-profiles.json --alpha 0.3

# 查看统计
python scripts/registry_cli.py stats --profiles references/capability-profiles.json
```

**集成方式**：Phase 1 规划师输出子任务列表后，对每个子任务调用 `match` 获取推荐专家，将匹配结果注入 `<assignment>` 的 `<expert_role>` 和 `<domain>` 字段。若 `score < 0.3` 或匹配为空，fallback 由规划师自行创建 ad-hoc 专家。

> 种子数据见 [capability-profiles.json](references/capability-profiles.json)（16 个专家画像，持续扩充）

## 前置红队（风险预扫描）

在专家产出前进行结构化风险扫描，复用宿主模型，仅切换 System Prompt，不增加额外 LLM 调用成本。

**四种红队**：

| 红队 | 触发条件 | 核心视角 | 产出标签 |
|------|---------|---------|---------|
| 架构红队 | 所有推理决策型任务 | 单点故障、扩展性瓶颈、数据一致性、观测盲区 | `<risk_profile type="arch">` |
| 安全红队 | 涉及 auth/data/network/依赖 | STRIDE 威胁建模、攻击面、供应链、零信任缺口 | `<risk_profile type="sec">` |
| 合规红队 | 高风险任务（risk_flag=是） | GDPR/PCI-DSS/等保/行业法规映射、证据链要求 | `<risk_profile type="comp">` |
| 成本红队 | 工具执行型或成本敏感 | Token/延迟/云资源上下界、冷启动、并发成本曲线 | `<risk_profile type="cost">` |

**使用方式**：
```
# 列出所有可用红队
python scripts/red_team_cli.py list-teams

# 运行全量红队扫描（输出 Prompt 模板）
python scripts/red_team_cli.py run --task "<任务描述>" --decomposition "<阶段1产出>" --teams arch,sec,comp,cost

# 获取单个红队 Prompt
python scripts/red_team_cli.py prompt --team arch --task "<任务描述>" --decomposition "<阶段1产出>"
```

**集成方式**：Phase 1 完成后，将任务描述和分解传给 `run` 命令，获取各红队的 System Prompt → 调用宿主模型获取 XML 风险清单 → 注入各 `<subtask>` 的 `<pre_risk>` 字段 → Phase 2 专家展开时须回应 pre_risk → Phase 3 批判者变为"复核 pre_risk 是否被充分覆盖"，减少无效攻击。

## 信号学习与画像进化

每次 MoA 执行完成后，从 Phase 4 输出的 `<signal>` 标签中提取信号数据，通过 EMA 加权更新对应专家的 `performance_vector`，让注册表"越用越准"。

**信号格式**（JSON 数组）：
```json
[
  {"metric": "synthesis_novelty", "score": 0.85, "expert_id": "expert-dist-arch", "source": "moa_run"},
  {"metric": "critique_specificity", "score": 0.72, "expert_id": "expert-security", "source": "moa_run"}
]
```

**使用方法**：
```
# MoA 执行完毕后调用
python scripts/registry_cli.py update --signals signals.json --profiles references/capability-profiles.json --alpha 0.3
```

**EMA 更新规则**：`new_value = 0.3 * signal_score + 0.7 * old_value`，其中 `alpha=0.3` 表示新信号占 30% 权重，历史积累占 70%。`alpha` 越大，历史衰减越快；`alpha` 越小，历史积累越稳定。

**自动触发**：每次 Phase 4 熔铸完成后，自动收集 `<signal>` 标签，调用 `update` 命令更新注册表。后续 Phase 1 匹配时将优先采用 `performance_vector` 中得分更高的专家。

## RHI 进化闭环

RHI（Recursive Harness Self-Improvement）是 MoA 的自我进化机制。每次 MoA 执行完成后，通过采集 `<signal>` 标签计算适应度（fitness），识别最弱维度，生成增强指令注入下一轮 Prompt，形成"执行-评估-改进-再执行"的进化循环。

### 适应度函数

```
fitness = 0.30 * synthesis_novelty     (熔铸创新度)
        + 0.25 * critique_specificity   (批判精准度)
        + 0.20 * revision_quality       (修正质量)
        + 0.15 * token_efficiency       (Token 效率)
        + 0.10 * immutability_intact    (IMMUTABLE 完整性)
```

| 适应度区间 | 判定 | 行动 |
|-----------|------|------|
| >= 0.85 | 已收敛 | 结束进化，采纳当前 Prompt |
| 0.70 - 0.85 | 持续改进 | 建议继续优化，至少再跑 1 轮 |
| < 0.70 | 需要改进 | 必须继续进化，针对最弱维度重点加强 |

### 使用方式

```bash
# 计算适应度
python scripts/rhi_runner.py fitness --signals signals.json

# 生成增强指令（纯文本，便于复制）
python scripts/rhi_runner.py enhance --signals signals.json --task "<任务描述>" --round 2 --text

# 批量分析多轮进化结果
python scripts/rhi_runner.py analyze --rounds round1.json round2.json round3.json
```

### 进化流程

```
第1轮: 执行 MoA → 采集 <signal> → 计算 fitness = 0.63
  → 最弱维度: critique_specificity (0.45)
  → 生成增强指令: 批判精度要求
  ↓
第2轮: 注入增强指令 → 重新执行 MoA → 采集 <signal> → 计算 fitness = 0.72
  → 最弱维度: token_efficiency (0.60)
  → 生成增强指令: 效率优化要求
  ↓
第3轮: 注入增强指令 → 重新执行 MoA → 采集 <signal> → 计算 fitness = 0.81
  → 最佳轮次（第3轮），趋势 improving，建议收敛
```

### 与注册表的联动

每次 MoA 执行后的信号标签同时用于：
1. 计算 fitness（RHI 闭环 — 判断是否收敛）
2. 更新专家 performance_vector（信号学习 — 让注册表越用越准）

> 适应度函数详情见 [fitness-function.md](references/fitness-function.md)
> Patch 规范见 [patch-spec.md](references/patch-spec.md)

## 使用示例

### 示例1: 技术架构评审
- 场景/输入: "评审我们的微服务架构是否存在单点故障风险"
- 预期执行:
  - Phase 0: 判断为推理决策型 → 辩论+加权投票协议，2轮深度对抗
  - Phase 1: 拆解为服务拆分合理性、数据一致性、故障隔离、监控告警等子任务
  - Phase 2: 分布式系统专家、数据一致性专家、SRE专家各自产出方案
  - Phase 3: 批判者攻击数据一致性方案的分区容忍性问题，专家修正v2
  - Phase 4: 熔铸决策者产出完整的架构评审报告
- 关键要点: 任务类型为推理决策型，需2轮对抗；涉及高风险，启用审计日志

### 示例2: 产品设计决策
- 场景/输入: "我们的SaaS产品是否应该引入AI助手功能"
- 预期执行:
  - Phase 0: 判断为推理决策型 → 辩论+加权投票协议
  - Phase 1: 拆解为用户价值分析、技术可行性、成本收益、竞品对比、风险评估
  - Phase 2: 产品策略专家、AI技术专家、财务分析师、竞品分析师各自产出
  - Phase 3: 批判者质疑ROI计算的乐观假设，财务分析师修正v2
  - Phase 4: 熔铸产出结构化的决策建议书
- 关键要点: 多领域交叉，需动态批判者指派覆盖合规领域

### 示例3: 代码安全审查
- 场景/输入: "审查这个支付模块的代码是否存在安全漏洞"
- 预期执行:
  - Phase 0: 判断为知识密集型+高风险 → 共识优先+总管复核，1轮事实核查
  - Phase 1: 拆解为输入验证、认证授权、数据加密、日志审计、依赖安全
  - Phase 2: 安全专家、密码学专家、合规专家各自产出
  - Phase 3: 批判者发现SQL注入风险，专家修正v2
  - Phase 4: 熔铸产出安全审查报告与修复建议
- 关键要点: 高风险任务，启用审计日志；知识密集型，1轮事实核查即可

## 参考文档导航

| 文件 | 何时读取 |
|------|---------|
| [architecture-overview.md](references/architecture-overview.md) | 需要理解系统架构层次、数据流全景、接口契约与扩展点时 |
| [PROJECT_OVERVIEW.md](references/PROJECT_OVERVIEW.md) | 需要理解全局架构、MoA/RHI 价值定位、设计决策时 |
| [moa-meta-prompt.md](references/moa-meta-prompt.md) | 需要复制完整元 Prompt 模板、协议选择决策树时 |
| [moa-system-guide.md](references/moa-system-guide.md) | 需要理解设计原理、分工协同机制、三次认知跃迁时 |
| [moa-tag-system.md](references/moa-tag-system.md) | 需要完整标签定义、属性值域、可见性矩阵时 |
| [moa-routing-design.md](references/moa-routing-design.md) | 需要路由规则、动态批判者逻辑、执行状态管理时 |
| [moa-case-study.md](references/moa-case-study.md) | 需要实战案例参考、失败模式、最佳实践时 |
| [moa-rhi-guide.md](references/moa-rhi-guide.md) | 需要了解 RHI 进化机制、设计原理时 |
| [moa-phase-transition.md](references/moa-phase-transition.md) | 需要了解过渡闸门条件、评估框架时 |
| [fitness-function.md](references/fitness-function.md) | 需要了解适应度函数公式、权重设计、收敛标准时 |
| [patch-spec.md](references/patch-spec.md) | 需要了解 Patch 结构、IMMUTABLE 校验规则、回滚策略时 |
| [capability-profiles.json](references/capability-profiles.json) | 需要查看或扩充种子专家画像数据时 |
| [phase0_cli.py](scripts/phase0_cli.py) | 需要任务类型判断、复杂度评估、风险等级识别、推荐执行策略和专家领域时 |
| [registry_cli.py](scripts/registry_cli.py) | 需要语义匹配专家、注册新专家、查看注册表统计、更新信号画像时 |
| [red_team_cli.py](scripts/red_team_cli.py) | 需要前置风险扫描、获取红队 Prompt 模板时 |
| [rhi_runner.py](scripts/rhi_runner.py) | 需要计算适应度、生成增强指令、批量分析多轮进化结果时 |
