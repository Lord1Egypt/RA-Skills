## Description:

Pollinations.ai API for AI generation and analysis - text, images, videos, audio, vision, and transcription. Use when user requests AI-powered content (text completion, image generation/editing, video generation, audio/TTS, image/video analysis, audio transcription) or mentions Pollinations. Supports 25+ models with OpenAI-compatible endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isaacgounton](https://clawhub.ai/user/isaacgounton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate text, images, video, and audio, edit or analyze media, transcribe audio, and list available models through Pollinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media are sent to external AI services, and model selection may route content to another provider.

Mitigation: Only send content you are comfortable sharing with third parties, and review the selected model's routing.

Risk: Some model requests may use paid billing or account quota.

Mitigation: Check the model's pricing and available quota before making requests.

Risk: The skill uses shell scripts, and runtime permission limits were not verified by the security assessment.

Mitigation: Review the scripts and their execution permissions before running them.

## Reference(s):

- [Pollinations API documentation](https://enter.pollinations.ai/api/docs)
- [Pollinations homepage](https://pollinations.ai)
- [Pollinations ClawHub release](https://clawhub.ai/isaacgounton/skills/pollinations)

## Skill Output:

**Output Type(s):** [Text, JSON, Images, Video, Audio, Analysis, Model listings]

**Output Format:** [Text or JSON responses, generated media files, and model listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and media settings depend on the selected operation and model.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
