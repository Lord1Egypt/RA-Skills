## Description:

Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, educators, and business users use this skill to create browser-native presentation decks, convert PPT/PPTX files to HTML slides, and improve existing HTML presentations with distinctive visual design and strict viewport fitting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Vercel deployment can publish presentation content to a public URL.

Mitigation: Use deployment only for decks that do not contain confidential or sensitive content, and remove the deployment when it is no longer needed.

Risk: PDF export and deployment workflows can run Node-based tooling and unpinned packages.

Mitigation: Review commands before execution, run them in a trusted workspace, and pin dependencies before production use.

Risk: The PDF export path starts a temporary local file server with path-containment concerns.

Mitigation: Use trusted local input files only and fix the export server path containment before relying on the workflow for sensitive material.

## Reference(s):

- [Style Presets Reference](references/STYLE_PRESETS.md)
- [Animation Patterns Reference](references/animation-patterns.md)
- [HTML Presentation Template](references/html-template.md)
- [Viewport Base CSS](references/viewport-base.css)
- [Vercel Documentation](https://vercel.com)
- [Playwright Documentation](https://playwright.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated self-contained HTML, inline CSS and JavaScript, and shell command blocks for conversion, export, or deployment workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML presentation files, style preview files, extracted PPTX assets, PDF exports, or deployment commands depending on the user workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
