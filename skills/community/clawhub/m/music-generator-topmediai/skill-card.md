## Description:

Generate AI music, BGM, or lyrics via TopMediai API with polling for preview and full audio outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topmediai](https://clawhub.ai/user/topmediai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate lyrics, instrumental background music, full songs, query generation task status, and request MP4 conversion through the TopMediai API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and prompts can be sent to a configured base URL that is not the official TopMediai endpoint.

Mitigation: Use a trusted .env and launcher environment, and keep TOPMEDIAI_BASE_URL set to https://api.topmediai.com unless the alternate endpoint is fully trusted.

Risk: Prompts, lyrics, and generation requests are sent to the TopMediai service.

Mitigation: Avoid submitting confidential prompts, personal data, or content that should not leave the local environment.

Risk: Debug mode can print request details in shared or logged environments.

Mitigation: Leave TOPMEDIAI_DEBUG disabled unless debugging in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/topmediai/skills/music-generator-topmediai)
- [TopMediai API base URL](https://api.topmediai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON status objects and text command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit multiple polling events, including lyrics_ready, submitted, preview_ready, full_ready, failed, and timeout.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
