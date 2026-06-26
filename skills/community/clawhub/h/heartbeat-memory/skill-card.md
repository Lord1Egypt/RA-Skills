## Description: <br>
Saves OpenClaw session summaries into workspace memory files through heartbeat-triggered or manual runs, generating daily notes and periodically refining MEMORY.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justzerox](https://clawhub.ai/user/justzerox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and workspace maintainers use this skill to preserve session history as daily notes and long-term memory. It is intended for workspaces where automatic conversation summarization into local memory files is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation summaries may contain sensitive or regulated information because the skill saves session content into long-lived workspace memory files. <br>
Mitigation: Use the skill only in workspaces where persistent memory is intended, avoid sessions containing secrets or regulated data, and review ./memory/ and ./MEMORY.md regularly. <br>
Risk: Filesystem scanning for deleted sessions can preserve information that users may expect to be gone from active session listings. <br>
Mitigation: Disable or limit filesystem scanning when deleted-session retention is not desired, and document the workspace retention policy for users. <br>
Risk: Troubleshooting steps may delete configuration or HEARTBEAT.md files. <br>
Mitigation: Back up workspace memory and heartbeat configuration files before following deletion-based troubleshooting steps. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/justzerox/heartbeat-memory) <br>
- [Configuration reference](references/config.md) <br>
- [API reference](references/api.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, JSON configuration, shell command snippets, and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workspace-relative memory artifacts such as ./memory/daily/YYYY-MM-DD.md, ./MEMORY.md, ./memory/heartbeat-state.json, ./memory/heartbeat-memory-config.json, and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
0.0.7 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
