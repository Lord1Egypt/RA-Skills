## Description:

长期计划推进技能（v2.0）。支持心跳联动内置、条件触发提醒、资产追踪、里程碑系统、多任务状态。当用户说"开一个长期计划"、"今天计划任务"、"阶段复盘"、"滚动下一阶段"、"列出所有计划"时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[141553](https://clawhub.ai/user/141553)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill to create, maintain, review, and roll forward long-term plans with stage tasks, milestones, reminders, asset snapshots, and plan relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores durable plan state, registers heartbeat-style checks, and mutates local task files.

Mitigation: Review the target workspace and filename validation before installation, and keep plan-state writes scoped to the intended tasks directory.

Risk: Asset tracking may send fund codes to a third-party market-data service.

Mitigation: Enable asset tracking only after user consent, and avoid entering sensitive holdings when external fund lookups are not acceptable.

Risk: Fuzzy matching and bulk completion can mark the wrong task as complete.

Mitigation: Require confirmation before bulk task completion or low-confidence matches, and review changed plan files after updates.

Risk: Automatic trigger setup can create reminders or checks the user did not intend.

Mitigation: Show proposed trigger configuration before registration and allow users to decline or edit it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/141553/skills/long-term-plan)
- [Publisher profile](https://clawhub.ai/user/141553)
- [Plan templates](artifact/templates.md)
- [Fund quote API pattern used by asset tracking](https://fundgz.1234567.com.cn/js/{fundCode}.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown and JSON plan artifacts with reminder text, review summaries, trigger configuration, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local plan state under the agent workspace and may call a third-party fund quote endpoint when asset tracking is enabled.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
