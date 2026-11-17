## Description:

Helps agents anticipate user needs, maintain persistent working memory, recover from context loss, and improve workflows through guardrails and verification practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent toward proactive assistance, persistent memory practices, context recovery, self-improvement routines, and implementation verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent working memory that may capture personal, confidential, credential, health, financial, or client data.

Mitigation: Set explicit rules requiring user approval before storing sensitive data, and limit persistent memory to necessary, reviewable information.

Risk: The skill encourages proactive or autonomous follow-up work with limited built-in user control.

Mitigation: Require approval before file changes, external communications, background jobs, or actions that affect user systems.

Risk: Security evidence rates the release as suspicious because broad persistence and autonomous behavior can increase privacy and control risks.

Mitigation: Review the skill before deployment, define boundaries for autonomous behavior, and audit memory files regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/proactive-agent-vic)
- [ClawHub publisher profile: chungvic](https://clawhub.ai/user/chungvic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt the agent to create or update local memory and configuration files.]

## Skill Version(s):

3.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
