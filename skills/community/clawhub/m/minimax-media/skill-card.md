## Description:

MiniMax Media helps agents generate voice, image, video, image-to-video, image-to-image, and music outputs through MiniMax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lqqk7](https://clawhub.ai/user/lqqk7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate MiniMax-powered speech, images, videos, image transformations, and music without managing individual API details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, and generation requests may be sent to the MiniMax API.

Mitigation: Use the skill only for content that is appropriate to send to MiniMax, and avoid sensitive inputs unless the user has approved that provider.

Risk: Media generation can affect API billing and writes files to either the current directory or the requested output path.

Mitigation: Verify API billing expectations and output paths before running generation requests.

Risk: Some MiniMax errors may be returned in Chinese.

Mitigation: Ask the agent to translate errors when needed before retrying or changing inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lqqk7/skills/minimax-media)
- [MiniMax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and media output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated MP3, image, video, or music files in the current directory or at an --output path.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
