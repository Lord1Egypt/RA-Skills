## Description: <br>
Connects to remote ConnectOnion agents so users can delegate tasks by agent address and handle one-shot or multi-turn responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openonion](https://clawhub.ai/user/openonion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use oo to connect a local agent identity to a trusted remote ConnectOnion agent, send a task by address, and relay responses or follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install ConnectOnion and create a persistent local agent identity. <br>
Mitigation: Review and approve installation and identity-creation steps before running them. <br>
Risk: Remote delegation can send task text or local context to another agent. <br>
Mitigation: Use only trusted ConnectOnion agent addresses and avoid sending secrets or private file contents. <br>
Risk: The artifact does not define a clear confirmation step before every remote connection. <br>
Mitigation: Prefer explicit user confirmation before connecting to a remote agent or sending task content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openonion/oo) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python code; remote agent responses are returned as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parses CO_* marker lines from command output and may continue multi-turn exchanges until completion or a 10-round limit.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
