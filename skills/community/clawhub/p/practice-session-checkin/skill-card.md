## Description:

Public-safe practice session intake, start confirmation, reminder flow, completion check, and follow-up tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoma970](https://clawhub.ai/user/guoma970)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to coordinate generic practice tasks through intake, start-time confirmation, reminder messages, completion checks, and unfinished-task follow-up while keeping examples public-safe and non-identifying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may enter identifying or sensitive schedule details while adapting the practice reminder flow.

Mitigation: Keep task examples generic and avoid real names, institution names, private schedules tied to identity, account IDs, group IDs, health-sensitive details, and child-identifying information.

Risk: The assistant could overstep by guessing missing practice details or follow-up decisions.

Mitigation: Record the task as provided, ask one short clarification question when needed, confirm start time before reminders, and require confirmation before follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoma970/skills/practice-session-checkin)
- [ClawHub publisher profile](https://clawhub.ai/user/guoma970)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)
- [Customization Guide](CUSTOMIZATION.md)
- [Release notes v1.0.1](releases/1.0.1.md)
- [Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise conversational text or Markdown check-in messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve the provided practice task, confirm timing before reminders, and avoid sensitive or identifying details.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
