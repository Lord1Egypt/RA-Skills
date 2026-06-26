## Description: <br>
Fetches daily Polymarket sports odds, supports AI analysis of betting opportunities, and sends concise recommendations to a configured Telegram chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wall-nut417](https://clawhub.ai/user/Wall-nut417) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch same-day pre-match NBA market data from Polymarket, have an agent draft brief betting-oriented analysis, and push the resulting summary to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and chat IDs can expose or misdirect messages if stored or shared carelessly. <br>
Mitigation: Keep credentials in environment variables or a private config file, protect the bot token, and confirm the chat ID before sending. <br>
Risk: The skill produces gambling-related prediction-market recommendations that may be wrong or financially harmful. <br>
Mitigation: Treat the output as risky gambling-related content rather than financial advice, and review recommendations before acting on them. <br>
Risk: A cron schedule can automatically send recommendations without a fresh human review. <br>
Mitigation: Review the configured schedule and run a manual test before enabling recurring Telegram delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wall-nut417/polymarket-telegram-picks) <br>
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com) <br>
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{token}/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries suitable for Telegram delivery, with shell commands and configuration examples in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Telegram delivery requires a bot token and chat ID; long messages may be truncated near Telegram's single-message limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
