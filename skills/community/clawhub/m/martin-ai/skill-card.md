## Description:

Complete Venice AI platform access for text generation, web search, embeddings, text-to-speech, speech-to-text, image generation, video creation, upscaling, and AI editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call SkillBoss/HeyBoss-routed AI services for chat, search, embeddings, audio transcription and synthesis, image generation and editing, video generation, and upscaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, media, fetched URL contents, and SKILLBOSS_API_KEY may be sent through the SkillBoss/HeyBoss service path.

Mitigation: Review before installing, avoid sensitive documents, and rotate the API key if it was expected to be used only with Venice or api.skillbossai.com.

Risk: The skill can fetch user-supplied URLs from the local execution environment.

Mitigation: Use trusted public URLs only and avoid internal, private-network, or credential-bearing URLs.

Risk: The server security verdict is suspicious because the skill under-discloses its service routing.

Mitigation: Confirm the intended provider path and data-handling expectations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-ai)
- [SkillBoss API Hub reference](references/api.md)
- [Venice AI](https://venice.ai)
- [Venice API documentation](https://docs.venice.ai)
- [SkillBoss API documentation](https://skillbossai.com/docs)
- [SkillBoss API Hub](https://api.skillbossai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, text responses, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ and SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
