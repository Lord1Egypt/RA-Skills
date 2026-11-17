## Description:

Provides scheduled briefings with filtered, deduplicated news on A-shares, HK, US markets, macro policies, and geopolitics via Feishu messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fishisnow](https://clawhub.ai/user/fishisnow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Chinese-language market briefings for A-share, Hong Kong, US market, macro policy, and geopolitical news. It is suited to scheduled or user-triggered news collection, summarization, deduplication, and Feishu delivery, not deep financial modeling or individualized stock analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs or broad market-topic triggers may send Feishu messages automatically.

Mitigation: Configure the Feishu target carefully, test with a private DM first, and add a confirmation or draft-only step before posting to shared chats.

Risk: Live market searches can surface incomplete, stale, or misleading news.

Mitigation: Review important items against the cited market sources before acting on the briefing.

Risk: Briefings include market direction and stock references that could be mistaken for investment advice.

Mitigation: Keep the disclaimer in every briefing and treat the output as reference material, not personalized financial advice.

## Reference(s):

- [Briefing templates](artifact/references/briefing-template.md)
- [Search topics configuration](artifact/references/topics.md)
- [Market Briefing ClawHub release](https://clawhub.ai/fishisnow/skills/market-briefing)
- [CLS telegraph](https://www.cls.cn/telegraph)
- [Jin10](https://www.jin10.com/)
- [Sina Finance](https://finance.sina.com.cn)
- [AAStocks](https://www.aastocks.com)
- [Caixin](https://www.caixin.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style Chinese briefing text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-aware morning, intraday, and closing modes; may update a local deduplication log and send Feishu messages.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
