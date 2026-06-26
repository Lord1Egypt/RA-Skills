## Description: <br>
OneDrive API integration with managed OAuth via Microsoft Graph for managing files, folders, drives, and sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to a OneDrive account through Maton-managed OAuth and perform file, folder, drive, and sharing operations through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and a OneDrive OAuth connection, which can expose sensitive credentials and account access if used in an untrusted environment. <br>
Mitigation: Install only when Maton is trusted to handle the API key, OAuth connection, and OneDrive traffic; keep MATON_API_KEY scoped to trusted execution environments. <br>
Risk: Write operations can create, upload, rename, move, copy, or delete OneDrive content. <br>
Mitigation: Confirm the target account, connection ID, file or folder, and intended effect before approving create, update, upload, move, copy, or delete actions. <br>
Risk: Sharing operations can create anonymous or edit-capable links that broaden access to files. <br>
Mitigation: Approve sharing only after checking the exact file, recipient or link scope, and permission level; prefer least-privilege read or organization-scoped access when appropriate. <br>
Risk: OneDrive download URLs returned by Microsoft Graph may be pre-authenticated and temporary. <br>
Mitigation: Avoid logging or redistributing download URLs, and treat them as sensitive while valid. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/one-drive) <br>
- [OneDrive Developer Documentation](https://learn.microsoft.com/en-us/onedrive/developer/) <br>
- [Microsoft Graph API Reference](https://learn.microsoft.com/en-us/graph/api/overview) <br>
- [DriveItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem) <br>
- [Drive Resource](https://learn.microsoft.com/en-us/graph/api/resources/drive) <br>
- [Sharing and Permissions](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/sharing) <br>
- [Large File Upload](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active OneDrive OAuth connection.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
