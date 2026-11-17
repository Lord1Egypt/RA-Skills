## Description:

抖音数据API工具集，包含用户数据获取、Cookie更新等完整API接口。适用于抖音数据采集的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnview](https://clawhub.ai/user/gnview)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a reference for calling Douyin data APIs to fetch video details, user profile information, user post lists, sec_user_id values, and optional analysis results. It also documents configuration and session-cookie update workflows needed by the API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents sending full Douyin login cookies or account session tokens to an external HTTP endpoint.

Mitigation: Do not submit real login cookies or account tokens through the documented endpoint; use a trusted HTTPS service or local processing with clear retention and revocation controls.

Risk: The documented data collection endpoints can retrieve user profile, video, and activity data that may be sensitive or access-restricted.

Mitigation: Use the endpoints only for authorized, lawful collection, minimize requested data, and respect platform access limits and permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gnview/skills/gnview-api-downloader)
- [GET_analysis.md](references/GET_analysis.md)
- [GET_douyin_web_fetch_one_video.md](references/GET_douyin_web_fetch_one_video.md)
- [GET_douyin_web_fetch_user_post_videos.md](references/GET_douyin_web_fetch_user_post_videos.md)
- [GET_douyin_web_get_sec_user_id.md](references/GET_douyin_web_get_sec_user_id.md)
- [GET_douyin_web_handler_user_profile.md](references/GET_douyin_web_handler_user_profile.md)
- [POST_hybrid_update_cookie.md](references/POST_hybrid_update_cookie.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference material with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured base_url for the API service; documented responses are JSON-oriented examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
