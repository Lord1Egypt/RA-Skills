## Description: <br>
Pipeworx Analyst lets agents query Pipeworx's external gateway across trade, finance, pharma, housing, government contracting, weather, and related data sources using natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to ask natural-language research questions against Pipeworx's remote MCP gateway and discover domain-specific tools for finance, trade, pharma, housing, and government-contracting analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Pipeworx's external MCP gateway and may include sensitive research context. <br>
Mitigation: Use the task-scoped URL when possible and do not send secrets, private documents, customer data, regulated personal information, or nonpublic business strategy. <br>
Risk: The skill includes remember and recall features that can retain information across tool calls. <br>
Mitigation: Use memory only for information intentionally retained and avoid storing confidential or regulated data. <br>
Risk: The gateway has broad data-query scope, including domains where incomplete or stale data could affect decisions. <br>
Mitigation: Review returned data and verify important findings against authoritative sources before relying on them for business, medical, financial, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-analyst) <br>
- [Pipeworx MCP gateway](https://gateway.pipeworx.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Natural-language answers, Markdown guidance, and JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include metadata such as cost breakdown, cache status, next-step suggestions, and error alternatives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
