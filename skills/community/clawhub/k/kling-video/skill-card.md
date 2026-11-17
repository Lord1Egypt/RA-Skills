## Description:

Generates, animates, and edits short AI videos through Atlas Cloud video models for text-to-video, image-to-video, reference-to-video, and video editing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce short AI-generated videos or edited video clips through Atlas Cloud, including text-to-video, image-to-video, reference-based generation, and natural-language editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, and uploaded media are sent to Atlas Cloud under the user's API key.

Mitigation: Use only content appropriate for Atlas Cloud processing, review media before upload, and confirm the account and API key before generation.

Risk: Generation can incur paid API charges.

Mitigation: Review the model ID, duration, tier, and extra parameters before submitting jobs.

Risk: The helper can call any Atlas Cloud video model, not only the Kling models described in the skill text.

Mitigation: Validate the selected model ID and prefer the documented Kling model IDs for this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/kling-video)
- [Publisher profile](https://clawhub.ai/user/xixihhhh)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud video generation API endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples and downloaded MP4 files from API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY; may send prompts, media URLs, and uploaded media to Atlas Cloud and can incur paid API usage.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
