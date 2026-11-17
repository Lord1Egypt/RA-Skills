## Description:

Guide for building with the Ika TypeScript SDK (@ika.xyz/sdk) on Mysten Sui v2. Use when creating dWallets, signing cross-chain transactions, managing encryption keys, or integrating with the Ika network from TypeScript/JavaScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omersadika](https://clawhub.ai/user/omersadika)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate @ika.xyz/sdk with TypeScript or JavaScript applications for dWallet creation, cross-chain signing, encryption key management, and Sui-based Ika network workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet key-handling examples can lead to exposure if placeholder seeds, private keys, serialized key bytes, or secret shares are copied into production code or stored in plaintext.

Mitigation: Use secure secret management, avoid logging sensitive values, replace placeholder seed examples, and review all generated key-management code before execution.

Risk: Converting zero-trust dWallet flows to shared dWallet flows changes who must participate in signing.

Mitigation: Treat zero-trust-to-shared conversion as an explicit security tradeoff and require application-level review before adopting it.

## Reference(s):

- [API Reference](references/api-reference.md)
- [End-to-End Flows](references/flows.md)
- [Types and Validation](references/types-and-validation.md)
- [Ika Homepage](https://ika.xyz)
- [ClawHub Skill Page](https://clawhub.ai/omersadika/skills/ika-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for agent responses; users should review key-management examples before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
