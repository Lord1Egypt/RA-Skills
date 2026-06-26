## Description: <br>
Bootstrap OpenClaw with Hippocampus memory under a branded, repeatable setup: workspace, agent ID, API key or bootstrap token, and MCP wiring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cezexPL](https://clawhub.ai/user/cezexPL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a new OpenClaw instance or workspace to Hippocampus memory with stable workspace, agent identity, gateway, and authentication settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding flow involves package execution, gateway configuration, local configuration writes, and credentials. <br>
Mitigation: Verify the `hipokamp-mcp` package and gateway before setup, prefer scoped bootstrap tokens over long-lived API keys, and keep unrelated projects in separate Hippocampus workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cezexPL/hippocampus-openclaw-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only onboarding guidance; no generated files are emitted by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
