## Description:

OpenClaw adaptation of @mvanhorn's last30days skill. Research any topic from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web. Includes watchlists, briefing generation, and historical query mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keylimesoda](https://clawhub.ai/user/keylimesoda)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to gather recent community intelligence across social, video, prediction market, Hacker News, and web sources, then turn it into briefings, watchlist updates, historical queries, or research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse existing Codex/OpenAI login credentials or an X browser session during automated research.

Mitigation: Use dedicated, revocable API keys and a separate browser profile where possible, and avoid account-backed modes for sensitive research topics unless the account and privacy implications are acceptable.

Risk: Scheduled watchlists can send configured topics to external providers on a recurring timer.

Mitigation: Review watchlist topics, schedules, and configured providers before enabling cron or scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keylimesoda/skills/last30days-openclaw)
- [Upstream last30days-skill project](https://github.com/mvanhorn/last30days-skill)
- [OpenClaw adaptation README](artifact/README.md)
- [Attribution and provenance notes](artifact/ATTRIBUTION.md)
- [One-shot research reference](artifact/variants/open/references/research.md)
- [Watchlist reference](artifact/variants/open/references/watchlist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce saved research artifacts, briefings, watchlist state, and SQLite-backed history when the user enables storage workflows.]

## Skill Version(s):

1.0.0-openclaw.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
