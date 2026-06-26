## Description: <br>
Search, read, and update Trello boards, lists, cards, checklists, members, and comments through a local MCP wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Trello boards and manage lists, cards, checklists, members, and comments from an MCP-compatible workflow. It is appropriate when the user asks to search, read, or make clearly authorized Trello task workflow updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Trello credentials and can read Trello board, list, card, checklist, member, and comment data. <br>
Mitigation: Install it only with a Trello token scoped to the boards and actions the agent is intended to access. <br>
Risk: Write tools can create, update, move, comment on, and otherwise change shared Trello cards. <br>
Mitigation: Confirm clear user intent and read current board, list, or card state before invoking write tools. <br>
Risk: The artifact installs mcporter without a pinned version by default. <br>
Mitigation: Pin mcporter in environments that require strict supply-chain controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-trello-mcp) <br>
- [mcporter](https://github.com/steipete/mcporter) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [Trello API](https://api.trello.com/1) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON from MCP tool calls with concise text guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAVERICK_TRELLO_MCP_ACCESS_TOKEN and MAVERICK_TRELLO_MCP_API_KEY; write operations may modify Trello board state.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
