## Description:

掘金工具专业版 helps teams manage Juejin multi-account content operations, including draft and scheduled publishing, topic trend analysis, approval workflows, and article performance reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content teams, and enterprise operators use this skill to coordinate Juejin account matrices, create draft or scheduled posts, route public publishing through approval, and analyze topic and performance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles multi-account Juejin session cookies and could expose account access if cookie files or prompts are not controlled.

Mitigation: Keep cookie files encrypted and access-limited, avoid pasting cookie values into prompts or logs, and rotate access according to team policy.

Risk: Multi-account draft, scheduled, or public posting can create unwanted publication activity if run without human approval.

Mitigation: Use draft mode by default and require explicit human approval before scheduled or public multi-account posting.

Risk: The security verdict is suspicious because broad activation wording is combined with posting authority and session-cookie handling.

Mitigation: Review the skill before deployment and restrict execution to intended Juejin publishing and analytics workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/juejin-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell command examples, and structured JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include execution status, result data, execution logs, and error fields.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
