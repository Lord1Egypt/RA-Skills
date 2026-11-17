## Description:

On-Chain Skill Audit checks, registers, audits, and vouches for agent skills using an on-chain Solana provenance registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emanz1](https://clawhub.ai/user/emanz1)

### License/Terms of Use:


## Use Case:

Developers and skill reviewers use this skill to check on-chain provenance, register local skill hashes, submit audit verdicts, and vouch for agent skills before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable external npm code may change after review.

Mitigation: Pin and review package versions before using the skill.

Risk: Wallet-enabled Solana writes can spend SOL or publish permanent audit and vouch records.

Mitigation: Use a dedicated low-balance wallet and verify transaction details before signing.

Risk: Public registration and vouch writes may not represent verified trust by themselves.

Mitigation: Check audit history, hashes, versions, and trust summaries before relying on a registry result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emanz1/skills/onchain-skill-audit)
- [@rocketlabs/skill-audit npm package](https://www.npmjs.com/package/@rocketlabs/skill-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with command summaries and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include on-chain trust summaries, transaction guidance, and wallet or IQ-token prerequisites; write actions are append-only.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
