## Description:

Generates Chinese-language analysis reports for pet technology products by combining product specifications, competitor comparisons, public user reviews, and sponsored-content screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, reviewers, and shopping researchers use this skill to compare smart cat litter boxes, automatic feeders, water fountains, and related pet devices before purchase. It helps produce structured, source-linked reports with product ratings, authenticity screening, and buying guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search public web platforms and ecommerce pages, which can expose sensitive prompt details if users provide private account information or personal data.

Mitigation: Use public product names and non-sensitive requirements, and avoid sharing private account details or sensitive personal data.

Risk: Product prices, reviews, and sponsorship signals change over time, so stale or incomplete public information can affect recommendations.

Mitigation: Include the analysis date, cite sources, and cross-check multiple current public sources before acting on purchase guidance.

Risk: Sponsored-content screening is heuristic and can misclassify authentic reviews or promotional posts.

Mitigation: Label source credibility, disclose low-confidence sources, and keep purchase advice conditional when evidence is mixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hwl1413520/skills/pet-product-analysis)
- [Pet Product Analysis Framework](references/ANALYSIS_FRAMEWORK.md)
- [Sponsored Content Screening Guide](references/SPONSORED_CONTENT_GUIDE.md)
- [Report Template](assets/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese-language Markdown report with comparison tables, source links, ratings, and purchase guidance; optionally structured JSON/CSV or document exports when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public source links and generated product comparison tables; report quality depends on current web search results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
