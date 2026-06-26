## Description: <br>
Manage documents in Paperless-ngx - search, upload, tag, and retrieve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madmantim](https://clawhub.ai/user/madmantim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, list, upload, download, and manage metadata in a Paperless-ngx document archive through the Paperless REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Paperless-ngx token can allow an agent to read documents, upload files, and create or modify archive metadata. <br>
Mitigation: Use a least-privilege Paperless account and review agent actions before running commands that change the archive. <br>
Risk: Connections to remote Paperless-ngx instances may expose sensitive document data or tokens if sent over insecure transport. <br>
Mitigation: Prefer HTTPS for remote Paperless-ngx instances and protect PAPERLESS_TOKEN as a secret. <br>
Risk: Downloads write document files to a local path chosen by the command. <br>
Mitigation: Pass a safe --output path when downloading and review the destination before execution. <br>
Risk: Advanced direct API operations can update, delete, or bulk-edit documents and metadata. <br>
Mitigation: Require explicit user approval before any advanced update, delete, or bulk operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/madmantim/paperless-ngx-tools) <br>
- [Paperless-ngx API Reference](artifact/references/api.md) <br>
- [Paperless-ngx project](https://github.com/paperless-ngx/paperless-ngx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Configuration] <br>
**Output Format:** [JSON responses from Node.js command-line scripts; downloaded documents are written as files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN; download output paths are user-controlled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
