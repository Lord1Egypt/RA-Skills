## Description: <br>
Provides scheduled, time-aware market intelligence briefings for A-shares, Hong Kong stocks, US markets, macro policy, and geopolitical news, with deduplication and Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fishisnow](https://clawhub.ai/user/fishisnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market watchers and operations teams use this skill to gather current public market news, filter repeated items, and send scheduled briefings through Feishu. It is suited to recurring morning, intraday, and closing summaries, not deep financial modeling or personalized investment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring Feishu delivery can send briefings to the wrong recipient if the chat target is misconfigured. <br>
Mitigation: Verify the Feishu chat target before enabling the cron schedule, and keep workspace configuration explicit. <br>
Risk: Workspace configuration or memory files may expose account tokens, personal holdings, or other sensitive financial details. <br>
Mitigation: Do not store tokens, portfolio holdings, or sensitive financial details in shared workspace config or memory files. <br>
Risk: Market news summaries and stock references can be mistaken for financial advice. <br>
Mitigation: Keep the investment disclaimer in generated briefings and treat outputs as reference material only. <br>


## Reference(s): <br>
- [Briefing Templates](references/briefing-template.md) <br>
- [Search Topics Configuration](references/topics.md) <br>
- [Market Briefing release page](https://clawhub.ai/fishisnow/market-briefing) <br>
- [CLS Telegraph](https://www.cls.cn/telegraph) <br>
- [Jin10](https://www.jin10.com/) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [AASTOCKS](https://www.aastocks.com) <br>
- [Caixin](https://www.caixin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing text with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are time-aware, deduplicated against a workspace log, and intended for Feishu message delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
