## Description:

Guides Chinese-speaking ecommerce operators to turn product details into strict soft-label ai_product_intro text aligned with a product-intake parser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdpb](https://clawhub.ai/user/kwdpb)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and merchants use this skill with a chat agent to collect product facts, selling points, audience, scenarios, and compliance boundaries into a strict Chinese ai_product_intro entry for an AI shopping-assistant knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product claims may be copied into a live ecommerce platform without enough factual or compliance review.

Mitigation: Review claims, source-backed facts, and restricted phrases before publication; use the disallowed and allowed expression fields to preserve compliance boundaries.

Risk: The skill is tailored to Chinese labels and ai_product_intro formatting, so unsupported labels, language changes, or loose formatting may not fit the intended intake workflow.

Mitigation: Keep the prescribed Chinese labels at the start of each line, preserve the expected punctuation, and ensure enough recognized labels are present before using the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kwdpb/skills/product-cognition-intake)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Product intake specification](artifact/规范.md)
- [Examples](artifact/examples.md)
- [Changelog](artifact/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text in strict Chinese soft-label lines; no code block.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses controlled Chinese labels, line-start label anchors, Chinese punctuation, and a minimum of three recognized labels with a core selling point or key fact.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
