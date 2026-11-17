## Description:

Permissionless DeFi yield and credit on Solana via Project 0 (P0), enabling agents to review wallet holdings, recommend deposits, borrows, swaps, and strategies, and execute user-confirmed on-chain actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borcherd](https://clawhub.ai/user/borcherd)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to evaluate P0 lending opportunities on Solana, compare yield and borrowing strategies, and carry out wallet-authorized DeFi actions with explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through high-impact wallet signing for Solana DeFi transactions.

Mitigation: Use only a dedicated wallet with limited funds and require explicit user approval immediately before every signature.

Risk: Swap transactions may not be sufficiently verified before signing.

Mitigation: Do not sign Jupiter swap transactions unless the transaction is decoded and checked against the user-approved quote.

Risk: Wallet portfolio lookups disclose the wallet address and holdings to ai.0.xyz.

Mitigation: Use read-only wallet lookup only when the user accepts this disclosure.

Risk: Borrowing and looping strategies can become unhealthy or liquidatable as market prices move.

Mitigation: Check account health, leave a borrow buffer, monitor active positions, and stop for user approval before increasing risk.

## Reference(s):

- [Project 0](https://0.xyz)
- [Project 0 Protocol Overview](https://docs.0.xyz/)
- [Project 0 TypeScript SDK](https://docs.0.xyz/typescript-sdk/overview)
- [Project 0 Skill on ClawHub](https://clawhub.ai/borcherd/skills/project-0)
- [Borcherd ClawHub Profile](https://clawhub.ai/user/borcherd)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Solana transaction links, wallet-position summaries, API-derived yield data, and credential setup guidance.]

## Skill Version(s):

2.2.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
