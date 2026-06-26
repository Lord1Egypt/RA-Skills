## Description: <br>
Entry point for Mobazha skills. Provides an overview of available skills and guides the AI agent to load the right one based on user intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this index skill to identify and load the appropriate Mobazha companion skill for deployment, setup, store operations, marketing, or MCP connection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Companion Mobazha skills may involve shell commands, MCP connections, or store credentials. <br>
Mitigation: Review each companion skill separately and require explicit approval before running commands, connecting MCP tools, or providing credentials. <br>
Risk: Users may treat this index skill as sufficient review for the broader Mobazha skill collection. <br>
Mitigation: Treat this skill as routing guidance only; evaluate referenced companion skills before deployment or store access. <br>


## Reference(s): <br>
- [Mobazha Website](https://mobazha.org) <br>
- [Mobazha Self-Host Guide](https://mobazha.org/self-host) <br>
- [Mobazha Download Page](https://mobazha.org/download) <br>
- [Mobazha SaaS Platform](https://app.mobazha.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Index-only; does not execute commands or access credentials by itself.] <br>

## Skill Version(s): <br>
0.3.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
