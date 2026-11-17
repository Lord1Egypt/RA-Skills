## Description:

利润优化引擎 — 订单管理/计价/结算模拟。核心能力：(1) 订单管理 (2) 计价模型 (3) 成本追踪 (4) 利润计算

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to simulate local order entry, pricing, cost tracking, profit calculation, and simple profit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent order storage has a verified file overwrite weakness.

Mitigation: Review before installing, fix file path validation and local file permissions, and do not use it for real business records until corrected.

Risk: Payment-state actions are under-documented.

Mitigation: Review confirmation behavior and require human validation before treating payment status changes as authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeman88-tch/skills/profit-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with command examples and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local JSON order records when commands are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
