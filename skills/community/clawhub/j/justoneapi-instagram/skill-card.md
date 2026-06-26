## Description: <br>
Analyze Instagram workflows with JustOneAPI, including user Profile, post Details, and user Published Posts across 5 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Instagram profile, post, user-post, hashtag-post, and reel-search data through JustOneAPI when they have the required identifiers and a JustOneAPI token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and could appear in full request URLs or logs. <br>
Mitigation: Use a scoped or low-risk token when available, avoid logging full request URLs, and rotate the token if it may have appeared in logs. <br>
Risk: The skill sends Instagram usernames, post codes, hashtags, search terms, and authentication credentials to JustOneAPI. <br>
Mitigation: Install and run the skill only if you trust JustOneAPI and are comfortable sharing those request values with the service. <br>
Risk: Returned Instagram content can involve privacy, copyright, platform, or organizational handling requirements. <br>
Mitigation: Handle retrieved social-media content according to applicable privacy, copyright, platform, and organizational rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-instagram) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram&utm_content=project_link) <br>
- [Instagram operations reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API-backed JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operation outputs depend on JustOneAPI responses and user-supplied Instagram usernames, post codes, hashtags, search terms, and pagination tokens.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
