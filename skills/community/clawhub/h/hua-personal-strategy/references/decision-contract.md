# 决策与资金内核契约

## 目录

- 决策顺序
- 目标带与金额
- 动作协议
- `decision_result.v1`
- 输出模板

## 决策顺序

1. 数据版本和分析门槛；
2. 用户政策状态与版本；
3. AI 观点、证据和 critic；
4. 同日自由现金；
5. 在途交易后的预计持仓；
6. 政策确认的回撤口径、软/硬风险线和 MCP 因子共识；
7. 战略目标带、分阶段风险收缩与受限 AI 战术变化；
8. 优先用新增现金补低配袖套；
9. 必要时降低超配或风险越界袖套；
10. 基金侧申赎、限购、QDII 与执行窗口；
11. 独立恒真条件验证。

当前 v4.3.0 只在政策批准的现有持仓基金中选择表达。新增基金、同袖套替换和全市场候选必须先经过单独研究、交易约束读取和政策批准，不能由名称匹配临时加入。

## 目标带与金额

战略目标来自用户确认的 `assetSleeves`。AI 只能在 `tacticalBudgetPct` 内提出变化；变化必须缩放到全部袖套仍满足上下限且合计 100%，现金袖套吸收其余变化。回撤越过用户有效硬上限时，高风险袖套只能向 `minWeightPct` 收缩，不能新增。政策启用 `DYNAMIC_REDUCE` 时，回撤越过软触发线后，内核必须先以 `fund_trend_consensus_v1` 判断具体袖套：

- 只读取同轮 MCP 基金指标的 `r20Pct`、`r60Pct`、`bias20Pct` 与 `ma20/ma60`；
- 每项因子覆盖市值至少 80%，同向市值至少 60% 才记为正向或不利；
- 不利因子达到政策门槛后，按已确认的因子数量—减仓步长表降低该袖套目标；
- 一轮只选择最严重的一个袖套，步长不超过袖套下限、现金上限与单笔交易上限；
- 因子缺失时不得猜测下行，也不得用 AI 文本替代服务端指标。

回撤比较必须先统一分母。`drawdownBasis.scope=MCP_FUND_PORTFOLIO` 时，有效回撤等于 MCP 原始回撤，且 MCP 配置上限必须与政策上限一致。`scope=TOTAL_INVESTABLE_ASSETS` 时，当前 MCP 只提供基金子组合回撤，因此 `STATIC_CASH_PROXY_V1` 使用：

```text
fund peak proxy = current MCP fund value / (1 - MCP fund drawdown)
non-MCP assets = total investable assets - current MCP fund value
total peak proxy = fund peak proxy + non-MCP assets
effective total drawdown = (total peak proxy - total investable assets) / total peak proxy
```

该代理明确假设非 MCP 资产自基金峰值以来保持不变，并把 MCP 的链接日收益回撤作用于当前基金市值以反推代理峰值。原始基金回撤仍写入 `sourceMcpDrawdownPct`，有效代理值写入 `currentDrawdownPct`；软线和硬线只比较有效值。原始 MCP 配置上限与总资产政策上限分母不同，不做跨口径冲突比较。缺少政策口径、回撤无效、基金市值无效或基金市值大于总可投资资产时返回 `NEEDS_PROFILE` 或 `BLOCKED`，不得触发金额。

确认后基金市值：

```text
current fund market value
+ pending BUY amount
- pending SELL amount
```

总可投资资产：

```text
sum(post-pending fund values)
+ same-day user-confirmed free cash
+ pending SELL proceeds not yet reusable
```

买入建议：

```text
sleeve gap = total investable assets × tactical target weight - post-pending sleeve value

cap = min(
  same-day free cash,
  sleeve gap,
  policy max-one-trade amount,
  policy monthly-turnover remaining capacity,
  remaining single-fund capacity,
  fund daily purchase limit
)

amount = floor_to_platform_step(max(0, cap))
```

启用动态换手时，普通交易的月度额度先按不超过 `maxMonthlyTurnoverPct` 的 0%–上限分档：因子一致数量决定因子上限，AI 置信度只能进一步缩小，二者取更低值。战略带越界使用普通硬上限。若已确认 `riskReductionExempt=true`，`RISK_REDUCE` 不计普通换手额度；它仍受单笔上限、实际持仓、赎回状态和用户确认约束。

已有持仓若超过 `maxSingleFundWeightPct`，或普通权益加主题权益超过 `maxEquityWeightPct`，或主题权益超过 `maxThemeWeightPct`，必须生成 `STRATEGIC_REBALANCE`。一轮选择最严重的一个越界项，金额以越界缺口为起点，并继续受单笔、持仓和执行门禁约束。

卖出建议使用目标超额、单笔上限和确认后基金持仓的最小值。金额低于政策 `minTradeCny` 或基金最低申购额时改为 `HOLD`。不得使用 500、1,000 等固定档位。

`cash.availableCny` 必须是用户本轮同日确认、已经排除在途买入和其他用途后的自由现金。缺失、过期或来源不是 `user_confirmed` 时，买卖方向可保留，`amountCny` 必须为 `null` 并返回 `BLOCKED`。

任何交易还必须提供同日活动账本。旧输入的 `activity.monthlyTurnoverUsedPct` 全部视为普通换手；`portfolio_activity.v2` 则要求 `gross = ordinary + protective_sell + risk_off_reentry`，分类事件金额与交易 ID 必须和完整账本一致。普通交易使用普通桶剩余额度；风险减仓即使获得豁免，也保留总换手审计。缺失或分类不守恒时返回 `BLOCKED`。

风险后再入场金额：

```text
re-entry remaining pct = min(
  policy max monthly re-entry pct - used re-entry pct,
  classified protective-sell pct - used re-entry pct
)

cap = min(
  re-entry remaining amount,
  same-day free cash,
  sleeve gap,
  policy max-one-trade amount,
  remaining single-fund capacity,
  fund daily purchase limit
)
```

该通道只在普通买入额度不足时评估。保护性卖出必须发生在此前日期且属于当前月；基金正向因子、AI 方向和置信度必须达到政策 `riskOffReentry` 门槛。它不是普通换手豁免，更不是卖多少就自动买回多少。

## 动作协议

| 动作 | 含义 |
|---|---|
| `HOLD` | 在目标带内或交易小于最小有效金额；明确保持不动 |
| `CONTRIBUTION_REBALANCE` | 用新增现金补最重要的低配袖套 |
| `STRATEGIC_REBALANCE` | 存量仓位越过长期目标带 |
| `RISK_REDUCE` | 组合越过硬风险线，或越过软风险线且下行因子达到确认门槛 |
| `TACTICAL_ROTATE` | AI 观点在战术预算内改变目标 |
| `REENTRY_AFTER_RISK_OFF` | 已分类保护性降仓后，在右侧因子和独立再入场预算内分批恢复 |
| `FUND_REPLACE` | 同袖套基金表达升级；首版默认阻断直至专项研究完成 |
| `BLOCKED` | 方向存在但今天不能执行 |
| `DATA_BLOCKED` | 数据不足，不能形成完整结论 |
| `NEEDS_PROFILE` | 政策缺失或需要复核 |
| `AI_MODEL_BLOCKED` | AI 研究能力或反方审查不合格 |
| `ENGINE_BLOCKED` | 资金内核不可用 |
| `INVALID_DECISION` | 恒真条件失败 |

`HOLD` 是首选方案，不是空结果。普通策略不得生成 `SELL_ALL`。

## `decision_result.v1`

```json
{
  "schemaVersion": "decision_result.v1",
  "status": "VALID",
  "executionMode": "ACTIVE",
  "action": "CONTRIBUTION_REBALANCE",
  "scope": "a-share-core",
  "fundCode": "000000",
  "fundName": "基金名称",
  "amountCny": 500,
  "currentWeightPct": 8,
  "targetWeightPct": 10,
  "targetBandPct": [9, 11],
  "changeWeightPct": 2,
  "drivers": ["SLEEVE_UNDERWEIGHT", "FREE_CASH_AVAILABLE"],
  "blockers": [],
  "confidence": "MEDIUM",
  "validUntil": "2026-07-22T14:55:00+08:00",
  "nextReviewAt": "2026-08-01",
  "dataAsOf": "2026-07-22",
  "amountTrace": {
    "rawGapCny": 820,
    "availableCashCapCny": 1200,
    "oneTradeCapCny": 500,
    "singleFundCapacityCny": 1000,
    "purchaseLimitCapCny": 1000,
    "effectiveCapCny": 500,
    "amountStepCny": 10
  },
  "invalidationTriggers": [],
  "audit": {
    "policyVersion": 3,
    "strategyVersion": "4.3.0",
    "engineVersion": "4.3.0",
    "aiModelVersion": "provider/model-version",
    "aiPromptVersion": "hua-investment-research-v1",
    "evidenceSetHash": "sha256",
    "contextHash": "sha256",
    "canonicalInputHash": "sha256",
    "canonicalOutputHash": "sha256"
  }
}
```

影子状态中，外层 `amountCny` 必须为 `null`；内部可以保存 `shadowAmountCny` 用于复盘，但不能展示成真实交易指令。

验证器至少检查：

- 目标权重非负、合计 100%、均在政策上下限；
- 普通权益与主题权益合计不超过权益总上限，主题权益合计同时不超过主题上限；
- 金额不超过自由现金、目标缺口、单笔上限、单基金容量和申购上限；
- 买入后不突破袖套/单基金上限，卖出不超过确认后持仓；
- `readyForAction=false`、截止时间关闭、侧向门禁失败或同向在途交易时无金额；
- 标的在政策批准基金池并映射到动作袖套；
- 现金、政策上限、数据时点或基金约束未知时金额为 `null`；
- 软风控因子只能来自 MCP 指标；动态换手额度不得超过普通硬上限，风险减仓豁免时仍不得突破单笔上限；
- `portfolio_activity.v2` 各桶合计必须等于总换手，分类事件必须唯一；再入场不得超过保护性卖出余额、政策再入场余额和普通单笔上限；
- 软/硬回撤必须使用政策确认的同口径有效值；总资产代理必须保留 MCP 原始值、资产分母、转换方法和假设；
- 数据没有来自未来；
- 正文不能生成第二笔引擎之外的“顺手建议”。

## 输出模板

> **今天建议：加仓 XXX 基金（000000）500 元。**
>
> **为什么：** 该袖套低于本轮目标；组合风险仍在个人上限内；政策批准且申购与交易窗口可用。
>
> **金额依据：** 目标缺口 820 元，自由现金 1,200 元，单笔上限 500 元，每日申购上限 1,000 元，因此取 500 元。
>
> **主要风险：** AI 对该袖套的中期判断可能错误；若长期趋势破坏或组合回撤越线，结论失效。
>
> **有效期：** 今日 14:55 前；过期后重新取数。

事实、AI 推断和政策约束要能区分。首屏不展示内部码、原始 JSON、工具轨迹或十四章报告。深度审计按需展开。

所有用户可见的基金引用必须写成“基金原名（6位代码）”，或在同一组件内同时展示原名与代码。即使前文已经出现过，也不得在风险说明、条件、时间线或审计入口中只写裸代码。原始 JSON 链接必须标明“机器审计数据（JSON）”，并说明它不是程序源码、日常阅读无需打开。
