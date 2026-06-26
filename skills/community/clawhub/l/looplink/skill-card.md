## Description: <br>
Interact with looplink (looplink.app) - A social content organizer / bookmarking app <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sleep9](https://clawhub.ai/user/sleep9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to connect OpenClaw to Looplink, dynamically discover Looplink MCP tools, and organize or retrieve social bookmarking content through the Looplink service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets a live remote MCP manifest define which Looplink tools are callable. <br>
Mitigation: Inspect the current manifest before use and require clear user confirmation before enabling write, delete, publish, share, or account-changing actions. <br>
Risk: The skill uses a permanent agent apiKey that represents the agent's persistent identity. <br>
Mitigation: Store the apiKey securely, never log or expose it, and confirm there is a way to revoke or rotate it before linking important accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sleep9/looplink) <br>
- [Looplink MCP manifest](https://api.looplink.app/mcp/manifest) <br>
- [Looplink MCP tool execution endpoint](https://api.looplink.app/mcp/call) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Structured JSON responses from Looplink MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The available tools and schemas are defined by the live Looplink MCP manifest.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
