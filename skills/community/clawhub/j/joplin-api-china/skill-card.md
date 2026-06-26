## Description: <br>
通过 Joplin Data API（Clipper Server）查询和管理笔记、笔记本、标签。支持本地直连和 SSH 远程两种模式。包含读写删全部操作，写/删需用户确认。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyangupday](https://clawhub.ai/user/yangyangupday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query, preview, create, update, and delete Joplin notes, notebooks, and tags through the Joplin Data API. It supports local Clipper Server access and optional SSH remote mode for users who keep Joplin on another host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Joplin note content and perform read, write, and delete operations. <br>
Mitigation: Install only where this access is intended, preview notes before modifying them, and require clear user confirmation for changes or deletions. <br>
Risk: The Joplin API token is required for every API call and may appear in local configuration or request URLs. <br>
Mitigation: Keep the token file private, restrict `.env` permissions, exclude it from version control, and rotate the token if exposure is suspected. <br>
Risk: SSH remote mode sends note content and the API token over the configured remote connection. <br>
Mitigation: Prefer local mode when possible and disclose the target SSH host before any write or delete operation in remote mode. <br>
Risk: Permanent deletion is not recoverable through Joplin trash. <br>
Mitigation: Use soft delete by default and require explicit confirmation before permanent deletion. <br>


## Reference(s): <br>
- [Joplin Data API reference](https://joplinapp.org/help/api/references/restapi) <br>
- [Bundled API docs](artifact/references/api-docs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, note previews, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Joplin API token and may operate through local or SSH remote Joplin access.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
