## Description: <br>
Trades logical inconsistency signals in geopolitical Polymarket clusters by checking strike-count, regional action, and prerequisite probabilities, then sizing correction trades by conviction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and traders use this skill to analyze near-term geopolitical prediction-market clusters, identify logical pricing inconsistencies, and run paper-mode or explicitly enabled live trading through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades with USDC. <br>
Mitigation: Keep the default paper venue unless real trading risk is explicitly accepted, and enable live mode only after reviewing position, spread, volume, and threshold tunables. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Protect and scope the key, store it only in the intended runtime secret store, and rotate it if exposure is suspected. <br>
Risk: Automated trading signals may be wrong or stale in fast-moving geopolitical markets. <br>
Mitigation: Review generated opportunities and risk settings before enabling schedules or live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-geopolitics-cluster-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with configurable environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket execution requires explicit live mode and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0 and clawhub.json reports 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
