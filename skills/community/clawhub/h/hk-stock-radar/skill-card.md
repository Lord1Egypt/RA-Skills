## Description:

Hong Kong stock market monitoring skill for Hang Seng indices, HK stock quotes, sector rankings, southbound fund flow, and market/news sentiment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-monitoring agents use this skill to fetch Hong Kong market snapshots, compare major index and sector movement, check selected stock quotes, and summarize recent sentiment signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external financial-data and news requests during normal use.

Mitigation: Run it only in environments where outbound requests to the listed market-data and news services are approved.

Risk: The skill text asks the agent to use a logged-in X/Twitter session for live sentiment checks.

Mitigation: Avoid granting personal account sessions unless the user explicitly accepts the privacy and account-context exposure.

Risk: Financial signals can be stale, unavailable, or affected by plaintext-HTTP sector data.

Mitigation: Treat outputs as unverified market-monitoring signals, cross-check against authoritative sources, and do not use them as trading advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/hk-stock-radar)
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=hkHSI,hkHSTECH,hkHSCEI)
- [Eastmoney Hong Kong sector API](http://push2.eastmoney.com/api/qt/clist/get)
- [Google News RSS search](https://news.google.com/rss/search?q=%E6%B8%AF%E8%82%A1+%E6%81%92%E7%94%9F+%E4%BB%8A%E6%97%A5+when:1h)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with market data summaries and runnable Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live third-party financial-data and news services and may be unavailable or stale.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
