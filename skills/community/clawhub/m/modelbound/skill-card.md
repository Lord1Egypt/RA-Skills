## Description: <br>
ModelBound connects an agent to the hosted ModelBound MCP server to search and pull team skills, rules, prompts, and knowledge, and to propose reviewed edits to team-managed files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modelbound](https://clawhub.ai/user/modelbound) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team AI administrators use this skill to retrieve team-managed skills, rules, prompts, and knowledge from ModelBound and to propose reviewed edits back to team-managed skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted ModelBound integration exposes a broad administration surface for skills, rules, prompts, knowledge bases, agents, evals, exports, and deploys. <br>
Mitigation: Install only for trusted ModelBound workspaces and require explicit user confirmation before uploads, agent or eval runs, exports, deploys, draft proposals, or other write actions. <br>
Risk: A ModelBound API key may grant access beyond simple team-knowledge search. <br>
Mitigation: Use an appropriately scoped ModelBound API key and workspace scoping through MODELBOUND_TEAM_ID or gateway.setWorkspace where available. <br>
Risk: Fetched team-managed files or generated proposals can introduce incorrect or misleading guidance into local agent skills and rules. <br>
Mitigation: Review fetched content before relying on it and use skills.proposeDraft for edits so teammates can approve changes in ModelBound. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modelbound/modelbound) <br>
- [Publisher profile](https://clawhub.ai/user/modelbound) <br>
- [ModelBound MCP endpoint](https://mcp.modelbound.co) <br>
- [ModelBound API keys](https://modelbound.co/api-keys) <br>
- [ModelBound MCP tool index](reference/tools.md) <br>
- [ModelBound MCP recipes](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-RPC examples, fetched file content, and review URLs when edits are proposed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses hosted HTTPS JSON-RPC tools; write actions require explicit user confirmation before uploads, agent or eval runs, exports, deploys, or draft proposals.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
