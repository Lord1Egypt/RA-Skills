## Description:

Translates local media or video URLs through Kre Video Translator, tracks progress, and helps review and export subtitles or subtitled video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skz7s](https://clawhub.ai/user/skz7s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users translate local media or video URLs into reviewed, timed subtitles and optionally burn subtitles into a video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source media, filenames, language settings, prompts, and optional subtitle references are sent to Kre's API.

Mitigation: Confirm the user is comfortable sharing those materials before submitting a translation.

Risk: API keys grant account and translation-task access.

Mitigation: Use the local key setup flow; do not request or paste keys in chat.

Risk: Optional dependency installation may invoke a local package manager or sudo.

Mitigation: Ask for separate approval before using --allow-install-tools.

Risk: Translated subtitles may contain meaning or timing errors.

Mitigation: Review translation completeness, meaning, timing, and line breaks before export.

## Reference(s):

- [Kre Video Translator on ClawHub](https://clawhub.ai/skz7s/skills/kre-video-translator)
- [Kre Video Translator Agent Skill overview](https://kretrans.com/en/video-translation-agent-skill/)
- [Kre Video Translator API](https://kretrans.com/api)
- [Runtime and recovery guidance](references/setup.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Task progress and subtitle JSON; exported SRT subtitles or MP4 video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include word timestamps; video export requires the original video and FFmpeg with libass.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
