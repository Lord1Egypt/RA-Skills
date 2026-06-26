# Routing Rules

Use this file only when route choice is unclear.

## Decision priority

Choose the route based on the **next best system action**, not on the meeting topic.

1. If the next step is a shared artifact, choose `feishu-doc`.
2. If the next step is row-based tracking across many items or owners, choose `feishu-bitable`.
3. If the next step is notifying or asking someone, choose `feishu-message`.
4. If the next step is time-based follow-through, choose `reminder`.
5. If the next step is deeper agent work, choose `same-gateway-agent`.
6. If none is safe or appropriate, choose `manual`.

## Examples

### Example 1
"把岗位发给同事看看有没有现成人"
- Best route: `feishu-message`
- Why: the next action is outbound communication

### Example 2
"把今天讨论的 follow-up 和 owner 写回会议纪要"
- Best route: `feishu-doc`
- Why: needs a durable shared artifact

### Example 3
"这些岗位后续跟进都记起来，每周看一次"
- Best route: `feishu-bitable`
- Why: repeated structured tracking

### Example 4
"下周提醒我追 DQ 是否看完合同模板"
- Best route: `reminder`
- Why: time-based follow-through

### Example 5
"研究一下全栈候选人薪资区间，给我一个短 memo"
- Best route: `same-gateway-agent`
- Why: requires substantive agent work, not simple delivery

### Example 6
"最后费率到底能不能做到 20%"
- Best route: `manual`
- Why: commercial judgment and approval authority required

## Batch rule
If many items point to the same route, batch them in presentation, but still keep one primary route per item.

## Feishu message caution
Only send if:
- the channel is configured
- the target is known
- the user has approved

Otherwise draft the message and surface the missing input.

## Delegation caution
Use same-gateway delegation only when the task clearly benefits from another agent turn. Do not delegate trivial one-line drafts.
