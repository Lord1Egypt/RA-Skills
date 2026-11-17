## Description:

Read and manage Kubera.com portfolio data, including net worth, assets, debts, allocation, holdings, and asset-value updates through a Python CLI/API client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bywallace](https://clawhub.ai/user/bywallace)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent users use this skill to query Kubera portfolios, summarize net worth and holdings, search assets or debts, and update asset values when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Kubera financial data to an agent session.

Mitigation: Install only for agents that need Kubera access, prefer read-only API credentials, and avoid sharing outputs beyond the intended workflow.

Risk: Write-enabled credentials can update asset or debt records.

Mitigation: Use read-only credentials by default and require explicit user confirmation before any update command or write-enabled key is used.

Risk: API credentials may be exposed if passed directly as command-line arguments.

Mitigation: Prefer environment variables or a managed secret store, and avoid using --api-key or --secret in shell history.

## Reference(s):

- [Kubera API Reference (V3)](references/api.md)
- [Kubera website](https://www.kubera.com)
- [Kubera API base URL](https://api.kubera.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from a Python CLI, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Kubera API credentials; update operations require --confirm and write-enabled credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
