## Description: <br>
Call GET /api/jd/get-item-comments/v1 for JD.com Product Comments through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's JD.com product comments endpoint for a given itemId. It supports customer feedback analysis and product research by retrieving comment data such as ratings, timestamps, and reviewer signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token, and token exposure through command lines, shared logs, or captured URLs could allow unauthorized API use. <br>
Mitigation: Use a limited or easily rotated token, avoid sharing command lines or logs that may contain the token, and rotate the token if exposure is suspected. <br>
Risk: Backend error payloads or raw API responses may contain request details or operational data that should not be broadly shared. <br>
Mitigation: Review output before forwarding it and redact tokens, identifiers, or sensitive response details from logs and screenshots. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-jd-get-item-comments) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link) <br>
- [Operations reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN. itemId is required; page is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
