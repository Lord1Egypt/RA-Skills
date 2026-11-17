## Description:

通过 Joplin Data API（Clipper Server）查询和管理笔记、笔记本、标签。支持本地直连和 SSH 远程两种模式。包含读写删全部操作，写/删需用户确认。触发词："查 Joplin"、"Joplin 笔记"、"joplin search"、"create note in joplin" 等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyangupday](https://clawhub.ai/user/yangyangupday)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking developers and agent users use this skill to search, inspect, create, update, and delete Joplin notes, notebooks, and tags through the Joplin Data API in local or SSH remote mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH remote mode may allow crafted note arguments to execute commands on the configured remote host.

Mitigation: Prefer local Joplin access; use SSH remote mode only with trusted, controlled hosts and after validating IDs and fields and avoiding shell interpolation of URLs and tokens.

Risk: Joplin API tokens are passed in request URLs and may appear in local, SSH, or proxy logs.

Mitigation: Protect the .env file with restrictive permissions, keep it out of version control, and avoid exposing token-bearing URLs in logs or shared terminals.

Risk: Create, update, and delete commands can modify or permanently remove notes.

Mitigation: Require explicit user confirmation for write and delete operations, preview the target note before deletion, and use soft delete unless permanent deletion is explicitly requested.

## Reference(s):

- [Joplin Data API Reference](https://joplinapp.org/help/api/references/restapi)
- [Artifact API Docs](artifact/references/api-docs.md)
- [ClawHub Skill Page](https://clawhub.ai/yangyangupday/skills/joplin-api-china)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text API output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JOPLIN_TOKEN and a running Joplin Clipper Server; optional SSH remote mode forwards note content and token over SSH.]

## Skill Version(s):

1.4.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
