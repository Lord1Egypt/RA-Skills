## Description:

Alchemy (alchemy.com). Use this skill for ANY Alchemy request — searching and reading data. Whenever a task involves Alchemy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet owners can use the OOMOL-connected Alchemy service to look up Ethereum mainnet token balances and metadata, NFT ownership and metadata, and historical asset transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote CLI installer whose implementation could not be verified, without an approval step.

Mitigation: Review the installer, prefer a separately reviewed version-pinned installation, and require approval before running either remote installer.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Alchemy API documentation](https://www.alchemy.com/docs/make-your-first-request)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes read-only Alchemy queries for Ethereum mainnet.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
