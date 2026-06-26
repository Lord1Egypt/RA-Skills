## Description: <br>
Manage documents in Paperless-ngx - search, upload, tag, and retrieve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madmantim](https://clawhub.ai/user/madmantim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search, retrieve, upload, download, and manage Paperless-ngx documents and metadata from an agent using a configured Paperless API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured token gives the agent access to the same Paperless-ngx account and documents as that token. <br>
Mitigation: Use a limited Paperless account or token whenever possible. <br>
Risk: Uploads, metadata creation, bulk edits, and deletes can change Paperless-ngx data. <br>
Mitigation: Confirm document-changing actions and command arguments before running them. <br>
Risk: Downloaded documents can be written to local paths selected by the command. <br>
Mitigation: Choose explicit safe output paths for downloads. <br>


## Reference(s): <br>
- [Paperless-ngx API Reference](references/api.md) <br>
- [Paperless-ngx project](https://github.com/paperless-ngx/paperless-ngx) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [JSON responses and shell command guidance; downloads may write document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN. Download output paths should be chosen explicitly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
