## Description: <br>
Connects OpenClaw to Pieces through MCP so an agent can use Pieces as external long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackrosspieces](https://clawhub.ai/user/jackrosspieces) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a Pieces MCP endpoint, connect it through MCPorter and mcp-remote, retrieve long-term memory, and create durable memory summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw receives persistent read and write access to a Pieces long-term memory service. <br>
Mitigation: Install only when this access is intentional, and set explicit rules for what the agent may store or retrieve. <br>
Risk: The skill relies on a tunneled MCP endpoint for long-term memory access. <br>
Mitigation: Prefer a private or authenticated tunnel, verify the MCP endpoint before use, and review the MCPorter configuration before applying it. <br>
Risk: Gateway restart and configuration changes can expose the memory server to agent workflows before the user is ready. <br>
Mitigation: Restart the gateway only after reviewing the mcporter.json change and confirming the endpoint is correct. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackrosspieces/pieces-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, verification, usage, and troubleshooting guidance for a Pieces MCP long-term memory connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
