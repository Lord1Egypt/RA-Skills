## Description:

Html Report Slides helps agents create single-file, PPT-style HTML report decks for strategy presentations, architecture overviews, cost analyses, and roadmap slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business users can use this skill to turn report content into a polished standalone HTML slide deck with reusable presentation components. It is aimed at technical briefings, cost reviews, strategy updates, product roadmaps, and architecture diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes behavior that may append future lessons back into SKILL.md.

Mitigation: Require explicit user approval before modifying the skill source, and review any persistent changes before installing in shared environments.

Risk: Generated or copied templates may load an external font resource.

Mitigation: Approve the external font load, remove it, or use the bundled fallback font stack before sharing or deploying in restricted environments.

Risk: Example files or copied snippets may contain leftover external links or context-specific content.

Mitigation: Audit generated HTML and reused examples before publishing, especially for external links, internal names, and sensitive report data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dengjiawei1226/skills/html-report-slides)
- [Design System](artifact/references/design-system.md)
- [SVG Architecture Rules](artifact/references/svg-architecture-rules.md)
- [Component Index](artifact/components/README.md)
- [Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Single-file HTML with Markdown or text guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks are intended to be standalone, browser-viewable, responsive, and print/PDF-ready.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
