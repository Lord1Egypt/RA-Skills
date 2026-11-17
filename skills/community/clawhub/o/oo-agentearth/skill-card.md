## Description:

Operate AgentEarth through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover AgentEarth tools, inspect their input schemas, and run account operations through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified installer and startup synchronization may alter other agents' skills.

Mitigation: Review the CLI setup first, use a separately reviewed and verified installation, and disable startup skill synchronization unless its broader changes are intended.

Risk: AgentEarth execution can delete or overwrite external resources and consume credits.

Mitigation: Inspect the requested target and effect before approving execution.

## Reference(s):

- [AgentEarth homepage](https://agentearth.ai/)
- [AgentEarth API documentation](https://agentearth.ai/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [AgentEarth ClawHub release](https://clawhub.ai/oomol/skills/oo-agentearth)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain data and an execution identifier; write and destructive actions can change external resources or consume credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
