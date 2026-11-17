## Description: <br>
精英长记忆 is a long-term memory skill for AI agents that uses write-ahead logging and workspace memory files to preserve context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an AI agent to keep durable project context, decisions, preferences, and todos across sessions using local workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory files may retain sensitive project context, secrets, or regulated personal data across sessions. <br>
Mitigation: Define what may be stored before use, avoid entering secrets or regulated personal data, and periodically inspect or delete SESSION-STATE.md, MEMORY.md, and memory/ logs. <br>
Risk: The optional callback_url parameter could send data to an unintended or untrusted destination. <br>
Mitigation: Leave callback_url unset unless the endpoint and transmitted data are explicitly reviewed and trusted. <br>
Risk: The skill does not provide clear consent, retention, or deletion controls for automatically stored context. <br>
Mitigation: Use it only in workspaces where durable memory is desired and establish a manual retention and deletion process before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/longmemo-elite-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files and concise guidance with occasional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update SESSION-STATE.md, MEMORY.md, and memory/YYYY-MM-DD.md in the workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, created 2026-07-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
