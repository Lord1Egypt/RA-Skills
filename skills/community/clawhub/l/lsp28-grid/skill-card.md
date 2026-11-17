## Description:

Manage LSP28 The Grid on LUKSO Universal Profiles. Create, update, and manage grid layouts with mini-apps, iframes, and external links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luksoagent](https://clawhub.ai/user/luksoagent)

### License/Terms of Use:


## Use Case:

Developers and Universal Profile operators use this skill to prepare LSP28 grid data, encode it as a VerifiableURI, and update a LUKSO Universal Profile through a Key Manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes code paths for live blockchain updates using a controller private key.

Mitigation: Use a least-privileged controller key, verify the RPC URL, chain ID, Key Manager, and target Universal Profile before broadcasting any transaction.

Risk: Grid items can reference external URLs or iframe sources.

Mitigation: Inspect and trust each external URL or iframe source before including it in grid data.

Risk: The server security verdict is suspicious because the transaction script has limited safety checks.

Mitigation: Review the skill and generated transaction data before use with any real account.

## Reference(s):

- [LSP28 local specification](artifact/references/lsp28-spec.md)
- [LSP28 Standard](https://github.com/lukso-network/LIPs/blob/main/LSPs/LSP-28-TheGrid.md)
- [LUKSO Docs](https://docs.lukso.tech)
- [ClawHub skill page](https://clawhub.ai/luksoagent/skills/lsp28-grid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable setup and optional Node.js execution paths for blockchain transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
