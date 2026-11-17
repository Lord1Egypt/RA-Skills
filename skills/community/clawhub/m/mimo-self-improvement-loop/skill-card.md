## Description:

Guides an agent through a self-improvement loop that mines weaknesses from execution traces, proposes targeted improvements, applies changes by risk level, and validates whether those changes improve future performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after important tasks, failures, repeated mistakes, or periodic reviews to turn execution history into concrete, testable process improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage long-term retention of execution history, weaknesses, mistakes, and validation records.

Mitigation: Use it in a contained workspace and disable, redact, or regularly review logs before applying it to sensitive tasks.

Risk: The skill can propose or apply changes to future instructions, skills, memory, tools, or decision rules.

Mitigation: Require reviewed diffs and explicit approval before any persistent behavior or instruction changes are accepted.

Risk: Self-improvement proposals may reduce quality if they are accepted without validation.

Mitigation: Run the skill's proposal validation step and roll back changes when measured outcomes are flat or worse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-self-improvement-loop)
- [Publisher profile](https://clawhub.ai/user/qqyougitcom)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and structured checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent memory records, improvement proposals, metrics, validation notes, and suggested changes to skills or decision rules.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
