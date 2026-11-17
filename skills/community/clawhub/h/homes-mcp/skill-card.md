## Description:

Look up real-estate listings, property details, price and tax history, market reports, saved homes, and photo galleries on homes.com via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and real-estate researchers use this skill to ask an agent for homes.com listing search, property records, price and tax history, market reports, saved homes, saved searches, photo galleries, and local mortgage or affordability calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm MCP package.

Mitigation: Pin and review the exact homes-mcp package version before installation or deployment.

Risk: The skill depends on a separate Chrome extension that routes requests through a signed-in browser session.

Mitigation: Install the extension only after source review, and use a dedicated Chrome profile with only the homes.com session needed for this workflow.

Risk: Saved homes and saved searches may expose private account data to the MCP flow.

Mitigation: Treat saved homes and saved searches as private data and limit use to trusted agent sessions.

Risk: homes.com does not publish a public consumer API, so page structure changes or WAF challenges can interrupt extraction.

Mitigation: Treat extracted data as a lookup aid, handle failures explicitly, and verify important property information with authoritative sources before decisions.

## Reference(s):

- [homes-mcp package on npm](https://www.npmjs.com/package/homes-mcp)
- [homes-mcp project reference](https://github.com/chrischall/homes-mcp)
- [fetchproxy extension setup](https://github.com/chrischall/fetchproxy)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/homes-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses, Markdown summaries, JSON-style MCP configuration snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP lookup flow; results depend on homes.com page availability, fetchproxy connectivity, and an authenticated browser session for saved homes or saved searches.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
