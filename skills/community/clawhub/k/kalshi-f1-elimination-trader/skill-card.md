## Description:

Trades F1 Drivers Championship markets on Kalshi by identifying mathematically eliminated drivers still priced above zero, using dry-run mode by default and requiring SIMMER_API_KEY plus simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users use this skill to analyze Kalshi F1 Drivers Championship markets for mathematically eliminated drivers and optionally execute NO-side trades through Simmer/DFlow when live mode is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real-money trades and requires access to trading credentials and a Solana private key.

Mitigation: Use dry-run first, segregate or limit credentials, and enable live mode only after reviewing the current strategy assumptions and configuration.

Risk: The security scan summary flags under-scoped live position-selling behavior.

Mitigation: Review open F1 positions before running with --live, especially if existing positions should not be sold automatically.

Risk: The default signal uses static F1 standings, which can become stale as races complete.

Mitigation: Refresh standings data or replace the template signal with live F1 data before relying on elimination detection for live trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-f1-elimination-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text and JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires the --live flag and configured SIMMER_API_KEY and SOLANA_PRIVATE_KEY credentials.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
