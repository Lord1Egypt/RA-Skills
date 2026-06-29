## Description: <br>
Microsoft OneDrive provides API and CLI guidance for accessing OneDrive through Maton-managed OAuth and Microsoft Graph to manage files, folders, drives, and sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to produce OneDrive API requests, Maton CLI commands, and code examples for listing, uploading, downloading, organizing, and sharing files in a connected OneDrive account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OneDrive write operations can create, upload, rename, move, copy, or delete files and folders. <br>
Mitigation: Confirm the exact resource, destination, account or connection, and intended effect before any write operation. <br>
Risk: Sharing operations can expose files to unintended recipients or anyone with a link. <br>
Mitigation: Confirm recipients, permission level, and whether the link is organization-only or anonymous before creating or sending shares. <br>
Risk: Multiple OneDrive connections can cause requests to target the wrong account. <br>
Mitigation: Specify and verify the intended connection when more than one OneDrive connection exists. <br>


## Reference(s): <br>
- [ClawHub Microsoft OneDrive Skill](https://clawhub.ai/byungkyu/skills/one-drive) <br>
- [OneDrive Developer Documentation](https://learn.microsoft.com/en-us/onedrive/developer/) <br>
- [Microsoft Graph API Reference](https://learn.microsoft.com/en-us/graph/api/overview) <br>
- [DriveItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem) <br>
- [Drive Resource](https://learn.microsoft.com/en-us/graph/api/resources/drive) <br>
- [Sharing and Permissions](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/sharing) <br>
- [Large File Upload](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API routes, JSON examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an active OneDrive OAuth connection.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
