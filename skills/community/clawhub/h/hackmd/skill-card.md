## Description: <br>
Work with HackMD documents by reading, creating, updating, deleting, and tracking changes across personal and team workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nulltea](https://clawhub.ai/user/nulltea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, editors, and content operators use this skill to manage HackMD notes and detect document changes from an agent workflow. It supports personal and team notes when the required HackMD CLI and API token are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete HackMD notes using the configured HackMD account. <br>
Mitigation: Supervise write and delete actions, verify note IDs and team paths before execution, and export important notes before deletion. <br>
Risk: The HackMD API token grants account access and may expose personal or team content if mishandled. <br>
Mitigation: Protect HMD_API_ACCESS_TOKEN, avoid logging or committing it, and install the skill only where that account access is acceptable. <br>
Risk: The local tracking state can contain note IDs, titles, timestamps, and related metadata. <br>
Mitigation: Treat ./.hackmd/tracked-notes.json as sensitive when note metadata is private and avoid committing it. <br>


## Reference(s): <br>
- [ClawHub HackMD skill page](https://clawhub.ai/nulltea/hackmd) <br>
- [HackMD API endpoint](https://api.hackmd.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; tracking commands can return JSON or note content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hackmd-cli and HMD_API_ACCESS_TOKEN; change tracking stores note metadata in ./.hackmd/tracked-notes.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
