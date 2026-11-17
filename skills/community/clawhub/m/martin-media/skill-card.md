## Description:

Use the SkillBoss API Hub for image generation, video generation, TTS speech, and audio understanding workflows with reusable code templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build multimodal media workflows for generating and understanding images, video, speech, and audio through SkillBoss API Hub. It provides Node.js and REST examples for composing generation, analysis, transcription, and TTS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media inputs may contain sensitive, confidential, regulated, or third-party content that should not be sent to an external service.

Mitigation: Use only media that is approved for SkillBoss processing, avoid secrets and regulated content unless explicitly authorized, and perform human review before production use.

Risk: Publicly hosted media URLs can expose content longer or more broadly than intended.

Mitigation: Prefer private short-lived signed URLs, and delete or revoke hosted media after processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-media)
- [SkillBoss API Hub pilot endpoint](https://api.skillbossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request templates, media URL handling guidance, retry patterns, and environment variable setup.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
