## Description: <br>
Exploits systematic weekday/weekend posting rate differences in post-count bin markets and can place paper or explicitly enabled live Polymarket trades through simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trading agents and advanced developers use this skill to identify post-count bin markets where weekend posting-rate drift may create mispricing, then evaluate or execute bounded paper trades by default and live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate financial trades when run with --live and a live-capable SIMMER_API_KEY. <br>
Mitigation: Start in paper mode, use the least-privileged or lowest-funded key available, and enable --live only after reviewing the strategy, simmer-sdk dependency, and tunables. <br>
Risk: Weekend-rate assumptions and fixed thresholds may be wrong for current markets or specific public figures. <br>
Mitigation: Review and adjust the tunables before use, including maximum position size, spread, market volume, trade thresholds, and maximum open positions. <br>
Risk: The skill requires a sensitive trading credential. <br>
Mitigation: Keep SIMMER_API_KEY private and avoid placing a live-capable key in environments where automated code can invoke live trading unintentionally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diagnostikon/polymarket-twitter-weekend-drift-trader) <br>
- [Simmer skill page](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text from market scans and trade attempts, with Python code and JSON configuration in the skill artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata and target metadata; artifact frontmatter says 1.0.0 and artifact clawhub.json says 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
