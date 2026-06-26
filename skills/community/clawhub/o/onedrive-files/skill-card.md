## Description: <br>
Browse, search, download, and share OneDrive files, create folders, upload files, and manage file actions via Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage files, folders, sharing links, permissions, and drive metadata in connected OneDrive and SharePoint accounts through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a Microsoft account through ClawLink and uses OAuth-backed access to OneDrive and SharePoint data. <br>
Mitigation: Review Microsoft consent scopes during connection and use a least-privileged or work account when possible. <br>
Risk: Write operations can create, move, update, share, or delete files and permissions. <br>
Mitigation: Confirm the exact target resource and intended effect before executing write or destructive actions. <br>
Risk: Sharing link creation can grant external access to files or folders. <br>
Mitigation: Confirm the recipient, link scope, and permission level before creating or updating sharing access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/onedrive-files) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>
- [Microsoft Graph OneDrive API Overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive) <br>
- [Microsoft Graph DriveItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem) <br>
- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration, JSON tool parameters] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions and ClawLink tool calls for Microsoft Graph-backed OneDrive and SharePoint actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
