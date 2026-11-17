## Description:

Analyzes low-star Amazon product reviews to extract product pain points and product opportunity insights with a Map-Reduce workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzhimin](https://clawhub.ai/user/zzhimin)

### License/Terms of Use:

MIT-0

## Use Case:

External product managers, product researchers, and ecommerce operators use this skill to analyze 1-3 star Amazon reviews, identify product defects and unmet needs, and turn them into a prioritized opportunity report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch Amazon review data through Bright Data and may store review data locally.

Mitigation: Review data handling before use, limit collection to needed reviews, and confirm retention or deletion of saved review files.

Risk: The helper script documents passing a Bright Data API key as a command-line argument.

Mitigation: Use a secret manager, environment variable, or interactive secret prompt instead of placing API keys in command history or process lists.

Risk: Generated opportunity reports may reflect incomplete or low-star-biased review data.

Mitigation: Review cited evidence and validate recommendations against broader product, market, and customer data before acting.

## Reference(s):

- [Product Opportunity Analyzer on ClawHub](https://clawhub.ai/zzhimin/skills/product-opportunity-analyzer)
- [Bright Data Amazon Product Reviews API](https://api.brightdata.com/datasets/v3/amazon_product_reviews)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports with structured JSON extraction steps and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch Amazon review data through Bright Data and may save extracted review data locally when the helper script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
