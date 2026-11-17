## Description:

Generates Excalidraw hand-drawn diagram files from natural language descriptions, including flowcharts, mind maps, architecture diagrams, ER diagrams, and sequence diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcdowell8023](https://clawhub.ai/user/mcdowell8023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to turn natural language diagram requests into editable Excalidraw files and, when appropriate, exported PNG images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PNG export runs Playwright/Chromium with network-loaded JavaScript and weakened browser isolation.

Mitigation: Make PNG export explicit opt-in and run it only in an isolated environment with pinned or vendored dependencies and browser sandboxing restored.

Risk: Sensitive diagram contents may be exposed or processed in a higher-risk path during PNG export.

Mitigation: Use plain .excalidraw JSON generation for sensitive diagrams, or use a trusted offline export path before exporting sensitive content.

## Reference(s):

- [Element Specification](references/element-spec.md)
- [Diagram Templates](references/diagram-templates.md)
- [Examples](references/examples.md)
- [Headless Export](references/headless-export.md)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Excalidraw JSON files (.excalidraw), optional PNG files, and concise Markdown status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG export uses Playwright/Chromium and network-loaded Excalidraw assets; plain .excalidraw JSON generation is lower risk.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
