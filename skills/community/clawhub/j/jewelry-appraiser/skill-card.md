## Description:

AI jewelry appraisal and buying assistant for diamonds, colored gemstones, jadeite, pearls, colored diamonds, precious metals, certificates, investment collecting, and custom rings; it can analyze user questions or uploaded jewelry/certificate images and generate an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers, collectors, jewelry buyers, and agents assisting them use this skill to interpret jewelry quality signals, certificates, price context, buying tradeoffs, and investment risks across common gem and precious-metal categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted user-provided text.

Mitigation: Escape or sanitize user-provided report content before rendering or sharing HTML output.

Risk: The report generator writes files and can accept an output path.

Mitigation: Do not allow untrusted users to choose arbitrary output paths; restrict output to a trusted workspace.

Risk: Price, appraisal, and investment guidance can be outdated or materially wrong.

Mitigation: Treat outputs as informational and verify significant purchases or investments with current market sources, certificates, and independent appraisers.

## Reference(s):

- [钻石 4C 标准与选购指南](references/diamond-4c.md)
- [彩色宝石鉴定与选购指南](references/colored-gems.md)
- [翡翠鉴定与选购指南](references/jadeite.md)
- [珍珠鉴定与选购指南](references/pearls.md)
- [彩钻鉴定与选购指南](references/colored-diamonds.md)
- [贵金属鉴定与选购指南](references/precious-metals.md)
- [珠宝鉴定证书解读指南](references/certificates.md)
- [珠宝投资收藏指南](references/investment-guide.md)
- [GIA Report Check](https://www.gia.edu/report-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown guidance and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-price context from web search when the agent has browsing available; generated reports should retain the skill disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
