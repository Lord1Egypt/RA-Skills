## Description:

Use for Notion API integration, pages, blocks, databases or data sources, comments, views, file uploads, workspace search, OAuth connections, and safe preview-first read or mutation workflows through @pontx/notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Notion API operations through Pontx discovery and @pontx/notion. It supports safe preview-first reads and mutations, OAuth connections, webhook handling, workspace search, and page, block, database or data-source, comment, view, and file-upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notion tokens or workspace content could be exposed if an agent logs credentials, request bodies, or responses.

Mitigation: Use least-privilege Notion tokens, keep requests and responses in the caller-owned process, and avoid logging tokens or workspace content.

Risk: Irreversible Notion actions such as deletes or token revocations could be triggered without adequate review.

Mitigation: Preview the exact request, confirm the target ID and payload, and require explicit review before deletes, revocations, or other irreversible changes.

Risk: High-volume API use could hit Notion rate limits or overload responses.

Mitigation: Respect Retry-After headers, use exponential backoff with jitter, paginate with opaque cursors, and retry only idempotent operations where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-notion)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first API guidance with credential handling, rate-limit, retry, OAuth, webhook, and mutation-safety practices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
