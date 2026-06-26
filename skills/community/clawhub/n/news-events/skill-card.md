## Description: <br>
Monitors 20+ premium RSS feeds for breaking news and matches stories to Polymarket markets via keyword analysis, trading when breaking news creates an estimated price impact exceeding 12%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor breaking news feeds, identify likely Polymarket-relevant events, and generate or execute trading signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place recurring real trades with limited built-in containment. <br>
Mitigation: Keep the skill in dry-run or simulation mode until the code, dependencies, venues, and trade behavior are reviewed. <br>
Risk: Scheduled execution can repeatedly evaluate news and place trades without direct operator review. <br>
Mitigation: Control or disable the cron schedule and add explicit market, trade-count, and daily-loss limits before enabling live trading. <br>
Risk: The skill requires a trading API key and may use real-market access depending on venue configuration. <br>
Mitigation: Use a capped or least-privilege trading key and verify the TRADING_VENUE setting before running outside simulation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/news-events) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with optional Simmer SDK trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live mode can place trades when invoked with --live.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter, clawhub.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
