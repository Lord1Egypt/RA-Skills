## Description:

Generate beautiful macaron-color cartoon illustration-style card images from text content. Supports various types such as book recommendation cards, concept cards, quote cards, and comparison cards, with multiple aspect ratios including 3:4, 9:16, and 1:1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn structured text into stylized card assets for book recommendations, concepts, quotes, and comparisons. It helps agents prepare card data, generate an HTML card, and render it to a PNG with browser screenshot tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted card text can become active HTML or JavaScript during screenshot rendering.

Mitigation: Render cards only from trusted content or isolate the screenshot browser; escape all text fields, add a restrictive Content Security Policy, and block network access during rendering.

Risk: Generated files can be written to paths supplied at runtime.

Mitigation: Keep generated HTML and PNG outputs inside a controlled workspace path.

## Reference(s):

- [Macaron Card Design Reference](references/design_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/macaron-card-generator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with JSON content examples, shell commands, generated HTML files, and PNG screenshot outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports book, concept, quote, and comparison card types with 1:1, 3:4, 4:3, 9:16, 16:9, and 2:3 aspect ratios.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
