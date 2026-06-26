## Description: <br>
Read Apple Messages data with imsgctl: check access, list chats, inspect message history, filter by time, include attachment metadata, and watch new activity from the local data available to imsgctl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpreagan](https://clawhub.ai/user/jpreagan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local Apple Messages chats, message history, attachment metadata, and live activity with imsgctl when the user has authorized access to the local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private Apple Messages chats and attachment metadata from the local machine or an imsgkit replica. <br>
Mitigation: Install and use it only when message inspection is intended; prefer specific chat IDs, small limits, and time windows. <br>
Risk: Direct access to the macOS Messages database may require broad local file permissions. <br>
Mitigation: Grant Full Disk Access only when necessary, avoid attachment access unless needed, and stop watch mode when live monitoring is no longer needed. <br>


## Reference(s): <br>
- [imsgkit project homepage](https://github.com/jpreagan/imsgkit) <br>
- [ClawHub skill page](https://clawhub.ai/jpreagan/imsgctl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or JSONL command-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers read-only imsgctl commands with JSON output, scoped chat IDs, limits, and time windows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
