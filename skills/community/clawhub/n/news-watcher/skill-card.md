## Description: <br>
Monitors CoinDesk or PANews for new cryptocurrency articles, fetches article text, asks OpenClaw to summarize it in Chinese, and sends updates to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvxer](https://clawhub.ai/user/vvxer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can run this skill to monitor selected crypto news sites, summarize newly detected articles, and receive Telegram notifications without separate news API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A copied README cron command can send Telegram output to a fixed chat ID. <br>
Mitigation: Replace any copied Telegram recipient with the intended TELEGRAM_USER_ID before enabling cron, background mode, or automatic messages. <br>
Risk: Scraped web article text is passed into the main OpenClaw agent for summarization. <br>
Mitigation: Run summarization in an isolated or tool-limited OpenClaw session when available, and review summaries before using them for decisions. <br>
Risk: The skill polls external news sites continuously and sends automatic notifications. <br>
Mitigation: Only enable background or cron execution when continuous polling and Telegram delivery are intended, and choose an appropriate check interval. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vvxer/news-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/vvxer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console output and Telegram messages containing article links and Chinese summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_MJS and TELEGRAM_USER_ID; optional CHROME_PATH and PLAYWRIGHT_HEADLESS control browser execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
