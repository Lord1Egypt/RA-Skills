## Description: <br>
Call GET /api/douyin-xingtu/get-kol-link-info/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Metrics through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and campaign planners use this skill to retrieve Douyin Creator Marketplace creator link metrics for a specified KOL ID. It supports creator evaluation, campaign planning, and marketplace research through the JustOneAPI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent as a request query parameter, which can expose credentials through logs or copied URLs. <br>
Mitigation: Use a low-scope, revocable token, avoid sharing full request URLs or logs, and prefer versions that send credentials in an Authorization header or clearly redact URL-based tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-link-info) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_info&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_info&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with a Node.js command and JSON API response payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a kolId query value; optional filters are industryTag and acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
