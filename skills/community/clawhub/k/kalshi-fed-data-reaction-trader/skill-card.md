## Description:

Trades Fed rate markets on Kalshi based on macro data releases by scanning CPI bin markets for implied CPI and adjusting rate cut probabilities with a data sensitivity model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to evaluate and optionally execute Kalshi Fed rate market trades after CPI or jobs data releases. It defaults to dry-run mode and requires explicit live mode for real trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Kalshi trades using high-value trading and wallet credentials.

Mitigation: Use paper or dry-run mode unless the SDK and strategy have been audited; provide only restricted trading credentials and use an isolated low-balance wallet if a Solana key is required.

Risk: Safeguards are reported as too broad or fail-open for real-money trading.

Mitigation: Do not run --live or scheduled automations until safeguard failures block trades and live behavior has been reviewed.

Risk: Exit logic may consider Fed rate positions beyond positions created by this skill.

Mitigation: Limit exit automation to positions created by this skill before using live mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/kalshi-fed-data-reaction-trader)
- [Publisher Profile](https://clawhub.ai/user/diagnostikon)
- [Simmer Markets Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON automaton reports, and Markdown setup guidance with Python and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trades require --live, SIMMER_API_KEY, and SOLANA_PRIVATE_KEY.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
