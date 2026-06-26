## Description: <br>
Analyze JD.com workflows with JustOneAPI, including product Details, product Comments, and shop Product List. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and ecommerce analysts use this skill to retrieve JD.com product details, product comments, and shop item lists through JustOneAPI when they have the required item or shop identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token can be exposed through command lines, full URLs, proxy logs, or error traces. <br>
Mitigation: Use a scoped or low-privilege token when available, keep JUST_ONE_API_TOKEN out of chat and logs, rotate it periodically, and avoid running the helper in shared or highly logged environments. <br>
Risk: The skill sends user-provided product or shop identifiers to JustOneAPI for JD.com lookups. <br>
Mitigation: Use the skill only when the requested JD.com lookup should be sent to JustOneAPI and provide only the identifiers needed for the selected operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-jd) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation-specific JD.com parameters such as itemId, page, or shopId.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
