## Description: <br>
Call GET /api/douyin-xingtu/get-kol-convert-ability/v1 for Douyin Creator Marketplace (Xingtu) Conversion Analysis through JustOneAPI with kolId and range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call a JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) conversion efficiency and commercial performance data. It supports creator evaluation, campaign planning, and marketplace research using a KOL ID and time range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent to api.justoneapi.com as a URL query parameter, which can expose it through copied URLs, logs, or failed-request diagnostics. <br>
Mitigation: Use a limited or rotatable JUST_ONE_API_TOKEN, avoid sharing request URLs or logs, and rotate the token if a URL may have been exposed. <br>
Risk: The skill calls a third-party analytics API and returns creator or campaign-related marketplace data. <br>
Mitigation: Install only if you trust JustOneAPI and handle returned data according to your organization's data-use and retention policies. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_ability&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_ability&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-convert-ability) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN, kolId, and range; optional acceptCache controls API cache use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
