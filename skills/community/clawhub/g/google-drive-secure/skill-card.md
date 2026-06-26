## Description: <br>
Google Drive Secure Management helps agents list, search, read text content, create files, upload binaries, create folders, rename, move, copy, share, and manage permissions on Google Drive files through PortEden. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to manage Google Drive files and folders through PortEden commands, including listing, reading, creating, uploading, moving, copying, sharing, permission review, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on Google Drive content available to the active PortEden token. <br>
Mitigation: Use the narrowest available Drive access and review accessInfo in command output before taking action. <br>
Risk: Sharing, permission changes, and deletion can expose or remove Drive content. <br>
Mitigation: Require explicit user confirmation before sharing files, changing permissions, or deleting files. <br>
Risk: Credentials may be provided through PE_API_KEY or stored in the system keyring after login. <br>
Mitigation: Protect PortEden credentials as sensitive secrets and avoid exposing them in prompts, logs, or command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/porteden/google-drive-secure) <br>
- [PortEden homepage](https://porteden.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PortEden CLI commands and the -jc JSON compact output mode for agent-friendly Drive results.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
