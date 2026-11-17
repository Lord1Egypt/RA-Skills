## Description:

Generates vertical miniature build and reveal videos with WeryAI from a text brief or a finished-shot image, using shallow depth of field, push-in camera movement, and lights-on reveal language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn miniature diorama concepts or public finished-shot image URLs into short vertical WeryAI videos. It helps agents expand a user brief into a production prompt, confirm generation parameters, run the bundled video CLI, and return playable video links or clear error details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can upload any readable local file if a local path is supplied as an image.

Mitigation: Prefer public HTTPS image URLs; allow local paths only after reviewing the exact path and receiving explicit user consent.

Risk: Prompts, image URLs, API-key-authenticated requests, and uploaded images are sent to WeryAI.

Mitigation: Do not include secrets or sensitive images; use an isolated environment or short-lived key when strict data control is needed.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/miniature-build-video)
- [WeryAI video generation API](https://api.weryai.com)
- [WeryAI model registry API](https://api-growth-agent.weryai.com)
- [WeryAI local file upload API](https://api-growth-agent.weryai.com/growthai/v1/generation/upload-file)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON command payloads and playable video URLs returned by the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, batch IDs, video URLs, cover URLs, error codes, and error messages from WeryAI.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
