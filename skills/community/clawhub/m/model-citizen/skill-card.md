## Description:

Model Citizen helps agents operate accountably with verifiable Ed25519 identity tied to a principal, scoped authority that only narrows, and signed receipts for permitted actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoess](https://clawhub.ai/user/aeoess)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Model Citizen to add accountable identity, scoped delegation, and auditable action receipts to agents using the Agent Passport System and optional MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run external npm packages and connect to a remote MCP service in an authority-delegation workflow.

Mitigation: Install only after reviewing and trusting the AEOESS package and service; prefer exact pinned versions or a reviewed lockfile.

Risk: Broad tokens or sensitive workspace data could be exposed while using the MCP service or optional registration workflows.

Mitigation: Run the skill in a least-privileged environment and avoid providing broad credentials or unnecessary sensitive data.

## Reference(s):

- [Model Citizen on ClawHub](https://clawhub.ai/aeoess/skills/model-citizen)
- [Agent Passport System npm package](https://www.npmjs.com/package/agent-passport-system)
- [Agent Passport System MCP npm package](https://www.npmjs.com/package/agent-passport-system-mcp)
- [Agent Passport System PyPI package](https://pypi.org/project/agent-passport-system/)
- [Remote MCP SSE endpoint](https://mcp.aeoess.com/sse)
- [Intent Network API](https://api.aeoess.com)
- [Agent Passport System GitHub repository](https://github.com/aeoess/agent-passport-system)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, package references, and remote service links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on npm packages, a remote MCP endpoint, and an optional GITHUB_TOKEN for public registration workflows.]

## Skill Version(s):

0.1.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
