## Description:

A privacy-focused multi-engine search skill with parallel retrieval, local RAG-lite answers, source checking, and privacy diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use the skill to search across multiple engines, inspect linked sources, and create cited summaries or privacy reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be disclosed to external search services, and strict privacy controls may not work as documented.

Mitigation: Avoid submitting sensitive queries until the search route and privacy configuration have been reviewed; verify settings before relying on strict mode.

Risk: Some referenced material was only partly inspected by the security review.

Mitigation: Review the referenced material and dependencies before relying on the skill for sensitive work.

## Reference(s):

- [Quick Start](artifact/references/QUICK_START.md)
- [Search Engines](artifact/references/engines.md)
- [MCP Schema](artifact/references/mcp_schema.md)
- [Search Syntax FAQ](artifact/references/detail_engine_syntax_faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Analysis]

**Output Format:** [Search results, cited summaries, and privacy reports in human-readable text or JSON, with optional Markdown exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include source links and confidence indicators; generated claims may be marked as unsupported.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
