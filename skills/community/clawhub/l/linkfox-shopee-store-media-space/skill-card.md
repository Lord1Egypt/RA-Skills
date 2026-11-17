## Description:

Helps agents upload Shopee MediaSpace images and manage chunked video upload workflows through LinkFox gateway endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, developers, and agents use this skill to upload local JPEG, PNG, or WebP images to Shopee MediaSpace and to initialize, upload, complete, query, or cancel Shopee video uploads for store and product workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because of silent feedback reporting, risky credential handling, and broad persistence and network behaviors.

Mitigation: Review before installing and use the skill only when LinkFox endpoints and the package behavior are trusted.

Risk: The skill can send selected local media, shop identifiers, API responses, phone/SMS onboarding data, and API keys through LinkFox endpoints.

Mitigation: Limit use to intended files and shops, avoid custom gateway environment variables unless the destination is trusted, and prefer temporary or managed credential storage.

Risk: Saved response files may contain sensitive shop or media data.

Mitigation: Store outputs only in approved workspaces, restrict access to the linkfox data directory, and delete saved JSON responses when no longer needed.

Risk: Onboarding guidance may place API keys in shell startup files.

Mitigation: Use a credential manager or temporary environment variable when possible instead of storing API keys in shell profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-media-space)
- [references/api.md](references/api.md)
- [references/onboarding.md](references/onboarding.md)
- [Shopee MediaSpace init_video_upload documentation](https://open.shopee.com/documents/v2/v2.media_space.init_video_upload?module=91&type=1)
- [Shopee MediaSpace upload_image documentation](https://open.shopee.com/documents/v2/v2.media_space.upload_image?module=91&type=1)
- [references/apis/cancel-video-upload.md](references/apis/cancel-video-upload.md)
- [references/apis/complete-video-upload.md](references/apis/complete-video-upload.md)
- [references/apis/get-video-upload-result.md](references/apis/get-video-upload-result.md)
- [references/apis/init-video-upload.md](references/apis/init-video-upload.md)
- [references/apis/upload-image.md](references/apis/upload-image.md)
- [references/apis/upload-video-part.md](references/apis/upload-video-part.md)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands; script outputs are JSON files and stdout JSON or summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are persisted under a linkfox session data directory; responses over 8 KB print a summary unless --inline is used.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
