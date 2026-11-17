## Description:

Generate polished slide decks as self-contained HTML and editable PowerPoint from notes, with theme, layout, and craft guidance for pitch decks, investor updates, keynotes, product launches, sales demos, and other presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isatimur](https://clawhub.ai/user/isatimur)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and presentation authors use this skill to turn briefs or notes into structured slide decks, rendered HTML presentations, and editable PowerPoint outputs. It is suited for business, product, sales, investor, keynote, and demo presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional share and deployment paths can publish decks externally.

Mitigation: Use the Vercel deployment path only when public or external sharing is intended, and confirm sensitive deck content before deployment.

Risk: npm-based rendering and deployment tooling may execute package versions from the registry.

Mitigation: Run the tooling in a constrained environment and prefer pinned or locally locked renderer and deployment dependencies.

Risk: Exporting untrusted HTML decks to PDF can expose the exporter to network requests from deck content.

Mitigation: Do not export untrusted HTML decks on networks that can reach sensitive internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/isatimur/skills/presentation-generator)
- [Presentation Generator Homepage](https://presentation-md.vercel.app)
- [Presentation Studio](https://presentation-md.vercel.app/studio)
- [Source Repository](https://github.com/isatimur/presentation-md)
- [Deck Schema](references/deck-schema.md)
- [Theme Guide](references/themes.md)
- [Layout Recipes](references/layout-recipes.md)
- [Markdown Import](references/markdown-import.md)
- [PPTX Import](references/pptx-import.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, deck JSON, self-contained HTML, editable PPTX export instructions, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local rendering, auditing, export, and optional deployment tooling when available.]

## Skill Version(s):

1.32.2 (source: frontmatter and server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
