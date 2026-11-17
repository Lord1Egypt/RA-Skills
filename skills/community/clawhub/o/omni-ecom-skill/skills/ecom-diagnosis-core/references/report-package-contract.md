# 报告包与完成态契约（v1.5.12）

`scripts/build_report_package.py` 是 PDF、PPT、Excel 等交付物的统一上游。它只接受通过 `validate_handoff.py` 的结构化交接，不接受成员的自由文本作为事实来源。

## 输入

- `handoff.json`：必须包含 `run_id`、`scope`、`gate_status`、`status`、事实、判断、行动、缺失数据和 `evidence_ledger`。
- 可选 `metrics_bundle.json`：只使用其中已通过闸门的 `rows`，来源会保留文件名和 SHA256，不公开本机绝对路径。
- 可选行动建议：写入当前报告包并绑定 `run_id`、`client_scope` 和来源。涉及平台动作时另走 `omni-ecom.controlled-action@2.0`、资格检查、可信审批、执行与回读链；`scripts/action_tracker.py` 只读查看 1.x 历史，不能维护当前行动。
- 可选报告配置：只用于标题或展示标签，不能覆盖闸门、指标或行动状态。
- `task_type`：从 `config/task-profiles.json` 选择。店铺诊断、周报、月报、季报、年报和大促复盘必须使用综合模式；数据质量审计与单项专题可显式使用单点模式。
- `version-info.json`：插件当前专家团版本的唯一来源；报告必须写入 `team_version`、发布日期、上一版本和 `version_diff`。
- `claim-ledger.json`：每个数字的来源、字段、期间、SHA256、状态和公式；必须先通过 `scripts/claim_guard.py`。
- 综合模式输入：团长最终 handoff 作为 `--handoff`，每位成员独立 handoff 通过重复的 `--member-handoff` 提交；所有交接必须同一 `run_id`、范围和期间。五位成员 handoff 必须包含 Agent 工具真实返回的 `agent_task_id`，以及由回传闩锁核验的 `agent_return_status=completed`、`agent_returned_at`、`agent_return_file` 和 `agent_return_sha256`。
- 单点模式必须显式传入 `--collaboration-mode single_point`；综合模式默认 fail closed。

## 数字来源与公式闸门

每个报告数字必须有 `claim_id`。买家转化率使用同口径支付买家数/去重访客数；订单/访客须单列，GMV/访客只表示访客价值。ROAS 绑定同期间同归因范围的归因销售额与广告费；利润 ROI 使用利润/总成本，并按 [来源与成本复算](../../../references/claim-sources-v2.md) 校验逐项证据。缺来源、公式不匹配、跨范围拼接或未知输入返回 `claim_guard_blocked`，不能只写 cost_complete=true。报告 Markdown 中的 claim 索引、`claim-receipt.json` 和冻结报告哈希必须一致。

## 输出状态

| 输入条件 | 报告包状态 | 允许内容 |
|---|---|---|
| `gate_status=BLOCKED` | `data_blocked` | 数据质量事实、风险、缺失数据和补数动作；不输出利润、预算、投放、定价、库存或增长结论 |
| `gate_status=PASS/WARN` 且 handoff 为草稿 | `draft_diagnosis` | 有证据的指标、事实、判断和待审批行动，不能写成已交付 |
| handoff 为 `ready_for_review` 且行动验收字段完整、审批状态不悬空 | `ready_for_review` | 可交付给人工复核；仍不是“已发布”或“已执行” |

## 下游规则

PDF/PPT/Excel 只能读取 `report.json` / `report.md`。下游不得重新解释指标、补造因果、替换审批状态或从旧报告抄数字。行动是否执行以行动记录的 `status` 和 `outcome` 为准：没有 `outcome` 就不能标记 `verified`。

报告首屏或摘要必须显示“专家团版本”，并列出本次相对上一版本的变更。版本号代表专家团运行能力，不代表客户平台已升级；平台连接器仍需查看 `connector-capability` 的真实状态。

报告还必须显示“本次专家协作记录”：六岗位完整名册、`contributed / pending_review / not_invoked` 状态、Agent 子任务 ID、回传状态与时间、贡献摘要、handoff 文件及 SHA256。候选稿生成时，团长与四位分析专家必须为 `contributed`，韦交达必须为 `pending_review`；不得把尚未发生的复核写成已贡献。综合模式缺少团长、数据专家、平台专家、内容直播专家或投流利润专家中的任一岗位时，构建器返回 `collaboration_incomplete`；成员缺少可查看的 `agent_task_id` 时返回 `collaboration_untraceable`；缺少真实完成回传凭证时返回 `collaboration_unreturned`。

## 对外交付

报告包保留证据 ID、来源文件名和哈希指纹，隐藏本机绝对路径、内部记忆和其他客户内容。生成成功只代表候选文件写入成功。

综合模式必须按顺序完成：`claim_guard → build_report_package --claim-ledger → review_guard prepare → 韦交达专属 review_attempt 回传 → attest-result → verify → public_output_guard --output → completion_gate --claim-receipt`。只有 `claim_guard_passed` 且 `completion-receipt.json.status=formal_delivery_complete` 才能称为正式报告完成；该凭证把候选稿中的韦交达 `pending_review` 更新为真实 `contributed`，并绑定其 Agent 子任务 ID。任何数字来源、报告、PDF、来源、复核或公域隔离凭证变化都会阻断完成，必须升修订号重新复核。
