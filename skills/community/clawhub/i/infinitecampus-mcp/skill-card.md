## Description: <br>
This skill helps agents use an Infinite Campus Campus Parent MCP server to access student grades, attendance, assignments, messages, documents, behavior, fees, and food service information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure an MCP server that lets an agent answer questions about a user's own Infinite Campus Campus Parent records, including grades, assignments, attendance, messages, and documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive student records from Infinite Campus through an MCP server. <br>
Mitigation: Install only for accounts and environments intended to access those records, treat outputs as confidential student information, and avoid shared LLM contexts. <br>
Risk: The skill requires credentials or browser-cookie based access to a Campus Parent portal. <br>
Mitigation: Store credentials carefully, restrict access to the MCP configuration, and disable the fetchproxy fallback in headless or CI environments when browser cookie access is not intended. <br>
Risk: Documentation mentions sending messages, while the security guidance says users should clarify whether the package actually supports message sending before account actions. <br>
Mitigation: Confirm supported account actions before enabling any write-like behavior beyond reading records and downloading documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/infinitecampus-mcp) <br>
- [npm package: infinitecampus-mcp](https://www.npmjs.com/package/infinitecampus-mcp) <br>
- [Source repository: infinitecampus-mcp](https://github.com/chrischall/infinitecampus-mcp) <br>
- [fetchproxy fallback extension](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive student-record content returned through the configured MCP server.] <br>

## Skill Version(s): <br>
2.3.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
