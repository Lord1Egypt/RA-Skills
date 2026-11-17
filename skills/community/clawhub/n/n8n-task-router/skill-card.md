## Description:

Decision framework for routing tasks between n8n and OpenClaw, used when deciding whether a new task should be automated in n8n or handled by an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to decide whether recurring deterministic tasks belong in n8n workflows or whether judgment-heavy work should stay with OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a concrete credential-vault locator.

Mitigation: Replace the concrete 1Password reference with a generic configuration reference and require explicit user approval before resolving secrets.

Risk: The skill directs users toward local n8n setup that can create persistent workflows.

Mitigation: Verify the referenced n8n start script and workflows separately, use a least-privilege n8n API key, and require approval before activating workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/n8n-task-router)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with decision tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing criteria and setup references; it does not execute automation directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and CHANGELOG, released 2026-06-09; server release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
