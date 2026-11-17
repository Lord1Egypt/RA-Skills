## Description:

健康指导助手 helps agents provide personalized wellness guidance with safety boundaries, evidence-level framing, baseline tracking, and professional referral prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn wellness questions into cautious, non-diagnostic guidance that emphasizes habits, uncertainty, baseline tracking, and escalation to medical professionals when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, command execution, and write capabilities for a health-advice use case.

Mitigation: Review the skill before installation, grant it only in trusted agent environments, and prefer a reduced-permission version or one that documents exactly when those powers are used.

Risk: Health prompts may contain sensitive personal information.

Mitigation: Avoid entering sensitive health details and do not configure callback URLs for health content unless the destination is trusted.

Risk: Users may mistake general wellness guidance for medical advice.

Mitigation: Keep responses non-diagnostic, avoid prescriptions, state uncertainty, and recommend a qualified medical professional for concerning or persistent symptoms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/health-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured guidance and occasional inline command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health advice should remain non-diagnostic, avoid prescriptions, state uncertainty, and recommend professional care for concerning or persistent symptoms.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
