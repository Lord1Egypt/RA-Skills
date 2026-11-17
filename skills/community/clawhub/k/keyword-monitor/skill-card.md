## Description:

关键词监控与内容采集自动化工具，支持多关键词并行监控、热门内容采集，并每日生成结构化报告推送到飞书群。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Content operations, competitive intelligence, marketing, and sales teams use this skill to monitor keyword-driven trends, collect popular content, and produce daily Markdown reports for review or Feishu group delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The privacy wording says data is local-only, while the security evidence says Tavily search queries are sent externally and Feishu webhook delivery sends generated reports to a Feishu group.

Mitigation: Review configured keywords, collected content, and generated reports for sensitive business information before enabling Tavily searches or Feishu webhook delivery.

Risk: The security verdict is suspicious because the documented data flow conflicts with disclosed third-party service use.

Mitigation: Require installer review of third-party service configuration and disable optional Feishu delivery when reports should remain local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/keyword-monitor)
- [Clawdis homepage](https://clawhub.ai/yesong-Hue/keyword-monitor)
- [Tavily API](https://tavily.com)
- [AI skill collection](http://ai.qnitgroup.com)
- [ShadowAI API](https://referer.shadowai.xyz/r/1056448)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown reports with structured tables and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include rank, title, platform, heat score, publication time, and source link fields.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
