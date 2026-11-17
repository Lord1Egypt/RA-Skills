## Description:

Provides TikTok creator/video account OAuth authorization, authorized account listing, token lookup, and access token refresh through LinkFox's /tiktokVideo gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators managing TikTok creator video accounts use this skill to start OAuth authorization, list authorized accounts, inspect token status, refresh expired access tokens, and prepare credentials for downstream TikTok video upload workflows.

### Deployment Geography for Use:

Global, with a documented US region option.

## Known Risks and Mitigations:

Risk: The skill handles TikTok creator account metadata and token-management actions.

Mitigation: Install only when LinkFox is trusted for this account data, and avoid displaying full accessToken or refreshToken values.

Risk: The API base URL can be overridden with TIKTOK_VIDEO_API_BASE_URL.

Mitigation: Use the default legitimate HTTPS LinkFox gateway and avoid setting TIKTOK_VIDEO_API_BASE_URL in normal operation.

Risk: Persisted API responses may contain sensitive account, token, or feedback data.

Mitigation: Write persisted outputs only to a private temporary directory and delete them after use.

Risk: The generic response wrapper can execute bundled scripts and capture their outputs.

Mitigation: Use the wrapper only with trusted skill scripts and avoid passing arbitrary scripts.

## Reference(s):

- [TikTok Video Authorization API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-video-auth)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown/plain text guidance with JSON API responses and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token query and refresh scripts mask access and refresh tokens in displayed output; large responses can be saved to private temporary files for selective field extraction.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
