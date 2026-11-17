## Description:

Generate images and videos, upscale or enhance images, train LoRA styles, and run creative media pipelines with the Krea.ai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertsalgueda](https://clawhub.ai/user/albertsalgueda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative practitioners, and external agent users use this skill to generate images and videos, enhance or upscale existing images, train custom LoRA styles, and automate multi-step media workflows through Krea.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image or video inputs, local files referenced by path, and training image URLs are sent to Krea.ai using the user's Krea API token.

Mitigation: Use only approved non-sensitive inputs, avoid sensitive or internal URLs, and provide tokens through intended runtime mechanisms.

Risk: Generated media, training manifests, cache files, and pipeline state can be written to local directories.

Mitigation: Run from the intended working directory, set output directories deliberately, and review saved files before sharing.

Risk: Skipping URL validation can submit unverified training inputs and waste compute units on unreachable or unintended URLs.

Mitigation: Keep URL validation enabled unless all training inputs are trusted and already verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albertsalgueda/skills/krea)
- [Krea API](https://api.krea.ai)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown guidance with command invocations and local file paths; scripts save generated media files and JSON manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Krea API token; prompts, media inputs, referenced local files, and training image URLs may be sent to Krea.ai.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
