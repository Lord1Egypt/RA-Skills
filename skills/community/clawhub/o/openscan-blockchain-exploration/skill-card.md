## Description:

Procedural knowledge for on-chain blockchain analysis using the openscan CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matiasos](https://clawhub.ai/user/matiasos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to inspect EVM addresses, transaction histories, token balances, gas price trends, and confirmed transaction traces with OpenScan CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global CLI package.

Mitigation: Use a pinned, locally installed, or sandboxed @openscan/cli version and avoid elevated privileges for npm global installs.

Risk: The skill includes credential-handling patterns for RPC and explorer API keys.

Mitigation: Use environment variables or restricted configuration for API keys, and avoid placing real keys directly in command lines.

Risk: The skill requires external OpenScan verification links in responses.

Mitigation: Treat those links as external verification links and omit or adapt them when they are not relevant to the user's request.

## Reference(s):

- [OpenScan Explorer GitHub](https://github.com/openscan-explorer)
- [OpenScan skill page](https://clawhub.ai/matiasos/skills/openscan-blockchain-exploration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and external verification links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include OpenScan verification links when command output provides them.]

## Skill Version(s):

0.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
