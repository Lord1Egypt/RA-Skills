## Description:

Render Mermaid code into PNG images supporting all 27 Mermaid 11 chart types, with optional upload to Feishu docs, requiring no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate Mermaid diagrams from prompts or Mermaid code and render them as PNG images, optionally uploading the result to Feishu documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering user-supplied diagram text in a browser can expose unsafe script or HTML handling.

Mitigation: Review diagram content before rendering, prefer HTML-escaped Mermaid input, and use strict Mermaid security settings.

Risk: External network paths may be used for Mermaid CDN loading, mermaid.ink fallback rendering, or optional Feishu upload.

Mitigation: Avoid sensitive diagrams unless external network use is acceptable, make external rendering and upload explicit opt-in actions, and prefer pinned or locally vendored Mermaid assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xx235300/skills/mermaid-canvas)
- [Mermaid syntax guide](references/syntax-guide.md)
- [Mermaid diagram patterns](references/diagram-patterns.md)
- [Mermaid official documentation](https://mermaid.nodejs.cn/)
- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid CDN](https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Mermaid code blocks and PNG image outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Feishu upload when requested.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
