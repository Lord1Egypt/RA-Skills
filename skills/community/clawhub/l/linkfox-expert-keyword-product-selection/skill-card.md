## Description:

关键词选品专家 runs an Amazon keyword-product selection workflow around a seed term or supplied keywords, using Amazon search, SellerSprite supply-demand metrics, and representative product details to produce ranked niche candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce analysts use this skill to expand or validate product keywords, compare demand and competition signals, screen out weak or crowded niches, and produce a ranked candidate list for product selection. The workflow supports configurable thresholds for price, demand, monopoly tolerance, competition, CPC, purchase rate, and ranking method.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox account credentials and onboarding tokens while calling LinkFox and Amazon-related services.

Mitigation: Use a dedicated, revocable LinkFox API key and prefer session-only credential storage instead of writing credentials to shell startup files.

Risk: The workflow can trigger paid-service actions and may consume account balance during repeated Amazon, SellerSprite, and Keepa calls.

Mitigation: Review the planned query volume and cost implications before high-frequency calls, pagination, or batch product-detail lookups.

Risk: The skill stores result files locally and may retain keyword, ASIN, market, and report data after a session.

Mitigation: Avoid sensitive inputs unless local retention is acceptable, and review or remove stored result files according to the user's data-handling requirements.

Risk: Optional file upload can make generated files publicly accessible, and generated HTML reports may contain business-sensitive research.

Mitigation: Review any uploaded file or generated report before sharing it publicly, and upload only content intended for external access.

Risk: The artifact describes automatic feedback reporting to LinkFox when behavior, results, or user sentiment indicate an issue.

Mitigation: Install only if this feedback behavior is acceptable, and review the skill's API references and security guidance before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-keyword-product-selection)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Keyword Selection Workflow](skills/keyword-selection-method/SKILL.md)
- [S1 Candidate Keyword Collection](skills/keyword-selection-method/references/steps/S1.md)
- [S2 Supply-Demand Filtering](skills/keyword-selection-method/references/steps/S2.md)
- [S3 Representative Product Enrichment](skills/keyword-selection-method/references/steps/S3.md)
- [S4 Ranked Candidate Output](skills/keyword-selection-method/references/steps/S4.md)
- [Report Layout Reference](skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON result files, shell command guidance, and optional HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include ranked keyword-market candidates with demand, supply-demand ratio, search volume, product count, CPC, monopoly rate, purchase metrics, competition grade, price band, funnel conclusion, suggested action, sort basis, and representative product details; missing source fields are explicitly marked as unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
