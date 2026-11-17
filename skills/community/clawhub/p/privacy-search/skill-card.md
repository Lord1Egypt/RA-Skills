## Description:

Helps agents search multiple engines with configurable privacy settings, ranked results, optional source-backed answers, and web-page retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search across web engines, review ranked sources, and optionally synthesize cited answers or retrieve page text while controlling search privacy settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and update checks send requests to external services and may expose queries or the user's IP address.

Mitigation: Use an appropriate proxy or local search setup for sensitive searches, and disable startup update checks when needed.

Risk: Local cache, history, and logs can retain sensitive search activity.

Mitigation: Disable cache, history, and logging for sensitive searches, or clear retained data afterward.

Risk: Optional answer synthesis may share prompts and fetched page text with an LLM provider when an API key is configured.

Mitigation: Do not configure synthesis with sensitive content unless that provider and data transfer are approved.

Risk: MCP page retrieval and synthesis can request arbitrary URLs from the user's machine.

Mitigation: Restrict MCP tools to those needed; disable fetch and synthesize in untrusted contexts.

## Reference(s):

- [ClawHub release](https://clawhub.ai/fyniujin/skills/privacy-search)
- [Quick start](references/QUICK_START.md)
- [Search engines](references/engines.md)
- [Search syntax and FAQ](references/detail_engine_syntax_faq.md)
- [MCP tool schema](references/mcp_schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Search results and optional cited answers as text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include source links and engine-count confidence indicators; optional answer synthesis and page retrieval.]

## Skill Version(s):

1.9.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
