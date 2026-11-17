## Description:

Operate Postqued through its remote MCP server or v2 REST API for social content uploads, multi-platform publishing and scheduling, calendar status, analytics, engagement, approval workflows, revisions, caption suggestions, client reviews, collaborators, connected accounts, workspaces, and billing capability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syeddhasnainn](https://clawhub.ai/user/syeddhasnainn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media operators use this skill to let an agent inspect Postqued workspaces, upload media, validate social platform constraints, schedule or publish content, review analytics and engagement, and coordinate approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, schedule, delete, disconnect accounts, change collaborators, and post comments through Postqued-connected social accounts.

Mitigation: Use dry-run validation, verify the selected workspace and connected account, and require explicit user review before externally visible or destructive actions.

Risk: A broad or misplaced API key could expose more Postqued workspace access than intended.

Mitigation: Use the least-privileged API key available, keep it out of logs and query parameters, and resolve the exact organization and workspace before each scoped operation.

Risk: Publishing retries after timeouts can duplicate or conflict with live social posting requests.

Mitigation: Use one fresh UUID idempotency key for each distinct live publish request and check durable publish status before retrying.

Risk: Approval, revision, and collaborator workflows can overwrite current work or affect other reviewers if stale state is used.

Mitigation: Read current state before mutations and preserve expected revision, version, role, and reviewer values when applying changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/syeddhasnainn/skills/postqued-api)
- [Postqued OpenClaw Setup](https://postqued.com/openclaw)
- [Postqued MCP Server](https://mcp.postqued.com/mcp)
- [Postqued v2 OpenAPI](https://api.postqued.com/v2/docs/openapi.json)
- [Postqued v2 REST API reference](references/api.md)
- [Postqued MCP tool catalog](references/mcp-tools.md)
- [Postqued publishing targets](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-oriented tool inputs, REST examples, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API calls or MCP tool plans that require a Postqued API key, explicit workspace selection, dry-run validation, and user confirmation before externally visible or destructive actions.]

## Skill Version(s):

1.0.7 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
