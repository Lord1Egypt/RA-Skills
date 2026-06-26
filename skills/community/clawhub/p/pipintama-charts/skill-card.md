## Description: <br>
Create, fetch, share, or update hosted Pipintama Charts through the MCP server for users who need a line, bar, pie, or radar chart from text or structured values and want a hosted chart link or PNG instead of only prose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, retrieve, share, update, and export hosted Pipintama charts from text or structured numeric data. It is suited for line, bar, pie, and radar charts when the useful answer is a hosted chart link or PNG export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart titles and source data are sent to the Pipintama hosted service. <br>
Mitigation: Avoid confidential, personal, regulated, or internal business data unless the chart is created with private visibility. <br>
Risk: The skill requires a Pipintama API key for MCP actions. <br>
Mitigation: Use a scoped or revocable API key where possible and do not call the service without valid authentication. <br>
Risk: Incorrect chart URLs could mislead users or point them away from the hosted chart. <br>
Mitigation: Return only the documented live Pipintama viewer or PNG export URL patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidk2yoyo/pipintama-charts) <br>
- [Pipintama MCP endpoint](https://api.pipintama.com/mcp) <br>
- [Pipintama MCP health check](https://api.pipintama.com/mcp-health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown with hosted viewer URLs and optional PNG export URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns live Pipintama chart URLs with a short explanation of what the chart shows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
