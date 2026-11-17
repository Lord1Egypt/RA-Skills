## Description:

Simulates live Amazon storefront searches so agents can retrieve current keyword rankings, product listings, prices, ratings, sponsored status, and marketplace-specific SERP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, Amazon sellers, and e-commerce analysts use this skill to inspect current Amazon search result pages for keyword ranking checks, competitor discovery, price comparison, sponsored product analysis, and new product monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines Amazon search with LinkFox account login, API key handling, balance purchases, local storage, and feedback reporting beyond the search workflow.

Mitigation: Review these behaviors before installation, use only trusted environment variables, and avoid custom LinkFox gateway URLs unless you control them.

Risk: Generated API keys, SMS codes, payment flow outputs, and full search responses may contain sensitive or business-relevant information.

Mitigation: Treat these values and saved response files as sensitive, run the skill in an appropriate workspace, and remove local artifacts when they are no longer needed.

Risk: Searches consume paid compute and repeated parameter changes can increase cost.

Mitigation: Confirm with the user before additional pages, changed keywords, changed postal codes, or other repeated searches that would incur extra consumption.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-search)
- [亚马逊前端搜索模拟 API 参考](artifact/references/api.md)
- [解决认证和算力问题](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries and tables with JSON API responses saved to local files when the search script runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses are summarized by default; full responses can be printed inline and are cached for 24 hours for identical parameters.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
