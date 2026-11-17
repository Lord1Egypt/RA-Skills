## Description:

Helps agents work with TikTok creator video workflows through LinkFox, including creator profile lookup, product selection, shoppable video precheck, publishing, status checks, and documented upload paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and commerce operators use this skill to guide authenticated TikTok creator video operations, including selecting products, preparing shoppable videos, running prechecks, publishing, and checking publishing status. Authorization is handled by the separate linkfox-tiktok-video-auth skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to LinkFox and TikTok creator credentials and can perform authenticated creator/video operations.

Mitigation: Install only when that access is acceptable, keep tokens out of user-facing summaries, and verify the auth dependency source and version before use.

Risk: A configurable API base URL could route credential-bearing requests to an unintended service.

Mitigation: Use the default LinkFox gateway or set TIKTOK_VIDEO_API_BASE_URL only to a trusted HTTPS LinkFox gateway.

Risk: Publishing videos or sending external feedback can create side effects outside the agent session.

Mitigation: Require explicit user confirmation before publishing a video or sending feedback.

Risk: Saved API responses may contain PII or auth-sensitive data.

Mitigation: Keep response_io.py output outside repositories, delete saved responses promptly, and do not commit response files.

## Reference(s):

- [TikTok Video API Reference](references/api.md)
- [Shoppable Video Large File Upload Solution](references/large-file-upload.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-video)
- [TikTok Shop Partner Center: Large File Upload](https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload)
- [TikTok Shop Partner Center: Get Creator Profile](https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508)
- [TikTok Shop Partner Center: Get Shop Products](https://partner.tiktokshop.com/docv2/page/get-shop-products-202509)
- [TikTok Shop Partner Center: Get Showcase Products](https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405)
- [TikTok Shop Partner Center: Upload Shoppable Video File](https://partner.tiktokshop.com/docv2/page/upload-shoppable-video-file-202505)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local response files for large API responses when the agent uses response_io.py.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
