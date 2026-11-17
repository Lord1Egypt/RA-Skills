<div align="center">

# 📖 术语表 · Glossary

**NOMOS · Second-Perspective**

*每个词都用一句人话解释 · Every term explained in one plain sentence*

</div>

---

> 英文术语保留原样，方便你对照 README、文档与代码。
> The English term is kept as-is so you can match it against the README, the docs and the code.

| 术语 Term | 中文 | 一句话人话 · Plain meaning |
|---|---|---|
| **NOMOS** | 决策中枢 | 一个「不猜、不学」的确定性决策内核——它给候选，不给结论。 |
| **IMDA AI Verify** | 新加坡 AI 合规评估 | IMDA 发布的测试框架；NOMOS 依据该框架自行评测为 95/100（提供方自测）。 |
| **Deterministic** | 确定性 | 同样的输入永远给同样的输出，没有随机、没有学习。 |
| **First-order invalidation** | 一阶失效 | 某个假设被推翻后向前传播，丢掉依赖它的那些备选方案。 |
| **Second-order interaction** | 二阶交互 | 假设与假设之间的相互影响，而不把失败当成互不相干的独立事件。 |
| **Synergy / Redundancy / Amplification** | 协同 / 冗余 / 放大 | 多个假设一起失效时，效果比简单相加更强、更弱、或不成比例。 |
| **Δ (interaction strength)** | 交互强度 | 二阶影响的大小，**必须由责任人显式声明**，引擎绝不估算也绝不学习。 |
| **I-1 … I-4** | 四条不变量 | 非臆测 · 阶数守恒 · 效应有界 · 单调——约束二阶交互不许乱来。 |
| **Three-layer reconstruction** | 三层因果重建 | 前向失效传播 + 后向根因追溯 + 增量重建；一轮跑一层。 |
| **DeltaVar** | 修正变量 | 由人声明的修正项，引擎逐字照做，绝不自行发明修正。 |
| **ConvergenceChecker** | 收敛判定器 | 用五个状态正式判定「到底收敛了没有」，而不是靠启发式猜测。 |
| **FIXED_POINT / NO_GAIN** | 定点 / 无增益 | 真正收敛的两种状态。 |
| **BUDGET_EXHAUSTED** | 预算耗尽 | 预算用完 **≠** 收敛，绝不允许被当成收敛上报。 |
| **DIVERGED / BLOCKED** | 发散 / 阻塞 | 仍在变化，或撞上结构性问题、必须由人介入。 |
| **P-1 / P-2 / P-3** | 三条命题 | 终止性 · 不动点 · 效应有界——收敛判定背后的数学依据。 |
| **session_root_hash** | 会话根哈希 | 把整轮会话串成一条哈希链的根；改任何一个字都对不上。 |
| **Human gate** | 人工闸门 | 每轮只推进一步就停下，必须由人签字才能进入下一轮。 |
| **LLM Gate (T1/T2/T3)** | 大模型护栏 | 批注 / 提议 / 叙述三档权限；LLM 永远不能裁决，也不能翻转状态或排名。 |
| **Provenance-tracked** | 可溯源 | 每条 LLM 输出都带来源标记，并被剥离了结构权力。 |
| **Counterfactual re-selection** | 反事实重选 | 「如果当时不是这样，结果会怎样」的重新演算。 |
| **Pareto / weight sensitivity** | 帕累托 / 权重敏感度 | 看哪个指标或权重一变，就会改变排序结果。 |
| **DecisionRecord** | 决策记录 | 只追加的决策档案，配合哈希链可被独立复验。 |
| **Domain control pack** | 领域控制包 | 可插拔的行业规则包（如金融风控）——只观察，绝不改判。 |
| **Tenant isolation** | 租户隔离 | 多租户数据互不可见，按 `X-Tenant-Id` 分区。 |
| **KMS signing** | 密钥托管签名 | 用 KMS 给产出物盖上 HMAC-SHA256 签章，防篡改。 |

---

## ✦ English Glossary

*Every term explained in one plain sentence.*

| Term | Plain meaning |
|---|---|
| **NOMOS** | A deterministic decision core that neither guesses nor learns — it offers candidates, never conclusions. |
| **IMDA AI Verify** | The IMDA-published test framework; NOMOS is self-assessed at 95/100 against it (self-assessed by the provider). |
| **Deterministic** | Same input always gives the same output — no randomness, no learning. |
| **First-order invalidation** | When an assumption is overturned, the invalidation propagates forward and drops every option that depended on it. |
| **Second-order interaction** | How assumptions affect each other, instead of treating failures as unrelated independent events. |
| **Synergy / Redundancy / Amplification** | When several assumptions fail together, the effect can be stronger, weaker, or out of proportion to a simple sum. |
| **Δ (interaction strength)** | The size of a second-order effect; **it must be declared explicitly by the responsible person** — the engine never estimates or learns it. |
| **I-1 … I-4** | Four invariants: non-conjecture · order conservation · bounded effect · monotonicity — they keep second-order interaction from running wild. |
| **Three-layer reconstruction** | Forward failure propagation + backward root-cause tracing + incremental rebuild; one layer per round. |
| **DeltaVar** | A correction term declared by a human; the engine applies it verbatim and never invents corrections of its own. |
| **ConvergenceChecker** | Formally decides whether convergence happened, using five states rather than heuristic guessing. |
| **FIXED_POINT / NO_GAIN** | The two states that count as truly converged. |
| **BUDGET_EXHAUSTED** | Running out of budget **≠** convergence, and it is never allowed to be reported as such. |
| **DIVERGED / BLOCKED** | Still changing, or stuck on a structural problem that needs a human to step in. |
| **P-1 / P-2 / P-3** | Three propositions: termination · fixed point · bounded effect — the mathematical basis behind convergence. |
| **session_root_hash** | The root that strings a whole session into a hash chain; change a single character and it no longer matches. |
| **Human gate** | Each round advances exactly one step and stops; a human signature is required to move on. |
| **LLM Gate (T1/T2/T3)** | Three permission tiers — annotate / propose / narrate; an LLM may never adjudicate, flip a state or change a ranking. |
| **Provenance-tracked** | Every LLM output carries a provenance mark and has been stripped of structural power. |
| **Counterfactual re-selection** | Recomputing "what would the result have been if it hadn't been this way". |
| **Pareto / weight sensitivity** | Finding which metric or weight, when changed, would alter the ranking. |
| **DecisionRecord** | An append-only decision file that, together with the hash chain, can be independently re-verified. |
| **Domain control pack** | A pluggable industry rule pack (e.g. financial risk control) — it only observes, never overrules. |
| **Tenant isolation** | Multi-tenant data is mutually invisible, partitioned by `X-Tenant-Id`. |
| **KMS signing** | Outputs are stamped with an HMAC-SHA256 signature via KMS to prevent tampering. |

---

<div align="center">

[← 返回说明文档](./README-zh.md)

<sub>NOHN AI · NOMOS</sub>

</div>
