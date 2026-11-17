## Description:

Finds and ranks relevant academic papers from Google Scholar using real-time Scholar retrieval, query expansion, deduplication, and local venue-quality scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[figpad](https://clawhub.ai/user/figpad)

### License/Terms of Use:

MIT

## Use Case:

Researchers, graduate students, and academic writers use this skill to turn a research topic or seed paper into a ranked literature table with source evidence, venue metrics, access links, and concise recommendation reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a working Google Scholar MCP server and may be blocked, rate-limited, or return incomplete records.

Mitigation: Fail closed when Scholar retrieval is unavailable and report the retrieval limitation instead of substituting another source or model memory.

Risk: External candidate metadata can appear in generated Markdown reports and may include unsafe or misleading raw HTML.

Mitigation: Review generated Markdown with raw HTML disabled or in a sanitized viewer, especially when metadata comes from untrusted sources.

Risk: Venue-quality matches can be missing or uncertain, which may affect ranking confidence.

Mitigation: Mark unmatched venues as unknown, keep relevance as the primary ranking signal, and require manual checks when relevance or metadata cannot be verified.

## Reference(s):

- [Search Workflow](references/search-workflow.md)
- [Quality Scoring](references/quality-scoring.md)
- [Venue Quality Data](data/README.md)
- [ClawHub Skill Page](https://clawhub.ai/figpad/skills/google-scholar-paper-finder)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown table by default, with optional enriched JSON and Markdown files from the scoring script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search queries used, source/tool status, candidate and dedupe counts, expansion terms, inclusion and exclusion notes, and limitations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
