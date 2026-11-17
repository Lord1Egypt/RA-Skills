## Description:

Creates a receive-only Nano wallet for an agent to generate an address, check addresses, view balances, and accept incoming payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhyabi2](https://clawhub.ai/user/dhyabi2)

### License/Terms of Use:

MIT

## Use Case:

Agents and their operators use this skill to receive Nano payments without giving the agent a send command. It creates a local wallet, validates addresses, checks balances, and accepts pending payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loss or exposure of the locally stored private key can put received funds at risk.

Mitigation: Back up the key securely and protect access to its configured file path.

Risk: The default public Nano RPC endpoint can observe account queries and signed receive blocks.

Mitigation: Use a trusted Nano RPC endpoint when account activity should not be shared with the default node.

## Reference(s):

- [Nano starter ClawHub listing](https://clawhub.ai/dhyabi2/skills/nano-starter)

## Skill Output:

**Output Type(s):** [Text, JSON data]

**Output Format:** [One JSON object per command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet address, address validity, balance, or received payment details; does not return the private key.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
