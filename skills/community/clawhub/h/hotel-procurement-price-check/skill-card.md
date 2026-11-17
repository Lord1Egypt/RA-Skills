## Description:

Provides hotel procurement teams with real-time price comparison across agricultural wholesale sources and e-commerce marketplaces, with procurement price guidance and cost-reference analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel procurement and food-service purchasing teams use this skill to compare agricultural wholesale and e-commerce prices for ingredients or supplies, then produce a sourced price range, recommended procurement range, and cost-reference notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product names and procurement interests may be sent to external search or marketplace sources.

Mitigation: Avoid confidential SKU codes, unreleased menu plans, supplier strategy, or sensitive internal product names unless the organization approves that disclosure.

Risk: Returned prices can be volatile, location-dependent, or incomplete when external sources fail.

Mitigation: Treat outputs as procurement references and verify source timestamps, local quotes, logistics, and specification differences before purchase decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/hotel-procurement-price-check)
- [Ministry of Agriculture and Rural Affairs price monitoring](http://www.scs.moa.gov.cn/jcyj/)
- [Agricultural product market dynamics](http://www.agri.cn/sj/jcyj/)
- [Yimutian wholesale marketplace](https://www.ymt.com/)
- [Huinoong market price listings](https://www.cnhnb.com/pi/list)
- [China Vegetable Network](http://www.vegnet.com.cn/)
- [Beijing Xinfadi wholesale market](https://www.xinfadi.com.cn/)
- [1688 Open Platform](https://open.1688.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style price reports with sourced price ranges, market comparisons, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source timestamps, platform comparisons, procurement price suggestions, cost-floor estimates, and caveats about local pricing, logistics, specifications, and source availability.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
