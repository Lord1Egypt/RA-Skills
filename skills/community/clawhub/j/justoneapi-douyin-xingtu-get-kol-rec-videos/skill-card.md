## Description: <br>
Call GET /api/douyin-xingtu/get-kol-rec-videos/v1 for Douyin Creator Marketplace (Xingtu) Recommended Videos through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, creator-marketplace analysts, and campaign planning teams use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) recommended video data for a specified KOL ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party JustOneAPI endpoint and should be installed only when the user trusts JustOneAPI and the publisher. <br>
Mitigation: Review the publisher and service documentation before use, and deploy only in environments where this third-party API dependency is acceptable. <br>
Risk: The API token is handled as a query parameter and may be exposed through command lines, request URLs, screenshots, or logs. <br>
Mitigation: Use a least-privilege token when available, avoid sharing command lines or logs that include request URLs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_rec_videos&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_rec_videos&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-rec-videos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, kolId, and optional acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
