## Description:

Use the Lingxing MCP connector through OOMOL to read, create, and update Lingxing ERP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users of a Lingxing-connected OOMOL account can use the skill to discover Lingxing MCP tools and read or make ERP changes through the connector. Write actions require confirmation of the intended action and payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install software and make persistent agent-skill changes without clearly explaining or approving them.

Mitigation: Review and approve CLI installation separately, decide whether automatic skill synchronization is acceptable, and use the documented OO_SKILLS_SYNC_DISABLED opt-out when appropriate.

Risk: Installer contents and the version eventually downloaded have not been verified.

Mitigation: Verify the installer and the exact CLI version before installation.

Risk: Connector actions can expose account data or make ERP changes.

Mitigation: Connect only the needed account permissions and confirm the exact payload and effect before write actions.

## Reference(s):

- [Lingxing MCP documentation](https://www.lingxing.com/help/article/mcp)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector payloads and responses, with shell command examples and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses may contain Lingxing business data; state-changing actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
