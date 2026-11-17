## Description:

Complete Polygon agent toolkit for creating session-based smart contract wallets, performing token operations, registering ERC-8004 identity and reputation, and using x402 micropayments through a CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameslawton](https://clawhub.ai/user/jameslawton)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure Polygon smart contract wallets, manage wallet sessions, fund accounts, execute token operations, register on-chain agent identity, and handle x402 payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of CLI wallet sessions with high-impact spending authority.

Mitigation: Set narrow session limits, use dry-runs before broadcast, and review each transaction path before execution.

Risk: The release has supply-chain and network exposure from an unpinned global install and automatic cloudflared tunnel binary download.

Mitigation: Prefer a pinned and audited version, avoid global installs where practical, and review the cloudflared download and tunnel behavior before wallet creation.

Risk: Sensitive wallet session material may be stored locally or in temporary files.

Mitigation: Protect the local wallet directory, keep approval URLs unmodified, and remove temporary session files immediately after use.

## Reference(s):

- [Polygon Agent Kit repository](https://github.com/0xPolygon/polygon-agent-kit)
- [Sequence ecosystem connector](https://agentconnect.polygon.technology/)
- [ClawHub skill page](https://clawhub.ai/jameslawton/skills/polygon-agents-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes dry-run-first transaction posture, environment setup, wallet approval flows, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
