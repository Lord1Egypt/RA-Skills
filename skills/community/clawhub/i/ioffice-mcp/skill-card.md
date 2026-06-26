## Description: <br>
Access iOffice workspace and facility data via MCP for buildings, floors, spaces, reservations, visitors, maintenance requests, moves, and mail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized workplace operations users use this skill to connect an agent to their organization's iOffice or Eptura Workplace tenant for facility lookups, room reservations, visitor workflows, maintenance requests, moves, and mail handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live tenant changes affecting facilities, employees, visitors, work orders, moves, reservations, and mail records. <br>
Mitigation: Install it only for authorized iOffice automation, use the least-privileged account available, and review delete, approve, check-in, check-out, archive, and update actions before execution. <br>
Risk: Use outside organizational policy or service terms could expose workplace data or disrupt operations. <br>
Mitigation: Confirm employer authorization before use, avoid bulk extraction or competing-product workflows, and stop using the server if the tenant owner, employer, or service provider objects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/ioffice-mcp) <br>
- [npm package](https://www.npmjs.com/package/ioffice-mcp) <br>
- [Project repository listed by the skill](https://github.com/chrischall/ioffice-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, MCP tool calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples, shell commands, and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed ioffice-mcp MCP server and authorized iOffice tenant credentials.] <br>

## Skill Version(s): <br>
2.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
