## Description:

Pull team skills, rules, and knowledge from the ModelBound hosted MCP server when users need to sync team context, search team knowledge, or propose edits to team-managed agent files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modelbound](https://clawhub.ai/user/modelbound)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to connect an agent to ModelBound-hosted team context, including skills, rules, prompts, and knowledge bases. It supports fetching managed files, answering questions from team knowledge with citations, and proposing reviewed edits to team-managed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote skill text can be copied into an active local agent skill directory without enough review controls.

Mitigation: Review, diff, and scan fetched SKILL.md content before placing it under an agent skill directory.

Risk: Broad ModelBound tool access can route through modelbound.callTool, including write-capable actions.

Mitigation: Require explicit user confirmation for agent runs, uploads, evals, exports, deploys, and any other write action.

Risk: A wrong or untrusted endpoint could expose credentials or return untrusted workspace content.

Mitigation: Keep MODELBOUND_ENDPOINT on the official service or another endpoint the user controls, and protect MODELBOUND_API_KEY.

## Reference(s):

- [ModelBound ClawHub Skill Page](https://clawhub.ai/modelbound/skills/modelbound)
- [ModelBound ClawDIS Homepage](https://clawhub.ai/modelbound/modelbound)
- [ModelBound MCP Endpoint](https://mcp.modelbound.co)
- [ModelBound MCP Tool Index](reference/tools.md)
- [ModelBound MCP Recipes](reference/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples and file-writing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ModelBound citations, fetched skill text, proposed draft review URLs, and local skill files.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
