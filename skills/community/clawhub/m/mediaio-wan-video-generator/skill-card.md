## Description:

Generate 1080p AI videos via Media.io Wan (v2.6) using text, images, or reference videos through the Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to call Media.io Wan video-generation APIs for text-to-video, image-to-video, and task-result workflows that require a Media.io API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task IDs, and image URLs are sent to Media.io's remote service.

Mitigation: Avoid confidential prompts or private image URLs unless Media.io processing is approved for the intended use.

Risk: The skill requires a Media.io API key.

Mitigation: Use a dedicated or narrowly scoped key, store it in the API_KEY environment variable, and rotate it if exposed.

Risk: Redirect behavior can affect where API requests are ultimately sent.

Mitigation: Review redirect handling before deployment and restrict redirects in the runtime if required.

## Reference(s):

- [Media.io OpenAPI documentation](https://platform.media.io/docs/)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-wan-video-generator)
- [Bundled Media.io API detail data](artifact/scripts/c_api_doc_detail.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and cURL examples, plus JSON API responses from Media.io.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation APIs return task IDs that are checked with the Task Result API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
