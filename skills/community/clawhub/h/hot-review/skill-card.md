## Description:

Analyzes Amazon bestseller and competitor reviews to identify product strengths, recurring complaints, buyer needs, and opportunities for product research and listing improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and product researchers use this skill to analyze Amazon product and competitor reviews, understand buyer sentiment, validate product ideas, and improve listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some review workflows may spend ARI credits without a clear confirmation, and a quote-only result may misstate whether a charge occurred.

Mitigation: Review the spending rules before installation, set ARI to ask before every charge, use the dedicated quote command for pricing, and approve recurring monitoring separately. Do not rely on the absent --confirm flag or deepdive's no-charge message; ask the publisher to correct these inconsistencies.

## Reference(s):

- [ARI API reference](references/reference.md)
- [ARI product management](https://ari.funewa.com/zh/products)
- [ARI reports](https://ari.funewa.com/zh/reports)
- [ARI monitoring](https://ari.funewa.com/zh/monitor)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Charts]

**Output Format:** [Concise natural-language summaries and Markdown reports, with rating, trend, and keyword charts where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the available review sample and time range; paid collection and analysis may use ARI credits.]

## Skill Version(s):

1.5.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
