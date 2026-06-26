## Description: <br>
Access and manage Google Drive files, folders, metadata, uploads, downloads, and sharing through the Maton Gateway with OAuth-backed authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare cURL requests for connecting to Google Drive through the Maton Gateway and managing files, folders, uploads, downloads, metadata, and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provided commands can delete, overwrite, move, upload, or share real Google Drive files. <br>
Mitigation: Require explicit confirmation before file-changing operations and verify file IDs, folder IDs, upload paths, connection IDs, and recipient email addresses before execution. <br>
Risk: MATON_API_KEY can authorize access through Maton to connected Google Drive accounts and files. <br>
Mitigation: Keep MATON_API_KEY secret, avoid logging it, rotate it if exposed, and use the least-privileged Drive account or connection practical. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/otman-ai/googledrive-maton) <br>
- [Maton Google Drive Gateway Base URL](https://gateway.maton.ai/google-drive/{native-api-path}) <br>
- [Maton Connection Management Endpoint](https://ctrl.maton.ai/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guide with cURL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MATON_API_KEY and optional Maton-Connection headers; examples can operate on live Google Drive resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
