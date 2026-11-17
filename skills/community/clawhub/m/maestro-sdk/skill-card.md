## Description:

Build AI agents that operate Solana vaults using the Maestro SDK (@trionlabs/maestro-sdk) for transfers, swaps, and policy-controlled vault interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamancan](https://clawhub.ai/user/yamancan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building ClawHub agents use this skill to integrate Maestro SDK flows for Solana policy-controlled vault discovery, health checks, balance checks, and transfers while preserving vault-owner controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill initializes or loads local wallet credentials and may access local key material.

Mitigation: Use it only where local key access is approved, pin the Maestro SDK version, and avoid placing real private keys in the agent environment unless a separate key-management policy is in place.

Risk: The skill can guide policy-authorized Solana transfers from a vault.

Mitigation: Require explicit user confirmation for setup and every transfer, and stop before transactions when health checks report critical issues.

Risk: The skill persists vault, owner, network, and transfer state for continuity.

Mitigation: Install only where persistent vault memory is acceptable and review stored memory for sensitive operational details.

Risk: The skill prompts funding and setup automatically when loaded.

Mitigation: Review before installing and require explicit user confirmation before any funding, setup, or transfer action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yamancan/skills/maestro-sdk)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guardrails, health checks, error responses, memory persistence guidance, and Maestro app navigation paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
