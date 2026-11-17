## Description:

Trades Polymarket prediction markets that resolve near known calendar catalyst events by scanning active markets, applying catalyst-window and price-threshold signals, and placing paper or explicitly enabled live orders through Simmer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to evaluate and automate a calendar-catalyst strategy for Polymarket markets, with paper trading as the default and live USDC trading only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real Polymarket trades using a high-value SIMMER_API_KEY.

Mitigation: Keep paper mode enabled unless live trading is intentional, require the explicit --live flag, and use an API key with strict account-side limits.

Risk: The security review flags weak dependency control for the SDK dependency.

Mitigation: Pin or verify simmer-sdk before deployment and review dependency updates before allowing live trading.

Risk: The security review says the advertised volume and open-position safeguards may be incomplete.

Mitigation: Enforce trading limits account-side and do not rely only on the skill's advertised safeguards until they are fixed or independently verified.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/diagnostikon/skills/polymarket-macro-calendar-catalyst-trader)
- [diagnostikon publisher profile](https://clawhub.ai/user/diagnostikon)
- [simmer-sdk package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text plus Simmer trade API calls and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence; artifact frontmatter reports 1.0 and artifact clawhub.json reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
