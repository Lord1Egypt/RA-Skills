## Description: <br>
Operates the Message-in-a-Bottle LIFO callback stack so agents can register wake paths, create, forward, return, and resolve callbacks, inspect the ledger, and optionally pipe callback activity to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albzhu](https://clawhub.ai/user/albzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate delegated work across agents without polling by packaging continuation context in a local callback ledger. It also supports observing callback events and reaping stale callback envelopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Callback task names, results, and workflow details can be exposed if the Discord observer is enabled for sensitive work. <br>
Mitigation: Keep the observer disabled for sensitive workflows unless the destination channel is trusted and appropriate for those details. <br>
Risk: Local callback state under ~/.openclaw can contain continuation context and delegation results. <br>
Mitigation: Install and run the skill only in environments where local callback state is expected and access to that state is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albzhu/skills/miab-broker) <br>
- [Publisher profile](https://clawhub.ai/user/albzhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The callback CLI emits machine-readable JSON for mutating commands; observer output may be rendered as human-readable log messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
