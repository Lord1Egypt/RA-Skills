<p align="center">  
  <img src="assets/banner.png" alt="NOMOS 横幅" style="width:100%">  
</p>

<p align="center">  
  <img src="https://img.shields.io/badge/python-D4AF37?style=flat-square" alt="python">  
  <img src="https://img.shields.io/badge/framework-v0.7.0-D4AF37?style=flat-square" alt="framework-v0.7.0">  
  <img src="https://img.shields.io/badge/AI_Verify_self--assessed-95%2F100-D4AF37?style=flat-square" alt="AI Verify self-assessed 95/100">  
</p>

<blockquote align="center">  
  <em>NOMOS · v0.7.0 —— 企业管理系统 · 可扩展智能决策中枢</em>  
</blockquote>

<p align="center">  
  简体中文  
</p>

<div style="max-width:880px;margin:0 auto;padding:0 16px">

## ✦ 关于

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
NOMOS 是一个<strong>企业管理系统</strong>，内核是一个<strong>可扩展的智能决策中枢</strong>：既可支撑数据中心完成数据汇聚、分析评估与业务决策等各项工作，也留出唯一扩展点（领域控制包），由企业自行挂载本企业的管理模块 —— NOMOS 交付内核与护栏，不代写企业制度。它依据新加坡 <strong>IMDA AI Verify</strong> 框架自行评测获得 <strong>95/100</strong> 分（提供方自测结果，非 IMDA 官方评估或认证）。该引擎将结构化评估、细粒度算法审计、声明式假设交互（二阶因果复合）、带确定性收敛证明的形式化有界三层重建、反事实重选、声明式场景压力测试、结构化认知挑战、信息优先级排序，以及人类治理，统一为一份哈希链报告。  
</p>

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
它从不虚构缺失的事实、权重、阈值、责任方、证据、概率<em>或交互强度</em>。二阶效应（协同、冗余、放大）必须<strong>由责任方显式声明</strong> —— 引擎从不估计或学习它们。LLM 被限制在三层权限区（标注 / 提案 / 叙述）内，永远不能自行翻转状态、作出裁决或改动权重。它在声明输入下产出候选，并始终将最终裁决保留在算法之外。  
</p>

<p align="center">  
  <img src="assets/overview.png" alt="NOMOS 概览" style="width:100%">  
</p>

</div>

<p align="center">— ✦ —</p>

## ✦ 内置通用审计引擎

<div style="max-width:880px;margin:0 auto;padding:0 16px">

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
NOMOS 自带一个<strong>通用审计引擎</strong> —— 它不是外挂补丁。审计轨迹内建于确定性内核之中：每一项决策、假设、约束与因果步骤都被记录、哈希链接，并可被独立验证。  
</p>

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
它依据新加坡 <strong>IMDA AI Verify</strong> 框架，在因果审计赛道自行评测获得 <strong>95/100</strong> 分（提供方自测结果）。自评测报告见 <code>IMDA_AI_Verify_Causal_Audit_Report.pdf</code>（提供方提交材料，非 IMDA 签发文件）。  
</p>

</div>

<p align="center">— ✦ —</p>

## ✦ 企业集成

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
作为<strong>企业管理系统</strong>，NOMOS 并不取代现有的 ERP/CRM/风控/合规/投决/HR/项目审批系统，也不打包出售成品业务模块：它是嵌入其后的<strong>确定性决策内核</strong>。每个上游系统提交带显式声明交互与责任方的结构化请求；NOMOS 返回候选、反事实、哈希链审计轨迹与形式化收敛状态；最终裁决始终由人签署后，才回流至下游的审计、审批与报告流程。企业管理中属于企业自己的那部分（人员调度、行业规则等），由企业以领域控制包自行扩展挂载。
</p>

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">
作为企业管理系统，它的能力边界由两类东西界定 —— <strong>内核自带的</strong>，与<strong>企业自己扩展的</strong>：
</p>

<ul style="font-size:15px;line-height:1.8;color:#2C2C2C">
  <li><strong>可扩展（企业自建）</strong> —— 新的管理功能由<strong>企业自己写成模块</strong>挂接，NOMOS 不提供成品业务模块、不代写企业制度。扩展点只有一个：领域控制包（<code>src/second_perspective/domain/</code>）。控制包位于确定性内核之外，只做观测：不改判结论、不编造缺失数据、不拖垮管线。加功能不等于改内核。</li>
  <li><strong>人员智能协同调度（扩展位 · 企业自建）</strong> —— 谁被分派、谁负责、谁必须确认，规则由企业自己编码；跨部门协作不再是一串聊天记录，而是一条可审计的链。NOMOS 只守一条线：调度建议停在 <code>AWAITING_HUMAN</code>，引擎绝不自行调动人员。</li>
  <li><strong>重大决策分析留痕（内核自带）</strong> —— 任何一套部署第一天就有，不需要挂模块：重大决策保留候选集、被考虑过的其他路径、审批动作与哈希链事件流；数月之后仍可逐步复现、逐项验证。</li>
  <li><strong>内部人员调度（扩展位 · 企业自建）</strong> —— 排人的制度是企业的：角色、技能、当前负载由企业声明为决策输入，什么算违规由企业的控制包判定。引擎补上企业写不了的那部分 —— 某项没有责任人、某个约束没声明，一律报缺，绝不悄悄补一个安排上去。</li>
</ul>

<p style="font-size:15px;line-height:1.8;color:#2C2C2C">  
扩展目录：<a href="./docs/ENTERPRISE_MODULES.md">Extending NOMOS into Enterprise Modules</a> —— 领域控制包契约，以及可扩展的企业模块类别。  
</p>

```text
企业管理系统（ERP/CRM/风控/合规/投决/HR/项目审批）
        │
        │  提交结构化决策请求 + 已声明的交互 + 责任人
        ▼
   ┌─────────────────┐
   │  NOMOS v0.7     │  ← 确定性决策内核（本仓库）
   │  - 一阶失效     │     输出：候选集 + 反事实 + 审计链 + 收敛状态
   │  - 二阶交互     │
   │  - 三层重建     │     不输出最终结论——结论由人签
   │  - LLM 护栏     │
   └─────────────────┘
        │
        ▼
   审计留痕 / 审批流 / 合规报告 / LLM 辅助叙述（T3）
```

<p align="center">— ✦ —</p>

## ✦ v0.7 新特性 —— 术语对齐（破坏性变更）

v0.7 将元因果账本的五个键改为全 ASCII，并收敛 reason 码前缀。**对消费方是破坏性变更。**

- `meta_ledger.bases` 的五个键现为 `trace_gap` / `parallel_convergence` / `narrative_occlusion` / `bounded_audit` / `causal_succession`。
- reason 码前缀收敛为 `TRACE_` / `CONVERGENCE_` / `NARRATIVE_` / `AUDIT_` / `SUCCESSION_`。
- 旧键与旧前缀一并废弃，**不保留别名** —— 让两套词汇长期共存，才是真正删不掉的成本。
- 不再逐字引用规范原文：改为改述并标注节号，因为机械替换曾把引文改写成本项目词汇。
- 测试 520 项全绿。

完整变更日志：[`CHANGELOG.md`](./CHANGELOG.md)。

## ✦ v0.6 新特性 —— 十算子认知审计内核

v0.6 将认知审计内核由五算子升级为十算子，移植 ⊙ORI / ⊞TPG / BFC / ⇄GRF / META 及拓扑底座（四进程校验，含公理 5 链内时序）。

- **META 元因果账本** —— 只做度量，结构上不允许阻断（恒 T2）。
- **契约扩展** —— `DecisionRequest` 新增可选一等字段 `origin`（`DecisionOrigin`）与 `rollout`（`DecisionRollout`）。
- **条件注册** —— 适配器仅在声明原点时注册 `ORI`、声明灰度阶梯时注册 `GRF`，杜绝引入永真阻断。
- **报告顶层视图** —— 新增 `topology` / `bfc` / `meta_ledger`，并注入 `_config` 使 A6/A10 阈值可配置。
- **自主进化层（⊛∞）** —— `evolve` 只提案不适用（`auto_applied` 恒 0）；`approve` 只记账、不改代码。
- 产物版本串 `GCAE-1.0.0 → GCAE-1.1.0`；测试 507 → 520。

## ✦ v0.5 新特性 —— 企业控制平面

v0.5 补齐了 v0.4「生产边界」中列出的全部缺口。所有新增能力均为 <strong>env 门控、默认关闭</strong>，因此既有的 v0.4 部署在相关环境变量未设置时行为完全不变。

- **持久化事件存储** —— 每次 `evaluate`/`approve` 的追加式、哈希链 `DomainEvent` 日志（`persistence/event_store.py`），并提供持久化的 `PostgresEventStore`。
- **租户隔离** —— 基于 `contextvars` 的活跃租户上下文，由 `X-Tenant-Id`（或 OIDC `tid`）解析；事件按租户分区。遗留表经由 `scripts/migrate.py` 预建 `tenant_id` 列。
- **OIDC + 授权强制** —— 写端点上的 opt-in 作用域强制（`SP_AUTHZ_ENFORCE=true`），通过 `require_scope()` 实现；构建于既有认证之上，默认不生效。
- **KMS 签名** —— 对密封产物哈希的分离式 HMAC-SHA256 签名（`security/kms.py`），以 `X-Nomos-Kms-Signature` 响应头返回；在设置 `SP_KMS_SECRET` 之前为透明 no-op。
- **限流** —— opt-in 令牌桶中间件（`SP_RATE_LIMIT`）。
- **可观测性** —— 进程内指标 + `X-Process-Time-Ms`，快照见 `GET /v1/metrics`。
- **备份 / 迁移** —— `scripts/migrate.py`（幂等 DDL）与 `scripts/backup.py`（JSON 导出）。
- **领域控制包** —— 可插拔的 `DomainControlPack` 协议 + 注册表；内置 `FinanceRiskControlPack`。控制包仅做观测，绝不篡改引擎结论。

## ✦ v0.4 新特性 —— 二阶因果框架

v0.4 是首个系统性地对<strong>假设与假设之间的交互</strong>进行推理的版本，而非将失效视为独立事件；它将迭代重建循环锚定到<strong>形式化分类的收敛状态</strong>（经证明而非启发式），并将 LLM 置于一道<strong>三层权限闸门</strong>之后，可证明地防止 LLM 输出成为裁决。

- **假设交互层**（`interaction/`）—— 声明的二阶效应（协同 / 冗余 / 放大），含四条不变式：
  - <strong>I-1 非臆测</strong> —— 每个交互强度 Δ 均由责任方声明；引擎从不估计或学习 Δ。
  - <strong>I-2 阶数守恒</strong> —— 仅当<em>全部</em>成员假设同时失效时交互才触发；部分失效不触发二阶效应。
  - <strong>I-3 效应有界</strong> —— 累积交互效应 ≤ `amplification_ceiling × Σ|一阶|`；冗余（负向）交互不做下限钳制，从而允许真实的阻尼。
  - <strong>I-4 单调性</strong> —— 扩充失效集合永远不会使已触发的交互反触发（并集语义）。
- **形式化收敛引擎**（`convergence/`）—— 以五态分类（`FIXED_POINT` / `NO_GAIN` / `BUDGET_EXHAUSTED` / `DIVERGED` / `BLOCKED`）取代启发式停止判据，并由三条可检验命题（P-1 终止性、P-2 不动点、P-3 效应有界）支撑。`is_true_convergence` 防止将预算耗尽误判为收敛这一经典缺陷。
- **LLM 合规层**（`llm_compliance/`）—— 三档权限（T1 标注 / T2 提案 / T3 叙述）、三条不变式（区隔离、不裁决、强度剥离），以及一个带溯源追踪的 `LLMGate`，在 LLM 响应触及决策图之前剥离其结构性权力。
- **核心集成** —— `DecisionRequest` 新增可选字段 `interaction_declaration`（默认 `None`，完全向后兼容）；`invalidation_closure_with_interaction()` 将一阶闭包与二阶联合效应复合；会话引擎将停止条件检查委托给形式化的 `ConvergenceChecker`。
- **保持向后兼容** —— 未提供 `interaction_declaration` 时，引擎行为与 v0.4 完全一致。未移除或重命名任何既有 API。审计引擎未改动。

测试：412 项通过（新增 132 项），0 失败。完整变更日志：[`CHANGELOG.md`](./CHANGELOG.md)。  
架构：[`docs/INTELLIGENT_DECISION_HUB_V0_4.md`](docs/INTELLIGENT_DECISION_HUB_V0_4.md)。

### v0.3 新特性

- 为每个主要确定性操作提供哈希链审计事件
- 约束与准则计算具备显式操作数与输出
- 在传递式假设失效后进行真正的候选重选
- 由用户声明的压力场景（假设失效、指标覆盖）
- 不推断任何心理状态的确定性认知风险挑战层
- 按优先级排序的信息获取与复核队列
- 一个 `IntelligentDecisionHub` 编排器与一个密封的 `HubReport`
- 基线与场景运行中均含完整审计账本
- 新增 `POST /v1/hub/analyze`，同时保留所有 v0.2 端点

## ✦ 三层因果重建（有界收敛 + 人工闸门）

`hub/session.py`（`ReconstructionSessionEngine`）与 `decision/reconstruction.py`（`reconstruct_with_delta`）中的新特性：此前一次性的因果重建被升级为一个<strong>有界、哈希链、人工闸门的迭代过程</strong>。

每一轮运行三个因果算子：

1. **前向失效传播** —— `invalidation_closure` 将已声明的假设失效向前传播，剔除失去该假设支撑的备选方案。
2. **反向根因追溯** —— 既有的反向 BFS 将偏差信号追溯至一组候选根因假设。
3. **增量重建** —— 将已声明的修正变量（`DeltaVar`）施加于请求副本，重跑确定性评估器，并判定领先候选集的收敛性。

设计不变式（与 NOMOS 内核一致）：

- **不猜测** —— 每个假设都是候选；由人决定。引擎从不自动循环。
- **确定性** —— 每一轮仅由已声明输入推导。
- **可审计** —— 每一轮都与上一轮哈希链接；整个会话构成一个 `session_root_hash`。
- **有界** —— 受 `max_iterations` 与 `max_evidence_requests` 限制。
- **人工闸门** —— `advance()` 恰好执行一轮，然后停在 `AWAITING_HUMAN`；只有人类决策（`approve` / 提供证据 / 拒绝）才能进入下一轮。

停止条件由 `ConvergenceChecker` <strong>形式化分类</strong>为五种状态：

- <strong>真收敛</strong>：`FIXED_POINT`（候选集与上一轮完全相同 —— P-2 证明）或 `NO_GAIN`（无未解决分支）。
- <strong>非收敛</strong>：`BUDGET_EXHAUSTED`（在到达不动点前预算耗尽 —— 明确<em>不是</em>收敛，且不得如此报告）、`DIVERGED`（仍有预算却仍在变化）、`BLOCKED`（命中结构性阻塞，需人工介入）。

```python
from second_perspective.models import DecisionRequest, DeviationSignal, DeltaVar
from second_perspective.hub.session import ReconstructionSessionEngine

engine = ReconstructionSessionEngine()
session = engine.start(request, signals, max_iterations=5)
session = engine.advance(session)                                   # 第 1 轮：三层重建
session = engine.advance(session, [                                 # 注入已声明的修正
    DeltaVar(path="A2", value=None, reason="...", responsibility="..."),
])
session = engine.human_decision(session, approved=True)             # 人工签署
print(session.session_root_hash)
```

`DeltaVar` 的路径有三种形式：`"A2"`（证伪某个假设，并通过依赖图传播）、`"criteria.K1.weight"`（改写某准则权重）、或 `"alternatives.S1.metrics.cost"`（改写某备选方案的指标）。引擎逐字镜像每个已声明的 `DeltaVar`，从不虚构修正。

## ✦ 架构

> **一句话：** NOMOS 以**确定性决策内核**的身份嵌在你现有业务系统背后——一个请求会沿着固定管线走完一串真实模块，而最终结论永远是人签的。

```mermaid
flowchart TB
    UP["上游业务系统（调用方）<br/>ERP · CRM · 风控 · 合规 · 投决 · HR"]

    A1["🚪 api/main.py · security.py<br/>收请求 · 鉴权限流 · 租户隔离"]
    A2["🔎 decision/evaluator · integrity<br/>结构 / 证据审计"]
    A3["⚖️ decision/policy<br/>硬约束 + 软约束"]
    A4["📊 decision/engine · causal<br/>归一化评分 → 一阶因果失效传播"]
    A5["🔗 interaction/engine<br/>二阶交互 · 不变量 I-1 … I-4"]
    A6["🧩 decision/reconstruction · hub/session<br/>三层重建：前向 / 后向 / 增量"]
    A7["✅ convergence/checker<br/>五态判定：定点 / 无增益 /<br/>预算耗尽 / 发散 / 阻塞"]
    A8["🔄 decision/counterfactual · selection · robustness<br/>反事实重选 · 帕累托 · 权重敏感度"]
    A9["🛡️ llm_compliance/gate<br/>T1 批注 / T2 提议 / T3 叙述 · LLM 永不裁决"]
    A10["📒 audit/ledger · persistence/event_store<br/>哈希链算法审计 + 只追加事件流"]
    OUT["📦 封存 HubReport + session_root_hash"]
    HUMAN["✍️ governance/approval<br/>人工签批 —— 最终结论留在算法之外"]

    UP --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    A6 --> A7
    A7 --> A8
    A8 --> A9
    A9 --> A10
    A10 --> OUT
    OUT --> HUMAN

    classDef cUp fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1px,color:#424242
    classDef cIn fill:#E8F0FE,stroke:#4285F4,stroke-width:1px,color:#173A66
    classDef cCore fill:#FFF8E1,stroke:#C9A96E,stroke-width:1px,color:#5B4614
    classDef cGate fill:#F3E8FD,stroke:#8E44AD,stroke-width:1px,color:#4A235A
    classDef cOut fill:#E6F4EA,stroke:#34A853,stroke-width:1px,color:#14512B
    class UP cUp
    class A1 cIn
    class A2,A3,A4,A5,A6,A7,A8 cCore
    class A9,A10 cGate
    class OUT,HUMAN cOut
```

**这张图怎么看**

1. **从上往下读，就是一个请求的一生。** 进来的是 `DecisionRequest`，出去的是带 `session_root_hash` 的封存 `HubReport`。
2. **每个框都写了真正干活的模块路径**，可以顺着图直接翻到源码文件。金色框是纯确定性计算。
3. **紫色两步是边界。** 大模型只能批注 / 提议 / 叙述，不能翻转状态或排名；留痕用哈希链；最终签字是绿色那步——永远不是算法。

📖 每个术语都用一句人话解释 → [术语表 GLOSSARY](./GLOSSARY.md)

**完整决策流水线（详细版）**

```text
HubAnalysisRequest（+ 可选 InteractionDeclaration）
  -> 决策内核
       -> 结构 / 证据审计
       -> 硬约束 + 软约束评估
       -> 归一化评分
       -> 因果失效（一阶）
       -> 假设交互层（二阶：合取 / 析取）
            -> I-1 非臆测 · I-2 阶数守恒 · I-3 效应有界 · I-4 单调
       -> 三层重建（前向 / 反向 / 增量）
            -> 形式化收敛检查器（P-1/P-2/P-3 → 五态分类）
       -> 反事实重选
       -> 帕累托 + 权重敏感性
       -> 哈希链算法审计
  -> LLM 闸门（T1 标注 / T2 提案 / T3 叙述；带溯源追踪、剥离状态）
  -> 声明式场景压力运行
  -> 结构化认知风险挑战
  -> 信息优先级队列
  -> 仅追加 DecisionRecord
  -> 密封 HubReport（session_root_hash）
  -> 人工批准 / 拒绝（最终裁决始终在算法之外）
```


## ✦ 安装与测试

```bash
python -m venv .venv
source .venv/bin/activate        # Windows：.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## ✦ 运行演示

核心决策内核：

```bash
nomos-demo
```

打印人类可读的决策摘要。用 `--decision <file>` 运行 `examples/` 中的任意决策 JSON（例如 `nomos-demo --decision examples/baidu_org.json`），用 `--json` 获取完整的机器可读结果：

```bash
nomos-demo --decision examples/baidu_org.json --json
```

NOMOS（智能决策中枢）含两个压力场景：

```bash
nomos-hub-demo
```

## ✦ Python 用法

```python
from second_perspective import IntelligentDecisionHub
from second_perspective.models import HubAnalysisRequest

request = HubAnalysisRequest.model_validate(
    {
        "decision": decision_payload,
        "scenarios": [
            {"id": "SC1", "name": "关键假设失效", "failed_assumption_ids": ["A1"]},
            {"id": "SC2", "name": "成本冲击", "metric_overrides": {"S2": {"capital_required": 6000000}}},
        ],
    }
)
report = IntelligentDecisionHub().analyze(request)
```

返回的报告包含基线决策记录、场景结果、认知发现、信息优先级、算法账本验证状态、策略快照与报告哈希。

## ✦ 运行 API

本地开发无需密钥：

```bash
export SP_ENV=development
uvicorn second_perspective.api.main:app --reload
```

生产环境缺少密钥将拒绝启动：

```bash
export SP_ENV=production
export SP_API_KEY="replace-with-a-strong-secret"
uvicorn second_perspective.api.main:app --host 0.0.0.0 --port 8000
```

受保护的客户端发送 `Authorization: Bearer <SP_API_KEY>`。

端点：

- `GET /health`
- `GET /v1/auth/me`
- `POST /v1/hub/analyze`
- `GET /v1/hub/reports/{hub_run_id}`
- `POST /v1/decisions/evaluate`
- `GET /v1/decisions/{decision_id}`
- `GET /v1/decisions/{decision_id}/history`
- `POST /v1/decisions/{decision_id}/approval`

可选的 PostgreSQL 持久化：设置 `SP_DATABASE_DSN`（`asyncpg`）；OIDC 感知身份：设置 `SP_OIDC_ISSUER`。

## ✦ 重新生成 OpenAPI Schema

```bash
SP_PUBLIC_BASE_URL=https://decision.example.com \
python scripts/export_openapi.py
```

## ✦ 兼容性

所有 v0.2 决策请求与端点仍然有效。响应新增 `counterfactuals`、`algorithm_audit`、`algorithm_audit_root_hash`。严格反序列化响应字段的客户端需更新其模型。

## ✦ 生产边界

v0.7 是一个功能完备的<em>确定性决策框架</em>，并附带企业控制平面与十算子认知审计内核。二阶因果层、形式化收敛与 LLM 护栏均已达到生产级。上述控制面能力（持久化事件存储、租户隔离、OIDC 与授权强制、KMS 签名、限流、可观测性、备份/迁移、领域控制包）已在 v0.5 中以 opt-in 方式提供。

剩余的生产加固项（尚未捆绑）：共享/云原生限流存储（如 Redis）、基于云 KMS 的信封加密、文档级（而非仅事件级）按租户分区、多区域高可用，以及 SLA 工具。

硬边界（不变式，而非未来工作）：

- 引擎从不估计缺失的交互强度、权重、概率或责任方。
- <strong>LLM 永不裁决</strong>：T2 提案需要显式人工批准；T3 叙述从决策图中剥离；任何 LLM 输出都不能翻转假设状态或备选方案的排序。
- `BUDGET_EXHAUSTED` 报告为<em>非收敛</em>；客户端不得将其误标为收敛。
- 认知扫描器只挑战结构性风险。它不诊断人、不读取动机，也不替代法律、医疗、金融或安全专业人士。

## ✦ 项目结构

```
nomos/
├── pyproject.toml              # 包：nomos-decision-engine v0.7.0
├── CHANGELOG.md                # 版本化变更日志
├── src/second_perspective/
│   ├── cli.py / hub_cli.py     # 演示入口（nomos-demo / nomos-hub-demo）
│   ├── service.py / repository.py / canonical.py / version.py
│   ├── api/                    # FastAPI：main.py、security.py
│   ├── audit/                  # auditor、execution、graph、ledger
│   ├── convergence/            # checker（五态分类）、propositions（P-1/P-2/P-3）、enums
│   ├── decision/               # causal、counterfactual、engine、evaluator、
│   │                           #   integrity、policy、robustness、selection、
│   │                           #   reconstruction（三层）
│   ├── governance/             # approval
│   ├── hub/                    # orchestrator、cognitive、information、integrity、
│   │                           #   policy、repository、scenario、session（闸门）
│   ├── interaction/            # engine（I-1..I-4）、model、validator、types
│   ├── llm_compliance/         # gate（T1/T2/T3）、invariants（L-1..L-3）、provenance、types
│   ├── models/                 # enums、hub、schemas
│   └── persistence/            # asyncpg PostgreSQL 仓库（SP_DATABASE_DSN）
├── docs/                       # DECISION_FOUNDATION_V0_2.md、INTELLIGENT_DECISION_HUB_V0_4.md、
│                               #   INTELLIGENT_DECISION_HUB_V0_4.md
├── examples/market_entry.json  # 示例决策请求
├── scripts/export_openapi.py
├── tests/                      # test_api / test_engine / test_hub / test_interaction /
│                               #   test_convergence / test_llm_compliance / test_v04_integration
├── Dockerfile · docker-compose.yml · openapi-action.yaml
├── requirements-engine.txt · requirements-engine-dev.txt
├── IMDA_AI_Verify_Causal_Audit_Report.pdf
└── assets/                     # banner.svg/png、overview.svg/png
```

<p align="center">— ✦ —</p>


<p align="center">— ✦ —</p>

## ✦ 许可与授权

本仓库<strong>并非开源</strong>。双轨模式：个人非商业研究免费；政府 / 企业需付费商业许可。详见 [LICENSE](./LICENSE) —— 许可方与适用法律取决于用户所在地（中国境内 → 上海霖铭均华科技有限公司，中国法律；境外 → NOHN AI TECHNOLOGY PTE. LTD.，新加坡法律 + SIAC 仲裁）。

- **申请许可**：国际 / 全球 —— <ai@nohnlins.com> · 中国 —— <lin@secondai.top>

合规文档：

中国（PRC）：

- [上海合规说明](./docs/COMPLIANCE_SHANGHAI.md)
- [隐私政策（中）](./docs/PRIVACY_POLICY_CN.md)
- [数据处理协议（中）](./docs/DATA_PROCESSING_AGREEMENT_CN.md)

国际 / 全球：

- [EU AI Act 合规说明](./docs/COMPLIANCE_EU_AI_ACT.md)
- [隐私政策（国际 · GDPR）](./docs/PRIVACY_POLICY_INTL.md)
- [数据处理协议（国际 · GDPR）](./docs/DATA_PROCESSING_AGREEMENT_INTL.md)
- [隐私政策（新加坡 · PDPA）](./docs/PRIVACY_POLICY_SG_PDPA.md)

框架对齐（非约束性参考）：

- [NIST AI RMF 1.0 映射](./docs/COMPLIANCE_NIST_AI_RMF.md)
- [ISO/IEC 42001:2023 对齐](./docs/COMPLIANCE_ISO_42001.md)

<p align="center">  
  <a href="https://github.com/nohn3043-arch">GitHub</a> · <a href="https://www.nohnlins.com">官网</a> · <a href="mailto:ai@nohnlins.com">ai@nohnlins.com</a>  
</p>  
<p align="center"><sub>NOHN AI · NOMOS</sub></p>
