## Description: <br>
OpenClaw skill for managing long-term plans as rolling stages with tasks, milestones, reminders, structured reviews, optional asset snapshots, and plan relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[141553](https://clawhub.ai/user/141553) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create, maintain, review, pause, resume, and relate long-running goals across short rolling phases. It is especially suited to local task plans that need reminders, milestones, review records, and optional fund-code based asset snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plan files can contain personal goals, tasks, optional holdings, and fund codes in local memory. <br>
Mitigation: Avoid storing brokerage credentials, account numbers, or sensitive financial records in plans, and review local plan files before sharing them. <br>
Risk: Asset tracking uses a third-party fund quote lookup and may return stale, unavailable, or incomplete market data. <br>
Mitigation: Confirm prices and any financial decisions with an authoritative source outside the skill. <br>
Risk: Fuzzy and bulk task-completion features may match the wrong task or update more tasks than intended. <br>
Mitigation: Confirm candidate matches and review the updated plan state before relying on completion status. <br>
Risk: Reminder and trigger behavior depends on local heartbeat execution and quote availability. <br>
Mitigation: Use the skill as an assistive tracker and keep separate reminders for critical deadlines or financial alerts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/141553/long-term-plan) <br>
- [Publisher profile](https://clawhub.ai/user/141553) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Plan templates](artifact/templates.md) <br>
- [Fund quote endpoint used by asset tracking](https://fundgz.1234567.com.cn/js/${code}.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown plan files, JSON trigger and index configuration, and short natural-language reminders or review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plan state locally under memory/tasks and may query fund quote data for asset snapshots when asset tracking is used.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
