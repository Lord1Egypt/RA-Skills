## Description:

Web3 development using MetaMask Smart Accounts Kit. Use when the user wants to build dApps with ERC-4337 smart accounts, send user operations, batch transactions, configure signers (EOA, passkey, multisig), implement gas abstraction with paymasters, create delegations, or request advanced permissions (ERC-7715). Supports Viem integration, multiple signer types (Dynamic, Web3Auth, Wagmi), gasless transactions, and the Delegation Framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayushbherwani1998](https://clawhub.ai/user/ayushbherwani1998)

### License/Terms of Use:


## Use Case:

Developers use this skill to build dApps with MetaMask smart accounts, ERC-4337 user operations, gas abstraction, delegation flows, and ERC-7715 advanced permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can spend tokens, spend gas, grant recurring permissions, or exercise signing authority.

Mitigation: Use testnets first, require explicit user confirmation before signing or broadcasting, and show clear permission details.

Risk: Private keys or signer credentials could be exposed if copied into source code or logs.

Mitigation: Keep private keys out of source code and logs, and use secure signer or wallet integrations.

Risk: Overly broad delegations can authorize unintended actions.

Mitigation: Use least-privilege scopes, caveats, expiration times, redeemer limits, and call limits before redeeming delegations.

## Reference(s):

- [MetaMask Smart Accounts Kit documentation](https://docs.metamask.io/smart-accounts-kit)
- [Smart Accounts Reference](references/smart-accounts.md)
- [Delegations Reference](references/delegations.md)
- [Advanced Permissions (ERC-7715) Reference](references/advanced-permissions.md)
- [MetaMask Flask](https://metamask.io/flask)
- [ERC-7710](https://eips.ethereum.org/EIPS/eip-7710)
- [ERC-7715](https://eips.ethereum.org/EIPS/eip-7715)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Web3 transaction, delegation, signer, paymaster, and permission guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
