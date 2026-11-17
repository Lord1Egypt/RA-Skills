## Description:

微信小程序开发辅助决策助手。用户提供产品名称和方向，综合微信指数、竞品分析、行业数据、商业模式、推广策略、开发技巧等多维度数据，生成专业的可行性决策报告（HTML）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product builders, and operators use this skill to assess whether a proposed WeChat Mini Program is commercially and technically feasible. It gathers public market signals, competitor context, monetization options, promotion paths, and development considerations into an HTML decision report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include untrusted research or user-supplied text, which may make a report unsafe to open or share.

Mitigation: Review generated reports before opening or sharing them, keep output paths explicit, and sanitize or escape report fields with a restrictive Content Security Policy before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/miniprogram-decision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and may use web search/fetch tools to gather current public market data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
