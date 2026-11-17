## Description:

Creates Reveal.js HTML presentations for decks, reports, and teaching slides, with guidance for layouts, themes, charts, speaker notes, and browser-based playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cao-yuu](https://clawhub.ai/user/cao-yuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate browser-run Reveal.js slide decks for presentations, reports, and teaching materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentations are active HTML and may load mutable third-party scripts or CDN resources.

Mitigation: Review generated HTML, CSS, and JavaScript before use, prefer pinned or local dependencies, and open outputs in a low-privilege browser context.

Risk: Helper scripts may process user-provided titles, stylesheet names, and output paths.

Mitigation: Use the skill only in a workspace where presentation files can be safely created, and avoid untrusted paths or untrusted presentation metadata.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cao-yuu/skills/ppt-skill)
- [Advanced Features Reference](revealjs/references/advanced-features.md)
- [Charts Reference](revealjs/references/charts.md)
- [Base Styles CSS](revealjs/references/base-styles.css)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets; generated presentation files are HTML and CSS.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces browser-runnable Reveal.js presentations and may use Node.js helper scripts for scaffolding and checks.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter and package.json: 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
