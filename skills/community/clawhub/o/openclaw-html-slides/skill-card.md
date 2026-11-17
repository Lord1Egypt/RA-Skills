## Description:

Creates self-contained HTML slide decks for OpenClaw from user requirements, existing outlines, PPT/PPTX files, or existing HTML presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[838997125](https://clawhub.ai/user/838997125)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create, convert, preview, share, and export browser-based slide presentations with predefined visual styles and responsive layout rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deployment can publish slide content to a public Vercel URL.

Mitigation: Use local-only workflows for sensitive presentations and require explicit user confirmation before any upload or public deployment.

Risk: Deployment and export workflows may execute third-party packages through Node.js tooling.

Mitigation: Review commands before execution and prefer pinned, preinstalled dependencies in controlled environments.

Risk: PDF export uses a temporary local server that can expose local presentation files during export.

Mitigation: Run export only in trusted local environments and avoid exporting sensitive decks unless the temporary server risk is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/838997125/skills/openclaw-html-slides)
- [README](README.md)
- [HTML Presentation Template](html-template.md)
- [Style Presets Reference](STYLE_PRESETS.md)
- [Animation Patterns Reference](animation-patterns.md)
- [Viewport Base CSS](viewport-base.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets; generated decks are self-contained HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally guide Vercel deployment and PDF export workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
