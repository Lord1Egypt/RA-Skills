## Description:

Run spreadsheet-compatible Four-Square rental analysis for Paragon MLS deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

External real-estate investors, analysts, and agent operators use this skill to underwrite Paragon MLS rental-property deals, compare listings, and produce sheet-style deal analysis with cash flow, NOI, DSCR, ROI, ROE, and IRR outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP implementation is an external Node project referenced by absolute local path and is not included in the skill package.

Mitigation: Install only after auditing and pinning that external project, its lockfile, and its runtime permissions.

Risk: MLS data and underwriting inputs can include business-sensitive information and materially affect investment decisions.

Mitigation: Verify parsed MLS values, rents, expenses, and financing assumptions against authoritative records before relying on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/paragon-mls-analyze-deal)
- [Publisher profile](https://clawhub.ai/user/earlvanze)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown with a compact comparison table and JSON detail block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Node-based paragon-mls MCP server configured outside the skill package.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
