# Intelligent Decision-Hub v0.3：从决策底座到决策中枢

## 定位

v0.2 解决的是“如何让一次决策计算可验证、可追责、可回放”。v0.3 在此基础上增加
中枢编排能力：一次请求同时完成基准决策、算法过程审计、假设反事实、用户声明的压力
情景、结构化认知质询、信息补全排序和治理记录。

因此，v0.3 可以正式称为 **Intelligent Decision-Hub 应用核心**，但还不能冒充完整的企业级
多租户控制平台。

## 与 v0.2 的关系

v0.3 没有推翻 `IntelligentDecisionEngine`，而是在其上增加 `IntelligentDecisionHub`：

```text
IntelligentDecisionHub
├── DecisionService
│   ├── IntelligentDecisionEngine
│   ├── StructuralAuditor
│   ├── Counterfactual Analyzer
│   ├── Robustness Analyzer
│   └── Append-only DecisionRepository
├── Scenario Analyzer
├── CognitiveRiskScanner
├── Information Priority Builder
├── HubReport Integrity Sealer
└── Immutable HubReport Repository Interface
```

旧的 `/v1/decisions/*` 接口保持可用；新的 `/v1/hub/analyze` 提供统一中枢报告。
已封存报告可通过 `/v1/hub/reports/{hub_run_id}` 读取；默认实现仍是进程内开发仓库。

## 一、细粒度算法审计

`DecisionResult.algorithm_audit` 不再只是四个阶段摘要。一次基准示例会生成独立事件，
覆盖：

1. 请求契约与有效评估时点；
2. 每条证据的状态、时效、质量维度和责任节点；
3. 每项假设的依赖、证据和责任节点；
4. 每个结构审计发现；
5. 每个方案的每次约束比较；
6. 每个指标的范围、规则、权重、归一化分和加权分；
7. 基础分、软惩罚、总分和方案状态聚合；
8. 假设失效传递闭包；
9. 反事实候选重选；
10. Pareto 前沿和每次权重扰动；
11. 领先候选选择和最终治理状态。

每个 `AlgorithmAuditEvent` 都包含序号、规则、操作、输入、输出、引用、上一事件哈希和
本事件哈希。`algorithm_audit_root_hash` 是整条执行链的根摘要。任何事件内容或顺序变化
都会使验证失败。

该机制审计的是成功进入引擎的算法执行。HTTP 解析前就被拒绝的非法请求仍需生产网关
或事件接收层记录，这属于 v0.4 控制面的职责。

## 二、真正的假设反事实重选

v0.2 已经能报告一个假设失败会影响哪些方案。v0.3 进一步执行：

```text
触发假设失败
-> 计算传递失效假设集合
-> 移除依赖这些假设的方案
-> 在剩余合格方案中重新选择领先者
-> 重新计算剩余集合的 Pareto 前沿
-> 标记 leader_stable / leader_changed / no_viable_alternative
```

这仍然是结构化反事实，不会凭空估计失败概率。

## 三、声明式压力情景

调用者可以在 `HubAnalysisRequest.scenarios` 中显式声明：

- 某个方案的已存在指标发生变化；
- 某些证据变为 `missing` 或 `disputed`；
- 某些假设发生失败。

每个情景都会重新执行确定性引擎，随后应用假设失效移除与候选重选，并返回：

- 情景结果状态；
- 失效假设与移除方案；
- 合格方案及新的领先者；
- 方案分数、审计问题和情景指纹；
- 完整情景算法审计链及验证结果。

系统不接受对不存在方案、指标、证据或假设的静默覆盖。

## 四、第二视角认知风险扫描

`CognitiveRiskScanner` 是确定性挑战规则，不推断人的心理状态。目前检查：

- 单项权重过度集中；
- 最终决策者同时控制大部分权重和约束；
- 当前领先者依赖会改变结果的关键假设；
- 关键证据来源或保管责任过度集中；
- 小幅权重变化导致排名脆弱；
- 合格方案集合过窄；
- 软约束惩罚反转基础排名。

每个发现都必须给出规则编号、严重度、解释、证据引用和一个可由责任人回答的质询问题。
这些发现不直接替代方案分数，也不绕过审批门。

## 五、信息补全优先级

中枢根据结构事实进行词典序排序，而不是捏造“信息价值概率”：

```text
blocking
> leader_exposed
> structural
> review
```

同一层级优先处理影响当前领先者和更多方案的变量。输出会指出变量引用、影响范围、
排序原因和建议动作。

## 六、完整性与治理

v0.3 同时保留三层完整性：

1. 单次算法执行的事件哈希链；
2. 同一决策多次评估/审批的 `DecisionRecord` 父哈希链；
3. 汇总基准决策、情景、认知发现和信息队列的 `HubReport.report_hash`。

哈希能检测内容被修改，但没有外部签名、可信时间戳和独立存储时，不能证明整个数据库
没有被整体重写。生产版本必须接入 KMS/HSM 和不可变事件存储。

## 七、核心请求结构

```json
{
  "decision": {
    "objective": "...",
    "decision_owner": {},
    "criteria": [],
    "constraints": [],
    "assumptions": [],
    "alternatives": [],
    "evidence": []
  },
  "scenarios": [
    {
      "id": "SC1",
      "name": "关键假设失败",
      "failed_assumption_ids": ["A1"]
    },
    {
      "id": "SC2",
      "name": "成本冲击",
      "metric_overrides": {
        "S2": {"capital_required": 6000000}
      }
    }
  ],
  "run_cognitive_audit": true
}
```

## 八、v0.4 建议路线

### 生产控制面

- PostgreSQL 事件仓库、HubReport 历史与乐观并发控制；
- OIDC、服务身份、责任委托链、RBAC/ABAC 和租户隔离；
- 策略注册、签名、灰度发布、回滚和历史回放；
- 请求幂等、限流、异步情景任务、指标、日志、追踪和告警；
- KMS/HSM 签名与可信时间戳。

### 高级决策分析

- 指标区间和概率分布；
- 固定随机种子的 Monte Carlo；
- TOPSIS、ELECTRE 等多策略分歧对照；
- 显式成本与概率输入后的 Value of Information；
- 组合方案和资源约束优化；
- 历史决策基准集、结果回放和策略漂移检测。

## 九、明确边界

- Hub 不自动批准决策；
- 认知扫描不诊断个人心理；
- 情景只使用用户显式声明的变化；
- 当前没有概率推断、Monte Carlo 或机器学习预测；
- 当前内存仓库不适合多实例生产；
- 医疗、法律、财务和安全决策仍由对应专业责任人承担。
