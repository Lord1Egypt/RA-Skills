## Description:

Ultra-fast speech transcription using iFLYTEK Speed Transcription API for audio files up to 5 hours in about 20 seconds per hour, with support for Chinese, English, and Chinese dialect detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to transcribe MP3 audio through iFLYTEK/XFYUN, including meetings, interviews, lectures, voice notes, call center recordings, legal proceedings, and medical consultations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio and file-path metadata are sent to iFLYTEK/XFYUN for transcription.

Mitigation: Use only with appropriate user consent and data handling approval, and avoid sending audio that should not leave the user's environment.

Risk: The artifact bundles a local .claude/settings.local.json with permissions unrelated to normal transcription use.

Mitigation: Remove .claude/settings.local.json before installing or using the skill.

Risk: The skill description advertises multiple audio formats, while the implementation and security guidance identify MP3-only behavior.

Mitigation: Treat input as MP3-only unless the implementation is updated and retested.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/qingzhe2020/skills/ifly-speed-transcription)
- [iFLYTEK Open Platform](https://www.xfyun.cn/)
- [iFLYTEK speed transcription API documentation](https://console.xfyun.cn/services/ost)
- [iFLYTEK fast transcription service pricing](https://www.xfyun.cn/services/fast_lfasr?target=price)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text transcript or JSON containing task metadata, transcript text, segments, and raw API response; output may be printed or saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET; the implementation uploads audio to iFLYTEK/XFYUN and enforces MP3 input.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
