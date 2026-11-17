## Description:

Iran War Tracker V2 generates Chinese structured daily situation briefs and real-time risk monitoring for the 2026 Iran war, combining current news, Jin10 flashes, market data, and a credibility-graded geopolitical and macro-impact framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinfi-codex](https://clawhub.ai/user/chinfi-codex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce concise Chinese Iran-war monitoring briefs with separated fact, market-signal, and scenario-judgment sections. It is intended for geopolitical and risk-asset tracking workflows that need time-bounded news collection, source credibility labels, and daily scenario probabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports embedded shared Jin10 credentials and copied tracking cookies.

Mitigation: Review the skill before installing, replace shared provider credentials where possible, and avoid supplying additional secrets beyond the documented market-data provider keys.

Risk: The skill depends on external news and market-data providers whose availability, freshness, and coverage can vary.

Mitigation: Keep source timestamps and credibility labels in the final brief, and treat single-source or unverified items as provisional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinfi-codex/skills/iran-war-tracker-v2)
- [Ceasefire-period analysis frame](artifact/【FRAME】停火期.md)
- [Daily report template](artifact/【TEMPLATE】.md)
- [Iran situation and economic-impact framework](artifact/伊朗局势关键变量与经济影响分析框架.md)
- [Jin10 MCP service](https://mcp.jin10.com/mcp)
- [Alpha Vantage API endpoint](https://www.alphavantage.co/query?)
- [Stooq quote CSV endpoint](https://stooq.com/q/l/?s=bz.f&i=d)
- [CLS telegraph endpoint](https://www.cls.cn/nodeapi/telegraphList)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown situation brief, with helper scripts able to emit JSON or Markdown data extracts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default brief is capped at about 3000 Chinese characters and uses source credibility labels for facts, market signals, and scenario judgments.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
