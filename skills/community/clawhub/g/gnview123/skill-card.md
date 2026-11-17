## Description:

Downloader helps agents reference Douyin, TikTok, and Bilibili API endpoints for extracting video details, play URLs, user posts, collections, comments, live room information, and dynamic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldknife6](https://clawhub.ai/user/goldknife6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as an API reference for collecting social-video metadata, playback links, user profile data, comments, live room details, and related endpoint parameters from Douyin, TikTok, and Bilibili services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Douyin or TikTok cookies may grant account access if sent to an untrusted API host.

Mitigation: Use only a trusted HTTPS API host, avoid primary-account cookies, prefer public-data endpoints or a dedicated low-privilege account, and revoke cookies after use when possible.

Risk: The artifact config leaves the API host unspecified, which can lead users to route requests and credentials to an unknown service.

Mitigation: Review and set the API host before use, and do not submit cookies or other secrets to placeholder, plain HTTP, or untrusted hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goldknife6/skills/gnview123)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code]

**Output Format:** [Markdown API reference with endpoint paths, parameter tables, JSON configuration, and example values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some endpoints may require a configured API host and user-provided platform cookies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
