## Description:

Use this skill when the user asks for an HTML-first visual design deliverable: interactive prototype, slide deck, motion demo, infographic, dashboard, landing page, whitepaper, changelog, business card, social cover, brand system, design critique, multi-variant exploration, or export planning for MP4, GIF, PPTX, PDF, or SVG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peixl](https://clawhub.ai/user/peixl)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and agents use this skill to turn natural-language visual design requests into local HTML-first artifacts, including prototypes, decks, dashboards, infographics, motion demos, brand systems, and export-ready source structures. It routes requests through predefined modes and templates, then reports assumptions, verification evidence, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commercial, client-owned, or white-label design work may include IFQ branding, ifq.ai text, links, colophons, or visual marks.

Mitigation: Ask explicitly for clean-room white-label output and audit generated HTML before delivery.

Risk: Some showcase files may load scripts from unpkg.com.

Mitigation: Avoid opening or reusing showcase files that load remote scripts unless that network execution is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peixl/skills/ifq-design-skills)
- [Project homepage](https://github.com/peixl/ifq-design-skills)
- [Package repository](https://github.com/peixl/ifq-design-clawhub)
- [README](README.md)
- [Modes](references/modes.md)
- [Template index](assets/templates/INDEX.json)
- [Asset protocol](references/asset-protocol.md)
- [Verification](references/verification.md)
- [Anti-slop preflight](references/anti-ai-slop.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML files with Markdown summaries, inline shell commands, and optional export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local workspace artifacts; optional outbound HTTPS may be used for fact checks, fonts, and legal image assets when available.]

## Skill Version(s):

2.4.3 (source: frontmatter, clawhub.json, package.json, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
