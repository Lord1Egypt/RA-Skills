## Description:

Daily Indian stock market briefing and price alerts for NSE/BSE stocks, personal watchlists, morning summaries, top gainers and losers, and user-configured stock alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utsavs](https://clawhub.ai/user/utsavs)

### License/Terms of Use:


## Use Case:

External users use this skill to monitor Indian NSE/BSE market activity, maintain a personal watchlist, receive concise market briefings, and manage price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watchlist entries and alert rules may persist in OpenClaw configuration or memory.

Mitigation: Store only intended ticker symbols and alert thresholds, and review or remove saved configuration when the skill is no longer needed.

Risk: Scheduled briefings or triggered alerts may be sent through the active messaging channel.

Mitigation: Use explicit commands for alerts and review cron jobs before enabling automated delivery.

Risk: External market data sources may be rate-limited, blocked, delayed, or temporarily unavailable.

Mitigation: Treat generated market updates as informational and retry or cross-check important market decisions with authoritative sources.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/utsavs/skills/india-market-pulse)
- [NSE India API](https://www.nseindia.com/api/)
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}.NS)
- [BSE India API](https://api.bseindia.com/BseIndiaAPI/api/)
- [Moneycontrol RSS](https://www.moneycontrol.com/rss/latestnews.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [WhatsApp- or Telegram-friendly Markdown text with optional shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current market levels, watchlist prices, news headlines, alert status, and cron setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
