## Description:

Access U.S. Congress data to search bills, retrieve bill details, get current members, and view recent congressional votes via the GovTrack API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query U.S. Congress data through a Pipeworx-hosted MCP endpoint for bill search, bill details, current members, and recent votes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Congress-related MCP queries are routed through the Pipeworx gateway.

Mitigation: Install only if that routing is acceptable, and avoid including confidential context in requests.

Risk: Returned legislative information may be incomplete, delayed, or unsuitable as the sole source for important decisions.

Mitigation: Cross-check important bill, member, and vote information against an authoritative congressional source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-congress)
- [Pipeworx Congress MCP Gateway](https://gateway.pipeworx.io/congress/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Congress data such as bill summaries, bill details, member records, and recent vote information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
