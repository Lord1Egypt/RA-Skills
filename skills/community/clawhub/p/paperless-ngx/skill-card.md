## Description: <br>
Interact with Paperless-ngx document management system via REST API. Use when users want to search, upload, download, organize documents, manage tags, correspondents, or document types in their Paperless-ngx instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OskarStark](https://clawhub.ai/user/OskarStark) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use this skill to manage documents in a Paperless-ngx instance through REST API requests, including search, upload, download, metadata updates, and organization resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change sensitive Paperless-ngx documents when configured with a powerful API token. <br>
Mitigation: Use a dedicated least-privilege API token and install the skill only for a Paperless-ngx instance the agent is intended to manage. <br>
Risk: Download, delete, bulk edit, and reprocess operations can expose sensitive files or make broad document changes. <br>
Mitigation: Manually confirm destructive, bulk, reprocess, and unnecessary download requests before allowing execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OskarStark/paperless-ngx) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN environment variables for Paperless-ngx API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
