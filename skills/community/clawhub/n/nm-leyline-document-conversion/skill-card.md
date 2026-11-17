## Description:

Converts documents and URLs to markdown via tiered fallback (MCP markitdown, native tools, user notice)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert documents and URLs into Markdown for downstream processing or editable project imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted external content may contain instruction-like text that affects downstream processing.

Mitigation: Follow the documented sanitization steps: strip system and instruction tags, apply size limits, and mark external-content boundaries.

Risk: The security scan is partial because two local references in SKILL.md could not be resolved.

Mitigation: Review the unresolved references before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-document-conversion)
- [Night Market Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown text, with JSON configuration examples when conversion support is unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted external content is sanitized, wrapped in source boundaries, and limited to 2,000 words per section.]

## Skill Version(s):

1.10.3 (source: frontmatter; release evidence: 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
