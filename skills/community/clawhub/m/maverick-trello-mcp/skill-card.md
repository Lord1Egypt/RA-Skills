## Description:

Work with Trello boards, lists, cards, checklists, Inbox, and Planner through Atlassian's official hosted Trello MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Trello users can ask the agent to inspect boards, organize lists and cards, manage checklists, and triage Inbox or Planner work through their authorized Atlassian account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration can access private Trello content and change shared workspace state under the connected account.

Mitigation: Authorize only the workspaces and permissions needed, and require clear user intent before changes; inspect the current board, list, or card first.

Risk: Setup writes supplied OAuth credentials to the local vault, and stale values can overwrite a rotated refresh token.

Mitigation: Protect stored credentials and rerun setup only with fresh OAuth values. Revoke Trello access when the integration is no longer needed.

## Reference(s):

- [Trello MCP server overview and admin controls](https://github.com/atlassian/trello-mcp-server)
- [Connect Trello to AI assistants](https://support.atlassian.com/trello/docs/connect-trello-to-ai-assistants-with-trello-mcp/)
- [Atlassian Trello MCP usage guide](https://github.com/atlassian/trello-mcp-server/blob/45d274db85936fa23131b25ba41d61780891c37a/skills/trello-use/SKILL.md)
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Natural-language responses and Trello MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool availability follows the live server catalog; actions can read Trello data or change shared board state.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
