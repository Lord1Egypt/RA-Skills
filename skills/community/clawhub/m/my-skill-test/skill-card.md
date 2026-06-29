## Description: <br>
Queries ZingAPI's creative-list endpoint to find advertising creatives by industry, country or region, channel, keyword, material type, AI tags, time range, and sorting criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[priesttomb](https://clawhub.ai/user/priesttomb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing analysts use this skill to translate natural-language creative-search requests into ZingAPI queries and inspect summarized advertising creative results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ZingAPI credentials and sends signed requests to a production API. <br>
Mitigation: Install it only when ZingAPI access is intended, keep credentials in environment variables, and do not expose access keys in chat, logs, or error output. <br>
Risk: Raw JSON request bodies can send broad or unintended creative-search queries. <br>
Mitigation: Review generated request bodies before execution and use dry-run mode when inspecting the signed request without calling the API. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/priesttomb/my-skill-test) <br>
- [ZingAPI creative-list endpoint](https://openapi.dataideaglobal.com/zingapi/v1/creative/list/{customer_name}) <br>
- [Parameter reference](references/parameters.md) <br>
- [Input mapping](references/input-mapping.md) <br>
- [Response fields](references/response-fields.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a summarized JSON-style result; raw API responses are available when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
