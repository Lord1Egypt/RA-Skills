---
name: linear-feedback-triage
description: Triage user-feedback issues in Linear, especially FB team / 用户反馈 workflows. Use when asked to query Linear issues, list recent complaints, find duplicate feedback, group membership/payment complaints, decide main issue vs sub-issue, suggest status/labels/assignee, or draft user replies for the Tide feedback process.
---

# Linear Feedback Triage

Use this skill for the Tide-style feedback workflow that lives in Linear.

## Quick start

When the user asks about recent feedback, membership complaints, duplicates, or FB issues:

1. Use `exec` with `npx -y mcporter ...` from `/Users/claw/.openclaw/workspace`.
2. Query the Linear MCP server configured in `config/mcporter.json`.
3. Prefer read-only queries first.
4. Summarize findings before proposing writes.
5. Only mutate Linear when the user clearly asks, or when the workflow explicitly calls for it.

Useful commands:

```bash
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.list_issues team=FB limit=10
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.get_issue id=FB-12345
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.list_issue_statuses team=FB
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.list_issue_labels team=FB
```

## Core workflow

### 1. Query first

For broad requests, start with `linear.list_issues`.

Good filters:
- `team=FB` for 用户反馈
- `label=会员支付` for membership/payment complaints
- `query=退款` / `query=续费` / `query=支付失败` for narrower searches
- `limit=10` unless the user asks for more

If descriptions are truncated, follow up with `linear.get_issue` on the specific IDs.

### 2. Normalize the feedback type

Map issues into a small set before deciding action:
- **建议**: product/content suggestion, feature request, request for a new payment method
- **BUG**: broken flow, payment failure, renewal failure, login/register issue, crash, data problem
- **内容反馈**: meditation/sleep/sound/content quality issues
- **其他**: unclear but not obviously a bug or suggestion

Keep labels to at most 3, mixing platform + primary class + one secondary domain when helpful.

## Label guidance

### Zero-level labels
- Android
- iOS
- Web
- 重要

### First-level labels
- 建议
- 功能故障
- 内容反馈
- 会员支付
- 注册登录
- 其他

### Second-level labels
- 专注功能
- 睡眠功能
- 帐号数据
- 网络问题
- 闪退崩溃
- 播放功能
- 冥想内容
- 声音内容
- 睡眠内容

## Status guidance

Use the user's workflow vocabulary when recommending or applying statuses:

- **待处理**: raw incoming feedback
- **待跟进**: assigned and entering workflow
- **沟通中**: active user communication
- **处理中**: analysis, fixing, discussion, or investigation underway
- **挂起**: blocked or dormant short-term
- **已解决**: issue resolved or recorded elsewhere and no further user question remains
- **已归档**: duplicate/aged-out/archive state
- **无效反馈**: spam or meaningless feedback; use sparingly

## Duplicate-handling rules

For suspected duplicates:

1. Compare issue title, complaint theme, platform, account hints, and timestamps.
2. If it is the same user and same complaint, treat it as a likely duplicate.
3. If it matches an existing unresolved bug:
   - recommend the new issue be archived
   - recommend linking it under the main issue as a sub-issue
   - reply to the user that the problem has been received and is being handled
4. If it matches an existing resolved bug:
   - recommend archive/sub-issue under the solved main issue
   - reply asking the user to update to the solved version or re-check

When confidence is low, say so explicitly instead of forcing a merge.

## Membership/payment complaint guidance

Common membership/payment buckets:
- refund / cancellation request
- auto-renewal complaint
- payment failure
- renewal failure
- purchase blocked by account conflict
- payment-method suggestion

Heuristic:
- **payment method request** → usually 建议 + 会员支付
- **cannot pay / renew / buy** → usually BUG or transactional failure + 会员支付
- **refund / cancel auto-renewal** → usually support/payment workflow item; still tag 会员支付

## Reply drafting

If the user asks for a reply draft, produce text that can be used with Tide Bot:

```text
@tidebot /reply <reply text>
```

Default tones:
- unresolved known/active issue: acknowledge receipt, say it is being handled
- resolved issue: suggest updating/retrying on latest version
- suggestion: thank the user and say it has been recorded for evaluation

Do not claim a fix is shipped unless Linear evidence supports it.

## Mutation commands

Only use these when needed:

```bash
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.save_issue id=FB-12345 state=处理中
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.save_issue id=FB-12345 labels='["会员支付","Android"]'
cd /Users/claw/.openclaw/workspace && npx -y mcporter call linear.save_comment issueId=FB-12345 body='处理中，已复现。'
```

Before writes, briefly state what you are about to change.

## Output format

For analysis requests, prefer:
- issue ID
- short title
- status
- labels
- why it matches the request
- duplicate/main-issue recommendation if relevant

For grouping requests, prefer buckets such as:
- 退款 / 退订
- 自动续费争议
- 支付失败
- 无法购买 / 无法续费
- 支付方式建议

Keep summaries compact and decision-oriented.
