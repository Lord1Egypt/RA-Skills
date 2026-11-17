## Description:

Fast, accurate automatic speech-to-text transcription supporting 100 languages from URLs or local files via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe audio from a trusted URL or local media file through SkillBoss API Hub and receive transcription text for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio, filenames, and downloaded URL contents are sent to SkillBoss API Hub for transcription.

Mitigation: Use only when that data sharing is acceptable, and avoid sensitive recordings or private files unless data-handling terms have been reviewed.

Risk: Broad URL handling could upload data from private, internal, localhost, cloud metadata, or very large URLs.

Mitigation: Restrict use to trusted public media URLs and add URL validation, media-type checks, and size limits before broader deployment.

Risk: Request construction may be affected by untrusted filenames or option values.

Mitigation: Use JSON-safe request construction and sanitize filenames and language values before invoking the transcription request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-asr)
- [SkillBoss API Hub](https://skillboss.co)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON response with transcription text at .result.text, plus shell command usage and environment-variable configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected audio content, filenames, and downloaded URL contents to SkillBoss API Hub.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-04-15T05:17:39Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
