## Description:

Skill for AI agents to set up the Potato Tipper on a Universal Profile on LUKSO, including private-key-based setup and guidance for tip-on-follow integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cj42](https://clawhub.ai/user/cj42)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and technical agents use this skill to understand Potato Tipper, configure LUKSO Universal Profiles, troubleshoot LSP6 permissions and ERC725Y data keys, and generate TypeScript, Solidity, and shell setup guidance for tip-on-follow integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to execute real on-chain wallet transactions with raw private keys.

Mitigation: Use a dedicated low-value controller key, prefer testnet first, and avoid putting production private keys in shell commands.

Risk: The setup flow uses an unpinned remote repository before running Foundry commands.

Mitigation: Pin and inspect any cloned repository before execution.

Risk: Incorrect contract addresses or unreconciled authorizations can expose token balances to unintended transfers.

Mitigation: Verify the PotatoTipper and token addresses, and know how to revoke both delegate settings and token operator authorization.

## Reference(s):

- [Potato Tipper ClawHub Skill Page](https://clawhub.ai/cj42/skills/potato-tipper)
- [Security and Limitations](references/security-and-limitations.md)
- [Deployed Contract Addresses](references/addresses.md)
- [Configuration and Data Keys](references/config-and-data-keys.md)
- [Permissions](references/permissions.md)
- [Foundry Batch Setup](references/foundry-batch-setup.md)
- [TypeScript Examples](references/typescript-examples.md)
- [Solidity Examples](references/solidity-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include on-chain addresses, ABI usage, environment variables, and transaction setup steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
