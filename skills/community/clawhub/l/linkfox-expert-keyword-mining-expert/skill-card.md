## Description:

亚马逊关键词挖掘与扩展专家，适用于关键词发现、种子词扩展、流量词挖掘、反查 ASIN 关键词、搜索词筛选，以及为亚马逊选品研究生成关键词列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this agent to mine, validate, classify, and prioritize Amazon keywords from ASIN traffic data, search suggestions, ABA search terms, product reviews, and competitor signals for Listing optimization and PPC planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox account credentials, Amazon research data, and paid-service actions.

Mitigation: Install only for trusted LinkFox workflows, keep API keys private, and run onboarding in a private environment.

Risk: The bundled capabilities include scheduled tasks, uploads, and generated reports that can affect account workflows or expose shared outputs.

Mitigation: Review scheduled-task changes carefully and avoid uploading sensitive reports or files unless they are intended to become shareable URLs.

Risk: An untrusted tool gateway could receive account or research data.

Mitigation: Use only trusted LINKFOX_TOOL_GATEWAY values and review environment configuration before running helper scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-keyword-mining-expert)
- [LinkFox service site](https://skill.linkfox.com/)
- [SIF ASIN keyword API reference](artifact/skills/linkfox-sif-asin-keywords/references/api.md)
- [SellerSprite traffic keyword API reference](artifact/skills/linkfox-sellersprite-traffic-keyword/references/api.md)
- [ABA intelligent query API reference](artifact/skills/linkfox-aba-intelligent-query/references/api.md)
- [Amazon reviews API reference](artifact/skills/linkfox-amazon-reviews-list/references/api.md)
- [Amazon keyword taxonomy details](artifact/skills/amazon-keyword-library-builder/references/taxonomy-details.md)
- [Root and negative keyword logic](artifact/skills/amazon-keyword-library-builder/references/root-and-negative-logic.md)
- [Report layout reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Concise chat responses, Markdown summaries, structured keyword tables, and generated report or spreadsheet files when long-form delivery is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return paths or URLs for generated reports and exported keyword libraries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
