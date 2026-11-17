## Description:

Provides command-line support for x402-style HTTP 402 payment flows, including endpoint checks, wallet configuration, simulated payments, mock balances, and payment history.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders can use this skill to explore x402-style payment workflows for API access, provider-side payment gates, wallet setup, and transaction history. As packaged, its payment, balance, and receipt behavior should be treated as mock/demo behavior rather than production payment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the payment, balance, and receipt flows are production-ready.

Mitigation: Treat these flows as mock/demo behavior until the skill implements real signing, settlement verification, and clearly documented limits.

Risk: Wallet private keys or other sensitive wallet values may be handled unsafely as packaged.

Mitigation: Do not use real private keys or real funds; revise storage and output behavior before any production use.

Risk: Payment capability claims may exceed the packaged implementation.

Mitigation: Review payment behavior against the security guidance and test with non-production endpoints before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-x402-payments)
- [Publisher profile](https://clawhub.ai/user/neckr0ik)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and Python examples; CLI output is plain text and JSON-like records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local configuration and history file behavior under the user's x402 configuration directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
