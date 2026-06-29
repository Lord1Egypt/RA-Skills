## Description: <br>
Converts documents and URLs to markdown via tiered fallback using MCP markitdown, native tools, and user notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDF, Office, web, data, image, audio, archive, and e-book inputs into markdown for downstream processing. It is most useful when the source content is not already plain text or markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes external documents and untrusted links, which can include sensitive data or embedded instructions. <br>
Mitigation: Invoke it only for files or URLs intended for conversion, and apply the documented content-sanitization checklist to converted content. <br>
Risk: Some formats depend on the markitdown MCP server; without it, conversion quality or coverage can degrade. <br>
Mitigation: Use the native fallback paths for supported formats and clearly notify the user when a format cannot be converted without markitdown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-leyline-document-conversion) <br>
- [Publisher Profile](https://clawhub.ai/user/athola) <br>
- [Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Format Support Matrix](artifact/modules/format-matrix.md) <br>
- [Fallback Tier Instructions](artifact/modules/fallback-tiers.md) <br>
- [URI Construction](artifact/modules/uri-construction.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include converted document content, fallback instructions, or setup guidance when markitdown MCP is unavailable.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
