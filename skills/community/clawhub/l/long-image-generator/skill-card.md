## Description:

Long Image Generator helps agents create vertical long-form PNG images from text, LaTeX formulas, code blocks, tables, and structured notes using canvas-rendered HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to convert lessons, study guides, reading notes, product explanations, and technical material into shareable long-form images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images may include sensitive notes, documents, code, or other private content if user-provided material is rendered directly.

Mitigation: Use local output by default, review generated images before sharing, and remove sensitive content before any upload.

Risk: The skill can send generated image files to external hosting to provide download links.

Mitigation: Require explicit user approval before uploading any generated image or source material to an external service.

Risk: Canvas templates load remote fonts and scripts, which may create network exposure or supply-chain risk.

Mitigation: Prefer trusted or bundled assets where available, and disclose or approve remote dependencies before rendering.

Risk: A fixed footer attribution may appear in generated templates even when it is not wanted.

Mitigation: Review and remove unwanted footer attribution before sharing or publishing generated images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daigxok/skills/long-image-generator)
- [Google Fonts stylesheet used by the canvas template](https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=JetBrains+Mono&display=swap)
- [KaTeX stylesheet used for formula rendering](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css)
- [KaTeX script used for formula rendering](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js)
- [highlight.js stylesheet used for code highlighting](https://cdn.jsdelivr.net/gh/highlightjs/cdn-@11.9.0/build/styles/github.min.css)
- [highlight.js script used for code highlighting](https://cdn.jsdelivr.net/gh/highlightjs/cdn-@11.9.0/build/highlight.min.js)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript snippets plus PNG image file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default canvas width is 1080px, height expands with content, and generated images may be kept local or uploaded for download links.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
