## Description: <br>
Auto-generated skill for mcp-server-chart tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send structured chart, spreadsheet, diagram, and map payloads to OneKey Gateway and receive generated outputs through a unified tool interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart, spreadsheet, diagram, and map inputs are sent to OneKey Gateway, an external service. <br>
Mitigation: Use the skill only for data appropriate to that service and review the provider's data-handling terms before submitting confidential, regulated, private address, or sensitive location data. <br>
Risk: The scripts include a shared demo-key fallback when no OneKey Gateway API key is set. <br>
Mitigation: Configure a scoped OneKey Gateway API key with DEEPNLP_ONEKEY_ROUTER_ACCESS for normal use instead of relying on the demo fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AI-Hub-Admin/mcp-server-chart) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, chart visualizations, diagram visualizations, spreadsheet outputs, map visualizations] <br>
**Output Format:** [JSON responses printed by command-line helper scripts after invoking OneKey Gateway tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inputs are JSON payloads supplied inline or from a file; an API key is required and the scripts include a shared demo-key fallback.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
