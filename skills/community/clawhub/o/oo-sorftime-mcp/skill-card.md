## Description:

Provides Sorftime marketplace research and supported data management actions through Sorftime MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can research products, categories, keywords, and trends across supported marketplaces, and use available Sorftime tools to manage saved favorites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may automatically execute downloaded code, and automatic synchronization may change other agent skills; the remote installer and CLI behavior were not audited.

Mitigation: Review and install a specific CLI release before use, inspect its behavior, and disable automatic skill synchronization if it is unwanted.

Risk: Some actions can delete data, and operations may consume credits.

Mitigation: Confirm the exact deletion target before acting and account for potential credit use.

## Reference(s):

- [Sorftime MCP documentation](https://www.sorftime.com/en-US/mcp)
- [Sorftime](https://www.sorftime.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured marketplace data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results and actions depend on the connected Sorftime account and tools; operations may consume credits.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
