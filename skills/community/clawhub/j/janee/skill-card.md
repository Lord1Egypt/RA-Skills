## Description: <br>
Secrets management for AI agents. Never expose your API keys again. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsdouglas](https://clawhub.ai/user/rsdouglas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Janee to give AI agents controlled access to API-backed services without exposing raw API keys to the agent. It is used to configure local secret storage, request policies, audit logs, and MCP or OpenClaw tool access for authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or misconfigured authenticated API access could allow an agent to perform unintended actions or send credentials to an unintended host. <br>
Mitigation: Use tightly scoped API keys, explicit allow rules, trusted service base URLs, and avoid write-capable or financial production credentials. <br>
Risk: Audit logs and local configuration can contain sensitive operational details. <br>
Mitigation: Treat ~/.janee/config.yaml and audit logs as sensitive files and restrict access to the local user. <br>
Risk: Auto-approval, sessions, and revoke controls are not strong standalone safety boundaries. <br>
Mitigation: Require explicit policies and review before installation, and do not rely on approval prompts or session controls as the only guardrail. <br>


## Reference(s): <br>
- [Janee on ClawHub](https://clawhub.ai/rsdouglas/janee) <br>
- [Janee GitHub Repository](https://github.com/rsdouglas/janee) <br>
- [Janee npm Package](https://www.npmjs.com/package/@true-and-useful/janee) <br>
- [Janee OpenClaw Plugin npm Package](https://www.npmjs.com/package/@true-and-useful/janee-openclaw) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [Path-Based Request Policies](docs/POLICIES.md) <br>
- [Changelog](docs/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration] <br>
**Output Format:** [MCP tool results, API responses, and Markdown guidance with shell commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests may include service, method, path, reason, and body parameters, with local audit logs written for activity review.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
