## Description: <br>
Google Drive: Upload a file with automatic metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting Google Workspace users use this skill to prepare Google Drive upload commands for local files, including optional destination folder and target filename settings. It is intended for upload workflows that require explicit user confirmation before writing to Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs a Google Drive write action and may upload the wrong local file, destination, or filename if the command is not reviewed. <br>
Mitigation: Confirm the exact local file path, parent folder, and target filename with the user before running the upload command. <br>
Risk: Uploads may be sent through an unintended Google account or an untrusted gws CLI installation. <br>
Mitigation: Use a trusted gws installation and verify it is configured for the intended Google account before uploading. <br>


## Reference(s): <br>
- [Gws Drive Upload on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-drive-upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and user confirmation before upload.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
