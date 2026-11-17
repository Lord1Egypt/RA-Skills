## Description:

OpenClaw skill for requesting NEAR testnet tokens and checking NEAR testnet account balances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and NEAR testnet users use this skill to request testnet NEAR tokens and check account balances during testnet development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation claims status checking and rate limiting, but the security evidence says those features are overstated.

Mitigation: Treat the skill as a testnet faucet requester and balance checker only; do not rely on it to enforce rate limits or track request status unless those features are added elsewhere.

Risk: The skill sends account identifiers to NEAR testnet faucet and RPC services.

Mitigation: Use it only with NEAR testnet accounts and review command output before acting on faucet or balance results.

## Reference(s):

- [NEAR Testnet Faucet](https://wallet.testnet.near.org/)
- [NEAR CLI Documentation](https://docs.near.org/tools/near-cli)
- [ClawHub Skill Page](https://clawhub.ai/shaiss/skills/near-faucet)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests use NEAR testnet services and return command-line status text.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
