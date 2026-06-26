## Description: <br>
Control OpenCode directly via the Agent Client Protocol (ACP). Start sessions, send prompts, resume conversations, and manage OpenCode updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berriosb](https://clawhub.ai/user/berriosb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate OpenCode through ACP: starting sessions, sending prompts, resuming prior conversations, and checking or triggering OpenCode updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update workflow may inspect local processes and stop OpenCode sessions too broadly. <br>
Mitigation: List exact OpenCode process IDs and ask for user confirmation before terminating any session. <br>
Risk: The manual update fallback recommends running a remote shell installer. <br>
Mitigation: Inspect the installer before running it, or install OpenCode through a package manager the user already trusts. <br>


## Reference(s): <br>
- [Agent Client Protocol Docs for Agents](https://agentclientprotocol.com/llms.txt) <br>
- [Opencode Acp Control Repository](https://github.com/berriosb/Opencode-Acp-Control) <br>
- [OpenCode Latest Releases](https://github.com/anomalyco/opencode/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON-RPC examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes polling, session-resume, and update-check workflows.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
