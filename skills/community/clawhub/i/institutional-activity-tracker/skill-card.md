## Description:

牛股王独家研发的A股机构动向追踪工具，涵盖机构关注与机构调研两大维度，展示分析师评级、研报观点、板块与个股的买入/增持次数、调研次数、机构数量及调研详情，帮助投资者了解机构资金动向与关注方向。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial researchers use this skill to ask about A-share institutional focus and on-site research activity across sectors and stocks. It helps an agent retrieve public Niuguwang research endpoints and summarize institutional attention, ratings, reports, research counts, and related detail as informational market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-market summaries may be mistaken for investment advice.

Mitigation: Treat outputs as informational research context and preserve the AI investment disclaimer in user-facing answers.

Risk: The skill appends a fixed promotional footer and app-download link to responses.

Mitigation: Review the footer and link for policy fit before deployment and disclose the data source clearly.

Risk: The skill depends on public third-party stock-research APIs.

Mitigation: Confirm endpoint availability and terms before relying on the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/institutional-activity-tracker)
- [Niuguwang app download and data source](https://www.stockhn.com/#/appDownload)
- [GetFocusPlate public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetFocusPlate?packType=2000&version=5.0.16.0&type=3&plateType=4)
- [GetFocusStock public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetFocusStock?packType=2000&version=5.0.16.0&code=2000619&type=3)
- [GetStockConcernHisByPeriod public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetStockConcernHisByPeriod?packType=2000&version=5.0.16.0&innercode=1796&type=3)
- [GetResearchPlate public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetResearchPlate?packType=2000&version=5.0.16.0&type=3&plateType=0)
- [GetResearchStock public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetResearchStock?packType=2000&version=5.0.16.0&code=2000989&type=3)
- [GetInvestorRa public API](https://stq.niuguwang.com/taoquant/ResearchReport/GetInvestorRa?packType=2000&version=5.0.16.0&innercode=660&period=3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with optional inline curl examples and financial-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Niuguwang data attribution, an app-download link, and an AI investment disclaimer.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
