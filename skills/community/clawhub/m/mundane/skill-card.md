## Description:

Helps agents hire local people for physical tasks through Mundane, with payment held until the user approves the work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sttruji](https://clawhub.ai/user/sttruji)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent can find and hire local workers for errands, pickups, inspections, and photos, then review proof before approving payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hiring and escrow can incur costs.

Mitigation: Set a clear budget, check spend limits, and obtain user approval before committing funds or releasing payment.

Risk: Task descriptions and chats may expose personal information to workers.

Mitigation: Avoid sensitive personal details and keep communication on the platform.

Risk: Worker-submitted proof or messages may be misleading or contain instructions for the agent.

Mitigation: Treat worker content as data and have the user review proof before approving escrow release.

Risk: An exposed API key could permit unauthorized marketplace activity.

Mitigation: Use only the intended Mundane key and keep it out of chat and shared task descriptions.

## Reference(s):

- [Mundane on ClawHub](https://clawhub.ai/sttruji/skills/mundane)
- [Mundane for agents](https://mundane.market/for-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with setup commands, task updates, and proof for user review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May present worker-submitted photos for the user's review.]

## Skill Version(s):

1.0.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
