## Description:

Converts Markdown into Word documents formatted for Chinese government official document layout under GB/T 9704-2012, with optional remote image embedding that can be disabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn Markdown reports, briefings, and structured documents into GB/T 9704-2012-style Word files. It is focused on formatting conversion and does not validate document content or add official document decorations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown containing remote image URLs can trigger outbound image fetches and expose network metadata in sensitive environments.

Mitigation: For untrusted Markdown or restricted networks, call md_to_docx with download_images=False and review image URLs before conversion.

Risk: The skill formats documents but does not review content, legal sufficiency, or official document completeness.

Mitigation: Review generated documents for content accuracy, compliance, and required official-document elements before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/gongwen-formatter)
- [Project homepage](https://github.com/EdwardWason/official-doc)

## Skill Output:

**Output Type(s):** [Files, Configuration, Guidance]

**Output Format:** [DOCX Word document with a success status and output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a .docx file; remote image downloads are optional and can be disabled with download_images=False.]

## Skill Version(s):

1.1.9 (source: server release evidence, artifact frontmatter, skill.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
