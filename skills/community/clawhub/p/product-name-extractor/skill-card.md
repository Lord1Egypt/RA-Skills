## Description:

Precisely extract product names from user-provided text, ignoring all irrelevant information and outputting only the product names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to extract only product names from supplied product descriptions, lists, articles, conversations, or similar text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally returns only product names or a no-detection message, so users should not expect explanations or evidence for each extraction.

Mitigation: Use it where terse extraction output is desired, and ask separately for reasoning or validation when those are required.

Risk: The skill is constrained not to fabricate product names, but ambiguous input may still lead to missed or incorrect detections.

Mitigation: Provide clear source text and review extracted names before using them in downstream records or customer-facing workflows.

## Reference(s):

- [Product Name Extractor on ClawHub](https://clawhub.ai/openlark/skills/product-name-extractor)
- [OpenLark Publisher Profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with one detected product name per line, or the exact no-detection message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No explanations, titles, formatting, or inferred product names should be included.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
