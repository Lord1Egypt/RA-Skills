## Description:

Video Generation and Editing with HappyHorse models. Supports text2video, image2video (first-frame based), reference2video (multi-image character fusion), and video editing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisyejh](https://clawhub.ai/user/krisyejh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate or edit video with Alibaba HappyHorse models through DashScope, including text-to-video, first-frame image-to-video, multi-reference image-to-video, and instruction-based video editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, media URLs, and selected local image or video files to Alibaba DashScope.

Mitigation: Use it only when that transfer is acceptable, and pass only intended media files.

Risk: Local file arguments can be encoded and submitted as media payloads.

Mitigation: Avoid paths to private documents, environment files, keys, credentials, or unrelated local files.

## Reference(s):

- [HappyHorse Text to Video API Documentation](references/happyhorse-t2v-api-doc.md)
- [HappyHorse Image to Video API Documentation](references/happyhorse-i2v-api-doc.md)
- [HappyHorse Reference to Video API Documentation](references/happyhorse-r2v-api-doc.md)
- [HappyHorse Video Edit API Documentation](references/happyhorse-videoedit-api-doc.md)
- [Alibaba ModelStudio model market](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)
- [ClawHub skill page](https://clawhub.ai/krisyejh/skills/happyhorse-video-gen-edit)
- [ClawHub publisher profile](https://clawhub.ai/user/krisyejh)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and DASHSCOPE_API_KEY; submitted tasks and generated video URLs are documented as valid for 24 hours.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
