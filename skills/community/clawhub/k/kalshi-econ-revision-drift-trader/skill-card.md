## Description: <br>
Trades CPI bin markets on Kalshi accounting for systematic upward revision bias (~0.03 pp) in initial CPI releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to evaluate CPI revision-drift signals for Kalshi CPI bin markets. It defaults to dry-run output and can place live trades only when explicitly run with live trading credentials and the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real funds and requires high-value trading and wallet credentials. <br>
Mitigation: Use dry-run first, review the strategy and simmer-sdk before live use, and use a dedicated low-balance wallet plus a scoped or revocable API key. <br>
Risk: The CPI revision-drift strategy may be wrong, stale, or unsuitable for current market conditions. <br>
Mitigation: Treat dry-run output as a signal to review, validate assumptions against current CPI and market data, and keep conservative position, slippage, and trade-count limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-econ-revision-drift-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown-style tables with optional trade execution actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires explicit --live execution and configured credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
