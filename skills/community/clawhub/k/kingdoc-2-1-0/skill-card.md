## Description:

KingDoc lets an agent create, edit, manage, search, convert, upload, share, and recover Kingsoft online documents across documents, spreadsheets, presentations, multidimensional tables, forms, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxy0204](https://clawhub.ai/user/zhangxy0204)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and workspace operators use this skill to let an agent perform Kingsoft document lifecycle tasks, including document creation, content editing, file management, permissions, version history, recycle-bin recovery, conversion, text extraction, notifications, and multidimensional-table workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful KingDoc document access and the security evidence says implemented safeguards may not match the safety promises.

Mitigation: Review the skill carefully before installation, test it in a non-sensitive workspace, and use a dedicated low-privilege KingDoc app.

Risk: App Secret exposure could allow unauthorized document API access.

Mitigation: Keep config.json out of shared locations and rotate the App Secret if the configuration is exposed.

Risk: Uploads, sharing, version rollback, batch changes, and deletion-like actions can materially change or expose user and team documents.

Mitigation: Require manual confirmation outside the skill before those operations and avoid granting access to sensitive team documents.

## Reference(s):

- [Kingsoft Open Platform](https://developer.kdocs.cn)
- [Authentication Reference](artifact/references/auth.md)
- [Workflow Reference](artifact/references/workflows.md)
- [Security Design Reference](artifact/references/security.md)
- [Multidimensional Table Reference](artifact/references/dbt_references.md)
- [Error Code Reference](artifact/references/error_codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, API-call guidance, and generated document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Kingsoft Open Platform App ID and App Secret; document operations depend on network access and granted Kingsoft scopes.]

## Skill Version(s):

2.1.0 (source: artifact frontmatter; release version 1.0.0 in evidence.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
