## Description:

MiniMax PDF Pro helps agents create PDFs from HTML/Paged.js or LaTeX and process existing PDFs for extraction, page operations, metadata updates, conversion, and form filling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate polished PDF documents, compile LaTeX when explicitly requested, and operate on existing PDFs for extraction, merging, splitting, rotation, cropping, metadata, conversion, and form filling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup can modify the development environment and includes a remote `curl | sh` installer path for Tectonic.

Mitigation: Install in an isolated environment and use a verified Tectonic release or package manager instead of piping a remote script into the shell.

Risk: HTML to PDF conversion can load local HTML through Chromium and may allow more file and network access than needed for untrusted input.

Mitigation: Run conversion in a sandbox with network access and local file reads disabled or tightly scoped when processing untrusted HTML.

Risk: PDF and Office processing depends on external tools such as Playwright, Chromium, Python packages, and LibreOffice.

Mitigation: Review requested commands before execution and pin or verify dependencies in the deployment environment.

## Reference(s):

- [MiniMax PDF Pro on ClawHub](https://clawhub.ai/luaqnyin/skills/minimax-pdf-pro)
- [HTML route evidence](artifact/handlers/html.md)
- [LaTeX route evidence](artifact/handlers/latex.md)
- [PDF processing route evidence](artifact/handlers/process.md)
- [LibreOffice download](https://www.libreoffice.org/download/)
- [Tectonic installer endpoint referenced by artifact](https://drop-sh.fullyjustified.net)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated artifacts such as HTML, LaTeX, JSON command output, and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local files and install document-processing dependencies when directed by the skill workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
