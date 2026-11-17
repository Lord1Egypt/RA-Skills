## Description:

IMA Skills YC helps an agent manage a user's Tencent IMA notes through IMA OpenAPI, including note search, notebook browsing, content retrieval, note creation, and appending Markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laineyboy](https://clawhub.ai/user/laineyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Tencent IMA OpenAPI credentials use this skill to let an agent search, list, read, create, and append personal IMA notes. It is intended for personal note-management workflows where the user has authorized access to the target account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify private IMA notes after credentials are configured.

Mitigation: Install it only for accounts where that access is intended, and require explicit confirmation before reading full note content, creating a note, importing a file, or appending to an existing note.

Risk: The setup guidance includes persistent shell environment variables for API credentials.

Mitigation: Use a dedicated secrets mechanism where available, avoid committing credentials, and avoid placing API keys in broadly readable shell startup files.

Risk: Broad activation rules may treat ambiguous requests such as remembering or finding prior writing as note-access requests.

Mitigation: Clarify the user's intent and requested scope before making API calls, especially in shared or group contexts.

## Reference(s):

- [IMA Note API Reference](references/api.md)
- [IMA Homepage](https://ima.qq.com)
- [IMA OpenAPI Credential Setup](https://ima.qq.com/agent-interface)
- [ClawHub Skill Page](https://clawhub.ai/laineyboy/skills/ima)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY; outputs may include private note metadata or note content when authorized.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
