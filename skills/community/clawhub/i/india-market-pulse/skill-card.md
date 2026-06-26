## Description: <br>
Daily Indian stock market briefing and price alerts. Monitors NSE/BSE stocks, tracks a personal watchlist, and delivers a morning summary via WhatsApp or Telegram. Covers Nifty 50, Sensex, top gainers/losers, and user-configured stock alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utsavs](https://clawhub.ai/user/utsavs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor Indian NSE/BSE market activity, track a configured stock watchlist, receive morning briefings, and manage price alerts through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a user's stock watchlist and alert thresholds in OpenClaw configuration or memory. <br>
Mitigation: Install only if storing that information is acceptable, and review configuration or memory entries that contain watchlist symbols or alert thresholds. <br>
Risk: Recurring cron jobs can send market briefings or alerts at unintended times if the UTC schedule is configured incorrectly. <br>
Mitigation: Enable cron jobs only for desired recurring messages and verify the UTC schedule before relying on automated delivery. <br>
Risk: Market data and headlines may be incomplete, delayed, blocked, or unsuitable as trading advice. <br>
Mitigation: Treat outputs as informational, review source availability, and avoid making trading decisions from the briefing alone. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utsavs/india-market-pulse) <br>
- [OpenClaw Homepage](https://clawhub.ai) <br>
- [NSE India API](https://www.nseindia.com/api/) <br>
- [Yahoo Finance India Chart API](https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}.NS) <br>
- [BSE India API](https://api.bseindia.com/BseIndiaAPI/api/) <br>
- [Moneycontrol Latest News RSS](https://www.moneycontrol.com/rss/latestnews.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [WhatsApp- or Telegram-friendly Markdown text with optional shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses INDIA_MARKET_WATCHLIST for watchlist configuration and may store alert thresholds in agent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
