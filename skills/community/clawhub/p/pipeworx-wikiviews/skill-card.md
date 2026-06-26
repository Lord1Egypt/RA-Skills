## Description: <br>
Provides Wikipedia pageview data, including daily views for specific articles, top 1000 articles by date, and total English Wikipedia traffic trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query Wikipedia article, top-page, and project-level pageview metrics through a Pipeworx-hosted MCP endpoint for research, trend analysis, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wikipedia article names and date ranges may be sent to a Pipeworx-hosted MCP endpoint. <br>
Mitigation: Avoid sensitive private context in prompts that invoke the skill and review endpoint use before deployment. <br>


## Reference(s): <br>
- [Pipeworx wikiviews MCP endpoint](https://gateway.pipeworx.io/wikiviews/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-wikiviews) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with JSON configuration and JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Wikipedia pageview counts, rankings, article titles, and aggregate traffic totals from the configured MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
