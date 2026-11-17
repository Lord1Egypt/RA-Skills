## Description:

MiniMax MCP tools - Web search and image understanding via MiniMax Coding Plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call MiniMax Coding Plan MCP tools for current web search and image understanding when a MiniMax API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports risky installation and runtime patterns that can execute third-party code locally.

Mitigation: Review the skill before installing, trust the MiniMax and uv sources, and pin or review the minimax-coding-plan-mcp package before allowing it to run.

Risk: The wrapper loads variables from ~/.openclaw/.env, which may expose unrelated secrets if that file contains more than the MiniMax configuration.

Mitigation: Keep only required MiniMax variables in ~/.openclaw/.env, avoid unrelated secrets there, and set restrictive file permissions.

## Reference(s):

- [MiniMax Platform](https://platform.minimaxi.com)
- [MiniMax API Host](https://api.minimaxi.com)
- [ClawHub Skill Page](https://clawhub.ai/russellfei/skills/minimax-mcp-call)
- [Publisher Profile](https://clawhub.ai/user/russellfei)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text and JSON responses from MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY, Node.js 18+, uv, and the minimax-coding-plan-mcp package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
