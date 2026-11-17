## Description:

Send and receive encrypted messages and manage handshakes on the Kaspa blockchain using the Kasia protocol and mcporter tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renkasiyas](https://clawhub.ai/user/renkasiyas)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate Kasia encrypted messaging workflows on Kaspa, including conversation lookup, handshakes, message sending, and on-chain storage through mcporter-configured MCP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets may be exposed through command-line arguments or mcporter configuration.

Mitigation: Use a dedicated wallet with minimal funds, avoid passing seed phrases on the command line, and restrict permissions on mcporter.json.

Risk: The setup script can install dependencies, build, and execute a local kasia-mcp checkout.

Mitigation: Run setup.sh only against a trusted kasia-mcp checkout after reviewing the local code and dependency changes.

Risk: Background polling can create persistent local storage and scheduled activity.

Mitigation: Enable polling only with an explicit schedule, storage location, retention policy, and removal process.

Risk: Write operations create mainnet Kaspa transactions that may spend KAS.

Mitigation: Review recipients, amounts, payloads, and transaction costs before broadcasting with kaspa-mcp.

## Reference(s):

- [Kasia Protocol Reference](references/protocol.md)
- [Kasia Indexer API](https://indexer.kasia.fyi)
- [ClawHub Skill Page](https://clawhub.ai/renkasiyas/skills/kasia)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-like transaction payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Kasia transaction payload values that require a separate user-approved broadcast through kaspa-mcp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
