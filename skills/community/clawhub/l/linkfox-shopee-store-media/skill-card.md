## Description:

This skill helps agents upload Shopee store media through LinkFox, covering image upload and the full chunked video upload lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce operators use this skill to upload images and videos for Shopee store workflows, including product media preparation and video upload status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox endpoint variables and API keys for Shopee media operations.

Mitigation: Install only in trusted environments, restrict LINKFOX_* endpoint variables, and verify the configured LinkFox API key before use.

Risk: The onboarding flow can request SMS codes and expose billing or payment links.

Mitigation: Only provide SMS codes intentionally for LinkFox onboarding and confirm any paid order before opening or scanning payment links.

Risk: Saved response files may contain shop, media, request, or account details.

Mitigation: Treat local LinkFox response files as sensitive and limit access, retention, and sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-media)
- [Shopee Media upload_image documentation](https://open.shopee.com/documents/v2/v2.media.upload_image?module=130&type=1)
- [Shopee Media cancel_video_upload documentation](https://open.shopee.com/documents/v2/v2.media.cancel_video_upload?module=130&type=1)
- [Shopee Media complete_video_upload documentation](https://open.shopee.com/documents/v2/v2.media.complete_video_upload?module=130&type=1)
- [Shopee Media get_video_upload_result documentation](https://open.shopee.com/documents/v2/v2.media.get_video_upload_result?module=130&type=1)
- [Shopee Media init_video_upload documentation](https://open.shopee.com/documents/v2/v2.media.init_video_upload?module=130&type=1)
- [Shopee Media upload_video_part documentation](https://open.shopee.com/documents/v2/v2.media.upload_video_part?module=130&type=1)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses as local JSON files and may print summaries for larger responses.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
