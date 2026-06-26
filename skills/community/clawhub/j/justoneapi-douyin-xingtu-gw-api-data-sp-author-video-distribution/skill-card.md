## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/author_video_distribution/v1 for Douyin Creator Marketplace (Xingtu) Video Distribution through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Douyin Creator Marketplace (Xingtu) video distribution data for a specified author ID through JustOneAPI, including content performance breakdowns for creator evaluation, campaign planning, and marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is passed in URL query parameters, which can expose credentials through logs or monitoring systems. <br>
Mitigation: Use low-privilege, revocable tokens; avoid environments where request URLs are logged; rotate any token that may have appeared in logs; prefer a version that sends credentials in a secure header if the provider supports it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-author-video-distribution) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_video_distribution&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_video_distribution&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with endpoint details, followed by raw JSON or JSON error details when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; optional platform defaults to SHORT_VIDEO.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
