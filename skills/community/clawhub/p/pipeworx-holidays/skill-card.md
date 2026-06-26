## Description: <br>
Public holidays for 100+ countries - look up by year, check if today is a holiday, or find the next upcoming ones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up public holidays by country and year, check whether today is a holiday, and find upcoming holidays for scheduling, travel planning, payroll, and HR workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday queries are sent to the Pipeworx remote MCP gateway. <br>
Mitigation: Use this skill for non-sensitive public holiday lookups and avoid sending confidential scheduling context unless the remote service is approved for that use. <br>
Risk: The setup example uses an unpinned mcp-remote@latest dependency. <br>
Mitigation: Pin the mcp-remote version in environments that require reproducible installs. <br>


## Reference(s): <br>
- [Pipeworx Holidays](https://pipeworx.io/packs/holidays) <br>
- [Pipeworx Holidays MCP Gateway](https://gateway.pipeworx.io/holidays/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and bash examples; tool responses include holiday dates, names, local names, and fixed-or-floating status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented API example and uses the Pipeworx remote MCP gateway for tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
