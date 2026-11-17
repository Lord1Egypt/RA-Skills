## Description:

Make your agent discoverable across the internet. Auto-configures OADP signals in your workspace files, emits presence pings to open hubs, and propagates discovery markers so other agents can find you.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add OADP discovery markers to an agent workspace, ping an external hub, and add recurring network status checks for agent discoverability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup behavior can persistently modify AGENTS.md and HEARTBEAT.md.

Mitigation: Review the proposed file changes before running setup and keep a clear rollback path for removing the OADP marker and Agent Network section.

Risk: The skill contacts a hard-coded third-party hub and can make the workspace and agent discoverable.

Mitigation: Use it only in workspaces intended for external discovery, and avoid sensitive or private workspaces unless that exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaflytok/skills/oadp-beacon)
- [OADP hub API](https://onlyflies.buzz/clawswarm/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with inline bash commands and workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The setup script can append OADP marker and heartbeat entries and can contact the configured external hub.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
