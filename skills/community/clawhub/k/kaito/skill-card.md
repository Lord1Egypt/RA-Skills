## Description:

Tracks mindshare trends for crypto tokens, projects, and Kaito narratives using Kaito MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yh9277](https://clawhub.ai/user/yh9277)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and workflow agents use this skill to retrieve and summarize Kaito mindshare data for tokens, projects, and narratives. It supports standalone social trend checks and composition into broader strategy, investigation, or social-listening workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external Kaito MCP data, so results may reflect source availability, coverage, or freshness limits.

Mitigation: Confirm access to the required Kaito MCP tools before installation and treat mindshare outputs as data-source-dependent analysis.

Risk: Incorrect or mismatched narrative IDs can silently return empty results.

Mitigation: Use the documented case-sensitive narrative IDs and verify ambiguous narratives before relying on the output.

Risk: Ticker-only lookups can produce all-zero data when Kaito indexes an entity by full project name.

Mitigation: Retry with the full project name when ticker results are all zero, then present historical context alongside current values.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured data summaries with trend values, historical context, rank interpretation, and movement classification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standalone use returns a readable mindshare summary; workflow use may return structured data for integration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
