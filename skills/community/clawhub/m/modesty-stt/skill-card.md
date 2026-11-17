## Description:

Transcribe audio files using SkillBoss API Hub STT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to transcribe local audio files such as OGG, MP3, WAV, and M4A recordings through SkillBoss API Hub STT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file path to a third-party API instead of limiting itself to verified audio files.

Mitigation: Control which paths agents pass to the script, avoid confidential recordings, and add validation for supported audio formats, regular files, and file size before upload.

Risk: Audio content is sent to SkillBoss API Hub for transcription.

Mitigation: Use the skill only when sending the selected audio to SkillBoss API Hub is acceptable under the user's data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-stt)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcript emitted to stdout with stderr error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and uploads selected audio file contents to SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
