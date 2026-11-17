## Description:

DingTalk MCP (dingtalk.com). Use this skill for ANY DingTalk MCP request — reading, creating, updating, and deleting data. Whenever a task involves DingTalk MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DingTalk users can use the OOMOL-connected DingTalk MCP account to discover available tools and perform DingTalk reads or changes through the oo CLI. The skill directs users to inspect each action's live schema and requires approval before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded CLI software without separate approval or integrity checks.

Mitigation: Review and approve CLI installation separately, using a reviewed, integrity-verified release.

Risk: CLI skill synchronization or a connection to the wrong DingTalk account may expose or change unintended data.

Mitigation: Disable automatic skill synchronization if unwanted, connect only the intended DingTalk account, and retain explicit approval requirements for changes.

## Reference(s):

- [DingTalk MCP ClawHub release](https://clawhub.ai/oomol/skills/oo-dingtalk-mcp)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [DingTalk](https://www.dingtalk.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration instructions, Operational guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; command responses are returned as JSON.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
