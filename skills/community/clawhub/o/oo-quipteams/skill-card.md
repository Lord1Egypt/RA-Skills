## Description:

Search and read Quipteams data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can search and read Quipteams employee, inventory, product, device action, kit, and quote data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions recommend running a remote CLI installer whose contents and local effects are unverified.

Mitigation: Review and approve CLI installation separately, verify the downloaded software, and inspect its effects before running it.

Risk: The CLI setup includes bundled-skill synchronization, and the connector can expose employee and business data.

Mitigation: Review or disable bundled-skill synchronization, connect only the Quipteams access needed, and handle returned employee and business data carefully.

## Reference(s):

- [Quipteams](https://www.quipteams.com)
- [Quipteams API documentation](https://api.quipteams.com/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Quipteams read action and query parameters.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
