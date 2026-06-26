## Description: <br>
Korean stock market AI analyst Telegram bot that monitors KOSPI/KOSDAQ, tracks watchlists, delivers AI briefings, and answers natural-language questions in Korean, Chinese, and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbtsm](https://clawhub.ai/user/lbtsm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this Telegram bot to monitor Korean equities, ask market and stock questions, manage watchlists and alerts, and receive optional AI-generated briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot stores Telegram user IDs, usernames, watchlists, preferences, alerts, push logs, and recent query history. <br>
Mitigation: Publish clear privacy, retention, deletion, and opt-out controls before deployment, and limit access to the SQLite database. <br>
Risk: User prompts or query-derived data may be sent to third-party AI and market-data services. <br>
Mitigation: Disclose third-party data sharing, avoid sending unnecessary personal information, and configure only the API providers the operator has approved. <br>
Risk: Telegram bot and data-provider tokens are sensitive credentials. <br>
Mitigation: Treat all configured tokens as secrets, rotate exposed credentials, and avoid committing credentials or local databases. <br>
Risk: Scheduled push jobs can message users or channels without further interaction once enabled. <br>
Mitigation: Enable cron jobs only after users have opted in, set ALLOWED_GROUPS explicitly, and test push behavior in a restricted environment first. <br>
Risk: Finance responses and briefings may be mistaken for investment advice. <br>
Mitigation: Add clear no-investment-advice wording and require human review for public-facing financial guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lbtsm/mapulse-korea) <br>
- [Publisher profile](https://clawhub.ai/user/lbtsm) <br>
- [DART Open API](https://opendart.fss.or.kr) <br>
- [Daum Finance](https://finance.daum.net) <br>
- [Daum Finance API reference](https://finance.daum.net/api) <br>
- [Naver Finance mobile API](https://m.stock.naver.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram messages, Markdown documentation, and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scheduled briefings, alerts, and operational reports when optional cron jobs and credentials are configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
