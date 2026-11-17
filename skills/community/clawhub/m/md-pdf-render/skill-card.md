## Description:

Converts Markdown documents into high-fidelity PDFs with GitHub-flavored Markdown, code highlighting, tables, task lists, generated tables of contents, custom CSS, and selectable themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to convert trusted Markdown files into browser-rendered PDF documents with configurable themes, page layout, math, diagrams, headers, footers, and tables of contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering raw HTML in a network-enabled browser can expose sensitive or untrusted Markdown content to active content and external resource loading.

Mitigation: Convert only trusted Markdown, and for private or sensitive documents disable raw HTML and JavaScript and block network access during rendering.

Risk: Mermaid mode loads mutable third-party code from a CDN during conversion.

Mitigation: Prefer a locally bundled, pinned Mermaid dependency with strict security settings, or avoid Mermaid mode when network access is not acceptable.

Risk: The skill installs and runs an npm/Puppeteer tool that launches Chromium.

Mitigation: Review dependency lockfiles and run the converter in a constrained environment appropriate for document conversion workloads.

## Reference(s):

- [markdown-it](https://github.com/markdown-it/markdown-it)
- [Puppeteer](https://pptr.dev/)
- [Mermaid](https://mermaid-js.github.io/mermaid/)
- [KaTeX](https://katex.org/)
- [highlight.js](https://highlightjs.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated output is a PDF file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm dependencies; Puppeteer uses Chromium for PDF rendering.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
