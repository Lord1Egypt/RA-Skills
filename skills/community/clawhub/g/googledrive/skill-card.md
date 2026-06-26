## Description: <br>
Google Drive API integration with managed OAuth for listing, searching, creating, and managing Google Drive files and folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprinterx69](https://clawhub.ai/user/sprinterx69) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to interact with Google Drive through Maton-managed OAuth, including file discovery, metadata retrieval, uploads, exports, sharing, moves, copies, updates, and deletes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify Google Drive content through a third-party gateway with broad read, upload, share, update, move, and delete capability. <br>
Mitigation: Install only when Maton and the publisher are trusted with the connected Google Drive account, and limit use to the intended account or connection. <br>
Risk: Destructive or sensitive operations such as delete, move, update, upload, download, export, and sharing can affect user files. <br>
Mitigation: Require explicit user confirmation before executing those operations and verify the target file, folder, Google account, and Maton connection first. <br>
Risk: Sample connection identifiers or default connections may target the wrong Google Drive account when multiple connections exist. <br>
Mitigation: Do not reuse sample connection IDs; select and verify the exact Maton connection before making API calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sprinterx69/googledrive) <br>
- [Google Drive API Reference](https://developers.google.com/drive/api/reference/rest/v3) <br>
- [Google Drive Files: list](https://developers.google.com/drive/api/reference/rest/v3/files/list) <br>
- [Google Drive Files: create](https://developers.google.com/drive/api/reference/rest/v3/files/create) <br>
- [Google Drive Uploads](https://developers.google.com/drive/api/guides/manage-uploads) <br>
- [Google Drive Search Query Syntax](https://developers.google.com/drive/api/guides/search-files) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with Python, JavaScript, bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Maton Google Drive connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
