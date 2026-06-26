## Description: <br>
Search the FBI's Most Wanted list - fugitives, missing persons, and wanted individuals with photos and case details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, researchers, journalists, and analysts use this skill to search or retrieve FBI Wanted person records by keyword, category, pagination, or UID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious and warns that related behavior can include unsandboxed review agents or high-impact write actions. <br>
Mitigation: Install only in a trusted maintainer workspace, confirm targets and credentials before running commands, and disable YOLO-style autoreview behavior when available. <br>
Risk: The skill depends on a remote MCP endpoint and command-line execution to retrieve wanted-person records. <br>
Mitigation: Review the endpoint and MCP client configuration before use, and treat returned case details as external data that should be checked before publication or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-fbiwanted) <br>
- [Pipeworx FBI Wanted pack](https://pipeworx.io/packs/fbiwanted) <br>
- [Pipeworx FBI Wanted MCP endpoint](https://gateway.pipeworx.io/fbiwanted/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented direct MCP request example; MCP client configuration uses mcp-remote via npx.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
