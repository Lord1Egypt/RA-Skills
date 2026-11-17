## Description:

Create and redeem Linkdrop claim links from the command line with strict JSON output on Base, Polygon, Arbitrum, Optimism, and Avalanche.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seichris](https://clawhub.ai/user/seichris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to create or redeem Linkdrop claim links from a local wallet while preserving machine-readable JSON output. It is intended for workflows on Base, Polygon, Arbitrum, Optimism, and Avalanche that can safely manage wallet and API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys, Linkdrop API keys, RPC URLs, claim URLs, recipient addresses, and chain selection as sensitive financial controls.

Mitigation: Use a dedicated low-balance wallet, keep secrets and claim URLs out of logs and git history, and verify the selected chain and recipient before each invocation.

Risk: The CLI can initiate irreversible on-chain deposits and redemptions.

Mitigation: Run a small test transfer first and require explicit human review of amount, token, chain, claim URL, and recipient before sending real value.

Risk: Dependency installation is not fully reproducible when using npm install without a reviewed lockfile.

Mitigation: Review package versions and dependency changes before exposing secrets, and prefer a reviewed lockfile with npm ci in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seichris/skills/linkdrop-agent-cli)
- [Project Homepage](https://github.com/seichris/linkdrop-sdk-cli)
- [Linkdrop Application](https://p2p.linkdrop.io)
- [Linkdrop Escrow API](https://escrow-api.linkdrop.io/v3)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects from command-line invocations with setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Success and failure return one JSON object per invocation; successful operations may include claim URLs, transfer IDs, deposit transactions, and redeem transactions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
