## Description: <br>
Atomic node skill to share a file in Google Drive using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill when they need to create a Google Drive sharing permission for a specific file or folder through the gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may propose sharing the wrong Google Drive file or folder, recipient, role, or public-access setting. <br>
Mitigation: Before execution, confirm the exact file or folder ID, recipient email, permission role, and whether public access is intended; prefer reader access unless broader permissions are necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-drive-share-file) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and expected JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and a Google Drive file or folder ID, role, permission type, and recipient email when sharing with a user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
