## Description:

用于拉取并展示最新热点内容，按模型预估点击率生成 Top 条目，并在用户确认后提供可选的 cron 注册命令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltang](https://clawhub.ai/user/xltang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current Chinese hotspot news, generate a concise Top list from item title and content, group titles by source_name, and check hotspot service status. It can also provide a user-approved cron command for scheduled hotspot updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts hotspot.api4claw.com when invoked to retrieve current hotspot data.

Mitigation: Install and use it only if calls to that disclosed API are acceptable for the deployment context.

Risk: The optional cron command could create unwanted scheduled hotspot messages if the schedule, timezone, channel, or recipient are wrong.

Mitigation: Review the generated cron command before approval, and leave scheduling disabled for manual-only hotspot lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xltang/skills/hotspots)
- [Hotspot API base URL](https://hotspot.api4claw.com)
- [Latest hotspots endpoint](https://hotspot.api4claw.com/hotspots/latest?timestamp=$TIME_STEMP)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Concise Markdown responses with ranked hotspot lists, source-grouped titles, status messages, and optional cron setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not display raw hotness, fetched_at, or data_date; optional cron setup requires explicit user approval.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
