## Description:

Guides agents through integrating Ika dWallet 2PC-MPC into Sui Move contracts for cross-chain signing, dWallet lifecycle operations, presigning, signing, future signing, and key import flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omersadika](https://clawhub.ai/user/omersadika)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Sui Move contracts and TypeScript workflows that integrate Ika dWallet 2PC-MPC for programmable cross-chain signing, treasury, DAO, presign pool, imported-key, and wallet lifecycle patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable shared-wallet functions may expose signing or wallet operations without sufficient authorization.

Mitigation: Add explicit authorization checks to every public shared-wallet entry point before production deployment.

Risk: Unbounded presign pool growth can increase costs or create operational risk.

Mitigation: Set fixed pool size limits, monitor pool state, and reject or throttle replenishment beyond the configured cap.

Risk: Weak seed handling or raw private-key import can put signing keys and funds at risk.

Mitigation: Use cryptographically random seed material stored in a secure keystore, avoid raw private-key import unless strictly required, and document user consent for shared signing.

Risk: Unpinned or unaudited dependencies can change security properties after release.

Mitigation: Pin dependency versions and review audited versions before production use.

## Reference(s):

- [Ika homepage](https://ika.xyz)
- [Protocol Complete Reference](references/protocols-detailed.md)
- [Integration Patterns Reference](references/patterns.md)
- [TypeScript Integration Reference](references/typescript-integration.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Move, TypeScript, TOML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Sui CLI for workflows that execute Sui operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
