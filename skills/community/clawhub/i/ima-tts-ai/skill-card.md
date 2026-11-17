## Description:

Convert text, scripts, and captions into natural voiceovers for videos, explainers, product demos, and social posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and teams use this skill to turn text, scripts, and captions into speech audio URLs for narration, social videos, demos, e-learning, accessibility, and IVR-style voice prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can be configured with a custom base URL, which could expose the IMA API key and submitted text to an untrusted endpoint.

Mitigation: Use the default IMA API host, avoid custom base URLs unless fully trusted, and prefer scoped or test API keys.

Risk: Text submitted for speech synthesis may contain confidential, personal, or regulated content.

Mitigation: Avoid sending sensitive content unless the user is authorized and the provider use is approved for that data.

Risk: The skill stores user preferences and operational logs under the user's OpenClaw directory.

Mitigation: Review retention expectations and delete local preference or log files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-tts-ai)
- [IMA Studio homepage](https://imastudio.com)
- [IMA Claw homepage](https://www.imaclaw.ai/)
- [Volcengine TTS timbre list](https://www.volcengine.com/docs/6561/1257544?lang=zh)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-language status text with audio URL/media result and optional JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_API_KEY; generated speech is returned as a remote audio URL rather than a local download.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact frontmatter and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
