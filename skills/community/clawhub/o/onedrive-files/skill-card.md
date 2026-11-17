## Description:

Browse, search, download, and share OneDrive files, create folders, upload files, and manage file actions via Microsoft Graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to manage OneDrive and SharePoint files through an agent, including browsing, searching, downloading, uploading, creating folders, and managing sharing permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Microsoft account may expose broad OneDrive, SharePoint, and drive metadata access through the integration.

Mitigation: Review the Microsoft consent screen and connect the least-privileged account suitable for the task.

Risk: Uploads, deletions, permission changes, and sharing-link creation can alter or expose cloud files.

Mitigation: Require explicit user confirmation before executing write, destructive, permission, or sharing actions, including the target resource and intended effect.

Risk: The skill depends on ClawLink connection state and the live OneDrive tool catalog.

Mitigation: Verify the OneDrive connection and available tools before acting, and report real tool errors rather than assuming capability.

## Reference(s):

- [ClawHub OneDrive Files release page](https://clawhub.ai/hith3sh/skills/onedrive-files)
- [Microsoft Graph OneDrive API overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive)
- [Microsoft Graph DriveItem resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [SharePoint REST API overview](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OneDrive and SharePoint actions depend on the live ClawLink tool catalog and the connected Microsoft account permissions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
