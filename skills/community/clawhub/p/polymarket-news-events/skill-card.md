## Description: <br>
Monitors premium RSS feeds for breaking news, matches stories to Polymarket markets through keyword analysis, and generates or executes trade signals when estimated price impact exceeds 12%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to monitor breaking news and produce dry-run or live Polymarket trade decisions. Live use is financial automation and should be enabled only with account limits, monitoring, and a least-privileged trading key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real trades automatically from RSS-based heuristics with limited built-in exposure controls. <br>
Mitigation: Start in dry-run or simulation, use a least-privileged trading key, keep trade size low, and do not enable scheduled live runs without independent account limits and monitoring. <br>
Risk: Breaking-news matching can misread story relevance, market fit, or direction and produce unsuitable trade decisions. <br>
Mitigation: Review configuration, thresholds, and market matches before live use; monitor execution logs and stop live runs when signals appear stale or unreliable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/polymarket-news-events) <br>
- [Publisher profile](https://clawhub.ai/user/Mibayy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Console text and API trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; TRADING_VENUE, NEWS_IMPACT_THRESHOLD, NEWS_TRADE_SIZE, and NEWS_MAX_AGE_MINUTES can tune venue, threshold, order size, and recency window.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
