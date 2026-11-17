## Description:

Oasis Audio helps agents create personalized Chinese or English narrated audio with background music from user prompts, selected local context, long content, or recent events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyxu](https://clawhub.ai/user/yuanyxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Oasis Audio to generate personalized audio narration, podcasts, briefings, digests, learning material, or reflective audio. The skill is useful when an audio version of a prompt, document, conversation topic, or recent life context would add value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw/QClaw conversations, memory files, and USER.md profile data to personalize audio.

Mitigation: Install and run it only when local history access is acceptable; use generic generation when personalization is unnecessary.

Risk: Derived personal context may be sent to xplai.ai as part of the composed prompt.

Mitigation: Review the composed prompt before sending and avoid health, financial, legal, relationship, credential, or other sensitive content.

Risk: Prompt details can be retained locally when audit or debug options are enabled.

Mitigation: Leave audit and debug modes off unless local plaintext prompt retention is intended and acceptable.

## Reference(s):

- [Oasis Audio ClawHub Skill Page](https://clawhub.ai/yuanyxu/skills/oasis-audio)
- [xplai.ai](https://www.xplai.ai/)
- [xplai.ai audio generation API endpoint](https://eagle-api.xplai.ai)
- [Audio Modes](artifact/audio_modes.md)
- [Text Architecture](artifact/text_architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated audio status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an audio generation request, an audio ID, status updates, and a final xplai.ai audio page URL when generation succeeds.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
