## Description: <br>
Generate daily business briefings from multiple data sources, including weather, crypto prices, news headlines, system health, calendar events, and formatted morning reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate scheduled morning business briefings and status summaries for personal planning, team standup preparation, dashboards, or client updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public APIs for weather, crypto, news, and quotes. <br>
Mitigation: Deploy only in environments where outbound requests to those public services are acceptable, and review generated content before using it for business decisions. <br>
Risk: Generated reports can include local disk and RAM statistics. <br>
Mitigation: Disable the system section or keep report outputs private when local resource information should not be shared. <br>
Risk: The optional NewsData.io API key can be stored locally and displayed in command output or agent transcripts. <br>
Mitigation: Avoid storing sensitive API keys in this version unless terminal output, files, and transcripts are access-controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/oc-daily-business-report) <br>
- [wttr.in weather API](https://wttr.in/) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/simple/price) <br>
- [NewsData.io latest news API](https://newsdata.io/api/1/latest) <br>
- [Quotable random quote API](https://api.quotable.io/quotes/random) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text reports, Markdown reports, JSON arrays, and CLI configuration output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated reports to a user-selected output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
