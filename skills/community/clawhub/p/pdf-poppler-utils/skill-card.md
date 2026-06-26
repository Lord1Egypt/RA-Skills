## Description: <br>
A collection of PDF manipulation tools from the poppler-utils package for extracting PDF text, images, metadata, fonts, attachments, signatures, page ranges, and converted output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xlionjuan](https://clawhub.ai/user/xlionjuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and document-processing agents use this skill to choose and run Poppler PDF command-line utilities for local PDF inspection, extraction, conversion, splitting, merging, attachment handling, and signature checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends `brew unlink curl -v`, a system-changing Homebrew operation that can affect other tools. <br>
Mitigation: Require explicit user approval and explain the impact before running it; prefer normal `brew install poppler` setup unless the user is troubleshooting a curl conflict. <br>
Risk: Password, DRM override, hidden-text extraction, attachment extraction, and signing options can expose protected content or alter document trust properties. <br>
Mitigation: Use these options only for documents the user is authorized to process, and avoid placing real passwords directly in command history. <br>
Risk: PDF conversion and extraction commands may write many output files or overwrite expected paths. <br>
Mitigation: Use a dedicated output directory or unique filename prefixes and review target paths before executing conversion, extraction, split, or merge commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xlionjuan/pdf-poppler-utils) <br>
- [Debian poppler-utils manpages](https://manpages.debian.org/testing/poppler-utils/index.html) <br>
- [Homebrew](https://brew.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, code] <br>
**Output Format:** [Markdown with inline bash code blocks and command option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local Poppler CLI command guidance; generated PDF, text, image, HTML, SVG, PostScript, or attachment files are produced by the invoked tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
