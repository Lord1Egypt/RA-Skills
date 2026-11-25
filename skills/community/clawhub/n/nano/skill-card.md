## Description:

Nano (XNO) wallet operations, transaction analysis, and explorer lookups. Use for send/receive, balances, pending funds, address validation, unit conversion, tx/hash/account lookup, explorer links, and Nano block-lattice questions. Uses locally configured OWS wallets; prefer xno-mcp, then xno-skills CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casualsecurityinc](https://clawhub.ai/user/casualsecurityinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to inspect Nano accounts and transactions, manage locally configured wallets, and perform requested send, receive, payment, validation, and unit-conversion tasks through MCP or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned MCP launch command and recovery guidance that may send wallet queries through third-party public RPC nodes.

Mitigation: Review MCP setup and recovery instructions, use a pinned package version, and choose RPC providers you trust; do not share private keys or mnemonic phrases.

Risk: Reference resolution was partial, so the security scan does not establish that all referenced material was reviewed.

Mitigation: Review the skill's referenced material and assess the package source and RPC providers before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casualsecurityinc/skills/nano)
- [Nano protocol site](https://nano.org)
- [MCP setup instructions](artifact/references/mcp.md)
- [RPC configuration](artifact/references/config.md)
- [RPC account balance](artifact/references/rpc_account-balance.md)
- [RPC account information](artifact/references/rpc_account-info.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Nano block-lattice reference](artifact/references/blocklattice.md)
- [Blocklattice explorer](https://blocklattice.io)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with JSON examples, shell commands, explorer links, and ASCII QR output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Nano transaction summaries and wallet operation guidance; wallet sends and receives are performed only when requested.]

## Skill Version(s):

6.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
