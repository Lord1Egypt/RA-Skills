# Source and Language Guards

Use this when a generated requirement contains details that may not be sourced, when data origin is unclear, or when technical / abstract language appears.

## Requirement Source Trace

Every generated detail needs a source:

| Detail Type | Examples | Required Source |
|---|---|---|
| Interaction | 可勾选、默认全选、可批量、可导出 | User confirmed, existing UI convention, design.md, or recommendation marked待确认 |
| Data | 未发运单、可开票明细、待处理数 | System/object/table/interface, authoritative source, filters, refresh timing |
| State | 待处理、已完成、有效、未发 | State field, enum/business meaning, display text |
| Default | 默认全选、默认今天、默认当前组织 | Default rule, risk, whether user can change |
| Statistic | 成功率、失败数、覆盖率 | Object, period, include/exclude states, dedupe, refresh |
| Extension | New state/field/page/component/exception not directly stated by user | User confirmation, business anchor, source data, existing system behavior, research recommendation, or待确认 |

Use:

| Requirement Item | Added Detail | Source Type | Evidence / Source | Confirmed? | If Unconfirmed |
|---|---|---|---|---|---|

Do not treat "best practice" as a source of truth. It is a recommendation until it is checked against the business anchors and confirmed.

## Data Source Table

For lists, fields, stats, defaults, filters, and options:

| Data Item | Scene | Source System/Object/Table/API | Authoritative Source | Generation / Calculation | Include / Exclude | Refresh Timing | Fallback | Confirm? |
|---|---|---|---|---|---|---|---|---|

## State Axis Lifecycle Guard

Do not define a shared "status" by mixing lifecycle stages from different business axes. For every object, start from the object's creation point and check whether there are stages before audit, payment, invoicing, push, or settlement.

Before writing a status table, answer:

| Check | Required Question |
|---|---|
| Object birth | When is this object created, and by which source document / action? |
| Initial state | What is the first business state after creation? |
| Pre-audit stage | Is there a business confirmation, calculation, matching, claim, signing, or submission step before audit? |
| Axis owner | Which role/system changes this axis: user, operator, finance, platform, channel, third party? |
| Trigger | What action/event moves the object to the next state? |
| Terminal states | Which states end the lifecycle, and can they be reversed or rebuilt? |
| Display scope | Are the same display labels valid for every listed object, or only for part of them? |

If one object has a meaningful stage before audit, do not include it directly under "audit status" as if it starts at "待审核". Create a separate axis or object-specific lifecycle wording.

Example:

- Bad: Put "成本账单" under audit status with allowed labels "待审核 / 已审核 / 已拒绝".
- Better: Cost bill lifecycle first has "成本确认状态: 待确认", then after contractor confirmation it enters "审核状态: 待审核 / 已审核 / 已拒绝".

When uncertain, write "待确认: 该对象创建后的初始状态和进入审核前的业务阶段需确认" instead of guessing.

## Technical Expression Conversion

Do not put SQL, code enum, interface params, or database fields into PRD正文. Convert them to business language.

| Technical Input | Business PRD Wording |
|---|---|
| `incomeStatus in (CONTRACTOR_PENDING, CONTRACTOR_CLAIMED)` | 展示收入状态为“待承包人处理”或“承包人已认领”的记录 |
| `status = 1` | 展示业务状态为“有效”的记录，具体状态口径待确认 |
| `isShow = true` | 对用户展示该信息 |

If enum meaning is not known, write:

> ⚠️ 待确认：技术枚举 XXX 对应的业务展示文案和状态口径。

## Abstract Business Word Decomposition

Never use abstract words as idempotency keys, unique constraints, filters, or acceptance rules unless decomposed.

High-risk words:

- 计价口径
- 统计口径
- 结算口径
- 规则
- 策略
- 配置
- 版本
- 范围
- 条件

Decompose into fields:

| Abstract Word | Replace With |
|---|---|
| 计价口径 | Rule config ID, rule version, fee item range, source bill snapshot, cost version, tax version |
| 统计口径 | Object, period, include states, exclude states, dedupe, refresh timing |
| 结算口径 | Settlement period, settlement object, source document set, settlement rule version |
| 规则/策略 | Rule ID, name, version, scope, priority, enable state |

Example:

Bad:

> 分润单唯一性：承包人 + 月份 + 计价口径。

Better:

> 分润单唯一性按“承包人 + 分润周期 + 分润规则配置 ID + 分润规则版本 + 来源对账单快照 ID + 成本账单版本”判断。若来源单据集合、成本版本或规则版本变化，是否允许作废后重建待确认。
