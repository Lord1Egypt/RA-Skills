## Description:

Compares public information about online dog and cat food products in a neutral, source-linked format without making purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen91](https://clawhub.ai/user/chenchen91)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather, cross-check, and compare dog and cat food product information from product links, names, packaging images, or screenshots. It produces neutral comparison tables with citations, missing-data notes, conflict handling, and a veterinary-decision disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public web, image, and review-source data may be outdated, incomplete, promotional, or inconsistent across sources.

Mitigation: Cross-check product facts across independent sources, cite each source, list conflicting values side by side, and mark unavailable fields as not found instead of filling gaps.

Risk: Packaging photos and screenshots can produce OCR or visual recognition mistakes.

Mitigation: Restate extracted product names and key structured fields for user confirmation, then verify missing or critical nutrition and ingredient data through public sources.

Risk: Animal-condition mapping, prescription diets, and health-related product context can be mistaken for veterinary advice.

Mitigation: Keep the output informational and neutral, avoid purchase or treatment recommendations, and include a disclaimer that final pet health decisions should rely on a veterinarian.

## Reference(s):

- [Server-resolved source provenance](https://github.com/chenchen91/pet-food-compare/tree/main/skills/pet-food-compare)
- [ClawHub skill page](https://clawhub.ai/chenchen91/skills/pet-food-compare-2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Simplified Chinese Markdown tables with source links and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs neutral product information only; it must not provide purchase recommendations or veterinary determinations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
