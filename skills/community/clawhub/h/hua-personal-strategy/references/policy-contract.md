# 用户政策契约

## 目录

- 状态机
- 首次建档
- `investor_policy.v1`
- 状态存储与复核

## 状态机

```text
ABSENT → DRAFT → CONFIRMED → SHADOW → ACTIVE
                              ↑         ↓
                         REVIEW_DUE ← 触发复核
                              ↓
                          SUSPENDED
```

| 状态 | 允许行为 |
|---|---|
| `ABSENT` | 只问第一个建档问题 |
| `DRAFT` | 一次只补一个问题；可解释压力情景，不给交易金额 |
| `CONFIRMED` | 生成战略配置与影子建议，金额不对用户生效 |
| `SHADOW` | 记录建议和结果；`amountCny=null`，不发送交易请求 |
| `ACTIVE` | 在已确认目标带内生成强建议，仍需用户决定真实买卖 |
| `REVIEW_DUE` | 暂停新增风险；允许诊断和风险降低候选 |
| `SUSPENDED` | 不生成调仓金额 |

行情、单次盈亏和短期赚钱不能自动提高风险等级。目标日期临近、资金规模显著变化、连续提款、收入/负债变化、应急资金变化或用户主动修改目标时，进入 `REVIEW_DUE`。

## 首次建档

一次只问一个问题，按以下顺序：

1. 这笔钱最主要用来做什么，预计什么时候使用？
2. 目标金额、当前可投资资产和未来每月/每年预计投入是多少？
3. 是否已经在投资账户之外留足应急资金，未来 12 个月预计取用多少？
4. 最多能接受多大阶段性亏损？用人民币压力场景复述。
5. 发生该亏损时更可能持有、补仓、退出，还是在较低软触发线后按趋势因子分批减仓？
6. 回撤上限按全部可投资资产还是只按 MCP 已买入基金计算？若选择全部资产但尚无总资产历史净值，是否接受静态现金代理口径？
7. 是否允许 A 股、港股/海外、债券、黄金、主动基金和主题基金？有哪些明确排除？
8. 最大权益、主题、单基金、单笔交易和月度换手上限是多少？
9. 希望多久收到一次常规建议和风险检查？是否启用快照归档？

风险预算取“风险能力”和“风险意愿”中更保守的一侧。目标收益与可承受风险不匹配时，明确提出延长期限、增加投入或降低目标，不为追求目标擅自加杠杆或提高权益仓位。

建档完成后必须复述：目标、期限、自由现金、最大回撤人民币金额、回撤计算口径、资产范围、袖套目标带、最小交易、建议频率和真实交易确认方式。只有用户明确确认，才写入 `CONFIRMED` 版本。

## `investor_policy.v1`

示例只说明字段，不代表默认配置：

```json
{
  "schemaVersion": "investor_policy.v1",
  "status": "DRAFT",
  "policyVersion": 1,
  "goals": [
    {
      "id": "long-term-growth",
      "purpose": "长期增值",
      "priority": 1,
      "targetDate": "2036-12-31",
      "targetAmountMode": "FIXED",
      "targetAmountCny": 300000,
      "plannedContributionCnyPerMonth": 2000
    }
  ],
  "riskCapacity": {
    "maxDrawdownPct": 15,
    "emergencyFundReady": true,
    "next12mWithdrawalCny": 0,
    "incomeStable": true
  },
  "riskTolerance": {
    "maxDrawdownPct": 12,
    "stressReaction": "DYNAMIC_REDUCE"
  },
  "drawdownBasis": {
    "scope": "TOTAL_INVESTABLE_ASSETS",
    "method": "STATIC_CASH_PROXY_V1"
  },
  "riskControls": {
    "softDrawdownTriggerPct": 8,
    "softTriggerMode": "DOWNTREND_FACTORS",
    "factorMethod": "fund_trend_consensus_v1",
    "minimumAdverseFactorCount": 2,
    "reductionStepPctByAdverseFactorCount": {"2": 2, "3": 3, "4": 5},
    "dynamicTurnover": {
      "enabled": true,
      "factorMethod": "fund_trend_consensus_v1",
      "tierStepPct": 5,
      "minimumConfirmingFactorCount": 2,
      "riskReductionExempt": true
    },
    "riskOffReentry": {
      "enabled": true,
      "maxMonthlyReentryPct": 10,
      "minimumPositiveFactorCount": 4,
      "minimumAiConfidence": 0.75,
      "allowedAiDirections": ["OVERWEIGHT"]
    }
  },
  "assetSleeves": [
    {
      "id": "a-share-core",
      "label": "A股宽基",
      "assetClass": "EQUITY_CN_CORE",
      "riskLevel": 3,
      "targetWeightPct": 50,
      "minWeightPct": 40,
      "maxWeightPct": 55,
      "tacticalBudgetPct": 5,
      "approvedFundCodes": ["000000"]
    },
    {
      "id": "cash",
      "label": "现金",
      "assetClass": "CASH",
      "riskLevel": 0,
      "targetWeightPct": 50,
      "minWeightPct": 45,
      "maxWeightPct": 60,
      "tacticalBudgetPct": 0,
      "approvedFundCodes": []
    }
  ],
  "fundSleeveMap": {"000000": "a-share-core"},
  "allowedAssets": ["EQUITY_CN_CORE", "CASH"],
  "excludedAssets": [],
  "portfolioLimits": {
    "maxEquityWeightPct": 55,
    "maxThemeWeightPct": 10,
    "maxSingleFundWeightPct": 50,
    "maxOneTradeWeightPct": 5,
    "maxMonthlyTurnoverPct": 15,
    "minTradeCny": 100,
    "amountStepCny": 10
  },
  "interactionPreferences": {
    "adviceMode": "DECISIVE",
    "normalReviewFrequency": "ON_DEMAND",
    "riskCheckFrequency": "ON_DEMAND",
    "requiresUserTradeDecision": true,
    "archiveSnapshots": false,
    "archiveMode": "EXPLICIT_ONLY"
  },
  "confirmedByUser": false,
  "effectiveAt": null,
  "lastReviewedAt": null,
  "nextReviewAt": null,
  "reviewTriggers": []
}
```

硬规则：

- 至少包含一个 `CASH` 袖套；全部 `targetWeightPct` 合计必须为 100。
- 每个袖套满足 `0 ≤ min ≤ target ≤ max ≤ 100`。
- 主题袖套同时计入 `maxThemeWeightPct` 和 `maxEquityWeightPct`；权益总上限必须覆盖普通权益与主题权益的合计，不能通过资产分类绕开。
- 单基金上限同时约束新增买入和已有持仓；已有单基金、主题合计或权益合计越界时，内核只能生成分阶段降低风险的候选，不能等待新增资金稀释后假装合规。
- `tacticalBudgetPct` 只允许 AI 在战略目标附近有限移动，不得突破袖套上下限。
- 所有当前持仓代码必须显式出现在 `fundSleeveMap`；不得从名称猜袖套后直接交易。
- 用户本轮自由现金不写成永久默认值。每次新增建议都需要同日 `cash.availableCny` 与 `source=user_confirmed`。
- `maxDrawdownPct` 不得写死；有效上限取风险能力与风险意愿中更低者。
- `drawdownBasis` 是已确认政策的一部分，不得由运行时模型猜测。只支持两组配对：`MCP_FUND_PORTFOLIO/MCP_REPORTED` 直接使用 MCP 基金子组合回撤；`TOTAL_INVESTABLE_ASSETS/STATIC_CASH_PROXY_V1` 把 MCP 基金回撤转换为总资产代理回撤。
- `STATIC_CASH_PROXY_V1` 假设当前不在 MCP 基金市值内的资产自基金子组合峰值以来保持不变，并把 MCP 的链接日收益回撤作用于当前基金市值以反推代理峰值。它必须同时披露 MCP 原始回撤、代理回撤、基金市值、非 MCP 资产、代理峰值和全部假设，不能声称是精确历史总资产回撤。MCP 后续提供完整总资产净值历史时，应通过新方法版本迁移，不得静默改变公式。
- v4.2.3 之前没有 `drawdownBasis` 的已确认政策必须重新确认口径后生成新版本；旧版本不得被自动补值或继续用于金额建议。
- 没有目标金额时显式写 `targetAmountMode="NONE"` 且 `targetAmountCny=null`；不得把用户已回答的“无目标金额”重新当作缺失值追问。
- `DYNAMIC_REDUCE` 必须同时配置 `riskControls`。软触发线必须低于有效硬回撤线，减仓步长不得超过单笔交易上限。
- `fund_trend_consensus_v1` 只使用 MCP 官方基金指标中的 `r20Pct`、`r60Pct`、`bias20Pct` 和 `ma20/ma60`。每项因子覆盖率至少 80%，同向市值占比至少 60% 才形成共识；缺失不得补成 0 或由 AI 猜测。
- `maxMonthlyTurnoverPct` 是普通交易硬上限。启用动态换手后，本月实际可用额度由因子数量与 AI 置信度中更保守的一侧分档；AI 只能缩小额度。若政策明确 `riskReductionExempt=true`，`RISK_REDUCE` 不受普通换手额度阻断，但仍受单笔上限和执行门禁限制。
- `riskOffReentry` 是可选、需用户确认的政策对象，不得静默补入旧政策。其月度再入场上限不得超过普通月换手上限；只允许 `OVERWEIGHT` 或用户明确批准的 `NEUTRAL` 方向，正向因子和 AI 置信度门槛必须写入政策。
- 保护性卖出仍计入 `grossMonthlyTurnoverUsedPct`，但从普通换手桶分离。再入场使用独立桶，不得把保护性卖出金额直接当成可买金额，也不得允许同日卖出后买回。
- `archiveSnapshots=false` 且 `archiveMode=EXPLICIT_ONLY` 表示默认不归档；只有用户当次明确要求时才保存快照。
- 朋友与本人使用同一 champion 策略，但政策和历史按 Huahua 用户隔离。

## 状态存储与复核

`policy_store.py` 默认使用 `~/.local/share/hua-personal-strategy`，也可通过 `HUA_PERSONAL_STRATEGY_STATE_DIR` 或 `--state-dir` 指定。用户目录只使用 UID 的 SHA-256 短哈希，不在路径中暴露原始 UID。

每次确认或状态迁移追加写入 `policy-events.jsonl`，并原子更新 `current-policy.json`。旧版本不得覆盖。常用命令：

```bash
python3 scripts/policy_store.py status --user-id '<uid>'
python3 scripts/policy_store.py save-draft --user-id '<uid>' --input draft.json
python3 scripts/policy_store.py confirm --user-id '<uid>' --input completed-policy.json
python3 scripts/policy_store.py shadow --user-id '<uid>'
python3 scripts/policy_store.py activate --user-id '<uid>'
python3 scripts/policy_store.py review-due --user-id '<uid>' --reason '目标日期临近'
python3 scripts/policy_store.py suspend --user-id '<uid>' --reason '用户暂停'
python3 scripts/activity_store.py list --user-id '<uid>'
```

`confirm`、`shadow`、`activate` 和恢复操作必须对应用户本轮明确授权。策略复盘不能自行执行状态迁移。
