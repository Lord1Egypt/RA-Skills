## Description:

Generates high-fidelity interactive product prototypes as standalone HTML files for quickly visualizing and validating product ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, designers, and developers use this skill to turn product concepts, MVP ideas, landing pages, and interface requests into clickable prototype pages for rapid review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad page, interface, or demo requests and produce a prototype when the user expected a narrower design artifact.

Mitigation: Confirm the product type, target users, core features, and visual style before generating the prototype.

Risk: Generated prototype HTML can load Tailwind CSS from a remote CDN.

Mitigation: Review generated HTML before use in restricted environments and replace the CDN dependency with approved local CSS when needed.

Risk: Prototype screens use simulated data and interactions that may be mistaken for production-ready behavior.

Mitigation: Label prototypes as validation artifacts and review them before entering sensitive or realistic test data.

## Reference(s):

- [Industry Design Specifications](artifact/references/industry-design-specs.md)
- [ClawHub Skill Page](https://clawhub.ai/yz6214589-hash/skills/product-prototype-design)
- [Tailwind CSS CDN](https://cdn.tailwindcss.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Standalone HTML file plus concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated prototypes may include Tailwind CSS from a remote CDN, native JavaScript interactions, simulated JSON data, and optional local assets.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
