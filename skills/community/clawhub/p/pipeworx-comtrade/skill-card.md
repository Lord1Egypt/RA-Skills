## Description: <br>
Retrieve international bilateral trade data, top trading partners, top traded commodities, and country ISO numeric codes through a Pipeworx MCP connector for the UN Comtrade API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query UN Comtrade-style trade data, identify top partner countries or commodities, and look up ISO numeric country codes for trade queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relevant requests may be handled by the remote Pipeworx MCP endpoint. <br>
Mitigation: Limit prompts and query inputs to the trade-data task, and avoid including unrelated secrets, credentials, or confidential context. <br>


## Reference(s): <br>
- [Pipeworx Comtrade ClawHub release](https://clawhub.ai/b-gutman/pipeworx-comtrade) <br>
- [Pipeworx Comtrade MCP endpoint](https://gateway.pipeworx.io/comtrade/mcp) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may depend on availability and behavior of the remote Pipeworx MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
