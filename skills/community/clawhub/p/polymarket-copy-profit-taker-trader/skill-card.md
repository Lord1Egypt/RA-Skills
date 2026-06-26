## Description: <br>
Detects when top whale wallets start taking profits by reducing winning positions, then identifies what markets they rotate INTO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to monitor top Polymarket wallets, detect profit-taking and rotations into new markets, and generate simulated or live trading actions through Simmer after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading may execute with a documented safety boundary that is not fully enforced in code. <br>
Mitigation: Run in paper mode first, use a tightly scoped and conservatively funded Simmer API key, and audit or fix the rotation timing and live-trading path before enabling --live. <br>
Risk: The skill requires sensitive trading credentials. <br>
Mitigation: Store SIMMER_API_KEY outside source files, scope it to the minimum required permissions, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-copy-profit-taker-trader) <br>
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python automation, environment configuration, and runtime trade/log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
