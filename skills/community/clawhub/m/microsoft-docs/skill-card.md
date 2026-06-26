## Description: <br>
Queries official Microsoft Learn documentation for current concepts, tutorials, architecture overviews, configuration guides, limits, and best practices across Azure, .NET, Microsoft 365, Windows, Power Platform, and other Microsoft technologies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdebruin](https://clawhub.ai/user/pdebruin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to search Microsoft Learn and fetch full documentation pages when excerpts are not enough for implementation, configuration, or learning tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation queries and fetched-page requests go to Microsoft Learn and may include user-provided text. <br>
Mitigation: Avoid including private code, secrets, or sensitive internal details in queries unless that text is appropriate to send to the external service. <br>
Risk: The skill depends on Microsoft Learn tooling for searching and fetching official documentation. <br>
Mitigation: Confirm the Microsoft Learn MCP Server is connected before relying on search or fetch results. <br>


## Reference(s): <br>
- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/pdebruin/microsoft-docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text documentation excerpts, fetched page content, and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Microsoft Learn MCP Server; documentation queries and fetched-page requests are sent to Microsoft Learn.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
