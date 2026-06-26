## Description: <br>
Provides ready-to-run Python scripts and guidance for listing, reading, creating, updating, deleting, and sharing Google Drive files and folders through the Drive API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DVNghiem](https://clawhub.ai/user/DVNghiem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate Google Drive operations into scripts or workflows. It supports public Drive reads with an API key and service-account based CRUD automation for folders, files, uploads, downloads, metadata updates, deletion, and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable credentials allow the helper scripts to change, delete, or share Google Drive files. <br>
Mitigation: Use a dedicated service account with access only to intended folders and require explicit confirmation before public sharing, writer sharing, or permanent deletion. <br>
Risk: Google API keys or service account JSON files could expose Drive access if committed or stored with the skill. <br>
Mitigation: Keep credentials outside repositories, load them through environment variables, and store service account keys in a secret manager or similarly controlled location. <br>
Risk: Running scripts from an unexpected SKILL_SCRIPTS location could execute the wrong local files. <br>
Mitigation: Resolve and inspect SKILL_SCRIPTS before execution, especially before using write, share, or delete operations. <br>


## Reference(s): <br>
- [Google Drive API v3 documentation](https://developers.google.com/drive/api/v3/reference) <br>
- [Google API Python Client Drive v3 reference](https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html) <br>
- [Google service accounts guide](https://developers.google.com/identity/protocols/oauth2/service-account) <br>
- [Google Drive MIME types](https://developers.google.com/drive/api/guides/mime-types) <br>
- [MIME types reference](references/mime_types.md) <br>
- [Google Drive errors reference](references/error_codes.md) <br>
- [Service account template](assets/service_account_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell command examples, and optional JSON or table output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google Drive credentials through environment variables; write-capable scripts can modify Drive resources and local files when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
