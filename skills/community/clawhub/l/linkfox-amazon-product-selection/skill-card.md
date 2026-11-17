## Description:

亚马逊选品一站式 AI 工具集，整合竞品查询、ABA、前台、Keepa、Sorftime、Jungle Scout、卖家精灵、SIF、极目和商业洞察等工具，覆盖选品、关键词、竞品、评论、利基与趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, e-commerce analysts, and agent users use this skill to gather Amazon product, keyword, competitor, review, niche, and trend data across supported marketplaces. It helps agents choose an appropriate LinkFox sub-capability, run the matching script, and summarize sourced product research results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and configurable remote endpoints.

Mitigation: Review before installation, keep LinkFox endpoint variables controlled by trusted users, and avoid custom gateway URLs unless the endpoint is trusted.

Risk: Generated API keys and billing artifacts may expose account or payment information.

Mitigation: Treat API keys as secrets, prefer a secret manager over shell-profile storage, and review payment or order QR files before sharing the workspace.

Risk: Full API responses may be written under a local linkfox directory.

Mitigation: Run the skill in a workspace with appropriate access controls and handle saved response files as potentially sensitive research data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-product-selection)
- [Main skill definition](artifact/SKILL.md)
- [ABA Intelligent Query](artifact/references/linkfox-aba-intelligent-query.md)
- [Amazon Alexa Shopping Assistant](artifact/references/linkfox-amazon-alexa-search.md)
- [Amazon Market Opportunity Report](artifact/references/linkfox-amazon-opportunity-report-by-keyword.md)
- [Amazon Opportunity Screener by Metrics](artifact/references/linkfox-amazon-opportunity-search-by-metrics.md)
- [Amazon Product Detail Lookup](artifact/references/linkfox-amazon-product-detail.md)
- [Amazon Product Reviews](artifact/references/linkfox-amazon-reviews-list.md)
- [Amazon Search by Image](artifact/references/linkfox-amazon-search-by-image.md)
- [Amazon Product Search](artifact/references/linkfox-amazon-search.md)
- [Jiimore Niche Info by Keyword](artifact/references/linkfox-jiimore-get-niche-info-by-keyword.md)
- [Jiimore Niche Market Info](artifact/references/linkfox-jiimore-get-niche-info.md)
- [Jiimore Niche Review from Keyword](artifact/references/linkfox-jiimore-get-niche-review-from-keyword.md)
- [Jiimore Page Asins By Asin](artifact/references/linkfox-jiimore-page-asins-by-asin.md)
- [Jiimore Product Discovery](artifact/references/linkfox-jiimore-product-discovery.md)
- [Jungle Scout Keyword by ASIN](artifact/references/linkfox-junglescout-keyword-by-asin.md)
- [Jungle Scout Keyword by Keyword](artifact/references/linkfox-junglescout-keyword-by-keyword.md)
- [Jungle Scout Keyword History](artifact/references/linkfox-junglescout-keyword-history.md)
- [Jungle Scout Keyword Share of Voice](artifact/references/linkfox-junglescout-keyword-share-of-voice.md)
- [Jungle Scout Product Database](artifact/references/linkfox-junglescout-product-database.md)
- [Jungle Scout Sales Estimates](artifact/references/linkfox-junglescout-sales-estimates.md)
- [Keepa Product Request](artifact/references/linkfox-keepa-product-request.md)
- [Keepa Product Search](artifact/references/linkfox-keepa-product-search.md)
- [Keepa Product Time-Series Data Explorer](artifact/references/linkfox-keepa-product-series.md)
- [SellerSprite Competitor Lookup](artifact/references/linkfox-sellersprite-competitor-lookup.md)
- [SellerSprite Market Research](artifact/references/linkfox-sellersprite-market-research.md)
- [SellerSprite Market Statistics](artifact/references/linkfox-sellersprite-market-statistics.md)
- [SellerSprite Product Search](artifact/references/linkfox-sellersprite-product-search.md)
- [SellerSprite Traffic Keyword](artifact/references/linkfox-sellersprite-traffic-keyword.md)
- [SIF ASIN Keyword Analysis](artifact/references/linkfox-sif-asin-keywords.md)
- [SIF ASIN Summary](artifact/references/linkfox-sif-asin-summary.md)
- [SIF Keyword Overview](artifact/references/linkfox-sif-keyword-overview.md)
- [SIF Keyword Traffic Source Summary](artifact/references/linkfox-sif-keyword-summary.md)
- [Sorftime Amazon Product Detail](artifact/references/linkfox-sorftime-amazon-product-detail.md)
- [Sorftime Product Search](artifact/references/linkfox-sorftime-amazon-product-query.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown summaries with script commands and local JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under a local linkfox session data directory; small responses may print inline, while larger responses print summaries unless inline output is requested.]

## Skill Version(s):

1.2.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
