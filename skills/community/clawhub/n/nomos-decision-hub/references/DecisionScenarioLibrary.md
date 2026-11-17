# Decision Scenario Library（技能层模板 · 对应 NOMOS 0.7.0）

预置决策场景，降低上手门槛。每个场景定义输入、所用的算子链与验收标准。复制 JSON、
替换内容、运行 hub。

> **定位说明**：本文件是**技能层模板**，不是引擎的输入契约。引擎输入见
> `examples/market_entry.json` 与 `openapi-action.yaml`；算子链由确定性内核固定，
> 模板不可增删算子。

## Scenario 1 — Compliance gate（监管准入）

| Field | Value |
|---|---|
| Question | Should we release this feature under current policy? |
| Inputs | feature spec, policy text, risk register |
| Operators | `NS` → `IAP` → `LCH` → `BFC` → `CCS` → `STATE`（`ORI` 在声明原点时先行注册） |
| Fragility focus | unstated policy exemptions, missing data paths |
| Acceptance | sealed report with ≥2 stress scenarios; verdict explicit; no `medium` confidence without evidence |
| Output | sealed report（见 `SealedReportSpec.md`） |

## Scenario 2 — Strategic bet（市场进入）

| Field | Value |
|---|---|
| Question | Enter market X with product Y? |
| Inputs | market data, competitor map, capability matrix, cost model |
| Operators | 完整十算子；`LCH` 聚焦需求假设与切换成本，`GRF` 需声明灰度阶梯才注册 |
| Acceptance | counterfactual re-selection over ≥3 alternative decisions; sealed report with scenario coverage table |
| Output | sealed report + decision log |

## Scenario 3 — Root-cause trace（事故追溯）

| Field | Value |
|---|---|
| Question | What caused the outage / drift / failure? |
| Inputs | event timeline, logs, config diffs |
| Operators | `NS` → `BFC` → `CCS`（反向根因链） → `STATE` |
| Fragility focus | correlation masquerading as causation |
| Acceptance | causal chain with each link evidenced; no probabilistic language; sealed |
| Output | sealed report |

## Scenario 4 — Resource allocation（预算约束）

| Field | Value |
|---|---|
| Question | How to allocate a fixed budget across N programs? |
| Inputs | program objectives, cost/benefit estimates, constraint set |
| Operators | 完整十算子 + 加权评估（`evaluation/` 的确定性打分，含 Pareto 与权重敏感性） |
| Acceptance | allocation table + sensitivity on top-2 uncertain inputs |
| Output | sealed report + allocation table |

## Usage rule

1. Pick the closest scenario template.
2. Replace content placeholders with real inputs.
3. Run the hub; the ten-operator kernel stays fixed (it is the deterministic core).
4. `META` 只做度量、**永不阻断**；`BUDGET_EXHAUSTED` 不得表述为「收敛」。
5. Every run ends with a sealed report; archive it append-only.
