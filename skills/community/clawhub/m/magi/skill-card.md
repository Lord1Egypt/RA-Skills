## Description:

Autonomous behavioral research loop that optimizes agent behavior through correction tracking and multi-perspective (MAGI) verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teenu](https://clawhub.ai/user/teenu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep a bounded local record of explicit corrections, test behavior rules, and reduce repeated agent mistakes through user-approved updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local behavioral memory can preserve incorrect or overly broad preferences if corrections are ambiguous.

Mitigation: Use only explicit corrections, require strong evidence before updating rules, and review memory.md periodically.

Risk: Stored corrections may capture sensitive user information.

Mitigation: Avoid credentials, financial data, health information, and third-party information in corrections; remove requested memories promptly.

Risk: Autonomous mode can let behavior rules change without interrupting the user.

Mitigation: Keep autonomous mode off unless the user is comfortable with local behavior updates; the default mode asks for confirmation before applying or measuring changes.

## Reference(s):

- [Self Improving on ClawHub](https://clawhub.ai/teenu/skills/magi)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and local memory/log file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit memory.md and append to corrections.md and experiments.md when the user approves; autonomous updates are disabled by default.]

## Skill Version(s):

1.8.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
