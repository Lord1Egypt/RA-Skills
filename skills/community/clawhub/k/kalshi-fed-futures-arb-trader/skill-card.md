## Description:

Compares CME FedWatch implied rate probabilities to Kalshi Fed rate decision market prices and trades when divergence exceeds threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to compare FedWatch-implied rate-cut probabilities with Kalshi market prices, then identify or execute trades when the configured divergence threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live trades when invoked with --live.

Mitigation: Use paper mode first, then enable --live only with tightly limited trading credentials and explicit loss limits.

Risk: The release asks for a raw Solana private key that the security evidence calls unnecessary.

Mitigation: Do not provide a funded Solana private key unless the publisher explains why this implementation needs it.

Risk: The trading dependency and execution path affect real funds.

Mitigation: Pin and review simmer-sdk before deployment and monitor trades with conservative position limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-fed-futures-arb-trader)
- [Simmer Skills homepage](https://simmer.markets/skills)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [CME FedWatch Tool](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON automaton reports, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in dry-run mode by default or execute live trades when explicitly invoked with --live.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
