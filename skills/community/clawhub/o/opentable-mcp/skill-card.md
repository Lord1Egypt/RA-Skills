## Description: <br>
Manage OpenTable reservations via MCP by searching restaurants, checking availability, booking tables, listing or canceling reservations, and managing favorites through a signed-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage OpenTable restaurant discovery and reservation workflows from the user's signed-in OpenTable browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real booking, modification, favorite, and cancellation actions through a signed-in OpenTable browser session. <br>
Mitigation: Require clear user confirmation before booking, modifying, or canceling reservations, especially when cancellation policies or card holds may apply. <br>
Risk: The skill can access OpenTable profile and reservation data from the signed-in browser session. <br>
Mitigation: Use it only in trusted agent sessions and limit shared reservation or profile details to what the user requested. <br>
Risk: Booking and slot tokens are short-lived, so delayed actions may fail or act on stale availability. <br>
Mitigation: Refresh availability shortly before committing a booking or modification and surface preview details before final action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/opentable-mcp) <br>
- [opentable-mcp npm package](https://www.npmjs.com/package/opentable-mcp) <br>
- [fetchproxy browser extension](https://github.com/chrischall/fetchproxy) <br>
- [OpenTable](https://www.opentable.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP setup snippets and tool-call guidance for reservation workflows.] <br>

## Skill Version(s): <br>
0.14.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
