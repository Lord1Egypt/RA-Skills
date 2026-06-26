## Description: <br>
A local password manager for storing, searching, updating, deleting, importing, and exporting account passwords with Fernet encryption when cryptography is installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyieleven11](https://clawhub.ai/user/wangyieleven11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage account credentials in a local OpenClaw workspace, including lookup, update, tagging, CSV import, and CSV export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passwords may be stored in plaintext if the cryptography dependency is unavailable. <br>
Mitigation: Verify cryptography is installed before saving credentials and inspect existing local password data before relying on encryption. <br>
Risk: CSV export creates plaintext credential dumps. <br>
Mitigation: Require explicit confirmation before export, store exports only temporarily, and delete exported files immediately after use. <br>
Risk: Service-wide or bulk deletion can remove many credential records. <br>
Mitigation: Require explicit confirmation before service-wide or bulk delete actions and keep a backup process appropriate for the user's environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangyieleven11/local-passwords-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write encrypted password data, local key material, and plaintext CSV exports in the user's local filesystem.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
