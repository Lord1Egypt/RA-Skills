## Description: <br>
Access Google Drive from OpenClaw using either GOOGLE_SERVICE_ACCOUNT_KEY service-account JSON or a GOOGLE_OAUTH_REFRESH_TOKEN from the Google Drive OAuth connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-piplabs](https://clawhub.ai/user/jack-piplabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, list, inspect, download, export, upload, and create folders in Google Drive through a service account or OAuth-connected user account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use broad long-lived Google credentials for Drive access. <br>
Mitigation: Use a dedicated least-privileged Google account or service account and prefer a single intended authentication mode. <br>
Risk: Domain-wide delegation or OAuth-connected accounts may expose more Drive content than intended. <br>
Mitigation: Avoid domain-wide delegation unless required, and confirm the authenticated account, folder, and filename before uploads or folder creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-piplabs/google-drive-service-account) <br>
- [Google Drive API endpoint](https://www.googleapis.com/drive/v3) <br>
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON, text, files] <br>
**Output Format:** [Markdown guidance with bash examples; helper commands can return JSON, text, or downloaded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and openssl plus Google Drive credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
