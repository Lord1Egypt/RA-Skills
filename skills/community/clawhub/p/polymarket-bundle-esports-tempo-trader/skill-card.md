## Description:

Trades tempo inconsistencies across Dota2 and esports game props on Polymarket by comparing first blood, kill-total, daytime-ending, rampage, and ultra-kill signals and sizing trades by conviction when those indicators conflict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Dota2 and esports prop-market tempo bundles, detect inconsistent Polymarket pricing signals, and generate simulated or live trade actions sized by conviction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real Polymarket trades and expose users to financial loss.

Mitigation: Keep the skill in paper mode until tested, use --live only after review, and limit SIMMER_API_KEY to the smallest necessary trading authority.

Risk: The security review says live-trading safeguards do not fully match the documentation.

Mitigation: Do not use --live until the market-identity fallback, volume filter, and true open-position limit are fixed.

Risk: The skill depends on simmer-sdk for market discovery and trade execution.

Mitigation: Pin and review simmer-sdk before granting trading authority.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-esports-tempo-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with trade decisions, skip reasons, and execution status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
