## Description:

Local text-to-speech using macOS `say` and ffmpeg for Telegram/Matrix voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zviratko](https://clawhub.ai/user/zviratko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate local text-to-speech audio with macOS `say`, convert it to Opus/Ogg with ffmpeg, and optionally send it as a Telegram or Matrix voice message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local `say` and `ffmpeg` commands to create audio files.

Mitigation: Keep execution permissions limited to a temporary audio folder and review generated shell commands before allowing them to run.

Risk: Generated audio may be sent to a Telegram or Matrix chat when the user invokes messaging behavior.

Mitigation: Review the target chat and generated media path before sending voice messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zviratko/skills/macos-say)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes macOS with local `say` and `ffmpeg` binaries available.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
