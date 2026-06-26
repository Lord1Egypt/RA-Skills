## Description: <br>
Call GET /api/jd/get-item-detail/v1 for JD.com Product Details through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and ecommerce analysts use this skill to retrieve JD.com product detail data by item ID for catalog analysis, product monitoring, and ecommerce research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The vendor API uses token-in-query authentication, so full request URLs can expose the JustOneAPI token in logs, shell history, monitoring, or screenshots. <br>
Mitigation: Use a scoped, revocable JustOneAPI token and avoid running the skill where full URLs may be captured in shared logs, shell history, monitoring, or screenshots. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_detail&utm_content=project_link) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with an inline shell command and JSON API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and a JD.com itemId; documented usage returns a short endpoint-specific summary before raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
