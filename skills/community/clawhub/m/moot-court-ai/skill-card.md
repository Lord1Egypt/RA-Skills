## Description:

Simulate a full Chinese civil court hearing with 4 role-based agents (clerk, plaintiff, defendant, judge) orchestrated by deterministic Lobster workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal-technology users use this skill to run a structured Chinese civil moot-court simulation with clerk, plaintiff, defendant, and judge agents, then review the resulting hearing log and judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Case materials may contain sensitive personal, financial, privileged, or confidential information and are processed through external LLM providers.

Mitigation: Redact sensitive details unless authorized to send them to DeepSeek and DashScope/Qwen, and review generated hearing logs and judgments before relying on them.

Risk: The release evidence notes missing Lobster workflow/setup validation.

Mitigation: Verify the Lobster workflow and local setup before operational use.

## Reference(s):

- [Moot Court AI homepage](https://github.com/baobaodawang-creater/moot-court-ai)
- [ClawHub skill page](https://clawhub.ai/baobaodawang-creater/skills/moot-court-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text simulation outputs such as hearing logs and judgments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on external DeepSeek and DashScope/Qwen model providers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
