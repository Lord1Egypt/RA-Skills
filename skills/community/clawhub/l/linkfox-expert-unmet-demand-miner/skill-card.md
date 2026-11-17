## Description:

亚马逊商品与细分市场未满足需求挖掘专家。适用于发现客户痛点、未满足需求、评论驱动的产品缺口、改良机会，以及从需求缺口生成产品概念的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, product researchers, and ecommerce operators use this skill to find products with meaningful demand and weak customer satisfaction, then review unmet needs, improvement opportunities, ranked candidates, and optional follow-on ASIN scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner found under-disclosed helpers that can persistently alter agent instructions.

Mitigation: Review or remove the CLAUDE.md patch helper before installation or execution.

Risk: The scanner found paths that can run environment-selected scripts and send credentials through environment-selected endpoints.

Mitigation: Install only in a controlled environment and lock LinkFox endpoint environment variables to intended HTTPS domains.

Risk: Scheduled product scouting can consume LinkFox credits.

Mitigation: Confirm every scheduled task, frequency, and estimated credit cost before enabling it.

Risk: File upload workflows can expose private files when public URLs or untrusted endpoints are used.

Mitigation: Upload only approved non-sensitive files and avoid public URLs for private data.

Risk: Unpinned dependencies can change behavior between installs.

Mitigation: Pin dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-unmet-demand-miner)
- [Amazon Product Scout API Parameters](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [SellerSprite Product Search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [ASIN Dynamic Scoring Example Expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [Task Scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)
- [Report Analysis Layouts](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [File Upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Excel files, CSV files, JSON, Guidance]

**Output Format:** [Markdown previews with generated Excel, CSV, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include Top 10 product previews, local file paths, scoring summaries, scheduled-task setup guidance, and follow-on research recommendations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
