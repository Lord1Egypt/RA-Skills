## Description:

Helps agents choose when to act, delegate, defer, or ask for confirmation, with self-checking and reflection loops intended to improve future autonomy decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add an autonomy gate that decides whether an agent should proceed, delegate, defer to a human, or ask for confirmation based on risk and confidence. It is also intended to record lessons from outcomes so future decisions can be adjusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store local cross-session memory about user tasks and outcomes.

Mitigation: Use it only in workspaces where persistence is acceptable, or disable and review persistence before use.

Risk: The skill describes automatic instruction writeback after repeated errors or usage.

Mitigation: Require human approval before any SKILL.md modification and review proposed changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-calibrated-autonomy)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce decision recommendations such as ACT, DELEGATE, DEFER, or ASK.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
