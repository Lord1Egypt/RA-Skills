## Description:

JustFix helps an agent quote UK trades jobs by calling the JustFix Estimator MCP server to return a scope summary, cost breakdown, and booking link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adam-graham](https://clawhub.ai/user/adam-graham)

### License/Terms of Use:

MIT

## Use Case:

External UK users can ask an agent for home-services pricing, and developers can embed the skill in agent harnesses to surface JustFix estimates and booking links for trades work.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill can send household repair details to a commercial MCP service when triggered by quote or booking requests.

Mitigation: Configure the agent to ask before sending repair details to JustFix unless the user clearly requested a quote or booking link.

Risk: One Codex CLI install path uses an unpinned npm proxy for the MCP connection.

Mitigation: Prefer a pinned reviewed mcp-remote version or a locked local install before deployment.

Risk: The skill returns estimates only and cannot guarantee actual labour time, availability, materials, payment, or completed booking.

Mitigation: Present the scope caveat and send users to the JustFix booking page to confirm details before committing.

## Reference(s):

- [JustFix skill repository](https://github.com/Just-Fix/justfix-skill)
- [JustFix homepage](https://justfix.app)
- [JustFix Estimator MCP endpoint](https://estimator-mcp.justfix.app/mcp)
- [JustFix support policy](https://www.justfix.app/support-policy)
- [ClawHub skill page](https://clawhub.ai/adam-graham/skills/justfix)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text quote card with cost breakdown, scope summary, caveat, and booking URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls public MCP tools for service lists, call-out fees, and estimate cards; booking completion happens on the JustFix website.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
