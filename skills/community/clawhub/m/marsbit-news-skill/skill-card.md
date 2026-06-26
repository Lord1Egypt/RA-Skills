## Description: <br>
Fetch MarsBit news and flash data through the hosted MCP route in marsbit-co for latest news, channel lookup, keyword search, detail, related news, and flash updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[domilin](https://clawhub.ai/user/domilin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to retrieve current MarsBit blockchain news, flash updates, news channels, keyword search results, item details, and related stories through a hosted MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MarsBit search terms and news identifiers are sent to the hosted www.marsbit.co MCP endpoint. <br>
Mitigation: Avoid submitting sensitive terms or private identifiers, and disclose the external request path to users before use in restricted environments. <br>
Risk: The skill depends on curl and the availability of a third-party hosted endpoint. <br>
Mitigation: Check connectivity with the tools/list request, handle endpoint errors clearly, and retry later when rate limits or availability issues occur. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/domilin/marsbit-news-skill) <br>
- [MarsBit hosted MCP endpoint](https://www.marsbit.co/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses that summarize JSON returned by MCP tool calls made with curl] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends requests to the hosted MarsBit MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
