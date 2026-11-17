## Description:

BT Panel MCP (bt.cn). Use this skill for ANY BT Panel MCP request — reading, creating, updating, and deleting data. Whenever a task involves BT Panel MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to work with BT Panel through the connected MCP account, including reading, creating, updating, and deleting data. It guides action discovery, schema checks, and execution while requiring confirmation for state-changing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run an online installer whose source and live connector implementation have not been verified, without a separate approval step.

Mitigation: Review and approve CLI installation separately using a pinned, independently verified source, and check whether installation adds or updates other agent skills.

Risk: Connected BT Panel actions can change server state, and the account may have broad permissions.

Mitigation: Limit the connected account's permissions and confirm each server-changing operation.

## Reference(s):

- [BT Panel MCP API documentation](https://docs.bt.cn/ai-ops/mcp/)
- [BT Panel](https://www.bt.cn/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, API calls]

**Output Format:** [Markdown instructions with shell commands and JSON payloads; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive operations require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
