## Description:

Find an MCP server or agent skill for a tool or task, check its facts (official, can change data, needs credentials, licence, last activity) and install it with the user's permission, using the Kitbay directory (kitbay.app). Use when the user asks whether an MCP server or skill exists for a tool ("is there an MCP server for Figma?", "a skill for code review"), wants to connect their AI client to a tool or service, or asks how to install one; also when you need a tool you do not have.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northlarkhq](https://clawhub.ai/user/northlarkhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use Kitbay to find MCP servers or agent skills for a named tool or task, review sourced project facts, and obtain client-specific installation guidance when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to Kitbay and could reveal private project details.

Mitigation: Use generic search terms and omit confidential information.

Risk: Kitbay records sourced listing facts but does not audit the listed project's code.

Mitigation: Review the project's sources and code before installation; treat a benign scan verdict as limited evidence rather than a guarantee of safety.

## Reference(s):

- [Kitbay directory](https://kitbay.app)
- [Kitbay MCP endpoint](https://kitbay.app/mcp)
- [Source repository (server-resolved provenance)](https://github.com/northlarkhq/kitbay-mcp/tree/main/skills/kitbay)
- [AI client configuration reference](reference/clients.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown summaries with sourced listing facts and client-specific setup instructions; may include configuration snippets or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing facts include source URLs and checked dates where available; unknown details remain explicitly unknown.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
