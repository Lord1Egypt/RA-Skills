## Description: <br>
Google Drive Secure Management. Use when the user wants to list, search, read text content, create files with inline content, upload binaries, create folders, rename, move, share, or manage permissions on Google Drive files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to manage Google Drive files and folders through the PortEden CLI, including listing, searching, reading text content, creating files, uploading binaries, moving, sharing, and trashing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, upload, share, move, and trash files in a connected Google Drive account. <br>
Mitigation: Install it only if you trust Porteden with the connected account and use least-privilege Drive scopes where possible. <br>
Risk: Share, public-access, move, upload, and delete commands may expose or alter sensitive Drive content if run against the wrong file, recipient, role, or account profile. <br>
Mitigation: Before running those commands, verify the exact provider-prefixed file ID, recipient email or domain, permission role, and active account profile. <br>


## Reference(s): <br>
- [PortEden homepage](https://porteden.com) <br>
- [ClawHub skill page](https://clawhub.ai/porteden/google-drive-secured) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends PortEden compact JSON output with -jc and provider-prefixed Google Drive file IDs.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
