## Description:

Complete Notion API integration with a Python CLI for search, page and database reads, page creation, property updates, block appends, soft deletes, auto-pagination, recursive block retrieval, and rate-limit retry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baixiaodev](https://clawhub.ai/user/baixiaodev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent work with shared Notion pages and databases through a guided CLI workflow. It supports discovery, inspection, planning, execution, and verification for read and write tasks in Notion workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Notion integration can read, create, update, append to, or archive content shared with its API key.

Mitigation: Keep the Notion API key secret, share only the specific pages or databases the agent should access, and review the agent's plan before create, update, append, or delete-block operations.

Risk: Bulk or write operations can unintentionally modify large amounts of workspace content.

Mitigation: Use the skill's discover, inspect, plan, execute, and verify workflow; batch writes conservatively and verify results after critical operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baixiaodev/skills/notion-pro)
- [Notion integrations](https://www.notion.so/profile/integrations)
- [Notion API documentation](https://developers.notion.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration API key and access only to pages or databases shared with that integration.]

## Skill Version(s):

1.0.1 (source: server evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
