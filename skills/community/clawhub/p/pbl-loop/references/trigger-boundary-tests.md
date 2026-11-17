# PBL Loop: trigger / boundary tests

## Should trigger (positive)
- 我想对照交付之外的能力成长做 start。
- 继续上次的 pbl-loop checkpoint，看看这次学习是否更可迁移。
- 帮我做一个 transfer：把这次方法迁移到另一个相似问题。
- 先给我一个 start，建立可复盘的能力目标。

## Should not trigger (negative)
- 我只想要本周交付状态，按任务列表汇报即可。
- 我们已经验收完了，直接给最终 status。
- 先解释这篇资料，我只想理解内容，不做能力循环。
- 给我列一下待办清单然后结项。
- 我只问这套技能能否在某宿主直接跑通，没有给出学习目标或转移需求。

## Anti-fabrication boundary
- 用户只说“给我 pbl start”但没提供验收阈值或周期，不得编造表单、完成率、复盘周期等细项；标为 `unknown`，再给出可确认的 `proposed` 版本。

## Semantic anti-patterns
- Wrong: 把“用户重视可见性”标为 `unknown-unknown`。Right: 这是产品假设，不分象限。
- Wrong: 一次 AI 辅助尝试后，把“我能识别关键证据”升为 `known-known`。Right: 保持 `known-unknown`，并列出仍缺的重复性、独立性或迁移证据。
- Wrong: 将有明确测试路径的能力缺口放入 `unknown-unknown`。Right: 转为 `known-unknown`。
- Wrong: 在 `required` 下添加“3 个样本、两周内、禁看原答案”等细项。Right: 每项只在可确认时写成 `source_status: proposed`，无法确认则省略。
- Wrong: 把 checkpoint 的学习评估结果写成 `delivery_goal`。Right: 当交付目标未知时写 `delivery_goal: unknown`，并将学习判断放到对应证据项。

## Start contract example (minimal, community reading event)

User input:

- “我今晚有一场社区共读活动，我的交付目标是完成30分钟读后讨论；本次能力目标是能在下一次活动里更快形成一段结构化复盘。可不可以先给我一个 start？”

Expected `start` behavior:

- `delivery_goal` is explicitly user-stated as `完成30分钟读后讨论`.
- `learning_goal` is explicitly user-stated as `我能更快形成结构化复盘`.
- `assistant_proposals` is either `[]` or contains only clearly flagged `source_status: proposed`.
- evidence context is explicit as unknown, e.g.:
  - `unknowns` includes `活动后的互动证据未提供（如发言数、反馈、时间分布）` with `evidence_status: unknown`.
- no invented duration/count/threshold/deadline/acceptance gate appears.
- response ends with exactly one focused question, e.g. one open question about observable proof:
  - “为了判断这个能力是否提升，下次你最想让我先观察哪个可观测结果？”

Example minimal `start` response skeleton (illustrative, not a strict full-conforming output):

```json
{
  "mode": "start",
  "delivery_goal": {"value": "完成30分钟读后讨论", "source_status": "user_stated", "evidence_status": "unknown", "assistance_provenance": "human"},
  "learning_goal": {"value": "我能更快形成结构化复盘", "source_status": "user_stated", "evidence_status": "unknown", "assistance_provenance": "human"},
  "user_stated_requirements": [{"text": "交付目标是完成30分钟读后讨论；目标能力是更快形成结构化复盘", "source_status": "user_stated", "evidence_status": "unknown", "assistance_provenance": "human"}],
  "assistant_proposals": [],
  "unknowns": [{"text": "活动后的互动反馈数据未提供（发言数、反馈内容、参与者分布）", "source_status": "unknown", "evidence_status": "unknown", "assistance_provenance": "ai_reasoning"}],
  "assistance_provenance": ["human", "ai_reasoning"],
  "delivery_evidence": [],
  "capability_evidence": [],
  "quadrant_before": "known-unknown",
  "capability_debt": "缺少可复用的复盘模板与迁移性证据",
  "next_deliberate_challenge": "先确认可观测结果定义（下次活动中哪个迹象将被视为能力提升）"
}
```

Then end with:

“为了判断这个能力是否提升，下次你最想让我先观察哪个可观测结果？”

## Negative regression note

- 禁止编造：
  - “15分钟活动”这类新活动时长；
  - 假定参与人数/样本量；
  - `20% / 60% / 70%` 这类阈值；
  - “24小时内完成”这类窗口；
  - 完整 intervention plan（含完整步骤、时间轴和验收标准）；
- 当证据缺失时，必须使用 `unknown` 或 `proposed`，不写实数。

## Host-neutral portability case (no state backend)

- 输入可直接是：
  “我在两个工具里都要用这个 skill，不想绑定数据库和 FlowGrid，能保证可移植吗？”
- 期望行为：
  - SKILL 保持 host-neutral 不依赖数据库/CLI/MCP/固定路径；
  - 提示 `persistence` 为默认可选且需要用户授权；
  - 明确给出“当前可在无状态下运行”的结论；
  - 不要求初始化 state backend，不要求外部平台账号或 SDK。
