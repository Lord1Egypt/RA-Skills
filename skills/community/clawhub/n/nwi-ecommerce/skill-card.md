## Description:

NWi跨境电商数据分析 helps agents query NWi ecommerce data for Amazon, Shopee, Lazada, and TikTok Shop, including sales, category distribution, brand rankings, shop rankings, and Southeast Asia market views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwi-official](https://clawhub.ai/user/nwi-official)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketplace analysts, and agents use this skill to query cross-border ecommerce performance across supported marketplaces. It helps compare platform, category, brand, shop, and product sales signals and summarize the results for market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NWi API keys could be exposed through source control, shared workspaces, or logs.

Mitigation: Keep generated or manually supplied API keys out of source control and avoid printing them in shared logs or transcripts.

Risk: Ecommerce query parameters and optional anomaly submissions may reveal confidential business context.

Mitigation: Do not include personal data, secrets, or confidential business details in anomaly descriptions or query context.

Risk: Automatically selected brand or category matches can be ambiguous when multiple similar results exist.

Mitigation: Show likely matches to the user and confirm uncertain brand or category selections before relying on the data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nwi-official/skills/nwi-ecommerce)
- [API reference](references/api.md)
- [Platform ID reference](references/platform_ids.md)
- [NWi official website](https://nuozhoushuzhi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and prose with curl command examples and JSON API summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-key handling guidance, query parameter choices, result validation notes, and anomaly-reporting prompts.]

## Skill Version(s):

0.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
