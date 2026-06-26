## Description: <br>
Upload and categorize documents using the Paperless-ngx API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thistine](https://clawhub.ai/user/thistine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload documents into a Paperless-ngx instance and optionally assign titles, tags, and document types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive documents and a Paperless-ngx API key. <br>
Mitigation: Use it only with a Paperless-ngx server you control, avoid placing API keys in commands or logs, and confirm the exact file and destination before upload. <br>
Risk: The upload script disables TLS certificate verification. <br>
Mitigation: Prefer HTTPS with certificate verification enabled before using the script against any network-accessible Paperless-ngx server. <br>


## Reference(s): <br>
- [Paperless-ngx API Endpoints](references/api_endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload guidance and command-line script usage for a user-supplied Paperless-ngx host, API key, document path, title, tags, and document type.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
