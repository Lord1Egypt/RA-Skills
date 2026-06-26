## Description: <br>
小龙虾备忘录 records quick ideas and local notes so an AI assistant can better support creative work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwbwbw](https://clawhub.ai/user/lwbwbw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assisted creators use this skill to run a lightweight local memo service for capturing ideas, tasks, tags, and context across sessions through a web UI, CLI, and simple HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memo service can expose private notes and deletion controls if reachable without authentication. <br>
Mitigation: Keep the service bound to localhost or behind strong access controls, and avoid storing sensitive notes until authentication is added. <br>
Risk: Optional nginx setup uses sudo commands and can change host web server routing. <br>
Mitigation: Review the nginx commands before applying them and confirm the target server configuration. <br>
Risk: Local memo data is stored in scripts/memos.db and could be lost or overwritten. <br>
Mitigation: Back up scripts/memos.db before relying on the service for important notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lwbwbw/idea-memos) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Node.js and SQLite memo service with web, CLI, and HTTP API access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
