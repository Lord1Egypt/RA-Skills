## Description:

查询安全水位的指标：mttr、事件量、ai提效

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuoxiangpang](https://clawhub.ai/user/zhuoxiangpang)

### License/Terms of Use:

MIT-0

## Use Case:

Security and operations employees use this skill to query security waterline metrics such as MTTR, event volume, and AI efficiency. It applies defaults for department and current-week queries when users omit those details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query internal security metrics.

Mitigation: Install and use it only where the agent is authorized to access the relevant security metrics.

Risk: Vague requests default to the Information Security department and the current week, which may not match the user's intent.

Mitigation: Clarify department and time range when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuoxiangpang/skills/mttr-ai)

## Skill Output:

**Output Type(s):** [Text, Guidance, Analysis]

**Output Format:** [Natural language text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
