## Description:

Intelligent product recommendation engine for retail digital employees that recommends products based on customer needs, budget, recipient, occasion, preferences, and purchase history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Retail teams and external-facing digital employees use this skill to answer customer help-me-choose requests with curated product shortlists, comparisons, pairing suggestions, and cautious upsell options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may relax budget constraints or fall back to top products when strict matches are unavailable.

Mitigation: Review or adjust fallback behavior before use cases where budget, allergy, material, safety, or other hard constraints must never be relaxed.

Risk: Recommendation quality depends on product catalog, attribute, and inventory data quality.

Mitigation: Use current product, stock, and attribute data, and review customer-facing recommendations before deployment in high-impact retail contexts.

## Reference(s):

- [Product Filtering & Scoring Logic](references/filtering-logic.md)
- [Intent Extraction Guide](references/intent-extraction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance for agent replies and JSON arrays from the bundled recommendation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script output may include recommendation scores when run with --include-scores.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
