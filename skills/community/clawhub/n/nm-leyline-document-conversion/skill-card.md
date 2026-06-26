## Description: <br>
Converts documents and URLs to markdown through a tiered fallback workflow using markitdown MCP when available, native tools where supported, and user-facing guidance when conversion is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn user-selected PDFs, Office documents, HTML, data files, images, audio, archives, e-books, or URLs into markdown for downstream processing while preserving clear fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted documents and URLs are external content and may contain misleading or instruction-like text. <br>
Mitigation: Apply the documented sanitization checklist, including size checks, stripping instruction tags, and external-content boundary markers. <br>
Risk: The optional markitdown MCP converter may process local files or remote URLs supplied by the user. <br>
Mitigation: Use it only for intended documents and avoid sensitive files unless the converter and execution environment are trusted. <br>
Risk: Some formats have limited or no native fallback support when markitdown MCP is unavailable. <br>
Mitigation: Follow the tiered fallback matrix and notify the user instead of guessing or fabricating content when conversion is unsupported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-document-conversion) <br>
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Format support matrix](artifact/modules/format-matrix.md) <br>
- [Fallback tier instructions](artifact/modules/fallback-tiers.md) <br>
- [URI construction rules](artifact/modules/uri-construction.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tiered fallback instructions and external-content sanitization guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
