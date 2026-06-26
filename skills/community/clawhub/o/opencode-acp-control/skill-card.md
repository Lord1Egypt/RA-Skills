## Description: <br>
Control OpenCode directly via the Agent Client Protocol (ACP). Start sessions, send prompts, resume conversations, and manage OpenCode updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjesuiter](https://clawhub.ai/user/bjesuiter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to control OpenCode through ACP, including starting sessions, sending prompts, reading responses, resuming conversations, and managing OpenCode updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to control a local OpenCode CLI with project file and terminal access. <br>
Mitigation: Install and use it only when the local OpenCode CLI is trusted and the working directory is intentionally selected. <br>
Risk: The update workflow can stop running OpenCode processes and includes a manual installer fallback using a remote shell script. <br>
Mitigation: Confirm exactly which OpenCode processes will be stopped, avoid unrelated sessions, and prefer a verified installer or release artifact before using remote install commands. <br>


## Reference(s): <br>
- [Agent Client Protocol docs for agents](https://agentclientprotocol.com/llms.txt) <br>
- [OpenCode ACP skill repository](https://github.com/bjesuiter/opencode-acp-skill) <br>
- [OpenCode releases](https://github.com/anomalyco/opencode/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON-RPC examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes polling, session tracking, resume, cancellation, and update guidance for OpenCode ACP workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
