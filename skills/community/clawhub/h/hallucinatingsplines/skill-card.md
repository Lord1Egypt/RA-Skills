## Description: <br>
Build and manage cities autonomously on Hallucinating Splines, a headless Micropolis simulator with a REST API and MCP server for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewedunn](https://clawhub.ai/user/andrewedunn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to create, monitor, and operate Hallucinating Splines cities through the service API or MCP server. It supports autonomous city-building loops, heartbeat checks, budgeting, map analysis, and game-state actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HS_API_KEY grants access to manage Hallucinating Splines cities for the associated account. <br>
Mitigation: Store HS_API_KEY as a secret, avoid placing it in prompts or committed files, and revoke or rotate it if exposed. <br>
Risk: API examples and MCP tools can mutate remote game state by creating cities, placing buildings, changing budgets, advancing time, or retiring cities. <br>
Mitigation: Run actions only against intended cities, review city IDs and action payloads before execution, and use conservative spending reserves for autonomous loops. <br>
Risk: Autonomous or heartbeat loops can continue unattended game actions. <br>
Mitigation: Use autonomous loops only when unattended play is acceptable, set clear intervals and stop conditions, and monitor funds, inactivity, and population stalls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andrewedunn/hallucinatingsplines) <br>
- [Hallucinating Splines homepage](https://hallucinatingsplines.com) <br>
- [Hallucinating Splines API](https://api.hallucinatingsplines.com/v1) <br>
- [Hallucinating Splines MCP server](https://mcp.hallucinatingsplines.com/mcp) <br>
- [Interactive API reference](https://api.hallucinatingsplines.com/reference) <br>
- [Hallucinating Splines documentation](https://hallucinatingsplines.com/docs) <br>
- [Skill source document](https://hallucinatingsplines.com/skill.md) <br>
- [Heartbeat document](https://hallucinatingsplines.com/heartbeat.md) <br>
- [MicropolisJS reference](https://github.com/graememcc/micropolisJS) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown instructions with curl commands, API examples, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HS_API_KEY; examples call the Hallucinating Splines REST API or MCP server and can change remote game state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
