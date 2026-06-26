## Description: <br>
Memory Maintenance 2.0.0 helps an agent maintain persistent task memories, execute user tasks, report progress, retry failures, and manage background sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucklylin](https://clawhub.ai/user/lucklylin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain persistent memory files, coordinate task execution through sessions, track progress, and record failures or retries. It is intended for workspace automation where task logs, memory updates, and scheduled cleanup are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent storage of task context and memory content, which could capture API keys, secrets, or sensitive user data. <br>
Mitigation: Use only in workspaces where persistent memory files are acceptable, and prevent secrets from being written to MEMORY.md, daily memory files, or failure logs. <br>
Risk: The skill has broad session and cleanup authority, including background session management and scheduled maintenance behavior. <br>
Mitigation: Review session spawning, termination, scheduled cleanup, and background maintenance behavior before installation, and verify that session termination controls are available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucklylin/memory-maintenance-2-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with code snippets, progress reports, memory entries, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent memory entries, daily memory files, and failure logs in the workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
