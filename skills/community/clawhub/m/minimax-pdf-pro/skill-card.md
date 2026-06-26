## Description: <br>
MiniMax PDF Pro helps agents create PDFs from HTML or LaTeX and process existing PDFs for extraction, merging, splitting, form filling, metadata, and file conversion tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate high-quality PDFs from HTML or LaTeX and to automate PDF workflows such as text extraction, table extraction, form filling, metadata updates, page operations, and office-file conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the local Node or Python environment and download browser or TeX dependencies. <br>
Mitigation: Run it in an isolated workspace or container, and preinstall and pin dependencies when possible. <br>
Risk: Browser-based HTML rendering and PDF processing can expose sensitive or untrusted document content to local tooling. <br>
Mitigation: Avoid sensitive or untrusted HTML unless network access is blocked and the execution environment is isolated. <br>
Risk: The LaTeX route documents a curl-to-shell Tectonic installation step. <br>
Mitigation: Do not use the curl-to-shell step without independent verification; install Tectonic through a trusted, pinned channel instead. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luaqnyin/minimax-pdf-pro) <br>
- [HTML route documentation](artifact/handlers/html.md) <br>
- [PDF processing route documentation](artifact/handlers/process.md) <br>
- [LaTeX route documentation](artifact/handlers/latex.md) <br>
- [LibreOffice download](https://www.libreoffice.org/download/) <br>
- [Tectonic installer endpoint](https://drop-sh.fullyjustified.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and generated HTML, LaTeX, JSON, or PDF-related files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or modify files and invoke local Node, Python, LibreOffice, Playwright, Chromium, or Tectonic tooling when dependencies are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
