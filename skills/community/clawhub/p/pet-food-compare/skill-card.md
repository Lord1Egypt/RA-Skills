## Description:

Compares online dog and cat food products by collecting sourced facts about ingredients, prices, origin, nutrition, manufacturers, packaging, public product events, and user-review language without making purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen91](https://clawhub.ai/user/chenchen91)

### License/Terms of Use:

MIT-0

## Use Case:

External users comparing one or more dog or cat food SKUs use this skill to assemble a neutral, sourced comparison of product facts. It supports product-name, link, packaging-image, and screenshot inputs, then produces structured tables and notes for user review rather than a purchase recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat ingredient-to-condition mappings or prescription-diet comparisons as veterinary advice.

Mitigation: Keep the output informational, preserve the skill's purchase-advice disclaimer, and direct users to a veterinarian for prescription diets, urinary issues, allergies, obesity, kidney disease, or other health concerns.

Risk: Public product facts such as prices, formulas, reviews, packaging, and regulatory events may be incomplete or change over time.

Mitigation: Use dated source attribution, cross-check independent sources when available, and clearly mark facts that were not found or conflict across sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchen91/skills/pet-food-compare)
- [ClawHub publisher profile](https://clawhub.ai/user/chenchen91)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown tables with source links, concise notes, and standard Markdown image references when packaging images are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes neutral disclaimers, dated source attribution, and explicit unresolved-field notes such as unavailable product facts.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
