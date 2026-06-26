## Description: <br>
Query official Microsoft documentation for concepts, tutorials, best practices, working code samples, API signatures, and SDK troubleshooting across Microsoft technologies such as Azure, .NET, Microsoft 365, Windows, Power Platform, Teams, and Dynamics 365. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[partychen](https://clawhub.ai/user/partychen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical users use this skill to find official Microsoft documentation, retrieve page content, and locate working code samples while answering Microsoft product questions or debugging Microsoft-related code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent or user to install or run the external npm package @microsoft/learn-cli. <br>
Mitigation: Verify the package source before installing globally or running with npx, and execute commands only in environments where that package is trusted. <br>
Risk: The trigger scope is broad and may activate for many Microsoft-related questions. <br>
Mitigation: Confirm the relevant Microsoft product or service and narrow searches with specific product names before relying on retrieved results. <br>


## Reference(s): <br>
- [Microsoft Learn documentation](https://learn.microsoft.com/) <br>
- [ClawHub skill page](https://clawhub.ai/partychen/microsoft-learn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, documentation links, excerpts, and optional JSON output from the Microsoft Learn CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include titles, URLs, content excerpts, code samples, and fetched page sections; machine-readable output is available when the CLI is run with --json.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
