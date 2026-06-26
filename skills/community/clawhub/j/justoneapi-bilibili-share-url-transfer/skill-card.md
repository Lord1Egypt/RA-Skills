## Description: <br>
Call GET /api/bilibili/share-url-transfer/v1 for Bilibili Share Link Resolution through JustOneAPI with shareUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve shortened Bilibili share links into video and page identifiers through JustOneAPI. It is intended for workflows that need Bilibili link normalization or metadata extraction from shared social media links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JUST_ONE_API_TOKEN is sent in the URL query string and may be exposed through shell history, logs, screenshots, or captured URLs. <br>
Mitigation: Use a scoped, revocable token; pass it through the JUST_ONE_API_TOKEN environment variable; avoid displaying full request URLs; and rotate the token if exposure is suspected. <br>
Risk: Submitted Bilibili share URLs are sent to JustOneAPI for resolution. <br>
Mitigation: Install and use the skill only when the publisher is trusted with the submitted Bilibili share URLs. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_share_url_transfer&utm_content=project_link) <br>
- [Bilibili Share Link Resolution API on ClawHub](https://clawhub.ai/justoneapi/justoneapi-bilibili-share-url-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN credential and a Bilibili shareUrl query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
