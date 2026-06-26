## Description: <br>
Model Citizen helps agents operate accountably with verifiable Ed25519 identity, scoped authority delegation, and signed receipts for permitted actions using the Agent Passport System. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoess](https://clawhub.ai/user/aeoess) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents accountable identity, narrowing delegated authority, and auditable receipts across sessions, handoffs, and other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AEOESS-hosted MCP and API services for agent identity and receipts. <br>
Mitigation: Deploy only where use of those remote services is acceptable for the agent workflow and data involved. <br>
Risk: Generated passport keys can function as sensitive agent identity material. <br>
Mitigation: Store and handle passport keys as credentials, and rotate or revoke delegated authority when access should end. <br>
Risk: The optional GitHub token can broaden impact if over-scoped or unnecessary. <br>
Mitigation: Avoid providing GITHUB_TOKEN unless the public-registration workflow is needed, and use the narrowest available scopes. <br>


## Reference(s): <br>
- [Model Citizen on ClawHub](https://clawhub.ai/aeoess/model-citizen) <br>
- [Agent Passport System npm package](https://www.npmjs.com/package/agent-passport-system) <br>
- [Agent Passport System MCP npm package](https://www.npmjs.com/package/agent-passport-system-mcp) <br>
- [Agent Passport System PyPI package](https://pypi.org/project/agent-passport-system/) <br>
- [Remote MCP endpoint](https://mcp.aeoess.com/sse) <br>
- [Agent Passport System GitHub project](https://github.com/aeoess/agent-passport-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference remote MCP and API services, local npm packages, Ed25519 key material, delegated authority scopes, signed receipts, and an optional GitHub token for public registration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
