## Description:

Detects crisis and news spikes across other Polymarket markets and adjusts expected posting rates upward for post-count bins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor Polymarket event signals and produce paper or live trade decisions for post-count prediction markets. It requires a Simmer API key and should be kept in paper mode unless the operator has reviewed the live-trading risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trade real USDC when run with --live.

Mitigation: Use paper mode by default, require explicit operator approval for --live, and keep live-capable credentials out of unattended environments.

Risk: Live-trading safety limits are reported as partly missing or weaker than advertised.

Mitigation: Independently enforce position, volume, spread, and concurrency limits before using the skill for live trading.

Risk: The skill depends on SIMMER_API_KEY and simmer-sdk for market access and execution.

Mitigation: Use a narrowly scoped trading key, protect it as a secret, and review the dependency before granting live-trading authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-twitter-sentiment-spike-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place simulated or live trade orders through the Simmer client depending on execution mode.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
