## Description: <br>
Call GET /api/douyin-xingtu/get-kol-touch-distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Touchpoint Distribution through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI for Douyin Creator Marketplace audience touchpoint distribution data for a specified KOL ID, then summarize the segment breakdowns, audience composition, and distribution signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to the API as a URL query parameter, which can expose it through chat transcripts, logs, or copied request URLs. <br>
Mitigation: Use the JUST_ONE_API_TOKEN environment variable, avoid pasting token values into chat or logs, and prefer scoped or short-lived tokens when available. <br>
Risk: The skill sends the requested KOL ID and API token to JustOneAPI and returns backend payloads, including error payloads. <br>
Mitigation: Use the skill only when you trust JustOneAPI for the data being requested and review backend responses before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-touch-distribution) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_touch_distribution&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response data when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; accepts kolId and optional acceptCache query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
