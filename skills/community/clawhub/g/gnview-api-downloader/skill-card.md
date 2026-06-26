## Description: <br>
Douyin data API toolkit for user data retrieval, Cookie updates, and data collection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnview](https://clawhub.ai/user/gnview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to understand and call documented Douyin API endpoints for video details, user profiles, user post lists, sec_user_id extraction, video analysis, and session Cookie maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented Cookie update endpoint can expose an active Douyin login session if real account cookies are sent to an untrusted or non-HTTPS API backend. <br>
Mitigation: Use only a verified HTTPS service you control, avoid real account cookies, prefer low-risk test accounts, and rotate or log out sessions if a cookie may have been exposed. <br>
Risk: The skill supports collection of Douyin user and video data, including potentially sensitive profile information. <br>
Mitigation: Collect only data you are authorized to access and review applicable platform terms, consent, and privacy requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gnview/gnview-api-downloader) <br>
- [GET_analysis.md](references/GET_analysis.md) <br>
- [GET_douyin_web_fetch_one_video.md](references/GET_douyin_web_fetch_one_video.md) <br>
- [GET_douyin_web_fetch_user_post_videos.md](references/GET_douyin_web_fetch_user_post_videos.md) <br>
- [GET_douyin_web_get_sec_user_id.md](references/GET_douyin_web_get_sec_user_id.md) <br>
- [GET_douyin_web_handler_user_profile.md](references/GET_douyin_web_handler_user_profile.md) <br>
- [POST_hybrid_update_cookie.md](references/POST_hybrid_update_cookie.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References an API base URL configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
