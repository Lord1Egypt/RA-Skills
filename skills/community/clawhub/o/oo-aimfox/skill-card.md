## Description:

Connects agents to Aimfox to retrieve campaign and lead information and manage campaign audiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Aimfox account users use this skill to retrieve campaign, lead, interaction, and workspace-label data, and to add or remove LinkedIn profiles from campaign audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installers without separate consent or a clear account of lasting changes.

Mitigation: Review and separately approve CLI installation before use; check the oo CLI synchronization control before allowing it to modify agent settings.

Risk: Using this integration entrusts OOMOL with access to the connected Aimfox account.

Mitigation: Confirm OOMOL is trusted for the account and review the connection and its scopes before use.

## Reference(s):

- [Aimfox homepage](https://aimfox.com)
- [Aimfox API documentation](https://docs.aimfox.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured Aimfox data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Aimfox account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
