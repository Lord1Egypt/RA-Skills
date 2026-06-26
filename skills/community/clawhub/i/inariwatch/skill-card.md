## Description: <br>
AI monitoring that fixes your code - query alerts, trigger remediations, rollback deploys, chat with your infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbita-pos](https://clawhub.ai/user/orbita-pos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to monitor production services, investigate alerts, assess remediation risk, and coordinate fixes or rollbacks through InariWatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate high-impact production remediation, rollback, code indexing, and auto-merge workflows. <br>
Mitigation: Install only when InariWatch is trusted for the connected projects, use the least-privilege token available, and require explicit review before approving fixes or rollbacks. <br>
Risk: Incorrect alert or project selection could affect live deployments or code repositories. <br>
Mitigation: Verify exact alert, project, repository, and pull request identifiers before authorizing execution tools. <br>
Risk: The setup flow may run an external npx package. <br>
Mitigation: Prefer manual MCP configuration or inspect the setup package before running the auto-detect command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbita-pos/inariwatch) <br>
- [InariWatch](https://inariwatch.com) <br>
- [InariWatch app](https://app.inariwatch.com) <br>
- [InariWatch MCP endpoint](https://mcp.inariwatch.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an INARIWATCH_TOKEN and produces guidance or actions scoped to the connected InariWatch account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
