## Description: <br>
Cross-platform divergence scanner comparing Kalshi and Polymarket prices on identical events, using fuzzy title matching, configurable thresholds, and volume filters to surface potential arbitrage opportunities and market mispricings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders, analysts, and developers use this skill to compare Kalshi and Polymarket markets, identify similar event contracts, and review price divergences before deciding whether to investigate or trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Kalshi credentials and reads a configured private key file. <br>
Mitigation: Use a dedicated least-privileged API key, keep private keys outside the skill directory, restrict file permissions, and rotate credentials if exposure is suspected. <br>
Risk: The skill writes persistent cache files containing market scan and divergence data, including during dry-run use. <br>
Mitigation: Run it under a profile where local cache persistence is acceptable, and delete or relocate cache files when trading or activity data should not remain on disk. <br>
Risk: Fuzzy matching can pair markets incorrectly or miss equivalent markets, which may make divergence output misleading. <br>
Mitigation: Review matched market titles, match scores, liquidity, and platform terms manually before treating any alert as actionable. <br>


## Reference(s): <br>
- [Fuzzy Title Matching](references/fuzzy-matching.md) <br>
- [Kalshi](https://kalshi.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Prediction Market Arbiter on ClawHub](https://clawhub.ai/kingmadellc/prediction-market-arbiter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples, shell commands, Python usage examples, console alerts, and JSON cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes divergence cache data for follow-up analysis and scheduled workflows.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
