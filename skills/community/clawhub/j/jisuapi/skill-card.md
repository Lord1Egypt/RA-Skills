## Description: <br>
用自然语言搜索并调用极速数据 500+ 接口，支持 search to execute 工作流和调用统计查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover JisuAPI tools from natural-language requests, execute selected APIs, and inspect usage or cost statistics without memorizing individual endpoint names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, parameters, and identifiers can be sent to JisuAPI and may include sensitive data. <br>
Mitigation: Use a scoped or limited JISU_API_KEY and review the selected tool plus exact parameters before sending phone numbers or other sensitive identifiers. <br>
Risk: Executed API calls may incur charges under the selected JisuAPI tool's pricing rules. <br>
Mitigation: Check stats, stats_detail, or stats_dashboard regularly and require confirmation before executing paid or ambiguous calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisuapi) <br>
- [JisuAPI Agent documentation](https://www.jisuapi.com/agent/docs/) <br>
- [JisuAPI Agent search API](https://www.jisuapi.com/agent/docs/search) <br>
- [JisuAPI Agent execute API](https://www.jisuapi.com/agent/docs/execute) <br>
- [JisuAPI Agent stats API](https://www.jisuapi.com/agent/docs/stats) <br>
- [JisuAPI Agent tools list](https://www.jisuapi.com/agent/docs/tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; API calls may return third-party service data and usage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
