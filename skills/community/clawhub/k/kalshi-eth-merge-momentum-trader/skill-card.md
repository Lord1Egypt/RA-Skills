## Description:

Trades ETH price markets on Kalshi using a post-merge deflation thesis based on EIP-1559 ETH burn assumptions, with SIMMER_API_KEY and simmer-sdk required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate and optionally trade Kalshi ETH price markets from a deflation-adjusted post-merge Ethereum thesis. It supports dry-run review, position checks, configuration inspection, and live execution when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place and close real Kalshi trades when live mode is enabled.

Mitigation: Use dry-run mode first, keep position and trade limits conservative, and treat --live as explicit authority for real financial execution.

Risk: The release asks for a Solana private key even though server security evidence flags that requirement for review.

Mitigation: Do not provide a wallet private key until the publisher documents exactly why it is needed; use narrowly scoped, revocable credentials.

Risk: Trading behavior depends on the external simmer-sdk package and live market API responses.

Mitigation: Pin or review the simmer-sdk version before installation and monitor behavior in dry-run mode before allowing live trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-eth-merge-momentum-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text with optional JSON automaton reports and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode is the default; live trading requires the explicit --live flag.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
