## Description: <br>
Control OpenCode directly via the Agent Client Protocol (ACP), including starting sessions, sending prompts, resuming conversations, and managing OpenCode updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[studio-hakke](https://clawhub.ai/user/studio-hakke) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to drive OpenCode in local project directories through ACP, including creating or resuming sessions, exchanging JSON-RPC messages, and checking or updating OpenCode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local OpenCode control in project directories. <br>
Mitigation: Use it only in intended directories, verify the local OpenCode installation, avoid sharing secrets, and require confirmation before file or terminal actions. <br>
Risk: The update workflow can stop running OpenCode processes and interrupt active work. <br>
Mitigation: Confirm before killing processes or triggering updates, and resume existing sessions only after the user selects the intended session. <br>


## Reference(s): <br>
- [Agent Client Protocol docs for agents](https://agentclientprotocol.com/llms.txt) <br>
- [Skill source repository](https://github.com/bjesuiter/opencode-acp-skill) <br>
- [Skill issue tracker](https://github.com/bjesuiter/opencode-acp-skill/issues) <br>
- [ClawHub skill page](https://clawhub.ai/studio-hakke/opencode-acp-control-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON-RPC examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes polling, session-resume, cancellation, and update workflows for OpenCode ACP control.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
