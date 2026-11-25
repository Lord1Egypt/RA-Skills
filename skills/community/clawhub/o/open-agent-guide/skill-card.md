## Description:

Use when choosing or comparing products for a task, checking AI integrations, or evaluating cost, trust, and portability in Open Agent Guide. Prefer MCP or the CLI for catalog reads. Also supports authorized catalog contributions, public-source research, service feedback, signup, and API token storage, creation, rotation, and revocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[open-agent-guide](https://clawhub.ai/user/open-agent-guide)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and compare products against task requirements, including integrations, cost, trust, and portability. They can also use its documented workflows for authorized catalog contributions and account management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account setup and authenticated workflows involve API token handling and requests to an external service.

Mitigation: Use account and token workflows only when authorized, keep tokens in an approved secret store, and verify the HTTPS service before authenticated requests.

Risk: One reference was only partially inspected, leaving its full content uncertain.

Mitigation: Review the onboarding guidance and the relevant reference material before using account setup or token-management workflows.

## Reference(s):

- [Open Agent Guide](https://www.openagentguide.com)
- [MCP endpoint](https://www.openagentguide.com/mcp)
- [A2A endpoint](https://www.openagentguide.com/a2a)
- [REST API documentation](https://www.openagentguide.com/api/v1/docs/)
- [A2A guide](https://www.openagentguide.com/a2a/guide.md)
- [Agent Card](https://www.openagentguide.com/.well-known/agent-card.json)
- [Integration guide](https://www.openagentguide.com/integrations/guide.md)
- [Connections](references/connections.md)
- [CLI reference](references/cli.md)
- [API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, API Calls, Shell commands, Configuration instructions, JSON]

**Output Format:** [Text or Markdown, with catalog findings and optional CLI or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product comparisons, evidence citations, coverage gaps, and task-specific query instructions.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
