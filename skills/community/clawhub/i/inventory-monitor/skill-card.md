## Description:

基于美兰中心C+服务.xlsx Excel台账监控库存水位、计算可用月数，并在库存低于阈值时生成补货提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and facilities teams use this skill to monitor inventory levels from an Excel ledger, calculate available months of supply, and prepare replenishment alerts for purchasing follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a real business inventory workbook through intake and withdrawal workflows.

Mitigation: Require role-based authorization, explicit confirmation before ledger changes, strict quantity and stock validation, backups, and an audit log.

Risk: The skill can send inventory alerts to an external WeCom destination.

Mitigation: Have an administrator configure and review the webhook destination, restrict who can trigger alerts, and avoid sending sensitive inventory details to unapproved recipients.

## Reference(s):

- [Reference Documentation for Inventory Monitor](artifact/references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/skills/inventory-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown text with inventory status summaries, replenishment alerts, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended purchase quantities and proposed ledger updates; external alert delivery depends on administrator-configured WeCom settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
