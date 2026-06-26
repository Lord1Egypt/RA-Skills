## Description: <br>
Generates long vertical images from text, LaTeX formulas, code blocks, tables, and structured notes using canvas-rendered HTML templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daigxok](https://clawhub.ai/user/daigxok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content creators use this skill to turn course notes, study guides, documentation, product guides, posters, and knowledge cards into polished vertical PNG images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may render untrusted user-provided markup or content. <br>
Mitigation: Review or sanitize user-provided content before rendering, especially when inputs include raw HTML or copied web content. <br>
Risk: Remote fonts and CDN assets may expose content-loading behavior to third-party services or fail when network access is unavailable. <br>
Mitigation: Avoid confidential notes when remote assets are enabled, or replace remote dependencies with reviewed local assets. <br>
Risk: Sharing generated images through upload or temporary-link services can disclose the image contents. <br>
Mitigation: Use approved storage and sharing paths for sensitive outputs, and review images before publishing links. <br>


## Reference(s): <br>
- [KaTeX CDN asset](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js) <br>
- [highlight.js CDN asset](https://cdn.jsdelivr.net/gh/highlightjs/cdn-@11.9.0/build/highlight.min.js) <br>
- [Google Fonts CSS](https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=JetBrains+Mono&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Files] <br>
**Output Format:** [Markdown instructions with HTML, JavaScript, JSON, and PNG image-file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 1080px-wide vertical images; height auto-expands, with very long content recommended to be rendered in chunks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
