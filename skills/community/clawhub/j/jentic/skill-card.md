## Description:

Jentic routes an agent's external API work through Jentic Mini or hosted Jentic so the agent can search API operations, inspect schemas, and execute authenticated requests through a broker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanblanchfield](https://clawhub.ai/user/seanblanchfield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to external services such as email, calendars, GitHub, Stripe, Twilio, and similar APIs through a central broker. It is intended for workflows where credential handling, operation discovery, schema inspection, and permission escalation need to remain separate from ordinary agent execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent default routing could cause broad external API work to flow through Jentic across sessions.

Mitigation: Review the TOOLS.md integration block before persistence and install only when Jentic should be the default broker for the workspace.

Risk: Running Jentic Mini on the same machine as the agent weakens the intended separation between agent execution and credential administration.

Mitigation: Prefer a separate Jentic Mini host and reserve same-machine deployments for development or testing contexts.

Risk: Setup includes high-impact shell commands and a curl-to-sudo installer path when Docker is missing.

Mitigation: Have a human review setup commands, pin and verify deployment artifacts where possible, and avoid delegating curl-to-sudo installation to an agent.

Risk: The JENTIC_API_KEY enables broker access for the agent.

Mitigation: Store the key only in the intended agent configuration, avoid independent credential storage, and rotate it if exposure is suspected.

## Reference(s):

- [Jentic ClawHub listing](https://clawhub.ai/seanblanchfield/skills/jentic)
- [Jentic Skills repository](https://github.com/jentic/jentic-skills)
- [Jentic Mini repository](https://github.com/jentic/jentic-mini)
- [Jentic Mini authentication documentation](https://github.com/jentic/jentic-mini/blob/main/docs/AUTH.md)
- [Jentic Mini credentials documentation](https://github.com/jentic/jentic-mini/blob/main/docs/CREDENTIALS.md)
- [TOOLS.md integration block](references/tools-block.md)
- [Publisher profile](https://clawhub.ai/user/seanblanchfield)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JENTIC_URL and JENTIC_API_KEY for live broker use.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
