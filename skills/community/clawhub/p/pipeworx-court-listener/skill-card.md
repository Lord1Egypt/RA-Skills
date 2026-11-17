## Description:

Search US court opinions and dockets by keyword, and retrieve specific CourtListener opinions by ID through the Pipeworx CourtListener MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal-research agents use this skill to configure a CourtListener MCP server, search US court opinions and dockets, and retrieve opinion text by CourtListener ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CourtListener searches, docket queries, and opinion IDs are sent to the third-party Pipeworx MCP gateway.

Mitigation: Install only when that trust boundary is acceptable for the intended legal-research workflow.

Risk: Case metadata or opinion text may be incomplete, stale, or unsuitable as the sole basis for important legal work.

Mitigation: Verify important results against CourtListener or another authoritative source before relying on them.

## Reference(s):

- [Pipeworx CourtListener MCP gateway](https://gateway.pipeworx.io/court-listener/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-court-listener)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses, plus JSON MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes CourtListener searches, docket queries, and opinion IDs through a third-party Pipeworx gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
