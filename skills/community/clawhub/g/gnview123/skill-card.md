## Description: <br>
Documents API endpoints for extracting and downloading Douyin, TikTok, and Bilibili video, user, comment, live, and collection data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldknife6](https://clawhub.ai/user/goldknife6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and automation agents use this skill to call a configured Douyin TikTok Download API host for social-video metadata, play URLs, comments, live data, ID extraction, and downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to send account cookies and exposes cookie-update endpoints. <br>
Mitigation: Use only dedicated or low-privilege accounts, avoid personal cookies, and deploy with HTTPS and secret handling before sending cookies. <br>
Risk: The skill exposes request-signing token endpoints for Douyin and TikTok API access. <br>
Mitigation: Use signing-token endpoints only with explicit authorization and avoid workflows that bypass service restrictions or access controls. <br>
Risk: The skill depends on a configured API host for extraction and downloading behavior. <br>
Mitigation: Install only when the configured host is trusted, controlled, and appropriate for the intended scraping or downloading functions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goldknife6/gnview123) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown documentation with endpoint paths, parameter tables, examples, and JSON response samples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured API host; some endpoints require user cookies or signing tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
