## Description:

Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking downloads and revenue, and market insights via api.admapix.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts, app publishers, and growth teams use this skill to search advertising creatives, analyze apps and competitors, review rankings, and summarize market, download, revenue, and ad distribution signals from AdMapix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may share campaign plans, app identifiers, personal user IDs, or other sensitive analytics context with the third-party AdMapix API.

Mitigation: Avoid submitting confidential or personal data unless sharing it with AdMapix is intended and approved.

Risk: The skill requires SKILLBOSS_API_KEY for API access, which could leak if printed in chat output, logs, or command traces.

Mitigation: Keep the key in the configured environment, never echo it, and use only presence checks that do not reveal the value.

Risk: The Chinese README includes an unpinned npx installation example.

Mitigation: Prefer the trusted ClawHub/OpenClaw install path or a pinned installer version before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/skills/martin-admapix)
- [AdMapix Website](https://www.admapix.com)
- [Creative Search API](artifact/references/api-creative.md)
- [Product and Company API](artifact/references/api-product.md)
- [Ranking API](artifact/references/api-ranking.md)
- [Download and Revenue API](artifact/references/api-download-revenue.md)
- [App Distribution API](artifact/references/api-distribution.md)
- [Market Analysis API](artifact/references/api-market.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, follow-up prompts, H5 result links, and inline shell commands for API key checks and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses adapt between Chinese and English and include disclaimers when download or revenue figures are third-party estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
