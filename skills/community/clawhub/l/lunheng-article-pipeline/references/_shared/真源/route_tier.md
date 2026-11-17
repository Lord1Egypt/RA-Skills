> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 模型路由三档（route_tier）—— Phase 0 探活 + 主人选择单一真源

> **背景（v2.15.13，反哺 FB-10/FB-11/R-04，2026-10-06 实测）**：Phase 0 顶配档探活已运行并发现仅 2 族可用（kimi-k3 = 429 额度耗尽 / glm-5.3 = timeout / kkaiapi = model not allowed），主人 16:21 拍板「降格接受」；但 17:38 T7 换族重派使独立性二次降级时**未回主人确认**，18:40 T9 第 1 次因 429 配额耗尽失败后跨族重试**无规则可依**（靠派发话术临场声明）。三处补救均为话术驱动，无字段承载。
> **定位**：本文件是「三档路由就绪性探活 + Phase 0 主人选择 + fallback 升级链」的**单一真源**。`模型候选池.md` §二·补（顶配档探活门）扩展接线到本文件；`SKILL.md` Phase 0 段、`dispatch-header.md`、`phase-order/t9_review.yaml` 只引用不重列（一条款一真源，防漂移）。
> **零 exec 口径**：探活 = 主控按 [`模型候选池.md`](模型候选池.md) §二 静态映射 + 宿主可见元数据（`session_status` 等**只读工具**）推理判定 + 本文件 §二 探活口径；**不跑 shell、不直连 provider 计费/配额 API、不做逐模型余额探测**（与候选池 §三 同口径）。

## 一、三档定义

| 档 | 名称 | 选择逻辑 | 适用 | 风险 |
|---|---|---|---|---|
| **T1 默认继承** | 同模型同族 | 派发时不指定模型，子代理沿用主对话当前模型 | 常规巡查 / 复制 / 低风险子任务 | 主对话模型**欠费即全链中断**，无隔离 |
| **T2 同平台换能力** | 同 provider 不同 model | 派发指定同 provider 其它 model（按候选池能力档梯度） | 深度推理 / 长上下文 / code 等能力型任务 | 同平台配额共享；账户级限流时仍整族失败 |
| **T3 跨平台换族** | 不同 provider 族 | 派发显式指定异族 provider/model | **T9 盲审、T7 审计等独立性强制节点**；兜底重试 | 风格漂移；凭据池维护成本 |

## 二、Phase 0 三档路由就绪性探活（顶配档探活门的扩展）

位置与口径继承 [`模型候选池.md`](模型候选池.md) §二·补（Phase 0 后置、spawn 前、≤3 次、间隔 ≥10s、结果含时间戳写任务简报 §模型映射、超 1 小时重探），并扩展三档：

1. **T1 探活**：主对话当前模型本轮可 spawn（静态映射确认在列即过，不做实弹）。
2. **T2 探活**：主对话同 provider 至少 1 个备 model 可被指派（候选池 §二 映射结果）。
3. **T3 探活（族数按独立性要求拆两档；两判据独立成立，**不得**互相顶替）**：
   - `writer_audit_distinct_families ≥ 2` = **写手族 ≠ 审计族**（T5 写手与 T7/T9 不同族）—— **最小池 2 族**；
   - `audit_full_independence_families ≥ 3` = **T6 / T7 / T9 三节点两两互异**（批判 / 审计 / 评审各占一族）—— **最小池 3 族**。

   > ⚠️ **算术纪律（2026-10-08 审计 R-4 修）**：原文写「至少 2 族可满足 T6/T7/T9 三节点两两互异」是**错的** —— 三节点两两互异需 **3 族**；2 族只能满足「每族至多承载 1 个独立节点」。按原文，主控会把 2 族误判为 T3 探活通过。实测 2026-10-06 即 2 族（deepseek / minimax）⇒ T6 与 T9 同族 ⇒ 仅「信息独立达成 / 模型独立性不成立」，已由该次 `final/交付说明.md` 披露。

   探活结论**分档分别**记录：`families_available: <N>` + `writer_audit_distinct: pass | degraded` + `audit_full_independence: pass | degraded`。**N=2 时 `audit_full_independence` 必判 `degraded`，不得判 `pass`**；N=1 时两判据均 `degraded`。

**探活产出**：`run/<项目名>/01-任务简报.md` §模型映射 段记三档结果 + 配额水位档位符号（✅/⚠️/❌，**不留具体数值**，遥测收容口径同 `关键协议.md` §遥测收容）。

**失败处置（不静默）**：任一档不可用 ⇒ Phase 0 **当场告知主人**降级路径（如「T3 仅 1 族 ⇒ T6/T7/T9 无法两两互异」），与顶配探活门三选一合并呈现，**不得 Phase 4 才披露**（实测教训：17:38 T7 换族独立性二次降级仅靠 T7 报告事后披露）。

> 📌 **`degraded` 判档的处置**（2026-10-08 审计 R-4 补）：`audit_full_independence: degraded`（N=2）本身即**属本节「失败处置」面** —— 必须在 Phase 0 当面告知「T6/T7/T9 只能部分互异，将产生同族节点」，并把「接受部分同族（须写 `final/交付说明.md` 独立性降级披露）/ 停摆 / 放宽」并入三选一。**禁止**把 N=2 静默记为通过、留到 Phase 4 再披露。

## 三、Phase 0 主人选择（owner 在环，agent 不静默自决）

Phase 0 弹「模型路由方案」选择（并入 checkpoint-card 呈现，**探活结果随卡附上**）：

```
T1 ▸ 继承主对话当前模型（<模型名>）—— 成本最低；欠费即全链中断
T2 ▸ 同平台换能力子模型（<备 model>）—— 能力梯度；同账户配额共享
T3 ▸ 跨平台换族（<可用族清单>）—— 独立性节点必需；单点失败完全隔离
自动建议：默认链 T1→T2→T3；T9/T7 固定 T3；其余默认 T1、失败自动升级
主人选择：[1] 接受自动建议（默认） [2] 全程 T1 禁升级 [3] 全程 T2 [4] 关键节点 T3+其余 T1 [5] 自定义
```

**记录**：选择结果写任务简报 §模型映射 `phase0_route:` 段（`profile` / `route_table{default, fallback_chain, pinned_tier}` / `probe` 时间戳 / `families_available` / `writer_audit_distinct` / `audit_full_independence` / **`selected_by: owner`**）。

> 🚫 **取消「无记录 = 走默认」（2026-10-08 审计 R-5 收口，fail-closed）**
> 原口径「无记录 = 按 [1] 默认链执行并披露『未显式选择，走默认』」与本仓全局纪律 **`silence_is_not_valid_decision`**（`phase-order/index.yaml` 顶层）/「静默 ≠ 决策」正面冲突：它让「**没被呈现**」「**呈现了但漏记录**」「**主人主动选 [1]**」三态在留痕层不可分 —— 同一缺陷已在 `phase0_definition` / `phase5_acceptance` 用 `pending_owner_halt` 修掉，唯独本处留了 fail-open 尾巴。
> **现口径**：`phase0_route` 段缺记录（或 `selected_by` 为空）⇒ **视同未过 Phase 0 后置**，`pre_spawn_enforcement` 判 **`path_or_param_error`** 并 `halt` 呈主人；修齐后重跑该节点，**不得**以默认链兜底推进。
> **选项 [1]「接受自动建议」保留**，但**必须由主人点选并落 `selected_by: owner`** —— 「默认」只能是**主人选出来的默认**，不是系统兜底。

## 四、fallback 升级链（运行时）

| 失败类型 | 判据（子代理自报 / spawn 回执） | 动作 | 计入 retry_limit？ |
|---|---|---|---|
| 配额 / 余额类 | 429 quota / 402 / `insufficient_balance` | 升 fallback_chain 下一档（换族优先，候选池 §三） | **不计入**（FB-11：配额类 ≠ 同质失败） |
| provider 限流 | 429 rate_limit | 退避 60s 重试本档 ≤3 次 → 升档 | 计入（≤3） |
| 模型不可用 | 404 / `model_not_found` | 立即升档 | 不计入 |
| 任务级失败 | spawn 成功但产物不达标 | 升档（独立性节点见下条约束） | 计入（≤2） |
| 执行器级失败 | 工具调用失败率高 | **不升档**，走 `permissions.md` §执行器降级路径 | — |

**独立性保护（硬约束）**：T9 / T7 等 `pinned_tier: T3` 节点的 fallback **只允许在 T3 池内换 provider**，禁止降回写手族；T9 失败处置唯一出口仍是 `t9_review.yaml` `independence_failure_policy`（只能重试 spawn、禁主控代笔）——本文件不放宽该条。
**中途换族回确认**：Phase 0 已选 `fallback_chain` = 预授权，运行中按链升档后**披露即可**（status 记 `route_degraded: T1→T2` 类）；**链外**换族（如 T7 静默后临时换族致独立性降级）⇒ 必须回主人确认（对应 17:38 实测缺口）。
**留痕三处**：产物头部标注 / `status.md` 模型分配表记 `route_degraded` / `final/交付说明.md` 披露实际路由路径与升档次数。

## 五、与既有条款的关系

- [`模型候选池.md`](模型候选池.md) §二·补 = 探活执行口径；§三 = 换族优先 + 族级独立性判据 + 断路器（本档表与其叠加执行，冲突以候选池为准）。
- `phase-order/index.yaml` `provider_silence_escalation`（同 provider 连续静默 ≥3 次三选）继续独立生效；本文件管「路由档位」，它管「静默升级」，互补不替代。
- T9 quota_class_retry 详规 = `phase-order/t9_review.yaml` `independence_failure_policy`（本文件只索引）。
