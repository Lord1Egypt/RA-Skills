## Description:

纪念.skill helps create memorial archives from chat logs, photos, interviews, and voice notes, including remembrance text, persona profiles, and optional voice-clone audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terry-cyx](https://clawhub.ai/user/terry-cyx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and families use this skill to assemble memorial archives from personal materials, then generate remembrance narratives, persona guidance, family interview prompts, and optional voice outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process private chat databases, family group metadata, voice messages, photos, and cloned voice models.

Mitigation: Use manually exported, narrowed data where possible, get consent from living subjects and affected participants, run in a separate environment, and delete decrypted WeChat work directories after extraction.

Risk: Voice cloning can be used deceptively or without consent.

Mitigation: Avoid deceptive voice use, keep synthesized audio clearly framed as memorial output, and review generated memorial skills before enabling them.

Risk: Persona outputs may be mistaken for the deceased person's actual views.

Mitigation: Keep remembrance disclosures visible, avoid using the persona for family decisions or estate matters, and phrase responses as memory-based inference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terry-cyx/skills/memorial)
- [Publisher profile](https://clawhub.ai/user/terry-cyx)
- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- [WeChat Windows 3.9.9.43 reference](https://github.com/tom-snow/wechat-windows-versions/releases/tag/v3.9.9.43)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio files]

**Output Format:** [Markdown files, generated skill files, shell command suggestions, configuration notes, and optional WAV audio.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated memorial content should remain labeled as remembrance or inference, not as statements from the subject.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
